import socket, cv2, pickle,struct,imutils
import threading
import time
# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # nature of scoket


host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9998
socket_address = (host_ip,port)

reciever_IP_address = '10.0.0.31'
reciever_port_address = 9999
reciever_socket_address = (reciever_IP_address, reciever_port_address)
# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(1)

# Socket Accept
def sending_data():
    print("LISTENING AT:",socket_address)
    while True:
    	client_socket,addr = server_socket.accept()
    	#print('GOT CONNECTION FROM:',addr)
    	if client_socket:
    		vid = cv2.VideoCapture("test_video_1.mp4")
    		
    		while(vid.isOpened()):
    			try:
        			img,frame = vid.read()
        			frame = imutils.resize(frame,width=320)
        			a = pickle.dumps(frame)
        			message = struct.pack("Q",len(a))+a
        			client_socket.sendall(message)
        			
        			#cv2.imshow('TRANSMITTING VIDEO',frame)
        			key = cv2.waitKey(1) & 0xFF
        			if key ==ord('q'):
        				client_socket.close()
    			except:
        			time.sleep(5)
        			continue
                    

def recieving_data():
    #client_socket.connect((host_ip,port)) # a tuple
    print("recieving from:", reciever_socket_address)
    reciever_socket.connect(reciever_socket_address)
    print("Recieving Started")
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
        	while len(data) < payload_size:
        		packet = reciever_socket.recv(4*1024) # 4K
        		if not packet: break
        		data+=packet
        	packed_msg_size = data[:payload_size]
        	data = data[payload_size:]
        	msg_size = struct.unpack("Q",packed_msg_size)[0]
        	
        	while len(data) < msg_size:
        		data += reciever_socket.recv(4*1024)
        	frame_data = data[:msg_size]
        	data  = data[msg_size:]
        	frame = pickle.loads(frame_data)
        	cv2.imshow("CLIENT RECEIVING VIDEO",frame)
        	key = cv2.waitKey(1) & 0xFF
        	if key  == ord('q'):
        		break
        except:
            continue
    reciever_socket.close()
    
    
x1 = threading.Thread(target = sending_data)
x2 = threading.Thread(target = recieving_data)

x1.start()
time.sleep(30)
x2.start()


x1.join()
x2.join()