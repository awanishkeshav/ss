from rest_framework import serializers
import json
import datetime
from datetime import timedelta

class SSConst(serializers.BaseSerializer):
    def to_representation(self):
        return {
            'TXN_REVIEW_STATUSES': self.getJson(self.TXN_REVIEW_STATUSES),
            'TXN_TYPES': self.getJson(self.TXN_TYPES),
            'NETWORK_TYPES': self.getJson(self.NETWORK_TYPES),
            'CARD_TYPES': self.getJson(self.CARD_TYPES),
            'APPROVAL_TYPES': self.getJsonArray(self.APPROVAL_TYPES),
            'OFFER_TARGET_TYPES': self.getJsonArray(self.OFFER_TARGET_TYPES),
            'COUPON_CODE_TYPES': self.getJsonArray(self.COUPON_CODE_TYPES),
            'DATE_RANGES': self.getDateRangeArray(self.DATE_RANGES),
            'OFFER_STATUSES': self.getJsonArray(self.OFFER_STATUSES),
            'CONSUMER_OFFER_STATUSES': self.getJsonArray(self.CONSUMER_OFFER_STATUSES)
        }

    def getJson(self, lst):
        record={}
        for st in lst:
            record[st[0]] = st[1]
        return record
    def getJsonArray(self, lst):
        records = []
        for st in lst:
            record = {st[0]:st[1]}
            records.append(record)
        return records

    def isValidTxType(self, val):
        valid =  False
        for st in self.TXN_TYPES:
            if st[0] == val:
                valid =  True
                break
        return valid

    def isValidCardNetwork(self, val):
        valid =  False
        for st in self.NETWORK_TYPES:
            if st[0] == val:
                valid =  True
                break
        return valid

    def isValidCardType(self, val):
        valid =  False
        for st in self.CARD_TYPES:
            if st[0] == val:
                valid =  True
                break
        return valid

    def getDateRangeArray(self, lst):
        records = []
        for st in lst:
            valObj = st[1]
            valObj["starting_from"] = self.getStartTime(valObj["name"])
            record = {st[0]:valObj}
            records.append(record)
        return records

    def getStartTime(self, key ):
        today = datetime.datetime.now()
        start_date = None
        if key == "this_week":
            start_date = today - timedelta(days=today.weekday())
        if key == "last_week":
            start_date = today - timedelta(days=today.weekday()+7)
        if key == "this_month":
            start_date = datetime.date(day=1, month=today.month, year=today.year)
        if key == "last_month":
            first = datetime.date(day=1, month=today.month, year=today.year)
            start_date = first - datetime.timedelta(days=1)
            start_date = start_date.replace(day=1)
        if key == "all_time":
            start_date = datetime.date(day=1, month=1, year=1970)
        st = datetime.datetime(start_date.year, start_date.month, start_date.day)
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = st - epoch
        return delta.total_seconds() * 1000

    CURRENCY_SYMBOL=u"\u20B9"
    TXN_REVIEW_STATUSES = (
        ('NR', 'Not requested'),
        ('RR', 'Review requested'),
        ('RD', 'Reviewed'),
    )

    OFFER_TARGET_TYPES = (
        ('customer_request', 'Customer request'),
        ('existing_customers', 'Existing customers'),
        ('location_based', 'Location based'),
        ('post_review', 'Post review'),
        ('post_swipe', 'Post swipe'),
    )
    OFFER_STATUSES = (
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
        ('Archived', 'Archived'),
    )

    CONSUMER_OFFER_STATUSES = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Archived', 'Archived'),
        ('Blocked', 'Blocked'),
    )
    COUPON_CODE_TYPES = (
        ('none', 'None'),
        ('text', 'Text'),
        ('bar_code', 'Bar code'),
        ('qr_code', 'QR code'),
    )
    TXN_TYPES = (
        ('Online', 'Online'),
        ('Recurring', 'Recurring'),
        ('Card Not Present', 'Card Not Present'),
        ('Card Present', 'Card Present'),
        ('International', 'International'),
    )

    NETWORK_TYPES = (
        ('Master', 'Master'),
        ('Visa', 'Visa'),
    )

    CARD_TYPES = (
        ('Credit card', 'Credit card'),
        ('Debit card', 'Debit card'),
    )

    APPROVAL_TYPES = (
        ('Approve', 'None'),
        ('Warn', 'Warn'),
        ('AskMe', 'Ask me'),
        ('Block', 'Block'),
    )


    APPROVAL_STATUSES = (
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
        ('SentForApproval', 'SentForApproval'),
        ('UserApproved', 'UserApproved'),
        ('UserDenied', 'UserDenied'),
    )

    PERIOD_KEYS = (
        ('Any', 'Any time'),
        ('Daily', '1 DAY'),
        ('Weekly', '1 WEEK'),
        ('Monthly', '1 Month'),
    )
    DEVICE_NOTIFICATION_TYPES = {
                              "Info" : "Info",
                              "ApprovalRequired" : "ApprovalRequired",
                              "ReviewRequired" : "ReviewRequired",
                              "Block" : "Block",
                              "Offer" : "Offer",
      }

    DATE_RANGES = (
    ("this_week", {"name":"this_week","display":"This week",
                        "starting_from":0} ),
    ("last_week", {"name":"last_week","display":"Last week",
                        "starting_from":0}),
    ("this_month", {"name":"this_month","display":"This month",
                        "starting_from":0}),
    ("last_month",{"name":"last_month","display":"Last month",
                         "starting_from":0} ),
    ("all_time", {"name":"all_time","display":"All time",
                       "starting_from":0} )
    )

    MCCCODE_TYPES = (
	(1000, 'Food'),
	(1001, 'Travel'),
	(1002, 'Shopping'),
	(1003, 'Entertainment')
    )

    ALL_CARD_ID = -1
    ANY_PERIOD_KEY = "Any"
    ANY_CATEGORY_KEY = "Any"
    ANY_TX_Type = "Any"

    ALLOWED_MILLIS_FOR_RETRY = 10 * 60 * 100

    MERCHANT_DEFAULT_CONTACT_NUM = "9826249953"
    MERCHANT_DEFAULT_ADDRESS = "M.G. Road"