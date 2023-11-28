from django.contrib import admin
from django.urls import path  # Uncomment this line
from.import views  
from .views import SignUp
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns= [
    
    path('send-email/', views.send_email, name='send_email'),
    path('',views.home1,name='home1'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset_email.html"), name="reset_password"), 
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_done.html"), name="password_reset_done"), 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"), 
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('register/',SignUp.as_view(template_name='register.html'),name='register'),
    #path('login/',auth_views.LoginView.as_view(
    #    template_name='login.html'),
    #     name='login'),
    path('login/', views.login_view, name='login_view'),
    path('mcs/<int:user_id>/',views.mcs,name='mcq'),
    path('mcq_save/<int:user_id>',views.mcs_save,name='mcq_save'),
    path('voice',views.transcribe_speech,name='voice'),
    #path('home/',Login.as_view(),
      #   name='login'),
    path('logout/', auth_views.LogoutView.as_view
         (template_name='logout.html'), name='logout'),
    path('',views.home1,name='home1'),
   # path('updatepro/',views.updatepro,name='updatepro'),
    path('home/',views.home,name='home'),
    path('home_doctor/',views.home_doctor,name='home_doctor'),
    path('viewCategory/',views.viewCategory,name="viewCategory"),
    path('profile/',views.profile,name="profile"),
    path('bookappoint',views.bookappoint,name="bookappoint") ,
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('addbooking/',views.addbooking,name="addbooking") ,
    path('chatbot',views.chat,name="chatbot"),
    path('api',views.chatapi,name="chatapi"),
    path('csv',views.csv1,name="csv"),
    path('about',views.about,name="about"),
    path('pre',views.pre,name="pre"),
    path('download_chat_data/<int:user_id>/', views.download_chat_data, name='download_chat_data'),
    path('view_app_detail/', views.view_app_detail, name='view_app_detail'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('analyze_sentiment/', SentimentAnalysisView.as_view(template_name = 'sentiment_analysis.html'), name='analyze_sentiment'),
    path('patientv/<int:doctor_id>/', views.patientv, name='patientv'),
    path('prescribe/<int:doctor_id>/', views.prescirbe, name='prescirbe'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('save_prescription/<int:book_id>/', save_prescription, name='save_prescription'),    
    path('result/', views.result, name='result'),
    path('resultb/', views.badresult, name='resultb'),

   
]