from django.shortcuts import redirect
from django.urls import reverse


class AuthenticatedRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # If the user is not authenticated, continue with the request
            return self.get_response(request)

        # If the user is already authenticated, redirect them to a different page
        if request.path_info in [reverse('login'), reverse('register'), reverse('user_auth')]:
            return redirect(reverse('home'))

        return self.get_response(request)
