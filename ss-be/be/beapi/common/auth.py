from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import authentication
from rest_framework import exceptions

from beapi.models import Consumer
from beapi.models import ConsumerDevice
from beapi.models import Client
from beapi.models import Merchant
from beapi.consumer.consumerService import ConsumerService
from beapi.exception.ssException import SSException
from beapi.common.cacheService import CacheService


class SSAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        cacheService = CacheService()
        deviceToken = request.META.get('HTTP_SSTOKEN')
        if not deviceToken:
            raise exceptions.NotAuthenticated(SSException.AUTH_FAILED)
        try:
            cd = cacheService.getConsumerDeviceByToken(deviceToken)
            c = cacheService.getConsumerById(cd.consumerId)
            return (c, None)
        except ConsumerDevice.DoesNotExist:
            cs = ConsumerService()
            cid = cs.registerDevice(deviceToken)
            c = Consumer.objects.get(id=cid)
            return (c, None)

class SSClientAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_SSCLIENTTOKEN')
        cacheService = CacheService()
        if not token:
            raise exceptions.NotAuthenticated(SSException.AUTH_FAILED)
        try:
            client = cacheService.getClientByToken(token)
            return (client, None)
        except Client.DoesNotExist:
            raise exceptions.NotAuthenticated(SSException.AUTH_FAILED)

class SSMerchantAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        uuid = request.META.get('HTTP_SSMERCHANTTOKEN')
        cacheService = CacheService()
        if not uuid:
            raise exceptions.NotAuthenticated(SSException.AUTH_FAILED)
        try:
            merchant = cacheService.getMerchantByUuid(uuid)
            if merchant.installed == 1:
                return (merchant, None)
            else:
                raise exceptions.NotAuthenticated(SSException.AUTH_FAILED)
        except Merchant.DoesNotExist:
            raise exceptions.NotAuthenticated(SSException.AUTH_FAILED)
