import uuid
from .models import Referral, Mentor

def create_referral(user):
    if isinstance(user, Mentor):
        code = uuid.uuid4().hex[:10].upper()
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
        pass  # Handle invalid referral code