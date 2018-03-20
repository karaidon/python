
import json, smtplib
from coinbase.wallet.client import Client
APIKEY=""
APISECRET=""
SANDBOXAPIKEY=""
SANDBOXAPISECRET=""
FEETHRESHOLD=10
DROPTHRESHOLD=25

#TODO: Take into account longer term trends. Rather than just check last peak price, also check sampled price last week/last month.
#Right now we kinda protect from fast plummets, but longer term drops/stagnation is not really accounted for?

#client = Client(SANDBOXAPIKEY, SANDBOXAPISECRET, base_api_uri='https://api.sandbox.coinbase.com')
client = Client(APIKEY, APISECRET,)
accountID = client.get_accounts()[0]['id']
currentBTCBal = client.get_accounts()[0]['balance']['amount']
print "Current BTC Bal is " + currentBTCBal
boughtPrice = 0
highestPriceSoFar = 0

dataRead = open('priceData.txt','r')
dataReadString = dataRead
dataReadJson = json.load(dataReadString)

boughtPrice = dataReadJson['boughtPrice']
highestPriceSoFar = dataReadJson['peakPrice']

print "Current bitcoin bought at " 
print boughtPrice
print "Peak price is "
print highestPriceSoFar

sellPriceJson = client.get_sell_price()
sellPrice = float(sellPriceJson['amount'])

if boughtPrice == 0:
 print "Sell has already executed. Waiting for new BTC purchase."
 boughtPrice = 0
 highestPriceSoFar = 0
else:
 if sellPrice > highestPriceSoFar:
  highestPriceSoFar = sellPrice
  print "New peak price. Price has increased to: "
  print sellPrice
 else:
  print "Price has decreased to: "
  print sellPrice
  if highestPriceSoFar - DROPTHRESHOLD <= sellPrice:
   if sellPrice > boughtPrice + FEETHRESHOLD:
    print "Price has dropped too low. Selling now!"
    client.sell(accountID, amount=currentBTCBal, currency='BTC')
    print "Selling " + currentBTCBal + " for approx. S$"
    print sellPrice * float(currentBTCBal)
    msg = "\r\n".join([
    "From: EMAIL",
    "To: EMAIL",
    "Subject: BTC has been sold",
    "",
    "Sold XBT" + currentBTCBal + " for approx. S$" + str(sellPrice * float(currentBTCBal)),
    " at the current rate of S$" + str(sellPrice) + " for XBT 1.0.",
    ])
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login("EMAIL", "EMAILPASSWORD")
    smtpObj.sendmail('EMAIL','EMAIL',msg)
    smtpObj.quit()
    boughtPrice = 0
    highestPriceSoFar = 0
 
 
print "Storing non-volatile data..."
storedData = {}
storedData['boughtPrice'] = boughtPrice
storedData['peakPrice'] = highestPriceSoFar
storedData['lastCheckedPrice'] = sellPrice
dataJson = json.dumps(storedData)

obj = open('priceData.txt','w')
obj.write(dataJson)
obj.close
print "Scheduled price check has ended."
