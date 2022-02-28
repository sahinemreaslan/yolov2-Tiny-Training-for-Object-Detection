int in1 = 10;
int in2 = 11;
int in3 = 8;
int in4 = 9;
int e1 = 5;
int e2 = 6;
void setup() {
  Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(e1, OUTPUT);
  pinMode(e2, OUTPUT);
}
void Default()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}
void loop()
{
  // send data only when you receive data:
  analogWrite(e1, 200);
  analogWrite(e2, 200);
  if (Serial.available())
  {
    char value = Serial.read();
    delay(115);

    if (value == 'l')
    {
      digitalWrite(in1, HIGH);
      digitalWrite(in2, LOW);
      delay(1000);
    }
    else if(value == 'r')
    {
      digitalWrite(in3,HIGH);
      digitalWrite(in4,LOW);
      delay(1000);
    }
    Default();
  }
  delay(1000);
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
