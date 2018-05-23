import time
import RPi.GPIO as GPIO
import MFRC522
import smbus
import datetime

# relais
#GPIO_relais = 32 # le relais est branché sur la pin 32 / GPIO12
#GPIO.setmode(GPIO.BOARD) # comme la librairie MFRC522
#GPIO.setup(GPIO_relais, GPIO.OUT)

# Define some device parameters
##I2C_ADDR  = 0x3F #Afficheur de Xavier I2C device address, if any error, change this address to 0x3f
I2C_ADDR  = 0x3F
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

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

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

def declencher_relais():
    GPIO.output(GPIO_relais, GPIO.LOW)
    time.sleep(1)
    GPIO.output(GPIO_relais, GPIO.HIGH)    

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

# Initialise display
lcd_init()

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
 
# Welcome message
print("Looking for cards")
print("Press Ctrl-C to stop.")
 
# This loop checks for chips. If one is near it will get the UID
try:
   
  while True:
      
    # Date
    stoday = datetime.datetime.today()
    # Display Message
    lcd_string(stoday.strftime("%d-%m-%Y %H:%M"),LCD_LINE_1)
    lcd_string("Attente Carte",LCD_LINE_2)
    
    
    # Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        data = [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
        # Print UID
        #print ("UID de la carte : "+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])+"."+str(uid[4]))
        # This is the default key for authentication
        keyA_Public = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        # Clee d authentification privée
        keyA_Prive = [0x59,0x61,0x50,0x6F,0x54,0x74] #"YaPoTt"
         
        key =  [0x59,0x61,0x50,0x6F,0x54,0x74,0xFF,0x07,0x80,0x69,0x59,0x61,0x50,0x6F,0x54,0x74]
        #keyA_Prive = key
        #keyA_Public = key
        # Select the scanned tag
        
        MIFAREReader.MFRC522_SelectTag(uid)
         
        # Authenticate with private key

        #print("..............................BLOC 1.....................................")
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 4,keyA_Prive, uid)
        nom=""
        prenom=""
        societe=""
        if(status == MIFAREReader.MI_OK):        
                ##print ("Authentification Avec la Clee Prive ",keyA_Prive,"\n")
                ##print("Carte déja initialisé sur secteur ",4)
                try:        
                    
                    nom = MIFAREReader.MFRC522_Read(4)
                    prenom = MIFAREReader.MFRC522_Read(5)
                    societe = MIFAREReader.MFRC522_Read(6)
                    
                    ##print(nom[0],"\n")
                    nom_str=chr(nom[0])+chr(nom[1])+chr(nom[2])+chr(nom[3])+chr(nom[4])+chr(nom[5])+chr(nom[6])+chr(nom[7])+chr(nom[8])+chr(nom[9])+chr(nom[10])+chr(nom[11])+chr(nom[12])+chr(nom[13])+chr(nom[14])+chr(nom[15])
                    ##nom_str=nom_str.decode("utf-8")
                    #print(nom_str)
                    prenom_str=chr(prenom[0])+chr(prenom[1])+chr(prenom[2])+chr(prenom[3])+chr(prenom[4])+chr(prenom[5])+chr(prenom[6])+chr(prenom[7])+chr(prenom[8])+chr(prenom[9])+chr(prenom[10])+chr(prenom[11])+chr(prenom[12])+chr(prenom[13])+chr(prenom[14])+chr(prenom[15])
                    ##prenom_str=""
                    #print(prenom_str)
                    societe_str=chr(societe[0])+chr(societe[1])+chr(societe[2])+chr(societe[3])+chr(societe[4])+chr(societe[5])+chr(societe[6])+chr(societe[7])+chr(societe[8])+chr(societe[9])+chr(societe[10])+chr(societe[11])+chr(societe[12])+chr(societe[13])+chr(societe[14])+chr(societe[15])
                    ##societe_str=""
                    #print(societe_str)
                    ##print(decode_secteur_hex(nom))
                    ##print(binascii.unhexlify(nom[0]))
                    ##print(bytes.fromhex(nom[0].decode('utf-8')))
                    lcd_string(stoday.strftime("%d-%m-%Y %H:%M"),LCD_LINE_1)
                    lcd_string(nom_str,LCD_LINE_2)
                    time.sleep(1)
                    lcd_string(prenom_str,LCD_LINE_2)
                    time.sleep(1)
                    lcd_string(societe_str,LCD_LINE_2)
                    GPIO.cleanup()
                except:
                    print("\nErreur Lecture  sur secteur ",4,"\n")
                    #GPIO.cleanup()



      # Déclencher relais
      #  declencher_relais()

      # Attendre 2 secondes
        time.sleep(1)
        GPIO.cleanup()
 
except KeyboardInterrupt:
    lcd_string("MACHINE ARRETEE",LCD_LINE_1)
    lcd_string("ESSAYEZ + TARD",LCD_LINE_2)
    GPIO.cleanup()