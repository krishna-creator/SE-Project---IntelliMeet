# Video and Audio Streaming Services of IntelliMeet !!

## Implemented P2P Video streaming service using UDP protocol (via peer-peer IP:Port_Address binding)
- Using Socket IO connections the video frames are transfered between two users in real-time.

## Dependencies
#### Required python-libraries for video-streaming
- opencv-python
- pickle
- struct
- socket
- imutils

- Install above dependencies to run the video_streaming service.

## Instructions
- edit the IP and Port addresses in the server ```Video_dual_server_communication.py``` and client service files accordingly ```Video_dual_client_communication.py```
- run the ```Video_dual_server_communication.py``` and ```Video_dual_client_communication.py``` seperately in diffrent machines for video calling.
- run commands := ```python Video_dual_server_communication.py``` & ```python Video_dual_client_communication.py```