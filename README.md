# IntelliMeet
Repository for CS 5704 Software Engineering project.

# IntelliMeet: AI-Enabled Decentralized Video Conferencing Application.

Introduction: ‘IntelliMeet’ is a peer-to-peer video conferencing application that is decentralized and combines federation learning techniques [3] with machine learning techniques to robustly automate minutes of meetings and analyze participant attentiveness. IntelliMeet enhances user privacy through peer-to-peer federation learning training mechanisms. Meeting attendees multitask while attending remote or virtual meetings, which can negatively affect teamwork and collaboration. IntelliMeet addresses this issue by using machine learning and pose-aware computer vision techniques to identify whether participants are paying attention, thereby encouraging more active participation and reducing the likelihood of multitasking. Furthermore, the application implements a log-mel transformer to automatically convert meeting speech to text in real-time; and GPT-based natural language processing techniques to analyze transcribed meeting notes to generate minutes of meetings via email triggers to meeting participants. This reduces participant workloads and increases productivity. The features of IntelliMeet, along with its architecture efficiency and automation capabilities, will provide a secure and private video conferencing experience that will enhance teamwork and collaboration. With the increase in remote work, IntelliMeet can play a crucial role in helping organizations and individuals achieve their productivity goals.

# APPLICATION PIPELINE:
![alt text](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/diagrams/pipeline.png)


## DESCRIPTION of ML FEATURE 1
The ML feature 1 utilizes facial detection and pose estimation algorithms, which are based on the RetinaFace architecture. The RetinaFace architecture [1] comprises a multi-stage convolutional neural network that uses a multi-task loss function. It has a context module that aids in effectively detecting and localizing faces and facial features within images or videos. To ensure efficient face detection, the multi-task loss function employs four different loss functions. The face detection algorithm in IntelliMeet locates the face within the input by identifying its x and y coordinates, while the pose estimation algorithm analyzes video frames and localized face coordinates to estimate the pose angles of the detected faces in real-time. By analyzing the facial coordinates and pose angles of participants in the video frame, ML feature 1 calculates their attention levels throughout the meeting. After the scheduled meeting concludes, participants receive an automatic attention analysis report via email.
![alt text](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/facial_analysis/curve/Screenshot%202023-05-06%20024354.jpg)

## DESCRIPTION of ML FEATURE 2
IntelliMeet uses two modules for speech-to-text transcription and text analysis. The speech-to-text transcription module is modeled after OpenAI's Whisper [2] and adopts a transformer-based CNN-RNN architecture with CTC loss function. This module processes audio sequences into log-mel spectrograms, and utilizes a beam search algorithm for real-time transcription. The speech transcription model used in IntelliMeet has ~78M parameters and takes up 470 MB of memory space. After transcription, the NLTK based text pre-processing algorithm is applied to remove text noises and correct any grammatical errors. The processed text is then sent to the text analysis module to generate the minutes of the meeting (MoM), which includes meeting notes, task reminders, and alerts. Once the MoM is created, it is automatically sent to each participant via email.
![alt text](https://raw.githubusercontent.com/openai/whisper/main/approach.png)

# USE-CASES IMPLMENTED
## Use Case 1: The camera streams of all participants are directed to the ML Feature 1 pipeline to undergo facial analysis and pose estimation. The facial analysis algorithm identifies each participant, while the pose estimation algorithm analyzes each individual's attention to create a customized attention report based on meeting timestamps. This report details the timestamps where the participant was not attentive and provides information on the meeting context that they may have missed. The personalized meeting attention reports are then emailed to each participant.
![alt text](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/diagrams/use-case-3.png)

## Use Case 2 (PARTIALLY IMPLEMENTED): The audio streams of all participants are directed to the ML Feature 2 pipeline for speech-to-text transcription and subsequent text analysis. The text-to-speech feature in ML Feature 2 transcribes the audio streams of each participant to text based on their participant ID. These transcripts are then processed by a text analysis module to generate a meeting summary. Additionally, text scraping is carried out on the transcripts to generate an email that consolidates all the issues, dependencies, tasks, or events that were discussed during the meeting.
![alt text]([https://raw.githubusercontent.com/openai/whisper/main/approach.png](https://github.com/niknarra/SE-Project---IntelliMeet/blob/main/diagrams/User%20Case%202.png))


# ENVIRONMENT SETUP:

# DEPENDENCIES INSTALLATION (Python Packages):

# NOTE:

# STEPS TO RUN THE PROGRAM

# APPLICATION TESTING DETAILS

## For more information on the facial analysis module
Refer to this [[paper]] [https://arxiv.org/abs/1905.00641], [[above directory]] [https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/facial_analysis], and [[parent repository]] [https://github.com/biubug6/Pytorch_Retinaface]

## For more information on the speech-to-text transcription module
Refer to this [[paper]] [https://arxiv.org/abs/2212.04356], above [[directory]] [https://github.com/niknarra/SE-Project---IntelliMeet/tree/main/audio_streaming], and [[parent repository]] [https://github.com/openai/whisper]

# REFERENCES
[1] J Deng, J Guo, E Ververas, I Kotsia, and S Zafeiriou. 2020. RetinaFace: Single- Shot Multi-Level Face Localisation in the Wild. In 2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 5202–5211.
[2] Alec Radford, Jong Wook Kim, et al. 2022. Robust Speech Recognition via Large-Scale Weak Supervision. In Arxiv. https://doi.org/10.48550/arXiv.2212. 04356Focustolearnmore.
[3] Yang, Qiang, Liu, et al. 2019. Federated Machine Learning: Concept and Applications. ACM Transactions on Intelligent Systems and Technology 10, 2 (2019), 1–19. 10.1145/3298981

# DONE by FORE-MEMBERS
-> Premith Kumar Chilukuri (VTID: cpremithkumar) (GitHub ID: chpk)
-> Nikhil Narra (VTID: nikhilnarra) (GitHub ID: niknarra)
-> Krishna vamsi Dhulipalla (VTID: kdhulipalla13) (GitHub ID: krishna-creator)
-> Siva sagar Kolachina (VTID: sivasagar) (GitHub ID: siva-sagar)
