from beapi.models import ConsumerCard
from beapi.models import Consumer
from beapi.models import Client
from beapi.models import Merchant
from beapi.models import ConsumerPrefs
from beapi.models import ConsumerDevice
from beapi.models import ConsumerAgg
from beapi.models import ConsumerTxn
from beapi.constantModels import TxnCategory

from django.core.cache import cache
from beapi.common.cacheKeys import CacheKeys

class CacheService:

    def getCardByNum(self, cardNum):
        card = None
        if CacheKeys.useCache():
            try:
                card = cache.get(CacheKeys.getCardNumKey(cardNum))
            except:
                pass

        if card is None:
            print "getting card from db"
            card = ConsumerCard.objects.get(cardNum=cardNum)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getCardNumKey(card.cardNum), card, None)
        return card

    def setCard(self, cardId):
        card = ConsumerCard.objects.get(id=cardId)
        cache.set(CacheKeys.getCardNumKey(card.cardNum), card, None)


    def getClientByToken(self, token):
        client = None
        if CacheKeys.useCache():
            try:
                client = cache.get(CacheKeys.getClientTokenKey(token))
            except:
                pass

        if client is None:
            print "getting client from db"
            client = Client.objects.get(token=token)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getClientTokenKey(client.token), client, None)
        return client

    def getClientById(self, id):
        client = None
        if CacheKeys.useCache():
            try:
                client = cache.get(CacheKeys.getClientIdKey(str(id)))
            except:
                pass

        if client is None:
            print "getting client from db"
            client = Client.objects.get(id=id)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getClientIdKey(str(id)), client, None)
        return client

    def getConsumerDeviceByToken(self, token):
        consumerDevice = None
        if CacheKeys.useCache():
            try:
                consumerDevice = cache.get(CacheKeys.getConsumerDeviceTokenKey(token))
            except:
                pass

        if consumerDevice is None:
            print "getting consumerDevice from db"
            consumerDevice = ConsumerDevice.objects.get(deviceToken=token)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getConsumerDeviceTokenKey(consumerDevice.deviceToken), consumerDevice, None)
        return consumerDevice

    def setDevice(self, id):
        consumerDevice = ConsumerDevice.objects.get(id=id)
        cache.set(CacheKeys.getConsumerDeviceTokenKey(consumerDevice.deviceToken), consumerDevice, None)

    def getConsumerById(self, id):
        consumer = None
        if CacheKeys.useCache():
            try:
                consumer = cache.get(CacheKeys.getConsumerIdKey(str(id)))
            except:
                pass

        if consumer is None:
            print "getting consumer from db"
            consumer = Consumer.objects.get(id=id)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getConsumerIdKey(str(id)), consumer, None)
        return consumer

    def setConsumer(self, id):
        consumer = Consumer.objects.get(id=id)
        cache.set(CacheKeys.getConsumerIdKey(str(id)), consumer, None)


    def getMerchantByUuid(self, uuid):
        print "getting merchant from cache.."
        merchant = None
        if CacheKeys.useCache():
            try:
                print "getting consumer from cache"
                merchant = cache.get(CacheKeys.getMerchantUuidKey(str(uuid)))
                print "after getting consumer from cache"
            except:
                pass

        if merchant is None:
            print "getting merchant from db"
            merchant = Merchant.objects.get(uuid=uuid)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getMerchantUuidKey(str(uuid)), merchant, None)
        return merchant

    def getCategoryByMccCode(self, mccCode):
        txnCategory = None
        if CacheKeys.useCache():
            try:
                txnCategory = cache.get(CacheKeys.getCategoryByMccCodeKey(str(mccCode)))
            except:
                pass

        if txnCategory is None:
            print "getting txnCategory from db"
            txnCategory = TxnCategory.objects.get(mccCode=mccCode)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getCategoryByMccCodeKey(str(mccCode)), txnCategory, None)
        return txnCategory

    def getConsumerAggs(self, id):
        consumerAggs = None
        if CacheKeys.useCache():
            try:
                consumerAggs = cache.get(CacheKeys.getConsumerAggsByIdKey(str(id)))
            except:
                pass

        if consumerAggs is None:
            print "getting consumerAggs from db"
            consumerAggs = ConsumerAgg.objects.all().filter(consumerId=id)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getConsumerAggsByIdKey(str(id)), consumerAggs, None)
        return consumerAggs

    def setConsumerAggs(self, id):
        consumerAggs = ConsumerAgg.objects.all().filter(consumerId=id)
        cache.set(CacheKeys.getConsumerAggsByIdKey(str(id)), consumerAggs, None)

    def getConsumerPrefs(self, id):
        prefs = None
        if CacheKeys.useCache():
            try:
                prefs = cache.get(CacheKeys.getConsumerPrefsByIdKey(str(id)))
            except:
                pass

        if prefs is None:
            print "getting ConsumerPrefs from db"
            prefs = ConsumerPrefs.objects.all().filter(consumerId=id)
            if CacheKeys.useCache():
                cache.set(CacheKeys.getConsumerPrefsByIdKey(str(id)), prefs, None)
        return prefs

    def setConsumerPrefs(self, id):
        consumerPrefs = ConsumerPrefs.objects.all().filter(consumerId=id)
        cache.set(CacheKeys.getConsumerPrefsByIdKey(str(id)), consumerPrefs, None)