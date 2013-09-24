Pyramid-Acceptors-Rpi-Python-Driver
===================================

This is for the Apex 7000 bill acceptor from http://pyramidacceptors.com/ Drivers for the Raspberry Pi

Created by 
Warren from Absorbing Technologies http://www.absorbingtechnologies.com/

continued development by BitHighlander

Setup
===================

clean Raspbian install

sudo apt-get install python-crypto

sudo apt-get install python-serial

sudo apt-get install zbar-tools


nano planb.py

copy/paste


install electrum
=================

sudo apt-get install python-qt4 python-pip

sudo pip install http://download.electrum.org/Electrum-1.8.1.tar.gz#md5=dc9f4b1cb38bd1d152be83d0a430cf62

startx and log into rpi

ctr shift T to open terminal

electrum

Backup seed (printer, or write it down) and make a new wallet

load btc into wallet

plug in webcam

sudo python planb.py

(currently headless, will scan for address's display in terminal and send btc after every bill that enterd) 

GUI is coming! 
