import uuid
from .models import Referral, Mentor


def create_referral(user):
    """ Only creates referrals if the user is a mentor. """
    if isinstance(user, Mentor): 
        code = uuid.uuid4().hex[:10].upper()
        referral = Referral.objects.create(referrer=user, code=code)
        return referral
    else:
        pass

def get_referral_code(user):
    referral = Referral.objects.filter(referrer=user).first()
    if referral:
        return referral.code
    else:
        return None
    
