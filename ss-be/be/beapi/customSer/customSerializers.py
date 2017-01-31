from rest_framework import serializers
from beapi.serializers import ConsumerOfferSerializer

class TxnTagSummarySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tagName = serializers.CharField(max_length=100)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

