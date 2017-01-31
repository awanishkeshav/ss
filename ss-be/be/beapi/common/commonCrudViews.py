from rest_framework import generics

from beapi.serializers import TxnCategorySerializer
from beapi.constantModels import TxnCategory


class TxnCategoryList(generics.ListCreateAPIView):
    queryset = TxnCategory.objects.all()
    serializer_class = TxnCategorySerializer

class TxnCategory(generics.RetrieveUpdateDestroyAPIView):
    queryset = TxnCategory.objects.all()
    serializer_class = TxnCategorySerializer
