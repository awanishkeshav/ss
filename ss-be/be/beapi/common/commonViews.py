import json
from json import JSONEncoder

from django.core import serializers

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import list_route
from rest_framework.views import APIView
from rest_framework.response import Response

from beapi.common.jsonResponse import JSONResponse
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.common.constants import SSConst
from beapi.serializers import TxnCategorySerializer
from beapi.constantModels import TxnCategory
from beapi.constantModels import Location
from beapi.serializers import LocationSerializer

@api_view(['GET'])
def getConsts(request):
    return JSONResponse(SSUtil.success(SSConst().to_representation()), status=status.HTTP_200_OK)

@api_view(['GET'])
def getCategories(request):
    ser = TxnCategorySerializer(TxnCategory.objects.all(), many=True)
    return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)

@api_view(['GET'])
def getLocations(request):
    ser = LocationSerializer(Location.objects.all(), many=True)
    return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)