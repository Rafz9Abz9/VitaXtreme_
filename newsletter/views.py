from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage

from .models import NewsletterSubscribers
from user.models import CustomUser
# Create your views here.


def subscribe_newsletter(request):
    email = None
    user = None

    if NewsletterSubscribers.objects.filter(email=email).exists():
        messages.warning(request, 'You Already Subscribed For News Letter')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, pk=request.user.id)
        email = user.email
        if request.method == 'POST':
            email = request.POST['email']
        newsletter, created = NewsletterSubscribers.objects.get_or_create(
            user_id=user.id, email=email)
        user.is_subscribed_newsletter = True
        user.save()
    else:
        email = request.POST['email']
        newsletter, created = NewsletterSubscribers.objects.get_or_create(
            email=email)
    # set up email notification to user
    email_subject = '@essence-newsletter'
    email_msg = "Thank you for for subscribing to our newsletter, We'll keep you posted on our product and trends."
    email_body = f"Hi {newsletter.email}, {email_msg}"

    mail_email = EmailMessage(
        email_subject,
        email_body,
        "noreply@essence.com",
        [newsletter.email],
        headers={"Message-ID": "@essence-hotdesk"},
    )
    # send email
    mail_email.send(fail_silently=False)
    messages.success(request, "Successfully Subscribed to Newsletter!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unsubscribe_newsletter(request):
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, pk=request.user.id)
        newsletter = get_object_or_404(
            NewsletterSubscribers, user_id=user.id, email=user.email)
        user.is_subscribed_newsletter = False
        user.save()

        newsletter.delete()

        # set up email notification to user
        email_subject = '@essence-newsletter'
        email_msg = "You have successfully unsubscribed from our newsletter, Hope to get in touch with you again."
        email_body = f"Hi {newsletter.email}, {email_msg}"

        email = EmailMessage(
            email_subject,
            email_body,
            "noreply@essence.com",
            [newsletter.email],
            headers={"Message-ID": "@essence-hotdesk"},
        )
        # send email
        email.send(fail_silently=False)
        messages.success(request, "Successfully Unsubscribed from Newsletter!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, 'user_profile/user_profile.html')
