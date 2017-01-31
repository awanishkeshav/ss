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
from beapi.serializers import ConsumerCardSerializer
from beapi.serializers import ConsumerTxnSerializer
from beapi.serializers import ConsumerTagSerializer
from beapi.customSer.customSerializers import TxnTagSummarySerializer
from beapi.serializers import ClientSerializer
from beapi.models import ConsumerCard
from beapi.models import Client
from beapi.models import ConsumerTxn
from beapi.consumerCard.cardService import CardService
from beapi.consumerCard.txnService import TxnService
from beapi.client.clientService import ClientService
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.common.constants import SSConst
from beapi.common.searchService import SearchService

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getCards(request):
    cs = CardService();
    serializer = ConsumerCardSerializer(cs.getCards(request.user.id), many=True)
    return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes((SSAuth,))
def card(request, pk):
    if request.method == 'GET':
        cs = CardService()
        ts = TxnService()
        cls = ClientService()
        try:
            card = cs.getCards(request.user.id, pk)
            txns = ts.getTxns(request.user.id, pk,0, 20,None,None)
            ccs = ConsumerCardSerializer(card, many=False)
            txs = ConsumerTxnSerializer(txns, many=True)
            cl = cls.get(card.clientId)
            client = ClientSerializer(cl, many=False)
            return Response(SSUtil.success({"card":ccs.data, "txns":txs.data,
                                           "client":client.data}),
                             status=status.HTTP_200_OK)
        except:
            return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                                status=status.HTTP_400_BAD_REQUEST)
    else:
         return JSONResponse(SSUtil.err(SSException.METHOD_NOT_APPLICABLE),
                              status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes((SSAuth,))
def registerCard(request):
    consumer = request.user
    data = json.loads(request.body)
    print data
    # TODO: Need to do it nicely
    if 'cardNum' not in data or data['cardNum'] is None:
        return JSONResponse(SSUtil.err(SSException.CARD_NUM_MISSING),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    elif 'phoneNum' not in data or data['phoneNum'] is None:
        return JSONResponse(SSUtil.err(SSException.PHONE_NUM_MISSING),
                             status=status.HTTP_412_PRECONDITION_FAILED)
    elif 'activationCode' not in data or data['activationCode'] is None:
        return JSONResponse(SSUtil.err(SSException.ACTIVATION_CODE_MISSING),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    else:
        cs = CardService()
        try:
            cc = cs.registerCard(consumer.id, data['cardNum'],
                                 data['activationCode'], data['phoneNum'])
            serializer = ConsumerCardSerializer(cc, many=False)
            return JSONResponse(SSUtil.success(serializer.data), status=status.HTTP_201_CREATED)
        except Exception as ex:
            return JSONResponse(SSUtil.err(ex.args[0]), status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getTxns(request, cardId):
    tServ = TxnService()
    try:
        try:
            start = int(request.GET['start'])
        except:
            start = 0
        try:
            limit = int(request.GET['limit'])
        except:
            limit = 25
        txns = tServ.getTxns(request.user.id, cardId,start, limit,
                             request.GET.get('tagIds'),request.GET.get('query'))
        txs = ConsumerTxnSerializer(txns, many=True)
        return Response(SSUtil.success(txs.data),
                            status=status.HTTP_200_OK)
    except:
         return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                             status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes((SSAuth,))
def getTxn(request, cardId, txnId):
    tServ = TxnService()
    try:
        txn = tServ.getTxn(request.user.id, cardId, txnId)
        txs = ConsumerTxnSerializer(txn, many=False)
        if not txn is None:
            return Response(SSUtil.success(txs.data),
                            status=status.HTTP_200_OK)
        else:
            return Response(SSUtil.err(SSException.INVALID_INPUT),
                            status=status.HTTP_200_OK)
    except:
         return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                             status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes((SSAuth,))
def getTxnMiscDetails(request, cardId, txnId):
    tServ = TxnService()
    try:
        txs = tServ.getTxnMiscDetails(request.user.id, cardId, txnId)
        if not txs is None:
            return Response(SSUtil.success(txs),
                            status=status.HTTP_200_OK)
        else:
            return Response(SSUtil.err(SSException.INVALID_INPUT),
                            status=status.HTTP_200_OK)
    except:
         return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                             status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@authentication_classes((SSAuth,))
def getTxnTaggedSummary(request, cardId):
    tServ = TxnService()
    try:
        try:
            start = int(request.GET['start'])
        except:
            start = 0
        try:
            limit = int(request.GET['limit'])
        except:
            limit = 100
        summary = tServ.getTxnTaggedSummary(request.user.id, cardId,start, limit)
        sumSer = TxnTagSummarySerializer(summary, many=True)
        return Response(SSUtil.success(sumSer.data),
                            status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                            status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes((SSAuth,))
def lockTxTypeStatus(request, cardId):
    data = json.loads(request.body)
    try:
        if data['txType'] is None:
            raise Exception()
    except Exception as e:
        return JSONResponse(SSUtil.err(e.message),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        cs = CardService()
        if data['txType'] == 'Intenational':
            data['txType'] = 'International'
        s = cs.lockTxTypeStatus(cardId, data['txType'])
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@authentication_classes((SSAuth,))
def unlockTxTypeStatus(request, cardId):
    data = json.loads(request.body)
    try:
        if data['txType'] is None:
            raise Exception()
    except Exception as e:
        return JSONResponse(SSUtil.err(e.message),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        cs = CardService()
        if data['txType'] == 'Intenational':
            data['txType'] = 'International'
        s = cs.unlockTxTypeStatus(cardId, data['txType'])
        return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@authentication_classes((SSAuth,))
def saveApproval(request, txnId):
    ssConst = SSConst()
    millis = SSUtil.getMillis()
    data = json.loads(request.body)
    try:
        if data['approval'] is None:
            raise Exception()
    except Exception as e:
        return JSONResponse(SSUtil.err(e.message),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    try:
        txn = ConsumerTxn.objects.get(pk = txnId)
        if data['approval'] == str(1):
            txn.ssApprovalStatus = ssConst.APPROVAL_STATUSES[3][0]
        else:
            txn.ssApprovalStatus = ssConst.APPROVAL_STATUSES[4][0]
        txn.updated = millis
        txn.save()
        return Response(SSUtil.success(1),
                            status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.INVALID_INPUT),
                            status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes((SSAuth,))
def addTag(request, txnId):
    data = json.loads(request.body)
    try:
        if data['tag'] is None:
            raise Exception()
    except Exception as e:
        return JSONResponse(SSUtil.err("Tag is missing"),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    print "tag is "+str(data['tag'])
    try:
        ts = TxnService()
        s = ts.addTag(txnId, data['tag'])
        ser = ConsumerTagSerializer(s,many=False)
        return JSONResponse(SSUtil.success(ser.data), status=status.HTTP_200_OK)
    except:
        return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes((SSAuth,))
def addTags(request, txnId):
    data = json.loads(request.body)
#     try:
    ts = TxnService()
    s = ts.manageTags(txnId, data['selected'], data['new'])
    return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
#     except:
#         return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@authentication_classes((SSAuth,))
def removeTag(request, txnId, tagId):
#     try:
    ts = TxnService()
    s = ts.removeTag(txnId, tagId)
    return JSONResponse(SSUtil.success(s), status=status.HTTP_200_OK)
#     except:
#         return JSONResponse(SSUtil.err(SSException.PROCESSING_FAILED),
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def searchTxns(request, cardId):
    searchServ = SearchService()
    if request.GET["q"] is None or request.GET["q"] == '':
        return JSONResponse(SSUtil.success(Array()), status=status.HTTP_200_OK)
    else:
        start = request.GET.get('start', 0)
        limit = request.GET.get('start', 10)
        res = searchServ.searchTxns(cardId, request.GET["q"], start, limit)
        return JSONResponse(SSUtil.success(res), status=status.HTTP_200_OK)
