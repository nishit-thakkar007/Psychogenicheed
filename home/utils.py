from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render,HttpResponse
from home.models import UserModel 

def send_password_reset_email(request, email):
    try:
        user = UserModel.objects.get(email=email)  
    except User.DoesNotExist:
        return HttpResponse("Email does not exist.")

    # Generate a reset token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_url = f"{request.scheme}://{request.get_host()}/re_pass/{uid}/{token}/"

    # Construct the email message with the reset URL
    message = f"Click the link below to reset your password:\n\n{reset_url}"

    # Send the reset password email
    subject = "Password Reset Request"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return HttpResponse("Password reset link sent successfully.")

import pandas as pd
from textblob import TextBlob

def analyze_sentiment(text):
    output_txt_path = 'F://Data_Mining//output_text.txt'
    df = pd.read_csv('F://Data_Mining//chat_data (18).csv')
    text_column = 'text'

   # concatenated_text = ' '.join(df[text_column].astype(str))

    # Write the concatenated text to a text file
    """with open(output_txt_path, 'w') as txt_file:
        txt_file.write(concatenated_text)
        file_content = txt_file.read()"""

    if isinstance(text, float):
        text = str(text)

    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    return sentiment