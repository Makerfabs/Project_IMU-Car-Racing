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