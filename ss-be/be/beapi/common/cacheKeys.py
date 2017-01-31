class CacheKeys(object):

    @staticmethod
    def getBuildVersion():
        return "3"


    @staticmethod
    def useCache():
        return False

    @staticmethod
    def getCardNumKey(cardNum):
        ver = CacheKeys.getBuildVersion()
        return ver+"_conCard_"+cardNum

    @staticmethod
    def getClientTokenKey(token):
        ver = CacheKeys.getBuildVersion()
        return ver+"_clt_"+token

    @staticmethod
    def getClientIdKey(id):
        ver = CacheKeys.getBuildVersion()
        return ver+"_cli_"+str(id)

    @staticmethod
    def getConsumerDeviceTokenKey(token):
        ver = CacheKeys.getBuildVersion()
        return ver+"_device_"+token

    @staticmethod
    def getConsumerIdKey(id):
        ver = CacheKeys.getBuildVersion()
        return ver+"_con_"+str(id)

    @staticmethod
    def getMerchantUuidKey(uuid):
        ver = CacheKeys.getBuildVersion()
        return ver+"_merch_"+str(uuid)

    @staticmethod
    def getCategoryByMccCodeKey(mccCode):
        ver = CacheKeys.getBuildVersion()
        return ver+"_cat_"+str(mccCode)

    @staticmethod
    def getConsumerAggsByIdKey(id):
        ver = CacheKeys.getBuildVersion()
        return ver+"_agg_"+str(id)

    @staticmethod
    def getConsumerPrefsByIdKey(id):
        ver = CacheKeys.getBuildVersion()
        return ver+"_prefs_"+str(id)
