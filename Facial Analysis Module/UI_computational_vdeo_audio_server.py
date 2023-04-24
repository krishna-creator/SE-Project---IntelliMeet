import socket, cv2, pickle,struct,imutils
import threading
import time
from video_face_detect import call_face_detection
import json
import pyaudio
import os
import wave
import whisper

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # nature of scoket


#host_name  = socket.gethostname()
host_ip = '10.0.0.31'
port = 9999
socket_address = (host_ip,port)
audio_server_socket_address = (host_ip,(port-20))
server_socket.bind(socket_address)
server_socket.listen(1)



reciever_IP_address = '10.0.0.31'
reciever_port_address = 9998
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
model = whisper.load_model("base", device = "cuda")
file_save_flag = 0
transcription_results = []

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
    print("LISTENING AT:",socket_address)
    while True:
    	client_socket,addr = server_socket.accept()
    	#print('GOT CONNECTION FROM:',addr)
    	if client_socket:
    		vid = cv2.VideoCapture(0)
    		
    		while(vid.isOpened()):
    			try:
        			img,frame = vid.read()
        			if server_frame_count%10==0:
        				current_server_time = get_time()
        				video_frames_processing.append({sequence_count: ["server", str(current_server_time), frame]})
        				sequence_count = sequence_count+1  
        			#frame = call_face_detection(frame)
        			frame = imutils.resize(frame,width=480)
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
        	#client_frame = call_face_detection(frame)
        	cv2.imshow("SERVER RECEIVING VIDEO",client_frame)
        	if client_frame_count%10==0:
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
            result = model.transcribe(temp_audio_file_path, fp16=False, language = 'english')
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
	print('Audio closed')
	os._exit(1)

###########################################################################################################

x1 = threading.Thread(target = sending_data)
x2 = threading.Thread(target = recieving_data)
x3 = threading.Thread(target = video_retinaface_processing)

t1 = threading.Thread(target=server_audio_stream, args=())
t2 = threading.Thread(target=client_audio_stream, args=())
t3 = threading.Thread(target=whisper_processing, args=())

x1.start()
t1.start()
x3.start()
t3.start()
time.sleep(20)
x2.start()
t2.start()


x1.join()
x2.join()
x3.join()
t1.join()
t2.join()
t3.join()