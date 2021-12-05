from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
ACCESS_TOKEN = os.environ["91F97TEl4XRd8yG8UJ5QjYfyBTplKVO6OAbdW9fAXbblrvjb/8LMHJ94xBt7MXTyovlzlW9aTzFy8W/PkvlzajWQG1fbRxCdKRTzF+e5F/qbkMUpbkgq7ReSl40ZWR1VNR8i5/cEyk70AJIkUk/OlwdB04t89/1O/w1cDnyilFU="]
SECRET = os.environ["94e8ecf70fc670b4680295658568d45e"]

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
