from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from .utils import encrypt_user_id, decrypt_user_id

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Custom authentication logic here
        user_model = get_user_model()
        user = super().authenticate(request, username, password, **kwargs)

        # Encrypt/decrypt user ID if needed
        if user:
            user.encrypted_id = encrypt_user_id(user.id, settings.ENCRYPTION_KEY)
            original_id = decrypt_user_id(user.encrypted_id, settings.ENCRYPTION_KEY)
            print(f"Original User ID: {original_id}")

        return user