import asyncio
import os
import time
import logging

import redis
from celery import shared_task
from cryptography.fernet import Fernet
from ping3 import ping
from telegram.error import NetworkError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MonTool.settings')

from app.models import Server, MonUser
from telegram import Bot
from telegram.constants import ParseMode

from celery_tasks.server_ssh import get_conn

EXCEPTIONS = False

TOKEN = os.getenv("TOKEN")
fernet = Fernet(os.getenv("ENCRYPTION_KEY").encode())

bot = Bot(token=TOKEN)

r = redis.Redis(host='redis', port=6379, db=1, decode_responses=True)

logger = logging.getLogger("celery")


async def tg_notification(ip, tg_id):
    """
    Send a Telegram notification about a server being down.
    """
    try:
        await bot.send_message(
            chat_id=tg_id,
            text=f"The server with IP '{ip}' is down! Check immediately!!!'",
            parse_mode=ParseMode.HTML,
        )
        logger.info("Tg notification is sent")
    except (RuntimeError, NetworkError) as error:
        logger.error(f"Error during tg notification delivery - {error}")


@shared_task
def connection_quality() -> None:
    """
    Ping all registered servers and update their connection quality
    status in the database. Send Telegram alert if server is offline.
    """
    server_ips = Server.objects.values_list('server_ip', 'id')
    try:
        for record in server_ips:
            ping_res = ping(record[0])
            if ping_res:
                ping_res *= 1000
                if ping_res <= 30:
                    Server.objects.filter(id=record[1]).update(status="🌟Excellent")
                    logger.info(f"Server(ip: {record[0]}) status is updated to Excellent")
                elif 100 <= ping_res > 30:
                    Server.objects.filter(id=record[1]).update(status="✅Good")
                    logger.info(f"Server(ip: {record[0]}) status is updated to Good")
                elif 1000 <= ping_res > 100:
                    Server.objects.filter(id=record[1]).update(status="⚠️Poor")
                    logger.info(f"Server status(ip: {record[0]}) is updated to ️Poor")
            else:
                Server.objects.filter(id=record[1]).update(status="❌Offline")
                logger.info(f"Server status(ip: {record[0]}) is updated to Offline")
                user_email = Server.objects.get(id=record[1]).owner
                tg_id = MonUser.objects.get(email=user_email).tg_id
                if tg_id:
                    asyncio.run(tg_notification(record[0], tg_id))
    except Exception as error:
        logger.error(f"Error within 'connection_quality' task execution - {error}")


active_monitoring_tasks = {}


@shared_task(bind=True)
def server_stats(self, server_id):
    """
    Collect memory, disk, and CPU stats from a specific server via SSH
    and store the values in Redis. Supports Linux and Windows servers.
    """
    try:
        if server_id in active_monitoring_tasks and active_monitoring_tasks[server_id] != self.request.id:
            return

        creds = Server.objects.filter(id=server_id).values_list('server_ip', 'user_name', 'password').first()
        password = fernet.decrypt(creds[2].encode()).decode()
        ssh = get_conn(creds[0], creds[1], password,)
        try:
            logger.info(server_id)
            if Server.objects.get(id=server_id).os_name == 'Linux':
                stdin, stdout, stderr = ssh.exec_command(
                    "echo $(free -m | awk '/^Mem:/ {print $4}') $(df -BG / | awk 'NR==2 {gsub(/G/, \"\", $4); print $4}') $(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)")
                output = stdout.read().decode().strip()
                free_mem, disk_space, cpu_load = output.split()
                r_key = f"server:{server_id}"
                r.hset(r_key, mapping={
                    'free_memory': free_mem,
                    'free_disk': disk_space,
                    'cpu_load': cpu_load
                })
                logger.info(f"The Linux server(id: {server_id}) stats are saved to Redis")
                r.expire(r_key, 3600)
            elif Server.objects.get(id=server_id).os_name == 'Windows':
                command = (
                    'powershell -Command '
                    '"$mem = [math]::Round((Get-WmiObject Win32_OperatingSystem).FreePhysicalMemory / 1KB); '
                    '$disk = [math]::Round((Get-PSDrive C).Free / 1GB, 2); '
                    '$cpu = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average; '
                    'Write-Output \\"$mem $disk $cpu\\""'
                )
                stdin, stdout, stderr= ssh.exec_command(command)
                output = stdout.read().decode().strip()
                free_mem, disk_space, cpu_load = output.split()
                logger.info(f"{free_mem, disk_space, cpu_load}")
                r_key = f"server:{server_id}"
                r.hset(r_key, mapping={
                    'free_memory': free_mem,
                    'free_disk': disk_space,
                    'cpu_load': cpu_load
                })
                logger.info(f"The Windows server(id: {server_id}) stats are saved to Redis")
                r.expire(r_key, 3600)
        finally:
            ssh.close()
        time.sleep(30)

        if server_id in active_monitoring_tasks and active_monitoring_tasks[server_id] == self.request.id:
            self.server_stats.delay(server_id)
    except Exception as error:
        logger.error(f"Error during 'server_stats' task execution -  {error}")
