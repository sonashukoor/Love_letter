from flask import Flask, request, render_template, jsonify 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    # Get JSON data from the frontend
    data = request.get_json()
    
    # Extract message and receiver email from the JSON payload
    message = data.get("message")
    receiver_email = data.get("email")
    
    # Validate if both message and email are provided
    if not message or not receiver_email:
        return jsonify({"message": "Message and receiver email cannot be empty"}), 400
    
    # Email credentials (use environment variables for security in production)
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD") # Use your generated App Password
    
    # Create the email structure
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "A Love Letter for You"

    custom_link = "https://drive.google.com/file/d/1TYrUIOxcJdE5A799dmVSFK1rmqaOmkFw/view?usp=sharing "
    full_message = f"{message}\n\nP.S. Your love made this for you: {custom_link}"

    msg.attach(MIMEText(full_message, 'plain'))
    
    try:
        # Connect to Gmail's SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Login to the email account
        server.sendmail(sender_email, receiver_email, msg.as_string())  # Send the email
        server.quit()  # Close the connection
        
        return jsonify({"message": "Love letter sent successfully!"})
    
    except Exception as e:
        # Handle any exceptions during the email sending process
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)