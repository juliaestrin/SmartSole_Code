/* BLE Example for SparkFun Pro nRF52840 Mini 
 *  
 *  This example demonstrates how to use the Bluefruit
 *  library to both send and receive data to the
 *  nRF52840 via BLE.
 *  
 *  Using a BLE development app like Nordic's nRF Connect
 *  https://www.nordicsemi.com/eng/Products/Nordic-mobile-Apps/nRF-Connect-for-Mobile
 *  The BLE UART service can be written to to turn the
 *  on-board LED on/off, or read from to monitor the 
 *  status of the button.
 *  
 *  See the tutorial for more information:
 *  https://learn.sparkfun.com/tutorials/nrf52840-development-with-arduino-and-circuitpython#arduino-examples  
*/
#include <bluefruit.h>
#include <Arduino.h>
#include <C:\Users\julia\Documents\ArduinoData\packages\adafruit\hardware\nrf52\1.3.0\variants\sparkfun_nrf52840_mini\variant.h>

BLEUart bleuart; // uart over ble

int LED = PIN_D17; 
int BUTTON = PIN_D15;

int adc0 = A0; 
int adc1 = A1;
int adc2 = A2;
int adc3 = A3;
int adc4 = A4;
int adc5 = A5;
int adc6 = A6;
int adc7 = A7;

int adc0value = 0;
int adc1value = 0;
int adc2value = 0;
int adc3value = 0;
int adc4value = 0;
int adc5value = 0;
int adc6value = 0;
int adc7value = 0;

int i = 0; 
int divider = 11; 

const int buflen = 400; 

int adcbuffer[buflen][10];
char result[10]; 

unsigned long starttime; 
unsigned long currenttime[buflen]; 

bool startadc = LOW; 
bool ledsignal = LOW; 
int ButtonState;


// Define hardware: LED and Button pins and states
const int LED_PIN = 7;
#define LED_OFF LOW
#define LED_ON HIGH

const int BUTTON_PIN = 13;
#define BUTTON_ACTIVE LOW

int lastButtonState = -1;

void setup() {
  // Initialize hardware:
  Serial.begin(9600); // Serial is the USB serial port
  pinMode(LED_PIN, OUTPUT); // Turn on-board blue LED off
  digitalWrite(LED_PIN, LED_OFF);
  pinMode(BUTTON_PIN, INPUT);

  pinMode(LED, OUTPUT);
  pinMode(BUTTON, INPUT);

  digitalWrite(LED,LOW); 

  // Uncomment the code below to disable sharing
  // the connection LED on pin 7.
  //Bluefruit.autoConnLed(false);

  // Initialize Bluetooth:
  Bluefruit.begin();
  // Set max power. Accepted values are: -40, -30, -20, -16, -12, -8, -4, 0, 4
  Bluefruit.setTxPower(4);
  Bluefruit.Periph.setConnectCallback(connect_callback);
  Bluefruit.setName("SparkFun_nRF52840");
  bleuart.begin();
  bleuart.bufferTXD(true);


  // Start advertising device and bleuart services
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addService(bleuart);
  Bluefruit.ScanResponse.addName();
  
  Bluefruit.Advertising.restartOnDisconnect(true);
  // Set advertising interval (in unit of 0.625ms):
  Bluefruit.Advertising.setInterval(32, 244);
  //Bluefruit.Advertising.setInterval(7.5, 244); 
  // number of seconds in fast mode:
  Bluefruit.Advertising.setFastTimeout(30);
  
  Bluefruit.Advertising.start(0); 
}

void connect_callback(uint16_t conn_handle)
{
  BLEConnection* conn = Bluefruit.Connection(conn_handle);
  Serial.println("Connected");

  // request PHY changed to 2MB
  Serial.println("Request to change PHY");
  conn->requestPHY();

  // request to update data length
  Serial.println("Request to change Data Length");
  conn->requestDataLengthUpdate();
    
  // request mtu exchange
  Serial.println("Request to change MTU");
  conn->requestMtuExchange(247);

  Serial.println("DONE"); 
  // request connection interval of 7.5 ms
  //conn->requestConnectionParameter(6); // in unit of 1.25

  // delay a bit for all the request to complete
  //delay(1000);
  delay(100); 
}

void printBuffer(){
  //Serial.println("Send Buffer"); 
  for (int j = 0; j < i; j++){
    for (int h = 0; h < 10; h++){ 
     // Serial.println(adcbuffer[j][h]);
      if (h == 0){ 
         sprintf(result, "%d", adcbuffer[j][h]);
         //sprintf(result, "%d", h);
         bleuart.write(result); 
      }
      else if (h == 1){
         sprintf(result, "xx%d", currenttime[j]);
         //sprintf(result, "%d", h);
         bleuart.write(result); 
      }
      else {
        sprintf(result, "0%1d%4d", h - 2, adcbuffer[j][h]);  
        //sprintf(result, "%d", h);
        bleuart.write(result); 
      }
      bleuart.flushTXD();
    } 
  }
}

void startTest(){
  ButtonState = digitalRead(BUTTON); 
  //Serial.println(ButtonState); 
  // if (ButtonState == 0 && lastButtonState == 1 && startadc == 0){ 
  if (ButtonState == 1 && lastButtonState == 0 && startadc == 0){ 
    startadc = 1; 
    ledsignal = 1; 
    Serial.println("Reading Sensors"); 
    //bleuart.write("Test Starting"); 
    //bleuart.flushTXD(); 
  }
  lastButtonState = ButtonState;  
}



void loop() {
  
  //Serial.println(startadc); 
  //ButtonState = digitalRead(BUTTON); 
  //Serial.println(ButtonState); 

    if (startadc == 0){
      startTest(); 
    }

//    if (ledsignal == 1){
//      digitalWrite(LED,HIGH); 
//    }
//    else{
//      digitalWrite(LED, LOW); 
//    }
//  

  if (startadc == 1){
    digitalWrite(LED, HIGH); 
    //Serial.print("write to ADC"); 
    // Get a fresh ADC value
    adc0value = analogRead(adc0);
    adc1value = analogRead(adc1);
    adc2value = analogRead(adc2); 
    adc3value = analogRead(adc3);
    adc4value = analogRead(adc4); 
    adc5value = analogRead(adc5);
    adc6value = analogRead(adc6);
    adc7value = analogRead(adc7); 
    currenttime[i] = millis();
    // Serial.println(currenttime[i]);  
    
    adcbuffer[i][0] = divider; 
    adcbuffer[i][1] = 0;   
    adcbuffer[i][3]= adc1value; 
    adcbuffer[i][4]= adc2value;
    adcbuffer[i][5]= adc3value; 
    adcbuffer[i][6]= adc4value; 
    adcbuffer[i][7]= adc5value;
    adcbuffer[i][8]= adc6value; 
    adcbuffer[i][9]= adc7value; 
    
    i++;  
  
    if (i == (buflen)) {
      digitalWrite(LED, LOW); \
      Serial.println("Send Buffer"); 
      printBuffer();
      startadc = 0;
       
      i = 0; 
    }
    delay(30); 
  }
}
