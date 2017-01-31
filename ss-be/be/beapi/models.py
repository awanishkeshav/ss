from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from beapi.common.constants import SSConst
from beapi.constantModels import TxnCategory
import uuid

def offersPath(self, filename):
   extension = filename.split('.')[-1]
   random_id = "rid_%s" % (uuid.uuid4().hex,)
   return "offers/%s.%s" %(random_id, extension)


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

# Create your models here.
class Consumer(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    firstname = models.CharField(max_length=100, blank=True, default='')
    lastname = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    dob = models.BigIntegerField(blank=True, default=0)
    status = models.SmallIntegerField(default=1)
    lat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    lng = models.DecimalField(max_digits=10, decimal_places=2 , blank=True, default=0)
    blockedCards = models.CharField(max_length=4096, blank=True, default='')
    blockedMerchants = models.CharField(max_length=4096, blank=True, default='')
    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer"

class ConsumerDevice(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    consumerId = models.BigIntegerField(db_index=True)
    cardNum = models.CharField(max_length=255, blank=True, default='',db_index=True)
    deviceType = models.SmallIntegerField(blank=True, default=1)
    deviceSubType = models.SmallIntegerField(blank=True,  default=1)
    deviceToken = models.CharField(max_length=255, blank=False, default='',db_index=True)
    deviceRegistrationId = models.CharField(max_length=512, blank=True, null=True, default=None)
    status = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_device"

class ConsumerCard(models.Model):
    clientId = models.BigIntegerField(blank=True, default=1)
    consumerId = models.BigIntegerField(db_index=True)
    accountId = models.BigIntegerField(db_index=True)
    cardNum = models.CharField(max_length=255, blank=True, default='',db_index=True)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    avaialbleLimit = models.DecimalField(max_digits=10, decimal_places=2)
    currOS = models.DecimalField(max_digits=10, decimal_places=2)
    amtSpentSS = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    cardNetwork = models.CharField(max_length=20, blank=False,  choices=SSConst.NETWORK_TYPES)
    cardType = models.CharField(max_length=20, blank=False,  choices=SSConst.CARD_TYPES)
    cardTitle = models.CharField(max_length=20, blank=False, default='Classic Card')
    status = models.SmallIntegerField(default=1)
    blockedTxTypes = models.CharField(max_length=255, blank=True, null=True, default='')
    created = models.BigIntegerField()
    updated = models.BigIntegerField()

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_card"

class ConsumerAccount(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    clientId = models.BigIntegerField(blank=True, default=1)
    cardNum = models.CharField(max_length=255, blank=True, default='')
    phoneNum = models.BigIntegerField(blank=True, default=1,db_index=True)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    avaialbleLimit = models.DecimalField(max_digits=10, decimal_places=2)
    currOS = models.DecimalField(max_digits=10, decimal_places=2)
    activationCode = models.CharField(max_length=255, blank=False, default='xxx')
    cardNetwork = models.CharField(max_length=20, blank=False,  choices=SSConst.NETWORK_TYPES)
    cardType = models.CharField(max_length=20, blank=False,  choices=SSConst.CARD_TYPES)
    cardTitle = models.CharField(max_length=20, blank=False, default='Classic Card')

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_account"

class ConsumerPrefs(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    consumerId = models.BigIntegerField(db_index=True)
    cardId = models.BigIntegerField()
    merchantId = models.BigIntegerField()
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    periodKey = models.CharField(max_length=20, blank=False, default='')
    categoryKey = models.CharField(max_length=20, blank=False, default='')
    txType = models.CharField(max_length=20, blank=False, default='')
    ssApproval = models.CharField(max_length=20, blank=False,  choices=SSConst.APPROVAL_TYPES)

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_prefs"

class ConsumerAgg(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    consumerId = models.BigIntegerField()
    cardId = models.BigIntegerField()
    merchantId = models.BigIntegerField()
    amtSpentSS = models.DecimalField(max_digits=10, decimal_places=2)
    periodKey = models.CharField(max_length=20, blank=False, default='')
    categoryKey = models.CharField(max_length=255, blank=False, default='')
    txType = models.CharField(max_length=20, blank=False, default='')

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_agg"

class ConsumerTag(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    consumerId = models.BigIntegerField(db_index=True)
    tag = models.CharField(max_length=255, blank=False, default='')

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_tag"

class TxnTag(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    cardId = models.BigIntegerField(db_index=True)
    consumerTxn = models.ForeignKey('ConsumerTxn', blank='False', related_name='consumer_txn_id')
    consumerTag = models.ForeignKey('ConsumerTag', blank='False', related_name='tagId')
    class Meta:
        ordering = ('created',)
        db_table = "ss_txn_tag"

class ConsumerTxn(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    consumerId = models.BigIntegerField(db_index=True)
    cardId = models.BigIntegerField(db_index=True)
    txDate = models.BigIntegerField()
    amtSpentSS = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('TxnCategory', blank=True,null=True, related_name='category')
    txType = models.CharField(max_length=20, blank=False,  choices=SSConst.TXN_TYPES)
    merchant = models.ForeignKey('Merchant', blank=True,null=True, related_name='merchantId')
    tags = models.ManyToManyField('ConsumerTag', through='TxnTag', blank=True, null=True)
    reviewStatus = models.CharField(max_length=2, choices=SSConst.TXN_REVIEW_STATUSES)
    review =  models.BigIntegerField( blank=True,null=True)
    ssApproval = models.CharField(max_length=20, choices=SSConst.APPROVAL_TYPES)
    ssApprovalStatus = models.CharField(max_length=20, choices=SSConst.APPROVAL_STATUSES)
    remarks = models.CharField(max_length=255, blank=False, null=True)

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_txn"

class Merchant(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    uuid = models.CharField(max_length=50, blank=False, db_index=True)
    name = models.CharField(max_length=100, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(max_length=30, blank=True, default='')
    description = models.CharField(max_length=512, blank=True, null=True, default='')
    businessHours = models.CharField(max_length=100, blank=True, null=True, default='')
    status = models.SmallIntegerField(default=1)
    reviewStatus = models.CharField(max_length=2, choices=SSConst.TXN_REVIEW_STATUSES)
    lat = models.DecimalField( blank=True, max_digits=10, decimal_places=2,default=0.00)
    lng = models.DecimalField( blank=True, max_digits=10, decimal_places=2,default=0.00)
    accessCode = models.CharField(max_length=50, blank=True, null=True)
    deviceType = models.SmallIntegerField(blank=True, null=True, default=1)
    deviceSubType = models.SmallIntegerField(blank=True, null=True,   default=1)
    deviceRegistrationId = models.CharField(max_length=256, blank=True, null=True, default=None)
    installed = models.SmallIntegerField(blank=False, null=False, default=0)
    mccCode = models.SmallIntegerField(blank=False, null=False, default=1000)
    class Meta:
        ordering = ('name',)
        db_table = "ss_merchant"


class MerchantOffer(models.Model):

    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='', null=True)
    endDate = models.BigIntegerField( null=True)
    startDate = models.BigIntegerField( null=True)  ## Added on 7 Apr
    codeType = models.CharField(max_length=30, null=True, choices=SSConst.COUPON_CODE_TYPES)  ## Added on 7 Apr
    code = models.CharField(max_length=100, null=True, blank=True, default='')  ## Added on 7 Apr
    imgUrl = models.ImageField(upload_to=offersPath, null=True)
    merchant = models.ForeignKey('Merchant', blank=False, related_name='offerMerchantId', db_index=True)
    category = models.ForeignKey('TxnCategory', blank=True,null=True, related_name='offerCategory')
    distance = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=30, null=True, choices=SSConst.OFFER_STATUSES)

    class Meta:
        ordering = ('title',)
        db_table = "ss_merchant_offer"

class MerchantOfferTargetting(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    offer = models.ForeignKey('MerchantOffer', db_index=True, blank=False, related_name='tagetMerchantOfferId')
    targetType = models.CharField(max_length=30, choices=SSConst.OFFER_TARGET_TYPES)
    minVisits = models.CharField(max_length=100, blank=True, default='')
    minTotalSpend = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('updated',)
        db_table = "ss_merchant_offer_targetting"


class ConsumerMerchant(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    consumerId = models.BigIntegerField(db_index=True)
    merchant = models.ForeignKey('Merchant', blank=True,null=True, related_name='cons_merch_id')
    status = models.SmallIntegerField(default=1)
    currentDistance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_merchant"

class ConsumerOffer(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    consumerId = models.BigIntegerField(db_index=True)
    offer = models.ForeignKey('MerchantOffer', blank=True,null=True, related_name='cons_offer_id')
    merchantId = models.BigIntegerField()
    status = models.CharField(max_length=30, choices=SSConst.CONSUMER_OFFER_STATUSES)
    endDate = models.BigIntegerField( null=True)
    startDate = models.BigIntegerField( null=True)  ## Added on 7 Apr

    class Meta:
        ordering = ('created',)
        db_table = "ss_consumer_offer"

class Client(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    name = models.CharField(max_length=100, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=100, blank=True, default='')
    token = models.CharField(max_length=255, blank=False, default='')
    status = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ('created',)
        db_table = "ss_client"

class Scenario(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    merchantName = models.CharField(max_length=100, blank=True, default='')
    merchantUuid =  models.CharField(max_length=100, blank=False, default='')
    txnType = models.CharField(max_length=100, blank=True, default='')
    mccCode = models.CharField(max_length=255, blank=True, default='')
    category = models.CharField(max_length=255, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    file = models.FileField(upload_to='media/files', blank=True)

    class Meta:
        ordering = ('id',)
        db_table = "ss_scenario"

class ReviewTemplate(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    criteria1 = models.CharField(max_length=100, blank=True, null=True, default='')
    criteria2 = models.CharField(max_length=100, blank=True, null=True, default='')
    criteria3 = models.CharField(max_length=100, blank=True, null=True, default='')
    version = models.IntegerField(default=1)
    commentRequired = models.SmallIntegerField(default=1)
    merchant = models.ForeignKey('Merchant', db_index=True, blank=False, related_name='reviewTmplMerchantId')
    class Meta:
        ordering = ('id',)
        db_table = "ss_review_template"

class TxnReview(models.Model):
    created = models.BigIntegerField()
    updated = models.BigIntegerField()
    txnId =  models.BigIntegerField(db_index=True)
    criteria1 = models.CharField(max_length=100, blank=True, null=True, default='')
    criteria1Value =  models.IntegerField(default=1, blank=True, null=True, )
    criteria2 = models.CharField(max_length=100, blank=True, null=True, default='')
    criteria2Value =  models.IntegerField(default=1, blank=True, null=True, )
    criteria3 = models.CharField(max_length=100, blank=True, null=True, default='')
    criteria3Value =  models.IntegerField(default=1, blank=True, null=True, )
    comment = models.CharField(max_length=512, blank=True, null=True, default='')
    response = models.CharField(max_length=512, blank=True, null=True, default='')
    offerId = models.BigIntegerField(null=True)
    merchant = models.ForeignKey('Merchant', db_index=True, blank=False, related_name='reviewMerchantId')
    class Meta:
        ordering = ('id',)
        db_table = "ss_txn_review"