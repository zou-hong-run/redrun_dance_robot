# 导入Microdot
from lib.microdot import Microdot,send_file,Request
from lib.microdot_websocket import with_websocket
from lib.microdot_cors import CORS
# 连接wifi
from common.connect_wifi import do_connect
from common.servo import Servo
import time
# 导入引脚
from machine import Pin


# 不加报错
Request.socket_read_timeout = None

# 对应四个电机 从左上角顺时针排序
s1 = Servo(Pin(15))
s2 = Servo(Pin(17))
s3 = Servo(Pin(25))
s4 = Servo(Pin(27))
# 复位
s1.write_angle(0)
s2.write_angle(180-0)
s3.write_angle(180-0)
s4.write_angle(0)
# esp32 引脚2是一颗自带的 led的灯
light = Pin(2,Pin.OUT)

# 开始连接wifi
do_connect()
# 实例化这个类
app = Microdot()
cors = CORS(app, allowed_origins=['*'],allow_credentials=True)
# get请求返回一个网页
@app.route('/')
def index(request):
    return send_file('public/index.html')

# @app.route('/music')
# def index(request):
#     return send_file('bg.mp3')

# 使用@with_websocket生成websocket服务
@app.route('/move')
@with_websocket
def echo(request, ws):
    while True:
        # 拿到客户端发送的数据
        data = ws.receive()
        print(data,type(data))
        s1.write_angle(int(data))
        s2.write_angle(180-int(data))
        s3.write_angle(180-int(data))
        s4.write_angle(int(data))    
        ws.send("移动："+(data))
        

# 启动后指示灯闪烁
def blink():
    for i in range(5):
        light.value(int(not light.value()))
        time.sleep(1)
blink()

# 端口号为5000
app.run(host='0.0.0.0', port=5000, debug=False, ssl=None)