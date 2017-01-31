from rest_framework import generics
from beapi.models import ConsumerCard
from beapi.models import Consumer
from beapi.models import ConsumerDevice
from beapi.models import ConsumerAccount
from beapi.models import ConsumerTxn
from beapi.models import TxnTag
from beapi.models import ConsumerTag
from beapi.models import ReviewTemplate
from beapi.models import ConsumerPrefs
from beapi.models import ConsumerAgg
from beapi.models import Merchant
from beapi.constantModels import TxnCategory
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.common.constants import SSConst
from beapi.rulesEngine.txnValidatorService import TxnValidationVO
from _ctypes import Array
from beapi.common.constants import SSConst
from beapi.common.cacheService import CacheService
from beapi.merchant.merchantService import MerchantService
from beapi.common.searchService import SearchService
from beapi.serializers import ConsumerTxnSerializer


class TxnService:

    def getTxn(self, consumerId, cardId, txnId):
        try:
            txn = ConsumerTxn.objects.get(id=txnId)
            return txn
        except ConsumerTxn.DoesNotExist:
            return None
    def getConsumerMerchantMiscDetails(self, consumerId, merchantId):
        try:
            miscDetails = {"totalOnMerchant" : 0.00,
                              "visitsOnMerchant" : 0  }
            try:
                totalOnMerchantMap = {'pk': 'id',
                     'total': 'total'}
                totalOnMerchant =  ConsumerTag.objects.raw(
                                    '''
                                    select sum(amtSpentSS) as total, 1 as id
                                    from ss_consumer_txn
                                    where merchant_id=%s
                                    and consumerId=%s
                                    and ssApproval='Approve'
                                    ''',[ merchantId,  consumerId], translations=totalOnMerchantMap)
                totalM = 0;
                for x in totalOnMerchant:
                    totalM = x.total
                if totalM is None:
                    totalM = 0.00
                miscDetails["totalOnMerchant"] = totalM

                visitsOnMerchantMap = {'pk': 'id',
                     'total': 'total'}
                visitsOnMerchant =  ConsumerTag.objects.raw(
                                    '''
                                    select count(*) as total, 1 as id
                                    from ss_consumer_txn
                                    where merchant_id=%s
                                    and consumerId=%s
                                    and ssApproval='Approve'
                                    ''',[merchantId,  consumerId], translations=visitsOnMerchantMap)
                totalV = 0;
                for x in visitsOnMerchant:
                    totalV = x.total
                if totalV is None:
                    totalV = 0
                miscDetails["visitsOnMerchant"] = totalV
                return miscDetails
            except ConsumerTxn.DoesNotExist:
                return None
        except ConsumerTxn.DoesNotExist:
            return None

    def getTxnMiscDetails(self, consumerId, cardId, txnId):
        try:
            txn = ConsumerTxn.objects.get(id=txnId)
            millis = SSUtil.getMillis()
            millisOneMonthBack = millis - (30*86400*1000)
            miscDetails = {"totalOnMerchant" : 0.00,
                              "visitsOnMerchant" : 0,
                              "monthlyOnCategory" : 0.00 }
            try:
                totalOnMerchantMap = {'pk': 'id',
                     'total': 'total'}
                totalOnMerchant =  ConsumerTag.objects.raw(
                                    '''
                                    select sum(amtSpentSS) as total, 1 as id
                                    from ss_consumer_txn
                                    where merchant_id=%s
                                    and cardId=%s
                                    and consumerId=%s
                                    and ssApproval='Approve'
                                    ''',[txn.merchant_id, txn.cardId, txn.consumerId], translations=totalOnMerchantMap)
                totalM = 0;
                for x in totalOnMerchant:
                    totalM = x.total
                if totalM is None:
                    totalM = 0.00
                miscDetails["totalOnMerchant"] = totalM

                visitsOnMerchantMap = {'pk': 'id',
                     'total': 'total'}
                visitsOnMerchant =  ConsumerTag.objects.raw(
                                    '''
                                    select count(*) as total, 1 as id
                                    from ss_consumer_txn
                                    where merchant_id=%s
                                    and cardId=%s
                                    and consumerId=%s
                                    and ssApproval='Approve'
                                    ''',[txn.merchant_id, txn.cardId, txn.consumerId], translations=visitsOnMerchantMap)
                totalV = 0;
                for x in visitsOnMerchant:
                    totalV = x.total
                if totalV is None:
                    totalV = 0
                miscDetails["visitsOnMerchant"] = totalV

                monthlyOnCategoryMap = {'pk': 'id',
                     'total': 'total'}
                monthlyOnCategory =  ConsumerTag.objects.raw(
                                    '''
                                    select sum(amtSpentSS)  as total, 1 as id
                                    from ss_consumer_txn
                                    where category_id=%s
                                    and cardId=%s
                                    and consumerId=%s
                                    and created > %s
                                    and ssApproval='Approve'
                                    ''',[txn.category_id, txn.cardId, txn.consumerId, millisOneMonthBack], translations=monthlyOnCategoryMap)
                totalC = 0;
                for x in monthlyOnCategory:
                    totalC = x.total
                if totalC is None:
                    totalC = 0.00
                miscDetails["monthlyOnCategory"] = totalC
                return miscDetails
            except ConsumerTxn.DoesNotExist:
                return None
        except ConsumerTxn.DoesNotExist:
            return None

    def getTxns(self, consumerId, cardId, start, limit, tagIds, searchParams):
        #manipulate the limit for django
        limit = limit + start
        try:
            if not tagIds is None and tagIds != '':
                tidList = [int(x) for x in tagIds.split(',')]
                txnTagIds = TxnTag.objects.values('consumerTxn').filter(cardId=cardId, consumerTag__in=tidList)
                txns = ConsumerTxn.objects.all().order_by('-created').filter(ssApproval='Approve', cardId=cardId, id__in=txnTagIds)[start:limit]
            else:
                txns = ConsumerTxn.objects.all().order_by('-created').filter(ssApproval='Approve', cardId=cardId)[start:limit]
            return txns
        except ConsumerTxn.DoesNotExist:
            return Array()

    def getTxnTaggedSummary(self, consumerId, cardId, start, limit):
        #manipulate the limit for django
        limit = limit + start
        name_map = {'pk': 'id',
                     'tagName': 'tagName',
                     'total': 'total'}
        try:
          summary =  ConsumerTag.objects.raw(
                                    '''
                                    select sum(t.amtSpentSS) as total,
                                    ctag.id as id,ctag.tag as tagName
                                    from ss_consumer_txn t,
                                    ss_consumer_tag ctag, ss_txn_tag tt
                                    where tt.consumerTxn_id=t.id and tt.consumerTag_id=ctag.id
                                    and t.cardId=%s
                                    group by ctag.id;
                                    ''',[cardId], translations=name_map)
          return summary
        except ConsumerTxn.DoesNotExist:
            return Array()


    def recordTxn(self, cardNum, txType, amount, mccCode, merchantUuid, merchantName, txnApprovalVO):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        cacheService = CacheService()
        merchServ = MerchantService()
        merchant = None
        print "inside record txn "+merchantUuid
        try:
            consumerCard = cacheService.getCardByNum(cardNum)
            category = cacheService.getCategoryByMccCode(mccCode)
            approvalTypeJson = ssConst.getJson(ssConst.APPROVAL_TYPES)
            try:
                merchant = cacheService.getMerchantByUuid(str(merchantUuid))
            except:
                merchant = merchServ.createMerchant(merchantUuid, merchantName, None, None,mccCode)
            # Record transaction
            txn = ConsumerTxn()
            txn.consumerId = consumerCard.consumerId
            txn.cardId = consumerCard.id
            txn.txType = txType
            txn.txDate = currTimeMillis
            txn.amtSpentSS = amount
            txn.category_id = category.id
            txn.merchant_id = merchant.id
            txn.reviewStatus = merchant.reviewStatus
            txn.ssApproval = txnApprovalVO.approval
             # decide over the status
            if(txnApprovalVO.approval == 'Approve' or txnApprovalVO.approval == 'Warn'):
                txn.ssApprovalStatus = ssConst.APPROVAL_STATUSES[0][0]
            if(txnApprovalVO.approval == 'Block'):
                txn.ssApprovalStatus = ssConst.APPROVAL_STATUSES[1][0]
            if(txnApprovalVO.approval == 'AskMe'):
                txn.ssApprovalStatus = ssConst.APPROVAL_STATUSES[2][0]

            txn.created = currTimeMillis
            txn.updated = currTimeMillis
            txn.save()

            #Establish relation with consumer and merchant
            merchServ.addConsumerRelation(merchant.id, consumerCard.consumerId)
            searchServ = SearchService()
            txnSerializer = ConsumerTxnSerializer(txn, many=False)
            if(txnApprovalVO.approval == 'Approve' or txnApprovalVO.approval == 'Warn'):
                searchServ.upload("txn",txn.id, txnSerializer.data);
            return txn

        except Exception as e:
            print "Exception while recording txn "+e.message
            # actually log the fact that it has gone wrong
            pass

    def recalculateAgg(self, consumerId, recentAmount, recentTxn):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        cacheService = CacheService()
        prefs = cacheService.getConsumerPrefs(consumerId)
        name_map = {'total': 'total', 'pk':'id'}
        periodKeysJson = ssConst.getJson(ssConst.PERIOD_KEYS)
        approvalTypeJson = ssConst.getJson(ssConst.APPROVAL_TYPES)
        if prefs:
            for pref in prefs:
                consumerAgg = ConsumerAgg()

                querySt = "select sum(amtSpentSS) as total, 1 as id from ss_consumer_txn where consumerId ="+str(consumerId)
                querySt += " and ssApproval='"+ssConst.APPROVAL_TYPES[0][0]+"'"
                if pref.periodKey != 'Any':
                    print "period key is "+pref.periodKey
                    print " value is "+periodKeysJson[pref.periodKey]
                    querySt += " and  FROM_UNIXTIME(created/1000) >= DATE_SUB(FROM_UNIXTIME("+str(currTimeMillis/1000)+"), INTERVAL "+periodKeysJson[pref.periodKey] + ")"
                if pref.categoryKey != 'Any':
                    category = TxnCategory.objects.get(name=pref.categoryKey)
                    querySt += " and  category_id = " + str(category.id)
                if pref.txType != 'Any':
                    querySt += " and  txType = '" + pref.txType +"'"
                if pref.cardId != -1:
                    querySt += " and  cardId = " + str(pref.cardId)
                if pref.merchantId != -1:
                    querySt += " and  merchant_id = " + str(pref.merchantId)
                print querySt
                res = ConsumerTxn.objects.raw(querySt, translations=name_map)
                total = 0
                for x in res:
                    total = x.total
                if total == None:
                    total = 0
                print total
                # check if aggregate exists for this pref
                print str(consumerId) + str(pref.cardId) + pref.periodKey +" "+pref.categoryKey +" "+ pref.txType +" "+ str(pref.merchantId)
                try:
                    consumerAgg = ConsumerAgg.objects.get(consumerId=consumerId,
                                cardId = pref.cardId, periodKey=pref.periodKey,
                                categoryKey=pref.categoryKey, txType = pref.txType,
                                merchantId = pref.merchantId
                                )
                    print "Got consumer agg "+ str(total)
                except ConsumerAgg.DoesNotExist:
                    consumerAgg.periodKey = pref.periodKey
                    consumerAgg.categoryKey = pref.categoryKey
                    consumerAgg.txType = pref.txType
                    consumerAgg.cardId = pref.cardId
                    consumerAgg.merchantId = pref.merchantId
                    consumerAgg.consumerId = pref.consumerId
                    consumerAgg.created = currTimeMillis
                consumerAgg.amtSpentSS = total
                consumerAgg.updated = currTimeMillis
                consumerAgg.save()

        cacheService.setConsumerAggs(consumerId)
        #fix balance now
        if not recentTxn is None:
            if recentTxn.ssApproval == ssConst.APPROVAL_TYPES[0][0]:
                card = ConsumerCard.objects.get(id=recentTxn.cardId)
                card.amtSpentSS = card.amtSpentSS + recentAmount
                card.currOS = card.currOS + recentAmount
                card.avaialbleLimit = card.limit - card.currOS
                card.updated = currTimeMillis
                card.save()
                cacheService.setCard(card.id)

    def manageTags(self, txnId, selected, newOne):
        millis = SSUtil.getMillis()
        txn = ConsumerTxn.objects.get(id=txnId)
        if not selected is None:
            txnTags = TxnTag.objects.all().filter(consumerTxn_id = txnId)
            for txnTag in txnTags:
                if not SSUtil.isIdinList(selected,txnTag.consumerTag_id):
                   self.removeTag(txnId, txnTag.consumerTag_id)
                else:
                    selected = SSUtil.removeIdFromList(selected,txnTag.consumerTag_id)
            # Now check what remains, and tag to them
            if not selected is None and selected != '':
                lst = selected.split(",")
                for tagId in lst:
                    txnTag = TxnTag()
                    txnTag.cardId=txn.cardId
                    txnTag.consumerTag_id = tagId
                    txnTag.consumerTxn_id = txnId
                    txnTag.created = millis
                    txnTag.updated = millis
                    txnTag.save()
        else: #Remove all
            txnTags = TxnTag.objects.filter(consumerTxn_id = txnId)
            for txnTag in txnTags:
                self.removeTag(txnId, txnTag.consumerTag_id)
        #Create new one if sent
        if not newOne is None and newOne !='':
            consumerTag = self.addTag(txnId, newOne)

    def addTag(self, txnId, tag):
        #first check if consumer has that tag
        consumerTag = None
        millis = SSUtil.getMillis()
        txn = ConsumerTxn.objects.get(id=txnId)
        try:
            consumerTag = ConsumerTag.objects.get(consumerId=txn.consumerId, tag=tag)
        except ConsumerTag.DoesNotExist:
            consumerTag = ConsumerTag()
            consumerTag.consumerId = txn.consumerId
            consumerTag.tag = tag
            consumerTag.created = millis
            consumerTag.updated = millis
            consumerTag.save()
        ## Now make mapping in txnTag
        try:
            txnTag = TxnTag.objects.get(cardId=txn.cardId,
                                        consumerTag_id = consumerTag.id,
                                        consumerTxn_id = txnId)
        except TxnTag.DoesNotExist:
            txnTag = TxnTag()
            txnTag.cardId=txn.cardId
            txnTag.consumerTag_id = consumerTag.id
            txnTag.consumerTxn_id = txnId
            txnTag.created = millis
            txnTag.updated = millis
            txnTag.save()
        txn = ConsumerTxn.objects.get(id=txnId)
        searchServ = SearchService()
        txnSerializer = ConsumerTxnSerializer(txn, many=False)
        searchServ.upload("txn",txn.id, txnSerializer.data);
        return consumerTag


    def removeTag(self, txnId, tagId):
        #first check if consumer has that tag
        consumerTag = None
        millis = SSUtil.getMillis()
        txn = ConsumerTxn.objects.get(id=txnId)
        ## Now make mapping in txnTag
        try:
            txnTag = TxnTag.objects.get(cardId=txn.cardId,
                                        consumerTag_id = tagId,
                                        consumerTxn_id = txnId)
            txnTag.delete()
        except TxnTag.DoesNotExist:
            pass

        return True

