import socket, cv2, pickle,struct,imutils
import threading
import time
import pyaudio
import tkinter
from PIL import Image, ImageTk
import json
# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # nature of scoket



def load_meeting_meta_data():
    meeting_file = open("form_data.json")
    meeting_data = json.load(meeting_file)
    
    host_ip = meeting_data[0]["main"]["ipaddress"]
    host_email = meeting_data[0]["main"]["email"]
    host_port_address = meeting_data[0]["main"]["port"]
    host_name = meeting_data[0]["main"]["name"]
    
    #print(host_ip, host_email, host_port_address, host_name)
    
    parasite_ip = meeting_data[1]["others"][0]["ipaddress"]
    parasite_email = meeting_data[1]["others"][0]["email"]
    parasite_port_address = meeting_data[1]["others"][0]["port"]
    parasite_name = meeting_data[1]["others"][0]["name"]
    
    print(host_ip, host_email, host_port_address, host_name)
    
    print(parasite_ip, parasite_email, parasite_port_address, parasite_name)
    
    return host_ip, host_email, host_port_address, host_name, parasite_ip, parasite_email, parasite_port_address, parasite_name


h_ip, h_email, h_port_address, h_name, p_ip, p_email, p_port_address, p_name = load_meeting_meta_data()


host_ip = h_ip
port = int(h_port_address)
socket_address = (host_ip,port)
audio_server_socket_address = (host_ip,(port-20))
server_socket.bind(socket_address)
server_socket.listen(1)



reciever_IP_address = p_ip
reciever_port_address = int(p_port_address)
reciever_socket_address = (reciever_IP_address, reciever_port_address)
audio_reciever_socket_address = (reciever_IP_address, (reciever_port_address-20))

UI_server_video_frames = []
UI_reciever_video_frames = []

########################################## VIDEO TRANSMISSION ##################################################
# Socket Accept
def sending_data():
    global UI_server_video_frames
    print("LISTENING AT:",socket_address)
    while True:
    	client_socket,addr = server_socket.accept()
    	#print('GOT CONNECTION FROM:',addr)
    	if client_socket:
    		vid = cv2.VideoCapture("test_1.mp4")
    		
    		while(vid.isOpened()):
    			try:
        			img,frame = vid.read()
        			frame = cv2.resize(frame, (640, 360), interpolation = cv2.INTER_AREA)
        			UI_server_video_frames.append(frame)
        			#frame = imutils.resize(frame,width=240)
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
    global UI_reciever_video_frames
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
        	UI_reciever_video_frames.append(frame)
        	#cv2.imshow("CLIENT RECEIVING VIDEO",frame)
        	key = cv2.waitKey(1) & 0xFF
        	if key  == ord('q'):
        		break
        except:
            continue
    reciever_socket.close()
########################################## VIDEO TRANSMISSION ##################################################


########################################## AUDIO TRANSMISSION ##################################################
def server_audio_stream():
    audio_server_socket = socket.socket()
    audio_server_socket.bind(audio_server_socket_address)
    server_FORMAT = pyaudio.paInt16
    audio_server_socket.listen(5)
    server_CHUNK = 1024
    #wf = wave.open("Recording.wav", 'rb')
    
    server_p = pyaudio.PyAudio()
    print('server listening at',audio_server_socket_address)
   
    
    server_stream = server_p.open(format=server_FORMAT,
                    channels=2,
                    rate=44100,
                    input=True,
                    input_device_index = 2,
                    frames_per_buffer=server_CHUNK)

             

    server_client_socket, server_addr = audio_server_socket.accept()
 
    server_data = None
    while True:
        if server_client_socket:
            while True:
              
                server_data = server_stream.read(server_CHUNK)
                server_a = pickle.dumps(server_data)
                server_message = struct.pack("Q",len(server_a))+server_a
                server_client_socket.sendall(server_message)


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
	clinet_socket_address = audio_reciever_socket_address
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

########################################## AUDIO TRANSMISSION ##################################################

########################################## APP UI ##################################################
def app_UI():
    global UI_server_video_frames
    global UI_reciever_video_frames
    root = tkinter.Tk()
    canvas1 = tkinter.Canvas(root, width=640 , height=360)
    canvas2 = tkinter.Canvas(root, width=640, height=360)

    canvas1.pack(padx=5, pady=10, side="left")
    canvas2.pack(padx=5, pady=60, side="left")
    
    server_frame = cv2.imread("error.jpg")
    reciever_frame = cv2.imread("error.jpg")
    
    while(True):
        if (len(UI_server_video_frames)>0):
            #try:
            server_frame = UI_server_video_frames.pop(0)
            #except:
            #    server_frame = cv2.imread("error.jpg")
                
        if (len(UI_reciever_video_frames)>0):
            #try:
            reciever_frame = UI_reciever_video_frames.pop(0)
            #except:
            #    reciever_frame = cv2.imread("error.jpg")
            
        server_cv2image = cv2.cvtColor(server_frame, cv2.COLOR_BGR2RGBA)
        reciever_cv2image = cv2.cvtColor(reciever_frame, cv2.COLOR_BGR2RGBA)
        
        server_img = Image.fromarray(server_cv2image)
        reciever_img = Image.fromarray(reciever_cv2image)
        
        imgtk_1 = ImageTk.PhotoImage(image=server_img)
        imgtk_2 = ImageTk.PhotoImage(image=reciever_img)
        canvas1.create_image(0, 0, image=imgtk_1, anchor=tkinter.NW)
        canvas2.create_image(0, 0, image=imgtk_2, anchor=tkinter.NW)
        #Setting the image on the label
        #root.config(image=imgtk)
        root.update()
########################################## APP UI ##################################################
    



x1 = threading.Thread(target = sending_data)
x2 = threading.Thread(target = recieving_data)

t1 = threading.Thread(target=server_audio_stream, args=())
t2 = threading.Thread(target=client_audio_stream, args=())

t3 = threading.Thread(target=app_UI, args=())

x1.start()
t1.start()
time.sleep(20)
x2.start()
t2.start()
time.sleep(5)
t3.start()

x1.join()
x2.join()
t1.join()
t2.join()
t3.join()
