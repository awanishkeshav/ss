from rest_framework import generics

from beapi.serializers import ConsumerCardSerializer
from beapi.models import ConsumerCard
from beapi.serializers import ConsumerAccountSerializer
from beapi.models import ConsumerAccount
from beapi.serializers import ConsumerTxnSerializer
from beapi.models import ConsumerTxn
from beapi.serializers import ConsumerTagSerializer
from beapi.models import ConsumerTag
from beapi.serializers import TxnTagSerializer
from beapi.models import TxnTag


class ConsumerAccountList(generics.ListCreateAPIView):
    queryset = ConsumerAccount.objects.all()
    serializer_class = ConsumerAccountSerializer

class ConsumerAccount(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConsumerAccount.objects.all()
    serializer_class = ConsumerAccountSerializer

class ConsumerCardVOList(generics.ListCreateAPIView):
    queryset = ConsumerCard.objects.all()
    serializer_class = ConsumerCardSerializer

class ConsumerCardVO(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConsumerCard.objects.all()
    serializer_class = ConsumerCardSerializer

class ConsumerTxnList(generics.ListCreateAPIView):
    queryset = ConsumerTxn.objects.all()
    serializer_class = ConsumerTxnSerializer

class ConsumerTxn(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConsumerTxn.objects.all()
    serializer_class = ConsumerTxnSerializer

class ConsumerTagList(generics.ListCreateAPIView):
    queryset = ConsumerTag.objects.all()
    serializer_class = ConsumerTagSerializer

class ConsumerTag(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConsumerTag.objects.all()
    serializer_class = ConsumerTagSerializer

class TxnTagList(generics.ListCreateAPIView):
    queryset = TxnTag.objects.all()
    serializer_class = TxnTagSerializer

class TxnTag(generics.RetrieveUpdateDestroyAPIView):
    queryset = TxnTag.objects.all()
    serializer_class = TxnTagSerializer


