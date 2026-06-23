// https://observablehq.com/@tmcw/copiable@82
export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md","copiable"], function(md,copiable){return(
md`# Copiable

This notebook provides an affordance for copying text. You can use it like this, and click this import statement to copy it:

${copiable(md`
\`\`\`js
import {copiable, style} from "@tmcw/copiable"
\`\`\``)}

It uses [execCommand](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand) to do its thing.

---

\`\`\`
md\`
This is a chunk of text, with this bit copiable:

$\{copiable(md\`Some content\`)}
\`
\`\`\`


---

\`\`\`js
style
\`\`\`

(the style value is a stylesheet that adds the nice yellow hover indication when something is copiable/copied)

`
)});
  main.variable(observer("copiable")).define("copiable", ["copy"], function(copy){return(
element => {
  element.addEventListener('click', e => {
    copy(element.textContent.trim());
    element.classList.add('copied');
    setTimeout(() => element.classList.remove('copied'), 500);
  });
  element.classList.add('copiable');
  return element;
}
)});
  main.variable(observer("copy")).define("copy", function(){return(
function copy(text) {
  const fakeElem = document.body.appendChild(document.createElement('textarea'));
  fakeElem.style.position = 'absolute';
  fakeElem.style.left = '-9999px';
  fakeElem.setAttribute('readonly', '');
  fakeElem.value = text;
  fakeElem.select();
  try {
    return document.execCommand('copy');
  } catch (err) {
    return false;
  } finally {
    fakeElem.parentNode.removeChild(fakeElem);
  }
}
)});
  main.variable(observer("style")).define("style", ["html"], function(html){return(
html`<style>
.copiable {
  position:relative;
  cursor:pointer;
}
.copiable:hover::after {
  background: #FBF1A9;
  content: 'click to copy';
  padding: 0px 10px;
}
.copiable.copied:hover::after {
  content: 'copied!';
}
</style>`
)});
  return main;
}
