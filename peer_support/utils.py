import uuid
from .models import Referral, Mentor

def create_referral(user):
    print("create referral called")
    # print(user.mentor_age_of_diagnosis)
    print(type(user))
    if isinstance(user, Mentor): 
        print("in the if statement")
        code = uuid.uuid4().hex[:10].upper()
        print(code)
        referral = Referral.objects.create(referrer=user, code=code)
        return referral
    else:
        pass

def claim_referral(user, code):
    try:
        referral = Referral.objects.get(code=code)
        referral.referred = user
        referral.claimed = True
        referral.save()
    except Referral.DoesNotExist:
        pass 

def get_referral_code(user):
    referral = Referral.objects.filter(referrer=user).first()
    if referral:
        return referral.code
    else:
        return None
    
def check_referral(referral_code):
        """Validation of referral code"""
        try:
            referral = Referral.objects.get(code=referral_code)
            if referral.is_valid():
                return True
            else:
                return False
        except Referral.DoesNotExist:
            return False