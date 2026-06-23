let font, grammar, grammarSd, grammarFw, lines = [4],
  jsonText, jsonSd, jsonFw, result, sd = [10],
  chineseV, wordsAddOn = [],
  flowAddOn = [],
  verLine = [],
  storeForPush, backgroundImage, songFin = true,
  songStartTime = 0,
  addTime = 0,
  wordInfo = [],
  appearEng = false,
  storeTimeDot = [],
  startText = true,
  createP,
  songA;

function preload() {
  font = loadFont('chineseWriting.otf');
  jsonText = loadStrings('poetryText.json');
  jsonSd = loadStrings("sound.json");
  jsonFw = loadStrings("sound.json");
  backgroundImage = loadImage('chunye.jpg');
  createPo = loadImage('createP.png');
  songA= loadImage('songAgain.png');
  sd[0] = loadSound('do.m4a');
  sd[1] = loadSound('re.wav');
  sd[2] = loadSound('mi.wav');
  sd[3] = loadSound('so.wav');
  sd[4] = loadSound('la.wav');
  sd[5] = loadSound('do2.wav');
  sd[6] = loadSound('re2.wav');
  sd[7] = loadSound('mi2.wav');
  sd[8] = loadSound('so2.wav');
  sd[9] = loadSound('la2.wav');
}

function setup() {

  createCanvas(800, 640);
  textSize(30);
  textAlign(LEFT);
  textFont(font);

  grammar = new RiGrammar(jsonText.join('\n'));
  grammarSd = new RiGrammar(jsonSd.join('\n'));
  grammarFw = new RiGrammar(jsonFw.join('\n'));

  lines = ["", "", "", ""];
  verLine = [];

  //a array of objects hold information of words
  for (i = 0; i < 16; i++) {
    wordInfo[i] = new wordInformation();
  }


  //for the dot for melody
  for (i = 0; i < 20; i++) {
    storeTimeDot[i] = 0;
  }

}

function draw() {

  background(220, 220, 220);
  image(backgroundImage, 0, 0, 800, 640);
  noStroke();
  fill(0, 0, 0, 200);


  if (songFin == true) {
    textAlign(CENTER);
    textSize(29);
    text("拍案叫絶", 500, 425);
    text("regenerate", 500, 450);
    if(startText==false){
    text("放歌縱酒",132,460);
    text("sing again",132,485);
  }
    

    if ((mouseX >= 326 && mouseX < 358 && mouseY >= 396 && mouseY <= 526) || (mouseX >= 356 && mouseX < 386 && mouseY >= 420 && mouseY <= 480) || (mouseX >= 382 && mouseX < 482 && mouseY >= 328 && mouseY <= 508) || (mouseX >= 480 && mouseX < 590 && mouseY >= 370 && mouseY <= 500) || (mouseX >= 590 && mouseX < 630 && mouseY >= 410 && mouseY <= 476) || (mouseX >= 628 && mouseX < 673 && mouseY >= 366 && mouseY <= 496)) {
      image(createPo, -6, -5, 810, 648);
      textAlign(CENTER);
      textSize(30);
      text("拍案叫絶", 500, 425.5);
      text("regenerate", 500, 450.5);
    }
    
     if (startText==false &&  ((mouseX >= 20 && mouseX < 60 && mouseY >= 446 && mouseY <= 482)||(mouseX >= 60 && mouseX < 230 && mouseY >= 432 && mouseY <= 504)||(mouseX >= 108 && mouseX < 168 && mouseY >= 390 && mouseY <= 440))) {
       image(songA, -2.3, -9, 815, 652);
       textAlign(CENTER);
       textSize(30);
       text("放歌縱酒",132,460);
       text("sing again",132,485);
       
     }
    
  }

  //beginning settings
  if (startText == true) {
    textAlign(CENTER);
    textSize(70);
    text("醉詠詩", 210, 150);
    textSize(36);
    text("Zui Yong Shi", 210, 185);

  }

  //clicked seting
  if(startText==false){
  if (appearEng == false) {
    fill(0, 200);
    noStroke();
  } else {
    fill(140, 119, 98, 200);
    noStroke();
  }
  textAlign(LEFT);
  textSize(48);
  text(verLine[0], 300, 80);
  text(verLine[1], 220, 80);
  text(verLine[2], 140, 80);
  text(verLine[3], 60, 80);

  //draw the dot and control
  for (i = 0; i < 20; i++) {
    fill(0, 200);
    noStroke();
    if (i > 0) {
      if (millis() < songStartTime + storeTimeDot[i] * 1000 && millis() > songStartTime + storeTimeDot[i - 1] * 1000) {
        if (i < 5) {
          ellipse(290, 64 + i * 60, 10, 10);
        } else if (i < 10) {
          ellipse(210, 64 + (i - 5) * 60, 10, 10);
        } else if (i < 15) {
          ellipse(130, 64 + (i - 10) * 60, 10, 10);
        } else if (i < 20) {
          ellipse(50, 64 + (i - 15) * 60, 10, 10);
        }
      }
    } else {
      if (millis() < songStartTime + storeTimeDot[i] * 1000) {
        ellipse(290, 64 + i * 60, 10, 10);
      }
    }
  }


  //prevent starting genarating again while songs are not finished
  if (millis() > songStartTime + addTime * 1000) {
    songFin = true;
  } else {
    songFin = false;
  }

  appearEng = false;

  //for english translation control
  for (i = 0; i < 16; i++) {
    if (mouseX > wordInfo[i].x && mouseX < wordInfo[i].x + 38 && mouseY > wordInfo[i].y - 36 && mouseY < wordInfo[i].y + 16) {
      fill(0, 200);
      noStroke();
      textSize(48);
      if (wordInfo[i].charNum == 1) {
        text(wordInfo[i].chi, wordInfo[i].x - 4, wordInfo[i].y + 8);
      } else if (wordInfo[i].charNum == 2) {
        let presCharStra = wordInfo[i].chi.split("");
        text(presCharStra[0], wordInfo[i].x - 4, wordInfo[i].y - 22);
        text(presCharStra[1], wordInfo[i].x - 4, wordInfo[i].y + 38);
      }
      textSize(30);
      stroke(1);
      text(wordInfo[i].eng, wordInfo[i].x + 50, wordInfo[i].y);
      appearEng = true;
    }
  }
  }
}

//object holding the information about the word
class wordInformation {
  constructor() {
    this.x = 0;
    this.y = 0;
    this.chi = 0;
    this.eng = 0;
    this.lin = 0;
    this.ord = 0;
    this.charNum = 0;
    this.wordNum = 0;
  }
}

function mouseClicked() {


  if (songFin == true) {

    //create new poem
    if ((mouseX >= 326 && mouseX < 358 && mouseY >= 396 && mouseY <= 526) || (mouseX >= 356 && mouseX < 386 && mouseY >= 420 && mouseY <= 480) || (mouseX >= 382 && mouseX < 482 && mouseY >= 328 && mouseY <= 508) || (mouseX >= 480 && mouseX < 590 && mouseY >= 370 && mouseY <= 500) || (mouseX >= 590 && mouseX < 630 && mouseY >= 410 && mouseY <= 476) || (mouseX >= 628 && mouseX < 673 && mouseY >= 366 && mouseY <= 496)) {


      startText = false;
      //reset
      for (i = 0; i < 16; i++) {
        wordInfo[i].eng = "";
      }
      result = grammar.expand();
      resultSd = grammarSd.expandFrom("<note>");
      resultFw = grammarFw.expandFrom("<flow>");
      wordsAddOn = [];
      flowAddOn = [];

      let poetry = result.split("%");

      //make the word appear vertically
      for (let i = 0; i < lines.length; i++) {
        lines[i] = translateC(poetry[i]);
        verLine[i] = (lines[i].charAt(0) + "\n" + lines[i].charAt(1) + "\n" + lines[i].charAt(2) + "\n" + lines[i].charAt(3) + "\n" + lines[i].charAt(4));
      }

      //x,y position for the English translation
      for (i = 0; i < 16; i++) {
        wordInfo[i].x = 384 - wordInfo[i].lin * 80;
        if (wordInfo[i].ord == 1) {
          wordInfo[i].y = 72 + (wordInfo[i].charNum - 1) * 30;
        }
        if (wordInfo[i].ord == 2) {
          wordInfo[i].y = 72 + wordInfo[i - 1].charNum * 60 + (wordInfo[i].charNum - 1) * 30;
        }
        if (wordInfo[i].ord == 3) {
          wordInfo[i].y = 72 + (wordInfo[i - 1].charNum + wordInfo[i - 2].charNum) * 60 + (wordInfo[i].charNum - 1) * 30;
        }
        if (wordInfo[i].ord == 4) {
          wordInfo[i].y = 72 + (wordInfo[i - 1].charNum + wordInfo[i - 2].charNum + wordInfo[i - 3].charNum) * 60 + (wordInfo[i].charNum - 1) * 30;
        }
      }

      // play sound with flow and melody
      let indvSd = RiTa.tokenize(resultSd);
      let indvFw = RiTa.tokenize(resultFw);
      songStartTime = millis();
      addTime = 0;
      for (let i = 0; i < indvSd.length; i++) {
        sd[transSd(indvSd[i])].play(addTime, 1, 0.4, 0, parseInt(indvFw[i]) * 0.26);
        addTime += parseInt(indvFw[i]) * 0.26;

        flowAddOn.push(parseInt(indvFw[i]) * 0.26);
      }

      //for dot
      for (i = 0; i < 20; i++) {
        if (i > 0) {
          storeTimeDot[i] = storeTimeDot[i - 1] + flowAddOn[i];
        } else {
          storeTimeDot[i] = flowAddOn[i];
        }
      }

    }

    //sing again
    if (startText==false && ((mouseX >= 20 && mouseX < 60 && mouseY >= 446 && mouseY <= 482)||(mouseX >= 60 && mouseX < 230 && mouseY >= 432 && mouseY <= 504)||(mouseX >= 108 && mouseX < 168 && mouseY >= 390 && mouseY <= 440))) {
      let indvSd = RiTa.tokenize(resultSd);
      let indvFw = RiTa.tokenize(resultFw);
      songStartTime = millis();
      addTime = 0;
      for (let i = 0; i < indvSd.length; i++) {
        sd[transSd(indvSd[i])].play(addTime, 1, 0.4, 0, parseInt(indvFw[i]) * 0.26);
        addTime += parseInt(indvFw[i]) * 0.26;

        flowAddOn.push(parseInt(indvFw[i]) * 0.26);
      }

      //for dot
      for (i = 0; i < 20; i++) {
        if (i > 0) {
          storeTimeDot[i] = storeTimeDot[i - 1] + flowAddOn[i];
        } else {
          storeTimeDot[i] = flowAddOn[i];
        }
      }
    }
  }

}

//seperate the chinese words and the following information
function translateC(chi) {
  let removeTheLast = RiTa.tokenize(chi);
  removeTheLast.pop();
  let restoreArray = RiTa.untokenize(removeTheLast);
  let splitEC = restoreArray.split("!");
  //console.log(splitEC);
  let chineseVA = [];
  for (let j = 0; j < floor(splitEC.length / 2); j++) {

    chineseVA.push(splitEC[j * 2]);
  }
  chineseV = RiTa.untokenize(chineseVA);
  chineseV = chineseV.replace(/\s+/g, '');
  return chineseV;
}

//make sure it rhymes
function test(w) {

  let splitRhyme = w.split("!");

  if (wordsAddOn.length == 0) {
    newW = w;
  } else if (wordsAddOn.length > 0 && wordsAddOn.length <= 4) {
    let egWithRhyKey = splitRhyme[splitRhyme.length - 2].split("@");
    rhymeKey = egWithRhyKey[1];
    newW = w;
  } else if (wordsAddOn.length <= 8) {
    let egWithRhyKey = splitRhyme[splitRhyme.length - 2].split("@");
    let rhymeKey3 = egWithRhyKey[1];
    if (rhymeKey3 != rhymeKey) {
      newW = w;
    } else {
      console.log(333);
      newW = grammar.expandFrom("<line1>");
    }
  } else if (wordsAddOn.length <= 12) {
    let egWithRhyKey = splitRhyme[splitRhyme.length - 2].split("@");
    let rhymeKey4 = egWithRhyKey[1];
    if (rhymeKey4 == rhymeKey) {
      newW = w;
    } else {
      console.log(444);
      newW = grammar.expandFrom("<line1>");
    }
  }

  storeForPush = newW;
  return newW;

}

//make sure every words only appears once 
function unique(s) {

  let splitSen = s.split("!");

  //for same word in the same sentence
  while (splitSen[0] === splitSen[2] || splitSen[0] == splitSen[4] || splitSen[0] == splitSen[6] || splitSen[2] == splitSen[4] || splitSen[2] == splitSen[6] || splitSen[4] == splitSen[6]) {
    console.log(111);
    if (wordsAddOn.length == 0) {
      s = grammar.expandFrom("<line1>");
    } else if (wordsAddOn.length <= 4) {
      s = grammar.expandFrom("<line2>");
    } else if (wordsAddOn.length <= 8) {
      s = grammar.expandFrom("<line3>");
    } else if (wordsAddOn.length <= 12) {
      s = grammar.expandFrom("<line4>");
    }
    splitSen = s.split("!");
  }

  //for same word appeared previously
  while (wordsAddOn.includes(splitSen[0]) || wordsAddOn.includes(splitSen[2]) || wordsAddOn.includes(splitSen[4]) || wordsAddOn.includes(splitSen[6])) {

    if (wordsAddOn.length <= 4) {
      s = grammar.expandFrom("<line2>");
      console.log(22);
    } else if (wordsAddOn.length <= 8) {
      s = grammar.expandFrom("<line3>");
      console.log(23);
    } else if (wordsAddOn.length <= 12) {
      s = grammar.expandFrom("<line4>");
      console.log(24);
    }
    splitSen = s.split("!");
  }

  return s;
}

//for storing the informtion
function storeForPushF() {
  splitStore = storeForPush.split("!");

  let lineWords = wordsAddOn.length;
  for (i = 0; i < floor(splitStore.length / 2); i++) {

    wordInfo[i + lineWords].chi = splitStore[i * 2];
    let splitEng = splitStore[i * 2 + 1].split("@")
    wordInfo[i + lineWords].eng = splitEng[0];
    wordInfo[i + lineWords].ord = i + 1;
    wordInfo[i + lineWords].wordNum = floor(splitStore.length / 2);
    if (lineWords == 0) {
      wordInfo[i + lineWords].lin = 1;
    } else if (lineWords <= 4) {
      wordInfo[i + lineWords].lin = 2;
    } else if (lineWords <= 8) {
      wordInfo[i + lineWords].lin = 3;
    } else if (lineWords <= 12) {
      wordInfo[i + lineWords].lin = 4;
    }
    if (wordInfo[i + lineWords].chi.charAt(1) == "") {
      wordInfo[i + lineWords].charNum = 1;
    } else {
      wordInfo[i + lineWords].charNum = 2;
    }
    wordsAddOn.push(splitStore[i * 2]);
  }

}

//tranform the symble for sound array
function transSd(str) {
  if (str == "do") {
    return (0);
  }
  if (str == "re") {
    return (1);
  }
  if (str == "mi") {
    return (2);
  }
  if (str == "so") {
    return (3);
  }
  if (str == "la") {
    return (4);
  }
  if (str == "do2") {
    return (5);
  }
  if (str == "re2") {
    return (6);
  }
  if (str == "mi2") {
    return (7);
  }
  if (str == "so2") {
    return (8);
  }
  if (str == "la2") {
    return (9);
  }

}