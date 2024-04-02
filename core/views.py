from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.views.defaults import server_error

from product.models import Product
from .forms import ContactForm
# Create your views here.


def index(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'about/about.html')


def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():

            contact = contact_form.save()

            email_subject = 'Contact @essence-hotdeskk'
            email_msg = "Thank you for your contact. We'll get in touch with you soon."
            email_body = "Hi " + contact.name + email_msg
            try:
                # setup email
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@essence.com",
                    [contact.email],
                    headers={"Message-ID": "@essence-hotdesk"},
                )
                # send email
                email.send(fail_silently=False)
                messages.success(request, "Contact submitted successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except Exception as e:
                print(f"Error sending email: {e}")

        else:
            messages.error(request, "Invalid Form")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    contact_form = ContactForm()
    return render(request, 'contact/contact.html', {'contact_form': contact_form})


def faq(request):
    return render(request, 'faq/faq.html')


# Error handling views
def custom_400_view(request, exception):
    return render(request, '403/403.html', status=400)


def custom_403_view(request, exception):
    return render(request, '403/403.html', status=403)


def custom_404_view(request, exception):
    return render(request, '404/404.html', status=404)


def custom_500_view(request):
    return server_error(request, template_name='500/500.html')
