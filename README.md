Dummy ChatGPT Microservice with Ollama LLM :
This is a simple microservice application built using Python, Flask, Docker, and Ollama LLM. It takes input from the user, sends the input to the Ollama API, and displays the response below the input box on a web page.

Project Structure: 

app.py – The main Flask backend file that handles routing and interacts with the Ollama API.
static/ – Folder for static assets (CSS, JS).
templates/ – Folder for HTML files.
requirements.txt – List of dependencies for the project.
Setup & Installation:
Prerequisites:
Make sure you have the following tools installed:
Python 3.x
Postman (for testing the API)
Steps to Run the Project:
1. Clone the repository
https://github.com/Prernagupta2226/MicroStudio.git
2. Install Python Dependencies
You can install the required dependencies using pip:
pip install -r requirements.txt
4. Run Flask Application
Whenever we run the flask application, the database is created which stores the all the prompts and responses.
Run command : python app.py
5. Run Frontend index.html:
6. Run microservice interface in the local host port number: 8080 using command : python -m http.server 8080
7. Interacting with the Ollama API
In the backend (app.py), Flask receives the user input and sends it to the Ollama LLM via a POST request using the Postman API. The response from Ollama is then displayed back on the page.

File Descriptions:

app.py
This is the core of the Flask application. It defines the routes for receiving and sending user input.

templates/index.html
The HTML form for accepting user input.

static/css/style.css
Basic styling for the input form and response area.

static/js/script.js
Handles the frontend logic for sending user input and updating the page dynamically with the response.

requirements.txt
Contains a list of Python dependencies. For this project, it includes:
Flask
Requests
Contributing

If you'd like to contribute to this project, feel free to open a pull request. Please make sure to follow the code style and conventions used in the project.

