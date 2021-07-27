import json
from django.test import TestCase
from django.utils import timezone
from factory import Faker
from factory.django import DjangoModelFactory
from rest_framework import status
from rest_framework.reverse import reverse

from guestbook_app.models import Message
from guestbook_app.serializers import MessageSerializer


class MessageStrTestCase(TestCase):
    def setUp(self):
        self.message = Message.objects.create(name="Test Name",
                                              subject="Test Subject",
                                              message="Test Message",
                                              created_at=timezone.now())

    def test_str(self):
        """Message object has its own subject as __str__"""
        self.assertEqual(str(self.message), self.message.subject)


class MessageTestCase(TestCase):
    serializer_class = MessageSerializer

    def test_str(self):
        """Test for string representation of created_at."""
        message = MessageFactory()

        serializer = self.serializer_class(message)
        """Serializer data matches the Message object for each field."""
        for field_name in ['name', 'subject', 'message', 'created_at']:
            if field_name == 'created_at':
                self.assertEqual(
                    serializer.data[field_name],
                    getattr(message, field_name).strftime("%m/%d/%y %H:%M:%S")
                )
            else:
                self.assertEqual(
                    serializer.data[field_name],
                    getattr(message, field_name)
                )


class MessageFactory(DjangoModelFactory):
    name = Faker('name')
    subject = Faker('name')
    message = Faker('text')
    created_at = Faker('date_time')

    class Meta:
        model = Message


class MessageViewSetTestCase(TestCase):
    def setUp(self):
        self.list_url = reverse('message-list')

    def get_detail_url(self, message_id):
        return reverse('message-detail', kwargs={'pk': message_id})

    def test_get_list(self):
        """GET the list page of Messages."""
        messages = [MessageFactory() for i in range(0, 3)]
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            set(message['name'] for message in response.data['results'][:3]),
            set(message.name for message in messages)
        )

    def test_get_detail(self):
        """GET a detail page for a Message."""
        message = MessageFactory()
        response = self.client.get(self.get_detail_url(message.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], message.name)

    def test_post(self):
        """POST to create a Message."""
        data = {
            'name': 'New name',
            'subject': 'New subject',
            'message': 'New message'
        }
        self.assertEqual(Message.objects.count(), 0)
        response = self.client.post(self.list_url, content_type='application/json', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.all().last()
        for field_name in data.keys():
            self.assertEqual(getattr(message, field_name), data[field_name])

    def test_put(self):
        """PUT to update a Message."""
        message = MessageFactory()
        data = {
            "name": "New name",
            "subject": "New subject put",
            "message": "New message put"
        }
        response = self.client.put(self.get_detail_url(message.id), content_type='application/json',
                                   data=json.dumps(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The object has really been updated
        message.refresh_from_db()
        for field_name in data.keys():
            self.assertEqual(getattr(message, field_name), data[field_name])

    def test_patch(self):
        """PATCH to update a Message."""
        message = MessageFactory()
        data = {
            "name": "New name patch",
            "subject": "New subject patch",
            "message": "New message Update"
        }
        response = self.client.patch(self.get_detail_url(message.id), content_type='application/json',
                                     data=json.dumps(data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # The object has really been updated
        message.refresh_from_db()
        self.assertEqual(message.name, data['name'])

    def test_delete(self):
        """DELETE"""
        message = MessageFactory()
        response = self.client.delete(self.get_detail_url(message.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
