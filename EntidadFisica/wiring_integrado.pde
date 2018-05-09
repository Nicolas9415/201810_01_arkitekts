#include <EEPROM.h>
#include <Keypad.h>
#define SIZE_BUFFER_DATA       50
boolean     stringComplete = false;
String      inputString = "";
char        bufferData [SIZE_BUFFER_DATA];

//Specified password
const String KEY = "5678";

//Time in milliseconds which the system is locked
const int LOCK_TIME = 30000;

//Keypad rows
const byte ROWS = 4; 

//Keypad columns
const byte COLS = 3;

//Maximum number of attempts allowed
const byte maxAttempts = 3;

//Button pin
const int CONTACT_PIN = 11;

//R LED pin
const int R_LED_PIN = 13;

//G LED pin
const int G_LED_PIN = 12;

//B LED pin
const int B_LED_PIN = 10;

int ledPin = 14;                // choose the pin for the LED
int inputPin = 2;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0; // variable for reading the pin status

//Door state
boolean open;

//Attribute that defines the button state
boolean buttonState;

//Current time when the button is tapped
long currTime;

//Number of current attempts
byte attempts;

//Minimum voltage required for an alert
const double MIN_VOLTAGE = 1.2;

//Battery measure pin
const int BATTERY_PIN = A0;

//Battery indicator
const int BATTERY_LED = 15;

//Current battery charge
double batteryCharge;

//Keypad mapping matrix
char hexaKeys[ROWS][COLS] = {
  {
    '1', '2', '3'
  }
  ,
  {
    '4', '5', '6'
  }
  ,
  {
    '7', '8', '9'
  }
  ,
  {
    '*', '0', '#'
  }
};

//Keypad row pins definition
byte rowPins[ROWS] = {
  9, 8, 7, 6
}; 

//Keypad column pins definition
byte colPins[COLS] = {
  5, 4, 3
};

//Keypad library initialization
Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

//Current key variable
String currentKey;
//If the number of current attempts exceeds the maximum allowed
boolean block;

void setup()
{
  Serial.begin(9600);
  buttonState = false;
  
  pinMode(R_LED_PIN, OUTPUT);
  pinMode(G_LED_PIN, OUTPUT);
  pinMode(B_LED_PIN, OUTPUT);
  pinMode(CONTACT_PIN,INPUT);
  
  setColor(0, 0, 255);
  
  currentKey = "";
  open = false;
  attempts = 0;
  block = false;
  
  pinMode(ledPin, OUTPUT);      // declare LED as output
  pinMode(inputPin, INPUT); // declare sensor as input
  
  // Ouput pin definition for BATTERY_LED
  pinMode(BATTERY_LED,OUTPUT);

  //Input pin definition for battery measure
  pinMode(BATTERY_PIN,INPUT);
}

void loop()
{
   //Button input read and processing 
  if(!buttonState) {
    if(digitalRead(CONTACT_PIN)) {
      currTime = millis();
      buttonState = true;
      setColor(0, 255, 0);
      open = true;
      attempts = 0;
      Serial.println("Door opened!!");
    }
  }
  else {
    if(digitalRead(CONTACT_PIN)) {
      if((millis()-currTime)>=5000) {
        setColor(255, 0, 0);
        Serial.println("Door opened for too long!");
      }
    }else{
      setColor(0, 0, 255);
      open = false;
      buttonState = false;
      Serial.println("Door closed!!");
    }
  }
  
  //Value conversion from digital to voltage
  batteryCharge = (analogRead(BATTERY_PIN)*5.4)/1024;
  
  //Measured value comparison with min voltage required
  if(batteryCharge<=MIN_VOLTAGE) {
    digitalWrite(BATTERY_LED,HIGH);
    Serial.println("LOW BATTERY");
  }
  else {
    digitalWrite(BATTERY_LED,LOW);
  }
  
  char customKey;

  if(!block) {
    //Selected key parsed;
    customKey = customKeypad.getKey();
  }
  else {
    Serial.println("Number of attempts exceeded");
    while(true);
  }

  //Verification of input and appended value
  if (customKey) {  
    currentKey+=String(customKey);
    Serial.println(currentKey);
  }

  //If the current key contains '*' and door is open
  if(open && currentKey.endsWith("*")) {
    open = false;
    Serial.println("Door closed");
    digitalWrite(10,LOW);
    setColor(0, 0, 255);
    currentKey = "";
  }
  //If the current key contains '#' reset attempt
  if(currentKey.endsWith("#")&&currentKey.length()<=KEY.length()) {
    currentKey = "";
    Serial.println("Attempt deleted");
  }

  //If current key matches the key length
  if (currentKey.length()== KEY.length()) {
    if(!open){
      currTime = millis();
    }
    if(currentKey == KEY) {
      digitalWrite(10,HIGH);
      open = true;
      setColor(0, 255, 0);
      attempts = 0;
      if((millis()-currTime)>=30000) {
        setColor(255, 0, 0);
        Serial.println("Door opened for too long!");
      }
      else{
        Serial.println("Door opened!!");
      }
    }
    else {
      attempts++;
      currentKey = "";
      setColor(255, 0, 0);
      delay(1000);
      setColor(0, 0, 255);
      Serial.println("Number of attempts: "+String(attempts));
    }
  }else if(currentKey.length()> KEY.length()){
    if((millis()-currTime)>=30000) {
        setColor(255, 0, 0);
        Serial.println("Door opened for too long!");
      }
      else{
        Serial.println("Door opened!!");
      }
  }
  if(attempts>=maxAttempts) {
    currentKey = "";
    attempts = 0;
    setColor(255, 0, 0);
    Serial.println("System locked");
    delay(LOCK_TIME);
    setColor(0, 0, 255);
    Serial.println("System unlocked");
  }
  
  val = digitalRead(inputPin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH
    digitalWrite(ledPin, HIGH);  // turn LED ON
    if (pirState == LOW) {
      // we have just turned on
      Serial.println("Motion detected!");
      // We only want to print on the output change, not state
      pirState = HIGH;
    }
  } else {
    digitalWrite(ledPin, LOW); // turn LED OFF
    if (pirState == HIGH){
      // we have just turned of
      Serial.println("Motion ended!");
      // We only want to print on the output change, not state
      pirState = LOW;
    }
  }
  
  receiveData();
  if (stringComplete){
      String cmd[4] = {"", "", ""};
      processCommand(cmd, inputString);
      if(cmd[1] == "DELETE_ALL"){
        deleteAllPasswords();
      }
      if(cmd[1] == "UPDATE_PASSWORD"){
        updatePassword(cmd[2].toInt(), cmd[3].toInt());
      }
      if(cmd[1] == "DELETE_PASSWORD"){
        deletePassword(cmd[1].toInt());
      }
      if(cmd[1] == "ADD_PASSWORD"){
        addPassword(cmd[2].toInt(), cmd[3].toInt());
      }
  }
  
  delay(100);
}

//Method that outputs the RGB specified color
void setColor(int redValue, int greenValue, int blueValue) {
  analogWrite(R_LED_PIN, redValue);
  analogWrite(G_LED_PIN, greenValue);
  analogWrite(B_LED_PIN, blueValue);
}

void receiveData() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      inputString.toCharArray(bufferData, SIZE_BUFFER_DATA);
      stringComplete = true;
      Serial.println("Se recibe");
      Serial.println(inputString);
    }
  }
}

// Method that compares a key with stored keys
boolean compareKey(String key) {
  int acc = 3;
  int codif, arg0, arg1; 
  for(int i=0; i<3; i++) {
    codif = EEPROM.read(i);
    while(codif!=0) {
      if(codif%2==1) {
        arg0 = EEPROM.read(acc);
        arg1 = EEPROM.read(acc+1)*256;
        arg1+= arg0;
        if(String(arg1)==key) {
          return true;
        }
      }
      acc+=2;
      codif>>=1;
    }
    acc=(i+1)*16+3;
  }
  return false;
}

// Methods that divides the command by parameters
void processCommand(String* result, String command) {
  char buf[sizeof(command)];
  String vars = "";
  vars.toCharArray(buf, sizeof(buf));
  char *p = buf;
  char *str;
  int i = 0;
  while ((str = strtok_r(p, ";", &p)) != NULL) {
    // delimiter is the semicolon
    result[i++] = str;
    Serial.println(str);
  }
}

//Method that adds a password in the specified index
void addPassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j |= i;
  EEPROM.write(location,j);
}

//Method that updates a password in the specified index
void updatePassword(int val, int index) {
  byte arg0 = val%256;
  byte arg1 = val/256;
  EEPROM.write((index*2)+3,arg0);
  EEPROM.write((index*2)+4,arg1);
}

//Method that deletes a password in the specified index
void deletePassword(int index) {
  byte i = 1;
  byte location = index/8;
  byte position = index%8;
  i<<=position;
  byte j = EEPROM.read(location);
  j ^= i;
  EEPROM.write(location,j);
}

//Method that deletes all passwords
void deleteAllPasswords() {
  //Password reference to inactive
  EEPROM.write(0,0);
  EEPROM.write(1,0);
  EEPROM.write(2,0);
}
