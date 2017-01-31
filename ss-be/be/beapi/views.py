from rest_framework import generics
from beapi.models import Consumer
from beapi.serializers import ConsumerSerializer
from beapi.models import ConsumerTxn
from beapi.serializers import ConsumerTxnSerializer

#Right now we actually don't need consumer list/detail
# but good for entering data
class ConsumerList(generics.ListCreateAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer

class ConsumerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer

class ConsumerTxnList(generics.ListCreateAPIView):
    queryset = ConsumerTxn.objects.all()
    serializer_class = ConsumerTxnSerializer

class ConsumerTxnDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConsumerTxn.objects.all()
    serializer_class = ConsumerTxnSerializer

