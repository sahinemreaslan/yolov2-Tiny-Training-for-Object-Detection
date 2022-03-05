#include <Servo.h>
Servo myServo;
int in1 = 9;
int in2 = 10;
int in3 = 7;
int in4 = 8;
int e1 = 5;
int e2 = 6;
char dizi[100];
bool targetFound = false;
int i = 0;
int sayac = 0;
void setup() {
  Serial.begin(115200); // opens serial port, sets data rate to 9600 bps
  pinMode(in1, OUTPUT); 
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(e1, OUTPUT);
  pinMode(e2, OUTPUT);
  pinMode(13, OUTPUT);
  myServo.attach(11);
}
void Wait()
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
void BackTurnLeft()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
}
void TurnRight()
{
  digitalWrite(in3,HIGH);
  digitalWrite(in4,LOW);
}
void BackTurnRight()
{
  digitalWrite(in3,LOW);
  digitalWrite(in4,HIGH);
}
void Forward()
{
  digitalWrite(in4,LOW);
  digitalWrite(in3,HIGH);
  digitalWrite(in2,LOW);
  digitalWrite(in1,HIGH);
}
void Backward()
{
    digitalWrite(in3,LOW);
    digitalWrite(in4,HIGH);
    digitalWrite(in1,LOW);
    digitalWrite(in2,HIGH);
}
void StartingPoint()
{
  for(int i = sayac;i>0;i--)
  {
    Serial.println(sayac);
    if(dizi[i] == 'r')
    {
      BackTurnRight();
    }
    else if(dizi[i] =='l')
    {
      BackTurnLeft();
    }
    else if(dizi[i] == 'f')
    {
      Backward();
    }
    delay(100);
  }
}
void SearchObject()
{
  for(int i = 0; i < 180;i+= 60)
  {
    myServo.write(i);
    delay(2000);
    if(Serial.available())
    {
      targetFound = true;
      // Aracın konumu kameranın konumuna göre ayarlanacaktır..
      break;
    }
  }
}
void Go(char value)
{
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
      Forward();
    }
    else if(value == 'b')//turn back
    {
      Backward();
    }
    else if(value == 'a')
    {
      StartingPoint();
    }
    else if(value == 'z')
    {
      BackTurnRight();
    }
    else
    {
      Wait();
    }
}
void DcMotorSettings()
{
  analogWrite(e1, 95);//95 ---> right wheel
  analogWrite(e2, 90);//90  ---> left wheel
}
void loop()
{
  DcMotorSettings();
  if (Serial.available())// a data in buffer
  {
    char value = Serial.read();
    dizi[sayac] = value;
    delay(115);
    Go(value);
    if(value == 'a') sayac = 0;//Starting point için a değeri geldiğinde onu sıfırlamak için kullanılıyor
    if(value == 'r' || value == 'l' || value == 'f' || value == 'b') sayac++;//Starting Point için tutulan verileri topluyor
    if(value == 'f' || value =='b')//İki motor aynı anda döndüğü için tek motora düşen hız 50 iki motora toplamda 100 hız düşüyor
    {
      delay(50); 
      //break;
    }
    else
    {
      delay(100);
    }
  }
  else if(targetFound == false)// veri gelmiyo ve targetFound == false
  {
    SearchObject();//Bu bloğa tek kere girmesi için
  }
}
  /*
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
  
    delayMicroseconds(2000); //Set the possition to 180 degrees
  }
  }
*/
