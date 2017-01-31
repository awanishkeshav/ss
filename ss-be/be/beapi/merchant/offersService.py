from rest_framework import generics
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from _ctypes import Array
from beapi.common.constants import SSConst
from beapi.common.cacheService import CacheService
from beapi.notif.android import Android

from beapi.models import ConsumerTxn
from beapi.models import Merchant
from beapi.models import MerchantOffer
from beapi.models import MerchantOfferTargetting
from beapi.models import ConsumerOffer
from beapi.models import ConsumerMerchant
from django.db.models import Q

from beapi.consumerCard.txnService import TxnService
from beapi.consumer.consumerService import ConsumerService

class OffersService:

    def processOfferNotification(self, txnId, targetType, deviceRegistrationId):
        millis = SSUtil.getMillis()
        ssConst = SSConst()
        txnService = TxnService()
        android = Android()
        consumerServ = ConsumerService()

        txn = ConsumerTxn.objects.get(id=txnId)
        if deviceRegistrationId is None:
            consumerDevice = consumerServ.getConsumerDevice(txn.consumerId)
            deviceRegistrationId = consumerDevice.deviceRegistrationId
        miscDetails = txnService.getTxnMiscDetails(txn.consumerId, txn.cardId, txn.id)
         # Get the merchant
        merchant = Merchant.objects.get(id=txn.merchant_id)

        # Get the offers for that merchant
        offers = MerchantOffer.objects.all().filter(merchant_id=txn.merchant_id, status=ssConst.OFFER_STATUSES[0][0])

        # Check targetting for these offers
        notificationSent = False
        for offer in offers:
            targettings = MerchantOfferTargetting.objects.all().filter(offer_id=offer.id)
            for targetting in targettings:
                if targetting.targetType == targetType:
                    # check if consumer qualifies for the offer
                    if( int(miscDetails["totalOnMerchant"]) >= int(targetting.minTotalSpend)
                     or int(miscDetails["visitsOnMerchant"]) >= int(targetting.minVisits)):
                        self.addConsumerOfferIfRequired(txn.consumerId, offer, merchant.id)
                        # Send only one notification
                        if not notificationSent:
                            android.sendOfferNotification(deviceRegistrationId,offer.title,
                                                          "Offer from "+merchant.name,
                                                          ssConst.DEVICE_NOTIFICATION_TYPES["Offer"],
                                                          offer.id, merchant.id)
                            notificationSent = True

    def processOffersForExistingConsumers(self):
        ssConst = SSConst()
        txnService = TxnService()
        merchantOffers = MerchantOffer.objects.filter(status=ssConst.OFFER_STATUSES[0][0])
        for offer in merchantOffers:
            consumerMerchants = ConsumerMerchant.objects.filter(merchant_id=offer.merchant_id)
            for cm in consumerMerchants:
                miscDetails = txnService.getConsumerMerchantMiscDetails( cm.consumerId, offer.merchant_id)
                targettings = MerchantOfferTargetting.objects\
                                                 .all()\
                                                 .filter(offer_id=offer.id,
                                                         targetType = ssConst.OFFER_TARGET_TYPES[3][0])
                for targetting in targettings:
                    if( int(miscDetails["totalOnMerchant"]) >= int(targetting.minTotalSpend)
                     or int(miscDetails["visitsOnMerchant"]) >= int(targetting.minVisits)):
                        self.addConsumerOfferIfRequired(cm.consumerId, offer, offer.merchant_id)

    def addConsumerOfferIfRequired(self, consumerId, offer, merchantId):
       millis = SSUtil.getMillis()
       ssConst = SSConst()
       consumerOffer = None
       try:
           consumerOffer = ConsumerOffer.objects.get(consumerId=consumerId,
                                                 offer_id=offer.id)
       except ConsumerOffer.DoesNotExist:
           if consumerOffer is None:
               consumerOffer = ConsumerOffer()
               consumerOffer.created = millis
               consumerOffer.updated = millis
               consumerOffer.offer_id = offer.id
               consumerOffer.merchantId = merchantId
               consumerOffer.consumerId = consumerId
               consumerOffer.status = ssConst.CONSUMER_OFFER_STATUSES[0][0]
               consumerOffer.startDate = offer.startDate
               consumerOffer.endDate = offer.endDate
               consumerOffer.save()

    def markConsumerOffersRead(self, consumerId):
       millis = SSUtil.getMillis()
       ssConst = SSConst()
       consumerOffer = ConsumerOffer.objects \
                                    .filter(status = ssConst.CONSUMER_OFFER_STATUSES[0][0],
                                     consumerId=consumerId) \
                                     .update(status = ssConst.CONSUMER_OFFER_STATUSES[1][0])
       return True

    def getConsumerOffers(self, consumerId):
       currTimeMillis = SSUtil.getMillis()
       ssConst = SSConst()
       consumerOffers = ConsumerOffer.objects \
                                     .filter(Q(status=ssConst.CONSUMER_OFFER_STATUSES[0][0])
                                      | Q(status=ssConst.CONSUMER_OFFER_STATUSES[1][0]),
                                      consumerId=consumerId, endDate__gt=currTimeMillis
                                      ).order_by("-updated")
       return consumerOffers

    def getConsumerOffersByMerchant(self, consumerId, merchantId):
       ssConst = SSConst()
       currTimeMillis = SSUtil.getMillis()
       consumerOffers = ConsumerOffer.objects \
                                     .filter(Q(status=ssConst.CONSUMER_OFFER_STATUSES[0][0])
                                      | Q(status=ssConst.CONSUMER_OFFER_STATUSES[1][0]),
                                      consumerId=consumerId, merchantId = merchantId
                                      , endDate__gt=currTimeMillis
                                      ).order_by("-updated")
       return consumerOffers



    def getOnDemandConsumerOffersByMerchant(self, consumerId, merchantId):
        ssConst = SSConst()
        txnService = TxnService()
        currTimeMillis = SSUtil.getMillis()
        merchantOffers = MerchantOffer.objects.filter(status=ssConst.OFFER_STATUSES[0][0], merchant_id = merchantId)
        miscDetails = txnService.getConsumerMerchantMiscDetails( consumerId, merchantId)
        for offer in merchantOffers:
            targettings = MerchantOfferTargetting.objects\
                                                 .all()\
                                                 .filter(offer_id=offer.id,
                                                         targetType = ssConst.OFFER_TARGET_TYPES[4][0])
            for targetting in targettings:
                    if( int(miscDetails["totalOnMerchant"]) >= int(targetting.minTotalSpend)
                     or int(miscDetails["visitsOnMerchant"]) >= int(targetting.minVisits)):
                        self.addConsumerOfferIfRequired(consumerId, offer, offer.merchant_id)


        consumerOffers = ConsumerOffer.objects \
                                     .filter(Q(status=ssConst.CONSUMER_OFFER_STATUSES[0][0])
                                      | Q(status=ssConst.CONSUMER_OFFER_STATUSES[1][0]),
                                      consumerId=consumerId, merchantId = merchantId
                                      , endDate__gt=currTimeMillis
                                      ).order_by("-updated")
        return consumerOffers

    def countNewOffers(self, consumerId):
       ssConst = SSConst()
       cnt = ConsumerOffer.objects \
                          .filter(status=ssConst.CONSUMER_OFFER_STATUSES[0][0],
                                  consumerId=consumerId)\
                          .count()
       return cnt

