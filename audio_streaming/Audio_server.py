# This is server code to send video and audio frames over TCP

import socket
import threading, wave, pyaudio,pickle,struct

host_name = socket.gethostname()
host_ip = '192.168.1.102'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9611

def audio_stream():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host_ip, (port-1)))

    server_socket.listen(5)
    CHUNK = 1024
    #wf = wave.open("temp.wav", 'rb')
    
    p = pyaudio.PyAudio()
    print('server listening at',(host_ip, (port-1)))
   
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=CHUNK)

             

    client_socket,addr = server_socket.accept()
 
    data = None
    while True:
        if client_socket:
            while True:
              
                data = stream.read(CHUNK)
                a = pickle.dumps(data)
                message = struct.pack("Q",len(a))+a
                client_socket.sendall(message)
                
t1 = threading.Thread(target=audio_stream, args=())
t1.start()

