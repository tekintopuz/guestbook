from django.urls import path

from guestbook_app.views import IndexView

urlpatterns = [
    path('index/', IndexView.as_view(), name="index"),
    path('',  IndexView.as_view(), name="index"),
]
