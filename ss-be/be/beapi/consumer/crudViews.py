from rest_framework import generics
from beapi.serializers import ConsumerSerializer
from beapi.models import Consumer

class ConsumerList(generics.ListCreateAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer

class Consumer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer