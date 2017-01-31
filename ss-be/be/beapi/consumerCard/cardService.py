from rest_framework import generics
from beapi.models import ConsumerCard
from beapi.models import Consumer
from beapi.models import ConsumerDevice
from beapi.models import ConsumerAccount
from beapi.models import ConsumerTxn
from beapi.models import ConsumerPrefs
from beapi.models import ConsumerAgg
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.consumerCard.cardVO import CardVO
from beapi.common.cacheService import CacheService

from _ctypes import Array


class CardService:
    def registerCard(self, consumerId, cardNum, activationCode, phoneNum):
        # first check if card exists in consumer account
        try:
            ca = ConsumerAccount.objects.get(cardNum__endswith=cardNum,
                    activationCode=activationCode, phoneNum=phoneNum)
            # check if same card is already registered
            try:
                cc = ConsumerCard.objects.get(accountId=ca.id, cardNum=ca.cardNum)
                raise Exception(SSException.CARD_ALREADY_REGISTERED)
            except ConsumerCard.DoesNotExist:
                t = SSUtil.getMillis()
                # Only if card doesn't exist, register the card
                cc = ConsumerCard(consumerId=consumerId, accountId=ca.id,
                                  clientId=ca.clientId, cardNum=ca.cardNum,
                                  limit=ca.limit, avaialbleLimit=ca.avaialbleLimit,
                                  amtSpentSS=ca.currOS, currOS=ca.currOS,
                                  cardNetwork=ca.cardNetwork,cardType=ca.cardType,
                                  cardTitle=ca.cardTitle, status=1, created=t, updated=t)
                cc.save()
                self.createDefaultPrefsAndAggs(cc)
                return cc
        except ConsumerAccount.DoesNotExist:
            raise Exception(SSException.CARD_NOT_PRESENT)

    def getCards(self, consumerId, pk=None):
        try:
            if pk is None:
                cards = ConsumerCard.objects.all().filter(consumerId=consumerId)
                return cards
            else:
                return ConsumerCard.objects.get(id=pk)
        except ConsumerCard.DoesNotExist:
            return Array()

    def lockTxTypeStatus(self, cardId, txType):
        millis = SSUtil.getMillis()
        statusFlag = 0
        cacheService = CacheService()
        try:
            consumerCard = ConsumerCard.objects.get(id=cardId)

            if not SSUtil.isIdinList(consumerCard.blockedTxTypes,txType):
                consumerCard.blockedTxTypes = SSUtil.addIdToList(consumerCard.blockedTxTypes,txType)
                statusFlag = 0

            consumerCard.updated = millis
            consumerCard.save()
            cacheService.setCard(cardId)
            return statusFlag
        except:
           raise Exception(SSException.PROCESSING_FAILED)

    def unlockTxTypeStatus(self, cardId, txType):
        millis = SSUtil.getMillis()
        statusFlag = 1
        cacheService = CacheService()
        try:
            consumerCard = ConsumerCard.objects.get(id=cardId)

            if SSUtil.isIdinList(consumerCard.blockedTxTypes,txType):
                consumerCard.blockedTxTypes = SSUtil.removeIdFromList(consumerCard.blockedTxTypes,txType)
                statusFlag = 1

            consumerCard.updated = millis
            consumerCard.save()
            cacheService.setCard(cardId)
            return statusFlag
        except:
           raise Exception(SSException.PROCESSING_FAILED)

    def createDefaultPrefsAndAggs(self, card):
        agg = None
        pref = None
        defPeriodKeys = {"Daily","Monthly"}
        defAction = "Approve"
        millis = SSUtil.getMillis()
        cacheService = CacheService()
        for periodKey in defPeriodKeys:
            try:
                pref = ConsumerPrefs.objects.get(consumerId=card.consumerId,
                                    cardId = card.id, periodKey=periodKey,
                                    categoryKey='Any')
            except:
                pref = ConsumerPrefs()
                pref.consumerId = card.consumerId
                pref.cardId = card.id
                pref.periodKey = periodKey
                pref.categoryKey = 'Any'
                pref.created = millis
                pref.txType = "Any"
                pref.merchantId = -1
                pref.ssApproval = defAction
            pref.limit = card.limit
            pref.updated = millis
            pref.save()

            try:
                agg = ConsumerAgg.objects.get(consumerId=card.consumerId,
                                    cardId = card.id, periodKey=periodKey,
                                    categoryKey='Any')
            except:
                agg = ConsumerAgg()
                agg.consumerId = card.consumerId
                agg.cardId = card.id
                agg.periodKey = periodKey
                agg.categoryKey = 'Any'
                agg.created = millis
                agg.txType = "Any"
                agg.merchantId = -1
                agg.ssApproval = defAction
            agg.amtSpentSS = 0.00
            agg.updated = millis
            agg.save()
        cacheService.setConsumerPrefs(card.consumerId)
        cacheService.setConsumerAggs(card.consumerId)
