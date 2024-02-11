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