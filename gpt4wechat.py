# encoding:utf-8
from concurrent.futures import ThreadPoolExecutor
import itchat
from itchat.content import *
from EdgeGPT import Chatbot, ConversationStyle
import asyncio,logging,json

@itchat.msg_register([TEXT, SHARING])
def handler_single_msg(msg):
    weChat().handle(msg)
    return None

@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def handler_group_msg(msg):
    weChat().handle_group(msg)
    return None

class weChat():
    def __init__(self):
        self.bot = asyncio.run(Chatbot.create(cookie_path='./cookies.json',proxy="http://127.0.0.1:7890")

    def startup(self):
        # login by scan QRCode
        itchat.auto_login(hotReload=True)
        # start message listener
        itchat.run()

    def handle(self, msg):
        thread_pool.submit(self._do_send, msg['Text'],msg['FromUserName'])

    def handle_group(self, msg):
        if not msg['IsAt']:
            return
        query = msg['Content'][len(msg['ActualNickName']) + 1:]
        if query is not None:
            thread_pool.submit(self._do_send_group, query, msg)

    def send(self, msg, receiver):
        itchat.send(msg, toUserName=receiver)

    def _do_send(self, query,reply_user_id):
        if query == '':
            return
        try:
            reply_text = self.reply(query)
            if reply_text is not None:
                self.send('[Bing]' + reply_text,reply_user_id)
        except Exception as e:
            log.exception(e)

    def _do_send_group(self, query, msg):
        if not query:
            return
        group_id = msg['User']['UserName']
        reply_text = self.reply(query)
        if reply_text is not None:
            self.send('@' + msg['ActualNickName'] + ' ' + reply_text.strip(), group_id)

    def reply(self,queryText):
        reply_text=None
        reply = asyncio.run(self.bot.ask(prompt=queryText, conversation_style=ConversationStyle.precise,
                                         wss_link="wss://sydney.bing.com/sydney/ChatHub"))
        if reply:
            reply_text = reply["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
        return reply_text

if __name__=='__main__':
    log = logging.getLogger('itchat')
    log.setLevel(logging.DEBUG)
    thread_pool = ThreadPoolExecutor(max_workers=8)
    wechat = weChat()
    wechat.startup()

