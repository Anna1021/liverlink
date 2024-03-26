"""Tests of the conversation creation view."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from peer_support.forms import ConversationForm, MessageForm
from peer_support.models import User, Conversation, GroupConversation, Notification
                  
class CreateConversationViewTestCase(TestCase):
    """Tests of the conversation creation view."""

    fixtures = ['peer_support/tests/fixtures/default_user.json',
                'peer_support/tests/fixtures/other_users.json',
                'peer_support/tests/fixtures/default_conversation.json',
                'peer_support/tests/fixtures/default_group_conversation.json',
                'peer_support/tests/fixtures/default_message.json',
                'peer_support/tests/fixtures/other_messages.json',
    ]

    def setUp(self):
        self.conversation = Conversation.objects.get(pk=1)
        self.url = reverse('create_conversation')
        self.user = User.objects.get(username='@johndoe')
        self.client.force_login(self.user)
        self.user.conversations.set([1,2])
        self.user.friends.set(User.objects.exclude(pk=1))
        self.other_users = [2]

    def test_create_conversation_url(self):
        self.assertEqual(self.url,'/create_conversation/')

    def test_get_create_conversation(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ConversationForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_conversation_creation(self):
        form_input = {
            'users':[]
        }
        before_count = Conversation.objects.count()
        response = self.client.post(self.url,data=form_input)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_conversation.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ConversationForm))
        self.assertTrue(form.is_bound)

    def test_successful_direct_conversation_creation(self):
        form_input = {
            'users':[3]
        }
        before_count = Conversation.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':3}), status_code=302, target_status_code=200)
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)

    def test_successful_direct_conversation_creation_sends_notification(self):
        form_input = {
            'users':[3]
        }
        before_count_conversation = Conversation.objects.count()
        before_count_notification = Notification.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count_conversation = Conversation.objects.count()
        after_count_notification = Notification.objects.count()
        self.assertEqual(after_count_conversation, before_count_conversation + 1)
        self.assertEqual(after_count_notification, before_count_notification + 1)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':3}), status_code=302, target_status_code=200)
        direct_conversation = Conversation.objects.last()
        content_type_id = ContentType.objects.get_for_model(Conversation)
        notification = Notification.objects.get(content_type=content_type_id, object_id = direct_conversation.id)
        self.assertEqual(notification.title, "New Conversation")
        self.assertEqual(notification.description, "@johndoe has created a conversation with you.")
        self.assertEqual(notification.user, User.objects.get(id=3))
        self.assertEqual(notification.notifying_user, self.user)
        self.assertEqual(notification.content_type, content_type_id)
        self.assertEqual(notification.object_id, direct_conversation.id)
        self.assertEqual(notification.content_object, direct_conversation)

    def test_successful_direct_conversation_retrieval(self):
        form_input = {
            'users':self.other_users
        }
        before_count = Conversation.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':1}), status_code=302, target_status_code=200)
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)

    def test_successful_group_conversation_creation(self):
        form_input = {
            'users':self.other_users,
            'group':':3'
        }
        before_count = Conversation.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count = Conversation.objects.count()
        self.assertEqual(after_count, before_count+1)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':3}), status_code=302, target_status_code=200)
        form = response.context['message_form']
        self.assertTrue(isinstance(form, MessageForm))
        self.assertFalse(form.is_bound)

    def test_successful_group_conversation_creation_sends_notifications(self):
        form_input = {
            'users':self.other_users,
            'group':':3'
        }
        before_count_conversation = GroupConversation.objects.count()
        before_count_notification = Notification.objects.count()
        response = self.client.post(self.url, data=form_input,follow=True)
        after_count_conversation = GroupConversation.objects.count()
        after_count_notification = Notification.objects.count()
        self.assertEqual(after_count_conversation, before_count_conversation + 1)
        self.assertEqual(after_count_notification, before_count_notification + 1)
        self.assertTemplateUsed(response, 'conversation.html')
        self.assertRedirects(response, reverse('conversation',kwargs={'conversation_id':3}), status_code=302, target_status_code=200)
        group_conversation = GroupConversation.objects.last()
        content_type_id = ContentType.objects.get_for_model(GroupConversation)
        notification = Notification.objects.get(content_type=content_type_id, object_id = group_conversation.id)
        self.assertEqual(notification.title, "New Group Conversation")
        self.assertEqual(notification.description, "@johndoe has added you to a group conversation.")
        self.assertEqual(notification.user, User.objects.get(id=2))
        self.assertEqual(notification.notifying_user, self.user)
        self.assertEqual(notification.content_type, content_type_id)
        self.assertEqual(notification.object_id, group_conversation.id)
        self.assertEqual(notification.content_object, group_conversation)
