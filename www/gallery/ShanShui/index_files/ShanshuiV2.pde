/* @pjs font="STXINGKA.ttf"; */
/* @pjs preload="mountain.png,bird.png,bamboo.png,boat.png,moutain_far.png,sunset.png,pine.png,tower.png,waterfall.png,forest.png"; */
import rita.*;
String WuyanGrammar =
"{\"<start>\": \"<A>|<B>|<C>|<D>\","

+ "\"<A>\": \"<zz_pp_z>%<pp_zz_p>%<pp_p_zz>%<zz_z_pp>|<zz_pp_z>%<pp_zz_p>%<pp_pz_z>%<zz_zp_p>|<zz_p_pz>%<pp_z_zp>%<pp_p_zz>%<zz_z_pp>|<zz_p_pz>%<pp_z_zp>%<pp_pz_z>%<zz_zp_p>\","
+ "\"<B>\": \"<zz_zp_p>%<pp_zz_p>%<pp_p_zz>%<zz_z_pp>|<zz_zp_p>%<pp_zz_p>%<pp_pz_z>%<zz_zp_p>|<zz_z_pp>%<pp_z_zp>%<pp_p_zz>%<zz_z_pp>|<zz_z_pp>%<pp_z_zp>%<pp_pz_z>%<zz_zp_p>\","
+ "\"<C>\": \"<pp_pz_z>%<zz_zp_p>%<zz_pp_z>%<pp_zz_p>|<pp_pz_z>%<zz_zp_p>%<zz_p_pz>%<pp_z_zp>|<pp_p_zz>%<zz_z_pp>%<zz_p_pz>%<pp_z_zp>|<pp_p_zz>%<zz_z_pp>%<zz_pp_z>%<pp_zz_p>\","
+ "\"<D>\": \"<pp_zz_p>%<zz_zp_p>%<zz_pp_z>%<pp_zz_p>|<pp_zz_p>%<zz_zp_p>%<zz_p_pz>%<pp_z_zp>|<pp_z_zp>%<zz_z_pp>%<zz_p_pz>%<pp_z_zp>|<pp_z_zp>%<zz_z_pp>%<zz_pp_z>%<pp_zz_p>\","

+ "\"<zz_pp_z>\": \"<zz>#<pp>#<z>\","
+ "\"<zz_p_pz>\": \"<zz>#<p>#<pz>\","

+ "\"<pp_zz_p>\": \"<pp>#<zz>#<p>\","
+ "\"<pp_z_zp>\": \"<pp>#<z>#<zp>\","

+ "\"<pp_p_zz>\": \"<pp>#<p>#<zz>\","
+ "\"<pp_pz_z>\": \"<pp>#<pz>#<z>\","

+ "\"<zz_z_pp>\": \"<zz>#<z>#<pp>\","
+ "\"<zz_zp_p>\": \"<zz>#<zp>#<p>\","

+ "\"<p>\": \"清#clear|佳#good|倾#lean|花#flower|惊#shock|还#come back\","
+ "\"<zp>\": \"月出#moon comes out|墨竹#bamboo|夏荷#lotus|桂花#osmanthus fragrans|小桥#little bridge\","
+ "\"<pp>\": \"空山#empty mountain|春山#mountain|深林#forest|清泉#spring water|枯藤#dried wine|松间#pines|青苔#moss|白石#stone|渔舟#boat\","

+ "\"<zz>\": \"夜静#silent night|日暮#sunset|返影#shadow|流水#flowing water|老树#old tree|古道#old street\","
+ "\"<z>\": \"上#up|后#back|塔#tower|落#drop|遍#spread\","
+ "\"<pz>\": \"春涧#gully|山鸟#mountain birds|新雨#rain|石上#above the stone|红叶#red leaves|烟渚#foggy islet|飞鸟#flying birds\"}";

RiGrammar grammar;
String[][] chchara= new String[4][3];
String[][] engchara= new String[4][3];
RiPhrase[][] phrase=new RiPhrase[4][3];
RiText trans;
int ydis=33;
boolean over;
int nopicktime=0;
float transparency=255;
float transpeed=0;
int counter=0;
PImage op1, op2;
int open=0;

RiText[] openchara= new RiText[3];//lines directly from grammar
String now;
String later;
PFont myfont;
PImage[] images=new PImage[12];
int[] opacity=new int[images.length];

void setup()
{
  size(1000, 440);
  frameRate(60);
  myfont=createFont("STXINGKA.ttf", 32);
  textFont(myfont);
  RiText.defaultFont(myfont);
  RiText.defaults.alignment = CENTER;
  RiText.defaultFill(50);

  //opening
  openchara[0] = new RiText(this, "Shan Shui", width / 2, height/2-35);
  openchara[1] = new RiText(this, "山水 ", width / 2, height/2);
  openchara[2] = new RiText(this, "Click", width / 2, height/2+45);

  //poetry
  grammar = new RiGrammar(WuyanGrammar);
  trans= new RiText(this, "", 0, 0);

  //painting
  images[0]= loadImage("mountain.png");
  images[1]= loadImage("bird.png");
  images[2]= loadImage("bamboo.png");
  images[3]= loadImage("boat.png");
  images[4]= loadImage("moutain_far.png");
  images[5]= loadImage("sunset.png");
  images[6]= loadImage("lotus.png");
  images[7]= loadImage("moon.png");
  images[8]= loadImage("pine.png");
  images[9]= loadImage("tower.png");
  images[10]= loadImage("waterfall.png");
  images[11]= loadImage("forest.png");
}

void draw()
{
  background(255);
  //painting
  pushMatrix();
  translate(0, 0);
  //near mountain
  tint(255, opacity[0]);
  image(images[0], 210, height-180);
  //far mountain
  tint(255, opacity[4]);
  image(images[4], 0, 0);
  //forest
  tint(255, opacity[11]);
  image(images[11], 0, 0);
  //pine
  tint(255, opacity[8]);
  image(images[8], width-270, 220);
  //waterfall
  tint(255, opacity[10]);
  image(images[10], width/2+20, 70);
  //tower
  tint(255, opacity[9]);
  image(images[9], 290, 10);
  //bamboo
  tint(255, opacity[2]);
  image(images[2], 0, 60);
  //lotus
  tint(255, opacity[6]);
  image(images[6], 0, 160);
  //boat
  tint(255, opacity[3]);
  image(images[3], width/2, height-140);
  //bird
  tint(255, opacity[1]);
  image(images[1], 300, height/2-130);
  //sunset
  tint(255, opacity[5]);
  image(images[5], 100, 0);
  //moon
  tint(255, opacity[7]);
  image(images[7], 150, 0);
  popMatrix();

  //poetry
  if (counter!=0) {
    for (int j = 0; j<phrase.length; j++)
      for (int i = 0; i <phrase[j].length; i++)
      {
        phrase[j][i].childOffsetY(ydis);
        phrase[j][i].draw();
        over = phrase[j][i].contains(mouseX, mouseY);
        if (over) {
          phrase[j][i].fadeIn(0.4);
          trans.text(phrase[j][i].translation).fadeIn(0.4, 0);
          trans.x=phrase[j][i].parent.x-20;
          trans.y=phrase[j][i].parent.y;
          trans.align(RIGHT).draw();
        }
        else
        {
          phrase[j][i].fadeOut(0.4);
        }
      }
    if (!anypicked(phrase)) { // nothing
        fadeInAll();
        trans.fadeOut(0.4, 0, true);
    }
  }
  //canvas

  //folding effect
  fill(255, transparency);
  transparency-=transpeed;
  // tint(255, transparency);
  noStroke();
  rect(0, 0, width, height);

  //opening
  for (int k = 0; k < openchara.length; k++)
  {
    openchara[k].draw();
    if (open==1)
      openchara[k].fadeOut(0.3, 0.1, true);
      transpeed=2;
  }
}


void mouseClicked()
{

  //tricky fadeIn+Out

  counter++;
  //opening
  if (counter==1)
  {
    open=1;
  }

  //generate poetry
  do {
    String result = grammar.expand();
    String[] lines = result.split("%");
    for (int j=0;j<chchara.length;j++)
    {
      String[] line=lines[j].split("#");
      for (int i=0;i<chchara[j].length;i++) {
        chchara[j][i]=line[2*i];//0,2,4
        engchara[j][i]=line[2*i+1];//1,3,5
      }
    }
  }
  while (checkrepetition (chchara));

  //Painting
  for (int i=0;i<images.length;i++) {
    opacity[i]=0;
  }
  //Create RiPhrase
  for (int j=0;j<phrase.length;j++)
  {
    for (int i=0;i<phrase[j].length;i++) {//0,1,2
      if (chchara[j][i].length()>1) {
        String chara1=chchara[j][i].substring(0, 1);
        String chara2=chchara[j][i].substring(1);
        if (phrase[j][i] == null)
          phrase[j][i] = new RiPhrase(this, chara1, chara2, engchara[j][i]);//1,3,5 English
        else
          phrase[j][i].setVariables(this, chara1, chara2, engchara[j][i]);
      }
      else {
        if (phrase[j][i] == null)
          phrase[j][i] = new RiPhrase(this, chchara[j][i], engchara[j][i]);
        else
          phrase[j][i].setVariables(this, chchara[j][i], null, engchara[j][i]);
      }
    }
  }
  /*
  for (int i=0;i<images.length;i++) {
   opacity[i]=255;
   }*/
  //IMG display
  for (int j=0;j<phrase.length;j++) {
    for (int i=0;i<phrase[j].length;i++)
    {
      if (engchara[j][i].equals("mountain"))
        opacity[0]=255;
      if (engchara[j][i].equals("mountain birds ")||engchara[j][i].equals("flying birds ") )
        opacity[1]=255;
      if (engchara[j][i].equals("bamboo"))
        opacity[2]=255;
      if (engchara[j][i].equals("boat"))
        opacity[3]=255;
      if (engchara[j][i].equals("empty mountain"))
        opacity[4]=255;
      if (engchara[j][i].equals("sunset"))
        opacity[5]=255;
      if (engchara[j][i].equals("lotus"))
        opacity[6]=255;
      if (engchara[j][i].equals("pines"))
        opacity[8]=255;
      if (engchara[j][i].equals("tower"))
        opacity[9]=255;
      if (engchara[j][i].equals("flowing water"))
        opacity[10]=255;
      if (engchara[j][i].equals("forest"))
        opacity[11]=255;
    }
  }
  // poem right position
  int xOff = width - 100, yOff;
  int change;
  for (int j = 0; j < phrase.length; j++) {
    if (j==0 || j==2) yOff = 50;
    else yOff=70;
    for (int i = 0; i < phrase[j].length; i++) {
      if (i!=0) {
        if (chchara[j][i-1].length()>1) change=ydis*2;
        else change=ydis;
      }
      else change=ydis;
      phrase[j][i].parent.x=xOff;
      phrase[j][i].parent.y=yOff +=change;
    }
    xOff -= 50;
  }
}

boolean checkrepetition(String[][] chchara) {
  boolean rep=false;
  for (int j=0;j<chchara.length;j++)
  {
    for (int i=0;i<chchara[j].length;i++)//0,1,2
    {
      now=chchara[j][i];
      for (int k=j;k<chchara.length;k++) {
        for (int h=i;h<chchara[k].length;h++)
        {

          if (h!=chchara[k].length-1)
          {
            later=chchara[k][h+1];
          }
          else if (h==chchara[k].length-1 && k!=chchara.length-1)
          {
            later=chchara[k+1][0];
          }
          else if (h==chchara[k].length-1 && k==chchara.length-1) later="";
          if (now.equals(later))
          {
            rep=true;
          }
        }
      }
    }
  }
  return rep;
}

boolean anypicked(RiPhrase[][] phrase)
{
  boolean anypicked=false;
  for (int j=0;j<phrase.length;j++) {
    for (int i=0;i<phrase[j].length;i++)
    {
      if (phrase[j][i].contains(mouseX, mouseY)) anypicked=true;
    }
  }
  return anypicked;
}

void fadeOutAll()
{
  for (int j = 0; j < phrase.length; j++)
    for (int i = 0; i < phrase[j].length; i++)

      phrase[j][i].fadeOut(0.8);
}

void fadeInAll()
{
  for (int j = 0; j <phrase.length; j++)
    for (int i = 0; i <phrase[j].length; i++)

      phrase[j][i].fadeIn(0.8);
}

class RiPhrase {

  RiText parent, child;
  String translation;

  RiPhrase(PApplet p, String c1, String trans)
  {
    this(p, c1, null, trans);
  }

  RiPhrase(PApplet p, String c1, String c2, String trans)
  {
    parent = new RiText(p, c1);
    if (c2 != null) {
      child = new RiText(p, c2);
    }
    translation = trans;
  }

  void setVariables(PApplet p, String c1, String c2, String trans)
  {
    parent.textTo(c1,1);
    if (c2 == null)
      child = null;
    else if (child == null)
      child = new RiText(p);
    if (child != null)
      child.textTo(c2,1);
    translation = trans;
  }

  void fadeIn(float alpha)
  {
    if (child != null)
      child.fadeIn(alpha);

    parent.fadeIn(alpha);
  }

  void fadeOut(float alpha)
  {
    if (child != null)
      child.fadeOut(alpha);
      parent.fadeOut(alpha);
  }

    void alpha(float alpha)
  {
    if (child != null)
      child.alpha(alpha);

    parent.alpha(alpha);
  }

  boolean contains(float mx, float my)
  {
    if (child == null) return parent.contains(mx, my);
    return parent.contains(mx, my) || child.contains(mx, my);
  }

  void childOffsetY(float yOff)
  {
    if (child != null)
      child.y = parent.y + yOff;
  }

  void draw()
  {
    parent.draw();
    if (child != null) {
      child.x = parent.x;
      child.draw();
    }
  }
}

