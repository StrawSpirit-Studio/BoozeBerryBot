import psutil
import platform
import wmi
import time


# Функції для отримання системної інформації
def get_processor_name():
    try:
        if platform.system() == "Windows":
            w = wmi.WMI()
            for cpu in w.Win32_Processor():
                return cpu.Name
        else:
            return platform.processor()
    except Exception:
        return "Unknown"

def get_disk_usage():
    try:
        disk = psutil.disk_usage('/')
        return f"{disk.used / (1024 ** 3):.2f} GB / {disk.total / (1024 ** 3):.2f} GB ({disk.percent}%)"
    except Exception:
        return "Disk info not available"

def get_system_uptime():
    try:
        uptime_seconds = psutil.boot_time()
        from datetime import datetime, timedelta
        uptime = datetime.now() - datetime.fromtimestamp(uptime_seconds)
        return str(timedelta(seconds=uptime.total_seconds())).split('.')[0]
    except Exception:
        return "Uptime info not available"

def get_network_usage():
    try:
        net = psutil.net_io_counters()
        sent = net.bytes_sent / (1024 ** 2)
        recv = net.bytes_recv / (1024 ** 2)
        return f"Sent: {sent:.2f} MB, Received: {recv:.2f} MB"
    except Exception:
        return "Network info not available"

def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = "🔌 Charging" if battery.power_plugged else "🔋 Discharging"
            return f"{status} ({battery.percent}%)"
        return "No battery"
    except Exception:
        return "N/A"

def get_gpu_info():
    try:
        if platform.system() == "Windows":
            w = wmi.WMI()
            for gpu in w.Win32_VideoController():
                return f"{gpu.Name} ({gpu.VideoMemoryType})"
        return "GPU info not available"
    except Exception:
        return "N/A"

async def get_telegram_ping(client):
    start_time = time.time()
    await client.get_me()
    return round((time.time() - start_time) * 1000, 2)

def get_network_name():
    try:
        if platform.system() == "Windows":
            w = wmi.WMI()
            for interface in w.Win32_NetworkAdapter(PhysicalAdapter=True):
                if interface.NetEnabled:
                    return interface.NetConnectionID or "Connected"
        return "Connected"
    except Exception:
        return "N/A"

async def ping_handler(client, message):
    if message.text and "$ping" in message.text:
        await message.edit_text(message.text.replace("$ping", "🪄"))
        
        api_ping = await get_telegram_ping(client)
        system_info = platform.uname()
        cpu_name = get_processor_name()
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk_usage = get_disk_usage()
        uptime = get_system_uptime()
        battery_info = get_battery_info()
        network_usage = get_network_usage()
        network_name = get_network_name()

        response = (
            f"**System Statistics**\n"
            f"🖥 **System**: {system_info.system} {system_info.release}\n"
            f"🔧 **Node**: {system_info.node}\n"
            f"💻 **Processor**: {cpu_name}\n"
            f"🔥 **GPU**: {get_gpu_info()}\n"
            f"🔥 **CPU Usage**: {cpu_usage}%\n"
            f"🧠 **Memory**: {memory.used / (1024 ** 3):.2f} GB / {memory.total / (1024 ** 3):.2f} GB\n"
            f"💾 **Swap**: {get_swap_usage()}\n"
            f"💿 **Disk Usage**: {disk_usage}\n"
            f"⏱ **Uptime**: {uptime}\n"
            f"🔋 **Battery**: {battery_info}\n"
            f"📡 **Network Name**: {network_name}\n"
            f"🌐 **Network**: {network_usage}\n"
            f"📶 **Telegram API Ping**: {api_ping} ms\n"
        )
        
        await message.edit_text(response)

def get_swap_usage():
    try:
        swap = psutil.swap_memory()
        return f"{swap.used / (1024 ** 3):.1f} GB / {swap.total / (1024 ** 3):.1f} GB"
    except Exception:
        return "Swap info not available"
