Dummy ChatGPT Microservice with Ollama LLM :
This is a simple microservice application built using Python, Flask, Docker, and Ollama LLM. It takes input from the user, sends the input to the Ollama API, and displays the response below the input box on a web page.

Project Structure
app.py – The main Flask backend file that handles routing and interacts with the Ollama API.
static/ – Folder for static assets (CSS, JS).
templates/ – Folder for HTML files.
Dockerfile – A Dockerfile to create a Docker container for the Flask application.
requirements.txt – List of dependencies for the project.
Setup & Installation
Prerequisites
Make sure you have the following tools installed:

Docker
Python 3.x
Postman (for testing the API)
Steps to Run the Project
1. Clone the repository
https://github.com/Prernagupta2226/MicroStudio.git
2. Install Python Dependencies
You can install the required dependencies using pip:
pip install -r requirements.txt
3. Docker Setup
You can also run the application inside a Docker container. Build the Docker image with:
docker build -t chatgpt-microservice .
After the image is built, you can run the container:
docker run -p 5000:5000 chatgpt-microservice
4. Run Flask Application
Alternatively, you can run the Flask application locally without Docker:
python app.py
5. Accessing the Application
Once the app is running, open a browser and go to http://localhost:5000.
You should see a simple form to input text.
Enter any query and click "Submit" to get a response from the Ollama LLM.
6. Interacting with the Ollama API
In the backend (app.py), Flask receives the user input and sends it to the Ollama LLM via a POST request using the Postman API. The response from Ollama is then displayed back on the page.

File Descriptions
app.py
This is the core of the Flask application. It defines the routes for receiving and sending user input.

templates/index.html
The HTML form for accepting user input.

static/css/style.css
Basic styling for the input form and response area.

static/js/script.js
Handles the frontend logic for sending user input and updating the page dynamically with the response.

Dockerfile
Contains instructions to create a Docker image for running the Flask application in a containerized environment.

requirements.txt
Contains a list of Python dependencies. For this project, it includes:

Flask
Requests
Contributing
If you'd like to contribute to this project, feel free to open a pull request. Please make sure to follow the code style and conventions used in the project.

