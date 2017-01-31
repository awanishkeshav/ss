import time
import json
import math
from decimal import Decimal

class SSUtil(object):

    @staticmethod
    def getMillis():
        return int(time.time() * 1000)

    @staticmethod
    def err(msg):
        res = {
                "success":False,
                "msg":msg
            }
        return res

    @staticmethod
    def success(o):
        res = {
                "success":True,
                "data":o
            }
        return res

    @staticmethod
    def isIdinList(strLst,id):
        if strLst is None or strLst == '':
            return False
        else:
            lst = strLst.split(",")
            if not str(id) in lst:
                return False
            else:
                return True

    @staticmethod
    def addIdToList(strLst,id):
        if strLst is None or strLst == '':
            strLst = str(id)
        else:
            lst = strLst.split(",")
            if not str(id) in lst:
                strLst += ","+str(id)
        return strLst

    @staticmethod
    def removeIdFromList(strLst,id):
        if not strLst is None and strLst != '':
            lst = strLst.split(",")
            if str(id) in lst:
                lst.remove(str(id))
                strLst = ",".join(lst)
        return strLst



    @staticmethod
    def distanceInKms(lat1, long1, lat2, long2):

        # Convert latitude and longitude to
        # spherical coordinates in radians.
        degrees_to_radians = Decimal(math.pi/180.0)

        # phi = 90 - latitude
        phi1 = (Decimal(90 - lat1))*degrees_to_radians
        phi2 = (Decimal(90 - lat2))*degrees_to_radians

        # theta = longitude
        theta1 = (Decimal(long1))*degrees_to_radians
        theta2 = (Decimal(long2))*degrees_to_radians


        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
               math.cos(phi1)*math.cos(phi2))
        arc = math.acos( cos )

        # Remember to multiply arc by the radius of the earth
        # in your favorite set of units to get length.
        return arc * 6373
