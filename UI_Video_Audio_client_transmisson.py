# loading dependencies and libraries
import socket, cv2, pickle,struct,imutils
import threading
import time
import pyaudio
import tkinter
from PIL import Image, ImageTk
import json
# Socket Create
# Socket Create for both participant 1 and participant 2
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # nature of scoket



def load_meeting_meta_data():
    # loding meeting meta data from form_data.json
    meeting_file = open("form_data.json")
    # load the data from teh .json file
    meeting_data = json.load(meeting_file)
    # extract participant-1/server's ip address email and port address from the json data
    host_ip = meeting_data[0]["main"]["ipaddress"]
    host_email = meeting_data[0]["main"]["email"]
    host_port_address = meeting_data[0]["main"]["port"]
    host_name = meeting_data[0]["main"]["name"]
    
    #print(host_ip, host_email, host_port_address, host_name)
    # extract participant-2/client's ip address email and port address from the json data
    parasite_ip = meeting_data[1]["others"][0]["ipaddress"]
    parasite_email = meeting_data[1]["others"][0]["email"]
    parasite_port_address = meeting_data[1]["others"][0]["port"]
    parasite_name = meeting_data[1]["others"][0]["name"]
    
    print(host_ip, host_email, host_port_address, host_name)
    
    print(parasite_ip, parasite_email, parasite_port_address, parasite_name)
    # return the extracted ip address email and port address from the json data
    return host_ip, host_email, host_port_address, host_name, parasite_ip, parasite_email, parasite_port_address, parasite_name

# getting the ip address email and port address from the json data of both participant 1 nd 2
h_ip, h_email, h_port_address, h_name, p_ip, p_email, p_port_address, p_name = load_meeting_meta_data()

# passing the extracted IP, port address, emails and sockets for server
host_ip = h_ip
port = int(h_port_address)
socket_address = (host_ip,port)
audio_server_socket_address = (host_ip,(port-20))
server_socket.bind(socket_address)
server_socket.listen(1)


# passing the extracted IP, port address, emails and sockets for client
reciever_IP_address = p_ip
reciever_port_address = int(p_port_address)
reciever_socket_address = (reciever_IP_address, reciever_port_address)
audio_reciever_socket_address = (reciever_IP_address, (reciever_port_address-20))

UI_server_video_frames = []
UI_reciever_video_frames = []

########################################## VIDEO TRANSMISSION ##################################################
# Socket Accept
def sending_data():
    # sennding video frames from server end
    global UI_server_video_frames
    print("LISTENING AT:",socket_address)
    while True:
        # establising socket connection
    	client_socket,addr = server_socket.accept()
    	#print('GOT CONNECTION FROM:',addr)
    	if client_socket:
            # capturing video from camera
    		vid = cv2.VideoCapture(0)
    		
    		while(vid.isOpened()):
    			try:
                    # reading video data from the capture class
        			img,frame = vid.read()
                    # resize the video frame
        			frame = cv2.resize(frame, (640, 360), interpolation = cv2.INTER_AREA)
                    # append the video frame to queue
        			UI_server_video_frames.append(frame)
        			#frame = imutils.resize(frame,width=240)
                    
                    # convert the matrix format of frames to bits
        			a = pickle.dumps(frame)
                    # append header data to teh message
        			message = struct.pack("Q",len(a))+a
                    # send data via socket connection
        			client_socket.sendall(message)
        			
        			#cv2.imshow('TRANSMITTING VIDEO',frame)
        			key = cv2.waitKey(1) & 0xFF
        			if key ==ord('q'):
        				client_socket.close()
    			except:
        			time.sleep(5)
        			continue
                    

def recieving_data():
    # recieve video feed data from the client end
    global UI_reciever_video_frames
    #client_socket.connect((host_ip,port)) # a tuple
    print("recieving from:", reciever_socket_address)
    reciever_socket.connect(reciever_socket_address)
    print("Recieving Started")
    # initilize the bite data storage
    data = b""
    payload_size = struct.calcsize("Q")
    # initilize the while loop to cointinously recieve the video ddata from other end
    while True:
        try:
            # check iof the data is enbough for payload
        	while len(data) < payload_size:
        		packet = reciever_socket.recv(4*1024) # 4K
        		if not packet: break
        		data+=packet
        	packed_msg_size = data[:payload_size] # pack the recieved video data for processing
        	data = data[payload_size:]
        	msg_size = struct.unpack("Q",packed_msg_size)[0] # unpack the video data fro the socket from its header
        	
        	while len(data) < msg_size:# wait till the recieved data is enough
        		data += reciever_socket.recv(4*1024)
        	frame_data = data[:msg_size]# crop the data as per the msg_size
        	data  = data[msg_size:]
        	frame = pickle.loads(frame_data)# load the nit serialized socket data into matrix format
        	UI_reciever_video_frames.append(frame)# append the video frmae sfrom client end to the queue
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
    # create a socket for auido server
    audio_server_socket = socket.socket()
    audio_server_socket.bind(audio_server_socket_address)
    # initilize instances and variables for microphone
    server_FORMAT = pyaudio.paInt16
    audio_server_socket.listen(5)
    server_CHUNK = 1024
    #wf = wave.open("Recording.wav", 'rb')
    # calling the pyduiusio class for audio retrival from microphone
    server_p = pyaudio.PyAudio()
    print('server listening at',audio_server_socket_address)
   
    # creating object to microphone audio transmission class
    server_stream = server_p.open(format=server_FORMAT,
                    channels=2,
                    rate=44100,
                    input=True,
                    input_device_index = 2,
                    frames_per_buffer=server_CHUNK)

             
    # creating socket instance
    server_client_socket, server_addr = audio_server_socket.accept()
 
    server_data = None
    while True:
        # transfering the socket data
        if server_client_socket:
            while True:
              # reading the audio data
                server_data = server_stream.read(server_CHUNK)# dump the audio data into byte format for trnasmisssion
                server_a = pickle.dumps(server_data)
                server_message = struct.pack("Q",len(server_a))+server_a# add header to the meesage
                server_client_socket.sendall(server_message)# send the data via socket


def client_audio_stream():
	# create client side socket instace for data recieving
    # initilize pyaudio class for audio data processing
    # declaring audio data variables
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
	print("CLIENT CONNECTED TO",clinet_socket_address)# initialize byte storage for audio trnasmission
	client_data = b""
	client_payload_size = struct.calcsize("Q")
	while True:
		try:
            # recieve the audio data if it is grater than payload size
			while len(client_data) < client_payload_size:
				clinet_packet = client_socket.recv(4*1024) # 4K
				if not clinet_packet: break
				client_data+=clinet_packet
			clinet_packed_msg_size = client_data[:client_payload_size]# pack the recieved audio data
			client_data = client_data[client_payload_size:]
			clinet_msg_size = struct.unpack("Q",clinet_packed_msg_size)[0]# unpack the header from data
			while len(client_data) < clinet_msg_size:
				client_data += client_socket.recv(4*1024)
			clinet_frame_data = client_data[:clinet_msg_size]# crop the data to remove unnecessary data
			client_data  = client_data[clinet_msg_size:]
			clinet_frame = pickle.loads(clinet_frame_data)# load data into pickle frame for processing
			client_stream.write(clinet_frame)

		except:
			
			break

	client_socket.close()

########################################## AUDIO TRANSMISSION ##################################################

########################################## APP UI ##################################################
def app_UI():
    global UI_server_video_frames
    global UI_reciever_video_frames
    # create window for UI
    root = tkinter.Tk()
    canvas1 = tkinter.Canvas(root, width=640 , height=360)
    canvas2 = tkinter.Canvas(root, width=640, height=360)
    # pack the initialized UI elements
    canvas1.pack(padx=5, pady=10, side="left")
    canvas2.pack(padx=5, pady=60, side="left")
    # read the error code image
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
        # show the image/video frame in UI
        imgtk_1 = ImageTk.PhotoImage(image=server_img)
        imgtk_2 = ImageTk.PhotoImage(image=reciever_img)
        canvas1.create_image(0, 0, image=imgtk_1, anchor=tkinter.NW)
        canvas2.create_image(0, 0, image=imgtk_2, anchor=tkinter.NW)
        #Setting the image on the label
        #root.config(image=imgtk)
        
        # refresh the UI window
        root.update()
########################################## APP UI ##################################################
    


# threading initilization for video and audio trnasmission server side
x1 = threading.Thread(target = sending_data)
x2 = threading.Thread(target = recieving_data)
# threading initilization for video and audio trnasmission client side
t1 = threading.Thread(target=server_audio_stream, args=())
t2 = threading.Thread(target=client_audio_stream, args=())
# initializing UI thread for the application
t3 = threading.Thread(target=app_UI, args=())
# starting the video, audio, UI threads for both client and server
x1.start()
t1.start()
time.sleep(20)
x2.start()
t2.start()
time.sleep(5)
t3.start()
# join the video, audio, UI threads for both client and server
x1.join()
x2.join()
t1.join()
t2.join()
t3.join()
