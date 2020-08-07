import pygame
import time
import random 

#udp init
import socket
BUFSIZE = 1024
ip_port = ('192.168.1.125', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp协议
server.bind(ip_port)

pygame.init()
display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)

car_width = 50
car_height = 100

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Car Racing")
clock = pygame.time.Clock()

carImg = pygame.image.load("car1.png") #load the car image
car2Img = pygame.image.load("car2.png")
bgImg = pygame.image.load("back2.jpg")
crash_img = pygame.image.load("crash.png")

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
		pygame.display.set_icon(carImg)
		
		pygame.draw.rect(gameDisplay,black,(200,400,100,50))
		pygame.draw.rect(gameDisplay,black,(500,400,100,50))
			
		gameDisplay.fill(white)
		message_display("CAR RACING",100,display_width/2,display_height/2)
		message_display("Press Go and rst esp32",30,display_width/2,display_height/2 + 200)
		pygame.draw.rect(gameDisplay,green,(200,400,100,50))
		pygame.draw.rect(gameDisplay,red,(500,400,100,50))
		
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		
		
		if menu1_x < mouse[0] < menu1_x+menu_width and menu1_y < mouse[1] < menu1_y+menu_height:
			pygame.draw.rect(gameDisplay,blue,(200,400,100,50))
			if click[0] == 1:
				intro = False
		if menu2_x < mouse[0] < menu2_x+menu_width and menu2_y < mouse[1] < menu2_y+menu_height:
			pygame.draw.rect(gameDisplay,blue,(500,400,100,50))
			if click[0] == 1:
				pygame.quit()
				quit()
	
		message_display("Go",40,menu1_x+menu_width/2,menu1_y+menu_height/2)
		message_display("Exit",40,menu2_x+menu_width/2,menu2_y+menu_height/2)
		
		pygame.display.update()
		clock.tick(50)

def highscore(count):
	font = pygame.font.SysFont(None,20)
	text = font.render("Score : "+str(count),True,black)
	gameDisplay.blit(text,(0,0))
	
def draw_things(thingx,thingy,thing):
	gameDisplay.blit(thing,(thingx,thingy))
	

def car(x,y):
	gameDisplay.blit(carImg,(int(x),int(y)))

def text_objects(text,font):
	textSurface = font.render(text,True,black)
	return textSurface,textSurface.get_rect()
	
	
def message_display(text,size,x,y):
	font = pygame.font.Font("SourceCodePro.ttf",size)
	text_surface , text_rectangle = text_objects(text,font)
	text_rectangle.center =(int(x),int(y))
	gameDisplay.blit(text_surface,text_rectangle)
	
	
	
	
def crash(x,y):
	gameDisplay.blit(crash_img,(x,y))
	message_display("You Crashed",115,display_width/2,display_height/2)
	pygame.display.update()
	time.sleep(2)
	gameloop() #for restart the game
	
def gameloop():
	bg_x1 = int((display_width/2)-(360/2))
	bg_x2 = int((display_width/2)-(360/2))
	bg_y1 = 0
	bg_y2 = -600
	bg_speed = 8
	bg_speed_change = 0
	car_x = ((display_width / 2) - (car_width / 2))
	car_y = (display_height - car_height)
	car_x_change = 0
	road_start_x =  (display_width/2)-112
	road_end_x = (display_width/2)+112
	
	thing_startx = random.randrange(road_start_x,road_end_x-car_width)
	thing_starty = -600
	thingw = 50
	thingh = 100
	thing_speed = 12
	count=0
	gameExit = False
	
	while not gameExit:
		#UDP
		data,client_addr = server.recvfrom(BUFSIZE)
		server.sendto(data.upper(),client_addr)
		print('server收到的数据:',data)
		data_str = data.decode('utf-8').encode('utf-8')
		xyz = eval(data_str)
		imu_direct_x = int(xyz["x"])
		imu_direct_y = 0 - int(xyz["y"])

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
			
		#udp	
		car_x = (display_width/2) + 112 * imu_direct_x / 10
		#car_y = (display_width/2) + 112 * imu_direct_y / 10

		#car_x+=car_x_change
		
		if car_x > road_end_x-car_width:
			crash(car_x,car_y)
		if car_x < road_start_x:
			crash(car_x-car_width,car_y)
		
		
		if car_y < thing_starty + thingh and car_y > thing_starty - thingh :
			if car_x >= thing_startx and car_x <= thing_startx+thingw:
				crash(car_x-25,car_y-car_height/2)
			if car_x+car_width >= thing_startx and car_x+car_width <= thing_startx+thingw:
				crash(car_x,car_y-car_height/2)
		
		gameDisplay.fill(green) #display white background
		
		gameDisplay.blit(bgImg,(int(float(bg_x1)),int(float(bg_y1))))
		gameDisplay.blit(bgImg,(bg_x2,bg_y2))
		car(car_x,car_y) #display car
		draw_things(thing_startx,thing_starty,car2Img)
		highscore(count)
		count+=1
		thing_starty += thing_speed - imu_direct_y
		
		if thing_starty > display_height:
			thing_startx = random.randrange(road_start_x,road_end_x-car_width)
			thing_starty = -200
			
		bg_y1 += bg_speed - imu_direct_y
		bg_y2 += bg_speed - imu_direct_y
		
		if bg_y1 >= display_height:
			bg_y1 = -600
			
		if bg_y2 >= display_height:
			bg_y2 = -600
			
		
		
		pygame.display.update() # update the screen
		clock.tick(60) # frame per sec
intro()		
gameloop()	
