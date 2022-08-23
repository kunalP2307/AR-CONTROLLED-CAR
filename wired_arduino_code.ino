String arrivingdatabyte;
int forward = 9;
int backward = 8;
int right = 7;
int left = 6;
void setup()
{
    Serial.begin(9600);

    pinMode(forward, OUTPUT);
    pinMode(backward, OUTPUT);
    pinMode(right, OUTPUT);
    pinMode(left, OUTPUT);
}
void loop()
{
    if (Serial.available() > 0)
    {
        arrivingdatabyte = Serial.readStringUntil('\n');
        if (arrivingdatabyte == "FORWARD GO STRAIGHT")
        {
            digitalWrite(forward, HIGH);
            digitalWrite(backward, LOW);
            digitalWrite(right, LOW);
            digitalWrite(left, LOW);
        }
        else if (arrivingdatabyte == "FORWARD GO LEFT")
        {
            digitalWrite(forward, HIGH);
            digitalWrite(backward, LOW);
            digitalWrite(right, LOW);
            digitalWrite(left, HIGH);
        }
        else if (arrivingdatabyte == "FORWARD GO RIGHT")
        {
            digitalWrite(forward, HIGH);
            digitalWrite(backward, LOW);
            digitalWrite(right, HIGH);
            digitalWrite(left, LOW);
        }

        else if (arrivingdatabyte == "REVERSE GO STRAIGHT")
        {
            digitalWrite(forward, LOW);
            digitalWrite(backward, HIGH);
            digitalWrite(right, LOW);
            digitalWrite(left, LOW);
        }
        else if (arrivingdatabyte == "FORWARD GO LEFT")
        {
            digitalWrite(forward, LOW);
            digitalWrite(backward, HIGH);
            digitalWrite(right, LOW);
            digitalWrite(left, HIGH);
        }
        else if (arrivingdatabyte == "FORWARD GO RIGHT")
        {
            digitalWrite(forward, LOW);
            digitalWrite(backward, HIGH);
            digitalWrite(right, HIGH);
            digitalWrite(left, LOW);
        }
    

        else if (arrivingdatabyte == "STOP")
        {
            digitalWrite(forward, LOW);
            digitalWrite(backward, LOW);
            digitalWrite(right, LOW);
            digitalWrite(left, LOW);
        }
    }
}