# include <Servo.h>
Servo myPan;
Servo myTilt;
int joyX = A0;
int joyY = A1;
int curPan = 0;
int curTilt = 180;
int xValue = 0; 
int yValue = 0; 

void setup() {
  myPan.attach(A5);
  myTilt.attach(A4);
  Serial.begin(9600);
}
 
void loop() {
  // put your main code here, to run repeatedly:
  xValue = analogRead(joyX);
  yValue = analogRead(joyY);
  xValue = map(xValue, 1, 1023, 1, 180); 
  yValue = map(yValue, 1, 1023, 1, 180); 

  if(xValue > 150 && curPan <175)
  {
    curPan += 5; 
  }
  if(xValue <10  && curPan > 0)
  {
    curPan -= 5; 
  }  
  if(yValue > 150 && curTilt <175)
  {
    curTilt += 5; 
  }
  if(yValue <10  && curTilt > 0)
  {
    curTilt -= 5; 
  }  
  myPan.write(curPan); 
  myTilt.write(curTilt);
  //print the values with to plot or view
  Serial.print(xValue);
  Serial.print("\t");
  Serial.println(yValue);
  Serial.print("\t");
  Serial.println(curPan);
  Serial.print("\t");
  Serial.println(curTilt);
  delay(100); 

}