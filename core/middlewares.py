from .models import AppUser

# MyFirst Middleware
class AppUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self,request):
        if request.user.is_authenticated:
            try:
                request.AppUser = AppUser.objects.get(user =request.user)
            except AppUser.DoesNotExist:
                request.AppUser = None
        response = self.get_response(request)



        return response
