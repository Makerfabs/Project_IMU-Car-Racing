# Project_IMU-Car-Racing

```
/*
Version:		V1.1
Author:			Vincent
Create Date:	2020/8/6
Note：
```

![main](md_pic/main.gif)



[toc]

# Overview

[Makerfabs home page](https://www.makerfabs.com/)

[Makerfabs Wiki](https://makerfabs.com/wiki/index.php?title=Main_Page)



Using the MPU6050 gyroscope to obtain its own tilt Angle to simulate the arrow keys, the control of a simple Python racing game.Realized the car up and down left and right movement. This project is implemented entirely in Python.

![oversee](md_pic/oversee.png)

# ESP32 IMU Module V1.1

## Product link ：[ESP32 6- Axis IMU](https://www.makerfabs.com/esp32-6-axis-imu.html) 

## Detail Info: [ESP32_IMU_Module](https://github.com/Makerfabs/ESP32_IMU_Module)

The Makerfabs IMU Module features the 6-axis MPU-6050 MEMS sensor from InvenSense. Each of these 6DoF IMU feature an ESP32 with a MPU-6050 which contains a 3-axis gyroscope as well as a 3-axis accelerometer. The MPU-6050 uses 16-bit analog-to-digital converters (ADCs) for digitizing 6 axes. By combining a MEMS 3-axis gyroscope and a 3-axis accelerometer on the same silicon die together with an onboard Digital Motion Processor™ (DMP™) .It can be used as a helicopter/quadcopter.

# STEPS

The car-racing game is change from : [sipspatidar/car_racing](https://github.com/sipspatidar/car_racing)

## Prepare And Burn ESP32_IMU

**If you have any questions，such as how to install the development board, how to download the code, how to install the library. Please refer to :[Makerfabs_FAQ](https://github.com/Makerfabs/Makerfabs_FAQ)**

- Connect esp32 to PC .
- You need change some code like wifi config in "/Project_IMU-Car-Racing/ESP32_mpu6050/workSpace/wifi.py"

```python
SSID = "Makerfabs"      #Modify here with SSID
PASSWORD = "20160704"   #Modify here with PWD
```

- Get your PC Lan IP, like use "ipcongfig" command, and change code in "/Project_IMU-Car-Racing/ESP32_mpu6050/workSpace/client.py"

![ipconfig](md_pic/ipconfig.png)

```python
def main():
  wifi.connect()
  ip_port = ('192.168.1.125', 80)
  client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
```



- Use uPyCraft upload all file in "/Project_IMU-Car-Racing/ESP32_mpu6050/workSpace"



## Prepare Upper Computer Software

- Install pygame library, like use : pip install pygame.
- Change code in car_racing.py , change ip port to your own Lan IP.

```python
#udp init
import socket
BUFSIZE = 1024
ip_port = ('192.168.1.125', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
server.bind(ip_port)
```

- Use command line run: python /Project_IMU-Car-Racing/car_racing_py/car_racing.py

![step1](md_pic/step1.jpg)

- Click GO and reset esp32.

![step2](md_pic/step2.jpg)

- Wait seconds , esp32 need connect wifi.
- Then game start.

![car_game](md_pic/imu_car.gif)

- Tilting the IMU left and right to control the car position.
- Tilting the IMU back and forth controls car speed.

# Code Explain

## UDP

In [computer networking](https://en.wikipedia.org/wiki/Computer_network), the **User Datagram Protocol** (**UDP**) is one of the core members of the [Internet protocol suite](https://en.wikipedia.org/wiki/Internet_protocol_suite). The protocol was designed by [David P. Reed](https://en.wikipedia.org/wiki/David_P._Reed) in 1980 and formally defined in [RFC](https://en.wikipedia.org/wiki/RFC_(identifier)) [768](https://tools.ietf.org/html/rfc768). With UDP, computer applications can send messages, in this case referred to as *[datagrams](https://en.wikipedia.org/wiki/Datagram)*, to other hosts on an [Internet Protocol](https://en.wikipedia.org/wiki/Internet_Protocol) (IP) network. Prior communications are not required in order to set up [communication channels](https://en.wikipedia.org/wiki/Communication_channel) or data paths.

UDP uses a simple [connectionless communication](https://en.wikipedia.org/wiki/Connectionless_communication) model with a minimum of protocol mechanisms. UDP provides [checksums](https://en.wikipedia.org/wiki/Checksum) for data integrity, and [port numbers](https://en.wikipedia.org/wiki/Port_numbers) for addressing different functions at the source and destination of the datagram. It has no [handshaking](https://en.wikipedia.org/wiki/Handshaking) dialogues, and thus exposes the user's program to any [unreliability](https://en.wikipedia.org/wiki/Reliability_(computer_networking)) of the underlying network; there is no guarantee of delivery, ordering, or duplicate protection. If error-correction facilities are needed at the network interface level, an application may use [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) (TCP) or [Stream Control Transmission Protocol](https://en.wikipedia.org/wiki/Stream_Control_Transmission_Protocol) (SCTP) which are designed for this purpose.

UDP is suitable for purposes where error checking and correction are either not necessary or are performed in the application; UDP avoids the overhead of such processing in the [protocol stack](https://en.wikipedia.org/wiki/Protocol_stack). Time-sensitive applications often use UDP because dropping packets is preferable to waiting for packets delayed due to [retransmission](https://en.wikipedia.org/wiki/Retransmission_(data_networks)), which may not be an option in a [real-time system](https://en.wikipedia.org/wiki/Real-time_system).[[1\]](https://en.wikipedia.org/wiki/User_Datagram_Protocol#cite_note-kuroseross-1)

## PC

### udp client.py

This is a demo used to test whether udp protocol can be transmitted through.This is the sender.If you can't communicate, you can debug your IP with this demo.

```python
#Need socket to create a udp link
import socket
BUFSIZE = 1024
#set UDP
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    #Set server port
    ip_port = ('192.168.1.125', 80)
    #Send encode string data to server by udp
    client.sendto("""{'x': 2, 'z': -8, 'y': 4}""".encode('utf-8'),ip_port)
 
	#UDP need reply and then send anoter msg.
    data,server_addr = client.recvfrom(BUFSIZE)
    print('client recvfrom ',data,server_addr)
 
client.close()
```

### udp_server.py

Udp test demo server part.

```python
import socket
BUFSIZE = 1024
#Set server port
ip_port = ('192.168.1.125', 80)
#Set udp
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
#Set bind mod
server.bind(ip_port)
while True:
    #Receive a udp package
    data,client_addr = server.recvfrom(BUFSIZE)
    #Decode receive msg.
    data_str = data.decode('utf-8').encode('utf-8')
    #Change string to json object
    xyz = eval(data_str)
    print('server receive', data)
    #print x angle and y angle
    print(xyz["x"])
    print(xyz["y"])
    #print("**************")
 	
    #UDP need a ack to send next package
    server.sendto(data.upper(),client_addr)
 
server.close()
```



### car_racing.py

Main file of the game.

- UDP setting.

```python
#udp init
import socket
BUFSIZE = 1024
ip_port = ('192.168.1.125', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
server.bind(ip_port)
```

- Game parameter Settings and initialization settings.

```python
#Pygame provides the framework for games, such as window display.
import pygame
import time
import random 

pygame.init()
#Game window dimensions
display_width = 742
display_height = 600

#Color RGB
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)

#Car dimensions
car_width = 50
car_height = 100

#Display game window
gameDisplay = pygame.display.set_mode((display_width,display_height))
#Set the title of the game window
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

#Pictures of game objects
logoImg = pygame.image.load("logo11-190x63.png")
carImg = pygame.image.load("car1.png") #load the car image
car2Img = pygame.image.load("car2.png")
bgImg = pygame.image.load("back2.jpg")
crash_img = pygame.image.load("crash.png")
```

- Game entry interface.Displays the title and hints of the game, and has two buttons: Start and Exit.

```python
#Game start menu
def intro():
	intro = True
	menu1_x = 200
	menu1_y = 400
	menu2_x = 500
	menu2_y = 400
	menu_width = 100
	menu_height = 50
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
        #Set the game window icon
		pygame.display.set_icon(carImg)
		
        #Fill the game screen in white
		gameDisplay.fill(white)

		#The top left corner displays the company logo.
		gameDisplay.blit(logoImg,(0,0))

		#Display the game name and description on the game screen.
		message_display("CAR RACING",100,display_width/2,display_height/2)
		message_display("Press Go and rst esp32",30,display_width/2,display_height/2 + 200)

		#Draw two rectangles as buttons and label the text.
		pygame.draw.rect(gameDisplay,green,(menu1_x,menu1_y,menu_width,menu_height))
		pygame.draw.rect(gameDisplay,red,(menu2_x,menu2_y,menu_width,menu_height))
		message_display("Go",40,menu1_x+menu_width/2,menu1_y+menu_height/2)
		message_display("Exit",40,menu2_x+menu_width/2,menu2_y+menu_height/2)

		#Set the mouse object and click action for PyGame.
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		
		#Click logic, click Go to start the game, and click Exit to close the window.
		if menu1_x < mouse[0] < menu1_x+menu_width and menu1_y < mouse[1] < menu1_y+menu_height:
			pygame.draw.rect(gameDisplay,blue,(menu1_x,menu1_y,menu_width,menu_height))
			if click[0] == 1:
				intro = False
		if menu2_x < mouse[0] < menu2_x+menu_width and menu2_y < mouse[1] < menu2_y+menu_height:
			pygame.draw.rect(gameDisplay,blue,(menu2_x,menu2_y,menu_width,menu_height))
			if click[0] == 1:
				pygame.quit()
				quit()
		
		#refresh
		pygame.display.update()
		clock.tick(50)
```

- Some control functions.

```python
#Statistics of highest score
def highscore(count):
	font = pygame.font.SysFont(None,20)
	text = font.render("Score : "+str(count),True,black)
	gameDisplay.blit(text,(0,0))

#Display obstacle
def draw_things(thingx,thingy,thing):
	gameDisplay.blit(thing,(thingx,thingy))
	
#Display car
def car(x,y):
	gameDisplay.blit(carImg,(int(x),int(y)))

#Set the text object
def text_objects(text,font):
	textSurface = font.render(text,True,black)
	return textSurface,textSurface.get_rect()
	
#Text display
def message_display(text,size,x,y):
	font = pygame.font.Font("SourceCodePro.ttf",size)
	text_surface , text_rectangle = text_objects(text,font)
	text_rectangle.center =(int(x),int(y))
	gameDisplay.blit(text_surface,text_rectangle)
    
#Crashed display
def crash(x,y):
	#Display a picture of the crash at coordinates
	gameDisplay.blit(crash_img,(x,y))
	#Display text message crashed
	message_display("You Crashed",115,display_width/2,display_height/2)
	pygame.display.update()
	time.sleep(2)
	#for restart the game
	gameloop() 
```

- Game main loop.

```python
def gameloop():
	#Road set
	bg_x1 = int((display_width/2)-(741/2))
	bg_x2 = int((display_width/2)-(741/2))
	bg_y1 = 0
	bg_y2 = -600
	road_start_x =  (display_width/2)-210
	road_end_x = (display_width/2)+210

	#Rolling speed setting
	bg_speed = 8
	bg_speed_change = 0

	#Car position setting
	car_x = ((display_width / 2) - (car_width / 2))
	car_y = (display_height - car_height)
	car_x_change = 0

	#Red cars list init
	thing_list = []
	for i in range(10):
		thing = {}
		#Create a random red car
		thing["x"] =  random.randrange(road_start_x,road_end_x-car_width)
		thing["y"] =  -600
		thing_list.append(thing)
	print(thing_list)

	#Obstacle parameter setting
	thingw = 50
	thingh = 100
	thing_speed = 12
	count=0
	gameExit = False
	
	while not gameExit:
		#Get the UDP package from the terminal
		data,client_addr = server.recvfrom(BUFSIZE)
		#Return response information
		server.sendto(data.upper(),client_addr)
		print('server reserve:',data)
		#Decoding the message
		data_str = data.decode('utf-8').encode('utf-8')
		#Strings are parsed into dictionary objects
		xyz = eval(data_str)
		#Parse the x and y angles
		imu_direct_x = int(xyz["x"])
		imu_direct_y = 0 - int(xyz["y"])

		#Key board logic
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
				pygame.quit()
				quit()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					car_x_change = -5
				elif event.key == pygame.K_RIGHT:
					car_x_change = 5
				elif event.key == pygame.K_UP:
					car_y_change = 5
				elif event.key == pygame.K_DOWN:
					car_y_change = -5
				
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					car_x_change = 0
			
		#Udp control car location
		car_x = (display_width/2) + 200 * imu_direct_x / 10
		
		#Crash logic
		if car_x > road_end_x-car_width:
			crash(car_x,car_y)
		if car_x < road_start_x:
			crash(car_x-car_width,car_y)

		#Game hard level
		level = int(count / 200)
		if level > 9:
			level = 9
		
		#Car crash logic
		for i in range(level + 1):
			if car_y < thing_list[i]["y"] + thingh and car_y > thing_list[i]["y"] - thingh :
				if car_x >= thing_list[i]["x"] and car_x <= thing_list[i]["x"]+thingw:
					crash(car_x-25,car_y-car_height/2)
				if car_x+car_width >= thing_list[i]["x"] and car_x+car_width <= thing_list[i]["x"]+thingw:
					crash(car_x,car_y-car_height/2)			

		#Display background
		gameDisplay.fill(green) #display white background
		
		#Display road
		gameDisplay.blit(bgImg,(int(float(bg_x1)),int(float(bg_y1))))
		gameDisplay.blit(bgImg,(bg_x2,bg_y2))
		car(car_x,car_y) #display car

		#Display red cars
		for i in range(level + 1): 
			draw_things(thing_list[i]["x"],thing_list[i]["y"],car2Img)
			thing_list[i]["y"] += thing_speed - imu_direct_y
		
			if thing_list[i]["y"] > display_height:
				thing_list[i]["x"] = random.randrange(road_start_x,road_end_x-car_width)
				thing_list[i]["y"] = -200

		#Display high score
		highscore(count)
		count+=1
			
		#Scroll road picture
		bg_y1 += bg_speed - imu_direct_y
		bg_y2 += bg_speed - imu_direct_y
		
		if bg_y1 >= display_height:
			bg_y1 = -600
			
		if bg_y2 >= display_height:
			bg_y2 = -600
			
		
		
		pygame.display.update() # update the screen
		clock.tick(60) # frame per sec
```

- Main logic

```python
intro()		
gameloop()	
```



## ESP32

### client.py

Udp connect and main code.

### mpu6050.py 

6-axis MPU-6050 MEMS sensor driver.

### wifi.py 

ESP32 wifi connect config.