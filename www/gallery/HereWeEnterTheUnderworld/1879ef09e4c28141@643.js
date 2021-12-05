// https://observablehq.com/@kerryrodden/simple-custom-weather-chart-in-d3@643
import define1 from "./e93997d5089d7165@2303.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Simple custom weather chart in D3 
`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`This notebook uses forecast data from the [National Weather Service API](https://www.weather.gov/documentation/services-web-api), which includes day-time high and night-time low temperatures, plus a brief text forecast.`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`For example, here’s the forecast for Central Park in New York:`
)});
  main.variable(observer("forecast")).define("forecast", ["d3"], async function(d3){return(
await d3.json(
  "https://api.weather.gov/gridpoints/OKX/33,37/forecast"
)
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Here is one way to visualize that forecast using D3.js – animating from a timeline into a temperature chart, while using color coding (and emojis!) to give some indication of the forecast conditions.`
)});
  main.variable(observer("viewof preferredUnit")).define("viewof preferredUnit", ["radio"], function(radio){return(
radio({
  title: "Preferred Temperature Unit",
  options: [
    { label: "Fahrenheit", value: "F" },
    { label: "Celsius", value: "C" }
  ],
  value: "F"
})
)});
  main.variable(observer("preferredUnit")).define("preferredUnit", ["Generators", "viewof preferredUnit"], (G, _) => G.input(_));
  main.variable(observer("weatherChart")).define("weatherChart", ["width","temperatureInPreferredUnits","preferredUnit","d3","forecast","IntersectionObserver","invalidation"], function*(width,temperatureInPreferredUnits,preferredUnit,d3,forecast,IntersectionObserver,invalidation)
{
  const minDayWidth = 100;
  const maxEntriesToShow = Math.floor(width / minDayWidth);
  const height = 200;
  const margin = { top: 15, right: 5, bottom: 15, left: 35 };
  const barHeight = 6;
  const minTemperature = temperatureInPreferredUnits(20, "F", preferredUnit);
  const maxTemperature = temperatureInPreferredUnits(90, "F", preferredUnit);

  const svg = d3
    .create("svg")
    .attr("viewBox", [0, 0, width, height])
    .style(
      "font",
      "10px -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif"
    );

  const temperatureUnit = forecast.properties.periods[0].temperatureUnit || "F";

  const forecasts = forecast.properties.periods
    .sort((a, b) => d3.ascending(a.number, b.number))
    .map(d => ({
      ...d,
      temperature: temperatureInPreferredUnits(
        d.temperature,
        temperatureUnit,
        preferredUnit
      ),
      startTime: new Date(d.startTime),
      endTime: new Date(d.endTime)
    }))
    .filter(d => d3.timeHour.offset(d.startTime, 2) <= d.endTime)
    .slice(0, maxEntriesToShow);

  const startTime = d3.min(forecasts, d => d.startTime);
  const endTime = d3.max(forecasts, d => d.endTime);
  const xScale = d3
    .scaleTime()
    .domain([startTime, endTime])
    .range([margin.left, width - margin.left - margin.right]);
  const yScale = d3
    .scaleLinear()
    .domain([
      Math.min(minTemperature, d3.min(forecasts, d => d.temperature)),
      Math.max(maxTemperature, d3.max(forecasts, d => d.temperature))
    ])
    .nice()
    .range([height - margin.bottom, margin.top]);

  const label = d => {
    if (d.number === 1) {
      // Shorten or suppress the label for the (shorter) first entry, to avoid overlap
      return d3.timeHour.offset(d.startTime, 6) > d.endTime ? "" : "Now";
    } else {
      return d.name;
    }
  };

  const conditions = [
    { name: "Snow", color: "#74ccfa", emoji: "❄️" },
    { name: "Rain", color: "#6786db", emoji: "☔" },
    { name: "Sunny", color: "#fcd92c", emoji: "☀️" }
  ];

  const findPrimaryWeather = forecastText => {
    const positions = conditions.map(d =>
      forecastText.includes(d.name) ? forecastText.indexOf(d.name) : null
    );
    const minIndex = d3.minIndex(positions);
    return minIndex >= 0 ? conditions[minIndex] : null;
  };

  const color = d => {
    const primaryWeather = findPrimaryWeather(d.shortForecast);
    return primaryWeather ? primaryWeather.color : "#ccc";
  };

  const emoji = d => {
    const primaryWeather = findPrimaryWeather(d.shortForecast);
    return primaryWeather ? primaryWeather.emoji : "";
  };

  const g = svg
    .selectAll("g")
    .data(forecasts)
    .join("g")
    .attr(
      "transform",
      d => `translate(${xScale(d.startTime)}, ${height - margin.bottom})`
    );

  g.append("rect")
    .attr("width", d => xScale(d.endTime) - xScale(d.startTime) - 2)
    .attr("height", barHeight)
    .attr("rx", 3)
    .attr("ry", 3)
    .attr("fill", "#ccc");

  g.append("text")
    .attr("y", -barHeight - 3)
    .attr("dy", "0.35em")
    .text(d => `${label(d)} ${emoji(d)}`);

  g.append("title").text(
    d =>
      `${d.shortForecast}, ${d.isDaytime ? "high" : "low"} of ${
        d.temperature
      }°${preferredUnit}`
  );

  const yAxis = svg
    .append("g")
    .attr("transform", `translate(${margin.left - 5}, 0)`)
    .call(
      d3
        .axisLeft(yScale)
        .ticks(7)
        .tickFormat(d => d + `°${preferredUnit}`)
        .tickSize(3)
    );

  yAxis.select(".domain").remove();
  yAxis
    .selectAll("text")
    .style("fill", "#666")
    .style(
      "font",
      "10px -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, Helvetica, Arial, sans-serif"
    );

  yield svg.node();

  // Animate the graph whenever this cell becomes visible or invisible
  const observer = new IntersectionObserver(entries => {
    const entry = entries.pop();
    if (entry.isIntersecting) {
      const t = g
        .transition()
        .duration(2000)
        .ease(d3.easeCubic);
      t.attr(
        "transform",
        d => `translate(${xScale(d.startTime)}, ${yScale(d.temperature)})`
      );
      t.select("rect").attr("fill", color);
    } else {
      g.attr(
        "transform",
        d => `translate(${xScale(d.startTime)}, ${height - margin.bottom})`
      );
      g.select("rect").attr("fill", "#ccc");
    }
  });
  observer.observe(svg.node());
  invalidation.then(() => observer.disconnect());
}
);
  main.variable(observer("temperatureInPreferredUnits")).define("temperatureInPreferredUnits", ["f2c","c2f"], function(f2c,c2f){return(
(t, currentUnit, preferredUnit) => {
  if (currentUnit === "F" && preferredUnit === "C") return f2c(t);
  if (currentUnit === "C" && preferredUnit === "F") return c2f(t);
  return t;
}
)});
  main.variable(observer("f2c")).define("f2c", function(){return(
t => Math.round((t - 32) * 5 / 9)
)});
  main.variable(observer("c2f")).define("c2f", function(){return(
t => Math.round((t * 9/5) + 32)
)});
  main.variable(observer()).define(["md"], function(md){return(
md`## Imports`
)});
  main.variable(observer("d3")).define("d3", ["require"], function(require){return(
require("d3@v5", "d3-array@2")
)});
  const child1 = runtime.module(define1);
  main.import("radio", child1);
  return main;
}
