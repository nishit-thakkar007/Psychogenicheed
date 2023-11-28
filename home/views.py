from django.shortcuts import render,HttpResponse
from django.urls import reverse_lazy 
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from home.form import CustomUserCreationForm
# Create your views here.
import speech_recognition as sr
from .models import Category as CategoryModel
from .forms.category import CategoryForm
from .forms.book import bookform
from .models import book as bookmodel

from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.conf import settings
from django.core import mail
from .models import UserModel
import json

import csv
import os
import openai
from .models import OpenAIData
from .models import mcs1
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
 
openai.api_key = "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"
def download_chat_data(request,user_id):
    # Fetch all chat data from the database
    chat_data = OpenAIData.objects.filter(user_id=user_id)

    # Create the response as a CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chat_data.csv"'

    # Create a CSV writer and write the header row
    writer = csv.writer(response)
    writer.writerow(['User', 'text'])

    # Write chat data to the CSV file
    for data in chat_data:
        writer.writerow([data.user, data.prompt])

    return response



def chatapi(request):
    if request.method == "POST":
        user = request.user
        prompt = request.POST["prompt"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Save the OpenAI data to the database
        openai_data = OpenAIData(user=user,prompt=prompt, response=response.choices[0].text)
        openai_data.save()

        return JsonResponse(response)
    return HttpResponse('error')






def transcribe_speech(request):
    recognizer = sr.Recognizer()

    # Use the microphone as a source for audio
    with sr.Microphone() as source:
        print("Please speak something...")
        audio = recognizer.listen(source)
        
    language_code = 'en-US'

    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio, language=language_code)
        print("You said: " + text)
        response_data = {'transcription': text}
        return JsonResponse(response_data)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        response_data = {'error': 'Could not request results'}
        return JsonResponse(response_data)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        response_data = {'error': 'Speech recognition could not understand audio'}
        return JsonResponse(response_data)

def append_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        typed_prompt = data.get('typed_prompt', '')

        # Fetch the existing OpenAIData record
        openai_data = OpenAIData.objects.first()  # You may need to retrieve the record based on your logic

        if openai_data:
            # Append the typed prompt to the existing response
            openai_data.response += typed_prompt
            openai_data.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'No OpenAIData record found'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login_view')
    template_name = 'register.html'


def edit_profile(request):
    if request.method == 'POST':
        # Handle form submission and update the user profile
        user_profile = request.user # Assuming you have a UserProfile field in your user model
        user_profile.first_name = request.POST['first_name']
        user_profile.last_name = request.POST['last_name']
        user_profile.save()
        return redirect('profile')  # Redirect to the profile page after editing

    return render(request, 'edit_profile.html')

def home(request):
    return render(request, 'home.html')
def home_doctor(request):
    return render(request, 'home_doctor.html')

def mcs(request,user_id):
    return render(request, 'mcq.html', {'user_id': user_id})

def home1(request):
    return render(request, 'home1.html')

def register(request):
    return render(request,'home/index.html')

class Login(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'login.html'

from django.contrib.auth import authenticate,login 
from home.form import LoginForm  
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.type=="Doctor":
                login(request, user)
                return redirect('home_doctor')
            elif user is not None and user.type=="Patient":
                login(request, user)
                return redirect('home')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})   

def deleteCategory(request, id):
    #dictionary for initial data with
    #field names as keys
    context={}
    #fetch the object related to passed id
    obj=get_object_or_404(CategoryModel,id= id)
    obj.delete()
    return redirect("viewCategory")

def bookappoint(request):
    messages.get_messages(request)
    doctors = UserModel.objects.filter(type='doctor')
    return render(request,"book.html",{'doctors':doctors})

def viewCategory(request):
     context={}
     context["categories"]=CategoryModel.objects.all()

     return render(request,"view.html",context)

def bulk_upload(request):
     return render(request,"bulkUpload.html")

def pre(request):
    logged_in_user = request.user.username 
    prescription_details = bookmodel.objects.filter(name=logged_in_user)
    return render(request, 'pre.html', {'prescription_details': prescription_details})

def patientv(request,doctor_id):
      doctor = bookmodel.objects.filter(doctor_id=doctor_id)
      return render(request, 'patientv.html', {'doctor': doctor})

def upload_csv(request):
     
     if("GET" == request.method):
          return HttpResponse("Not Valid method")
     
     csv_file=request.FILES["csv_file"]
     if not csv_file.name.endswith('.csv'):
          return HttpResponse("File not valid")
     if csv_file.multiple_chunks():
          return HttpResponse("Uploaded file is big")
     file_data = csv_file.read().decode("utf-8")
     lines = file_data.split("\n")
     c=len(lines)
     #return Httpresponse(lines[0])
     for i in range(0,c-1):
          feilds = lines[i].split(",")
          data_dict = {}
          data_dict["title"] = feilds[0]
          data_dict["description"] = feilds[1]

          cform=CategoryForm(data_dict)
          if cform.is_valid():
               cform.save()

     return redirect("viewCategory")

def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="category.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description'])  # Use writer.writerow(), not writer.writerrow()

    for data in CategoryModel.objects.all():
        writer.writerow([data.title, data.description])

    return response

"""def signup(request):
    
    username=""
    userimage=""
    email=""
    first_name=""
    last_name=""
    password=""
    if request.method=="POST":
      username=request.POST.get('username')
      userimage=request.POST.get('userProfile')
      email=request.POST.get('email')
      first_name=request.POST.get('first_name')
      last_name=request.POST.get('last_name')
      password=request.POST.get('password')

    if UserModel.objects.filter(email=email).exists():
            messages.error(request, f'A booking already exists for the email {email}. Please choose a different email.')
            return redirect("register")

    
    em=UserModel(username=username,userProfile=userimage,email=email,first_name=first_name,last_name=last_name,password=password)
    em.save()
    return render(request, "login.html")"""
 
from datetime import datetime
def addbooking(request):
   
   if request.method=="POST":
    name=request.POST.get('name')
    mobilenum=request.POST.get('mobilenum')
    email=request.POST.get('email')
    date=request.POST.get('date')
    doctor_id = request.POST.get('doctor')

    try:
            doctor = UserModel.objects.get(id=doctor_id, type='doctor')
    except UserModel.DoesNotExist:
            messages.error(request, 'Invalid doctor selected.')
            return redirect("bookappoint")

    if bookmodel.objects.filter(email=email).exists():
            messages.error(request, f'A booking already exists for the email {email}. Please choose a different email.')
            return redirect("bookappoint")

    date_datetime = datetime.strptime(date, "%Y-%m-%dT%H:%M")
    
        # Check if a booking with the same date and hour exists
    if bookmodel.objects.filter(date__year=date_datetime.year, 
                                    date__month=date_datetime.month, 
                                    date__day=date_datetime.day, 
                                    date__hour=date_datetime.hour).exists():
            messages.error(request, f'The slot for {date} is already taken. Please choose a different date.')
            return redirect("bookappoint")
    
    en=bookmodel(name=name,mobilenum=mobilenum,email=email,date=date,doctor=doctor)
    en.save()
#email code start
    from_email=settings.EMAIL_HOST_USER
    connection=mail.get_connection()
    connection.open()
    email_message=mail.EmailMessage(f'Email from {name}',f'UserNumber:{mobilenum}\n Usermail:{email}\n date:{date}',from_email,['psychogenicheed@gmail.com'],['psychogenicheed@gmail.com'],
                                    connection=connection)
    email_client=mail.EmailMessage('psychogenic Heed Response','Thanks for reaching us',from_email,[email],
                                    connection=connection)
    connection.send_messages([email_message,email_client])
    connection.close()
    
    return render(request, "book.html")
from django.shortcuts import get_object_or_404
def view_app_detail(request):
  
    user = request.user
    booking_details = bookmodel.objects.filter(email=user.email)
    context = {
        'booking_details': booking_details
    }
    return render(request, 'app_detail.html', context)

def cancel_booking(request, booking_id):
  
    booking = get_object_or_404(bookmodel, id=booking_id)
    booking.delete()
    return redirect('bookappoint')


def profile(request):
   return render(request,"profile.html",)

def chat(request):
   return render(request,"chatbot.html",)

def about(request):
   return render(request,"about.html",)

def result(request):
   return render(request,"resultmcq.html",)

def csv1(request):
   return render(request,"home.html",)

def badresult(request):
   return render(request,"badresult.html",)

def forgot(request):
   return render(request,"password_reset_email.html",)
import base64
def re_pass(request, uidb64, token):
    return render(request, 'reset_pass.html', { 'uidb64': uidb64, 'token': token})

def mcs_save(request,user_id):
  if request.method=="POST":
     a=request.POST.get('a')
     b=request.POST.get('b')
     c=request.POST.get('c')
     d=request.POST.get('d')
     e=request.POST.get('e')
     f=request.POST.get('f')
     g=request.POST.get('g')
     h=request.POST.get('h')
     i=request.POST.get('i')
     j=request.POST.get('j')
     usid=get_object_or_404(UserModel, id=user_id)
     if a:
            
            en = mcs1(a=a,b=b,c=c,d=d,e=e,f=f,g=g,h=h,i=i,j=j,usid=usid)
            en.save()
            disagree_count = sum(1 for answer in [a, b,c,d,e,f,g,h,i,j] if answer == 'yes')
            if disagree_count > 7 :
             messages.error(request,'Not good condition')
             return redirect("resultb")
            elif disagree_count >= 5:
             messages.error(request,'Needs improvement')
             return redirect("resultb")
            elif disagree_count < 4:
             messages.error(request,'Excellent')
             return redirect("result")
     else:
            return HttpResponse('Invalid form data: Field "a" is empty')
  else:
      return HttpResponse('Invalid request method')

def custom_password_reset(request,uidb64, token):
       return render(request, "reset_pass.html", {"uidb64": uidb64, "token": token})



from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_POST
from .utils import send_password_reset_email

@require_POST
def reset_password(request):
    email = request.POST.get('email')  # Assuming you have a form where users input their email
    if email:
        send_password_reset_email(request, email)
        return HttpResponse("Password reset link sent successfully.")
    else:
        return HttpResponse("Please provide an email address.")



import pandas as pd
from django.views import View
from .utils import analyze_sentiment  


class SentimentAnalysisView(View):
    template_name = 'analysis.html' 

    def get(self, request):
        df = pd.read_csv('F://Data_Mining//chat_data (18).csv')
        df['sentiment'] = df['text'].apply(analyze_sentiment)

        # Pass the DataFrame with sentiment analysis results to the template
        return render(request, self.template_name, {'df': df})
  

def delete_book(request, book_id):
        booking = get_object_or_404(bookmodel, id=book_id)
        booking.delete()
        return redirect('home_doctor')


def prescirbe(request,doctor_id):
      doctor = bookmodel.objects.filter(doctor_id=doctor_id)
      return render(request, 'prescribe.html', {'doctor': doctor})


def save_prescription(request, book_id):
    if request.method == 'POST':
        prescription = request.POST.get('prescription')  
        book_instance = bookmodel.objects.get(pk=book_id)  
        book_instance.prescription = prescription 
        book_instance.save()  

        return redirect('home_doctor')




from django.core.mail import send_mail
from django.http import JsonResponse
import json

def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email', '')

        print('Email sending code reached')  # Add this line for debugging

        try:
            # Your logic to send the email
            send_mail(
                'Appointment Accepted',
                'Your appointment has been accepted.',
                'psychogenicheed@gmail.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'Error sending email: {e}')  # Add this line for debugging
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})
send_mail(
    'Subject',
    'what the fuck done ',
    'psychogenicheed@gmail.com',
    ['thakkarnishit007@gmail.com'],
    fail_silently=False,
)
  