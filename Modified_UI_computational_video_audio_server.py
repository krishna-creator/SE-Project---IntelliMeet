import socket, cv2, pickle,struct,imutils
import threading
import time
from video_face_detect import call_face_detection
import json
import pyaudio
import os
import wave
import whisper
import tkinter
from PIL import Image, ImageTk
#from graph_plotting import use_case_1
import sys
#from tkinter import *


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

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # nature of scoket


#host_name  = socket.gethostname()
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


# Socket Listen
video_frames_processing = []
sequence_count = 0
video_file_save_flag = 0
face_analysis_results = []
video_json_filename = "face_detection_results.json"
json_filename = "audio_results.json"
result_json_lst = []
#temp_count = 0
audio_files_processing = []
model = whisper.load_model("small", device = "cuda")
file_save_flag = 0
transcription_results = []


UI_server_video_frames = []
UI_reciever_video_frames = []
UI_string = ""

def get_time():
    temp_time = time.localtime()
    current_time = time.strftime("%H$%M$%S", temp_time)
    return str(current_time)
    
#{sequence_count: ["server", str(current_server_time), frame]}

def video_json_filecreation(temp_sequence_count, temp_name, temp_time, ret_status):
    global video_file_save_flag
    global face_analysis_results
    #print(input_file_type, input_file_time, input_file_sequence)
    try:
        temp_dict = {}
        with open(video_json_filename, "w") as file:
            if video_file_save_flag ==1:
                #temp_contents = file.read()
                #temp_read_data = json.load(file)
                temp_dict[temp_sequence_count] = {temp_name: [[temp_time], [ret_status]] }
                face_analysis_results.append(temp_dict)
                #file.seek(0)
                json.dump(face_analysis_results, file)
                #video_file_save_flag = video_file_save_flag+1
            else:
                temp_dict[temp_sequence_count] = {temp_name: [[temp_time], [ret_status]] }
                face_analysis_results.append(temp_dict)
                json.dump(face_analysis_results, file)
                video_file_save_flag = 1
    except:
        print("error faced")
        pass


##########################################################################################
def video_retinaface_processing():
    global video_frames_processing
    print("hi")
    while True:
        if len(video_frames_processing)>0:
            temp_video_frame_data = video_frames_processing.pop(0)
            temp_sequence_count = list(temp_video_frame_data.keys())[0]
            temp_name = temp_video_frame_data[temp_sequence_count][0]
            temp_time = temp_video_frame_data[temp_sequence_count][1]
            temp_video_frame = temp_video_frame_data[temp_sequence_count][2]
            #print(temp_audio_file_path)
            try:
                result, ret_status = call_face_detection(temp_video_frame)
            except:
                ret_status = -1
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(ret_status)
            video_json_filecreation(temp_sequence_count, temp_name, temp_time, ret_status)
        else:
            time.sleep(0.5)
            continue
##########################################################################################




# Socket Accept

def sending_data():
    server_frame_count = 0
    global video_frames_processing
    global sequence_count
    global UI_server_video_frames
    print("LISTENING AT:",socket_address)
    while True:
    	client_socket,addr = server_socket.accept()
    	#print('GOT CONNECTION FROM:',addr)
    	if client_socket:
    		vid = cv2.VideoCapture(0)
    		
    		while(vid.isOpened()):
    			try:
        			img,frame = vid.read()
        			frame = cv2.resize(frame, (640, 360), interpolation = cv2.INTER_AREA)
        			UI_server_video_frames.append(frame)
        			if server_frame_count%20==0:
        				current_server_time = get_time()
        				video_frames_processing.append({sequence_count: ["server", str(current_server_time), frame]})
        				sequence_count = sequence_count+1  
        			#frame = call_face_detection(frame)
        			#frame = imutils.resize(frame,width=240)
        			a = pickle.dumps(frame)
        			message = struct.pack("Q",len(a))+a
        			client_socket.sendall(message)
        			server_frame_count =server_frame_count + 1
        			#cv2.imshow('TRANSMITTING VIDEO',frame)
        			key = cv2.waitKey(1) & 0xFF
        			if key ==ord('q'):
        				client_socket.close()
    			except:
        			time.sleep(5)
        			continue
                    


def recieving_data(): 
    global UI_reciever_video_frames
    client_frame_count = 0
    global video_frames_processing
    global sequence_count
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
        	client_frame_data = data[:msg_size]
        	data  = data[msg_size:]
        	client_frame = pickle.loads(client_frame_data)
        	UI_reciever_video_frames.append(client_frame)
        	#client_frame = call_face_detection(frame)
        	#cv2.imshow("SERVER RECEIVING VIDEO",client_frame)
        	if client_frame_count%20==0:
        		current_clinet_time = get_time()
        		video_frames_processing.append({sequence_count: ["client", str(current_clinet_time), client_frame]})
        		sequence_count = sequence_count+1 
                
        	client_frame_count = client_frame_count+1
        	key = cv2.waitKey(1) & 0xFF
        	if key  == ord('q'):
        		break
        except:
            continue
    reciever_socket.close()

#########################################  AUDIO CREATION  ########################################################################
def json_filecreation(input_file_path, input_text):
    global file_save_flag
    global transcription_results
    global UI_string
    temp_data = input_file_path.split("temp_dir/")[1]
    input_file = temp_data.split(".wav")[0]
    input_file_type = input_file.split("__")[0]
    input_file_time = (input_file.split("__")[1]).split("_")[1]
    input_file_sequence = (input_file.split("__")[1]).split("_")[0]
    #print(input_file_type, input_file_time, input_file_sequence)
    try:
        temp_dict = {}
        with open(json_filename, "w") as file:
            if file_save_flag ==1:
                #temp_contents = file.read()
                #temp_read_data = json.load(file)
                UI_string = input_text
                temp_dict[input_file_sequence] = {input_file_type: [[input_file_time], [input_text]] }
                transcription_results.append(temp_dict)
                #file.seek(0)
                json.dump(transcription_results, file)
                #file_save_flag = file_save_flag+1
            else:
                temp_dict[input_file_sequence] = {input_file_type: [[input_file_time], [input_text]] }
                transcription_results.append(temp_dict)
                json.dump(transcription_results, file)
                file_save_flag = 1
    except:
        print("error faced")
        pass
    

def whisper_processing():
    global audio_files_processing
    while True:
        if len(audio_files_processing)>0:
            temp_audio_file_path = audio_files_processing.pop(0)
            #print(temp_audio_file_path)
            result = model.transcribe(temp_audio_file_path, fp16=True, language = 'english')
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(result["text"])
            json_filecreation(temp_audio_file_path, result["text"])
            os.remove(temp_audio_file_path)
        else:
            time.sleep(0.5)
            continue



def server_audio_stream():
    global audio_files_processing
    global sequence_count
    audio_server_socket = socket.socket()
    audio_server_socket.bind(audio_server_socket_address)
    server_FORMAT = pyaudio.paInt16
    audio_server_socket.listen(5)
    server_CHUNK = 1024
    server_frame_count = 0
    server_audio_size = 0
    #server_temp_count = 0
    server_frames = []
    #wf = wave.open("Recording.wav", 'rb')
    
    server_p = pyaudio.PyAudio()
    print('server listening at ',audio_server_socket_address)
   
    
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
                server_frames.append(server_data)
                server_a = pickle.dumps(server_data)
                server_message = struct.pack("Q",len(server_a))+server_a
                server_client_socket.sendall(server_message)
                server_audio_size = server_audio_size + len(server_data)
                if (server_frame_count > int(44100 / server_CHUNK * 5)) and (server_audio_size>(0.7*(int(44100 / server_CHUNK * 5))*4096)):
                    print("Saving server side audio "+str(sequence_count))
                    server_temp_time = time.localtime()
                    server_current_time = time.strftime("%H$%M$%S", server_temp_time)
                    temp_server_audiofile_name = "temp_dir/server__"+str(sequence_count)+"_"+str(server_current_time)+".wav"
                    waveFile = wave.open(temp_server_audiofile_name, 'wb')
                    waveFile.setnchannels(2)
                    waveFile.setsampwidth(server_p.get_sample_size(server_FORMAT))
                    waveFile.setframerate(44100)
                    waveFile.writeframes(b''.join(server_frames))
                    waveFile.close()
                    audio_files_processing.append(temp_server_audiofile_name)
                    server_frame_count = 0
                    server_audio_size = 0
                    server_frames = []
                    sequence_count = sequence_count +1
                server_frame_count = server_frame_count + 1
 
    
def client_audio_stream():
	global audio_files_processing
	global sequence_count
	client_p = pyaudio.PyAudio()
	client_CHUNK = 1024
	client_FORMAT = pyaudio.paInt16
	client_stream = client_p.open(format = client_p.get_format_from_width(2),
					channels=2,
					rate=44100,
					output=True,
					frames_per_buffer=client_CHUNK)
					
	# create socket
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket_address = audio_reciever_socket_address
	print('server listening at',client_socket_address)
	client_socket.connect(client_socket_address) 
	print("CLIENT CONNECTED TO",client_socket_address)
	client_data = b""
	client_payload_size = struct.calcsize("Q")
	clinet_frames = []
	client_fame_count = 0
	#client_temp_count = 0
	client_audio_size = 0
	while True:
		try:
			while len(client_data) < client_payload_size:
				client_packet = client_socket.recv(4*1024) # 4K
				if not client_packet: break
				client_data+=client_packet
			client_packed_msg_size = client_data[:client_payload_size]
			client_data = client_data[client_payload_size:]
			client_msg_size = struct.unpack("Q",client_packed_msg_size)[0]
			while len(client_data) < client_msg_size:
				client_data += client_socket.recv(4*1024)
			client_frame_data = client_data[:client_msg_size]
			client_data  = client_data[client_msg_size:]
			client_frame = pickle.loads(client_frame_data)
			client_audio_size = client_audio_size + len(client_frame)
			client_stream.write(client_frame)
			clinet_frames.append(client_frame)
			if (client_fame_count > int(44100 / client_CHUNK * 5)) and (client_audio_size>(0.7*(int(44100 / client_CHUNK * 5))*4096)):
				print("Saving client side audio "+str(sequence_count))
				client_temp_time = time.localtime()
				client_current_time = time.strftime("%H$%M$%S", client_temp_time)
				temp_client_audiofile_name = "temp_dir/client__"+str(sequence_count)+"_"+str(client_current_time)+".wav"
				waveFile = wave.open(temp_client_audiofile_name, 'wb')
				waveFile.setnchannels(2)
				waveFile.setsampwidth(client_p.get_sample_size(client_FORMAT))
				waveFile.setframerate(44100)
				waveFile.writeframes(b''.join(clinet_frames))
				waveFile.close()
				audio_files_processing.append(temp_client_audiofile_name)
                
				clinet_frames = []
				client_fame_count =0
				client_audio_size =0
				sequence_count = sequence_count+1
				#print("completed saving audio")
			client_fame_count = client_fame_count + 1

		except:	
			break

	client_socket.close()
	#print('Audio closed')
	#os._exit(1)

###########################################################################################################

def end_meeting():
    from graph_plotting import use_case_1
    print("!!!!!!  meeting ended  !!!!!!!")
    use_case_1()
    #sys.exit(0)
    

########################################## APP UI ##################################################
def app_UI():
    global UI_server_video_frames
    global UI_reciever_video_frames
    global UI_string
    root = tkinter.Tk()
    root.title("Intellimeet")
    root.configure(bg='white')
    root.geometry("1400x530")
    root.resizable(False,False)
    title_label = tkinter.Label( root, text="Intellimeet", font=("Arial", 22), fg="maroon", bg='white' )
    title_label.place(relx = 0.5, rely = 0.0)
    canvas1 = tkinter.Canvas(root, width=640, height=360, highlightthickness=4, highlightbackground="maroon", bg='white')
    canvas2 = tkinter.Canvas(root, width=640, height=360, bg='white')
    canvas3 = tkinter.Canvas(root, width=61, height=290, bg='white', highlightthickness=0, highlightbackground="white")

    canvas1.pack(padx=5, pady=5, side="left")
    canvas2.pack(padx=5, pady=5, side="left")
    canvas3.pack(padx=22, pady=5, side="left")
    
    server_frame = cv2.imread("error.jpg")
    reciever_frame = cv2.imread("error.jpg")
    mic_video_button = cv2.imread("mic_video_buttons.jpg")
    mic_video_button = cv2.resize(mic_video_button, (40, 192), interpolation = cv2.INTER_AREA)
    #temp_label = tkinter.Label(root, text = "Audio Transcripts !!")
    #temp_label.place(relx = 0.0, rely = 0.9, anchor ='sw')
    audio_label = tkinter.Label(root, text = "Audio Transcripts: ", font=("Arial", 13), bg='white')
    audio_label.place(relx = 0.0, rely = 0.9, anchor ='sw')
    my_label = tkinter.Label(root, text = "  ", font=("Arial", 12), bg='white')
    my_label.place(relx = 0.0, rely = 1.0, anchor ='sw')
    end_button = tkinter.Button(root, text ="End Meeting", command = end_meeting, bg = "maroon",fg="white",font=("Arial", 13))
    end_button.place(relx = 1.0, rely = 0.0, anchor ='ne')
    #my_label.pack()
    #root.mainloop()
    #my_label.place(x=100, y=100)
    
    #####################################
    buttons_cv2image = cv2.cvtColor(mic_video_button, cv2.COLOR_BGR2RGBA)
    buttons_img = Image.fromarray(buttons_cv2image)
    button_imgtk = ImageTk.PhotoImage(image=buttons_img)
    canvas3.create_image(0, 0, image=button_imgtk, anchor=tkinter.NW)
    #####################################
    
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
        
        try:
            my_label.config(text = UI_string)
        except:
            my_label.config(text = "Audio Transcripts !!")

        
        #Setting the image on the label
        #root.config(image=imgtk)
        
        root.update()
########################################## APP UI ##################################################



x1 = threading.Thread(target = sending_data)
x2 = threading.Thread(target = recieving_data)
x3 = threading.Thread(target = video_retinaface_processing)

t1 = threading.Thread(target=server_audio_stream, args=())
t2 = threading.Thread(target=client_audio_stream, args=())
t3 = threading.Thread(target=whisper_processing, args=())


a1 = threading.Thread(target=app_UI, args=())

x1.start()
t1.start()
x3.start()
t3.start()
time.sleep(20)
x2.start()
t2.start()
time.sleep(5)
a1.start()


x1.join()
x2.join()
x3.join()
t1.join()
t2.join()
t3.join()
a1.join()
