import uuid
from peer_support.models import Referral, Professional, User, Post, FriendRequest, Notification, PostComment
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.contrib import messages
from datetime import date
import pycountry
import pycountry_convert as pc
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

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
    """ Only creates referrals if the user is a professional."""

    if isinstance(user, Professional): 
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
    """Gets users who are not friends, blocked, deactivated or have been requested"""

    friends_ids = current_user.friends.values_list("id", flat=True)
    requested_users = FriendRequest.objects.filter(sender=current_user).values_list('receiver_id', flat=True)
    blocked_users_ids = current_user.blocked_users.values_list("id", flat=True)
    blocked_by_ids = current_user.blocked_by.values_list("id", flat=True)
    eligible_users = (
        User.objects.exclude(id=current_user.id)
        .exclude(id__in=friends_ids)
        .exclude(id__in=blocked_users_ids)
        .exclude(id__in=blocked_by_ids)
        .exclude(is_active=False)
        .exclude(id__in=requested_users)
        .distinct()
    )
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

def no_conversation_url(request):
    context = {'user_conversations':request.user.sort_conversations()}
    return redirect(reverse('conversation',kwargs={'conversation_id':0}),context)

def retrieve_friend_posts(request):
    user_friends = request.user.friends.all()
    return Post.objects.filter(Q(author__in=user_friends) | Q(author=request.user)).order_by("-created_at")

def get_post(request,post_id):
    posts = (retrieve_friend_posts(request)|Post.objects.filter(visibility='G')).filter(id=post_id)
    if posts.exists():
        return Post.objects.get(id=post_id)

def get_comment(comment_id):
    comments = PostComment.objects.filter(id=comment_id)
    if comments.exists():
        return comments[0]

def user_exists(username):
    return User.objects.filter(username=username).exists()

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def country_to_continent(country_code):
    """Converts a country code to continent name"""

    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except KeyError:
        return "Unknown"
    
def country_to_continent_specific(country_code):
    """gets continent and full country name from code returns both."""

    country = pycountry.countries.get(alpha_2=country_code)
    country_name = country.name if country else "Unknown"
    continent_name = country_to_continent(country_code)
    return continent_name, country_name
    
def map_blank_key(key):
    """Return 'Unknown' if the key is blank or None, otherwise return the ethnicity."""
     
    return key if key else "Unknown"

def get_user_type(user):
    if hasattr(user, 'parent'):
        return "PARENT"
    elif hasattr(user, 'patient'):
        return "PATIENT"
    elif hasattr(user, 'mentor'):
        return "MENTOR"
    elif hasattr(user, 'professional'):
        return "PROFESSIONAL"
    else:
        return "ADMIN"

def filter_notifications(request, notifications):
    """Filter notifications by type and/or timeframe."""
    
    type = request.GET.get('type', None)
    timeframe = request.GET.get('timeframe', None)
    if type:
        notifications = filter_by_type(notifications, type)
    if timeframe:
        notifications = filter_by_timeframe(notifications, timeframe)
    return notifications

def filter_by_timeframe(notifications, timeframe):
    """Filter notifications by the specified timeframe."""

    now = timezone.now()
    if timeframe == 'past_24_hours':
        start_time = now - timedelta(hours=24)
        notifications = notifications.filter(created__gte=start_time, created__lt=now)
    elif timeframe == 'past_7_days':
        start_time = now - timedelta(days=7)
        notifications = notifications.filter(created__gte=start_time, created__lt=now)
    elif timeframe == 'past_4_weeks':
        start_time = now - timedelta(weeks=4)
        notifications = notifications.filter(created__gte=start_time, created__lt=now)
    elif timeframe == 'earlier':
        start_time = now - timedelta(weeks=4)  
        notifications = notifications.filter(created__lt=start_time)
    return notifications

def filter_by_type(notifications, type):
    """Filter notifications by the specified type."""

    return notifications.filter(content_type__model=type.lower().replace(" ", ""))