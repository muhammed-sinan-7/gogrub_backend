from django.urls import path
from .views import ChatBotView, ClearChatView

urlpatterns = [
    path("chat/", ChatBotView.as_view(), name='chatbot'),
    path('chat/clear/', ClearChatView.as_view(), name='clear-chatbot')
]
