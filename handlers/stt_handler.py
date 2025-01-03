from faster_whisper import WhisperModel
import os
import torch
import asyncio
from config import FFMPEG_PATH, whisper_presets, beam_size, best_of, temperature
from datetime import datetime
import logging

logger = logging.getLogger("whisper")

class WhisperManager:
    _instance = None
    _model = None 
    _model_size = None 
    
    @classmethod
    def get_instance(cls, model_size="turbo"):
        if cls._instance is None or cls._model_size != model_size:
            cls._instance = cls(model_size)
        return cls._instance
    
    def __init__(self, model_size):
        self._model_size = model_size
        self._model = None
        self.MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "packages", "models")
        self.TEMP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp_files")
        os.makedirs(self.MODELS_DIR, exist_ok=True)
        os.makedirs(self.TEMP_DIR, exist_ok=True)
    
    async def load_model(self, message=None):
        
        if self._model is None:
            try:
                if message:
                    await message.edit_text("🔄 Завантаження моделі Whisper...")
                
                device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"Завантаження моделі {self._model_size} на {device}")
                if self._model_size is None:
                    raise ValueError("model_size cannot be None")
                    
                self._model = WhisperModel(
                    str(self._model_size),
                    device=device,
                    download_root=self.MODELS_DIR,
                    compute_type="float16" if device == "cuda" else "float32"
                )
                
                if message:
                    await message.edit_text("✅ Модель успішно завантажена!")
                logger.info("Модель Whisper завантажена")
            except Exception as e:
                logger.error(f"Помилка завантаження моделі: {e}")
                if message:
                    await message.edit_text(f"❌ Помилка завантаження моделі: {e}")
                raise e
    
    async def transcribe(self, audio_path, language=None, quality=whisper_presets, message=None):
        if self._model is None:
            raise Exception("Модель не завантажена")
        
        presets = {
            'fast': {'beam_size': 1, 'best_of': 1, 'temperature': 0.0},
            'normal': {'beam_size': 5, 'best_of': 5, 'temperature': 0.0},
            'accurate': {'beam_size': 10, 'best_of': 10, 'temperature': 0.2},
            'custom': {'beam_size': beam_size, 'best_of': best_of, 'temperature': temperature}
        }
        
        params = presets.get(quality, presets[whisper_presets])
        
        segments, info = self._model.transcribe(
            audio_path,
            language=language,
            **params,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=400
            ),
            condition_on_previous_text=False,
            initial_prompt=None 
        )
        
        return segments, info

async def stt_handler(client, message):
    voice_ogg = None
    voice_wav = None
    try:
        # Перевірка команди та мови
        if message.text and "$stt" in message.text:
            command_parts = message.text.split()
            language = command_parts[1] if len(command_parts) > 1 else "uk"
            await message.edit_text("🎯 Ініціалізація...")
        else:
            await message.edit_text("🛑 Використовуйте команду $stt [код_мови]")
            return
        # Перевірка чи встановлено FFMPEG
        if not os.path.isfile(FFMPEG_PATH):
            if message:
                await message.edit_text(f"`FFMPEG не знайдено.` Будь ласка, переконайтеся, що `FFMPEG` встановлено в директорію `{FFMPEG_PATH}`")
            return

        # Перевірка відповіді на голосове повідомлення
        if not message.reply_to_message or not message.reply_to_message.voice:
            await message.edit_text("🛑 Відповідайте на голосове повідомлення")
            return

        # Ініціалізація менеджера Whisper
        whisper = WhisperManager.get_instance()
        await whisper.load_model(message)

        # Завантаження голосового повідомлення
        voice = message.reply_to_message.voice
        file_size = voice.file_size / (1024 * 1024)  # Розмір в МБ
        
        await message.edit_text(f"⏳ Завантаження голосового повідомлення ({file_size:.1f}MB)...")
        
        voice_ogg = os.path.join(whisper.TEMP_DIR, f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg")
        voice_wav = voice_ogg.replace(".ogg", ".wav")
        
        await client.download_media(voice.file_id, file_name=voice_ogg)
        
        if not os.path.exists(voice_ogg):
            raise Exception("❌ Помилка завантаження голосового повідомлення")
        
        # Конвертація в WAV
        await message.edit_text("🔄 Конвертація аудіо...")
        process = await asyncio.create_subprocess_exec(
            FFMPEG_PATH, "-i", voice_ogg, "-ar", "16000", "-ac", "1", voice_wav,
            stderr=asyncio.subprocess.PIPE
        )
        await process.communicate()
        
        if process.returncode != 0:
            raise Exception("❌ Помилка конвертації")

        # Розпізнавання
        await message.edit_text("🧠 Розпізнавання мовлення...")
        segments, _ = await whisper.transcribe(voice_wav, language, message=message)
        
        # Формування результату
        transcription = " ".join(segment.text for segment in segments)
        
        result = (
            f"🎯 **Розпізнаний текст:**\n{transcription}\n\n"
        )
        
        await message.edit_text(result)

    except Exception as e:
        error_text = f"❌ Помилка: {str(e)}"
        if message in locals():
            await message.edit_text(error_text)
        else:
            await message.edit_text(error_text)
        logger.error(f"Помилка STT: {e}", exc_info=True)
    
    finally:
        # Очищення тимчасових файлів
        for file in [voice_ogg, voice_wav]:
            if file and os.path.exists(file):
                os.remove(file)