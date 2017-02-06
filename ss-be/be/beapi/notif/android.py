import time
import urllib,urllib2
import json
from _ctypes import Array
from beapi.common.ssUtil import SSUtil
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from beapi.common.jsonResponse import JSONResponse
@api_view(['GET'])
def test(request):
        a = Android()
        id = "APA91bF4iIj3uhEoJGpX11KjZTjtZ0Uw1NDvF_cGJnizYCSTpaNsRJ2QR7i4nsVE_Qlu7kDLDOW4GYJm1ILUgvALL4xQjl7Osg4bcVxeu0GSmpQ4gIuiIKPc1-2FkkVKRIqlC9rywNtuNIwapnxY3ebi1l7wu4DjcQ"
        a.send(id, "test","xys",'Approve',1)
        return Response(SSUtil.success(1),
                            status=status.HTTP_200_OK)
class Android:
    def getGCMUrl(self):
        return "https://android.googleapis.com/gcm/send"
    def getGCMAccessKey(self):
        return "AIzaSyC5myLtS_v2PZANX_15KnYSz0YWaoZnyJM"
    def getTimestampForMsg(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(SSUtil.getMillis()/1000))
    def sendToGCM(self,registrationId, data):
        payload = dict(registration_ids=[registrationId], data=data)
        print payload
        request = urllib2.Request(url=self.getGCMUrl(), data=json.dumps(payload))
        request.add_header('Authorization','key='+self.getGCMAccessKey())
        request.add_header('Content-Type', 'application/json')
        res = urllib2.urlopen(request)
        responseAsString = res.read()
        print "aft 2-"+responseAsString


    def sendTxnNotification(self, registrationId, msg, title, type, txnId, cardId, approvalType, screenMessage):
        sound = 1
        if approvalType=='Approve':
            sound=0
        data = dict(
            message = msg,
            title = title,
            subtitle = 'Time - '+str(self.getTimestampForMsg()),
            tickerText = 'Ticker',
            vibrate = 1,
            sound = sound,
            largeIcon = 'large_icon',
            smallIcon ='small_icon',
            type = type,
            txnId = txnId,
            cardId = cardId,
            url = 'http://ec2-34-198-167-207.compute-1.amazonaws.com/beapi/consumer/txn/'+str(txnId)+'/approval',
            screenMessage = screenMessage
            )
        self.sendToGCM(registrationId, data)


    def sendMerchantResponse(self, registrationId, msg, title, type, offerId, merchantId):
        data = dict(
            message = msg,
            title = title,
            subtitle = 'Time - '+str(self.getTimestampForMsg()),
            tickerText = 'Ticker',
            vibrate = 1,
            sound = 0,
            largeIcon = 'large_icon',
            smallIcon ='small_icon',
            type = type,
            offerId = offerId,
            merchantId = merchantId
            )
        if offerId is None:
            data.pop('offerId')
        self.sendToGCM(registrationId, data)

    def sendOfferNotification(self, registrationId, msg, title, type, offerId, merchantId):
        data = dict(
            message = msg,
            title = title,
            subtitle = 'Time - '+str(self.getTimestampForMsg()),
            tickerText = 'Ticker',
            vibrate = 1,
            sound = 0,
            largeIcon = 'large_icon',
            smallIcon ='small_icon',
            type = type,
            offerId = offerId,
            merchantId = merchantId
            )
        self.sendToGCM(registrationId, data)