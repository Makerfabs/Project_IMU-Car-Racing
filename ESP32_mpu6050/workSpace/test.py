#仅测试用
#!/usr/bin/python3
import mpu6050
from machine import Pin,I2C
import machine
import time

i2c = I2C(scl=Pin(5), sda=Pin(4))
accelerometer = mpu6050.accel(i2c)
ints = accelerometer.get_ints()
#初始化传感器
sum_val = 0
for i in range(400):
  acc_data = accelerometer.get_values()
  sum_val+=acc_data['AcX']/16384

error_x = sum_val/400

#平滑滤波器

class avg_fiter():
    def __init__(self, data_list):
        self.data_sum=sum(data_list)
        self.data_list=data_list

    def fit(self, data, len):
        #data是传入的数据,len是平滑的长度
        self.data_sum = self.data_sum - self.data_list[0] + data
        self.data_list.pop(0)
        self.data_list.append(data)
        data = self.data_sum/len
        return data

data_list=[0,0,0,0,0]
'''
for i in range(5):
  acc_data = accelerometer.get_values()
  data_list.append(acc_data['AcX']/16384)
 ''' 
avgfiter = avg_fiter(data_list)
  
#t1 = machine.Timer(2)
#t1.init(period=50, mode=t1.PERIODIC, callback=tcb)
while True:
  #这个速度不能太快
  time.sleep_ms(100)
  acc_data = accelerometer.get_values()
  try:
    temp = avgfiter.fit(acc_data['AcX']/16384-error_x,5)
    print(temp)
    if temp > 0.5 :
        print("0000*")
    elif temp < -0.5 :
        print("*0000")
    elif -0.5 < temp < -0.2  :
        print("0*000")
    elif 0.2 < temp < 0.5 :
        print("000*0")
    elif -0.2 < temp < 0.2 :
        print("00*00")
    

  except:
    print('===========END============')
    break


