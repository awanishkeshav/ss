import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from rest_framework.decorators import authentication_classes

from beapi.consumer.consumerService import ConsumerService
from beapi.exception.ssException import SSException
from beapi.common.jsonResponse import JSONResponse
from beapi.common.auth import SSAuth
from beapi.models import Consumer
from beapi.models import ConsumerPrefs
from beapi.serializers import ConsumerSerializer
from beapi.serializers import ConsumerPrefsSerializer
from beapi.serializers import ConsumerCardSerializer
from beapi.serializers import ConsumerMerchantSerializer
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.decorators import list_route
from beapi.models import ConsumerCard
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from django.core.cache import cache
from beapi.merchant.merchantService import MerchantService
@api_view(['GET'])
@authentication_classes((SSAuth,))
def testAuth(request, format=None):
    c = request.user
    print "auth called"
    cache.set('a-unique-key', 'this is a string which will be cached')
    print cache.get('a-unique-key')
    content = {
            'user': unicode(c.id),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
    }
    return JSONResponse(content)


@api_view(['GET'])
def register(request, format=None):
    token = request.META.get('HTTP_SSTOKEN')
    try:
        if token is None:
             return JSONResponse(SSUtil.err(SSException.DEVICE_TOKEN_MISSING), status=status.HTTP_400_BAD_REQUEST)
        else:
            cs = ConsumerService()
            id = cs.registerDevice(token)
            return JSONResponse(SSUtil.success(id), status=status.HTTP_201_CREATED)
    except:
        return JSONResponse(SSUtil.err(SSException.DEVICE_TOKEN_EXISTS), status=status.HTTP_409_CONFLICT)


@api_view(['PUT'])
@authentication_classes((SSAuth,))
def toggleCardLockStatus(request, cardId):
    try:
        cs = ConsumerService()
        s = cs.toggleCardLockStatus(cardId, request.user.id)
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes((SSAuth,))
def lockMerchantStatus(request, merchantId):
    try:
        cs = ConsumerService()
        s = cs.lockMerchantStatus(merchantId, request.user.id)
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes((SSAuth,))
def unlockMerchantStatus(request, merchantId):
    try:
        cs = ConsumerService()
        s = cs.unlockMerchantStatus(merchantId, request.user.id)
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes((SSAuth,))
def saveDeviceRegistrationId(request):
    data = json.loads(request.body)
    try:
        if data['registrationId'] is None:
            raise Exception()
    except Exception as e:
        return JSONResponse(SSUtil.err(e.message),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        cs = ConsumerService()
        s = cs.registerDeviceGCMRegistrationId(data['registrationId'], request.user.id)
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConsumerViewSet(viewsets.ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer

    @authentication_classes((SSAuth,))
    @list_route(methods=['post','get'], url_path='cards')
    def cards(self, request, pk=None):

            if request.method == 'GET':
                cards = ConsumerCard.objects.all();
                serializer = ConsumerCardSerializer(cards, many=True)
                return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_201_CREATED)

            elif request.method == 'POST':
                consumer = request.user
                cc = ConsumerCard()
                cc.consumerId = consumer.id
                cc.cardNum = '1'
                cc.clientId = 0
                cc.limit = 10000
                cc.amtSpentSS = 1000
                cc.currOS = 1100
                cc.save()
                return JSONResponse(SSUtil.success(cc.id), status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def blockedMerchants(request):
    ms = MerchantService();
    serializer = ConsumerMerchantSerializer(ms.getBlockedMerchants(request.user.id), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getPrefs(request, cardId):
    try:
        cs = ConsumerService()
        prefJson = cs.getPrefsJson(request.user.id, cardId)
        return JSONResponse(SSUtil.success(prefJson), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes((SSAuth,))
def saveLimitPrefs(request, cardId):
    data = json.loads(request.body)
    if not 'categoryKey' in data or data['categoryKey'] is None:
        return JSONResponse(SSUtil.err("Category key is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    if not 'periodKey' in data or data['periodKey'] is None:
        return JSONResponse(SSUtil.err("Period key is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    if not 'userLimit' in data or data['userLimit'] is None:
        return JSONResponse(SSUtil.err("User specified limit is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    if not 'action' in data or data['action'] is None:
        return JSONResponse(SSUtil.err("action is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        cs = ConsumerService()
        s = cs.savePref(request.user.id, cardId, data['categoryKey'],
                        data['periodKey'], data['action'], data['userLimit'])
        ser = ConsumerPrefsSerializer(s, many=False)
        return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes((SSAuth,))
def deleteLimitPrefs(request, cardId):
    data = json.loads(request.body)
    if not 'categoryKey' in data or data['categoryKey'] is None:
        return JSONResponse(SSUtil.err("Category key is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    if not 'periodKey' in data or data['periodKey'] is None:
        return JSONResponse(SSUtil.err("Period key is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        cs = ConsumerService()
        s = cs.deletePref(request.user.id, cardId, data['categoryKey'],
                        data['periodKey'])
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes((SSAuth,))
def saveLocation(request):
    data = json.loads(request.body)
    if not 'lat' in data or data['lat'] is None:
        return JSONResponse(SSUtil.err("Latitude  is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    if not 'lng' in data or data['lng'] is None:
        return JSONResponse(SSUtil.err("Longitude  is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        cs = ConsumerService()
        s = cs.saveLocation(request.user.id,   data['lat'],
                            data['lng'])
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
