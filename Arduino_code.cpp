String cmd;
int led = 9;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(led, OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  cmd = Serial.readStringUntil('\n');
  Serial.print(cmd);
  if (cmd == "ReverseGoLeft")
  {
    digitalWrite(led, HIGH);
    delay(1000);
  }
  else if(cmd == "ForwardGoLeft")
  {
    //Code For Forward Go Left
  }
   else if(cmd == "ReverseGoRight")
  {
    //Code For Reverse Go Right
  }
   else if(cmd == "ForwardGoRight")
  {
        //Code For Forward Go Right
  }
   else if(cmd == "ReverseGoStraight")
  {
    //Code For Reverse Go Straight
  }
   else if(cmd == "ForwardGoStraight")
  {
    //Code For Forward Go Straight
  }
  digitalWrite(led, LOW);
  delay(1000);
}