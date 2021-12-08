// https://observablehq.com/@jashkenas/inputs@2303
export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["capstan.gif",new URL("./files/c051fbc024553912e31968b35e537d4ad3592201b5f8e7bd13fd9d02e38599c5d541a704d0858c676328babb3e5c9c35dd7c6d67240090d094882a1cad8eece4",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md","FileAttachment"], async function(md,FileAttachment){return(
md`# Inputs
<div style="margin-top: -3px; font-size: 1.05em;">*a.k.a “The Grand Native Inputs Bazaar”*</div>

<div style="max-width: 500px; margin: 30px 0; padding: 15px 30px; background-color: #ffffee; font: 700 18px/24px sans-serif;">✨ Rejoice! Observable now has <a href="https://observablehq.com/@observablehq/inputs">an official inputs library</a>. If it contains the input you need, you should probably be using that instead of this notebook. ✨</div>

<img width="350px" src="${await FileAttachment("capstan.gif").url()}" />

A collection of assorted fancy inputs, odds and ends — with which to produce values to feed your burgeoning sketches. All inputs support optional **titles** and **descriptions**; where it makes sense, inputs also support a **submit** option, which allows you to prevent the value from updating until the input has been finalized.

Wares we have on offer: 
  * [\`slider\`](#sliderDemo)
  * [\`button\`](#buttonDemo)
  * [\`select\`](#selectDemo)
  * [\`autoSelect\`](#autoSelectDemo)
  * [\`color\`](#colorDemo)
  * [\`coordinates\`](#coordinatesDemo)
  * [\`worldMapCoordinates\`](#worldMapCoordinatesDemo)
  * [\`usaMapCoordinates\`](#usaMapCoordinatesDemo)
  * [\`date\`](#dateDemo)
  * [\`time\`](#timeDemo)
  * [\`file\`](#fileDemo)
  * [\`text\`](#textDemo)
  * [\`textarea\`](#textareaDemo)
  * [\`radio\`](#radioDemo)
  * [\`checkbox\`](#checkboxDemo)
  * [\`number\`](#numberDemo)
  * [\`password\`](#passwordDemo)`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`| <h3>Friends & Family:</h3>  |   |
|---|---|
| **[@mbostock/form-input](/@mbostock/form-input)**  | Fully custom forms, combining inputs into a single reactive cell. |
| **[@mbostock/scrubber](/@mbostock/scrubber)** | A slider that automatically plays through its range, useful for driving and scrubbing through animations. |
| **[@bumbeishvili/input-groups](/@bumbeishvili/input-groups)** | A wrapper function that can put many of these inputs into a more compact grid layout. | 
| **[@zechasault/color-schemes-and-interpolators-picker](/@zechasault/color-schemes-and-interpolators-picker)**  | Color scheme and interpolation pickers. |
| **[@awhitty/fips-county-code-brush](/@awhitty/fips-county-code-brush)**  | A brushable map of the United States, allowing you to quickly select sets of counties to get their FIPS codes. |
| **[@mootari/range-slider](https://observablehq.com/@mootari/range-slider)**  |  True range sliders, setting both a minimum and maximum value. |
| **[@bumbeishvili/data-driven-range-sliders](/@bumbeishvili/data-driven-range-sliders)** | Data-driven range sliders, displaying a distribution histogram of the underlying data. |
| **[@trebor/snapping-histogram-slider](/@trebor/snapping-histogram-slider)** | Another data-driven range slider option. |
| **[@mootari’s 2D Slider](https://observablehq.com/d/98bbb19bf9e859ee)** | Two dimensional sliders, exploring discrete points on a plane. |
| **[@yurivish/ternary-slider](/@yurivish/ternary-slider)** | Nifty ternary plot inputs, describing the percentages of a whole composed of exactly three things. |
| **[@rreusser/binary-input](/@rreusser/binary-input)** | Input numbers in binary, great for working with values where results vary with specific bit positions. |
| **[@bartok32/diy-inputs](/@bartok32/diy-inputs)** | A fun tool for defining your own fancy and colorful inputs. |
| **[@bobkerns/elements-input](/@bobkerns/elements-input)** | A periodic table of the elements input! You can construct molecules programmatically, or click on the table to create formulas. |
| **[@fil/selectflat](/@fil/selectflat)** | A fast selector to explore a discrete parameter space. The value changes on mouseover, and sticks when you click. |
| **[@oscar6echo/player](/@oscar6echo/player)** | A slider with buttons to play, pause, step, and change speed and direction — useful for animations. |
| **[@harrislapiroff/list-input](/@harrislapiroff/list-input)** | A input for when you want more than one of something. |
| **[@nhogs/easing-graphs-editor](/@nhogs/easing-graphs-editor)** | A curve input to display and edit values of animated properties over time, such as easing curves and animation curves. |
| **[@j-f1/checkbox](/@j-f1/checkbox)** | A simple checkbox input that provides a boolean value. |

<br>*If you have any improvements for the bazaar, [please make your change in a fork and send it to me as a suggestion.](https://observablehq.com/@observablehq/suggestions-and-comments)*`
)});
  main.variable(observer("sliderDemo")).define("sliderDemo", ["md"], function(md){return(
md`---
## Sliders

~~~js
import {slider} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof a")).define("viewof a", ["slider"], function(slider){return(
slider()
)});
  main.variable(observer("a")).define("a", ["Generators", "viewof a"], (G, _) => G.input(_));
  main.variable(observer("viewof a1")).define("viewof a1", ["slider"], function(slider){return(
slider({
  min: 0, 
  max: 1, 
  step: 0.01, 
  format: ".0%",
  description: "Zero to one, formatted as a percentage"
})
)});
  main.variable(observer("a1")).define("a1", ["Generators", "viewof a1"], (G, _) => G.input(_));
  main.variable(observer("viewof a1_1")).define("viewof a1_1", ["slider"], function(slider){return(
slider({
  min: 0, 
  max: 1, 
  step: 0.01, 
  format: v => `${Math.round(100 * v)} per cent`,
  description: "Zero to one, formatted with a custom function"
})
)});
  main.variable(observer("a1_1")).define("a1_1", ["Generators", "viewof a1_1"], (G, _) => G.input(_));
  main.variable(observer("viewof a2")).define("viewof a2", ["slider"], function(slider){return(
slider({
  min: 0,
  max: 1e9,
  step: 1000,
  value: 3250000,
  format: ",",
  description:
    "Zero to one billion, in steps of one thousand, formatted as a (US) number"
})
)});
  main.variable(observer("a2")).define("a2", ["Generators", "viewof a2"], (G, _) => G.input(_));
  main.variable(observer("viewof a3")).define("viewof a3", ["slider"], function(slider){return(
slider({
  min: 0, 
  max: 100, 
  step: 1, 
  value: 10, 
  title: "Integers", 
  description: "Integers from zero through 100"
})
)});
  main.variable(observer("a3")).define("a3", ["Generators", "viewof a3"], (G, _) => G.input(_));
  main.variable(observer("viewof a4")).define("viewof a4", ["slider"], function(slider){return(
slider({
  min: 0.9,
  max: 1.1,
  precision: 3,
  description: "A high precision slider example"
})
)});
  main.variable(observer("a4")).define("a4", ["Generators", "viewof a4"], (G, _) => G.input(_));
  main.variable(observer("viewof a5")).define("viewof a5", ["slider"], function(slider){return(
slider({
  min: 0.9,
  max: 1.1,
  precision: 3,
  submit: true,
  description: "The same as a4, but only changes value on submit"
})
)});
  main.variable(observer("a5")).define("a5", ["Generators", "viewof a5"], (G, _) => G.input(_));
  main.variable(observer()).define(["md"], function(md){return(
md`More [fancy slider techniques](https://observablehq.com/@mootari/prime-numbers-slider).`
)});
  main.variable(observer("slider")).define("slider", ["input"], function(input){return(
function slider(config = {}) {
  let {
    min = 0,
    max = 1,
    value = (max + min) / 2,
    step = "any",
    precision = 2,
    title,
    description,
    disabled,
    getValue,
    format,
    display,
    submit
  } = typeof config === "number" ? { value: config } : config;
  precision = Math.pow(10, precision);
  if (!getValue)
    getValue = input => Math.round(input.valueAsNumber * precision) / precision;
  return input({
    type: "range",
    title,
    description,
    submit,
    format,
    display,
    attributes: { min, max, step, disabled, value },
    getValue
  });
}
)});
  main.variable(observer("buttonDemo")).define("buttonDemo", ["md"], function(md){return(
md`---
## Buttons

~~~js
import {button} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof b")).define("viewof b", ["button"], function(button){return(
button()
)});
  main.variable(observer("b")).define("b", ["Generators", "viewof b"], (G, _) => G.input(_));
  main.variable(observer()).define(["b"], function(b)
{
  b
  return !this;
}
);
  main.variable(observer("viewof b1")).define("viewof b1", ["button"], function(button){return(
button({value: "Click me", description: "We use a reference to the button below to record the time you pressed it."})
)});
  main.variable(observer("b1")).define("b1", ["Generators", "viewof b1"], (G, _) => G.input(_));
  main.variable(observer()).define(["b1"], function(b1)
{
  b1;
  return new Date(Date.now()).toUTCString()
}
);
  main.variable(observer("button")).define("button", ["input"], function(input){return(
function button(config = {}) {
  const {
    value = "Ok", title, description, disabled
  } = typeof config === "string" ? {value: config} : config;
  const form = input({
    type: "button", title, description,
    attributes: {disabled, value}
  });
  form.output.remove();
  return form;
}
)});
  main.variable(observer("selectDemo")).define("selectDemo", ["md"], function(md){return(
md`---
## Dropdown Menus and Multiselects

~~~js
import {select} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof dd")).define("viewof dd", ["select"], function(select){return(
select(["Spring", "Summer", "Fall", "Winter"])
)});
  main.variable(observer("dd")).define("dd", ["Generators", "viewof dd"], (G, _) => G.input(_));
  main.variable(observer()).define(["dd"], function(dd){return(
dd
)});
  main.variable(observer("viewof dd1")).define("viewof dd1", ["select"], function(select){return(
select({
  title: "Stooges",
  description: "Please pick your favorite stooge.",
  options: ["Curly", "Larry", "Moe", "Shemp"],
  value: "Moe"
})
)});
  main.variable(observer("dd1")).define("dd1", ["Generators", "viewof dd1"], (G, _) => G.input(_));
  main.variable(observer()).define(["dd1"], function(dd1){return(
dd1
)});
  main.variable(observer("viewof dd2")).define("viewof dd2", ["select"], function(select){return(
select({
  description: "As a child, which vegetables did you refuse to eat?",
  options: ["Spinach", "Broccoli", "Brussels Sprouts", "Cauliflower", "Kale", "Turnips", "Green Beans", "Asparagus"],
  multiple: true
})
)});
  main.variable(observer("dd2")).define("dd2", ["Generators", "viewof dd2"], (G, _) => G.input(_));
  main.variable(observer()).define(["dd2"], function(dd2){return(
dd2
)});
  main.variable(observer("viewof dd3")).define("viewof dd3", ["select"], function(select)
{
  const dd3 = select({
    title: "How are you feeling today?",
    options: [
      { label: "🤷", value: "shrug" },
      { label: "😂", value: "tears-of-joy" },
      { label: "😍", value: "loving-it" },
      { label: "🤔", value: "hmmm" },
      { label: "😱", value: "yikes", disabled: true },
      { label: "😈", value: "mischievous" },
      { label: "💩", value: "poo" }
    ],
    value: "hmmm"
  });
  dd3.input.style.fontSize = "30px";
  dd3.input.style.marginTop = "8px";
  return dd3;
}
);
  main.variable(observer("dd3")).define("dd3", ["Generators", "viewof dd3"], (G, _) => G.input(_));
  main.variable(observer()).define(["dd3"], function(dd3){return(
dd3
)});
  main.variable(observer("select")).define("select", ["input","html"], function(input,html){return(
function select(config = {}) {
  let {
    value: formValue,
    title,
    description,
    disabled,
    submit,
    multiple,
    size,
    options
  } = Array.isArray(config) ? { options: config } : config;
  options = options.map(o =>
    typeof o === "object" ? o : { value: o, label: o }
  );
  const form = input({
    type: "select",
    title,
    description,
    submit,
    attributes: { disabled },
    getValue: input => {
      const selected = Array.prototype.filter
        .call(input.options, i => i.selected)
        .map(i => i.value);
      return multiple ? selected : selected[0];
    },
    form: html`
      <form>
        <select name="input" ${
          multiple ? `multiple size="${size || options.length}"` : ""
        }>
          ${options.map(({ value, label,disabled }) =>
            Object.assign(html`<option>`, {
              value,
              selected: Array.isArray(formValue)
                ? formValue.includes(value)
                : formValue === value,
              disabled : disabled ? disabled : false,
              textContent: label
            })
          )}
        </select>
      </form>
    `
  });
  form.output.remove();
  return form;
}
)});
  main.variable(observer("autoSelectDemo")).define("autoSelectDemo", ["md"], function(md){return(
md`---
## Autoselects
*A variant of an option menu, using an autocompleting text input, via HTML’s datalist element.* 

~~~js
import {autoSelect} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof as")).define("viewof as", ["autoSelect","usa"], function(autoSelect,usa){return(
autoSelect({
  options: usa.objects.states.geometries.map(d => d.properties.name),
  placeholder: "Search for a US state . . ."
})
)});
  main.variable(observer("as")).define("as", ["Generators", "viewof as"], (G, _) => G.input(_));
  main.variable(observer()).define(["as"], function(as){return(
as
)});
  main.variable(observer("autoSelect")).define("autoSelect", ["input","html"], function(input,html){return(
function autoSelect(config = {}) {
  const {
    value,
    title,
    description,
    disabled,
    autocomplete = "off",
    placeholder,
    size,
    options,
    list = "options"
  } = Array.isArray(config) ? { options: config } : config;

  const optionsSet = new Set(options);

  const form = input({
    type: "text",
    title,
    description,
    attributes: { disabled },
    action: fm => {
      fm.value = fm.input.value = value || "";
      fm.onsubmit = e => e.preventDefault();
      fm.input.oninput = function(e) {
        e.stopPropagation();
        fm.value = fm.input.value;
        if (!fm.value || optionsSet.has(fm.value))
          fm.dispatchEvent(new CustomEvent("input"));
      };
    },
    form: html`
      <form>
         <input name="input" type="text" autocomplete="off" 
          placeholder="${placeholder ||
            ""}" style="font-size: 1em;" list=${list}>
          <datalist id="${list}">
              ${options.map(d =>
                Object.assign(html`<option>`, {
                  value: d
                })
              )}
          </datalist>
      </form>
      `
  });

  form.output.remove();
  return form;
}
)});
  main.variable(observer("colorDemo")).define("colorDemo", ["md"], function(md){return(
md`---
## Color Pickers

*value: a hexadecimal string, e.g. * \`"#bada55"\` 

~~~js
import {color} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof c")).define("viewof c", ["color"], function(color){return(
color()
)});
  main.variable(observer("c")).define("c", ["Generators", "viewof c"], (G, _) => G.input(_));
  main.variable(observer("viewof c1")).define("viewof c1", ["color"], function(color){return(
color({
  value: "#0000ff",
  title: "Background Color",
  description: "This color picker starts out blue"
})
)});
  main.variable(observer("c1")).define("c1", ["Generators", "viewof c1"], (G, _) => G.input(_));
  main.variable(observer("color")).define("color", ["input"], function(input){return(
function color(config = {}) {
  const { value = "#000000", title, description, disabled, submit, display } =
    typeof config === "string" ? { value: config } : config;
  const form = input({
    type: "color",
    title,
    description,
    submit,
    display,
    attributes: { disabled, value }
  });
  // The following two lines are a bugfix for Safari, which hopefully can be removed in the future.
  form.input.value = '';
  form.input.value = value;
  if (title || description) form.input.style.margin = "5px 0";
  return form;
}
)});
  main.variable(observer("coordinatesDemo")).define("coordinatesDemo", ["md"], function(md){return(
md` ---
## Coordinates

*value: an array pair of \`[longitude, latitude]\`, e.g. * \`[-122.27, 37.87]\` 

~~~js
import {coordinates} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof coords1")).define("viewof coords1", ["coordinates"], function(coordinates){return(
coordinates()
)});
  main.variable(observer("coords1")).define("coords1", ["Generators", "viewof coords1"], (G, _) => G.input(_));
  main.variable(observer()).define(["coords1"], function(coords1){return(
coords1
)});
  main.variable(observer("viewof coords2")).define("viewof coords2", ["coordinates"], function(coordinates){return(
coordinates({
  title: "Hometown",
  description: "Enter the coordinates of where you were born",
  value: [-122.27, 37.87],
  submit: true
})
)});
  main.variable(observer("coords2")).define("coords2", ["Generators", "viewof coords2"], (G, _) => G.input(_));
  main.variable(observer()).define(["coords2"], function(coords2){return(
coords2
)});
  main.variable(observer("coordinates")).define("coordinates", ["html","input"], function(html,input){return(
function coordinates(config = {}) {
  const { value = [], title, description, submit } = Array.isArray(config)
    ? { value: config }
    : config;
  let [lon, lat] = value;
  lon = lon != null ? lon : "";
  lat = lat != null ? lat : "";
  const lonEl = html`<input name="input" type="number" autocomplete="off" min="-180" max="180" style="width: 80px;" step="any" value="${lon}" />`;
  const latEl = html`<input name="input" type="number" autocomplete="off" min="-90" max="90" style="width: 80px;" step="any" value="${lat}" />`;
  const form = input({
    type: "coordinates",
    title,
    description,
    submit,
    getValue: () => {
      const lon = lonEl.valueAsNumber;
      const lat = latEl.valueAsNumber;
      return [isNaN(lon) ? null : lon, isNaN(lat) ? null : lat];
    },
    form: html`
      <form>
        <label style="display: inline-block; font: 600 0.8rem sans-serif; margin: 6px 0 3px;">
          <span style="display: inline-block; width: 70px;">Longitude:</span>
          ${lonEl}
        </label>
        <br>
        <label style="display: inline-block; font: 600 0.8rem sans-serif; margin: 0 0 6px;">
          <span style="display: inline-block; width: 70px;">Latitude:</span>
          ${latEl}
        </label>
      </form>
    `
  });
  form.output.remove();
  return form;
}
)});
  main.variable(observer("worldMapCoordinatesDemo")).define("worldMapCoordinatesDemo", ["md"], function(md){return(
md` ---
## World Map Coordinates

*value: an array pair of \`[longitude, latitude]\`, e.g. * \`[-122.27, 37.87]\` 

~~~js
import {worldMapCoordinates} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof worldMap1")).define("viewof worldMap1", ["worldMapCoordinates"], function(worldMapCoordinates){return(
worldMapCoordinates([-122.27, 37.87])
)});
  main.variable(observer("worldMap1")).define("worldMap1", ["Generators", "viewof worldMap1"], (G, _) => G.input(_));
  main.variable(observer()).define(["worldMap1"], function(worldMap1){return(
worldMap1
)});
  main.variable(observer("worldMapCoordinates")).define("worldMapCoordinates", ["html","DOM","d3geo","graticule","land","countries","input"], function(html,DOM,d3geo,graticule,land,countries,input){return(
function worldMapCoordinates(config = {}) {
  const {
    value = [], title, description, width = 400
  } = Array.isArray(config) ? {value: config} : config;
  const height = Math.round((210 / 400) * width);
  let [lon, lat] = value;
  lon = lon != null ? lon : null;
  lat = lat != null ? lat : null;
  const formEl = html`<form style="width: ${width}px;"></form>`;
  const context = DOM.context2d(width, height);
  const canvas = context.canvas;
  canvas.style.margin = "10px 0 3px";
  const projection = d3geo
    .geoNaturalEarth1()
    .precision(0.1)
    .fitSize([width, height], { type: "Sphere" });
  const path = d3geo.geoPath(projection, context).pointRadius(2.5);
  formEl.append(canvas);

  function draw() {
    context.fillStyle = "#fff";
    context.fillRect(0, 0, width, height);
    context.beginPath();
    path(graticule);
    context.lineWidth = 0.35;
    context.strokeStyle = `#ddd`;
    context.stroke();
    context.beginPath();
    path(land);
    context.fillStyle = `#f4f4f4`;
    context.fill();
    context.beginPath();
    path(countries);
    context.strokeStyle = `#aaa`;
    context.stroke();
    if (lon != null && lat != null) {
      const pointPath = { type: "MultiPoint", coordinates: [[lon, lat]] };
      context.beginPath();
      path(pointPath);
      context.fillStyle = `#f00`;
      context.fill();
    }
  }

  canvas.onclick = function(ev) {
    const { offsetX, offsetY } = ev;
    var coords = projection.invert([offsetX, offsetY]);
    lon = +coords[0].toFixed(2);
    lat = +coords[1].toFixed(2);
    draw();
    canvas.dispatchEvent(new CustomEvent("input", { bubbles: true }));
  };

  draw();

  const form = input({
    type: "worldMapCoordinates",
    title,
    description,
    display: v =>
      html`<div style="width: ${width}px; white-space: nowrap; color: #444; text-align: center; font: 13px sans-serif; margin-bottom: 5px;">
            <span style="color: #777;">Longitude:</span> ${lon != null ? lon.toFixed(2) : ""}
            &nbsp; &nbsp; 
            <span style="color: #777;">Latitude:</span> ${lat != null ? lat.toFixed(2) : ""} 
          </div>`,
    getValue: () => [lon != null ? lon : null, lat != null ? lat : null],
    form: formEl
  });
  return form;
}
)});
  main.variable(observer("usaMapCoordinatesDemo")).define("usaMapCoordinatesDemo", ["md"], function(md){return(
md` ---
## U.S.A. Map Coordinates

*value: an array pair of \`[longitude, latitude]\`, e.g. * \`[-122.27, 37.87]\` 

~~~js
import {usaMapCoordinates} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof usaMap1")).define("viewof usaMap1", ["usaMapCoordinates"], function(usaMapCoordinates){return(
usaMapCoordinates([-122.27, 37.87])
)});
  main.variable(observer("usaMap1")).define("usaMap1", ["Generators", "viewof usaMap1"], (G, _) => G.input(_));
  main.variable(observer()).define(["usaMap1"], function(usaMap1){return(
usaMap1
)});
  main.variable(observer("viewof usaMap2")).define("viewof usaMap2", ["usaMapCoordinates"], function(usaMapCoordinates){return(
usaMapCoordinates({
  title: "A Mini Map",
  description: "Defaults to New York City",
  width: 200,
  value: [-74, 40.71]
})
)});
  main.variable(observer("usaMap2")).define("usaMap2", ["Generators", "viewof usaMap2"], (G, _) => G.input(_));
  main.variable(observer()).define(["usaMap2"], function(usaMap2){return(
usaMap2
)});
  main.variable(observer("usaMapCoordinates")).define("usaMapCoordinates", ["html","DOM","d3geo","nation","states","input"], function(html,DOM,d3geo,nation,states,input){return(
function usaMapCoordinates(config = {}) {
  const {
    value = [], title, description, width = 400
  } = Array.isArray(config) ? {value: config} : config;
  const scale = width / 960;
  const height = scale * 600;
  let [lon, lat] = value;
  lon = lon != null ? lon : null;
  lat = lat != null ? lat : null;
  const formEl = html`<form style="width: ${width}px;"></form>`;
  const context = DOM.context2d(width, height);
  const canvas = context.canvas;
  canvas.style.margin = "5px 0 20px";
  const projection = d3geo
    .geoAlbersUsa()
    .scale(1280)
    .translate([480, 300]);
  const path = d3geo
    .geoPath()
    .context(context)
    .pointRadius(2.5 / scale);
  formEl.append(canvas);

  function draw() {
    context.clearRect(0, 0, width, height);
    context.save();
    context.scale(scale, scale);
    context.lineWidth = 0.35 / scale;
    context.beginPath();
    path(nation);
    context.fillStyle = `#f4f4f4`;
    context.fill();
    context.beginPath();
    path(states);
    context.strokeStyle = `#aaa`;
    context.stroke();
    if (lon != null && lat != null) {
      const pointPath = {
        type: "MultiPoint",
        coordinates: [projection([lon, lat])]
      };
      context.beginPath();
      path(pointPath);
      context.fillStyle = `#f00`;
      context.fill();
    }
    context.restore();
  }

  canvas.onclick = function(ev) {
    const { offsetX, offsetY } = ev;
    var coords = projection.invert([offsetX / scale, offsetY / scale]);
    lon = +coords[0].toFixed(2);
    lat = +coords[1].toFixed(2);
    draw();
    canvas.dispatchEvent(new CustomEvent("input", { bubbles: true }));
  };

  draw();

  const form = input({
    type: "worldMapCoordinates",
    title,
    description,
    display: v =>
      html`<div style="position: absolute; width: ${width}px; white-space: nowrap; color: #444; text-align: center; font: 13px sans-serif; margin-top: -18px;">
            <span style="color: #777;">Longitude:</span> ${lon != null ? lon : ""}
            &nbsp; &nbsp; 
            <span style="color: #777;">Latitude:</span> ${lat != null ? lat : ""} 
          </div>`,
    getValue: () => [lon != null ? lon : null, lat != null ? lat : null],
    form: formEl
  });
  return form;
}
)});
  main.variable(observer("dateDemo")).define("dateDemo", ["md"], function(md){return(
md` ---
## Dates

*value: a YYYY-MM-DD formatted string: * \`"2016-11-08"\` 

~~~js
import {date} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof d")).define("viewof d", ["date"], function(date){return(
date()
)});
  main.variable(observer("d")).define("d", ["Generators", "viewof d"], (G, _) => G.input(_));
  main.variable(observer("viewof d1")).define("viewof d1", ["date"], function(date){return(
date({
  title: "2017", 
  min: "2017-01-01",
  max: "2017-12-31",
  value: "2017-01-01",
  description: "Only dates within the 2017 calendar year are allowed"
})
)});
  main.variable(observer("d1")).define("d1", ["Generators", "viewof d1"], (G, _) => G.input(_));
  main.variable(observer("date")).define("date", ["input"], function(input){return(
function date(config = {}) {
  const { min, max, value, title, description, disabled, display } =
    typeof config === "string" ? { value: config } : config;
  return input({
    type: "date",
    title,
    description,
    display,
    attributes: { min, max, disabled, value }
  });
}
)});
  main.variable(observer("timeDemo")).define("timeDemo", ["md"], function(md){return(
md` ---
## Times

*value: a HH:MM:SS formatted string: * \`"09:30:45"\`
<br>*(Time values are always in 24-hour format)*

~~~js
import {time} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof t")).define("viewof t", ["time"], function(time){return(
time()
)});
  main.variable(observer("t")).define("t", ["Generators", "viewof t"], (G, _) => G.input(_));
  main.variable(observer()).define(["t"], function(t){return(
t
)});
  main.variable(observer("viewof t1")).define("viewof t1", ["time"], function(time){return(
time({
  title: "Afternoon",
  min: "12:00:00",
  max: "23:59:59",
  value: "13:00:00",
  step: 1,
  description: "Only times after noon are allowed, and seconds are included"
})
)});
  main.variable(observer("t1")).define("t1", ["Generators", "viewof t1"], (G, _) => G.input(_));
  main.variable(observer()).define(["t1"], function(t1){return(
t1
)});
  main.variable(observer("time")).define("time", ["input"], function(input){return(
function time(config = {}) {
  const { min, max, step, value, title, description, disabled, display } =
    typeof config === "string" ? { value: config } : config;
  const el = input({
    type: "time",
    title,
    description,
    display,
    getValue: d => (d.value ? d.value : undefined),
    attributes: { min, max, step, disabled, value }
  });
  el.output.remove();
  return el;
}
)});
  main.variable(observer("fileDemo")).define("fileDemo", ["md"], function(md){return(
md`---
## File Upload
*Use the JavaScript [File API](https://developer.mozilla.org/en-US/docs/Web/API/File/Using_files_from_web_applications) to work with uploaded file contents.*

\`import {file} from "@jashkenas/inputs"\``
)});
  main.variable(observer("viewof e")).define("viewof e", ["file"], function(file){return(
file()
)});
  main.variable(observer("e")).define("e", ["Generators", "viewof e"], (G, _) => G.input(_));
  main.variable(observer("viewof e1")).define("viewof e1", ["file"], function(file){return(
file({
  title: "Photographs",
  description: "Only .jpg files are allowed in this example. Choose some images, and they’ll appear in the cell below.",
  accept: ".jpg",
  multiple: true,
})
)});
  main.variable(observer("e1")).define("e1", ["Generators", "viewof e1"], (G, _) => G.input(_));
  main.variable(observer()).define(["html","e1","Files"], async function(html,e1,Files)
{
  const div = html`<div>`;
  for (var j = 0; j < e1.length; j++) {
    let file = e1[j];
    let img = html`<img height="125px" style="margin: 2px;" />`;
    img.src = await Files.url(e1[j]);
    div.append(img);
  }
  return div;
}
);
  main.variable(observer("file")).define("file", ["input"], function(input){return(
function file(config = {}) {
  const { multiple, accept, title, description, disabled } = config;
  const form = input({
    type: "file",
    title,
    description,
    attributes: { multiple, accept, disabled },
    action: form => {
      form.input.onchange = () => {
        form.value = multiple ? form.input.files : form.input.files[0];
        form.dispatchEvent(new CustomEvent("input"));
      };
    }
  });
  form.output.remove();
  form.input.onchange();
  return form;
}
)});
  main.variable(observer("textDemo")).define("textDemo", ["md"], function(md){return(
md`---
## Text Inputs

~~~js
import {text} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof f")).define("viewof f", ["text"], function(text){return(
text()
)});
  main.variable(observer("f")).define("f", ["Generators", "viewof f"], (G, _) => G.input(_));
  main.variable(observer("viewof f1")).define("viewof f1", ["text"], function(text){return(
text({title: "A Text Input", placeholder: "Placeholder text", description: "Note that text inputs don’t show output on the right"})
)});
  main.variable(observer("f1")).define("f1", ["Generators", "viewof f1"], (G, _) => G.input(_));
  main.variable(observer()).define(["f1"], function(f1){return(
f1
)});
  main.variable(observer("viewof f2")).define("viewof f2", ["text"], function(text){return(
text({placeholder: "Placeholder text", description: "This input only changes value on submit", submit: "Go"})
)});
  main.variable(observer("f2")).define("f2", ["Generators", "viewof f2"], (G, _) => G.input(_));
  main.variable(observer()).define(["f2"], function(f2){return(
f2
)});
  main.variable(observer("text")).define("text", ["input"], function(input){return(
function text(config = {}) {
  const {
    value,
    title,
    description,
    disabled,
    autocomplete = "off",
    maxlength,
    minlength,
    pattern,
    placeholder,
    size,
    submit,
    getValue
  } = typeof config === "string" ? { value: config } : config;
  const form = input({
    type: "text",
    title,
    description,
    submit,
    getValue,
    attributes: {
      value,
      autocomplete,
      maxlength,
      minlength,
      pattern,
      placeholder,
      size,
      disabled
    }
  });
  form.output.remove();
  form.input.style.fontSize = "1em";
  return form;
}
)});
  main.variable(observer("textareaDemo")).define("textareaDemo", ["md"], function(md){return(
md`---
## Textareas

~~~js
import {textarea} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof g")).define("viewof g", ["textarea"], function(textarea){return(
textarea()
)});
  main.variable(observer("g")).define("g", ["Generators", "viewof g"], (G, _) => G.input(_));
  main.variable(observer()).define(["g"], function(g){return(
g
)});
  main.variable(observer("viewof g1")).define("viewof g1", ["textarea"], function(textarea){return(
textarea({
  title: "Your Great American Novel", 
  placeholder: "Insert story here...", 
  spellcheck: true,
  width: "100%",
  rows: 10,
  submit: "Publish"
})
)});
  main.variable(observer("g1")).define("g1", ["Generators", "viewof g1"], (G, _) => G.input(_));
  main.variable(observer()).define(["g1"], function(g1){return(
g1
)});
  main.variable(observer("textarea")).define("textarea", ["input","html"], function(input,html){return(
function textarea(config = {}) {
  const {
    value = "",
    title,
    description,
    autocomplete,
    cols = 45,
    rows = 3,
    width,
    height,
    maxlength,
    placeholder,
    spellcheck,
    wrap,
    submit,
    disabled,
    getValue
  } = typeof config === "string" ? { value: config } : config;
  const form = input({
    form: html`<form><textarea style="display: block; font-size: 0.8em;" name=input>${value}</textarea></form>`,
    title,
    description,
    submit,
    getValue,
    attributes: {
      autocomplete,
      cols,
      rows,
      maxlength,
      placeholder,
      spellcheck,
      wrap,
      disabled
    }
  });
  form.output.remove();
  if (width != null) form.input.style.width = width;
  if (height != null) form.input.style.height = height;
  if (submit) form.submit.style.margin = "0";
  if (title || description) form.input.style.margin = "3px 0";
  return form;
}
)});
  main.variable(observer("radioDemo")).define("radioDemo", ["md"], function(md){return(
md`---
## Radio Buttons

~~~js
import {radio} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof r")).define("viewof r", ["radio"], function(radio){return(
radio(["Lust", "Gluttony", "Greed", "Sloth", "Wrath", "Envy", "Pride"])
)});
  main.variable(observer("r")).define("r", ["Generators", "viewof r"], (G, _) => G.input(_));
  main.variable(observer()).define(["r"], function(r){return(
r
)});
  main.variable(observer("viewof r1")).define("viewof r1", ["radio"], function(radio){return(
radio({
  title: 'Contact Us',
  description: 'Please select your preferred contact method',
  options: [
    { label: 'By Email', value: 'email' },
    { label: 'By Phone', value: 'phone' },
    { label: 'By Pager', value: 'pager' },
  ],
  value: 'pager'
})
)});
  main.variable(observer("r1")).define("r1", ["Generators", "viewof r1"], (G, _) => G.input(_));
  main.variable(observer()).define(["r1"], function(r1){return(
r1
)});
  main.variable(observer("radio")).define("radio", ["input","html"], function(input,html){return(
function radio(config = {}) {
  let {
    value: formValue,
    title,
    description,
    submit,
    options,
    disabled
  } = Array.isArray(config) ? { options: config } : config;
  options = options.map(o =>
    typeof o === "string" ? { value: o, label: o } : o
  );
  const form = input({
    type: "radio",
    title,
    description,
    submit,
    getValue: input => {
      if (input.checked) return input.value;
      const checked = Array.prototype.find.call(input, radio => radio.checked);
      return checked ? checked.value : undefined;
    },
    form: html`
      <form>
        ${options.map(({ value, label }, i) => {
          const input = html`<input type=radio name=input ${
            value === formValue ? "checked" : ""
          } style="vertical-align: top; ${
            i === 0 ? `margin-left: 1px;` : ``
          }" />`;
          input.setAttribute("value", value);
          if (disabled) input.setAttribute("value", disabled);
          const tag = html`
          <label style="display: inline-block; margin: 5px 10px 3px 0; font-size: 0.85em;">
           ${input}
           ${label}
          </label>`;
          return tag;
        })}
      </form>
    `
  });
  form.output.remove();
  return form;
}
)});
  main.variable(observer("checkboxDemo")).define("checkboxDemo", ["md"], function(md){return(
md`---
## Checkboxes

~~~js
import {checkbox} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof ch")).define("viewof ch", ["checkbox"], function(checkbox){return(
checkbox(["Lust", "Gluttony", "Greed", "Sloth", "Wrath", "Envy", "Pride"])
)});
  main.variable(observer("ch")).define("ch", ["Generators", "viewof ch"], (G, _) => G.input(_));
  main.variable(observer()).define(["ch"], function(ch){return(
ch
)});
  main.variable(observer("viewof ch1")).define("viewof ch1", ["checkbox"], function(checkbox){return(
checkbox({
  title: "Colors",
  description: "Please select your favorite colors",
  options: [
    { value: "r", label: "Red" },
    { value: "o", label: "Orange" },
    { value: "y", label: "Yellow" },
    { value: "g", label: "Green" },
    { value: "b", label: "Blue" },
    { value: "i", label: "Indigo" },
    { value: "v", label: "Violet" }
  ],
  value: ["r", "g", "b"],
  submit: true
})
)});
  main.variable(observer("ch1")).define("ch1", ["Generators", "viewof ch1"], (G, _) => G.input(_));
  main.variable(observer()).define(["ch1"], function(ch1){return(
ch1
)});
  main.variable(observer("viewof ch3")).define("viewof ch3", ["checkbox"], function(checkbox){return(
checkbox({
  description: "Just a single checkbox to toggle",
  options: [{ value: "toggle", label: "On" }],
  value: "toggle"
})
)});
  main.variable(observer("ch3")).define("ch3", ["Generators", "viewof ch3"], (G, _) => G.input(_));
  main.variable(observer()).define(["ch3"], function(ch3){return(
ch3
)});
  main.variable(observer("checkbox")).define("checkbox", ["input","html"], function(input,html){return(
function checkbox(config = {}) {
  let {
    value: formValue,
    title,
    description,
    submit,
    disabled,
    options
  } = Array.isArray(config) ? { options: config } : config;
  options = options.map(o =>
    typeof o === "string" ? { value: o, label: o } : o
  );
  const form = input({
    type: "checkbox",
    title,
    description,
    submit,
    getValue: input => {
      if (input.length)
        return Array.prototype.filter
          .call(input, i => i.checked)
          .map(i => i.value);
      return input.checked ? input.value : false;
    },
    form: html`
      <form>
        ${options.map(({ value, label }, i) => {
          const input = html`<input type=checkbox name=input ${
            (formValue || []).indexOf(value) > -1 ? "checked" : ""
          } style="vertical-align: top; ${
            i === 0 ? `margin-left: 1px;` : ``
          }" />`;
          input.setAttribute("value", value);
          if (disabled) input.setAttribute("disabled", disabled);
          const tag = html`<label style="display: inline-block; margin: 5px 10px 3px 0; font-size: 0.85em;">
           ${input}
           ${label}
          </label>`;
          return tag;
        })}
      </form>
    `
  });
  form.output.remove();
  return form;
}
)});
  main.variable(observer("numberDemo")).define("numberDemo", ["md"], function(md){return(
md`---
## Numbers

~~~js
import {number} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof h")).define("viewof h", ["number"], function(number){return(
number()
)});
  main.variable(observer("h")).define("h", ["Generators", "viewof h"], (G, _) => G.input(_));
  main.variable(observer()).define(["h"], function(h){return(
h
)});
  main.variable(observer("viewof h1")).define("viewof h1", ["number"], function(number){return(
number({placeholder: "13+", title: "Your Age", submit: true})
)});
  main.variable(observer("h1")).define("h1", ["Generators", "viewof h1"], (G, _) => G.input(_));
  main.variable(observer()).define(["h1"], function(h1){return(
h1
)});
  main.variable(observer("number")).define("number", ["input"], function(input){return(
function number(config = {}) {
  const {
    value,
    title,
    description,
    disabled,
    placeholder,
    submit,
    step = "any",
    min,
    max
  } =
    typeof config === "number" || typeof config === "string"
      ? { value: +config }
      : config;
  const form = input({
    type: "number",
    title,
    description,
    submit,
    attributes: {
      value,
      placeholder,
      step,
      min,
      max,
      autocomplete: "off",
      disabled
    },
    getValue: input => input.valueAsNumber
  });
  form.output.remove();
  form.input.style.width = "auto";
  form.input.style.fontSize = "1em";
  return form;
}
)});
  main.variable(observer("passwordDemo")).define("passwordDemo", ["md"], function(md){return(
md`---
## Passwords

~~~js
import {password} from "@jashkenas/inputs"
~~~`
)});
  main.variable(observer("viewof i")).define("viewof i", ["password"], function(password){return(
password({value: "password"})
)});
  main.variable(observer("i")).define("i", ["Generators", "viewof i"], (G, _) => G.input(_));
  main.variable(observer()).define(["i"], function(i){return(
i
)});
  main.variable(observer("viewof i1")).define("viewof i1", ["password"], function(password){return(
password({
  title: "Your super secret password", 
  description: "Less than 12 characters, please.",
  minlength: 6,
  maxlength: 12
})
)});
  main.variable(observer("i1")).define("i1", ["Generators", "viewof i1"], (G, _) => G.input(_));
  main.variable(observer()).define(["i1"], function(i1){return(
i1
)});
  main.variable(observer("password")).define("password", ["input"], function(input){return(
function password(config = {}) {
  const {
    value,
    title,
    description,
    disabled,
    autocomplete = "off",
    maxlength,
    minlength,
    pattern,
    placeholder,
    size,
    submit
  } = typeof config === "string" ? { value: config } : config;
  const form = input({
    type: "password",
    title,
    description,
    submit,
    attributes: {
      value,
      autocomplete,
      maxlength,
      minlength,
      pattern,
      placeholder,
      size,
      disabled
    }
  });
  form.output.remove();
  form.input.style.fontSize = "1em";
  return form;
}
)});
  main.variable(observer()).define(["md"], function(md){return(
md`---
## Wishlist (Send suggestions, please!)

* 3D coordinate input (for say, positioning a camera in a WebGL sketch)
* Geocoder search with location autocomplete that returns longitude and latitude.
* Degrees or radians input, for circular things, or angles.
* A dimensions input, or a box-model input, with margin (and optionally, padding).
* A map-projection-picker input, rendering little thumbnails of all the d3-geo-projections.
* Drag and drop file upload input.
* Alternative coordinate inputs, e.g. Right Ascension, Declination.
* Other useful formatting options.

---`
)});
  main.variable(observer("input")).define("input", ["html","d3format"], function(html,d3format){return(
function input(config) {
  let {
    form,
    type = "text",
    attributes = {},
    action,
    getValue,
    title,
    description,
    format,
    display,
    submit,
    options
  } = config;
  const wrapper = html`<div></div>`;
  if (!form)
    form = html`<form>
	<input name=input type=${type} />
  </form>`;
  Object.keys(attributes).forEach(key => {
    const val = attributes[key];
    if (val != null) form.input.setAttribute(key, val);
  });
  if (submit)
    form.append(
      html`<input name=submit type=submit style="margin: 0 0.75em" value="${
        typeof submit == "string" ? submit : "Submit"
      }" />`
    );
  form.append(
    html`<output name=output style="font: 14px Menlo, Consolas, monospace; margin-left: 0.5em;"></output>`
  );
  if (title)
    form.prepend(
      html`<div style="font: 700 0.9rem sans-serif; margin-bottom: 3px;">${title}</div>`
    );
  if (description)
    form.append(
      html`<div style="font-size: 0.85rem; font-style: italic; margin-top: 3px;">${description}</div>`
    );
  if (format)
    format = typeof format === "function" ? format : d3format.format(format);
  if (action) {
    action(form);
  } else {
    const verb = submit
      ? "onsubmit"
      : type == "button"
      ? "onclick"
      : type == "checkbox" || type == "radio"
      ? "onchange"
      : "oninput";
    form[verb] = e => {
      e && e.preventDefault();
      const value = getValue ? getValue(form.input) : form.input.value;
      if (form.output) {
        const out = display ? display(value) : format ? format(value) : value;
        if (out instanceof window.Element) {
          while (form.output.hasChildNodes()) {
            form.output.removeChild(form.output.lastChild);
          }
          form.output.append(out);
        } else {
          form.output.value = out;
        }
      }
      form.value = value;
      if (verb !== "oninput")
        form.dispatchEvent(new CustomEvent("input", { bubbles: true }));
    };
    if (verb !== "oninput")
      wrapper.oninput = e => e && e.stopPropagation() && e.preventDefault();
    if (verb !== "onsubmit") form.onsubmit = e => e && e.preventDefault();
    form[verb]();
  }
  while (form.childNodes.length) {
    wrapper.appendChild(form.childNodes[0]);
  }
  form.append(wrapper);
  return form;
}
)});
  main.variable(observer("d3geo")).define("d3geo", ["require"], function(require){return(
require("d3-geo@1")
)});
  main.variable(observer("d3format")).define("d3format", ["require"], function(require){return(
require("d3-format@1")
)});
  main.variable(observer("topojson")).define("topojson", ["require"], function(require){return(
require("topojson-client@3")
)});
  main.variable(observer("world")).define("world", async function(){return(
(await fetch("https://cdn.jsdelivr.net/npm/world-atlas@1/world/110m.json")).json()
)});
  main.variable(observer("land")).define("land", ["topojson","world"], function(topojson,world){return(
topojson.feature(world, world.objects.land)
)});
  main.variable(observer("countries")).define("countries", ["topojson","world"], function(topojson,world){return(
topojson.feature(world, world.objects.countries)
)});
  main.variable(observer("usa")).define("usa", async function(){return(
(await fetch("https://cdn.jsdelivr.net/npm/us-atlas@^2.1/us/states-10m.json")).json()
)});
  main.variable(observer("nation")).define("nation", ["topojson","usa"], function(topojson,usa){return(
topojson.feature(usa, usa.objects.nation)
)});
  main.variable(observer("states")).define("states", ["topojson","usa"], function(topojson,usa){return(
topojson.feature(usa, usa.objects.states)
)});
  main.variable(observer("graticule")).define("graticule", ["d3geo"], function(d3geo){return(
d3geo.geoGraticule10()
)});
  main.variable(observer("viewof license")).define("viewof license", ["md"], function(md)
{
  const license = md`License: [MIT](https://opensource.org/licenses/MIT)`;
  license.value = "MIT";
  return license;
}
);
  main.variable(observer("license")).define("license", ["Generators", "viewof license"], (G, _) => G.input(_));
  main.variable(observer()).define(["md"], function(md){return(
md`*Clip art courtesy [ClipArt ETC](https://etc.usf.edu/clipart/), radio buttons and checkboxes courtesy [Amit Sch](https://observablehq.com/@meetamit/multiple-choice-inputs).*`
)});
  return main;
}
