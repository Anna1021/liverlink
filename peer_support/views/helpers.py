import uuid
from peer_support.models import Referral, Mentor, User
from django.conf import settings
from django.shortcuts import redirect,reverse
from peer_support.models import Notification
from django.contrib import messages

def login_prohibited(view_function):
    """Decorator for view functions that redirect users away if they are logged in."""
    
    def modified_view_function(request):
        if request.user.is_authenticated:
            return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        else:
            return view_function(request)
    return modified_view_function

def notifications(request):
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
    referral = Referral.objects.filter(referrer=user).first()
    if referral:
        return referral.code
    return None

def get_addable_peers(current_user):
    """Gets users who are not admin, friends or user"""
    friends_ids = current_user.friends.values_list('id', flat=True)
    eligible_users = User.objects.exclude(is_staff=True).exclude(id=current_user.id).exclude(id__in=friends_ids).distinct()
    return eligible_users

def conversation_does_not_exist(request,conversations):
    if conversations.count() == 0 or request.user not in conversations[0].users.all():
        messages.error(request,"This conversation does not exist.")
        return True
    return False

def conversation_is_direct(request,conversation):
    if conversation.as_group() is None:
        messages.error(request,"You can only do this for a group conversation")
        return True
    return False

def message_does_not_exist(request,conversation_messages):
    if conversation_messages.count() == 0 or request.user not in conversation_messages[0].visible_to.all():
        messages.error(request,"This message does not exist.")
        return True
    return False

def no_conversation_url(request):
    context = {'user_conversations':request.user.sort_conversations()}
    return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)
