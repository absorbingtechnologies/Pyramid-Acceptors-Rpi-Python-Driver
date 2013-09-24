import os
import MySQLdb
import sys
import json
import decimal

#get price
getgox = 'curl https://data.mtgox.com/api/2/BTCUSD/money/ticker'

#os.system(cmd)
x = os.popen(getgox)
output = x.read()
decode = json.loads(output)
#print decode
last = decode['data']['last']['display_short']
pretty = decimal.Decimal(last[1:])
#this is where I pass bills tenderd in
dollars = 1

#convert USD/BTC
amount = dollars/pretty

#round to satoshi
amount = round(amount,8)
#convert to satoshi
amount = int(amount * 100000000)
print amount
#send btc from electrum

#if amount > free inputs, error (reject bill)

#get address
address = '16o94qS8ZFEoKUTrZfLd2sLhvDqLKi4hDe'

#command line
electrumsend = "electrum payto" + " " + address + " " + amount
x = os.popen(cmd)
output = x.read()

print 'Sent: ' + amount + ' to: ' + address + ' TXhash: ' + output 
