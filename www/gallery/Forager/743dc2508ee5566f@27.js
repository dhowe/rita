// https://observablehq.com/@dla/functions@27
export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Functions`
)});
  main.variable(observer("alignWords")).define("alignWords", function(){return(
function(reduct_json, secondsAtEndOfText = 3) {
  let a = [];
  Object.keys(reduct_json).forEach(segments => {
    reduct_json[segments].forEach(speech => {
      a = a.concat(speech.wdlist);
    });
  });
  a.forEach((word, index) => {
    word.word = word.word.trim();
    index < a.length - 1
      ? (word.gap = a[index + 1].start - word.end)
      : (word.gap = secondsAtEndOfText);
  });
  return a;
}
)});
  main.variable(observer("heads")).define("heads", ["randInt"], function(randInt){return(
() => {
  return randInt(2) == 0;
}
)});
  main.variable(observer("mod")).define("mod", function(){return(
function (n, m) {
  // mod function that handles negative numbers, usage: mod(num, modulous)
  return ((n % m) + m) % m;
}
)});
  main.variable(observer("randInt")).define("randInt", function(){return(
maxPlusOne => (maxPlusOne * Math.random()) | 0
)});
  main.variable(observer()).define(["randInt"], function(randInt){return(
randInt(2)
)});
  main.variable(observer("randElement")).define("randElement", ["randInt"], function(randInt){return(
(array) => array[randInt(array.length)]
)});
  main.variable(observer("randIntBetween")).define("randIntBetween", function(){return(
(min, max) => {
  return Math.floor(Math.random() * (max - min) + min);
}
)});
  main.variable(observer("shuffle")).define("shuffle", ["randInt"], function(randInt){return(
arr => {
  for (let i = arr.length - 1; i >= 0; i--) {
    let randomIndex = randInt(i + 1); // Math.floor(Math.random() * (i + 1));
    let itemAtIndex = arr[randomIndex];
    arr[randomIndex] = arr[i];
    arr[i] = itemAtIndex;
  }
  return arr;
}
)});
  return main;
}
