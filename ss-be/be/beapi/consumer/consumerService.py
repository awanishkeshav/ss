from rest_framework import generics

from beapi.common.ssUtil import SSUtil
from beapi.common.constants import SSConst
from beapi.models import Consumer
from beapi.models import ConsumerCard
from beapi.models import ConsumerPrefs
from beapi.models import ConsumerAgg
from beapi.models import ConsumerDevice
from beapi.models import ConsumerMerchant
from beapi.models import Merchant
from beapi.exception.ssException import SSException
from beapi.common.cacheService import CacheService
from beapi.consumerCard.txnService import TxnService
from beapi.merchant.merchantService import MerchantService
from gettext import lngettext


class ConsumerService:

   def registerDevice(self, deviceToken):
        # first check if device exists
        try:
            cc = ConsumerDevice.objects.get(deviceToken=deviceToken)
            raise Exception(SSException.DEVICE_TOKEN_EXISTS)
        except ConsumerDevice.DoesNotExist:
            t = SSUtil.getMillis()
            firstName = 'Vijay'
            lastName='Kalra'
            c = Consumer(created=t, updated=t)
            c.save()
            cc = ConsumerDevice(firstname=firstName, lastname=lastName, deviceToken=deviceToken, consumerId=c.id, created=t, updated=t)
            cc.save()
            return cc.id

   def registerDeviceGCMRegistrationId(self, registrationId, consumerId):
        millis = SSUtil.getMillis()
        cacheService = CacheService()
        try:
           consumerDevice = ConsumerDevice.objects.get(consumerId=consumerId)
           consumerDevice.deviceRegistrationId = registrationId
           consumerDevice.updated = millis
           consumerDevice.save()
           cacheService.setDevice(consumerDevice.id)
           return 1
        except:
           raise Exception(SSException.PROCESSING_FAILED)

   def toggleCardLockStatus(self, cardId, consumerId):
        millis = SSUtil.getMillis()
        cacheService = CacheService()
        statusFlag = 0
        try:
           consumer = Consumer.objects.get(id=consumerId)
           consumerCard = ConsumerCard.objects.get(id=cardId)

           if SSUtil.isIdinList(consumer.blockedCards,cardId):
               consumer.blockedCards = SSUtil.removeIdFromList(consumer.blockedCards,cardId)
               statusFlag = 1
               consumerCard.status=1
           else:
               consumer.blockedCards = SSUtil.addIdToList(consumer.blockedCards,cardId)
               statusFlag = 0
               consumerCard.status=0

           consumer.updated = millis
           consumerCard.updated = millis
           consumer.save()
           cacheService.setConsumer(consumer.id)
           consumerCard.save()
           cacheService.setCard(consumerCard.id)
           return statusFlag
        except:
           raise Exception(SSException.PROCESSING_FAILED)

   def lockMerchantStatus(self, merchantId, consumerId):
        millis = SSUtil.getMillis()
        statusFlag = 0
        cacheService = CacheService()
        try:
            consumer = Consumer.objects.get(id=consumerId)

            if not SSUtil.isIdinList(consumer.blockedMerchants,merchantId):
                consumer.blockedMerchants = SSUtil.addIdToList(consumer.blockedMerchants,merchantId)
                statusFlag = 0

            consumer.updated = millis
            consumer.save()
            cacheService.setConsumer(consumer.id)
            merchServ = MerchantService()
            merchServ.toggleStatus(merchantId, consumerId,statusFlag)
            return statusFlag
        except:
           raise Exception(SSException.PROCESSING_FAILED)

   def unlockMerchantStatus(self, merchantId, consumerId):
        millis = SSUtil.getMillis()
        statusFlag = 1
        cacheService = CacheService()
        try:
            consumer = Consumer.objects.get(id=consumerId)

            if SSUtil.isIdinList(consumer.blockedMerchants,merchantId):
                consumer.blockedMerchants = SSUtil.removeIdFromList(consumer.blockedMerchants,merchantId)
                statusFlag = 1

            consumer.updated = millis
            consumer.save()
            cacheService.setConsumer(consumer.id)
            merchServ = MerchantService()
            merchServ.toggleStatus(merchantId, consumerId,statusFlag)
            return statusFlag
        except:
           raise Exception(SSException.PROCESSING_FAILED)

   def getConsumerDevice(self, consumerId):
        return ConsumerDevice.objects.get(consumerId=consumerId)

   def getPrefsJson(self, consumerId, cardId):
       consumerCard = None
       cacheService = CacheService()
       ssConst = SSConst()
       periodKeysJson = ssConst.getJson(ssConst.PERIOD_KEYS)
       txnTypesJson = ssConst.getJson(ssConst.TXN_TYPES)
       approvalTypeJson = ssConst.getJson(ssConst.APPROVAL_TYPES)
       try:
           consumerCard = ConsumerCard.objects.get(id=cardId)
       except ConsumerCard.DoesNotExist:
           raise Exception(SSException.CARD_NOT_PRESENT)
       prefsJson = {
                     "txTypes": {"Online":1,"International":1},
                     "limits": { "Daily":{"userLimit":consumerCard.limit, "action":"Block", "maxLimit":consumerCard.limit},
                                 "Monthly":{"userLimit":consumerCard.limit, "action":"Block", "maxLimit":consumerCard.limit},
                                },
                     "customLimits":[]
                    }
       if SSUtil.isIdinList(consumerCard.blockedTxTypes, "Online"):
          prefsJson["txTypes"]["Online"] = 0
       if SSUtil.isIdinList(consumerCard.blockedTxTypes, "International"):
          prefsJson["txTypes"]["International"] = 0
       prefs = cacheService.getConsumerPrefs(consumerId)
       if prefs:
           for pref in prefs:
               if str(pref.cardId) == str(cardId):
                   if pref.categoryKey == 'Any':
                       prefsJson["limits"][pref.periodKey]["userLimit"] = pref.limit
                       prefsJson["limits"][pref.periodKey]["action"] = pref.ssApproval
                   else:
                       customLimit = {}
                       if not customLimit.get(pref.periodKey):
                           customLimit[pref.periodKey] = {}
                       customLimit[pref.periodKey]["userLimit"] = pref.limit
                       customLimit[pref.periodKey]["action"] = pref.ssApproval
                       customLimit[pref.periodKey]["categoryKey"] = pref.categoryKey
                       customLimit[pref.periodKey]["maxLimit"] = consumerCard.limit
                       prefsJson["customLimits"].append(customLimit)
       return prefsJson

   def savePref(self, consumerId, cardId, categoryKey, periodKey, action, userLimit):
        pref = None
        millis = SSUtil.getMillis()
        cacheService = CacheService()
        txnService = TxnService()
        try:
            if categoryKey is None:
                pref = ConsumerPrefs.objects.get(consumerId=consumerId,
                                    cardId = cardId, periodKey=periodKey,
                                    categoryKey='Any')
            else:
                pref = ConsumerPrefs.objects.get(consumerId=consumerId,
                                    cardId = cardId, periodKey= periodKey,
                                    categoryKey=categoryKey)
        except ConsumerPrefs.DoesNotExist:
                pref = ConsumerPrefs()
                pref.consumerId = consumerId
                pref.cardId = cardId
                pref.periodKey = periodKey
                pref.categoryKey = categoryKey
                pref.created = millis
                pref.txType = "Any"
                pref.merchantId = -1
        pref.ssApproval = action
        pref.limit = userLimit
        pref.updated = millis
        pref.save()
        cacheService.setConsumerPrefs(consumerId)
        txnService.recalculateAgg(consumerId, None, None)
        cacheService.setConsumerAggs(consumerId)
        return pref

   def deletePref(self, consumerId, cardId, categoryKey, periodKey):
        pref = None
        millis = SSUtil.getMillis()
        cacheService = CacheService()
        txnService = TxnService()
        try:
            pref = ConsumerPrefs.objects.get(consumerId=consumerId,
                                    cardId = cardId, periodKey= periodKey,
                                    categoryKey=categoryKey)
            pref.delete()
        except ConsumerPrefs.DoesNotExist:
            pass

        try:
            agg = ConsumerAgg.objects.get(consumerId=consumerId,
                                    cardId = cardId, periodKey= periodKey,
                                    categoryKey=categoryKey)
            agg.delete()
        except ConsumerAgg.DoesNotExist:
            pass
        cacheService.setConsumerPrefs(consumerId)
        txnService.recalculateAgg(consumerId, None, None)
        cacheService.setConsumerAggs(consumerId)
        return True

   def saveLocation(self, consumerId, lat, lng):
        consumer = Consumer.objects.get(id=consumerId)
        consumer.lat = lat
        consumer.lng = lng
        consumer.save()
        # Find consumer's merchants
        try:
            lst = ConsumerMerchant.objects.all().filter(consumerId=consumerId)
            for cm in lst:
                try:
                    m = Merchant.objects.get(id=cm.merchant_id)
                    kms = SSUtil.distanceInKms(m.lat,m.lng,lat, lng)
                    cm.currentDistance = kms
                    cm.save()
                except:
                    pass
        except:
            pass
        return True


