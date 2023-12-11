import IP2Location
from django.conf import settings
from django.core.signing import dumps
from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings
import logging
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def get_geolocation_info(ip_address):
    database_path = getattr(settings, 'IP2LOCATION_DATABASE_PATH', '')
    
    if not database_path:
        raise ValueError('IP2Location database path is not configured.')

    ip2location = IP2Location.IP2Location(database_path)
    result = ip2location.get_all(ip_address)

    return result

#this is your "password/ENCRYPT_KEY". keep it in settings.py file
#key = Fernet.generate_key() 

def encrypt_id(txt):
    try:
        # convert integer etc to string first
        txt = str(txt)
        # get the key from settings
        cipher_suite = Fernet(settings.ENCRYPT_KEY) # key should be byte
        # #input should be byte, so convert the text to byte
        encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
        # encode to urlsafe base64 format
        encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
        return encrypted_text
    except Exception as e:
        # log the error if any
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt_id(txt):
    try:
        # base64 decode
        txt = base64.urlsafe_b64decode(txt)
        cipher_suite = Fernet(settings.ENCRYPT_KEY)
        decoded_text = cipher_suite.decrypt(txt).decode("ascii")     
        return decoded_text
    except Exception as e:
        # log the error
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None
    