// https://observablehq.com/@dla/styles@171
import define1 from "./82fed029a9e5449f@845.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Styles`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`#### Verse
Examples of various ways to style verse for Markdown or html in Observable:`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`*Everything in-line, nothing to import:*`
)});
  main.variable(observer("allinlineDemo")).define("allinlineDemo", ["md"], function(md){return(
md`<div style='white-space: break-spaces;'>A line of poetry
    An indented line,
And     a line with     space     within it.
</div>`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`*For the following version, you'd have to add:*<br>
\`import { verseClass } from "@dla/styles"\``
)});
  main.variable(observer("styledDivClassDemo")).define("styledDivClassDemo", ["md"], function(md){return(
md`<div class="verse">A line of poetry
    An indented line,
And     a line with     space     within it.
</div>`
)});
  main.variable(observer("verseClass")).define("verseClass", ["html"], function(html){return(
html`
<style>
  .verse {
    white-space: break-spaces;
  }
</style>`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`*For the following, you’d have to add:*<br>
\`import { verseTag } from "@dla/styles"\``
)});
  main.variable(observer("customTag")).define("customTag", ["md"], function(md){return(
md`<dla-verse>A line of poetry
    An indented line,
And     a line with     space     within it.
</dla-verse>`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`*The following cell creates and registers a custom HTML tag. NOTE that the names of custom tags must include a “-” (hyphen).*`
)});
  main.variable(observer("verseTag")).define("verseTag", ["HTMLElement","customElements"], function(HTMLElement,customElements)
{
  class Verse extends HTMLElement {
    constructor() {
      super(); // Always call super first in constructor
      this.setAttribute('style', 'white-space: break-spaces');
    }
  }
  try {
    customElements.define('dla-verse', Verse);
    return "<dla-verse> has been initially constructed and registered";
  } catch (err) {
    if (err.name == "NotSupportedError")
      return "<dla-verse> is constructed and registered";
    console.error(err);
  }
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`#### Appendix for tests and demos.`
)});
  main.variable(observer()).define(["customTag"], function(customTag){return(
customTag.innerText
)});
  const child1 = runtime.module(define1);
  main.import("rs", child1);
  main.import("pulse", child1);
  main.variable(observer("rsDemo")).define("rsDemo", ["rs"], function(rs){return(
rs`A line of ( poetry | verse )
    An indented line,
And     a line with     space     within it.
`
)});
  main.variable(observer("oneSecondPulse")).define("oneSecondPulse", ["pulse"], function(pulse){return(
pulse(1000)
)});
  main.variable(observer("rsPulseDemo")).define("rsPulseDemo", ["oneSecondPulse","rs"], function(oneSecondPulse,rs){return(
oneSecondPulse,
rs`<dla-verse>A line of (poetry | verse | arty prose)
    An indented ( line | gobbet),
And     a (line | gobbet) with     ( space | nothings )    within it.
</dla-verse>`
)});
  return main;
}
