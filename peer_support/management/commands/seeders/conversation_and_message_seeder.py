from random import randint
from peer_support.management.commands.helpers import get_user
from peer_support.management.commands.seeders.parent_seeder import parent_fixtures
from peer_support.management.commands.seeders.patient_seeder import patient_fixtures
from peer_support.models import Conversation, Message, User

message_fixtures = [
    {"sender": patient_fixtures[0], "content": "Hello, how are you?"},
    {"sender": parent_fixtures[0], "content": "I am good, thank you."},
    {"sender": parent_fixtures[0], "content": "How are you?"},
    {"sender": patient_fixtures[1], "content": "I am good"},
    {"sender": parent_fixtures[1], "content": "Hi"},
    {"sender": parent_fixtures[2], "content": "Hello"},
]

conversation_fixtures = [
    {
        "users": [patient_fixtures[0], parent_fixtures[0]],
        "messages": [message_fixtures[0], message_fixtures[1], message_fixtures[2]],
    },
    {
        "users": [patient_fixtures[1], parent_fixtures[1]],
        "messages": [message_fixtures[3], message_fixtures[4]],
    },
    {
        "users": [patient_fixtures[0], parent_fixtures[2]],
        "messages": [message_fixtures[5]],
    },
]


class ConversationAndMessageSeeder:
    """Seed conversations and messages into the database."""

    CONVERSATION_COUNT = 500

    def __init__(self, faker):
        self.faker = faker
        self.users = User.objects.all()

    def create_conversations(self):
        self.generate_conversation_fixtures()
        self.generate_random_conversations()

    def generate_conversation_fixtures(self):
        for data in conversation_fixtures:
            self.try_create_conversation(data)

    def generate_random_conversations(self):
        conversation_count = Conversation.objects.count()
        while conversation_count < self.CONVERSATION_COUNT:
            print(f"Seeding conversation {conversation_count}/{self.CONVERSATION_COUNT}", end='\r')
            self.generate_conversation()
            conversation_count = Conversation.objects.count()
        print("Conversation seeding complete.      ")

    def generate_conversation(self):
        users = [
            self.users[randint(0, len(self.users) - 1)],
            self.users[randint(0, len(self.users) - 1)],
        ]
        users = [{"username": user.username} for user in users]
        messages = []
        for _ in range(randint(1, 15)):
            sender = users[randint(0, len(users) - 1)]
            content = self.faker.text(max_nb_chars=100)
            message = {"sender": sender, "content": content}
            messages.append(message)
        self.try_create_conversation({"users": users, "messages": messages})

    def try_create_message(self, data):
        try:
            return self.create_message(data)
        except:
            pass

    def try_create_conversation(self, data):
        try:
            self.create_conversation(data)
        except:
            pass

    def create_message(self, data):
        data["sender"] = get_user(data["sender"])
        message = Message.objects.create(**data)
        return message

    def create_conversation(self, data):
        users = [get_user({"username": user["username"]}) for user in data["users"]]
        conversation = Conversation.objects.create()
        message_objects = [self.try_create_message(message) for message in data["messages"]]
        for message_object in message_objects:
            message_object.visible_to.set(users)
        conversation.users.set(users)
        conversation.messages.set(message_objects)
        conversation.save()
        for user in users:
            user.conversations.add(conversation)    
