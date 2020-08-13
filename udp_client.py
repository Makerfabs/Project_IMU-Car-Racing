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