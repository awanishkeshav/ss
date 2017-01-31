from django.conf.urls import url
from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns

from beapi import views
from beapi.consumerCard import cardViews
from beapi.consumerCard import crudViews
from beapi.client import clientCrudViews
from beapi.merchant import merchantCrudViews
from beapi.rulesEngine import txnRulesViews

from beapi.consumer import consumerViews
from beapi.common import commonCrudViews
from beapi.common import commonViews
from beapi.merchant import merchantViews
from beapi.notif import android

##Crud apis -  primarily for the backend team
urlpatterns = [

    url(r'^beapi/crud/common/category/$', commonCrudViews.TxnCategoryList.as_view()),
    url(r'^beapi/crud/common/category/(?P<pk>[0-9]+)/$', commonCrudViews.TxnCategory.as_view()),

    url(r'^beapi/crud/client/$', clientCrudViews.ClientList.as_view()),
    url(r'^beapi/crud/client/(?P<pk>[0-9]+)/$', clientCrudViews.Client.as_view()),

    url(r'^beapi/crud/consumer/card/$', crudViews.ConsumerCardVOList.as_view()),
    url(r'^beapi/crud/consumer/card/(?P<pk>[0-9]+)/$', crudViews.ConsumerCardVO.as_view()),

    url(r'^beapi/crud/consumer/account/$', crudViews.ConsumerAccountList.as_view()),
    url(r'^beapi/crud/consumer/account/(?P<pk>[0-9]+)/$', crudViews.ConsumerAccount.as_view()),

    url(r'^beapi/crud/consumer/txn/$', crudViews.ConsumerTxnList.as_view()),
    url(r'^beapi/crud/consumer/txn/(?P<pk>[0-9]+)/$', crudViews.ConsumerTxn.as_view()),

    url(r'^beapi/crud/consumer/tag/$', crudViews.ConsumerTagList.as_view()),
    url(r'^beapi/crud/consumer/tag/(?P<pk>[0-9]+)/$', crudViews.ConsumerTag.as_view()),

    url(r'^beapi/crud/tag/txn$', crudViews.TxnTagList.as_view()),
    url(r'^beapi/crud/tag/txn(?P<pk>[0-9]+)/$', crudViews.TxnTag.as_view()),

    url(r'^beapi/crud/merchant/$', merchantCrudViews.MerchantList.as_view()),
    url(r'^beapi/crud/merchant/(?P<pk>[0-9]+)/$', merchantCrudViews.Merchant.as_view()),
]

## Customer APIs -  for app and simulator
urlpatterns += [
    url(r'^beapi/consumer/signup', consumerViews.register),
    url(r'^beapi/consumer/testAuth', consumerViews.testAuth),
    url(r'^beapi/consumer/location', consumerViews.saveLocation),
    url(r'^beapi/testmsg', android.test),

    url(r'^beapi/consts', commonViews.getConsts),
    url(r'^beapi/categories', commonViews.getCategories),
    url(r'^beapi/locations', commonViews.getLocations),


    #Consumer card
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/prefs$', consumerViews.getPrefs), #GET
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/prefLimits$', consumerViews.saveLimitPrefs), #PUT, DELETE
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/delPrefLimits$', consumerViews.deleteLimitPrefs), #PUT, DELETE
    url(r'^beapi/consumer/cards$', cardViews.getCards), #GET
    url(r'^beapi/consumer/card$', cardViews.registerCard), #POST - create card
    url(r'^beapi/consumer/card/(?P<pk>[0-9]+)/$', cardViews.card), #GET,PUT, DELETE - card
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/toggleLock$', consumerViews.toggleCardLockStatus), #PUT - card
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/txType/lock$', cardViews.lockTxTypeStatus), #PUT - card
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/txType/unlock$', cardViews.unlockTxTypeStatus), #PUT - card
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/txns$', cardViews.getTxns), #GET
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/txns/search$', cardViews.searchTxns), #GET
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/txn/(?P<txnId>[0-9]+)/$', cardViews.getTxn), #GET
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/txn/(?P<txnId>[0-9]+)/miscDtl$', cardViews.getTxnMiscDetails), #GET
    url(r'^beapi/consumer/card/(?P<cardId>[0-9]+)/txns/taggedSummary$', cardViews.getTxnTaggedSummary), #GET

    url(r'^beapi/consumer/merchant/(?P<merchantId>[0-9]+)/reviewTemplate$', merchantViews.getReviewTemplate), #GET
    url(r'^beapi/consumer/merchant/(?P<merchantId>[0-9]+)/offers$', merchantViews.getOffers), #GET
    url(r'^beapi/consumer/merchant/(?P<merchantId>[0-9]+)/reviewSummary', merchantViews.reviews), #GET
    url(r'^beapi/consumer/merchant/(?P<merchantId>[0-9]+)/lock', consumerViews.lockMerchantStatus), #PUT - card
    url(r'^beapi/consumer/merchant/(?P<merchantId>[0-9]+)/unlock$', consumerViews.unlockMerchantStatus), #PUT - card
    url(r'^beapi/consumer/blockedMerchants$', consumerViews.blockedMerchants), #GET
    url(r'^beapi/consumer/merchant/offers$', merchantViews.getConsumerOffers), #GET
    url(r'^beapi/consumer/merchant/(?P<merchantId>[0-9]+)/offersOnRequest$', merchantViews.getOffersByDemand), #GET
    url(r'^beapi/consumer/merchant/offers/newCnt$', merchantViews.getNewOffersCnt), #GET
    url(r'^beapi/consumer/merchant/offers/nearBy$', merchantViews.getAllOffersNearMe), #GET
    url(r'^beapi/consumer/merchant/offers/(?P<offerId>[0-9]+)/$', merchantViews.getOffer), #GET
    url(r'^beapi/consumer/merchant/offers/read', merchantViews.markConsumerOffersRead), #GET



    url(r'^beapi/consumer/device/gcm/$', consumerViews.saveDeviceRegistrationId), #POST
    url(r'^beapi/consumer/txn/(?P<txnId>[0-9]+)/approval$', cardViews.saveApproval), #POST
    url(r'^beapi/consumer/txn/(?P<txnId>[0-9]+)/tag$', cardViews.addTag), #POST
    url(r'^beapi/consumer/txn/(?P<txnId>[0-9]+)/tags$', cardViews.addTags), #POST
    url(r'^beapi/consumer/txn/(?P<txnId>[0-9]+)/tag/(?P<tagId>[0-9]+)$', cardViews.removeTag), #POST
    url(r'^beapi/consumer/txn/(?P<txnId>[0-9]+)/review$', merchantViews.review), #GET, #POST

    url(r'^beapi/merchants$', merchantViews.getMerchants), #GET, POST
    url(r'^beapi/merchant$', merchantViews.merchant), #GET, POST
    url(r'^beapi/merchant/txnSummary$', merchantViews.getTxnAggSummary), #GET
    url(r'^beapi/merchant/reviews$', merchantViews.getReviews), #GET
    url(r'^beapi/merchant/reviewTemplate$', merchantViews.reviewTemplate), #GET , #PUT
    url(r'^beapi/merchant/review/(?P<reviewId>[0-9]+)$', merchantViews.getReviewDtl), #GET
    url(r'^beapi/merchant/offers$', merchantViews.getMerchantOffers), #GET
    url(r'^beapi/merchant/review/(?P<reviewId>[0-9]+)/response$', merchantViews.saveReviewResponse), #PUT
    url(r'^beapi/merchant/device$', merchantViews.register), #POST
    url(r'^beapi/merchant/location', merchantViews.saveLocation),
    url(r'^beapi/merchant/offer/(?P<offerId>[0-9]+)$', merchantViews.offer), #GET, PUT
    url(r'^beapi/merchant/offer$', merchantViews.addOffer), #GET
    url(r'^beapi/merchant/offer/(?P<offerId>[0-9]+)/status$', merchantViews.markOfferStatus), #PUT
    url(r'^beapi/merchant/offer/(?P<offerId>[0-9]+)/targetting/(?P<targettingId>[0-9]+)$', merchantViews.offerTargetting), #GET, PUT, DELETE
    url(r'^beapi/merchant/offer/(?P<offerId>[0-9]+)/targettings$', merchantViews.getOfferTargettingList), #GET,
    url(r'^beapi/merchant/offer/(?P<offerId>[0-9]+)/targetting$', merchantViews.addOfferTargetting), #GET,
]

##Rules Engine
urlpatterns += [
    url(r'^beapi/rules/txn', txnRulesViews.processTxn), #POST
]
##Temp
urlpatterns += [
    url(r'^beapi/loadConsumerOffers', merchantViews.loadConsumerOffers), #POST
]

urlpatterns = format_suffix_patterns(urlpatterns)
