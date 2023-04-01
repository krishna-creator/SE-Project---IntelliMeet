# Video and Audio Streaming Services of IntelliMeet !!

## Implemented P2P Video streaming service using UDP protocol (via peer-peer IP:Port_Address binding)
- Using Socket IO connections the video frames are transfered between two users in real-time.
- For more details go to ```./video_streaming/``` directory.

## Implemented P2P Audio streaming service using TCP protocol (via peer-peer IP:Port_Address binding)
- Using Socket IO connections the audio bytes frames are transfered between two users in real-time.
- Real time Speech-Text conversion is performed using OpenAI's Whisper model.
- Seperate Audio streaming services are included #computational Hub nodes and #normal peer nodes.
- For more details go to ```./audio_streaming/``` directory.
