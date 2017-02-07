from rest_framework import generics
from beapi.models import MerchantOffer
from beapi.models import ConsumerMerchant
from beapi.models import Merchant
from beapi.models import MerchantOfferTargetting
from beapi.models import ConsumerTxn
from beapi.models import ReviewTemplate
from beapi.models import TxnReview
from beapi.constantModels import TxnCategory
from beapi.models import ConsumerDevice
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from _ctypes import Array
from beapi.common.constants import SSConst
from beapi.common.cacheService import CacheService
from beapi.serializers import TxnReviewSerializer
from beapi.notif.android import Android
from django.db.models import Q
from beapi.models import ConsumerOffer

class MerchantService:

    def getMerchants(self):
        return Merchant.objects.all().order_by('updated')

    def getOffers(self, merchantId, status):
        try:
            ssConst = SSConst()
            if status is None:
                offers = MerchantOffer.objects \
                                      .all() \
                                      .order_by('status','-updated') \
                                      .filter(~Q(status = ssConst.OFFER_STATUSES[2][0]),
                                       merchant_id=merchantId)
                print str(offers.query)
            else:
                offers = MerchantOffer.objects.all().order_by('status','-updated').filter(merchant_id=merchantId, status=status)
            return offers
        except MerchantOffer.DoesNotExist:
            return []

    def getOffer(self, offerId):
        try:
            return MerchantOffer.objects.get(id=offerId)
        except MerchantOffer.DoesNotExist:
            return None

    def getAllOffers(self, status):
        currTimeMillis = SSUtil.getMillis()
        try:
            offers = MerchantOffer.objects.all().order_by('status','-updated').filter(endDate__gt=currTimeMillis, status=status)
            return offers
        except MerchantOffer.DoesNotExist:
            return Array()

    def getAllOffersNearMe(self, consumerId, status):
        currTimeMillis = SSUtil.getMillis()
        try:
            cms = ConsumerMerchant.objects.all().filter(consumerId=consumerId, currentDistance__lt=50)
            merchants = ConsumerMerchant.objects.all().filter(consumerId=consumerId, currentDistance__lt=50).values_list("merchant_id", flat = True)
            print "merchants are "+str(merchants.query)
            offers = MerchantOffer.objects.all().order_by('status','-updated').filter(status=status,merchant_id__in = merchants)
            print "offers are "+str(offers.query)
            for offer in offers:
                for cm in cms:
                    if offer.merchant_id == cm.merchant_id:
                        offer.distance = cm.currentDistance
            return offers
        except MerchantOffer.DoesNotExist:
            return Array()


    def addConsumerRelation(self, merchantId, consumerId):
        currTimeMillis = SSUtil.getMillis()
        try:
            cm = ConsumerMerchant.objects.get(merchant_id=merchantId, consumerId=consumerId)
        except ConsumerMerchant.DoesNotExist:
            cm = ConsumerMerchant()
            cm.created = currTimeMillis
            cm.updated = currTimeMillis
            cm.consumerId = consumerId
            cm.merchant_id = merchantId
            cm.status = 1
            cm.currentDistance = 100
            cm.save()


    def addConsumerRelationWithAllMerchants(self, consumerId):
        mLst = Merchant.objects.all().filter(status=1)
        for m in mLst:
            self.addConsumerRelation(m.id, consumerId)

    def toggleStatus(self, merchantId, consumerId, statusFlag):
        currTimeMillis = SSUtil.getMillis()
        try:
            cm = ConsumerMerchant.objects.get(merchant_id=merchantId, consumerId=consumerId)
        except ConsumerMerchant.DoesNotExist:
            cm = ConsumerMerchant()
            cm.created = currTimeMillis
            cm.consumerId = consumerId
            cm.merchant_id = merchantId
            cm.currentDistance = 100
        cm.status = statusFlag
        cm.updated = currTimeMillis
        cm.save()


    def getBlockedMerchants(self,consumerId):
        currTimeMillis = SSUtil.getMillis()
        try:
            return ConsumerMerchant.objects.all().filter(consumerId=consumerId, status=0)
        except ConsumerMerchant.DoesNotExist:
            return Array()

    def getReviewTemplate(self,merchantId):
        try:
            return ReviewTemplate.objects.get(merchant_id=merchantId)
        except ReviewTemplate.DoesNotExist:
            return None

    def saveReview(self, txnId, criteria1Value, criteria2Value, criteria3Value, comment):
        millis = SSUtil.getMillis()
        ssConst = SSConst()
        consumerTxn = ConsumerTxn.objects.get(id=txnId)
        reviewTemplate = None

        try:
            reviewTemplate = ReviewTemplate.objects.get(merchant_id=consumerTxn.merchant_id)
        except reviewTemplate.DoesNotExist:
            raise Exception(SSException.NO_REVIEW_TEMPLATE)
        txnReview = TxnReview()
        try:
            txnReview = TxnReview.objects.get(txnId=txnId)
        except TxnReview.DoesNotExist:
            txnReview = TxnReview()
            txnReview.txnId = txnId
            txnReview.merchant_id = consumerTxn.merchant_id
            txnReview.criteria1 = reviewTemplate.criteria1
            txnReview.criteria2 = reviewTemplate.criteria2
            txnReview.criteria3 = reviewTemplate.criteria3
            txnReview.created = millis
            if comment is None:
                comment = 'No comments provided.'
        txnReview.criteria1Value =  criteria1Value
        txnReview.criteria2Value =  criteria2Value
        txnReview.criteria3Value =  criteria3Value
        txnReview.updated = millis
        if not comment is None:
            txnReview.comment = comment
        txnReview.save()
        consumerTxn.review = round((criteria1Value+criteria2Value+criteria3Value)/3.0)
        consumerTxn.reviewStatus = ssConst.TXN_REVIEW_STATUSES[2][0]
        consumerTxn.save()
        return consumerTxn

    def saveReviewTemplate(self, merchantId, criteria1Value, criteria2Value, criteria3Value):
        millis = SSUtil.getMillis()
        reviewTemplate = None
        try:
            reviewTemplate = ReviewTemplate.objects.get(merchant_id=merchantId)
        except reviewTemplate.DoesNotExist:
            reviewTemplate = ReviewTemplate()
            reviewTemplate.version=0
            reviewTemplate.commentRequired=1
            reviewTemplate.created = millis
        reviewTemplate.merchant_id = merchantId
        reviewTemplate.criteria1 = criteria1Value
        reviewTemplate.criteria2 = criteria2Value
        reviewTemplate.criteria3 = criteria3Value
        reviewTemplate.version = reviewTemplate.version + 1
        reviewTemplate.updated = millis
        reviewTemplate.save()
        return reviewTemplate

    def getReview(self,txnId):
        try:
            return TxnReview.objects.get(txnId=txnId)
        except ReviewTemplate.DoesNotExist:
            return None


    def getReviewSummary(self,merchantId, fromDate):
        try:
             reviewSummaryMap = {'pk': 'id',
                     'total': 'total',
                    'average':'average'}
             reviewSummary =  TxnReview.objects.raw(
                                    '''
                                    select 1 as id, count(*) as total,
                                    round((avg(criteria1Value)+avg(criteria2Value)+avg(criteria3Value))/3) as average
                                    from ss_txn_review where merchant_id=%s and created > %s
                                    ''',[merchantId, fromDate], translations=reviewSummaryMap)
             reviewSum = {
                            'total':0,
                            'average':0
                          }
             for x in reviewSummary:
                    reviewSum['total'] = x.total
                    reviewSum['average']=x.average
             return reviewSum
        except TxnReview.DoesNotExist:
            return None

    def saveLocation(self, merchantId, lat, lng):
        merchant = Merchant.objects.get(id=merchantId)
        merchant.lat = lat
        merchant.lng = lng
#         merchant.save()

    def createMerchant(self, merchantUuid, merchantName, accessCode, deviceRegistrationId, mccCode):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        merchant = Merchant()
        if merchantName is None:
            merchantName = ''
        merchant.name = merchantName
        merchant.uuid = merchantUuid
        merchant.phone = ssConst.MERCHANT_DEFAULT_CONTACT_NUM
        merchant.address = ssConst.MERCHANT_DEFAULT_ADDRESS
        merchant.reviewStatus = ssConst.TXN_REVIEW_STATUSES[0][0]
        merchant.status = 1
        merchant.created = currTimeMillis
        merchant.updated = currTimeMillis
        merchant.installed=1
        merchant.mccCode = mccCode
        if not accessCode is None:
            merchant.accessCode = accessCode
        if not deviceRegistrationId is None:
            merchant.deviceRegistrationId = deviceRegistrationId
            merchant.deviceType = 1
            merchant.deviceSubType = 1
        merchant.save()

        reviewTemplate = ReviewTemplate()
        reviewTemplate.criteria1 = "Overall Rating"
        reviewTemplate.merchant_id = merchant.id
        reviewTemplate.commentRequired = 1
        reviewTemplate.version = 1
        reviewTemplate.created = currTimeMillis
        reviewTemplate.updated = currTimeMillis
        reviewTemplate.save()

        return merchant


    def registerMerchant(self, merchantUuid, accessCode):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        merchant = None
        try:
            merchant = Merchant.objects.get(uuid=merchantUuid,
                                            accessCode=accessCode)
            if merchant is None:
                raise Exception("Invalid combination of ID and Access Code")
            elif merchant.installed is 0:
                merchant.installed=1
                merchant.save()
            else:
                pass
        except Merchant.DoesNotExist:
            raise Exception("Invalid combination of ID and Access Code")
        return merchant

    def updateMerchant(self, merchantId, name, description, businessHours):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        merchant = None
        try:
            merchant = Merchant.objects.get(id=merchantId)
            if not name is None:
                merchant.name = name
            if not description is None:
                merchant.description = description
            if not businessHours is None:
                merchant.businessHours = businessHours
            merchant.uodated = currTimeMillis
            merchant.save()
        except Merchant.DoesNotExist:
            raise Exception("Invalid merchant")
        return merchant

    def getTxnAggSummary(self,merchantId, durationKey):
        try:
            ssConst = SSConst()
            txnAggSummaryMap = {'pk': 'id',
                     'visits': 'visits',
                    'spend':'spend',
                    'reviews':'reviews',
                    'reviewsAverage':'reviewsAverage',}


            txnAggSummary =  ConsumerTxn.objects.raw(
                                    '''
                                    select 1 as id, count(*) as total, sum(amtSpentSS) as spend
                                    from ss_consumer_txn where merchant_id=%s
                                    and created > %s and ssApproval='Approve'
                                    ''',[merchantId, ssConst.getStartTime(durationKey)], translations=txnAggSummaryMap)
            txnAggSum = {
                            'visits':0,
                            'spend':0,
                            'reviews':0,
                            'reviewsAverage':0,
                          }
            for x in txnAggSummary:
                    txnAggSum['visits'] = x.total
                    txnAggSum['spend']=x.spend
            reviewSum = self.getReviewSummary(merchantId,
                                              ssConst.getStartTime(durationKey))
            txnAggSum['reviews'] = reviewSum['total']
            txnAggSum['reviewsAverage'] = reviewSum['average']
            return txnAggSum
        except TxnReview.DoesNotExist:
            return None

    def getMerchantReviews(self, merchantId, fromDate, limit, start):
        res = None
        try:
            res =  TxnReview.objects.all().order_by('-updated').filter(merchant_id=merchantId, created__gt=fromDate)[start:(start+limit)]
        except:
            res = Array()
        return res

    def getReviewDtl(self, reviewId):
        res = {
                "review": None,
                "visits": None,
                "spend": None,
                "averageRating": None
               }
        txnReview = None
        try:
            txnReview = TxnReview.objects.get(id=reviewId)
        except:
            return None
        txn = None
        try:
            txn = ConsumerTxn.objects.get(id=txnReview.txnId)
            summary = self.getConsumerMerchantSummary(txn.merchant_id, txn.consumerId)
            averages = self.getReviewSummary(txn.merchant_id, 0) #all the txns
            res["review"] = TxnReviewSerializer(txnReview).data
            res["visits"] = summary["visits"]
            res["spend"] = summary["spend"]
            res["averageRating"] = averages["average"]
            return res
        except:
            return None

    def getConsumerMerchantSummary(self,merchantId, consumerId):
        try:
            ssConst = SSConst()
            consumerMerchantSummaryMap = {'pk': 'id',
                     'visits': 'visits',
                    'spend':'spend', }


            consumerMerchantSummary =  ConsumerTxn.objects.raw(
                                    '''
                                    select 1 as id, count(*) as total, sum(amtSpentSS) as spend
                                    from ss_consumer_txn where merchant_id=%s
                                    and consumerId = %s and ssApproval='Approve'
                                    ''',[merchantId, consumerId], translations=consumerMerchantSummaryMap)
            consumerMerchantSum = {
                            'visits':0,
                            'spend':0
                          }
            for x in consumerMerchantSummary:
                    consumerMerchantSum['visits'] = x.total
                    consumerMerchantSum['spend']=x.spend
            return consumerMerchantSum
        except ConsumerTxn.DoesNotExist:
            return None

    def saveReviewResponse(self, reviewId, merchantComment, offerId):
        try:
            txnReview = TxnReview.objects.get(id=reviewId)
            txnReview.response = merchantComment
            if not offerId is None:
                txnReview.offerId = offerId
            txnReview.save()
            # Send notification to consumer
            try:
                ssConst = SSConst()
                txn = ConsumerTxn.objects.get(id=txnReview.txnId)
                consumerDevice = ConsumerDevice.objects.get(consumerId=txn.consumerId)
                android = Android()
                merchant = Merchant.objects.get(id=txnReview.merchant_id)
                offer =  None
                if not offerId is None:
                    offer = MerchantOffer.objects.get(id=offerId)
                android.sendMerchantResponse(consumerDevice.deviceRegistrationId,
                        merchantComment, "Response from "+merchant.name,
                        ssConst.DEVICE_NOTIFICATION_TYPES["Offer"],
                         offerId, txnReview.merchant_id)
            except Exception as e:
                print e.message
                pass

            return txnReview
        except:
            return False

    def addOffer(self, merchantId, title, description, code, codeType, endDate,categoryId, imgUrl):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        merchantOffer = MerchantOffer()
        merchantOffer.title = title
        merchantOffer.description = description
        if not endDate is None:
            merchantOffer.endDate = int(endDate)
        merchantOffer.startDate = currTimeMillis
        merchantOffer.codeType = codeType
        merchantOffer.code = code
        merchantOffer.merchant_id = merchantId
        if categoryId is None:
            merchant = Merchant.objects.get(id=merchantId)
            category = TxnCategory.objects.get(mccCode = merchant.mccCode)
            categoryId = category.id
        merchantOffer.category_id = categoryId
        merchantOffer.status = ssConst.OFFER_STATUSES[0][0]
        merchantOffer.imgUrl = imgUrl
        merchantOffer.created = currTimeMillis
        merchantOffer.updated = currTimeMillis
        merchantOffer.save()
        return merchantOffer

    def updateOffer(self, offerId, title, description, code, codeType, endDate):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        merchantOffer = None
        try:
            merchantOffer = MerchantOffer.objects.get(id=offerId)
        except:
            msg = "Offer does not exist for id "+offerId
            raise Exception(msg)
        merchantOffer.title = title
        merchantOffer.description = description
        merchantOffer.endDate = endDate
        merchantOffer.codeType = codeType
        merchantOffer.code = code
        merchantOffer.updated = currTimeMillis
        merchantOffer.save()
        return merchantOffer


    def markOfferStatus(self, offerId,status):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        merchantOffer = None
        try:
            merchantOffer = MerchantOffer.objects.get(id=offerId)
        except:
            msg = "Offer does not exist for id "+offerId
            raise Exception(msg)
        merchantOffer.status = status
        merchantOffer.updated = currTimeMillis
        merchantOffer.save()
        # if status is archived or suspended then mark them so
        # in consumer offer
        if status != ssConst.OFFER_STATUSES[0][0]:
            ConsumerOffer.objects\
                         .filter(offer_id=offerId)\
                         .update(status=ssConst.CONSUMER_OFFER_STATUSES[2][0])
        return merchantOffer

    def getOfferTargettingList(self, offerId):
        res = []
        try:
            res = MerchantOfferTargetting.objects.order_by('-updated').filter(offer_id=offerId)
        except Exception as e:
            print e.message
        return res

    def addOfferTargetting(self, offerId, targetType, minVisits, minTotalSpend):
        currTimeMillis = SSUtil.getMillis()
        ssConst = SSConst()
        merchantOfferTargetting = None
        mot = MerchantOfferTargetting()
        mot.offer_id = offerId
        mot.targetType = targetType
        mot.minVisits = minVisits
        mot.minTotalSpend = minTotalSpend
        mot.created = currTimeMillis
        mot.updated = currTimeMillis
        mot.save()
        return mot

    def getOfferTargetting(self, targettingId):
        res = None
        try:
            res = MerchantOfferTargetting.objects.get(id=targettingId)
        except:
            pass
        return res

    def updateOfferTargetting(self, targettingId, targetType, minVisits, minTotalSpend):
        currTimeMillis = SSUtil.getMillis()
        mot = None
        try:
            mot = MerchantOfferTargetting.objects.get(id=targettingId)
        except:
            return mot
        mot.targetType = targetType
        mot.minVisits = minVisits
        mot.minTotalSpend = minTotalSpend
        mot.updated = currTimeMillis
        mot.save()
        return mot

    def deleteOfferTargetting(self, targettingId):
        res = True
        try:
            obj = MerchantOfferTargetting.objects.get(id=targettingId)
            obj.delete()
        except Exception as e:
            print e.message
            res = False
        return res


