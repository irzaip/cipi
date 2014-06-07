

// Learning Processing
// Daniel Shiffman
// http://www.learningprocessing.com
import se.goransson.qatja.messages.*;
import se.goransson.qatja.*;

int time;
int waitsend = 10;
Qatja client;

String broker = "192.168.32.47";
String message = ""; 
String sens1 = "";
String sens2 = "";
String sens3 = "";
String sens4 = "";
String nav1 = "";
String nav2 = "";
String nav3 = "";
String nav4 = "";
String stat1 = "";
String stat2 = "";
String stat3 = "";
String stat4 = "";
String warn1 = "";
String warn2 = "";
String typing = "";
String saved = "";

int DIRL = 0;
int DIRR = 0;
int PWML = 0;
int PWMR = 0;

int LPWML = 0;
int LPWMR = 0;

boolean comm_mqtt = false;
boolean comm_teleop = false;
boolean comm_sensor = false;
boolean comm_vision = false;
boolean comm_arm = false;
boolean comm_ext = false;
boolean comm_ros = false;
boolean comm_main = false;

boolean voice = false;

PImage img;
PFont f;

// Example 3-5: mousePressed and keyPressed
void setup() {
  time = millis();
  size(1024,780);
  //background(255);
  img = loadImage("cipi_CC.png");
  f = loadFont( "ArialMT-16.vlw" );
  client = new Qatja( this );
  client.connect( broker, 1883, "irqwan" );
  comm_mqtt = true;
}

void mqttCallback(MQTTPublish msg){}


void draw() {
 // Nothing happens in draw() in this example!
  //background(255);
  //textFont(f,16); // Step 4: Specify font to be used
  //fill(0);        // Step 5: Specify font color
  image(img,0,0);
  // Step 6: Display Text
  fill(200,200,200);
  textFont(f,20);
  text ( sens1 ,54,140); 
  text ( sens2 ,54,165);
  text ( sens3 ,54,190);
  text ( sens4 ,54,215);
  
  text ( nav1 , 54,315);
  text ( nav2 , 54,340);
  text ( nav3 , 54,365);
  text ( nav4 , 54,390);

  text ( stat1, 54,485);
  text ( stat2, 54,510);
  text ( stat3, 54,535);
  text ( stat4, 54,560);  

  textFont(f,14);
  text (typing, 54, 623);
  text (saved, 54, 655);

  textFont(f,20);
  fill(200,0,0);
  text ( warn1, 520, 693);
  text ( warn2, 520, 716);
  
  if (comm_mqtt){fill(0,200,0);rect(880,120,80,32);fill(200,0,0);}
  rect(880,200,80,32);
  rect(880,280,80,32);
  rect(880,360,80,32);
  rect(880,440,80,32);
  rect(880,517,80,32);
  rect(880,597,80,32);
  rect(880,677,80,32);
}

// Whenever a user clicks the mouse the code written inside mousePressed() is executed.
void mousePressed() {
}

void reconnect(){
  comm_mqtt = false;
  client.disconnect();
  client = new Qatja( this );
  client.connect( broker, 1883, "irqwan" );
  client.publish("speak","reconnect");
  comm_mqtt = true;

 }


void sendpub(){
  message = str(DIRL)+":"+str(DIRR)+":"+str(PWML)+":"+str(PWMR)+":#";
  if(millis() - time >= waitsend){
    client.publish( "teleop", message );
    time = millis();}
}

// Whenever a user presses a key the code written inside keyPressed() is executed.
void keyPressed() {
  if (voice){
    if (key == '\n'){
      saved = typing;
      client.publish( "speak", typing );
      typing = "";
      voice = false;
      stat1 = "";
      stat2 = "";
    } else {
      typing = typing + key;
    }
  }
  else {
  if (key == '1') { nav1 = "SPEED 10%"; LPWML=10;LPWMR=10;}
  if (key == '2') { nav1 = "SPEED 20%"; LPWML=20;LPWMR=20;}
  if (key == '3') { nav1 = "SPEED 30%"; LPWML=25;LPWMR=25;}
  if (key == '4') { nav1 = "SPEED 40%"; LPWML=30;LPWMR=30;}
  if (key == '5') { nav1 = "SPEED 50%"; LPWML=35;LPWMR=35;}
  if (key == '6') { nav1 = "SPEED 60%"; LPWML=40;LPWMR=40;}
  if (key == '7') { nav1 = "SPEED 70%"; LPWML=50;LPWMR=50;}
  if (key == '8') { nav1 = "SPEED 80%"; LPWML=80;LPWMR=80;}
  if (key == '9') { nav1 = "SPEED 90%"; LPWML=90;LPWMR=90;}
  if (key == '0') { nav1 = "SPEED 100%"; LPWML=100;LPWMR=100;}
  if (key == ' ') { PWML=0;PWMR=0;nav2="STOPPED";}
  if (key == '.') { client.publish("sound","rnd");}
  if (key == 'p') { client.publish("speak","pong");}
  if (key == 'm') { client.publish("speak","music start");}
  if (key == ',') { client.publish("speak","music stop");}
  if (key == 'r') { reconnect();}
  if (keyCode == ENTER) { stat1 = "VOICE MODE"; stat2 = "please type"; voice = true; }
  if (key == 'q') { exit(); }

  if (key == CODED){
    if (keyCode == UP) { nav2 = "MOVE FORWARD"; DIRL=0; DIRR=0;PWML=LPWML;PWMR=LPWMR;sendpub();}
    if (keyCode == DOWN) { nav2 = "MOVE BACKWARD"; DIRL=1; DIRR=1;PWML=LPWML;PWMR=LPWMR;sendpub();}
    if (keyCode == LEFT) {nav2 = "TURN LEFT"; DIRL=0; DIRR=1;PWML=LPWML;PWMR=LPWMR;sendpub();}
    if (keyCode == RIGHT) {nav2 = "TURN RIGHT"; DIRL=1; DIRR=0;PWML=LPWML;PWMR=LPWMR;sendpub();}
  }}
}

void keyReleased(){
  if (key == CODED){
    if (keyCode == UP) {LPWML=PWML;LPWMR=PWMR;PWML=0;PWMR=0;nav2="STOPPED";sendpub();}
    if (keyCode == DOWN) {LPWML=PWML;LPWMR=PWMR;PWML=0;PWMR=0;nav2="STOPPED";sendpub();}
    if (keyCode == LEFT) {LPWML=PWML;LPWMR=PWMR;PWML=0;PWMR=0;nav2="STOPPED";sendpub();}
    if (keyCode == RIGHT) {LPWML=PWML;LPWMR=PWMR;PWML=0;PWMR=0;nav2="STOPPED";sendpub();}
}}

void exit() {
  client.disconnect();
  super.exit();
}

