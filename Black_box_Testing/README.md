## Details for Black Box testing will be added here


## NOTE: 
#### Generic black-box testing can't be performed because the usecases require high computational power to execute. The following are the compulsory requirements to execute a generic Usecase 1 blackbox testing: client-server architecure, CUDA, NVIDIA GTX/RTX GPU, Intel <i7 9th gen processors.


## NOTE (Proves USE CASE 1): 
#### So to ease the process of blackbox testing in this case (consider TC_001 and TC_002), i.e for any user to execute the the functionality of UseCase 1, we have fragmented a piece of code in IntelliMeet, which considers already generated (PRE-BUILT) meeting notes and participant's attentiveness report to generate personalized meeting attention report.


## Environment Setup:
-> Installing python language in your PC/Laptop, for more details [refer to] (https://www.tutorialspoint.com/how-to-install-python-in-windows)
-> Install miniconda terminal in your PC/Laptop, for more detils [refer to] (https://docs.conda.io/en/latest/miniconda.html)
-> create a "conda environment" using the following command ```conda create --name intellimeet```, after creating the envoronment for intellimeet, activate the environment by executing ```conda activate intellimeet```.


## Python Libraries/Dependecy Installation:
-> Install the following python libraries that are required to run the black-box test case
```bash
# install json library
pip install json # if this command dosent work try the below one
pip3 install json

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
```

## BLACK-BOX TEST CASES

### Test ID: TC_001

-> Description: Proves Use Case 1, check if personalized meeting reports are sent to “dcbrown@vt.edu” and “smgruber@vt.edu” emails.

-> Pre-Conditions:
* The user must have a stable internet condition
* The user must have an active VT email ID
* The user must set up the testing environment by following the steps mentioned in “Environment Setup” Sub Section.
* The user must install all the necessary python libraries and dependencies by following the steps mentioned in “Python Libraries/Dependencies Installation” Sub Section.
* The user must clone the repository that includes /Black_box_Testing directory.
* The user must make sure that the files present in the /Black_box_Testing directory are present without fail. Necessary files are “audio_results.json”, “face_detection_results.json”, “form_data.json”, “meeting_notes.txt”, and “black_box_test_case.py”.

-> Steps:
* Clone the repository using ```https://github.com/niknarra/SE-Project---IntelliMeet.git```
* Navigate to the ```/Black_box_Testing/``` directory
* Open a terminal in the ```/Black_box_Testing/``` directory 
* Then run the “black_box_test_case.py” code, using the following command ```python black_box_test_case.py```, if an error is faced, execute the following command ```python3 black_box_test_case.py```
* Wait for 5 to 10 seconds and then check email if personalized meeting summaries are received from “sid2lose@outlook.com” email.
* If an email is not received, please check the spam folder in your email.

-> Expected Output:
* After executing “black_box_test_case.py”, the user should receive an email from “sid2lose@outlook.com”, which consists of personalized meeting summaries.
* If any error is faced or files are missing in the code, “please check the dependencies” error message will be displayed. 

-> Actual Result: 
* Successfully received an email from “sid2lose@outlook.com”, which consists of personalized meeting summaries.



### Test ID: TC_002

-> Description: Proves Use Case 1, check if participants attentiveness graphs are stored locally.

-> Pre-Conditions:
* The user must set up the testing environment by following the steps mentioned in “Environment Setup” Sub Section.
* The user must install all the necessary python libraries and dependencies by following the steps mentioned in “Python Libraries/Dependencies Installation” Sub Section.
* The user must clone the repository that includes /Black_box_Testing directory.
* The user must make sure that the files present in the /Black_box_Testing directory are present without fail. Necessary files are “audio_results.json”, “face_detection_results.json”, “form_data.json”, “meeting_notes.txt”, and “black_box_test_case.py”.

-> Steps:
* Clone the repository using ```https://github.com/niknarra/SE-Project---IntelliMeet.git```
* Navigate to the ```./Black_box_Testing/``` directory
* Open a terminal in the ```./Black_box_Testing/``` directory 
* Then run the “black_box_test_case.py” code, using the following command ```python black_box_test_case.py```, if an error is faced, execute the following command ```python3 black_box_test_case.py```
* Wait for 5 to 10 seconds and then check if the meeting attention graphs of participants “participant_1.png” and “participant_2.png” are stored locally.

-> Expected Output:
* After executing “black_box_test_case.py”, the user should be able to see 2 attention graphs stored locally in the “./Black_box_Testing/” directory.
* If any error is faced or files are missing in the code, “please check the dependencies” error message will be displayed. 

-> Actual Result: 
* Successfully saved 2 meeting attention graphs in the “./Black_box_Testing/” directory.

