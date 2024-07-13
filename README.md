## Introduction
This project is a messaging system that supports sending emails and logging events. The system is built using Flask, with Celery for handling asynchronous email sending tasks and Flask-Mail for sending the emails. The project uses `python-dotenv ` to manage sensitive information like email credentials.

## Technologies Used
- Flask: A micro web framework for Python.
- Celery: An asynchronous task queue/job queue.
- Flask-Mail: An extension for Flask to handle email sending.
- RabbitMQ: The message broker used by Celery.
- python-dotenv: A library to load environment variables from a `.env ` file.
- Logging: Python's built-in logging module for logging events.

## Project Setup
### Prerequisites
- Python 3.x
- RabbitMQ server
- Virtual environment (optional but recommended)
### Installation
**Clone the repository:**
```
git clone https://github.com/yourusername/messaging_system.git
cd messaging_system
```bash

**Create and activate a virtual environment:**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
**Install dependencies:**
```
pip install -r requirements.txt
```

### Configuration
Create a `.env`file in the project root directory:
```
# .env file
EMAIL_USERNAME=
EMAIL_PASSWORD=
```

Configure Flask-Mail and Celery in the `app.py` file:

The email credentials and other configuration settings are loaded from the environment variables defined in the .env file.
```
from dotenv import load_dotenv
import os

load_dotenv()

email_username = os.getenv('EMAIL_USERNAME')
email_password = os.getenv('EMAIL_PASSWORD')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = email_username
app.config['MAIL_PASSWORD'] = email_password

app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
```

##Running the Application
**Start the RabbitMQ server:**

Ensure that RabbitMQ is running on your local machine. If not, you can start it using:
```
rabbitmq-server
```

**Start the Celery worker:**

Open a new terminal window and start the Celery worker:
```
celery -A app.celery worker --loglevel=info
```
Run the Flask application:
```
flask run
```

### Endpoints
`GET /: `The main endpoint to trigger email sending and logging.

Query parameters:
`sendmail: ` The recipient email address to send an email.
`talktome: ` Any value to trigger logging of the current time.
`GET /log: ` Endpoint to download the log file.

### Logging
Logging is configured to write to /var/log/messaging_system.log. The application logs email sending events and accesses to the talktome endpoint with timestamps.

