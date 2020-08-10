import socket
BUFSIZE = 1024
ip_port = ('192.168.1.125', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # udp
server.bind(ip_port)
while True:
    data,client_addr = server.recvfrom(BUFSIZE)
    data_str = data.decode('utf-8').encode('utf-8')
    xyz = eval(data_str)
    print('server receive', data)
    print(xyz["x"])
    print(xyz["y"])
    #print("**************")
 
    server.sendto(data.upper(),client_addr)
 
server.close()