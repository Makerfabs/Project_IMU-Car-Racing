import pygame
import time
import random 

#udp init
import socket
BUFSIZE = 1024
ip_port = ('192.168.1.125', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
server.bind(ip_port)

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

	#障碍物参数设置
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
intro()		
gameloop()	
