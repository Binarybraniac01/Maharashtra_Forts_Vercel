from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings

from .models import *

import os


@login_required(login_url="/login-page/")
def feedback(request):

    # To get the current users instance
    if request.user.is_authenticated:
        email = request.user.email

    if request.method == "POST":
        data = request.POST

        mail = data.get("email")
        usermessage = data.get("message")
        rating = data.get("rating")

        Feedback.objects.create(
            user = request.user,
            email = mail,
            user_feedback = usermessage,
            rating = rating
        )

        # send feedback to website mail
        subject = f"This feedback is from {request.user}"
        message = f"User Mail : {mail}\n\nUser Feedback : \n{usermessage}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['maharashtraforts.official@gmail.com']  
        send_mail(subject, message, from_email, recipient_list)

        messages.info(request, "Feeedback submited successfully.")
        return redirect('/feedback/')

    return render(request, "feedback.html", {'email': email})
