import socket
import threading, pyaudio,pickle,struct
import os
import time

server_host_ip = '10.0.0.31'
server_port_address = 9611
print(server_host_ip, server_port_address)

client_host_ip = '10.0.0.189'
client_port = 9543
print(client_host_ip, client_port)



def server_audio_stream():
    server_socket = socket.socket()
    server_socket.bind((server_host_ip, (server_port_address-1)))
    server_FORMAT = pyaudio.paInt16
    server_socket.listen(5)
    server_CHUNK = 1024
    #wf = wave.open("Recording.wav", 'rb')
    
    server_p = pyaudio.PyAudio()
    print('server listening at',(server_host_ip, (server_port_address-1)))
   
    
    server_stream = server_p.open(format=server_FORMAT,
                    channels=2,
                    rate=44100,
                    input=True,
                    input_device_index = 2,
                    frames_per_buffer=server_CHUNK)

             

    server_client_socket, server_addr = server_socket.accept()
 
    server_data = None
    while True:
        if server_client_socket:
            while True:
              
                server_data = server_stream.read(server_CHUNK)
                server_a = pickle.dumps(server_data)
                server_message = struct.pack("Q",len(server_a))+server_a
                server_client_socket.sendall(server_message)
                


###############################################################################################################################



def client_audio_stream():
	
	client_p = pyaudio.PyAudio()
	client_CHUNK = 1024
	client_stream = client_p.open(format = client_p.get_format_from_width(2),
					channels=2,
					rate=44100,
					output=True,
					frames_per_buffer=client_CHUNK)
					
	# create socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clinet_socket_address = (client_host_ip, client_port-1)
	print('server listening at',clinet_socket_address)
	client_socket.connect(clinet_socket_address) 
	print("CLIENT CONNECTED TO",clinet_socket_address)
	client_data = b""
	client_payload_size = struct.calcsize("Q")
	while True:
		try:
			while len(client_data) < client_payload_size:
				clinet_packet = client_socket.recv(4*1024) # 4K
				if not clinet_packet: break
				client_data+=clinet_packet
			clinet_packed_msg_size = client_data[:client_payload_size]
			client_data = client_data[client_payload_size:]
			clinet_msg_size = struct.unpack("Q",clinet_packed_msg_size)[0]
			while len(client_data) < clinet_msg_size:
				client_data += client_socket.recv(4*1024)
			clinet_frame_data = client_data[:clinet_msg_size]
			client_data  = client_data[clinet_msg_size:]
			clinet_frame = pickle.loads(clinet_frame_data)
			client_stream.write(clinet_frame)

		except:
			
			break

	client_socket.close()
	print('Audio closed')
	os._exit(1)
	

t1 = threading.Thread(target=server_audio_stream, args=())
t2 = threading.Thread(target=client_audio_stream, args=())


t1.start()
time.sleep(2)
t2.start()

