from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from .utils import token_generator
from .forms import RegistrationForm, LoginForm, PasswordChangeForm,  PasswordResetForm

from .models import ShippingAddress, CustomUser
from product.models import Review
from checkout.models import Order


# Create your views here.
def user_auth_view(request):
    reg_form = RegistrationForm
    login_form = LoginForm
    current_tab = 'login'

    context = {
        "reg_form": reg_form,
        "login_form": login_form,
        "current_tab": current_tab,
    }

    return render(request, 'user_auth/user_auth.html', context)


def register(request):
    current_tab = 'register'
    if request.method == 'POST':
        current_tab = 'register'
        email = request.POST.get('email')
        user_exist = CustomUser.objects.filter(email=email).exists()
        if user_exist:
            messages.warning(
                request, 'An account with this email already exists. Please use a different email address.')
            return redirect('register')
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Form data is valid; create a new user,
            user = form.save()
            # create user
            # e user profile
            new_shipping_address = ShippingAddress.objects.create(
                email=email, user=user)

            user.is_active = False
            user.save()
            # email subject here
            email_subject = 'Activate Your Account'
            # email body

            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse('activate', kwargs={
                'uidb64': uidb64, 'token': token
            })

            domain = get_current_site(request).domain
            activate_url = 'http://'+domain+link
            email_body = f"Dear {
                user.email},  Please use this link to verify your account\n {activate_url}"
            # setup email
            email = EmailMessage(
                email_subject,
                email_body,
                "noreply@essence.com",
                [user.email],
                headers={"Message-ID": "@essence-hotdesk"},
            )
            # send email
            email.send(fail_silently=False)

            messages.success(
                request, "Your Registration is Successful, check your mailbox to activate your account before login")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    form = LoginForm(request.POST)
    reg_form = RegistrationForm(request.POST)
    context = {
        "reg_form": reg_form,
        "login_form": form,
        "current_tab": current_tab
    }

    return render(request, 'user_auth/user_auth.html', context)


def login_view(request):
    current_tab = 'login'
    if request.method == 'POST':
        current_tab = 'login'
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        remember_me = request.POST.get('remember_me')
        if user is not None:
            login(request, user)

            if not remember_me:
                # Set session to expire when the browser is closed
                request.session.set_expiry(0)
            greetings = "You're Welcome!"
            messages.success(request, greetings)
            # redirect to home
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    form = LoginForm(request.POST)
    reg_form = RegistrationForm(request.POST)
    context = {
        "reg_form": reg_form,
        "login_form": form,
        "current_tab": current_tab,
    }

    return render(request, 'user_auth/user_auth.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out successfully")
    # Redirect to login
    return redirect('user_auth')


def user_profile(request):
    change_password_form = PasswordChangeForm(request.POST)
    user_reviews = None
    user_shipping_address = None
    orders = None

    if request.user.is_authenticated:
        user_shipping_address, created = ShippingAddress.objects.get_or_create(
            user=request.user)
        user_reviews = Review.objects.filter(user=request.user)
        orders = Order.objects.filter(user_id=request.user.id)

    context = {
        "user_shipping_address": user_shipping_address,
        "change_password_form": change_password_form,
        "user_reviews": user_reviews,
        "orders": orders,
    }

    return render(request, 'user_profile/user_profile.html', context)


def update_user_info(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, pk=request.user.id)
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()
            messages.success(request, "Updated successfully!")
        else:
            # Unauthenticated user
            messages.warning(request, 'Only Authenticated User is Allowed')
            raise PermissionDenied
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_shipping_info(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_shipping_address = get_object_or_404(
                ShippingAddress, user=request.user)

            email = request.POST['shipping_email']
            phone = request.POST['phone']
            street_address = request.POST['street_address']
            post_code = request.POST['post_code']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']

            if user_shipping_address:
                user_shipping_address.email = email
                user_shipping_address.phone = phone
                user_shipping_address.street_address = street_address
                user_shipping_address.post_code = post_code
                user_shipping_address.city = city
                user_shipping_address.state = state
                user_shipping_address.country = country

                user_shipping_address.save()
                messages.success(request, "Updated Successfully!")

        else:
            # Unauthenticated user
            messages.warning(request, 'Only Authenticated User is Allowed')
            raise PermissionDenied
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_review(request, review_id):
    user_review = None
    if request.user.is_authenticated:
        user_review = get_object_or_404(
            Review, user=request.user, pk=review_id)
        user_review.delete()

        messages.success(request, "Deleted Successfully!")

    else:
        # Unauthenticated user
        messages.warning(request, 'Only Authenticated User is Allowed')
        raise PermissionDenied

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_password(request):
    if request.method == 'POST':
        change_password_form = PasswordChangeForm(
            user=request.user, data=request.POST)

        if change_password_form.is_valid():
            change_password_form.save()
            messages.success(
                request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        change_password_form = PasswordChangeForm(user=request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def request_password_reset(request):

    if request.method == 'POST':
        email = request.POST.get('email')

        if email:

            if get_object_or_404(CustomUser, email=email):
                user = get_object_or_404(CustomUser, email=email)
                # email subject here
                email_subject = 'Password Reset Request'
                # email body
                print(user.email)
                token = token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                link = reverse('reset_password', kwargs={
                    'uidb64': uidb64, 'token': token
                })

                domain = get_current_site(request).domain
                pwd_reset_link = 'http://'+domain+link
                email_body = (
                    f"""Dear {user, email},!

                        We received password reset request from you.
                        Use the link here to confirm your email. {pwd_reset_link}

                        Kindly Ignore this mail if you haven't requested for password rest.

                        Thank you for shopping with Essence!

                        Best regards,
                        Essence
                        """)

                # setup email
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@essence.com",
                    [user.email],
                    headers={"Message-ID": "@essence-hotdesk"},
                )
                # send email
                email.send(fail_silently=False)
                messages.success(
                    request, "Check your mailbox for password reset confirmation link")
            else:
                messages.warning(
                    request, "Requested user does not exist, Pleaser verify your email or register with a new account")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def reset_password(request, uidb64, token):
    form = PasswordResetForm(request)

    if request.method == "POST":
        id = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=id)
        form = PasswordResetForm(request.POST or None, user=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Password Reset Successfully, Login with your new Password')
            return redirect(reverse('user_auth'))
        else:
            messages.error(request, 'Password Do Not Match')
    context = {
        'form': PasswordResetForm,
        'uidb64': uidb64,
        'token': token,
    }
    return render(request, 'password_reset/password_reset.html', context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)
            greetings = f"You're Welcome {
                user.email}, Account activated successfully."
            if user.is_active:
                messages.info(request, "user account is already activated.")
                login(request, user)
                # Redirect to a success page, e.g., user's profile page
                return redirect("home")
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, greetings)
            return redirect("home")

        except Exception as ex:
            messages.error(request, "Error Activating Your Account.")
            print(f"Error Activating Your Account: {ex}")
        return redirect("user_auth")
