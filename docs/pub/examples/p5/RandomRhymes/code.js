let rhymes, word;

function setup() {
  createCanvas(300, 300);
  
  fill(255);
  textFont("Georgia");
  textLeading(17);

  findRhymes();
}

function draw() {
  background(100, 0, 100);

  textSize(36);
  textAlign(RIGHT);
  text(word, 280, 40);

  textSize(14);
  textAlign(LEFT);
  text(rhymes, 30, 73);
}

function findRhymes() {

  let tmp;
  do {
    word = RiTa.randomWord();
    tmp = RiTa.rhymesSync(word, { limit: 13 });
  }
  while (tmp.length < 3)

  rhymes = tmp.join("\n");

  // run again in 1.5 sec
  setTimeout(findRhymes, 1500);
}

    


