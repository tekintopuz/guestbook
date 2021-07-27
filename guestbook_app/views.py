from django.contrib.auth.models import User, Group
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
from django.views import View
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
)
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from guestbook_app.models import Message
from guestbook_app.serializers import UserSerializer, GroupSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageApiView(GenericViewSet,  # generic view functionality
                     CreateModelMixin,  # handles POSTs
                     RetrieveModelMixin,  # handles GETs for 1 Message
                     UpdateModelMixin,  # handles PUTs and PATCHes
                     DestroyModelMixin,  # handles DELETE
                     ListModelMixin):  # handles GETs for many Messages

    parser_classes = (FormParser, JSONParser, MultiPartParser)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        message = Message(created_at=timezone.now())
        serializer = self.serializer_class(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndexView(View):
    def get(self, request):
        template = loader.get_template('guestbook_app/index.html')
        context = {}
        return HttpResponse(template.render(context, request))
