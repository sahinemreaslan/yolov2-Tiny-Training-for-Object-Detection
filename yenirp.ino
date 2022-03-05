#include <Servo.h>
Servo myServo;
int in1 = 9;
int in2 = 10;
int in3 = 7;
int in4 = 8;
int e1 = 5;
int e2 = 6;
int servo1v = 12;
int position = 0;
void setup() {
  Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(e1, OUTPUT);
  pinMode(e2, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(servo1v, OUTPUT);
  myServo.attach(11);
  myServo.write(0);
}
void Default()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void TurnLeft()
{
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
}
void TurnRight()
{
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
}

void loop()
{
  //digitalWrite(servo1v, HIGH);
  // send data only when you receive data:
  digitalWrite(13,LOW);
  digitalWrite(servo1v, HIGH);
  analogWrite(e1, 85);//80
  analogWrite(e2, 90);//90
  if (Serial.available())
  {
    char value = Serial.read();
    delay(115);

    if (value == 'l')
    {
      TurnLeft();
    }
    else if(value == 'r')
    {
      TurnRight();
    }
    else if(value == 'f')//front back
    {
      digitalWrite(in4,LOW);
      digitalWrite(in3,HIGH);
      digitalWrite(in2,LOW);
      digitalWrite(in1,HIGH);
    }
    else if(value == 'b')//turn back
    {
      digitalWrite(in3,LOW);
      digitalWrite(in4,HIGH);
      digitalWrite(in1,LOW);
      digitalWrite(in2,HIGH);
    }
    else if(value == 's')
    {
      //position += 60;
      myServo.write(90);
      delay(1000);
      myServo.write();
      delay(1000);
      myServo.write(0);
      //nesneyi tespit ederse 
        //break et
    }
    else
    {
      Default();
    }

    delay(100);
  }
}
  /*
    else if()
    {
    Serial.println("emre");
    digitalWrite(in3,HIGH);
    digitalWrite(in4,LOW);
    }
    else
    {
    Serial.println("emre");
    digitalWrite(in1,LOW);
    digitalWrite(in2,LOW);
    digitalWrite(in3,LOW);
    digitalWrite(in4,LOW);
    }

}
void serialEvent()
{
  while (Serial.available())
  {
    char gelen = char(Serial.read());
    veri += gelen;
    if (gelen == '\n')
    {
      durum = true;
    }
  }
}
/*
   int servo = 14;

  void setup() {

  pinMode(servo, OUTPUT); //OUTPUT setup

  for ( int i = 0; i > 5; i++){ // Set the possition to 90 degrees
   digitalWrite(servo, HIGH);
    delayMicroseconds(1500);
    digitalWrite(servo, LOW);
  }
  delay(2000);
  }


  void loop() {
  for ( int i = 0; i > 50; i++){
    digitalWrite(servo, HIGH);
    delayMicroseconds(1000); // Set the possition to 0 degrees
    digitalWrite(servo, LOW);
    delay(19);
  }
  for ( int i = 0; i > 50; i++){
    digitalWrite(servo, HIGH);
    delayMicroseconds(2000); //Set the possition to 180 degrees
    digitalWrite(servo, LOW);
    delay(18);
  }
  }
*/
