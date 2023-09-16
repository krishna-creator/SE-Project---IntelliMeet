# Details of IntelliMeet's Black Box testing

## Environment Setup:
* Installing python language in your PC/Laptop, for more details [refer to] (https://www.tutorialspoint.com/how-to-install-python-in-windows)
* Install miniconda terminal in your PC/Laptop, for more detils [refer to] (https://docs.conda.io/en/latest/miniconda.html)
* create a "conda environment" using the following command ```conda create --name intellimeet```, after creating the envoronment for intellimeet, activate the environment by executing ```conda activate intellimeet```.

## Python Libraries/Dependecy Installation:
* Install the following python libraries that are required to run the unit test cases
```bash
# install json library
pip install json # if this command dosent work try the below one
pip3 install json

# install matplotlib library
pip install matplotlib  # if this command dosent work try the below one
pip3 install matplotlib

# install OpenCV library
pip install opencv-python # if this command dosent work try the below one
pip3 install opencv-python

# install imutils library
pip install imutils # if this command dosent work try the below one
pip3 install imutils

# install PIP library
pip install --upgrade Pillow # if this command dosent work try the below one
pip3 install --upgrade Pillow

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

## STEPS ON HOW TO RUN THE UNIT TEST CASES
* setup the unit test case environment as mentioned above
* Install the necessary python libraries (as mentioned above) that are required to run the unit-box test case
```shell
# check if the transfered image has width, height and depth of 360px, 462, 3
python -m unittest Image_data_transfer_unit_test_1.py

# check if the transfered image has width of 360px
python -m unittest Image_data_transfer_unit_test_2.py

# check if the transfered image has width of 360px by "asserNotEqual" function
python -m unittest Image_data_transfer_unit_test_3.py

# checking if the email authentication service is from OUTLOOK
python -m unittest unit_test_1.py

# Validating if the email address to send are "sid2lose@outlook.com", "ch.premith.k@gmail.com"
python -m unittest unit_test_2.py

# validating if the email's subject is "Personlized Meeting Attentiveness summary"
python -m unittest unit_test_3.py

# validating if the email's subject is "Personlized Meeting Attentiveness summary" by "asserNotEqual" function
python -m unittest unit_test_4.py

# validating host email address
python -m unittest Unit_Test_Meeting_data_retrival.py

# validating host IP ADDRESS
python -m unittest Unit_Test_Meeting_data_retrival_1.py

# validating receiver IP ADDRESS
python -m unittest Unit_Test_Meeting_data_retrival_2.py

# validating receiver email address
python -m unittest Unit_Test_Meeting_data_retrival_3.py

# validating receiver port address
python -m unittest Unit_Test_Meeting_data_retrival_4.py

# validating host/server's port address
python -m unittest Unit_Test_Meeting_data_retrival_5.py
```
