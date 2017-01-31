import random
from _ctypes import Array
import json
from decimal import Decimal

from rest_framework import generics

from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.common.constants import SSConst
from beapi.models import ConsumerCard
from beapi.models import Consumer
from beapi.models import Merchant
from beapi.models import ConsumerPrefs
from beapi.models import ConsumerAgg
from beapi.models import ConsumerTxn
from beapi.constantModels import TxnCategory
from beapi.common.cacheService import CacheService
from beapi.consumerCard.cardService import CardService


class TxnValidationVO():
    def __init__(self, immediateApproval, recordTxn, approval, remarks, sendNotif):
        self.immediateApproval = immediateApproval
        self.recordTxn = recordTxn
        self.approval = approval
        self.remarks = remarks
        self.sendNotif = sendNotif
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

class TxnValidatorService:
    def getApproval(self, cardNum, amount, merchantUuid,merchantName, txType,
                     mccCode):
        ssConst = SSConst()
        consumerCard = None
        consumer = None
        category = None
        prefs = None
        aggs = None
        merchant = None
        millis = SSUtil.getMillis()
        cacheService = CacheService()
        cardService = CardService()
        approvalTypeJson = ssConst.getJson(ssConst.APPROVAL_TYPES)
        print "1"
        # Check if card exists
        try:
            consumerCard = cacheService.getCardByNum(cardNum)
        except Exception as e:
            return TxnValidationVO(False, False, 'Block', SSException.INVALID_CARD, False )
        print "1.5 "+str(consumerCard.blockedTxTypes)

        if SSUtil.isIdinList(consumerCard.blockedTxTypes, txType):
                 return TxnValidationVO(False, True, 'Block',
                                        txType+" transactions are disabled.", True)

        print "2"
        try:
            merchant = cacheService.getMerchantByUuid(merchantUuid)
        except Exception as e:
            pass
        print "3"

        # Check if card is blocked
        if consumerCard.status == 0:
            return TxnValidationVO(False, True, 'Block', "Your card is blocked.", True )

        print "4"

        # By any chance the category is not in our records, go back,
        # Also need this for previous txn
        try:
            category = cacheService.getCategoryByMccCode(mccCode)
        except TxnCategory.DoesNotExist:
            return TxnValidationVO(False, False, 'Block', "Unknown category.", False )
        print "5"

        # if it was tried in last 10 minutes and user approved it - go ahead
        try:
            if not merchant is None:
                maxAllowedCreatedTime = millis - ssConst.ALLOWED_MILLIS_FOR_RETRY
                qs = ConsumerTxn.objects.all().filter(consumerId=consumerCard.consumerId,
                              cardId=consumerCard.id, txType__endswith=txType,
                              category_id=category.id,merchant_id = merchant.id,
                              amtSpentSS = amount,
                              created__gt = maxAllowedCreatedTime
                              ).order_by('-created')[:1]
                consumerTxn = qs[0]
                if not consumerTxn is None and consumerTxn.ssApprovalStatus == ssConst.APPROVAL_STATUSES[3][0]:
                    return TxnValidationVO(True, True, 'Approve',
                                           "We approved a transaction on your card for "+ssConst.CURRENCY_SYMBOL+str(amount) +".", True )
        except Exception as e:
            print "Error while matching transaction "+e.message
            pass
        print "6"

        # No point in moving further if the consumer doesn't exist, but don't record it for now
        try:
            consumer = cacheService.getConsumerById(consumerCard.consumerId)
        except Consumer.DoesNotExist:
            return TxnValidationVO(False, False, 'Block', SSException.INVALID_USER, False )
        print "7"

        # Check if merchant is blocked
        print "blocked merchants are  "+consumer.blockedMerchants
        if not merchant is None:
            if SSUtil.isIdinList(consumer.blockedMerchants, merchant.id):
                 return TxnValidationVO(False, True,'Block',
                                        "You have blocked all transactions from Merchant \""+ merchant.name+"\"", True)
        print "8"

        # Now check the aggregates and preferences
        prefs = cacheService.getConsumerPrefs(consumer.id)
        if not prefs:
            cardService.createDefaultPrefsAndAggs(consumerCard)
        print "9"

        aggs = cacheService.getConsumerAggs(consumer.id)
        if not aggs:
            #TODO:  If user has no aggregates then no point in holding it - we just tried creating
            return TxnValidationVO(True, True, 'Block', "Internal server error - No aggregates available for the user. ", False)
        for pref in prefs:
             #Ignore the preferences which are of no use for this transaction
            if pref.categoryKey != 'Any' and pref.categoryKey != category.name:
                continue
            if pref.txType != 'Any' and pref.txType != txType:
                continue
            if not merchant is None and pref.merchantId != -1 and pref.merchantId != merchant.id:
                continue
            if pref.cardId != -1 and pref.cardId != consumerCard.id:
                continue

            # Compare matching aggs for the rest of the preferences
            for agg in aggs:
                 if pref.periodKey == agg.periodKey and pref.categoryKey == agg.categoryKey and pref.txType == agg.txType and agg.merchantId == pref.merchantId and agg.cardId == pref.cardId:
                    if pref.limit < (agg.amtSpentSS + Decimal(amount)):
                        if  pref.ssApproval == 'Block' or pref.ssApproval == 'AskMe' :
                            msgToUser = "You have exceeded your "+pref.periodKey.lower()+" spend limit of  "+ssConst.CURRENCY_SYMBOL+str(pref.limit)
                            if pref.categoryKey != 'Any':
                                msgToUser = msgToUser +" for " + pref.categoryKey
                            msgToUser = msgToUser +"."
                            return TxnValidationVO(False, True, pref.ssApproval,
                                                   msgToUser, True)
        print "10"

        return TxnValidationVO(True, True,'Approve', "We approved a "+ssConst.CURRENCY_SYMBOL+str(amount) +" charge from "+merchantName+".", True)



