#!/usr/bin/env python
#-*- coding: utf-8 -*-
# /etc/init.d/sample.py
import RPi.GPIO as GPIO
import MFRC522
import smbus
from datetime import date
import time
import datetime
import hexdump

#################################################VARIABLES#################################################
today = datetime.datetime.today()
str_today =today.strftime("%Y%m%d")
Date_du_jour = str_today

B2S8=8
B2S9=9
B2S10=10
B3S12=12
B3S13=13

forward=True
# relais
GPIO_relais = 40# le relais est branche sur la pin 32 / GPIO12
GPIO.setmode(GPIO.BOARD) # comme la librairie MFRC522
GPIO.setwarnings(False)
GPIO.setup(GPIO_relais, GPIO.OUT)
# led
##time_sleep_led = 2
##GPIO_greenPin=12
##GPIO_redPin=16
##GPIO.setmode(GPIO.BOARD)
##GPIO.setwarnings(False)
##GPIO.setup(GPIO_redPin, GPIO.OUT)
##GPIO.setup(GPIO_greenPin, GPIO.OUT)
# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address, if any error, change this address to 0x3f
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005





######################################################################################################################
#################################################FONCTIONS#################################################
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  message = message.ljust(LCD_WIDTH," ")
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

##def turnOn(pin):
##    GPIO.output(pin,True)
##    time.sleep(time_sleep_led)
##    GPIO.output(pin,False)
##
##def LED_Blink(Kel_led):
##    print("Blinking...")
##    iLed = threading.local()
##    iLed.i = 0
##    GPIO.setmode(GPIO.BOARD)
##    GPIO.setwarnings(False)
##    GPIO.setup(Kel_led, GPIO.OUT)
##    while (iLed.i <= 25):
##        GPIO.output(Kel_led, True)
##        time.sleep(0.1)   
##        GPIO.output(Kel_led, False)
##        time.sleep(0.1)
##        iLed.i = iLed.i + 1
        
def declencher_relais():
    time.sleep(1)
    GPIO.output(GPIO_relais, GPIO.LOW)
    time.sleep(1)
    GPIO.output(GPIO_relais, GPIO.HIGH)
    lcd_init()
    
bus = smbus.SMBus(1)
lcd_init()
lcd_byte(0x01,LCD_CMD)
######################################################################################################################
continue_reading = True
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
# Welcome message
##print("Looking for cards")
##print("Press Ctrl-C to stop.")
 
# This loop checks for chips. If one is near it will get the UID
try:

  while continue_reading:
    ##print("Looking for cards")

    # Date
    stoday = datetime.datetime.today()
    # Display Message
    lcd_string(stoday.strftime("%d-%m-%Y %H:%M"),LCD_LINE_1)
    lcd_string("Attente Carte",LCD_LINE_2)


    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Carte detectee")
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
        # Print UID
        print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])+"."+str(uid[4]))
        # This is the default key for authentication
        keyA_Public = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Clee d authentification privee
        keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
         
        key =  [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
        #keyA_Prive = key
        #keyA_Public = key
        # Select the scanned tag
        
        MIFAREReader.MFRC522_SelectTag(uid)
         
        # Authenticate with private key

        print("..............................BLOC 1.....................................")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 4,keyA_Prive, uid)
        nom=""
        if(status == MIFAREReader.MI_OK):        
                ##print ("Authentification Avec la Clee Prive ",keyA_Prive,"\n")
                ##print("Carte deja initialise sur secteur ",4)
                try:        
                    
                    nom = MIFAREReader.MFRC522_Read(4)
                    prenom = MIFAREReader.MFRC522_Read(5)
                    societe = MIFAREReader.MFRC522_Read(6)
                    
                    ##print(nom[0],"\n")
                    nom_str=chr(nom[0])+chr(nom[1])+chr(nom[2])+chr(nom[3])+chr(nom[4])+chr(nom[5])+chr(nom[6])+chr(nom[7])+chr(nom[8])+chr(nom[9])+chr(nom[10])+chr(nom[11])+chr(nom[12])+chr(nom[13])+chr(nom[14])+chr(nom[15])
                    ##nom_str=nom_str.decode("utf-8")
                    print(nom_str)
                    prenom_str=chr(prenom[0])+chr(prenom[1])+chr(prenom[2])+chr(prenom[3])+chr(prenom[4])+chr(prenom[5])+chr(prenom[6])+chr(prenom[7])+chr(prenom[8])+chr(prenom[9])+chr(prenom[10])+chr(prenom[11])+chr(prenom[12])+chr(prenom[13])+chr(prenom[14])+chr(prenom[15])
                    ##prenom_str=""
                    print(prenom_str)
                    societe_str=chr(societe[0])+chr(societe[1])+chr(societe[2])+chr(societe[3])+chr(societe[4])+chr(societe[5])+chr(societe[6])+chr(societe[7])+chr(societe[8])+chr(societe[9])+chr(societe[10])+chr(societe[11])+chr(societe[12])+chr(societe[13])+chr(societe[14])+chr(societe[15])
                    ##societe_str=""
                    print(societe_str)
                    ##print(decode_secteur_hex(nom))
                    
                    ##print(binascii.unhexlify(nom[0]))
                    ##print(bytes.fromhex(nom[0].decode('utf-8')))

                except:
                    print("\nErreur Lecture  sur secteur ",4,"\n")                    
        
        #next = False
        print("..............................BLOC 2.....................................")   
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B2S8,keyA_Prive, uid)
        # Check if authenticated
        if(status == MIFAREReader.MI_OK):
                ##next = True

                ##print ("Authentification Avec la Clee Prive ",keyA_Prive,"\n")
                ##print("Carte deja initialise sur secteur ",B2S8)
                try:
                      
                    status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A,B2S8,keyA_Prive, uid)
                    backData = MIFAREReader.MFRC522_Read(B2S8)
                    conso = 500
                    maxseau = 10
##                    s = b"C" +b"20190502" + (conso).to_bytes(2, byteorder='big') + (maxseau).to_bytes(1, byteorder='big') + b"...."
##                    MIFAREReader.MFRC522_Write(B2S8,s)
####                    print(".........................................................................")    
##                    ##MIFAREReader.MFRC522_Read(B2S8)
##                    #print("Traduction en ASCII : ", end='')
##                    break
                    
                    c= 1
                    Date_LV=""
                    Date_LV_Out=""
                    
                    while (c<9):
                        if(backData[c]!=0) :
                            try :
                                Date_LV=str(chr(backData[c]))
                                Date_LV_Out=Date_LV_Out+Date_LV
                            except :
                                print(" Contenu Illisible")
                        c+=1
                    if(Date_du_jour <= Date_LV_Out):
                        forward= True
                        print("Votre carte est à jour")
                    else:
                        #L1=
                        print("La validite de votre carte est expire")
                        MIFAREReader.MFRC522_StopCrypto1()
                        lcd_string("CARTE",LCD_LINE_1)
                        lcd_string("EXPIRE ",LCD_LINE_2)
                        time.sleep(2)
                        #turnOn(GPIO_redPin)
                        forward= False
                        continue_reading = True
  
                    print("Date du jour            : "+Date_du_jour)
                    print("Date limite de validite : "+Date_LV_Out)
                    Credit_C=int(backData[9])*256+int(backData[10])
                    Seaux_MAX=int(backData[11])
                    print("Credit cumule           : ",Credit_C)
                    ##print("cons ",backData[9],backData[10])
                    Max_Seaux = int(backData[11])
                    print("Max seaux par jour     : ",Max_Seaux)
                    
                    #MIFAREReader.MFRC522_StopCrypto1()
                     
                except:
                    print("\nErreur Lecture  sur secteur ",B2S8,"\n")
                        
                #continue_reading = False
                #next = False
        else:
            print ("\nErreur d\'Authentification Avec la Clee Prive sur secteur ",B2S8,"\n")


        ##print("\nTu es ici")
        if(forward== True):
            print("..............................BLOC 3.....................................")  
            status1 = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B3S12,  keyA_Prive, uid)
            if status1 == MIFAREReader.MI_OK:
                today = datetime.datetime.today()
                str_today =today.strftime("%Y%m%d")
                    #cmpt = cmpt + 1
                    ##blockAddr = B3S12
                   # MIFAREReader.MFRC522_Read(B3S12)
                backData = MIFAREReader.MFRC522_Read(B3S12)

                La_date_Dernier_Passage = str(chr(backData[1]))+str(chr(backData[2]))+str(chr(backData[3]))+str(chr(backData[4]))+str(chr(backData[5]))+str(chr(backData[6])+str(chr(backData[7]))+str(chr(backData[8])))
                    ##print("La_date_Dernier_Passage ",La_date_Dernier_Passage)
                    #print("case 9 case 10",backData[9]+backData[10])
                Unite_CT=(str(int(backData[9])*256+int(backData[10])))
                Unite_CJ=(str(int(backData[11])))
                    
                if(int(backData[11]) <= Max_Seaux):
                    
                    #turnOn(GPIO_greenPin)
                            
                    print("Nombre seaux authorise",Seaux_MAX," par jour non-atteint",Unite_CJ)

                            #print("Max seaux par jour     : ",Seaux_MAX)
                            #print("Unitee(s) consommee(s) du jour :",Unite_CJ)
                            ##print("Unites consommees total : ",int(backData[9])*256+int(backData[10]))           
                    backDatacmpt = int(str(backData[9]))
                            ##print("\nbackDatacmpt",backDatacmpt)
                    Datacompteur = backDatacmpt +  1
                            ##print("\nDatacompteur",Datacompteur)
                    compteur = str(chr(Datacompteur))
                    La_date_du_jour = str_today
                            
                            ##La_date_Dernier_Passage = "20180431"
                            
                            ##print(str_today)
                            ##print("DADER",La_date_Dernier_Passage)
                    print("DAJOU",La_date_du_jour)
                            
                    if(La_date_Dernier_Passage != La_date_du_jour):
                        backDataNbr = int(str(backData[10]))
                        print("backDataNbr",backDataNbr)
                                ##DataNbr = 1
                                ##print("\nDataNbr",DataNbr)
                        Unite_CJ = 1
                        print("\nRemise du compteur à :",Unite_CJ)
                                ##Nbr = str(chr(DataNbr))
                        Unite_CT = (int(Unite_CT)+1)
                        print("Unitee(s) consommee(s) total   :",Unite_CT)
                                #print("Nbr Seaux Consommees dans la journee jour",Nbr)
                                #Nbr = 1
                        print(int(La_date_du_jour))
                                
                        Solde=Credit_C-Unite_CT
                        L1="Solde : "+str(Solde)
                        #Affichage
                        lcd_string(L1,LCD_LINE_1)
                        lcd_string("RECUPERER BALLES",LCD_LINE_2)
                        time.sleep(2)

                        super_date=stoday.strftime("%Y%m%d")
                                ##yoyo=ord(int((La_date_du_jour[:8])))
                        s = b"X" + super_date.encode() + (Unite_CT).to_bytes(2, byteorder='big') + (Unite_CJ).to_bytes(1, byteorder='big') + b"...."
                        print("s : ",hexdump.dump(s,sep=":"))
                              
                        MIFAREReader.MFRC522_Write(B3S12,s)
                        MIFAREReader.MFRC522_StopCrypto1()
                        declencher_relais()
                                
                    elif(La_date_Dernier_Passage == La_date_du_jour):
                        print("Date du dernier passage        :",La_date_Dernier_Passage)
                        backDataNbr = int(str(backData[10]))
                                ##print("\nLa_date_Dernier_Passage ",La_date_Dernier_Passage,"sont egaux a la date du jour",str_today)
                                ##print("backDataNbr",backDataNbr)
                        DataNbr = backDataNbr + 1
                                ##print("\nDataNbr",DataNbr)
                        Nbr = str(chr(DataNbr))
                                ##print("Nbr : ",int(ord(Nbr)))
                        Unite_CJ = (int(Unite_CJ)+1)
                        print("Unitee(s) consommee(s) du jour :",Unite_CJ)
                        Unite_CT = (int(Unite_CT)+1)
                        print("Unitee(s) consommee(s) total   :",Unite_CT)
                                
                        Solde=Credit_C-Unite_CT
                        L1="SOLDE : "+str(Solde)
                        #Affichage
                        lcd_string(L1,LCD_LINE_1)
                        lcd_string("RECUPERER BALLES",LCD_LINE_2)
                                
                            ##super_date=datetime.datetime.today().strftime("%Y%m%d")
                        super_date=stoday.strftime("%Y%m%d")

                        s = b"X" + super_date.encode() + (Unite_CT).to_bytes(2, byteorder='big') + (Unite_CJ).to_bytes(1, byteorder='big') + b"...."
                        print("s : ",hexdump.dump(s,sep=":"))
                                #if Ecriture == True:
                    
                        MIFAREReader.MFRC522_Write(B3S12,s)
        
                        declencher_relais()
                        
                else:
                    #turnOn(GPIO_redPin)
                    print("Nombre seaux authorise par jour atteint")
                    #Affichage
                    L1="NOMBRE SEAUX"
                    L2="PAR JOUR ATTEINT"
                    lcd_string(L1,LCD_LINE_1)
                    lcd_string(L2,LCD_LINE_2)
                    time.sleep(2)
                        
                 
                MIFAREReader.MFRC522_StopCrypto1()
                    
                #continue_reading = False
                    
                #nexto = False
            
            else:
                print("\nAuthentication error Avec la Clee Prive sur secteur",B3S12,"\n")
                #nexto =True
##        else:
##            print("La validite de votre carte est expire")
##            lcd_string("VALIDITE CARTE",LCD_LINE_1)
##            lcd_string("EXPIRE "+Date_LV_Out,LCD_LINE_2)
            
    #time.sleep(2)

except KeyboardInterrupt:
    lcd_byte(0x01,LCD_CMD)
    GPIO.cleanup()
