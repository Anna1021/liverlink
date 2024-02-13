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

from .send_friend_request_view import send_friend_request, accept_friend_request
from .inbox_view import InboxView
from .delete_notification_view import delete_notification