from django.urls import path

from ServerApp import consumers

websocket_urlpatterns = [
    path('ws/broker/', consumers.BrokerConsumer),
    path('ws/server/', consumers.ServerConsumer),
]
