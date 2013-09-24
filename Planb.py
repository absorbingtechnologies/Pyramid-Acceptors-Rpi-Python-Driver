#!/usr/bin/env python
#gen1 9/5 *received BitHighlander
-
-
-"""   
-    This program is free software: you can redistribute it and/or modify
-    it under the terms of the GNU General Public License as published by
-    the Free Software Foundation, either version 3 of the License, or
-    (at your option) any later version.
-
-    This program is distributed in the hope that it will be useful,
-    but WITHOUT ANY WARRANTY; without even the implied warranty of
-    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-    GNU General Public License for more details.
-
-    You should have received a copy of the GNU General Public License
-    along with this program.  If not, see <http://www.gnu.org/licenses/>.
-""" 


import os
#import MySQLdb
import sys
import json
import decimal
from subprocess import Popen, PIPE
import sys, thread, time, shlex, math, re
from Crypto.Hash import SHA256
import serial, time, binascii

escrowed = False
ackBit = 0
apexModel = 0
apexVersion = 0
billCredit = 0
billCount = bytearray([0,0,0,0,0,0,0,0])
laststatus = ''

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    bytesize=serial.SEVENBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE
)

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58decode(v, length):
    """ decode v into a string of len bytes                                                                                                                            
    """
    long_value = 0L
    for (i, c) in enumerate(v[::-1]):
        long_value += __b58chars.find(c) * (__b58base**i)
    
    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result
    
    nPad = 0
    for c in v:
        if c == __b58chars[0]: nPad += 1
        else: break
    
    result = chr(0)*nPad + result
    if length is not None and len(result) != length:
        return None
    
    return result

def get_bcaddress_version(strAddress):
    """ Returns None if strAddress is invalid.  Otherwise returns integer version of address. """
    addr = b58decode(strAddress,25)
    if addr is None: return None
    version = addr[0]
    checksum = addr[-4:]
    vh160 = addr[:-4] # Version plus hash160 is what is checksummed                                                                                                    
    h3=SHA256.new(SHA256.new(vh160).digest()).digest()
    if h3[0:4] == checksum:
        return ord(version)
    return None

# threaded function to scan
def scan_QR():
    global QR_code
    #global stop_scan
    proc = Popen(shlex.split('zbarcam --raw --nodisplay --prescale=640x480'), stdout=PIPE)
    #while 1:
    #    print proc.communicate()[0]
    #    time.sleep(1)
    while (stop_scan == False):
        line = proc.stdout.readline()
        if line:
            QR_code = line.strip()
        time.sleep(0.1)
    print("stopping scanner")
    proc.terminate()
    thread.exit()

    
# dummy thread
def dummy():
    global QR_code
    global stop_scan
    while 1:
        if (QR_code != ''):
            print "Raw code found:", QR_code
            QR_code = QR_code.strip('bitcoin:')
            QR_code = QR_code.split('?',1)[0]
            QR_code = QR_code.strip()
            
            if re.match(r"[a-zA-Z1-9]{27,35}$", QR_code) is None:
                print "Invalid Bitcoin (error 1)"
            version = get_bcaddress_version(QR_code)
            if version is None:
                print "Invalid Bitcoin (error 2)"
            else:
                print "BitCoin Address verified:",QR_code," Ver:",version
            QR_code = ''
        time.sleep(0.1)
        #pass
    
QR_code = ''
stop_scan = False


# main code start
try:
    thread.start_new_thread( scan_QR, () )
    thread.start_new_thread( dummy, () )
except:
    print("Unable to start threads")

print("scanner started")
    
print "opening port"
ser.open()

while ser.isOpen():
    
    # basic message   0      1      2      3      4      5      6      7
    #               start,   len,   ack, bills,escrow,resv'd,  end, checksum
    msg = bytearray([0x02,  0x08,  0x10,  0x7F,  0x10,  0x00,  0x03,  0x00])
    
    msg[2] = 0x10 | ackBit
    if (ackBit == 1):
        ackBit = 0
    else:
        ackBit = 1
    
    if (escrowed):
        msg[4] |= 0x20
    
    #calculate checksum of message for Byte 7
    msg[7] = msg[1] ^ msg[2]
    msg[7] ^= msg[3]
    msg[7] ^= msg[4]
    msg[7] ^= msg[5]
    
    #print(">> %s" % binascii.hexlify(msg))
    ser.write(msg)
    time.sleep(0.1)
    
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if (out == ''): continue
        
    #print "<<", binascii.hexlify(out)
    
    status = ""
    if (ord(out[3]) & 1): status += " IDLING "
    if (ord(out[3]) & 2): status += " ACCEPTING "
    if (ord(out[3]) & 4):
        status += " ESCROWED "
        escrowed = True
    else:
        escrowed = False
    if (ord(out[3]) & 8): status += " STACKING "
    if (ord(out[3]) & 0x10): status += " STACKED "
    if (ord(out[3]) & 0x20): status += " RETURNING "
    if (ord(out[3]) & 0x40): status += " RETURNED "
    
    if (ord(out[4]) & 1): status += " CHEATED! "
    if (ord(out[4]) & 2): status += " REJECTED "
    if (ord(out[4]) & 4): status += " JAMMED! "
    if (ord(out[4]) & 8): status += " FULL! "
    if (ord(out[4]) & 0x10): status += " w/CASSETTE "
    if (laststatus != status):
        print 'Acceptor status:',status
        laststatus = status
    
    if (ord(out[5]) & 1): print 'Acceptor powering up / initializing.'
    if (ord(out[5]) & 2): print 'Acceptor received invalid command.'
    if (ord(out[5]) & 4): print 'Acceptor has failed!'
    
    if (out[7] != apexModel or out[8] != apexVersion):
        apexModel = out[7]
        apexVersion = out[8]
        print "Connected to Acceptor model", binascii.hexlify(apexModel), "FW ver", binascii.hexlify(apexVersion)

    #print status
    
    billCredit = ord(out[5]) & 0x38
    if(billCredit == 0): billCredit = 0
    if(billCredit == 8): billCredit = 1
    if(billCredit == 0x10): billCredit = 2
    if(billCredit == 0x18): billCredit = 3
    if(billCredit == 0x20): billCredit = 4
    if(billCredit == 0x28): billCredit = 5
    if(billCredit == 0x30): billCredit = 6
    if(billCredit == 0x38): billCredit = 7
    
    if(billCredit != 0):
        lastCredit = billCredit
        if(ord(out[3]) & 0x10):
            #Send bitcoin
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
	    dollars = billCredit
	    #convert USD/BTC
	    amount = dollars/pretty
   	    #round to satoshi
	    amount = round(amount,8)
	    #convert to satoshi
	    amount = int(amount * 100000000)
	    amount = str(amount)
	    print amount
	    #send btc from electrum
	    #if amount > free inputs, error (reject bill)
	    #get address
	    #address = '16o94qS8ZFEoKUTrZfLd2sLhvDqLKi4hDe'
            address = QR_code
            #command line
	    electrumsend = "electrum payto" + " " + address + " " + amount
	    x = os.popen(cmd)
	    output = x.read()
  	    print 'Sent: ' + amount + ' to: ' + address + ' TXhash: ' + output 
	    print output
	    print "Bill credited: Bill", billCredit
            billCount[billCredit] += 1
            print "Acceptor now holds:",binascii.hexlify(billCount)  
    time.sleep(0.1)
    #print binascii.hexlify(billCount)
    
    
print "port closed"
ser.close()
