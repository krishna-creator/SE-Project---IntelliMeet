import socket, cv2, pickle,struct,imutils
import threading
import time
from video_face_detect import call_face_detection
import json
# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
reciever_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # nature of scoket


#host_name  = socket.gethostname()
host_ip = '10.0.0.31'
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)

reciever_IP_address = '10.0.0.31'
reciever_port_address = 9998
reciever_socket_address = (reciever_IP_address, reciever_port_address)
# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(1)
video_frames_processing = []
sequence_count = 0
file_save_flag = 0
face_analysis_results = []
json_filename = "face_detection_results.json"

def get_time():
    temp_time = time.localtime()
    current_time = time.strftime("%H$%M$%S", temp_time)
    return str(current_time)
    
#{sequence_count: ["server", str(current_server_time), frame]}

def json_filecreation(temp_sequence_count, temp_name, temp_time, ret_status):
    global file_save_flag
    global face_analysis_results
    #print(input_file_type, input_file_time, input_file_sequence)
    try:
        temp_dict = {}
        with open(json_filename, "w") as file:
            if file_save_flag ==1:
                #temp_contents = file.read()
                #temp_read_data = json.load(file)
                temp_dict[temp_sequence_count] = {temp_name: [[temp_time], [ret_status]] }
                face_analysis_results.append(temp_dict)
                #file.seek(0)
                json.dump(face_analysis_results, file)
                #file_save_flag = file_save_flag+1
            else:
                temp_dict[temp_sequence_count] = {temp_name: [[temp_time], [ret_status]] }
                face_analysis_results.append(temp_dict)
                json.dump(face_analysis_results, file)
                file_save_flag = 1
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
            result, ret_status = call_face_detection(temp_video_frame)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(ret_status)
            json_filecreation(temp_sequence_count, temp_name, temp_time, ret_status)
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
        			frame = imutils.resize(frame,width=720)
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
    
    
x1 = threading.Thread(target = sending_data)
x2 = threading.Thread(target = video_retinaface_processing)
x3 = threading.Thread(target = recieving_data)

x1.start()
x3.start()
time.sleep(30)
x2.start()


x1.join()
x2.join()
x2.join()