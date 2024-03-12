import uuid
from peer_support.models import Referral, Mentor, User, Question, Response
from django.conf import settings
from django.shortcuts import redirect,reverse,get_object_or_404
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