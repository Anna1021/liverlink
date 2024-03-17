import uuid
from peer_support.models import Referral, Mentor, User, Patient, Parent
from django.conf import settings
from django.shortcuts import redirect,reverse
from peer_support.models import Notification
from django.contrib import messages
from collections import Counter
from datetime import date

def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""

    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def notifications(request):
    """Returns whether notifications have been viewed for the current user."""

    if request.user.is_authenticated:
        has_unviewed_notifications = Notification.objects.filter(user=request.user, viewed=False).exists()
        return {'has_unviewed_notifications': has_unviewed_notifications}
    else:
        return {'has_unviewed_notifications': False}
    
def create_referral(user):
    """ Only creates referrals if the user is a mentor. """

    if isinstance(user, Mentor): 
        code = uuid.uuid4().hex[:10].upper()
        referral = Referral.objects.create(referrer=user, code=code)
        return referral

def get_referral_code(user):
    """Gets the referral code for a user, if it exists."""

    referral = Referral.objects.filter(referrer=user).first()
    if referral:
        return referral.code
    return None

def get_addable_peers(current_user):
    """Gets users who are not admin, friends, blocked or user"""

    friends_ids = current_user.friends.values_list('id', flat=True)
    blocked_users_ids = current_user.blocked_users.values_list('id', flat=True)
    blocked_by_ids = current_user.blocked_by.values_list('id', flat=True)
    eligible_users = User.objects.exclude(is_staff=True).exclude(id=current_user.id).exclude(id__in=friends_ids).exclude(id__in=blocked_users_ids).exclude(id__in=blocked_by_ids).distinct()
    return eligible_users

def check_blocked_dm(current_user, conversation):
    """Check if the conversation is a DM and, if so, whether there is a block between the 2 users."""
    
    if conversation.as_group() is None:
        user = conversation.users.exclude(id=current_user.id).get()
        if current_user in user.blocked_users.all() or user in current_user.blocked_users.all():
            return True
    return False

def get_conversation(request,conversation_id):
    conversations = request.user.conversations.filter(id=conversation_id)
    if conversations.count() == 0:
        messages.error(request,"This conversation does not exist.")
        return None
    return conversations.get(id=conversation_id)

def conversation_is_direct(request,conversation):
    if conversation.as_group() is None:
        messages.error(request,"You can only do this for a group conversation")
        return True
    return False

def get_message(request,conversation,message_id):
    conversation_messages = conversation.messages.filter(id=message_id)
    if conversation_messages.count() == 0 or request.user not in conversation_messages[0].visible_to.all():
        messages.error(request,"This message does not exist.")
        return None
    return conversation_messages.get(id=message_id)

def no_conversation_url(request):
    context = {'user_conversations':request.user.sort_conversations()}
    return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)

def user_exists(username):
    return User.objects.filter(username=username).exists()

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def get_age_ranges():
    users_ages = [calculate_age(user.date_of_birth) for user in User.objects.all() if user.date_of_birth is not None]
    age_ranges = {"13-20": 0, "21-30": 0, "31-40": 0, "41-50": 0, "51-60": 0, "61-70": 0, "71+":0}
    for age in users_ages:
        if 13 <= age <= 20:
            age_ranges["13-20"]+=1
        elif 21 <= age <= 30:
            age_ranges["21-30"]+=1
        elif 31 <= age <= 40:
            age_ranges["31-40"]+=1
        elif 41 <= age <= 50:
            age_ranges["41-50"]+=1
        elif 51 <= age <= 60:
            age_ranges["51-60"]+=1
        elif 61 <= age <= 70:
            age_ranges["61-70"]+=1
        else:
            age_ranges["71+"]+=1
    return age_ranges

def get_user_ethnicities():
    users_ethnicities = User.objects.values_list('ethnicity', flat=True)
    return Counter(users_ethnicities) 

def get_patient_conditions():
    patient_conditions = Patient.objects.values_list('condition', flat=True)
    return Counter(patient_conditions) 

def get_mentor_conditions():
    mentor_conditions = Mentor.objects.values_list('condition', flat=True)
    return Counter(mentor_conditions) 

def get_parent_child_conditions():
    parent_child_conditions = Parent.objects.values_list('child_condition', flat=True)
    return Counter(parent_child_conditions) 

def get_genders():
    genders = User.objects.values_list('gender', flat=True)
    return Counter(genders) 

def get_locations():
    location = User.objects.values_list('location', flat=True)
    return Counter(location) 

