from django.forms import widgets
from rest_framework import serializers
from beapi.models import Consumer
from beapi.models import ConsumerDevice
from beapi.models import ConsumerDevice
from beapi.models import ConsumerCard
from beapi.models import ConsumerPrefs
from beapi.models import ConsumerAgg
from beapi.models import ConsumerTxn
from beapi.models import Merchant
from beapi.models import MerchantOffer
from beapi.models import MerchantOfferTargetting
from beapi.models import ConsumerMerchant
from beapi.models import ConsumerOffer
from beapi.models import Client
from beapi.models import ConsumerAccount
from beapi.models import ConsumerTxn
from beapi.models import ConsumerTag
from beapi.models import TxnTag
from beapi.models import ReviewTemplate
from beapi.models import TxnReview
from beapi.constantModels import TxnCategory
from beapi.constantModels import Location


class TxnCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TxnCategory
        fields = ('id','name', 'mccCode')

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ('id', 'firstname', 'lastname', 'email', 'dob', 'status',
                  'lat','lng','created','updated')
class ConsumerAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerAccount
        fields = ('id','cardNum','clientId','phoneNum', 'limit', 'avaialbleLimit',
                  'currOS','activationCode','cardNetwork',
                  'cardType','cardTitle', 'created','updated')
class ConsumerDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerDevice
        fields = ('id', 'consumerId', 'cardNum', 'deviceType', 'deviceSubType',
                  'deviceToken','status', 'created', 'updated')

class ConsumerCardSerializer(serializers.ModelSerializer):
     class Meta:
        model = ConsumerCard
        fields = ('id','clientId', 'accountId', 'consumerId', 'cardNum',
                  'limit','avaialbleLimit','currOS','amtSpentSS',
                  'cardNetwork','cardType','cardTitle','status', 'blockedTxTypes','created','updated')
class ConsumerPrefsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerPrefs
        fields = ('id', 'consumerId','cardId','merchantId','periodKey', 'limit',
                  'categoryKey','txType','ssApproval','created', 'updated')

class ConsumerAggSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerAgg
        fields = ('id', 'consumerId','cardNum','periodKey', 'amtSpentSS',
                  'categoryKey','txType','blockedCards','blockedMerchants',
                  'created', 'updated')

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ('id', 'uuid','accessCode', 'name', 'email','phone','address','status',
                  'lat','lng','deviceType','deviceSubType',
                  'installed','deviceRegistrationId',
                  'description', 'businessHours')

class MerchantOfferSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(many=False, read_only=True)
    category = TxnCategorySerializer(many=False, read_only=True)
    class Meta:
        model = MerchantOffer
        fields = ('id', 'title', 'description','merchant','category','imgUrl','distance',
                  'startDate','endDate','codeType','code','status','created', 'updated')

class ConsumerOfferSerializer(serializers.ModelSerializer):
    offer = MerchantOfferSerializer(many=False, read_only=True)
    class Meta:
        model = ConsumerOffer
        fields = ('id', 'consumerId','merchantId','offer','status','created', 'updated')

class MerchantOfferTargettingSerializer(serializers.ModelSerializer):
    offer = MerchantOfferSerializer(many=False, read_only=True)
    class Meta:
        model = MerchantOfferTargetting
        fields = ('id', 'offer', 'targetType','minVisits','minTotalSpend','created', 'updated')

class ConsumerMerchantSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(many=False, read_only=True)
    class Meta:
        model = ConsumerMerchant
        fields = ('id', 'consumerId', 'merchant','status',
                  'created', 'updated','currentDistance')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'name', 'email','phone','status',
                  'created', 'updated')

class ConsumerTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumerTag
        fields = ('id', 'consumerId', 'tag','created','updated')

class TxnTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TxnTag
        fields = ('id', 'consumerTxn','consumerTag', 'cardId','created','updated')

class ConsumerTxnSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(many=False, read_only=True)
    category = TxnCategorySerializer(many=False, read_only=True)
    tags = ConsumerTagSerializer(many=True, read_only=False)
    class Meta:
        model = ConsumerTxn
        fields = ('id','consumerId', 'cardId',
                   'amtSpentSS','category','txDate',
                  'txType','reviewStatus', 'review','merchant', 'tags','created','updated')

class ReviewTemplateSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(many=False, read_only=True)
    class Meta:
        model = ReviewTemplate
        fields = ('id','merchant', 'criteria1',
                   'criteria2','criteria3','version',
                  'commentRequired','created','updated')

class TxnReviewSerializer(serializers.ModelSerializer):
    merchant = MerchantSerializer(many=False, read_only=True)
    class Meta:
        model = TxnReview
        fields = ('id','txnId','merchant', 'criteria1','criteria1Value',
                   'criteria2','criteria2Value','criteria3','criteria3Value',
                  'comment','response','offerId','created','updated')
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id','name', 'international')


