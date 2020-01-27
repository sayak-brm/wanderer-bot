#include <NewPing.h>
#include <Wire.h> #$$

#define US_MAX_DISTANCE 255
NewPing sonar1(5,  6,  US_MAX_DISTANCE);
NewPing sonar2(28, 26, US_MAX_DISTANCE);
NewPing sonar3(48, 46, US_MAX_DISTANCE);
byte sonar[3] = {0, 0, 0};

PROGMEM const byte us_highs[3] = {4, 30, 50};
PROGMEM const byte us_lows[3]  = {7, 24, 44};

#define SLAVE_ADDRESS 0x01

int  write_flag = -1;
byte write_data = -1;

// callback for received data
void receiveData(int n){
  /*
   * LOW          0x0
   * HIGH         0x1
   * ----------------
   * INPUT        0x0
   * OUTPUT       0x1
   * INPUT_PULLUP 0x2
  */
  Serial.print("Recv. bytes:");
  Serial.println(n);
  
  byte command[n] = {0}; n=0;
  while(Wire.available())
    command[n++] = Wire.read();
  
  switch(command[0]){
    case 0: //sonar req
      Serial.println("Recv. sonar request");
      write_flag = 0;
      break;

    case 1: //pinMode
      Serial.println("Recv. pinMode");
      Serial.print("Pin:");
      Serial.println((int) command[1]);

      switch(command[2]){
        case 0: // INPUT
          pinMode((int) command[1], INPUT);
          Serial.println("Setting INPUT");
          break;
        case 1: //OUTPUT
          pinMode((int) command[1], OUTPUT);
          Serial.println("Setting OUTPUT");
          break;
        case 2: //INPUT_PULLUP
          pinMode((int) command[1], INPUT_PULLUP);
          Serial.println("Setting INPUT_PULLUP");
          break;
      }
      break;

    case 2: //digitalWrite
      Serial.println("Recv. digitalWrite");
      Serial.print("Pin:");
      Serial.println((int) command[1]);

      switch(command[2]){
        case 0: //INPUT_PULLUP
          digitalWrite((int) command[1], LOW);
          Serial.println("Setting LOW");
          break;
        case 1: //INPUT_PULLUP
          digitalWrite((int) command[1], HIGH);
          Serial.println("Setting HIGH");
          break;
      }
      break;

    case 3: //digitalRead
      Serial.println("Recv. digitalRead");
      Serial.print("Pin:");
      Serial.println((int) command[1]);
      write_flag = 1;
      write_data = command[1];
      break;

    case 4: //analogWrite
      Serial.println("Recv. analogWrite");
      Serial.print("Pin:");
      Serial.println((int) command[1]);
      Serial.print("Level:");
      Serial.println((int) command[2]);
      analogWrite((int) command[1], (int) command[2]);
      break;

    case 5: //analogRead
      Serial.println("Recv. analogRead");
      Serial.print("Pin:");
      Serial.println((int) command[1]);
      write_flag = 2;
      write_data = command[1];
      break;
  }
}

// callback for sending data
void sendData(){
  Serial.println("Recv. data request");
  int reading = 0;
  switch(write_flag){
    case 0: //init, sonar data
      Wire.write(sonar, 3);
      Serial.println("Sonar data transmitted");
      break;

    case 1: //digitalRead
      reading = digitalRead((int) write_data);
      Wire.write(reading);
      Serial.println("Digital data transmitted");
      Serial.print("Value:");
      Serial.println(reading);
      break;

    case 2: //analogRead
      reading = analogRead((int) write_data);
      Wire.write(highByte(reading));
      Wire.write( lowByte(reading));
      Serial.println("Analog data transmitted");
      Serial.print("Value:");
      Serial.println(reading);
      break;
  }
  write_flag = -1;
}

void setup() {
  Serial.begin(9600); // start serial for output
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);
  
  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  
  for(byte i=0; i<3; i++){
    pinMode(us_lows[i],  OUTPUT);
    pinMode(us_highs[i], OUTPUT);
  }
  
  for(byte i=0; i<3; i++)
    digitalWrite(us_highs[i], HIGH);

  for(byte i=0; i<3; i++)
    digitalWrite(us_lows[i], LOW);

  Serial.println("Ready!");
}

void loop(){
  sonar[0] = lowByte(sonar1.convert_cm(sonar1.ping_median()));
  sonar[1] = lowByte(sonar2.convert_cm(sonar2.ping_median()));
  sonar[2] = lowByte(sonar3.convert_cm(sonar3.ping_median()));
}
