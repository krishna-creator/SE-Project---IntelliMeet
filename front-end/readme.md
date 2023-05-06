# UI Development !!

# Intellimeet

Intellimeet is a Flask-based web application that allows you to create a meeting room and send invites to participants via email. It provides a user-friendly interface for adding participants and managing the invitation process.

## Features

- Create a meeting room by adding participants' information.
- Display the list of invited participants.
- Send email invites to participants with attached JSON file.
- Form validation for input fields.
- Responsive design for optimal viewing on various devices.

## Installation

1. Clone the repository:

```shell
git clone https://github.com/niknarra/SE-project---intellimeet.git
```

2. Navigate to the project directory:

```shell
cd intellimeet
```

3. Install the required dependencies using pip:

```shell
pip install -r requirements.txt
```

4. Set up environment variables:
Create a .env file in the project root directory.
Add the following line to the .env file and replace your_password with the password for the sender email account:

```shell
PASSWORD=your_password
```
## Usage

1. Run the application:

```shell
python app.py
```

2. Access the application in your web browser at http://localhost:5000.

3. Fill in the participant details in the form and click "ADD" to add them to the list.

4. To send invites, click the "Send Invites" button. Invites will be sent to all participants via email, with a JSON file attachment containing the form data.

## Contributing
Contributions to Intellimeet are welcome! If you have any bug fixes, improvements, or new features to add, please follow these steps:

1. Fork the repository.

2. Create a new branch for your feature:

```shell
git checkout -b feature/your-feature-name
```

3. Commit your changes and push to the branch:

```shell
git commit -am "Add your commit message"
git push origin feature/your-feature-name
```

4. Create a pull request on GitHub.
