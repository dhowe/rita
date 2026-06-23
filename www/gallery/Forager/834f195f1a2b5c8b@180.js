// https://observablehq.com/@dla/imports@180
import define1 from "./743dc2508ee5566f@27.js";
import define2 from "./12467aabdea216dd@1588.js";
import define3 from "./cb53b6da9939a3b3@171.js";
import define4 from "./304a96e9418b6e7e@82.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Imports`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`This is intended to be an as-comprehensive-as-possible gathering of \`imports\` useful for \`@dla\` so that those in the know will always be able to use the formula:
~~~
import { [ useful-import-name [, another-import-name, ... ] ] } from "@dla/imports"
~~~

If you add imports to this notebook, please add each import separately and in alphabetical order.`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`---
***alignWords(reduct_json)*** takes a json transcript produced by [app.reduct.video](https://app.reduct.video) and produces an array of word objects with aligned timestamps.

${copiable(md`~~~js
  import {alignWords} from "@dla/imports"
~~~`)}

`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`---
***heads*** flips a coin.  It’s a function in [@dla/functions](https://observablehq.com/@dla/functions).

&nbsp;&nbsp; \`if (heads()) { ... }\`
${copiable(md`~~~js
  import {heads} from "@dla/imports"
~~~`)}

`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`---
***pulse***, by [@dhowe/rita](https://observablehq.com/@dhowe/rita), simulates a timer. You can use it to refresh a cell – whose value changes – at whatever speed you choose.

one cell might contain:<br>
&nbsp;&nbsp; \`asecond = pulse(1000)\`<br>
then another cell:<br>
&nbsp;&nbsp; \`asecond, [any cell content that changes]\`<br>
typically a cell with some \`rs\` in it (see below)
${copiable(md`~~~js
  import {pulse} from "@dla/imports"
~~~`)}

`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`---
***rs*** is a tagged template, by [@dhowe/rita](https://observablehq.com/@dhowe/rita), which does 3 things: a) interprets RiScript, b) processes Markdown tags, and c) injects a style that tells Markdown *not* to ignore multiple spaces or linebreaks.

${copiable(md`~~~js
  import {rs} from "@dla/imports"
~~~`)}

`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`---
***rsr*** is a tagged template, by [@dhowe/rita](https://observablehq.com/@dhowe/rita), as above but function like raw Markdown, \`rsr(aw)\`.

${copiable(md`~~~js
  import {rsr} from "@dla/imports"
~~~`)}

`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`---
***shuffle*** shuffles an array. It’s in [@dla/functions](https://observablehq.com/@dla/functions).

&nbsp;&nbsp; \`shuffle(["a", "b", "c", "d", "e"])\`
${copiable(md`~~~js
  import {rsr} from "@dla/imports"
~~~`)}

`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`---
***verseTag*** gives you the use of a custom html tag, \`<dla-verse></dla-verse>\`. Once imported to your notebook, you can use it in Markdown or html, allowing spaces and line breaks to be respected. It’s in [@dla/styles](https://observablehq.com/@dla/styles). You need to reference \`verseTag\` at least once in your notebook. One easy way (this is what you’d type into your cell):
~~~
verseTag, md\`<dla-verse>
  an indented line
a line with     some    space in it
</dla-verse>\`
~~~
${copiable(md`~~~js
  import {verseTag} from "@dla/imports"
~~~`)}

`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`----
#### *The actual imports themselves. You can follow the links to the originals! :*`
)});
  const child1 = runtime.module(define1);
  main.import("alignWords", child1);
  const child2 = runtime.module(define1);
  main.import("heads", child2);
  const child3 = runtime.module(define2);
  main.import("pulse", child3);
  const child4 = runtime.module(define2);
  main.import("rs", child4);
  const child5 = runtime.module(define2);
  main.import("rsr", child5);
  const child6 = runtime.module(define1);
  main.import("shuffle", child6);
  const child7 = runtime.module(define3);
  main.import("verseTag", child7);
  main.variable(observer()).define(["md"], function(md){return(
md`----
#### *Conveniences for this notebook (but also generally useful) :*`
)});
  const child8 = runtime.module(define4);
  main.import("copiable", child8);
  main.import("style", child8);
  main.variable(observer()).define(["md"], function(md){return(
md`<small>\`style\`*, as above, has to be referenced in the notebook:*`
)});
  main.variable(observer()).define(["style"], function(style){return(
style
)});
  return main;
}
