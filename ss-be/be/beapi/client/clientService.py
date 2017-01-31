from rest_framework import generics
from beapi.models import Client
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.common.cacheService import CacheService


class ClientService:
    def get(self, clientId):
        # first check if card exists in consumer account
        try:
            cacheService = CacheService()
            ca = cacheService.getClientById(clientId)
            return ca
        except Client.DoesNotExist:
            raise Exception(SSException.CLIENT_NOT_PRESENT)
