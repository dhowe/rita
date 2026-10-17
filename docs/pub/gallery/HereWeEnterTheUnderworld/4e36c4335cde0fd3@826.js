// https://observablehq.com/@observablehq/a-taste-of-observable@826
import define1 from "./1879ef09e4c28141@643.js";
import define2 from "./e93997d5089d7165@2303.js";
import define3 from "./60ea978986bfd25e@1624.js";
import define4 from "./7764a40fe6b83ca1@427.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  const fileAttachments = new Map([["image@1.png",new URL("./files/46c8df99316e9926d90ff847b4aa5cc4755ec8a1699f2d81ee6daec11e397e0bf090556bb9488461ed942a251f0ca8b4eb9b2b0281065bd5b13cac54b548ae17",import.meta.url)],["canned-forecast.json",new URL("./files/a033960c84e9ea9d99675223913e00af5ced5d2e833762a3cd2bdac843795ec672ac61b9f27e3a8a1719de6bdd5fa7363fc1cd05aa51c164b88a4aa170a650a0",import.meta.url)]]);
  main.builtin("FileAttachment", runtime.fileAttachments(name => fileAttachments.get(name)));
  main.variable(observer()).define(["md"], function(md){return(
md`# A Taste of Observable

Hello and welcome to Observable! 👋`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Observable helps you sketch with live data, prototype visualizations, connect to Web APIs, share and reuse techniques and components with a friendly community of other authors, and publish your work for the world to see.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`A notebook is made up of a series of cells, and each cell is defined by its JavaScript source code.

👈 Click the margin to the left of any cell (including this one!), to toggle it open and closed, and see, and even edit, the source that lies below.

Let’s start by loading up some data. We’re going to use weather forecast data for the purposes of this example. After getting a taste of Observable, you can use similar techniques on the data you care about.

Here, we have a cell containing a recent forecast from the weather station on Belvedere Castle in Central Park, New York City:`
)});
  main.variable(observer("nycForecast")).define("nycForecast", ["FileAttachment"], function(FileAttachment){return(
FileAttachment("canned-forecast.json").json()
)});
  main.variable(observer()).define(["md","caret"], function(md,caret){return(
md`👆 This is a snapshot of raw data from the National Weather Service, unprocessed and full of crufty metadata describing different attributes of the weather forecast. You can explore it yourself by clicking into the carets: ${caret()}`
)});
  main.variable(observer()).define(["md","code"], function(md,code){return(
md`Prefer live data instead? No problem. We can do that by fetching directly from ${code(`api.weather.gov`)}. (We’ve attached a snapshot of this data to this notebook so the notebook will continue working if the API is unavailable.)`
)});
  main.variable(observer()).define(function(){return(
fetch("https://api.weather.gov/gridpoints/OKX/33,37/forecast").then(response => response.json())
)});
  main.variable(observer()).define(["md","caret"], function(md,caret){return(
md`Let’s drill down to the actual weather forecast.

👇 Try inspecting the data in \`nycForecastPeriods\` by clicking on ${caret()}\`Array(14)\`, and then toggle open some of the specific forecasts over the week to come.`
)});
  main.variable(observer("nycForecastPeriods")).define("nycForecastPeriods", ["nycForecast"], function(nycForecast){return(
nycForecast.properties.periods
)});
  main.variable(observer()).define(["md"], function(md){return(
md`You’ll notice that they include the forecasted temperature, a description of what the weather is going to do, information about wind speed, and even something called \`icon\`.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Let’s make that forecast easier to read by taking the next few days of weather and turning it into a table:`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`### New York City weather forecast`
)});
  main.variable(observer()).define(["table","nycForecastPeriods","md","html"], function(table,nycForecastPeriods,md,html){return(
table(
  nycForecastPeriods.slice(0, 7).map(
    ({ name, temperature, icon, detailedForecast, shortForecast }) => ({
      Day: md`**${name}**`,
      Temp: md`**${temperature}&nbsp;°F**`,
      Icon: html`<img width=70 src="${icon}" />`,
      Forecast: detailedForecast
    })
  )
)
)});
  main.variable(observer()).define(["md","code","run"], function(md,code,run){return(
md`👆 In the code of the cell above, try replacing ${code(
  `Forecast: detailedForecast`
)} with ${code(
  `Forecast: shortForecast`
)}. Then press the blue play button ${run()} or use Shift-Return to run your change. What happens?

...

You’ll notice that the table above reacts, displaying a \`shortForecast\` instead of the \`detailedForecast\` that it contained previously.

This reactivity is the heart of what makes Observable notebooks a special environment for exploration. Whenever you change anything, or anything changes by itself, the rest of the notebook instantly updates to reflect the latest information. In technical terms, this is called reactive, or dataflow programming. But in practical terms, it means that your notebooks never get stuck in a broken state, and that you never have to refresh the page. Reactivity gives you immediate feedback when you are exploring your data, sketching ideas in code, and collaborating with others.

Once you start sketching ideas in a reactive, web-enabled notebook, it’s hard to go back to scripts,  spreadsheets and web servers.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Let’s continue by putting that same NYC forecast data into a plot. We’ll use Vega-Lite, a simple charting library, to draw the forecasted temperatures over the coming week. The daytime temperatures are marked in orange, and the forecasted nighttime temperatures in blue.`
)});
  main.variable(observer()).define(["vl","nycForecastPeriods"], function(vl,nycForecastPeriods){return(
vl
  .markCircle()               // Make a plot of circles
  .data(nycForecastPeriods)   // Using the NYC forecast data
  .encode(
    vl
      .x()                    // For the X axis
      .fieldN('name')         // Use "name"
      .sort(null),            // But don’t sort alphabetically
    vl
      .y()                    // For the Y axis
      .fieldQ('temperature'), // Use "temperature"
    vl
      .color()                // For the color
      .fieldN('isDaytime')    // Use "isDaytime"
  )
  .render()
)});
  main.variable(observer()).define(["md","code","run"], function(md,code,run){return(
md`👆 In the code of the cell above, try replacing ${code(
  `markCircle()`
)} with ${code(
  `markSquare()`
)}. Then press the blue play button ${run()} or use Shift-Return to run your change. What happens? How about ${code(
  `markPoint()`
)} ?`
)});
  main.variable(observer()).define(["nycForecastPeriods","md"], function(nycForecastPeriods,md)
{
  const [now, _, later] = nycForecastPeriods;
  const trend = later.temperature - now.temperature < 0 ? `colder` : `warmer`;
  return md`Of course, you can use data to drive prose just as easily as visualizations. For example, from the chart and table above, you can see how in New York City, it is going to be ${trend} on ${later.name} than it is ${now.name}. Click on the left margin 👈 to see how I’m using data from the forecast to generate the text for this paragraph, awkward capitalization and all.`
}
);
  main.variable(observer()).define(["md"], function(md){return(
md`But perhaps you don't live in New York? (Sadly, I no longer do.) 

Let’s make a version that:

- Allows you to pick any location in the United States.
- Uses the Weather.gov API to find the nearest weather station.
- Renders the current forecast into our table and chart.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`We need to start with a longitude and latitude pair. You could write this by hand, like: \`[-73.7, 40.8]\`, but it takes at least five seconds and another browser tab to Google for coordinates, so we’ll do something more convenient by importing a handy map widget from [an existing notebook](https://observablehq.com/@jashkenas/inputs#usaMapCoordinates). `
)});
  main.variable(observer("viewof coordinates")).define("viewof coordinates", ["usaMapCoordinates"], function(usaMapCoordinates){return(
usaMapCoordinates({
  value: [-122.27, 37.87],  // The default location: Berkeley, CA.
  width: 350, 
  title: "Pick a location, see the weather forecast"
})
)});
  main.variable(observer("coordinates")).define("coordinates", ["Generators", "viewof coordinates"], (G, _) => G.input(_));
  main.variable(observer()).define(["md"], function(md){return(
md`Now, when you click on the map above 👆, watch how the data flows through to the coordinates data below 👇. You may notice that the left margin flashes whenever a cell receives new data and runs again.`
)});
  main.variable(observer()).define(["coordinates"], function(coordinates){return(
coordinates
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Here, the \`coordinates\` flow into a request to the National Weather Service API, to find the closest weather station. (Again, a flash of the left margin.)`
)});
  main.variable(observer("weatherStation")).define("weatherStation", ["coordinates"], async function(coordinates)
{
  const [lng, lat] = coordinates;
  return (await fetch(`https://api.weather.gov/points/${[lat, lng]}`)).json()
}
);
  main.variable(observer()).define(["md","place"], function(md,place){return(
md`Looks like you picked a point near **${place}**.`
)});
  main.variable(observer("place")).define("place", ["weatherStation"], function(weatherStation)
{
  const {city, state} = weatherStation.properties.relativeLocation.properties;
  return `${city}, ${state}`;
}
);
  main.variable(observer()).define(["md","place","caret"], function(md,place,caret){return(
md`Now, we’ll use the \`weatherStation\`’s \`forecast\` URL to retrieve the current forecast for ${place}. This data has exactly the same shape as the NYC forecast at the top of the page. As before, click on the caret ${caret()} to explore the raw data.`
)});
  main.variable(observer("localForecast")).define("localForecast", ["weatherStation"], async function(weatherStation){return(
(await fetch(weatherStation.properties.forecast)).json()
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Here’s our formatted weather table:`
)});
  main.variable(observer()).define(["md","place"], function(md,place){return(
md`### Current weather forecast for ${place}`
)});
  main.variable(observer()).define(["table","localForecast","md","html"], function(table,localForecast,md,html){return(
table(
  localForecast.properties.periods.slice(0, 7).map(
    ({ name, temperature, icon, detailedForecast, shortForecast }) => ({
      Day: md`**${name}**`,
      Temp: md`**${temperature}&nbsp;°F**`,
      Icon: html`<img width=70 src="${icon}" />`,
      Forecast: detailedForecast
    })
  )
)
)});
  main.variable(observer()).define(["md"], function(md){return(
md`And our daytime and nighttime forecasted temperature chart:`
)});
  main.variable(observer()).define(["md","place"], function(md,place){return(
md`### Forecasted temperature chart for ${place}`
)});
  main.variable(observer()).define(["vl","localForecast","domain"], function(vl,localForecast,domain){return(
vl
  .markCircle()               
  .data(localForecast.properties.periods)
  .encode(
    vl.x().fieldN('name').sort(null),            
    vl.y().scale(domain).fieldQ('temperature'), 
    vl.color().fieldN('isDaytime')    
  )
  .render()
)});
  main.variable(observer()).define(["md"], function(md){return(
md`If you scroll back up and pick a different location, you’ll notice that the table and chart will have automatically updated within a second or two — the amount of time it takes for the National Weather Service to generate and serve your forecast.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`For a final fancy touch, let’s connect our forecast data to [this custom D3 weather visualization](/@kerryrodden/simple-custom-weather-chart-in-d3), implemented in a different notebook. Vega-Lite is great for the rapid creation of basic charts, but sometimes you want to create something custom with more visual flair. For that, D3 is an excellent choice, and Observable makes it particularly easy to repurpose and remix other peoples’ D3 visualizations. Since the external notebook also happens to also render data in the Weather.gov forecast format, that’s not going to be too hard. 

We import the \`weatherChart\` from that notebook, and inject our live \`localForecast\` data into it:`
)});
  const child1 = runtime.module(define1).derive([{name: "localForecast", alias: "forecast"}], main);
  main.import("weatherChart", child1);
  main.variable(observer()).define(["md"], function(md){return(
md`And then render the chart onto the page:`
)});
  main.variable(observer()).define(["weatherChart"], function(weatherChart){return(
weatherChart
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Even though this is code being imported from another notebook, as you change your location on the map, it reacts to changes in the forecast data in the same way as any other cell.

If you’d like to work on a notebook with someone else, you can enable link sharing, and send them the URL. Then, after tinkering with your notebook, they can click a button to [send you their comments and code suggestions](https://observablehq.com/@observablehq/suggestions-and-comments). Or, you can work together on a notebook in real time, using [Observable Teams](https://observablehq.com/teams).`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`🌈 I think that’s it for our first taste of Observable!

If you’d like to learn more, about how to actually *build* notebooks like this one, we recommend starting with these introductory notebook sequences, which gently teach Observable concepts with special consideration for folks from different backgrounds, having different goals:`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`
- **[Learn D3](/@d3/learn-d3)**<br>  D3 is a powerful JavaScript library that helps you bring data to life using HTML, SVG, and CSS. If you already have some D3 under your belt, you'll find using D3 in Observable is a little bit different. Whether you're new to D3, Observable, or both, get your feet wet here.

- **[Observable for Jupyter Users](/@observablehq/observable-for-jupyter-users?collection=@observablehq/observable-for-jupyter-users)**<br> If you have a Python data science background, or just feel more comfortable in Python than in JavaScript, these tutorials will help ease you in.

- **[Charting with Vega-Lite](/@observablehq/vega-lite)**<br> Vega-Lite is probably the best JavaScript library for extremely rapid visual exploration of data sets. You can iterate on your Vega visualizations even faster in Observable’s reactive environment.
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`And if you don’t want to hold hands and would prefer to dive straight into the deep end, I’d recommend bookmarking the [User Manual](https://observablehq.com/@observablehq/user-manual) (everything is in there), and checking out the [Explore](https://observablehq.com/explore) page for inspiration.

Have fun! 👋`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`<br><br><br><br><br><br><br><br><br>

--- 

## Appendix

The cells below power the cells above.`
)});
  main.variable(observer("domain")).define("domain", ["localForecast"], function(localForecast)
{
  const temps = localForecast.properties.periods.map(d => d.temperature);
  const high = Math.max.apply(Math, temps);
  const low = Math.min.apply(Math, temps);
  return {domain: [Math.min(low, 0), Math.max(high, 90)]};
}
);
  main.variable(observer("code")).define("code", ["html"], function(html){return(
function code(s) {
  return html`<code style="white-space: nowrap;">${s}</code>`;
}
)});
  main.variable(observer("caret")).define("caret", ["caretImage"], function(caretImage){return(
function caret() {
  const c = caretImage.cloneNode(true);
  c.style.verticalAlign = "middle";
  return c;
}
)});
  main.variable(observer("caretImage")).define("caretImage", ["FileAttachment"], async function(FileAttachment){return(
Object.assign(await FileAttachment("image@1.png").image(), {width: 18})
)});
  main.variable(observer("run")).define("run", ["svg"], function(svg){return(
function run() {
  return svg`<svg width="16" height="16" class="db bump" stroke-linejoin="round" fill="#3b5fc0"><path d="M11.7206 6.94335C12.2406 7.34365 12.2406 8.12786 11.7206 8.52816L5.60999 13.2321C4.95242 13.7383 4 13.2696 4 12.4397L4 3.03178C4 2.20194 4.95243 1.73318 5.60999 2.23937L11.7206 6.94335Z" stroke="#3b5fc0" stroke-width="1.6"></path></svg>`;
}
)});
  main.variable(observer("style")).define("style", ["html"], function(html){return(
html`<style>

.table-2 table td,
.table-2 table th {
  padding: 5px 10px;
}

</style>`
)});
  const child2 = runtime.module(define2);
  main.import("usaMapCoordinates", child2);
  const child3 = runtime.module(define3);
  main.import("table", child3);
  const child4 = runtime.module(define4);
  main.import("vl", child4);
  return main;
}
