import processing.opengl.*;
import se.goransson.qatja.messages.*;
import se.goransson.qatja.*;

Qatja client;

/*---->>>
 Program: Joystick
 
 This program simulates using a joystick by using a mouse and
 the graphics features of Processing.
 
 Author: Vince Thompson
 
http://www.twitter.com/SomeoneKnows
 
<<<----*/
 
int displayWidth = 640;
int displayHeight = 480;
int joyOutputRange = 90;  //Maximum value for full horiz or vert position where centered is 0.
int textHorizPos, textVertPos;  //Display positions for text feedback values.
int fontSpace = 12;
 
float curJoyDisplayWidth;
float curJoyDisplayHeight;
 
float maxJoyRange=200;     //Maximum joystick range
float curJoyAngle;     //Current joystick angle
float curJoyRange;     //Current joystick range
float joyDisplayCenterX;  //Joystick displayed Center X
float joyDisplayCenterY;  //Joystick displayed Center Y
 
float surfDisplayCenterX;
float surfDisplayCenterY;

float rSize;
 
boolean isMouseTracking=false;
color color1;
color color2;
 
void setup() {
  PFont font;
  size(displayWidth, displayHeight, OPENGL);
  joyDisplayCenterX = displayWidth/2;
  joyDisplayCenterY = 25 + maxJoyRange/2;
  curJoyDisplayWidth = maxJoyRange * .85;
  curJoyDisplayHeight = curJoyDisplayWidth;
  maxJoyRange = curJoyDisplayWidth / 2;
 
  surfDisplayCenterX=displayWidth/2;
  surfDisplayCenterY=displayHeight* .65;
 
  smooth();
  strokeWeight(10.0);
  stroke(0, 100);
  color1=color(0);  //Color = Black
  color2=color(150);  
 
  rSize = displayWidth/2;
 
  //font = loadFont("Monospaced.bold-12.vlw");
  //textFont(font);
    client = new Qatja( this );
  
  // 2. Request a connection to a broker. The identification
  //    string at the end must be unique for that broker!
  client.connect( "192.168.30.95", 1883, "irqwan" );
  
}
 
void mqttCallback(MQTTPublish msg){}

void draw()
{
  float joyHorizontalText, joyVerticalText;
 
  background(226);
 
  float dx = mouseX - joyDisplayCenterX;
  float dy = mouseY - joyDisplayCenterY;
  
  if(mousePressed && (mouseButton == LEFT))
    isMouseTracking = true;
  else
    isMouseTracking = false;
    
  if(mousePressed && (mouseButton == RIGHT))
    isMouseTracking = false;

 
  if (isMouseTracking)
  {
    curJoyAngle = atan2(dy, dx);
    curJoyRange = dist(mouseX, mouseY, joyDisplayCenterX, joyDisplayCenterY);
    //String message = str(int(dx)) + "-" + str(int(dy));
    String message = "";
    if(dy < 0)
      if(dx>0)
        message = "1:1:" + str(abs(int(dy))) + ":" + str(int(100-dx))+":#";
      else
        message = "1:1:" + str(int(100-dx))+ ":" + str(abs(int(dy))) + ":" +":#";
    else
      if(dx>0)
        message = "0:0:" + str(abs(int(dy))) + ":" + str(int(100-dx))+":#";
      else
        message = "0:0:" + str(abs(int(dy))) + ":" + str(int(100-dx))+":#";
      

    client.publish( "teleop", message);

  }
  else
  {
    curJoyRange = 0;
  }
 
  fill(200);
  noStroke();
  ellipse(joyDisplayCenterX, joyDisplayCenterY, curJoyDisplayHeight, curJoyDisplayWidth);
 
  stroke(0,100);
  segment(joyDisplayCenterX, joyDisplayCenterY, curJoyAngle);
  ellipse(joyDisplayCenterX, joyDisplayCenterY, 20, 20);
 
  fill(160,0,0);
  textHorizPos = 50;
  textVertPos = (int)(joyDisplayCenterY - 50);
  text("Horiz:", textHorizPos, textVertPos);
  textHorizPos += (4*fontSpace);
  joyHorizontalText = (joyOutputRange*(cos(curJoyAngle) * curJoyRange)/ maxJoyRange);
  text(nf(joyHorizontalText, 2, 1), textHorizPos, textVertPos);
 
  textHorizPos = 50;
  textVertPos += 12;  
 
  text("Vert:", textHorizPos, textVertPos);
  textHorizPos += (4*fontSpace);
  joyVerticalText = (joyOutputRange*(-(sin(curJoyAngle) * curJoyRange)/maxJoyRange));
  text(nf(joyVerticalText, 2, 1), textHorizPos, textVertPos);
 
  labySurface(joyHorizontalText, joyVerticalText);
}
 
void segment(float x, float y, float a)
{
  pushMatrix();
  translate(x, y);
  rotate(a);
  if (curJoyRange > maxJoyRange)
    curJoyRange = maxJoyRange;
 
  line(0, 0, curJoyRange, 0);
  popMatrix();
}
 
void labySurface(float angleHoriz, float angleVert)
{
  float radHoriz;
  float radVert;
 
  radHoriz = radians(angleHoriz) * .15;
  radVert = radians(angleVert-60) * .15;
  noFill();
  stroke(200);
  pushMatrix();
  translate(surfDisplayCenterX, surfDisplayCenterY, 0);
  rotateX(HALF_PI+ (radians(-60) * .15));
  box(rSize+5, rSize+5, 1);
  popMatrix();
 
  pushMatrix();
  stroke(0);
  translate(surfDisplayCenterX, surfDisplayCenterY, 0);
  rotateX(HALF_PI+radVert);
  rotateY(radHoriz);
  fill(0,20,240);
  box(rSize, rSize, 8);
  popMatrix();
 
}

void exit() {
  client.disconnect();
  super.exit();
}
