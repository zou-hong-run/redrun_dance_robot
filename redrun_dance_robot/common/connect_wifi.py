# 操作esp32引脚
from machine import Pin

# 操作时间 延迟几秒等
import time

# 网络相关的函数
import network

# esp32 引脚2是一颗自带的 led的灯
light = Pin(2,Pin.OUT)
def do_connect():
    # wifi模式
    wlan = network.WLAN(network.STA_IF)
    # 激活
    wlan.active(True)
    print("开始连接...")
    print("连接中...")
    #  连接超时设置
    start_time = time.time()
    if not wlan.isconnected():
        # 自家的wifi名和密码        
        wlan.connect("Xiaomi_A246","zy415415666")
        while not wlan.isconnected():
            # 灯亮
            light.value(1)
            # 延迟一秒
            time.sleep(1)
            # 灯灭
            light.value(0)
            time.sleep(1)
            # 15秒内没连接上就是超时了
            if time.time() - start_time > 15:
                print("wifi连接超时！！！")
                break
        return False
    else:
        print("连接成功！！！！")
        light.value(0)
        # 打印 网络信息
        print("网络配置:",wlan.ifconfig())
        return True