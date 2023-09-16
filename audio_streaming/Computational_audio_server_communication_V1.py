import socket
import threading, pyaudio,pickle,struct
import os
import wave
import whisper
import time
import json

json_filename = "result.json"
result_json_lst = []
temp_count = 0
audio_files_processing = []

server_host_ip = '10.0.0.31'
server_port_address = 9611
print(server_host_ip, server_port_address)

client_host_ip = '10.0.0.31'
client_port = 9543
print(client_host_ip, client_port)
json_filename = "audio_results.json"

model = whisper.load_model("base", device = "cuda")
file_save_flag = 0
transcription_results = []

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
    global temp_count
    server_socket = socket.socket()
    server_socket.bind((server_host_ip, (server_port_address-1)))
    server_FORMAT = pyaudio.paInt16
    server_socket.listen(5)
    server_CHUNK = 1024
    server_frame_count = 0
    server_audio_size = 0
    #server_temp_count = 0
    server_frames = []
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
                server_frames.append(server_data)
                server_a = pickle.dumps(server_data)
                server_message = struct.pack("Q",len(server_a))+server_a
                server_client_socket.sendall(server_message)
                server_audio_size = server_audio_size + len(server_data)
                if (server_frame_count > int(44100 / server_CHUNK * 5)) and (server_audio_size>(0.7*(int(44100 / server_CHUNK * 5))*4096)):
                    print("Saving server side audio "+str(temp_count))
                    server_temp_time = time.localtime()
                    server_current_time = time.strftime("%H$%M$%S", server_temp_time)
                    temp_server_audiofile_name = "temp_dir/server__"+str(temp_count)+"_"+str(server_current_time)+".wav"
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
                    temp_count = temp_count +1
                server_frame_count = server_frame_count + 1
                


###############################################################################################################################



def client_audio_stream():
	global audio_files_processing
	global temp_count
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
	client_socket_address = (client_host_ip, client_port-1)
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
				print("Saving client side audio "+str(temp_count))
				client_temp_time = time.localtime()
				client_current_time = time.strftime("%H$%M$%S", client_temp_time)
				temp_client_audiofile_name = "temp_dir/client__"+str(temp_count)+"_"+str(client_current_time)+".wav"
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
				temp_count = temp_count+1
				#print("completed saving audio")
			client_fame_count = client_fame_count + 1

		except:	
			break

	client_socket.close()
	print('Audio closed')
	os._exit(1)
	

t1 = threading.Thread(target=server_audio_stream, args=())
t2 = threading.Thread(target=client_audio_stream, args=())
t3 = threading.Thread(target=whisper_processing, args=())

t1.start()

time.sleep(10)
t2.start()
t3.start()

