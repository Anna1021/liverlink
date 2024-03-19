import uuid
from peer_support.models import Referral, Mentor, User, Patient, Parent, Post, FriendRequest
from django.conf import settings
from django.shortcuts import redirect, reverse
from peer_support.models import Notification, PostComment
from django.contrib import messages
from collections import Counter
from datetime import date
import pycountry
import pycountry_convert as pc
from collections import defaultdict
from django.db.models import Q

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
    """Gets users who are not admin, friends, blocked or have been requested"""

    friends_ids = current_user.friends.values_list('id', flat=True)
    requested_users = FriendRequest.objects.filter(sender=current_user).values_list('receiver_id', flat=True)
    blocked_users_ids = current_user.blocked_users.values_list('id', flat=True)
    blocked_by_ids = current_user.blocked_by.values_list('id', flat=True)
    eligible_users = User.objects.exclude(is_staff=True).exclude(id=current_user.id).exclude(id__in=friends_ids).exclude(id__in=blocked_users_ids).exclude(id__in=blocked_by_ids).exclude(is_active=False).exclude(id__in=requested_users).distinct()
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

def retrieve_friend_posts(request):
    user_friends = request.user.friends.all()
    # Retrieve the user's posts and friends' posts
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

def get_user_types():
    num_patients = Patient.objects.count()
    num_parents = Parent.objects.count()
    num_mentors = Mentor.objects.count()
    return {'patients': num_patients,
        'parents': num_parents,
        'mentors': num_mentors,}

def get_user_ethnicities():
    users = User.objects.all()
    ethnicity_names = [user.ethnicity_name() for user in users]
    ethnicity_counts = Counter(ethnicity_names)
    return ethnicity_counts

def get_patient_conditions():
    patient_conditions = Patient.objects.values_list('condition', flat=True)
    return Counter(patient_conditions) 

def get_parent_child_conditions():
    parent_child_conditions = Parent.objects.values_list('child_condition', flat=True)
    return Counter(parent_child_conditions) 

def get_genders():
    genders = User.objects.values_list('gender', flat=True)
    return Counter(genders) 

def get_locations():
    """Returns set of all continets and number of users in each"""

    country_codes = User.objects.values_list('location', flat=True)
    continents = [country_to_continent(code) for code in country_codes if country_to_continent(code) is not None]
    continent_counts = Counter(continents)
    return Counter(continent_counts) 

def country_to_continent(country_code):
    """Converts a country code to continent name"""

    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_name = pc.convert_continent_code_to_continent_name(continent_code)
        return continent_name
    except KeyError:
        return ""
    
def country_to_continent_specific(country_code):
    """gets continent and full country name from code returns both"""

    country = pycountry.countries.get(alpha_2=country_code)
    country_name = country.name if country else ""
    continent_name = country_to_continent(country_code)
    return continent_name, country_name
    
def get_locations_specific():
    """Returns set of all countries for each continent and number of users in each"""

    country_codes = User.objects.values_list('location', flat=True)
    continent_to_countries = defaultdict(list)
    for code in country_codes:
        continent, country = country_to_continent_specific(code)
        continent_to_countries[continent].append(country)
    continent_counts = {continent: Counter(countries) for continent, countries in continent_to_countries.items()}
    return(continent_counts)
           
def get_user_type(user):
    if hasattr(user, 'parent'):
        return "PARENT"
    elif hasattr(user, 'patient'):
        return "PATIENT"
    elif hasattr(user, 'mentor'):
        return "MENTOR"
    else:
        return "ADMIN"
