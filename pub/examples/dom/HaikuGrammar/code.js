let grammar, lines;

$(function () {

  $.getJSON('../../data/haiku.json', json => {

    grammar = RiTa.grammar(json);

    lines = $('.lines');
    $(lines[0]).text("click to");
    $(lines[1]).text("generate");
    $(lines[2]).text("a haiku");

    $('#content').click(haiku);
  });
});

function haiku() {

  let expanded = grammar.expand();
  let haiku = expanded.split("%");
  for (let i = 0; i < haiku.length; i++) {
    $(lines[i]).text(haiku[i]);
  }
}
