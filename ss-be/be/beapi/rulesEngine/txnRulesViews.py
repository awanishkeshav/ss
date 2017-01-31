import json
from json import JSONEncoder

from django.core import serializers

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import authentication_classes


from beapi.common.jsonResponse import JSONResponse
from beapi.common.auth import SSClientAuth
from beapi.exception.ssException import SSException
from beapi.common.ssUtil import SSUtil
from beapi.common.constants import SSConst
from beapi.consumerCard.txnService import TxnService
from beapi.rulesEngine.txnValidatorService import TxnValidatorService
from beapi.async.tasks import asyncRecordTransaction

@api_view(['POST'])
@authentication_classes((SSClientAuth,))
def processTxn(request):
    data = json.loads(request.body)
    print data
    try:
        validate(data)
    except Exception as e:
        return JSONResponse(SSUtil.err(e.message),
                            status=status.HTTP_412_PRECONDITION_FAILED)
    tvServ = TxnValidatorService()
    txnApprovalVO = tvServ.getApproval(data['cardNum'], data['amount'],
                            data['merchantUuid'], data['merchantName'],
                            data['txType'], data['mccCode'])
    delayed = True
    millisStart = SSUtil.getMillis()
    if delayed:
        asyncRecordTransaction.delay(data['cardNum'], data['amount'],
                            data['merchantUuid'], data['merchantName'],
                            data['txType'], data['mccCode'], txnApprovalVO, request.user)
    else:
        asyncRecordTransaction(data['cardNum'], data['amount'],
                            data['merchantUuid'], data['merchantName'],
                            data['txType'], data['mccCode'], txnApprovalVO, request.user)
    millisEnd = SSUtil.getMillis()
    timeTaken = millisEnd - millisStart
    res={ "flag":txnApprovalVO.immediateApproval,
           "msg":txnApprovalVO.remarks,
           "time":timeTaken
        }
    return JSONResponse(SSUtil.success(res), status=status.HTTP_200_OK)

def validate(data):
    if 'cardNum' not in data or data['cardNum'] is None:
        raise Exception(SSException.CARD_NUM_MISSING)
    elif 'txType' not in data or data['txType'] is None:
        raise Exception(SSException.TXN_TYPE_MISSING)
    elif 'merchantUuid' not in data or data['merchantUuid'] is None:
        raise Exception(SSException.MERCHANT_ID_MISSING)
    elif 'mccCode' not in data or data['mccCode'] is None:
        raise Exception(SSException.MCC_CODE_MISSING)
    elif 'amount' not in data or data['amount'] is None:
        raise Exception(SSException.AMOUNT_MISSING)
    ssConst = SSConst()
    if not ssConst.isValidTxType(data['txType']):
        raise Exception(SSException.INVALID_TXN_TYPE)

