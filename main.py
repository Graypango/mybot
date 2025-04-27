import discord
import os
import requests

TOKEN = os.environ['DISCORD_TOKEN']

raw_ids = os.environ.get('SOURCE_CHANNEL_IDS', '')
SOURCE_CHANNEL_IDS = [int(i.strip()) for i in raw_ids.split(',') if i.strip()]
TARGET_CHANNEL_ID = int(os.environ['TARGET_CHANNEL_ID'])

N8N_WEBHOOK_URL = os.environ['N8N_WEBHOOK_URL']   # 用环境变量获取

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'登录为: {self.user}')

    async def on_message(self, message):
        if message.channel.id in SOURCE_CHANNEL_IDS:
            payload = {
                "content": message.content,
                "author": str(message.author),
                "channel_id": message.channel.id,
                "attachments": [a.url for a in message.attachments]
            }
            try:
                requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
                print("已推送到n8n:", payload)
            except Exception as e:
                print("推送n8n出错:", e)

            target_channel = self.get_channel(TARGET_CHANNEL_ID)
            if target_channel:
                await target_channel.send(f'转发: {message.content}')

client = MyClient()
client.run(TOKEN)
