import json
from json import JSONEncoder

from django.core import serializers

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import list_route
from rest_framework.views import APIView
from rest_framework.response import Response

from beapi.common.jsonResponse import JSONResponse
from beapi.common.auth import SSAuth
from beapi.common.auth import SSMerchantAuth
from beapi.serializers import MerchantOfferSerializer
from beapi.serializers import MerchantSerializer
from beapi.serializers import MerchantOfferTargettingSerializer
from beapi.serializers import MerchantSerializer
from beapi.serializers import ReviewTemplateSerializer
from beapi.serializers import ConsumerOfferSerializer
from beapi.serializers import TxnReviewSerializer
from beapi.merchant.merchantService import MerchantService
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.common.constants import SSConst
from beapi.merchant.offersService import OffersService
from beapi.models import ConsumerOffer



@api_view(['GET'])
def getMerchants(request):
    ms = MerchantService();
    serializer = MerchantSerializer(ms.getMerchants(), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getOffers(request, merchantId):
    ssConst = SSConst()
    offerServ = OffersService();
    serializer = ConsumerOfferSerializer(offerServ.getConsumerOffersByMerchant(request.user.id, merchantId), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SSMerchantAuth,))
def getMerchantOffers(request):
    ms = MerchantService();
    st = None
    if 'status' in request.GET and not request.GET['status'] is None  and request.GET['status'] != '':
        st = request.GET['status']
    serializer = MerchantOfferSerializer(ms.getOffers(request.user.id, st), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getOffer(request, offerId):
    print "Here"
    ms = MerchantService();
    try:
        serializer = MerchantOfferSerializer(ms.getOffer(offerId), many=False)
        return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.INVALID_INPUT), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getAllOffers(request):
    ssConst = SSConst()
    st = ssConst.OFFER_STATUSES[0][0]
    ms = MerchantService();
    serializer = MerchantOfferSerializer(ms.getAllOffers(st), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getOffersByDemand(request, merchantId):
    ssConst = SSConst()
    offerServ = OffersService();
    serializer = ConsumerOfferSerializer(offerServ.getOnDemandConsumerOffersByMerchant(request.user.id, merchantId), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SSAuth,))
def getConsumerOffers(request):
    ssConst = SSConst()
    offerServ = OffersService();
    serializer = ConsumerOfferSerializer(offerServ.getConsumerOffers(request.user.id), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getNewOffersCnt(request):
    ssConst = SSConst()
    offerServ = OffersService();
    cnt = offerServ.countNewOffers(request.user.id)
    print "cnt is " +str(cnt)
    return JSONResponse(SSUtil.success(cnt), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SSAuth,))
def getAllOffersNearMe(request):
    ms = MerchantService();
    ssConst = SSConst()
    serializer = MerchantOfferSerializer(ms.getAllOffersNearMe(request.user.id, ssConst.OFFER_STATUSES[0][0]), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getReviewTemplate(request, merchantId):
    try:
        ms = MerchantService();
        serializer = ReviewTemplateSerializer(ms.getReviewTemplate(merchantId), many=False)
        return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                                status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT'])
@authentication_classes((SSMerchantAuth,))
def reviewTemplate(request):
    if request.method == 'GET':
        try:
            ms = MerchantService();
            serializer = ReviewTemplateSerializer(ms.getReviewTemplate(request.user.id), many=False)
            return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                                    status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if not 'criteria1' in data or data['criteria1'] is None:
            return JSONResponse(SSUtil.err("Criteria1  is required"),
                                status=status.HTTP_412_PRECONDITION_FAILED)
        if not 'criteria2' in data or data['criteria2'] is None:
            return JSONResponse(SSUtil.err("Criteria2  is required"),
                                status=status.HTTP_412_PRECONDITION_FAILED)
        if not 'criteria3' in data or data['criteria3'] is None:
            return JSONResponse(SSUtil.err("Criteria3  is required"),
                                status=status.HTTP_412_PRECONDITION_FAILED)
        try:
            ms = MerchantService();
            res = ReviewTemplateSerializer(ms.saveReviewTemplate(request.user.id,
                        data['criteria1'], data['criteria2'], data['criteria3']),many=False)
            return JSONResponse(SSUtil.success(res.data), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes((SSAuth,))
def review(request, txnId):
    if request.method == 'GET':
        try:
            ms = MerchantService();
            serializer = TxnReviewSerializer(ms.getReview(txnId), many=False)
            return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err("No reviews available"),
                                    status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            comment=None
            ms = MerchantService();
            data = json.loads(request.body)
            if not 'criteria1' in data or data['criteria1'] is None:
                return JSONResponse(SSUtil.err("Criteria1 is required"),
                                    status=status.HTTP_412_PRECONDITION_FAILED)
            if not 'criteria2' in data or data['criteria2'] is None:
                return JSONResponse(SSUtil.err("Criteria2 is required"),
                                    status=status.HTTP_412_PRECONDITION_FAILED)
            if not 'criteria3' in data or data['criteria3'] is None:
                return JSONResponse(SSUtil.err("Criteria3 is required"))
            if not 'comment' in data or data['comment'] is None:
                comment=None
            else:
                comment = data['comment']
            try:
                consumerTxn = ms.saveReview(txnId, data['criteria1'], data['criteria2'], data['criteria3'], comment)
                offersServ = OffersService()
                ssConst = SSConst()
                offersServ.processOfferNotification(consumerTxn.id, ssConst.OFFER_TARGET_TYPES[2][0], None)
                return JSONResponse(SSUtil.success(True), status=status.HTTP_200_OK)
            except:
                return JSONResponse(SSUtil.err(SSException.NO_REVIEW_TEMPLATE), status=status.HTTP_400_BAD_REQUEST)
        except:
            return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                                status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def reviews(request, merchantId):
    try:
        ms = MerchantService();
        ssConst = SSConst()
        data = ms.getReviewSummary(merchantId, ssConst.getStartTime("all_time"))
        return JSONResponse(SSUtil.success(data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err("No reviews available"),
                                status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes((SSMerchantAuth,))
def saveLocation(request):
    data = json.loads(request.body)
    if not 'lat' in data or data['lat'] is None:
        return JSONResponse(SSUtil.err("Latitude  is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    if not 'lng' in data or data['lng'] is None:
        return JSONResponse(SSUtil.err("Longitude  is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        ms = MerchantService()
        s = ms.saveLocation(request.user.id,   data['lat'],
                        data['lng'])
        return JSONResponse(SSUtil.success(True), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def register(request, format=None):
    data = json.loads(request.body)
    if not 'uuid' in data or data['uuid'] is None:
        return JSONResponse(SSUtil.err("Merchant Id is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    if not 'accessCode' in data or data['accessCode'] is None:
        return JSONResponse(SSUtil.err("Access Code is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        ms = MerchantService();
        merchant = ms.registerMerchant(data['uuid'], data['accessCode'])
        ser = MerchantSerializer(merchant)
        return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(SSUtil.err(e.message), status=status.HTTP_409_CONFLICT)

@api_view(['GET', 'PUT'])
@authentication_classes((SSMerchantAuth,))
def merchant(request, format=None):
    if request.method == 'GET':
        try:
            ser = MerchantSerializer(request.user)
            return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(SSUtil.err(e.message), status=status.HTTP_409_CONFLICT)
    elif  request.method == 'PUT':
        try:
            data = json.loads(request.body)
            name = None
            description = None
            businessHours = None
            if 'name' in data and not data['name'] is None:
               name = data['name']
            if 'description' in data and not data['description'] is None:
               description = data['description']
            if 'businessHours' in data and not data['businessHours'] is None:
               businessHours = data['businessHours']
            ms = MerchantService()
            merchant = ms.updateMerchant(request.user.id, name, description, businessHours)
            ser = MerchantSerializer(merchant)
            return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(SSUtil.err(e.message), status=status.HTTP_409_CONFLICT)

@api_view(['GET'])
@authentication_classes((SSMerchantAuth,))
def getTxnAggSummary(request, format=None):
    if 'duration' not in request.GET or request.GET["duration"] is None or request.GET["duration"] == '':
        return JSONResponse(SSUtil.err("Duration is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        ms = MerchantService();
        data = ms.getTxnAggSummary(request.user.id, request.GET['duration'])
        return JSONResponse(SSUtil.success(data), status=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(SSUtil.err(e.message), status=status.HTTP_409_CONFLICT)


@api_view(['GET'])
@authentication_classes((SSMerchantAuth,))
def getReviews(request):
    limit = 100
    start = 0
    duration = "all_time"
    if 'duration' in request.GET and not request.GET["duration"] is None and request.GET["duration"] != '':
        duration = request.GET["duration"]
    if 'limit' in request.GET and not request.GET["limit"] is None and request.GET["limit"] != '':
        limit = int(request.GET["limit"])
    if 'start' in request.GET and not request.GET["start"] is None and request.GET["start"] != '':
        start = int(request.GET["start"])
    try:
        ms = MerchantService();
        ssConst = SSConst()
        res = ms.getMerchantReviews(request.user.id, ssConst.getStartTime(duration), limit, start)
        serializer = TxnReviewSerializer(res, many=True)
        return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err("No reviews available"),
                                status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes((SSMerchantAuth,))
def getReviewDtl(request, reviewId):
    try:
        ms = MerchantService();
        res = ms.getReviewDtl(reviewId)
        return JSONResponse(SSUtil.success(res), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err("Invalid data"),
                                status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes((SSMerchantAuth,))
def saveReviewResponse(request, reviewId):
    data = json.loads(request.body)
    if not 'merchantComment' in data or data['merchantComment'] is None:
        return JSONResponse(SSUtil.err("Merchant comment is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    offerId = None
    if 'offerId' in data and not data['offerId'] is None:
       offerId = data['offerId']
    try:
        ms = MerchantService();
        res = ms.saveReviewResponse(reviewId, data['merchantComment'], offerId)
        if res is None:
            return JSONResponse(SSUtil.err(False), status=status.HTTP_200_OK)
        else:
            ser = TxnReviewSerializer(res, many=False)
            return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err("Invalid data"),
                                status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
@authentication_classes((SSMerchantAuth,))
def offer(request, offerId):
    ms = MerchantService();
    if request.method == 'GET':
        try:
            serializer = MerchantOfferSerializer(ms.getOffer(offerId), many=False)
            return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.INVALID_INPUT), status=status.HTTP_400_BAD_REQUEST)
    else:
        title = None
        description = None
        endDate = None
        code = None
        codeType = "text"
        categoryId = None
        if not 'title' in request.DATA or request.DATA['title'] is None:
            return JSONResponse(SSUtil.err("Title  is required"),
                                status=status.HTTP_412_PRECONDITION_FAILED)
        else:
            title =  request.DATA['title']
        if 'description' in request.DATA and not request.DATA['description'] is None:
            description = request.DATA['description']
        if 'endDate' in request.DATA and not request.DATA['endDate'] is None:
            endDate = request.DATA['endDate']
        if 'code' in request.DATA and not request.DATA['code'] is None:
            code = request.DATA['code']
        if 'codeType' in request.DATA and not request.DATA['codeType'] is None:
            codeType = request.DATA['codeType']
        if 'categoryId' in request.DATA and not request.DATA['categoryId'] is None:
            categoryId = request.DATA['categoryId']
        try:
            ser = MerchantOfferSerializer(ms.updateOffer(offerId,title,description,
                            code,codeType,endDate))
            return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes((SSMerchantAuth,))
def addOffer(request):
    ms = MerchantService()
    title = None
    description = None
    endDate = None
    code = None
    codeType = "text"
    categoryId = None
    imgUrl =  None
    if not 'title' in request.POST or request.POST['title'] is None:
        return JSONResponse(SSUtil.err("Title  is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    else:
        title =  request.POST['title']
    if 'description' in request.POST and not request.POST['description'] is None:
        description = request.POST['description']
    if 'endDate' in request.POST and not request.POST['endDate'] is None:
        endDate = request.POST['endDate']
    if 'code' in request.POST and not request.POST['code'] is None:
        code = request.POST['code']
    if 'codeType' in request.POST and not request.POST['codeType'] is None:
        codeType = request.POST['codeType']
    if 'imgUrl' in request.FILES and not request.FILES['imgUrl'] is None:
        print "imgurl is not none"
        imgUrl = request.FILES['imgUrl']
#     try:
    ser = MerchantOfferSerializer(ms.addOffer(request.user.id,title,description,
                    code,codeType,endDate,categoryId, imgUrl))
    return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
#     except:
#         return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes((SSMerchantAuth,))
def markOfferStatus(request, offerId):
    ms = MerchantService();

    st = None
    if not 'status' in request.DATA or request.DATA['status'] is None:
        return JSONResponse(SSUtil.err("Status  is required"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    else:
        st =  request.DATA['status']
    try:
        ser = MerchantOfferSerializer(ms.markOfferStatus(offerId,st))
        return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PUT'])
@authentication_classes((SSAuth,))
def markConsumerOffersRead(request):
    offerServ = OffersService();
#     try:
    res = offerServ.markConsumerOffersRead(request.user.id)
    return JSONResponse(SSUtil.success(res), status=status.HTTP_200_OK)
#     except:
#         return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@authentication_classes((SSMerchantAuth,))
def getOfferTargettingList(request, offerId):
    ms = MerchantService();
#     try:
    serializer = MerchantOfferTargettingSerializer(ms.getOfferTargettingList(offerId), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
#     except:
#         return JSONResponse(SSUtil.err(SSException.INVALID_INPUT), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@authentication_classes((SSMerchantAuth,))
def offerTargetting(request, offerId, targettingId):
    ms = MerchantService();
    if request.method == 'GET':
        try:
            serializer = MerchantOfferTargettingSerializer(ms.getOfferTargetting(targettingId), many=False)
            return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.INVALID_INPUT), status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            flag = ms.deleteOfferTargetting(targettingId)
            if flag:
                return JSONResponse(SSUtil.success(flag), status=status.HTTP_200_OK)
            else:
                return JSONResponse(SSUtil.err(flag), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.INVALID_INPUT), status=status.HTTP_400_BAD_REQUEST)
    else:
        data = json.loads(request.body)
        targetType = None
        minVisits = 0
        minTotalSpend = 0
        if 'targetType' in data and not data['targetType'] is None:
            targetType = data['targetType']
        if 'minVisits' in data and not data['minVisits'] is None:
            minVisits = data['minVisits']
        if 'minTotalSpend' in data and not data['minTotalSpend'] is None:
            minTotalSpend = data['minTotalSpend']
        try:
            ser = MerchantOfferTargettingSerializer(ms.updateOfferTargetting(targettingId,
                            targetType, minVisits, minTotalSpend))
            return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes((SSMerchantAuth,))
def addOfferTargetting(request, offerId):
    ssConst = SSConst()
    ms = MerchantService()
    data = json.loads(request.body)
    targetType = None
    minVisits = 0
    minTotalSpend = 0
    if 'targetType' in data and not data['targetType'] is None:
        targetType = data['targetType']
    else:
        targetType = ssConst.OFFER_TARGET_TYPES[3][0]
    if 'minVisits' in data and not data['minVisits'] is None:
        minVisits = data['minVisits']
    if 'minTotalSpend' in data and not data['minTotalSpend'] is None:
        minTotalSpend = data['minTotalSpend']
    try:
        ser = MerchantOfferTargettingSerializer(ms.addOfferTargetting(offerId,targetType,
                        minVisits,minTotalSpend))
        return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def loadConsumerOffers(request):
    ofs = OffersService();
    ofs.processOffersForExistingConsumers()
    return JSONResponse(SSUtil.success(True), status=status.HTTP_200_OK)