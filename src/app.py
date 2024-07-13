from flask import Flask, request, send_file
from celery import Celery
from flask_mail import Mail, Message
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch sensitive information from environment variables
email_username = os.getenv('EMAIL_USERNAME')
email_password = os.getenv('EMAIL_PASSWORD') 

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = email_username
app.config['MAIL_PASSWORD'] = email_password
mail = Mail(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Logging configuration
log_file_path = '/var/log/messaging_system.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

@celery.task(bind=True, max_retries=3, default_retry_delay=30)
def send_async_email(self, recipient):
    with app.app_context():
        msg = Message('Hello', sender=email_username, recipients=[recipient])
        msg.body = 'This is a test email sent from a Flask application using Celery and RabbitMQ.'
        try:
            mail.send(msg)
            logging.info(f'Email sent to {recipient} at {datetime.now()}')
        except Exception as exc:
            logging.error(f'Error sending email: {exc}')
            self.retry(exc=exc)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    if sendmail:
        send_async_email.delay(sendmail)
        logging.info(f'Email queued to {sendmail} at {datetime.now()}')
        return f'Email has been queued to {sendmail}'
    
    if talktome is not None:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'{current_time}: talktome endpoint was called\n')
        logging.info('{current_time}: talktome endpoint was called')
        return 'Current time has been logged.'

    return 'Please provide a valid parameter.'


@app.route('/log')
def get_log():
    try:
        return send_file(log_file_path, as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)