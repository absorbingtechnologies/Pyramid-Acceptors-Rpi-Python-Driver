import easygui as eg
import sys

while 1:
    title = "Cash2BTC"
    eg.msgbox("Welcome to Cash2BTC's PlanB Bitcoin ATM.", title)
# IF NOT SETUP	start setup*

    msg ="Select your Wallet interface options"
    title = "Avaible Wallet Configurations"
    choices = ["Cash2BTC.com's hosted wallet", "Electrum", "BitcoinD", "Blockchain.info's API"]
    choice = eg.choicebox(msg, title, choices)

    # note that we convert choice to string, in case
    # the user cancelled the choice, and we got None.
    eg.msgbox("You chose: " + str(choice), "Survey Result")

    msg = "You are about to set up a "+str(choice)+" wallet Do you want to continue?"
    title = "Please Confirm"
    if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
	eg.msgbox("Lets set an administrator password")
    
    else:
        sys.exit(0)           # user chose Cancel

#   ***TO DO***

#*** Setup Wallet ***

#if Cash2BTC wallet

	#connect to server
	#request assignment
	#generate an mysql mysql user/password and store it locally
 
#if electrum, run electrum and have user backup wallet seed
	
	#command line electrum

#if BitcoinD

	#encrypt wallet with user defined password

#if Blockchain.info
	
	#bring an Iframe up with blockchain.info's webpage
	#instruct user to set second password for API! **** account options/api
	#promt user to enter BOTH***  passwords, and test the connection


#*** Setup Exchange *** 

#promt, would you like to link an exchange?

#how much of a buffer would to like? (amount of btc held in wallet before withdrawl from exchange
	
	#MTgox
		#scan API key in via webcam	
	#bitstamp.net
		#scan API key in via webcam
	#BTC-E
		#scan API key in via webcam

#****admin control panel****

	#run bill acceptor polling
	#check location of webcam, If no webcam found warn! 
		#if laser qr, find and verify its connected
	#have a button to *start atm* brings up new fullscreen window. Locks down Rpi, required admin password to exit window. (current price, BTC avaible, QR code reader, QR code generator of past transactions)  with iframe of clark moody for market watch
	#if rebooted (or power loss) go directly back into lock window
