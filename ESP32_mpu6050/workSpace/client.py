# Upload the slanted value of MPU to PC by UDP and test with udp_server.py
#wifi
import socket
import time
import wifi
BUFSIZE = 1024

#mpu
import mpu6050
from machine import Pin,I2C
import machine

#mpu init
i2c = I2C(scl=Pin(5), sda=Pin(4))
accelerometer = mpu6050.accel(i2c)
ints = accelerometer.get_ints()

#init sensor
sum_val = 0
for i in range(400):
  acc_data = accelerometer.get_values()
  sum_val+=acc_data['AcX']/16384

error_x = sum_val/400

sum_val = 0
for i in range(400):
  acc_data = accelerometer.get_values()
  sum_val+=acc_data['AcY']/16384

error_y = sum_val/400

sum_val = 0
for i in range(400):
  acc_data = accelerometer.get_values()
  sum_val+=acc_data['AcZ']/16384

error_z = sum_val/400

#avg filter

class avg_fiter():
    def __init__(self, data_list):
        self.data_sum=sum(data_list)
        self.data_list=data_list

    def fit(self, data, len):
        self.data_sum = self.data_sum - self.data_list[0] + data
        self.data_list.pop(0)
        self.data_list.append(data)
        data = self.data_sum/len
        return data

data_list_x=[0,0,0,0,0]
data_list_y=[0,0,0,0,0]
data_list_z=[0,0,0,0,0]
avgfiter_x = avg_fiter(data_list_x)
data_list_x=[0,0,0,0,0]
avgfiter_y = avg_fiter(data_list_y)
data_list_x=[0,0,0,0,0]
avgfiter_z = avg_fiter(data_list_z)





def main():
  wifi.connect()
  ip_port = ('192.168.1.125', 80)
  client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  while True:
    #z is wrong, isn't used.
    xyz = {"x":0,"y":0,"z":0}
    time.sleep_ms(10)
    acc_data = accelerometer.get_values()
    try:
      temp = avgfiter_x.fit(acc_data['AcX']/16384-error_x,5)
      temp_int = int(temp*10)
      xyz["x"] = temp_int
      temp = avgfiter_y.fit(acc_data['AcY']/16384-error_y,5)
      temp_int = int(temp*10)
      xyz["y"] = temp_int
      temp = avgfiter_z.fit(acc_data['AcZ']/16384-error_z,5)
      temp_int = int(temp*10)
      xyz["z"] = temp_int

      print(xyz)

    except:
      print('===========END============')
      break

    text = str(xyz)
    client.sendto(text.encode('utf-8'),ip_port)
    data,server_addr = client.recvfrom(BUFSIZE)
    #print('client recvfrom ',data,server_addr)
    pass

if __name__ == '__main__':
    main()
    # print(__name__)




