import discord
import os

# 获取并解析环境变量
token = os.environ['DISCORD_TOKEN']
raw_source_ids = os.environ.get('SOURCE_CHANNEL_IDS', '')
source_channel_ids = [int(cid.strip()) for cid in raw_source_ids.split(",") if cid.strip()]
target_channel_id = int(os.environ['TARGET_CHANNEL_ID'])

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'登录为: {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.channel.id in source_channel_ids:
            target_channel = self.get_channel(target_channel_id)
            if target_channel:
                # 支持纯文本+附件
                content = message.content
                files = []
                # 下载并转发所有附件（比如图片）
                for attachment in message.attachments:
                    import aiohttp, io
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            data = await resp.read()
                            f = discord.File(io.BytesIO(data), filename=attachment.filename)
                            files.append(f)
                await target_channel.send(content, files=files)

client = MyClient()
client.run(token)
