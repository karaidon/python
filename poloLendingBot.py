import urllib
import urllib2
import json
import time
import hmac,hashlib

def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class Poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret

    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if('return' in after):
            if(isinstance(after['return'], list)):
                for x in xrange(0, len(after['return'])):
                    if(isinstance(after['return'][x], dict)):
                        if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))
                            
        return after

    def api_query(self, command, req={}):

        if(command == "returnTicker" or command == "return24Volume"):
            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/public?command=' + command))
            return json.loads(ret.read())
        elif(command == "returnOrderBook"):
            ret = urllib2.urlopen(urllib2.Request('http://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif(command == "returnMarketTradeHistory"):
            ret = urllib2.urlopen(urllib2.Request('http://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(req['currencyPair'])))
            return json.loads(ret.read())
        elif (command =="returnLoanOrders"):
            ret = urllib2.urlopen(urllib2.Request('http://poloniex.com/public?command=' + "returnLoanOrders" + "&currency=" + str(req['currency'])))
            return json.loads(ret.read())
        else:
            req['command'] = command
            req['nonce'] = int(time.time()*1000)
            post_data = urllib.urlencode(req)

            sign = hmac.new(self.Secret, post_data, hashlib.sha512).hexdigest()
            headers = {
                'Sign': sign,
                'Key': self.APIKey
            }

            ret = urllib2.urlopen(urllib2.Request('https://poloniex.com/tradingApi', post_data, headers))
            jsonRet = json.loads(ret.read())
            return self.post_process(jsonRet)
        
polo = Poloniex("YOUR API KEY","YOUR API KEY SECRET")
currentLoanOrders = polo.api_query("returnLoanOrders", {"currency" : "ETH"})['offers']
currentLowestRate = float(currentLoanOrders[0]['rate'])
stopIteration = 0
currentRateIndex = 0
while stopIteration >= 4:
    nextHighestRate = float(currentLoanOrders[currentRateIndex+1]['rate'])
    if nextHighestRate - float(currentLoanOrders[currentRateIndex]['rate']) >= 0.000003:
        currentLowestRate = nextHighestRate
        currentRateIndex += 1
    else:
        stopIteration += 1
        currentRateIndex += 1


outstandingOffers = polo.api_query("returnOpenLoanOffers")
if (len(outstandingOffers) > 0):
    outstandingEthOffers = outstandingOffers["ETH"]
    for x in range(0,len(outstandingEthOffers)):
        offer = outstandingEthOffers[x]
        if (float(offer["rate"]) > float(currentLowestRate) + 0.00001):
            print polo.api_query("cancelLoanOffer", {"orderNumber" : offer["id"]})

print "currentLowestRate is "
print currentLowestRate
myRate = float(currentLowestRate) - 0.00000100
print "myRate is "
print myRate
myBalance = polo.api_query("returnAvailableAccountBalances", {'account': 'lending'})['lending']['ETH']
print "current unloaned balance is "
print myBalance
if float(myBalance) < 0:
    if myRate < 0.0004:
        myRate = 0.0004
myDuration = int(((myRate-0.0005)*10000))
if myDuration < 0:
    myDuration = 0
myDuration += 2
print "myDuration is "
print myDuration
if (float(myBalance) >= 1):
    myLoanAmt = float(myBalance)-0.0000001
    print polo.api_query("createLoanOffer", {"currency" : "ETH", "amount" : str(myLoanAmt), "duration" : str(myDuration), "autoRenew" : "0", "lendingRate" : str(myRate)})
	
activeLoans = polo.api_query("returnActiveLoans")["provided"]
if (len(activeLoans) > 0):
	for x in range(0,len(activeLoans)):
		loan = activeLoans[x]
		if loan["currency"] == "ETH":
			if float(loan["rate"]) >= myRate:
				if loan["autoRenew"] == 0:
					print ""
					print "loanrate is "
					print loan["rate"]
					print "toggling to on"
					polo.api_query("toggleAutoRenew", {"orderNumber" : loan["id"]})
			else:
				if loan["autoRenew"] == 1:
					print ""
					print "loanrate is "
					print loan["rate"]
					print "toggling to off"
					polo.api_query("toggleAutoRenew", {"orderNumber" : loan["id"]})
