import socket
BUFSIZE = 1024
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
    #msg = input(">> ").strip()
    ip_port = ('192.168.1.125', 80)
    #client.sendto(msg.encode('utf-8'),ip_port)
    client.sendto("msg".encode('utf-8'),ip_port)
 
    data,server_addr = client.recvfrom(BUFSIZE)
    print('client recvfrom ',data,server_addr)
 
client.close()