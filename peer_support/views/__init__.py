"""Views for the tasks app."""

from .dashboard_view import dashboard
from .home_view import home
from .log_in_view import LogInView
from .log_out_view import log_out
from .password_view import PasswordView
from .profile_update_view import ProfileUpdateView
from .sign_up_view import SignUpView
from .view_mixins import LoginProhibitedMixin
from .profile_deactivate_view import deactivate_user
from .conversation_view import ConversationView
from .peer_select_view import PeerView
from .create_conversation_view import CreateConversationView
from .delete_message_view import DeleteMessageView
from .new_question_page_view import newQuestionPage
from .reply_page_view import replyPage
from .resources_view import resources
from .question_page_view import questionPage
from .send_friend_request_view import SendFriendRequestView
from .accept_friend_request_view import AcceptFriendRequestView
from .friends_list_view import friends_list
from .other_user_profile_view import OtherUserProfileView
from .inbox_view import InboxView
from .delete_notification_view import delete_notification
from .clear_notifications_view import clear_notifications
from .conversation_details_view import ConversationDetailsView
