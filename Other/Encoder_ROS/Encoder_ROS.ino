/* 
DC MOTOR CONTROL WITH ENCODER
Version: 1.0
Status : Working

Test with DFROBOT Motor Shield and Encoder LM393
compatible.

publish encoder every second to topic /rotation
subscribe PWM read to topic /motor

Timer Interupt Encoder on PIN D2 (for Data)


*/

#include <TimerOne.h>
#include <ros.h>
#include <std_msgs/Float32.h>
#include <std_msgs/UInt16.h>

std_msgs::UInt16 rpm_msg;
ros::Publisher pub_rpm("rotation", &rpm_msg);
ros::NodeHandle nh;

//setup for MOTOR (DFROBOT Motor Shield)
int E1 = 5;  
int M1 = 4; 
int E2 = 6;                      
int M2 = 7;  

void motor_cb( const std_msgs::UInt16& cmd_msg){
    analogWrite(E1, cmd_msg.data);   //PWM Speed Control
    analogWrite(E2, cmd_msg.data);   //PWM Speed Control
}
ros::Subscriber<std_msgs::UInt16> sub("motor", motor_cb);


unsigned int counter=0;
unsigned int rotation=0;

void docount()
{
  counter++;
}

void timerIsr()
{
  Timer1.detachInterrupt();
  //Serial.print("Motor Speed:");
  rotation = counter;
  //Serial.print(rotation,DEC);
  //Serial.println(" Rotation per seconds");
  rpm_msg.data=rotation;
  pub_rpm.publish(&rpm_msg);

  counter = 0;
  Timer1.attachInterrupt( timerIsr );
  
}


void setup() {
  // put your setup code here, to run once:
    //Serial.begin(9600);
    pinMode(M1, OUTPUT);   
    pinMode(M2, OUTPUT); 
    
    digitalWrite(M1,HIGH);   
    digitalWrite(M2, HIGH);       

 Timer1.initialize(1000000); // set timer for 1 sec
 attachInterrupt(0, docount, RISING);
 Timer1.attachInterrupt( timerIsr);

    nh.initNode();
    nh.advertise(pub_rpm);
    nh.subscribe(sub);
 
}

void loop() {
 
   nh.spinOnce();
   delay(1);
}
