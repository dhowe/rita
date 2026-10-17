// https://observablehq.com/@dla/rita-utilities@845
import define1 from "./304a96e9418b6e7e@82.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["RiTa.png",new URL("./files/5ad1543f837d40bf1e53e53aed49c6130d630660020409c1b8667bdba391951d629d12003864064f1c31034230eb893315f9d46b9d325922eda0ebfdfa1bbd38",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md","FileAttachment","style","copiable"], async function(md,FileAttachment,style,copiable){return(
md`# RiTa + Observable <img height="37px" style="float: right; margin-right:300px" src="${await FileAttachment(
  "RiTa.png"
).url()}" />
  
Tools for using [RiTa](https://rednoise.org/rita) and [RiScript](/@dhowe/riscript) in observable. 

<small><em>If you're not yet familiar with RiTa, check out the  <a href="https://rednoise.org/rita" target="new">website</a>  or this observable <a href="https://observablehq.com/collection/@dhowe/rita" target="new">collection</a>...<br></em></small>

To require RiTa itself <small>(not needed for the tools below)</small> do: ${style}

${copiable(md`~~~js
  RiTa = require("rita"); 
~~~`)}
or
${copiable(md`~~~js
  import {RiTa} from "@dhowe/rita"
~~~`)}


<!--To import tools:
  * [\`RiScript editor\`](#editorDemo)
  * [\`Tagged templates\`](#templateDemo)-->
`
)});
  main.variable(observer("templateDemo")).define("templateDemo", ["md","copiable"], function(md,copiable){return(
md`---
## RiScript tagged template

${copiable(md`~~~js
  import {rs} from "@dhowe/rita"
~~~`)}

Enables <span class=code>rs</span> as a tagged template, which can be used wherever you would use <span class=code>md</span>...

The <span class=code>rs</span> tag does 3 things:
1. interprets [RiScript](./riscript) expressions
2. processes [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) tags 
3. injects a style into all <small><span class=code>&lt;p&gt;</span></small> tags telling Markdown not to ignore spaces and linebreaks  <small>(thanks to [@shadoof](https://observablehq.com/@shadoof)).</small>

<div class=examples>Examples:</div>
`
)});
  main.variable(observer()).define(["rs"], function(rs){return(
rs`### A Title
Some text with    spaces
       and line-breaks`
)});
  main.variable(observer()).define(["sec","rs"], function(sec,rs){return(
sec,rs`### A Title 
Some [RiScript](/@dhowe/riscript) code
  that we can (format|arrange|layout)
     with *(embedded | inline)* Markdown
       and rerun (each | once per) second
         (via|using|with) the **(pulse).qq** function below

`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`<p><small><em>Note: if you want vanilla or 'raw' Markdown (which ignores multiple spaces and line-breaks) you can use the following import instead:</em></small>
${copiable(md`~~~js
  import {rsr} from "@dhowe/rita"
~~~

`
)}</p>`
)});
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`--------
## RiTa pulse
${copiable(md`~~~js
  import {pulse} from "@dhowe/rita"
~~~`)}
The *pulse* function simulates a simple timer, via a generator function, that you can use to refresh a cell at whatever speed you choose.

For example, in the cell above, we set a pulse at 1000ms (or 1 second)
~~~js
  sec = pulse(1000) 
~~~
Then we reference *sec* in the cell we want to refresh:
~~~
  sec,rs\`
      Some code
        we want to refresh
          each second
  \`~~~
`
)});
  main.variable(observer()).define(["html"], function(html){return(
html`
<div class="rc">
<h3>&nbsp;&nbsp;&nbsp;Related Resources</h3>
<ul>
<li>The <a href="/@dhowe/the-rita-reference">RiTa reference</a> in observable</li>
<li>The <a href="https://rednoise.org/rita" target="new">RiTa website</a>: examples, docs, gallery, etc.</li>
<li>A tutorial on<a href="/@dhowe/riscript" target="new"> RiScript</a>, RiTa's simple scripting language</li>
<!--li>Tools for <a href="/@dhowe/rita" target="new">RiTa in observable</a>, including the <span style="color: #c7254e;background-color: #f9f2f4;">rs</span> template</li-->
<li>Using RiScript and RiTa Grammars <a href="./rita-in-twine" target="new"> within Twine</a></li>
<li>Generating with RiTa <a href="/@dhowe/tut-rita-grammars" target="new">grammars</a> and <a href="./tut-rita-ngrams" target="new">Markov chains</a></li>
<li>RiTa's <a href="/@dhowe/rita-lexicon" target="new">Lexicon and Letter-to-Sound engine</a></li></ul>
</div>
<br>
<style>
.rc {
  border-radius: 25px;
  border: 2px solid #000;
  padding: 20px 0px 10px 20px;
  width: 400px;
  font-size: .8em;
}
</style>

`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`-----------
## Appendix`
)});
  main.variable(observer("RiTa")).define("RiTa", ["require"], function(require){return(
require("rita@2.4.84")
)});
  main.variable(observer()).define(["RiTa"], function(RiTa){return(
RiTa.VERSION
)});
  main.variable(observer("editor")).define("editor", ["html","md","RiTa"], function(html,md,RiTa){return(
function editor(params) { //not used at moment

  const value = params.value || "//\nadd code here\n\n\n";
  const theme = params.theme ? params.theme + "Mode" : "darkMode";
  const width = params.width || "800px";
  const height = params.height || "auto";
  const fontSize = params.fontSize || "16px";

  // modified from https://observablehq.com/@benatkin/codemirror-iframe
  let t = theme;
  let fn = ({CodeMirror} = {}) => {
    return ({id, value, t}) => {
      CodeMirror.defineSimpleMode("RiScript", {
        start: [
          //RiScript
          { regex: /\(([^)]*\|)+[^)]*\)/g, token: "choice" },
          //choices
          { regex: /(\.[\w]+(\(\))?)/g, token: "transform" },
          //transforms 
          { regex: /\$\w+/g, token: "symbol" },
          //symbol
          { regex: /\$\$\w+/g, token: "dynamic" },
          //dynamic symbol
          { regex: /\/\/.*/g, token: "comment" },
          //single line comment
          { regex: /\/\*/, token: "comment", next: "comment" },
          //multi lines comment
        ],
        comment: [
          {regex: /.*?\*\//, token: "comment", next: "start"},
          {regex: /.*/, token: "comment"}
        ],
      });
      const cm = CodeMirror(document.body, {
        value,
        mode: 'RiScript',
        theme: t,
        lineNumbers: true
      })
      CodeMirror.modeURL = 'https://codemirror.net/mode/%N/%N.js';
      cm.on('change', (cm, changes) => {
        window.parent.postMessage({
          id,
          value: cm.getValue(),
          height: document.body.offsetHeight
        }, `https://${document.domain}`);
      })
      setInterval(() => {
        window.parent.postMessage({
          id,
          height: document.body.offsetHeight
        }, `https://${document.domain}`);
      }, 300);
    }
  }
  const randomId = `el${Math.floor(Math.random() * 1000000)}`
  const frameSrc = `
<link rel="stylesheet" href="https://unpkg.com/codemirror@5.59.2/lib/codemirror.css" />
<script src="https://unpkg.com/codemirror@5.59.2/lib/codemirror.js"></script>
<script src="https://codemirror.net/addon/mode/simple.js"></script>
<style type="text/css">
body, html {
margin: 0;
padding: 0;
overflow-y: hidden;
}
.CodeMirror {
border: 1px solid #eee;
height: auto;
font-size: ` + fontSize + `;
}
.CodeMirror-scroll {
height: auto;
overflow-y: hidden;
overflow-x: auto;
}

/*
* lightMode theme
*/
.CodeMirror.cm-s-lightMode { background: #ffffff; color: #363636; }
.cm-s-lightMode .div.CodeMirror-selected { background: #264f78; }
.cm-s-lightMode .CodeMirror-gutters { border-right: 1px solid #ddd; background-color: #f7f7f7; white-   space: nowrap; }
.cm-s-lightMode .CodeMirror-linenumbers {}
.cm-s-lightMode .CodeMirror-linenumber { padding: 0 3px 0 5px; min-width: 20px; text-align: right; color: #6998ac; white-space: nowrap; }
.cm-s-lightMode .CodeMirror-cursor { border-left: 1px solid #1e1e1e; }

/* color for symbols (e.g $foo) */
.cm-s-lightMode span.cm-symbol { color: #3d409b; }

/* color ffor dynamics */
.cm-s-lightMode span.cm-dynamic { color: #2e2bf9; }

/* color for choices (e.g (a|b)) */
.cm-s-lightMode span.cm-choice { color: #b66661; }

/* color for transforms (e.g $foo.pluralize) */
.cm-s-lightMode span.cm-transform { color: #867959; }

/* color for comment */
.cm-s-lightMode span.cm-comment { color: #669851; }

.cm-s-lightMode .CodeMirror-activeline-background { background: #2F2F2F; }
.cm-s-lightMode .CodeMirror-matchingbracket { text-decoration: underline; color: white !important; }

/*
* darkMode theme
*/
.CodeMirror.cm-s-darkMode { background: #1e1e1e; color: #cbcbcb; }
.cm-s-darkMode .CodeMirror-selected { background: #264f78; }
.cm-s-darkMode .CodeMirror-gutters { background: #464646; border-right: 0px; color: #cbcbcb;}
.cm-s-darkMode .CodeMirror-linenumber { color: #cbcbcb; }
.cm-s-darkMode .CodeMirror-cursor { border-left: 1px solid #c4c2bd; }

/* color for symbols (e.g $foo) */
.cm-s-darkMode span.cm-symbol { color: #9bdbff; }

/* color for dynamics */
.cm-s-darkMode span.cm-dynamic { color: #4ebfff; }

/* color for choices (e.g (a|b)) */
.cm-s-darkMode span.cm-choice { color: #ad94b9; }

/* color for transforms (e.g $foo.pluralize) */
.cm-s-darkMode span.cm-transform { color: #cdab53; }

/* color for comment */
.cm-s-darkMode span.cm-comment { color: #669851; }

.cm-s-darkMode .CodeMirror-activeline-background { background: #2F2F2F; }
.cm-s-darkMode .CodeMirror-matchingbracket { text-decoration: underline; color: white !important; }
</style>
<script type="text/javascript">
document.addEventListener('DOMContentLoaded', () => {
(${fn({}).toString().trim()})(${JSON.stringify({id: randomId, value, t})})
})
</script>
`
  const frameStyle = `width: ` + width + `;height: ` + height + `; border: 0; overflow-y: auto;`
  const frame = html`<iframe style="${frameStyle}"></iframe>`;
  const messageListener = event => {
    if (document.contains(frame)) {
      if (event.data.id == randomId) {
        if (event.data.value != undefined) {
          value = event.data.value;
          frame.value = event.data.value;
          frame.dispatchEvent(new CustomEvent("input"));
        }
        frame.style.height = `${event.data.height + 30}px`;
      }
    } else {
      window.removeEventListener('message', messageListener);
    }
  }
  window.addEventListener('message', messageListener, false);
  frame.srcdoc = frameSrc;
  frame.value = (() => md`${RiTa.evaluate(value.trim())}`)();
  return frame;
}
)});
  main.variable(observer("rs")).define("rs", ["template","md"], function(template,md){return(
template(md)
)});
  main.variable(observer("rsr")).define("rsr", ["template"], function(template){return(
template()
)});
  const child1 = runtime.module(define1);
  main.import("copiable", child1);
  main.import("style", child1);
  main.variable(observer("sec")).define("sec", ["pulse"], function(pulse){return(
pulse(1000)
)});
  main.variable(observer("pulse")).define("pulse", ["Promises"], function(Promises){return(
function*(ms) {
  while (true) {
    yield Promises.tick(ms);
  }
}
)});
  main.variable(observer("template")).define("template", ["RiTa"], function(RiTa){return(
function(md, opts = {}) {
    let fun = (strs, ...vals) => {
      try {
        return RiTa.RiScript.eval(strs.reduce
          ((a, s, i) => a + s + (vals[i] || ''), ''));
      }
      catch (e) {
        console.error('[RiScript] ' + e.message);
        return '[RiScript] ' + e.message;
      }
    }
    if (!md) return fun;
    return (s, ...v) => {
      let res = md`${fun(s, v)}`;
      Array.from(res.children).forEach((e,i) => {
        if (e.tagName === 'P') e.style['white-space'] = 'break-spaces';
      });
      return res;
    }
  }
)});
  main.variable(observer()).define(["html"], function(html){return(
html`<style>
.examples {
  font-size:20px;
  font-style: italic;
}
.code {
  color: #c7254e;
  background-color: #f9f2f4;
}`
)});
  return main;
}
