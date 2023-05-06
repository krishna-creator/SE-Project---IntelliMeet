# IntelliMeet
Repository for CS 5704 Software Engineering project.

# IntelliMeet: AI-Enabled Decentralized Video Conferencing Application.
### Introduction: 
‘IntelliMeet’ is a peer-to-peer video conferencing application that is decentralized and combines federation learning techniques [3] with machine learning techniques to robustly automate minutes of meetings and analyze participant attentiveness. IntelliMeet enhances user privacy through peer-to-peer federation learning training mechanisms. Meeting attendees multitask while attending remote or virtual meetings, which can negatively affect teamwork and collaboration. IntelliMeet addresses this issue by using machine learning and pose-aware computer vision techniques to identify whether participants are paying attention, thereby encouraging more active participation and reducing the likelihood of multitasking. Furthermore, the application implements a log-mel transformer to automatically convert meeting speech to text in real-time; and GPT-based natural language processing techniques to analyze transcribed meeting notes to generate minutes of meetings via email triggers to meeting participants. This reduces participant workloads and increases productivity. The features of IntelliMeet, along with its architecture efficiency and automation capabilities, will provide a secure and private video conferencing experience that will enhance teamwork and collaboration. With the increase in remote work, IntelliMeet can play a crucial role in helping organizations and individuals achieve their productivity goals.

## DEVELOPED by THE FORE-MEMBERS
* Premith Kumar Chilukuri (VTID: cpremithkumar) (GitHub ID: chpk)
* Nikhil Narra (VTID: nikhilnarra) (GitHub ID: niknarra)
* Krishna vamsi Dhulipalla (VTID: kdhulipalla13) (GitHub ID: krishna-creator)
* Siva sagar Kolachina (VTID: sivasagar) (GitHub ID: siva-sagar)

## APPLICATION PIPELINE:
![alt text](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/diagrams/pipeline.png)


### DESCRIPTION of ML FEATURE 1
The ML feature 1 utilizes facial detection and pose estimation algorithms, which are based on the RetinaFace architecture. The RetinaFace architecture [1] comprises a multi-stage convolutional neural network that uses a multi-task loss function. It has a context module that aids in effectively detecting and localizing faces and facial features within images or videos. To ensure efficient face detection, the multi-task loss function employs four different loss functions. The face detection algorithm in IntelliMeet locates the face within the input by identifying its x and y coordinates, while the pose estimation algorithm analyzes video frames and localized face coordinates to estimate the pose angles of the detected faces in real-time. By analyzing the facial coordinates and pose angles of participants in the video frame, ML feature 1 calculates their attention levels throughout the meeting. After the scheduled meeting concludes, participants receive an automatic attention analysis report via email.
![alt text](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/facial_analysis/curve/Screenshot%202023-05-06%20024354.jpg)

### DESCRIPTION of ML FEATURE 2
IntelliMeet uses two modules for speech-to-text transcription and text analysis. The speech-to-text transcription module is modeled after OpenAI's Whisper [2] and adopts a transformer-based CNN-RNN architecture with CTC loss function. This module processes audio sequences into log-mel spectrograms, and utilizes a beam search algorithm for real-time transcription. The speech transcription model used in IntelliMeet has ~78M parameters and takes up 470 MB of memory space. After transcription, the NLTK based text pre-processing algorithm is applied to remove text noises and correct any grammatical errors. The processed text is then sent to the text analysis module to generate the minutes of the meeting (MoM), which includes meeting notes, task reminders, and alerts. Once the MoM is created, it is automatically sent to each participant via email.
![alt text](https://raw.githubusercontent.com/openai/whisper/main/approach.png)

## USE-CASES IMPLMENTED
### Use Case 1: 
The camera streams of all participants are directed to the ML Feature 1 pipeline to undergo facial analysis and pose estimation. The facial analysis algorithm identifies each participant, while the pose estimation algorithm analyzes each individual's attention to create a customized attention report based on meeting timestamps. This report details the timestamps where the participant was not attentive and provides information on the meeting context that they may have missed. The personalized meeting attention reports are then emailed to each participant.
![alt text](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/diagrams/use-case-3.png)

### Use Case 2 (PARTIALLY IMPLEMENTED): 
The audio streams of all participants are directed to the ML Feature 2 pipeline for speech-to-text transcription and subsequent text analysis. The text-to-speech feature in ML Feature 2 transcribes the audio streams of each participant to text based on their participant ID. These transcripts are then processed by a text analysis module to generate a meeting summary. Additionally, text scraping is carried out on the transcripts to generate an email that consolidates all the issues, dependencies, tasks, or events that were discussed during the meeting.
![alt text](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/diagrams/User%20Case%202.png)

## NOTE:
#### Execution/building IntelliMeet project requires high computational power. Also, as the application is not deployed, it will be bit tricky to run the application, because the server and client codes should have to be executed simultaneously in-order to work properly during data transmission. Moreover, the following are the  requirements to run IntelliMeet: 
* 20+ dependencies
* client-server architecure support
* CUDA
* NVIDIA GTX/RTX GPU (with VRAM capacity <= 6GB)
* greater than Intel i7 9th gen processors for CPU
* RAM capacity <8 GB
* Proper Internet Connection.

## ENVIRONMENT SETUP:
* Installing ```python3 language``` in your PC/Laptop, for more details [refer to] (https://www.tutorialspoint.com/how-to-install-python-in-windows), Generally Python3 is pre-built for Linux.
* Install ```miniconda terminal``` in your PC/Laptop, for more detils [refer to] (https://docs.conda.io/en/latest/miniconda.html)
* create a "conda environment" using the following command ```conda create --name intellimeet``` 
* after creating the environment for intellimeet, activate the environment by executing ```conda activate intellimeet```.
* install ffmpeg on your device, follow the instruction provided in this [link for windows] (https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) or [this link for linux] (https://phoenixnap.com/kb/install-ffmpeg-ubuntu).
* repeat the above steps for all the computers/devices in which you are planning to run IntelliMeet.


## DEPENDENCIES INSTALLATION (Python Packages):
Install the following python libraries that are required to run the application (we are implementing the application in python3)
```bash
# [important note:] INSTALL PyTORCH library (installation process will be difffrent for every OS and GPU support) by following the documentationof in this link "https://pytorch.org/get-started/locally/"

# install json library
pip install json # if this command dosent work try the below one
pip3 install json

# install argparse library
pip install argparse # if this command dosent work try the below one
pip3 install argparse

# install numpy library
pip install numpy
pip3 install numpy

# install OpenCV library
pip install opencv-python # if this command dosent work try the below one
pip3 install opencv-python

# install Sockets library
pip install sockets # if this command dosent work try the below one
pip3 install sockets

# install struct library
pip install supyr-struct # if this command dosent work try the below one
pip3 install supyr-struct

# install imutils library
pip install imutils # if this command dosent work try the below one
pip3 install imutils

# install time library
pip install python-time # if this command dosent work try the below one
pip3 install python-time

# Manually install portaudio library

# install pyaudio library
pip install PyAudio # if this command dosent work try the below one
pip3 install PyAudio

# install wave library
pip install Wave # if this command dosent work try the below one
pip3 install Wave
pip install PyWave # if this command dosent work try the below one
pip3 install PyWave

# install PIP library
pip install --upgrade Pillow # if this command dosent work try the below one
pip3 install --upgrade Pillow

install whisper library
pip install -U openai-whisper # if this command dosent work try the below one
pip3 install -U openai-whisper
pip install setuptools-rust # if this command dosent work try the below one
pip install setuptools-rust

# install transformers library
pip install transformers # if this command dosent work try the below one
pip3 install transformers

# install matplotlib library
pip install matplotlib  # if this command dosent work try the below one
pip3 install matplotlib

# install smtplib library
pip install secure-smtplib  # if this command dosent work try the below one
pip3 install secure-smtplib

# install mime library
pip install mime  # if this command dosent work try the below one
pip3 install mime

# install email library
pip install email  # if this command dosent work try the below one
pip3 install email

# install flask library for UI
pip install Flask  # if this command dosent work try the below one
pip3 install Flask

# install tKinter library for UI
pip install tk  # if this command dosent work try the below one
pip3 install tk

# install dotenv library for UI
pip install python-dotenv  # if this command dosent work try the below one
pip3 install python-dotenv
```


## STEPS TO RUN THE APPLICATION
### How to send meeting invites using the meeting registration page
* Clone the repository using ```https://github.com/niknarra/SE-Project---IntelliMeet.git```
* Navigate to ```./front-end/``` directory.
* run the app.py using ```python app.py``` command (if that didn't work, try this) ```python3 app.py``` command
* open a browser and then enter the following [url] (http://localhost:5000/)
* enter the meeting details (ADD a total of 2 participants only)
* click on "send invite" button, an email containing "form_data.json" will be mailed to you.
* place the "form_data.json" in ```SE-Project---IntelliMeet``` repository.

### Steps to run the application at server-side (i.e computational HUB, note this device should have high computational power.)
* Clone the repository using ```https://github.com/niknarra/SE-Project---IntelliMeet.git``` (Ignore if already done)
* Navigate to ```SE-Project---IntelliMeet``` repository using ```cd ./SE-Project---IntelliMeet/```
* Download the latest "form_data.json" meeting invite from your email
* Make sure your have the latest "form_data.json" file locally in the ```SE-Project---IntelliMeet``` repository
* Download the ML feature 1 (facial analysis) model weights by following the instructions specified in this [link] (https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/weights)
* place the downloaded weight files in the ```./weights/``` directory itself.
* Make sure if your have "audio_results.json", "error.jpg", "face_detection_results.json", "form_data.json", "graph_plotting.py", "meeting_notes.txt", "mic_video_buttons.jpg", "video_face_detect.py" files locally in the ```./SE-Project---IntelliMeet/``` directory.
* Now, run the "Modified_UI_computational_video_audio_server.py" file using ```python Modified_UI_computational_video_audio_server.py``` command, (if that didn't work, try this) ```python Modified_UI_computational_video_audio_server.py``` command
* Now wait till the meeting UI pops up, once its pops up start your meeting with the other participant (i.e. the person on the client side (steps on how to run the application at client side is provided below))
* close the UI by clicking the cross button (located on top-right), and then stop the code execution in terminal to completely stop the execution of IntelliMeet.

### Steps to run the application at server-side (i.e computational HUB, note this device should have high computational power.)
* Clone the repository using ```https://github.com/niknarra/SE-Project---IntelliMeet.git``` (Ignore if already done)
* Navigate to ```SE-Project---IntelliMeet``` repository using ```cd ./SE-Project---IntelliMeet/```
* Download the latest "form_data.json" meeting invite from your email
* Make sure your have the latest "form_data.json" file locally in the ```SE-Project---IntelliMeet``` repository
* Now, run the "UI_Video_Audio_client_transmisson.py" file using ```python UI_Video_Audio_client_transmisson.py``` command, (if that didn't work, try this) ```python UI_Video_Audio_client_transmisson.py``` command
* Now wait till the meeting UI pops up, once its pops up start your meeting with the other participant (i.e. the person on the server side (steps on how to run the application at siver side is provided above))
* close the UI by clicking the cross button (located on top-right), and then stop the code execution in terminal to completely stop the execution of IntelliMeet.


## APPLICATION TESTING DETAILS
### Unit Testing
* For more details on IntelliMeet's Unit Testing refer to the [following directory] [https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/Unit_Tests]
* The Above directory consists of dependency installation instructions and some sample unit test cases which were done during the testing phase of IntelliMeet.

### Black-Box testing
* For more details on IntelliMeet's Black-Box Testing refer to the [following directory] [https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/Black_box_Testing]
* The Above directory consists of dependency installation instructions, black-box test-plan, and a black-box test case related to Use-Case 1.
* More details regarding black-box testing on the meeting registration page can be found [here] (https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/front-end/BlackBox_TestCases)


## FOR INFORMATION ON FACIAL ANALYSIS MODULE
* Refer to this [paper] [https://arxiv.org/abs/1905.00641], [directory] [https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/facial_analysis], and [parent repository] [https://github.com/biubug6/Pytorch_Retinaface]
## FOR INFORMATION ON SPEECH-TO-TEXT TRANSCRIPTION MODULE
* Refer to this [paper] [https://arxiv.org/abs/2212.04356], [directory] [https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/audio_streaming], and [parent repository] [https://github.com/openai/whisper]


## REFERENCES
* [1] J Deng, J Guo, E Ververas, I Kotsia, and S Zafeiriou. 2020. RetinaFace: Single- Shot Multi-Level Face Localisation in the Wild. In 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 5202–5211.
* [2] Alec Radford, Jong Wook Kim, et al. 2022. Robust Speech Recognition via Large-Scale Weak Supervision. In Arxiv. https://doi.org/10.48550/arXiv.2212. 04356Focustolearnmore.
* [3] Yang, Qiang, Liu, et al. 2019. Federated Machine Learning: Concept and Applications. ACM Transactions on Intelligent Systems and Technology 10, 2 (2019), 1–19. 10.1145/3298981

## Issue Tracking and Project Planning
* We used [GitHub issues] (https://github.com/niknarra/SE-Project---IntelliMeet/issues?q=is%3Aopen) to track and resolve the issues.
* we used [GitHub's Kanban board] (https://github.com/users/niknarra/projects/1) for task planning, estimation, scheduling, and prioritization.

## Link for Project DEMO
* [Google Drive Link] (https://drive.google.com/file/d/1S2qJ1yGH0lBaoXBXXAPqjtfLwIzaFg08/view?usp=sharing)

