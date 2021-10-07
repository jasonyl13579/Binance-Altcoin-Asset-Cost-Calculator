from telethon import TelegramClient, events
import sys

class telegramClient():
    def __init__(self):
        self.name = None
        self.api_id = None
        self.api_hash = None
        self.target_chat_id = None
    def set_info(self, telegram_info):
        try:
            self.name = telegram_info['name']
            self.api_id = telegram_info['api_id']
            self.api_hash = telegram_info['api_hash']
            self.target_chat_id = telegram_info['target_chat_id']
            self.client = TelegramClient(self.name, self.api_id, self.api_hash)
        except:
            print ("Error while creating telegram client.")
    def get_info(self):
        res = {}
        res['api_id'] = self.api_id
        res['api_hash'] = self.api_hash
        res['target_chat_id'] =self.target_chat_id
        return res
    def send_msg_to_telegram_channel(self, msg):
        with self.client:
            self.client.loop.run_until_complete(self.async_send_msg(msg))
    async def async_send_msg(self, msg):
        #me = await self.client.get_me()
        await self.client.send_message(self.target_chat_id, msg)
    