#%%
import websocket
import threading
import json
from time import time, sleep
from datetime import date, datetime

class TimeTester:
    def __init__(self):
        self.min_diff = 999

    def receive(self, message):
        message = json.loads(message)
        action = message.get("action")
        table = message.get("table")
        data = message.get("data")

        if action == "insert" and table == "trade":
            r = data[-1]

            remote_date = datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
            local_date = datetime.utcnow()

            delta = local_date - remote_date

            delta_seconds = delta.total_seconds()

            if delta_seconds < self.min_diff:
                self.min_diff = delta_seconds

            # print(data[-1]["timestamp"])
            # self.write(data)

tt = TimeTester()


url = "wss://www.bitmex.com/realtime?subscribe=trade:XBTUSD"
ws = websocket.WebSocketApp(url, on_message=tt.receive)
wst = threading.Thread(target=lambda: ws.run_forever())
wst.daemon = True
wst.start()

sleep(3)
if not ws.sock or not ws.sock.connected:
    raise websocket.WebSocketTimeoutException()


while True:
    print tt.min_diff
    sleep(5)
