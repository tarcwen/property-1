from UserAction.models import UserAction
from mysite.utils import encrypt_id

class UserActionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Log user action
        if request.user.is_authenticated:
            UserAction.objects.create(
                user=request.user,
                action=request.path,
                details=str(request.GET.dict())  # You can customize the details based on your needs
            )
        
        return response
    
class EncryptUserIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Encrypt user ID if authenticated
        if request.user.is_authenticated:
            request.encrypted_id = encrypt_id(request.user.id)
        else:
            request.encrypted_id = None

        response = self.get_response(request)
        return response