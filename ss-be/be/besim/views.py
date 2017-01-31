import json
import urllib2

from django.contrib.sites.models import Site
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, loader

from django.contrib.sites.models import get_current_site
from beapi.common.jsonResponse import JSONResponse

from beapi.models import Scenario
from besim.forms import NameForm
from besim.forms import UsecaseForm
from beapi.models import Consumer
from beapi.constantModels import TxnCategory
from beapi.constantModels import Location

# list of mobile User Agents
mobile_uas = [
	'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
	'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
	'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
	'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
	'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
	'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
	'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
	'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
	'wapr','webc','winw','winw','xda','xda-'
	]

mobile_ua_hints = []


def mobileBrowser(request):
    ''' Super simple device detection, returns True for mobile devices '''
    print request.META['HTTP_USER_AGENT']
    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

    if (ua in mobile_uas):
        mobile_browser = True
    else:
        for hint in mobile_ua_hints:
            if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                mobile_browser = True

    return mobile_browser

def besim_home(request):
   if request.POST.has_key('card_number'):
        card_num = request.POST['card_number']
        amount = request.POST['amount']

        response_data = {}
        response_data['cardNum'] = card_num
        response_data['amount'] = amount

        if request.POST.has_key('scenario_id'):

           scenario_id = request.POST['scenario_id']
           ScenarioObj = Scenario.objects.get(id=scenario_id)
           response_data['merchantUuid'] = ScenarioObj.merchantUuid
           response_data['merchantName'] = ScenarioObj.merchantName
           response_data['txType'] = ScenarioObj.txnType
           response_data['mccCode'] = ScenarioObj.mccCode
           response_data['custom'] = 0
        else:
           response_data['merchantUuid'] = request.POST['merchantUuid']
           response_data['merchantName'] = request.POST['merchantName']
           response_data['txType'] = 'Card Present'
           response_data['mccCode'] = request.POST['category']
           international = int(request.POST['location'])
           response_data['custom'] = 1
           if international is 1:
              response_data['txType'] = 'International'


        api_url = ''.join(['http://', get_current_site(request).domain])
        api_url += '/beapi/rules/txn'

        request = urllib2.Request(api_url,headers={"SSCLIENTTOKEN" : "sbi-token"})
        request.add_data(json.dumps(response_data))
        response = urllib2.urlopen(request)
        resp_parsed = json.loads(response.read())
        return JSONResponse(json.dumps(resp_parsed))
   else:
        name_map = {'pk': 'id',
                     'firstName': 'firstName',
                     'lastName': 'lastName',
                    'cardNum' : 'cardNum'}

        consumers =  Consumer.objects.raw(
                                    '''
                          select c.id, cc.cardNum as cardNum,
                          c.firstname as firstName, c.lastname as lastName
                          from ss_consumer c LEFT JOIN ss_consumer_card cc ON c.id = cc.consumerId
                          group by c.id;
                                    ''', translations=name_map)
        form = UsecaseForm()
        scenario_list = Scenario.objects.order_by('id')
        mccCodes = TxnCategory.objects.order_by('id')
        locations = Location.objects.order_by('id')

#         if mobileBrowser(request):
#            return render(request, 'besim/mhome.html',{'TxnCategory' : mccCodes,'form': form ,
#                'scenario_list': scenario_list, 'consumers' : consumers, 'locations' : locations})
#         else:
        return render(request, 'besim/home.html',{'TxnCategory' : mccCodes,'form': form ,
               'scenario_list': scenario_list, 'consumers' : consumers, 'locations' : locations})

def besim_downloads(request):
 	return render(request, "besim/downloads.html")
