class SetDefaultCartsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set default value for 'carts' if not present
        request.session.setdefault('carts', [])

        response = self.get_response(request)
        return response
