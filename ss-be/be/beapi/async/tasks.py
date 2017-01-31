"""
Celery tasks
"""
import time
from celery import task
from decimal import Decimal
from beapi.consumerCard.txnService import TxnService
from beapi.consumer.consumerService import ConsumerService
from beapi.notif.android import Android
from beapi.common.constants import SSConst
from beapi.models import Merchant
from beapi.models import MerchantOffer
from beapi.models import MerchantOfferTargetting
from beapi.models import ConsumerMerchant
from beapi.common.cacheService import CacheService
from beapi.merchant.offersService import OffersService


@task()
def asyncRecordTransaction(cardNum, amount, merchantUuid, merchantName,
                            txType, mccCode, txnApprovalVO, client):
    ssConst = SSConst()
    txnServ = TxnService()
    offerServ = OffersService()
    print "transaction recorded "+txnApprovalVO.to_JSON()
    approvalTypeJson = ssConst.getJson(ssConst.APPROVAL_TYPES)
    txn = txnServ.recordTxn(cardNum, txType, Decimal(amount), int(mccCode), merchantUuid, merchantName, txnApprovalVO)
    merchant = Merchant.objects.get(pk = txn.merchant_id)

    print txnApprovalVO.approval+" ---- "+str(txn.cardId)

    if txnApprovalVO.sendNotif:
        screenMessage = ''
        try:
            notificationType = ssConst.DEVICE_NOTIFICATION_TYPES["Info"]
            msg = ""
            if txnApprovalVO.approval == 'Warn' or txnApprovalVO.approval == 'Approve' :
                msg = txnApprovalVO.remarks
                if merchant.reviewStatus == 'RR':
                    notificationType = ssConst.DEVICE_NOTIFICATION_TYPES["ReviewRequired"]
            elif txnApprovalVO.approval == 'Block':
               # msg = "We denied a transaction on your card for Rs. "+str(amount) +"."
               msg = txnApprovalVO.remarks
               notificationType =  ssConst.DEVICE_NOTIFICATION_TYPES["Block"]
            else:
                msg = "Approval required for "+ssConst.CURRENCY_SYMBOL+str(amount)  +" charge from "+merchant.name+"."
                notificationType =  ssConst.DEVICE_NOTIFICATION_TYPES["ApprovalRequired"]
                screenMessage = txnApprovalVO.remarks
            consumerServ = ConsumerService()
            consumerDevice = consumerServ.getConsumerDevice(txn.consumerId)
            android = Android()
            android.sendTxnNotification(consumerDevice.deviceRegistrationId,msg,
                         "Alert from "+client.name, notificationType, txn.id, txn.cardId, txnApprovalVO.approval, screenMessage)
        except Exception as e:
                print "Exception while sending communication "+e.message +" "+ssConst.APPROVAL_TYPES[0][0]

    # Aggregate Txn if it was approved
    txnServ.recalculateAgg(txn.consumerId, Decimal(amount), txn)

    # Process post_swipe_offer
    if txnApprovalVO.approval == 'Warn' or txnApprovalVO.approval == 'Approve':
        time.sleep(20)
        offerServ.processOfferNotification(txn.id, ssConst.OFFER_TARGET_TYPES[1][0], consumerDevice.deviceRegistrationId)

@task()
def processOffersForExistingConsumers():
    offerServ = OffersService()
    offerServ.processOffersForExistingConsumers()


