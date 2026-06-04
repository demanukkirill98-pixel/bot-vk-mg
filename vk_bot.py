import vk_api
import mysql.connector
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

VK_TOKEN = "vk1.a.xie8b5Il8ehezLE3JOCsIBTP3TeENvzecg8d5PRfGiU4RNqHDW9L4bRyz_1M6fz32BegIOViPNJpokpHpKUFuT_E5cKsmFk2sy9PNXTIfZ1BUTs4nUJos7QC1if9IXV4QT_kO3MCbR6b4yHYikjUeb4I9_uZ-YGsdYlY6crCk0dQ1VS2kGGUW49TgweKafX-vognYAwuHxuvHswMC3whaQ"
GROUP_ID = 239035916
ADMIN_VK_IDS = [835770623, 1042002945]

DB_CONFIG = {
    'host': '149.202.88.119',
    'user': 'gs341801',
    'password': 'X0w20ypr9q0B',
    'database': 'gs341801'
}

def set_admin_in_db(player_name, level):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET admin = %s WHERE name = %s", (level, player_name))
    conn.commit()
    result = f"✅ {player_name} получил {level} уровень админа" if cursor.rowcount > 0 else f"❌ Игрок {player_name} не найден"
    cursor.close()
    conn.close()
    return result

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

print("✅ Бот запущен на Bothost")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.message.from_id in ADMIN_VK_IDS:
        text = event.message.text.strip()
        if text.lower().startswith('/setadmin'):
            parts = text.split()
            if len(parts) == 3 and parts[2].isdigit() and 1 <= int(parts[2]) <= 13:
                vk.messages.send(peer_id=event.message.peer_id, message=f"🔄 Выдаю {parts[1]} {parts[2]} уровень...", random_id=random.randint(1, 10**9))
                vk.messages.send(peer_id=event.message.peer_id, message=set_admin_in_db(parts[1], int(parts[2])), random_id=random.randint(1, 10**9))
