"""
URL configuration for peer_support_network project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from peer_support import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('settings/password/', views.PasswordView.as_view(), name='password'),
    path('settings/', views.ProfileUpdateView.as_view(), name='settings'),
    path('deactivate_user/', views.deactivate_user, name='deactivate_user'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('resources/', views.resources, name='resources'),
    path('question/<int:id>', views.questionPage, name='question'),
    path('new-question/', views.newQuestionPage, name='new-question'),
    path('reply', views.replyPage, name='reply'),
    path('conversation/<int:conversation_id>', views.ConversationView.as_view(), name='conversation'),
    path('peer_select/', views.PeerView.as_view(), name='peer_select'),
    path('create_conversation/',views.CreateConversationView.as_view(),name='create_conversation'),
    path('delete_message/<int:conversation_id>/<int:message_id>/',views.DeleteMessageView.as_view(),name='delete_message'),
    path('create_conversation/', views.CreateConversationView.as_view(), name='create_conversation'),
    path('send_friend_request/<int:user_id>', views.SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:friend_request_id>/<int:notification_id>/', views.AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('clear_notifications/', views.clear_notifications, name='clear_notifications'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('conversation_details/<int:conversation_id>',views.ConversationDetailsView.as_view(),name="conversation_details"),
]
