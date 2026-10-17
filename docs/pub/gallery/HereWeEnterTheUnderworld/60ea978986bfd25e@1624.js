// https://observablehq.com/@tmcw/tables/2@1624
import define1 from "./dbd7aeb5832fdd8a@205.js";

export default function define(runtime, observer) {
  const main = runtime.module();
  main.variable(observer()).define(["md"], function(md){return(
md`# Tables

I truly believe that _tables are visualization_, and great tables are both extraordinarily effective and very hard to achieve with system defaults. This notebook is part of a continuing effort to make excellent tables available without lots of nitpicky tweaks - or rather, that I try to automate all the nitpicky tweaks.

Out of the box, this notebook achieves some of those nitpicky details: good typography for numbers, filters, querying, and a paging interface that can tolerate big datasets. There’s more ground to cover, though, and I’d love to get some help from folks who have done this sort of thing a lot before.

Versus the original tables notebook, this has some revisions.

- REMOVED: The idea of formatters is dropped, and in its place you can specify html cells. It's better to transform your data into one predictable form than to have transformers built into the table abstraction.
- ADDED: Paging is robust, having been built in the early stages of the notebook. If a table has fewer than 5 pages, each page is linked. If more, then pages are accessible through a select box.
- ADDED: Smart facets and querying.
- IMPROVED: Smarter number formatting. Combines locale formatting with a somewhat smarter system to determine how many decimal points should be included per number, so that numbers like 20 and 20.1 align correctly.
- IMPROVED: Instead of using a monospace font for numbers, use tabular numbers in a system font. This works on Mac OS with SF, and I’ll eventually create backward-compatibility.

---

A first example: the \`mtcars\` dataset. Notice the special number formatting - that 21mpg is formatted as 21.0 to match the other MPG readings. The numbers use tabular figures, so that characters like 1 have the same width as 'wider' characters like 0, and they all line up. Click the search icon to filter and search the dataset.`
)});
  main.variable(observer()).define(["table","mtcars"], function(table,mtcars){return(
table(mtcars, { title: "Cars" })
)});
  main.variable(observer()).define(["table","aapl"], function(table,aapl){return(
table(aapl, { title: "Apple stock price" })
)});
  main.variable(observer()).define(["md"], function(md){return(
md`Tables also now work as views:`
)});
  main.variable(observer("viewof diamondsPage")).define("viewof diamondsPage", ["table","diamonds"], function(table,diamonds){return(
table(diamonds, { title: "Diamonds" })
)});
  main.variable(observer("diamondsPage")).define("diamondsPage", ["Generators", "viewof diamondsPage"], (G, _) => G.input(_));
  main.variable(observer()).define(["md","diamondsPage"], function(md,diamondsPage){return(
md`Average price of this selection: $${new Intl.NumberFormat().format(
  diamondsPage.data.reduce((sum, d) => sum + d.price, 0) /
    diamondsPage.data.length
)}`
)});
  main.variable(observer()).define(["md","diamondsPage"], function(md,diamondsPage){return(
md`Average price of this page: $${new Intl.NumberFormat().format(
  diamondsPage.reduce((sum, d) => sum + d.price, 0) / diamondsPage.length
)}`
)});
  main.variable(observer()).define(["md"], function(md){return(
md`An example of a very wide dataset, with over 200 columns. This is a work in progress, because there are a few connected behaviors for this case that I’d like to tune:

- The table assumes 100% width instead of being constricted to 640px.
- The table is allowed to scroll, but the search / paging bar does not.
- Potentially in this case it’s preferable to add vertical lines between columns, like in GitHub Gists?`
)});
  main.variable(observer("helpfullTable")).define("helpfullTable", ["table","datasets"], async function(table,datasets){return(
table(await datasets.HELPfull.data)
)});
  main.variable(observer("style")).define("style", ["html","filterStyles"], function(html,filterStyles){return(
() => html`<style>
.table-2.wide .scroll-zone {
  overflow-x: auto;
  max-width: 100%;
}
.table-2.narrow-columns td,
.table-2.narrow-columns th {
  border: 1px solid #eee;
  padding: 4px;
}
.table-2.narrow-columns th {
  background: #f9f9f9;
  border-right: 1px solid #eee;
}
.table-2.wide .pager {
  max-width: 100%;
}
.table-2 table th,
.table-2 table td {
  padding: 3px 0px;
}
.table-2 table th,
.table-2 table td {
  vertical-align: top;
}
.table-2 table td:not(:first-child),
.table-2 table th:not(:first-child) {
  padding-left: 4px;
}
.table-2 table thead th {
  ____text-transform: uppercase;
  font-weight:500;
}
.table-2 .pager .title {
  flex: auto;
  font-weight: 700;
}
.table-2 .pager {
  margin-bottom: 4px;
  box-sizing: border-box;
  border-bottom:1px solid #ccc;
  font-size: 14px;
  font-weight: 500;
  display: flex;
  max-width: 640px;
  align-items: center;
  font-family: var(--sans-serif);
  justify-content: space-between;
}
.table-2 .pager .button.disabled {
  color: #ccc;
  pointer-events:none;
}
.table-2 .pager .button {
  display: inline-flex;
  align-items: center;
  color: #333;
}
.table-2 .pager .button:hover {
  color: #000;
  cursor: pointer;
}
.table-2 .pager select {
  font-family: var(--sans-serif);
}
.table-2 .pager .page-links {
  display: inline-flex;
  align-items: center;
}
.table-2 .pager .page-links div {
  padding: 2px 4px 2px 4px;
  cursor: pointer;
  color: #888;
}
.table-2 .pager .page-links div.current {
  padding: 2px 4px 0 4px;
  pointer-events: none;
  color: #000;
  border-bottom:2px solid #000;
}
.table-2 .pager .page-links .page-selector-container {
  padding: 4px 0;
}
${filterStyles}
</style>`
)});
  main.variable(observer("recommendVerticalBorders")).define("recommendVerticalBorders", function(){return(
function recommendVerticalBorders(table) {
  let narrowCells = 0;
  for (let cell of table.querySelectorAll("tbody tr:first-child td")) {
    if (cell.offsetWidth < 50) narrowCells++;
    if (narrowCells > 8) return true;
  }
}
)});
  main.variable(observer("table")).define("table", ["detectColumns","html","leftIcon","rightIcon","searchIcon","header","search","style","row","recommendVerticalBorders"], function(detectColumns,html,leftIcon,rightIcon,searchIcon,header,search,style,row,recommendVerticalBorders){return(
function table(inputData, options = {}) {
  let { page, pageSize, date, title, debug } = {
    pageSize: 15,
    page: 0,
    date: "day",
    title: "",
    debug: false,
    ...options
  };
  let first = true;
  let searching = false;
  let filters = {};
  let searchQuery = "";
  let adata = Array.from(inputData); // Normalize iterables to plain arrays.
  let detectedColumns = detectColumns(adata);
  let supercontainer = html`<div class='table-2'></div>`;

  function render() {
    let data;
    if (Object.keys(filters).length || searchQuery) {
      data = adata.filter(obj => {
        for (let [col, value] of Object.entries(filters)) {
          if (obj[col] !== value) return false;
        }
        if (searchQuery) {
          let strValue = "";
          for (let key of Object.keys(obj)) {
            strValue += obj[key];
          }
          if (!strValue.toLowerCase().includes(searchQuery.toLowerCase())) {
            return false;
          }
        }
        return true;
      });
    } else {
      data = adata;
    }
    // If we're on page 5 and then filter and yield
    // fewer than 5 pages.
    if (page * pageSize > data.length) {
      page = Math.floor(data.length / pageSize);
    }
    let start = page * pageSize;
    let end = Math.min(data.length, (page + 1) * pageSize);
    let pageCount = pageSize ? Math.ceil(data.length / pageSize) : 0;
    let chunk = data.slice(start, end);
    let hasPrev = page > 0;
    let hasNext = end < data.length;

    let prevButton = html`<div title="Previous" class='button ${
      hasPrev ? "" : "disabled"
    }'>${leftIcon()}</div>`;
    let nextButton = html`<div title="Next" class='button ${
      hasNext ? "" : "disabled"
    }'>${rightIcon()}</div>`;
    prevButton.onclick = () => {
      page--;
      render();
    };
    nextButton.onclick = () => {
      page++;
      render();
    };
    let pageLinks = html`<div class='page-links'></div>`;
    if (pageCount < 5) {
      for (let i = 0; i < pageCount; i++) {
        let elem = html`<div class='${i === page ? "current" : ""}'>${i +
          1}</div>`;
        elem.onclick = () => {
          page = i;
          render();
        };
        pageLinks.appendChild(elem);
      }
    } else {
      const select = html`<div class='page-selector-container'><label for='page-selector'>Page</label> <select id='page-selector'>
    ${Array.from({ length: pageCount }, (_, i) => {
      let elem = html`<option value='${i}'>${i + 1}</option>`;
      return elem;
    })}
</select></div>`;
      select.querySelector("select").value = page;
      pageLinks.appendChild(select);
      select.onchange = e => {
        page = parseInt(e.target.value, 10);
        render();
      };
    }
    let searchToggle = html`<div style='flex:auto;display:inline-flex;'><div title="Search / Filter" class='button'>${searchIcon()}</div></div>`;
    searchToggle.querySelector(".button").onclick = () => {
      searching = !searching;
      render();
    };
    let navigation = html`<div class='pager'>${searchToggle}
<div class='title'>${title}</div>
          ${pageLinks}
          ${prevButton}
          ${nextButton}
        </div>`;
    let tbody = html`<tbody></tbody>`;
    let table = html`<table>${header(detectedColumns)}${tbody}</table>`;
    let searchUI = searching
      ? search(adata, detectedColumns, filters, searchQuery)
      : "";
    let container = html`<div>
${searchUI}
${
      hasNext || hasPrev ? navigation : ""
    }<div class='scroll-zone'>${table}</div>${style()}</div>`;
    for (let d of chunk) {
      tbody.appendChild(row(d, detectedColumns, { date }));
    }

    if (searchUI) {
      searchUI.addEventListener("setfilters", e => {
        ({ filters, searchQuery } = e.target.value);
        render();
      });
      searchUI.addEventListener("closefilters", e => {
        ({ filters, searchQuery } = e.target.value);
        searching = false;
        render();
      });
    }

    supercontainer.innerHTML = "";
    supercontainer.appendChild(container);
    supercontainer.value = chunk;
    supercontainer.value.data = data;
    supercontainer.dispatchEvent(new CustomEvent("input"));

    if (first) {
      setTimeout(() => {
        // If the table wants to be wide, let it be wide and scrollable.
        if (supercontainer.querySelector("table").scrollWidth > 640) {
          supercontainer.classList.add("wide");
        }
        if (recommendVerticalBorders(supercontainer)) {
          supercontainer.classList.add("narrow-columns");
        }
      }, 0);
      first = false;
    }
  }
  render();
  return supercontainer;
}
)});
  main.variable(observer("getDropdowns")).define("getDropdowns", function(){return(
function getDropdowns(inputData, detectedColumns) {
  let dropdowns = new Map();
  // Find columns with under 25 distinct values and
  // avoiding columns with string values over 100.
  for (let [column] of detectedColumns) {
    let uniqueValues = new Set();
    for (let row of inputData) {
      uniqueValues.add(row[column]);
      if (uniqueValues.size > 25) break;
      if (typeof row[column] === "string" && row[column].length > 100) break;
    }
    if (uniqueValues.size !== 26) {
      dropdowns.set(column, uniqueValues);
    }
  }
  let ret = new Map();
  for (let [column, choices] of dropdowns) {
    ret.set(
      column,
      [...choices].sort((a, b) => (typeof a === "string" ? b > a : b - a))
    );
  }
  return ret;
}
)});
  main.variable(observer("filterStyles")).define("filterStyles", function(){return(
`
.search {
  padding:5px 0;
  font-family: var(--sans-serif);
  font-size: 80%;
  border-bottom:1px solid #ccc;
  max-width: 640px;
  display: flex;
  justify-content: space-between;
}
.search .search-dropdown select {
  font-family: var(--sans-serif);
}
.search .search-dropdown {
  padding-right:10px;
}
.search .query {
  padding-bottom: 5px;
}
.search .filters {
  display: flex;
  flex-wrap: wrap;
}
.search .button {
  color: #aaa;
}
.search .button:hover {
  color: #000;
  cursor: pointer;
}
`
)});
  main.variable(observer()).define(["search","diamonds","detectColumns"], function(search,diamonds,detectColumns){return(
search(diamonds, detectColumns(diamonds), {}, "")
)});
  main.variable(observer("search")).define("search", ["getDropdowns","html","xCircleIcon","dropdown"], function(getDropdowns,html,xCircleIcon,dropdown){return(
function search(data, detectedColumns, filters, searchQuery) {
  let dropdowns = getDropdowns(data, detectedColumns);
  let filterContainer = html`<div class='filters'></div>`;

  let closeButton = html`<div title='Close' class='button'>${xCircleIcon()}</div>`;
  let query = html`<div class='query'>
<input type='search' autocomplete=off />
<button type=button>Search</button>
</div>`;
  let container = html`<div class='search'>
<div>
${query}
${filterContainer}
</div>
${closeButton}
</div>`;
  closeButton.onclick = () => {
    container.value = { filters: {}, searchQuery: "" };
    container.dispatchEvent(new CustomEvent("closefilters"));
  };

  let setSearchQuery = () => {
    searchQuery = query.querySelector("input").value;
    container.value = { filters, searchQuery };
    container.dispatchEvent(new CustomEvent("setfilters"));
  };
  query.querySelector("button").onclick = setSearchQuery;
  query.querySelector("input").onsearch = setSearchQuery;
  query.querySelector("input").value = searchQuery;
  [...dropdowns.entries()].map(([column, choices]) => {
    let d = dropdown(column, choices, filters);
    filterContainer.appendChild(d);
    d.addEventListener("setfilters", e => {
      e.stopPropagation();
      filters[column] = e.target.value;
      if (filters[column] === undefined) delete filters[column];
      container.value = { filters, searchQuery };
      container.dispatchEvent(new CustomEvent("setfilters"));
    });
  });
  return container;
}
)});
  main.variable(observer("dropdown")).define("dropdown", ["idx","html"], function(idx,html){return(
function dropdown(column, choices, filters) {
  choices = [...choices];
  let id = idx();
  let elem = html`<div class='search-dropdown'>
<label for='search-${id}'>${column}</label>
<select id='search-${id}'>
<option value='-1'></option>
${choices.map((choice, i) => html`<option value=${i}>${choice}</option>`)}
</select>
</div>`;
  if (filters[column] !== undefined) {
    elem.querySelector("select").value = choices.indexOf(filters[column]);
  }
  elem.querySelector("select").onchange = e => {
    elem.value = choices[e.target.value];
    elem.dispatchEvent(new CustomEvent("setfilters"));
  };
  return elem;
}
)});
  main.variable(observer("idx")).define("idx", function(){return(
(() => {
  let i = 0;
  return () => ++i;
})()
)});
  main.variable(observer("row")).define("row", ["html","td"], function(html,td){return(
function row(data, detectedColumns, options) {
  return html`<tr>
    ${detectedColumns.map(column => td(data, column, options))}
  </tr>`;
}
)});
  main.variable(observer("tdStyles")).define("tdStyles", function(){return(
{
  number: "text-align:right;font-variant-numeric:tabular-nums;",
  date: "font-variant-numeric:tabular-nums;"
}
)});
  main.variable(observer("td")).define("td", ["basicDayFormat","basicYearFormat","html","tdStyles"], function(basicDayFormat,basicYearFormat,html,tdStyles){return(
function td(data, [key, { type, decimalsRequired }], options) {
  let rep = data[key];
  let title = "";
  if (rep === null) {
    rep = "null";
  } else if (rep === undefined) {
    rep = "–";
  } else {
    if (type === "number") {
      rep = new Intl.NumberFormat("en-US", {
        minimumFractionDigits: decimalsRequired
      }).format(data[key]);
    }
    if (type === "date") {
      title = data[key].toLocaleString();
      switch (options.date) {
        case "day":
          rep = basicDayFormat(data[key]);
          break;
        case "year":
          rep = basicYearFormat(data[key]);
          break;
        case "full":
          rep = data[key].toLocaleString().toLowerCase();
          break;
      }
    }
  }
  return html`<td title='${title}' style='${tdStyles[type] || ""}'>${rep}</td>`;
}
)});
  main.variable(observer("header")).define("header", ["html","th"], function(html,th){return(
function header(detectedColumns) {
  return html`<thead>
    ${detectedColumns.map(th)}
  </thead>`;
}
)});
  main.variable(observer("thStyles")).define("thStyles", function(){return(
{
  number: "text-align:right;"
}
)});
  main.variable(observer("th")).define("th", ["html","thStyles"], function(html,thStyles){return(
function th([key, { type }]) {
  return html`<th style='${thStyles[type] || ""}'>${key}</th>`;
}
)});
  main.variable(observer()).define(["detectColumns"], function(detectColumns){return(
detectColumns([{ name: "Tom", age: 17 }])
)});
  main.variable(observer("detectColumns")).define("detectColumns", ["countDecimals"], function(countDecimals){return(
function detectColumns(data) {
  let columns = new Map();
  for (let row of data) {
    for (let key in row) {
      if (columns.has(key)) continue;
      if (
        typeof row[key] === "object" &&
        row[key] !== null &&
        "html" in row[key]
      ) {
        columns.set(key, { type: "html" });
      } else {
        if (row[key] instanceof Date) {
          columns.set(key, { type: "date" });
        } else {
          columns.set(key, { type: typeof row[key] });
        }
      }
    }
  }
  for (let [key, { type }] of columns) {
    if (type === "number") {
      let decimalsRequired = 0;
      for (let row of data) {
        if (countDecimals(row[key]) > decimalsRequired) {
          decimalsRequired = countDecimals(row[key]);
        }
        if (decimalsRequired == 4) break;
      }
      columns.get(key).decimalsRequired = decimalsRequired;
    }
  }
  return [...columns.entries()];
}
)});
  main.variable(observer("countDecimals")).define("countDecimals", function(){return(
number =>
  number != null
    ? Math.min((number.toString().split(".")[1] || "").length, 4)
    : 0
)});
  main.variable(observer()).define(["table"], function(table){return(
table([
  { name: "A", count: 1 },
  { name: "B", count: 2 },
  { name: "C", count: null }
])
)});
  main.variable(observer("leftIcon")).define("leftIcon", ["svg"], function(svg){return(
() =>
  svg`<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>`
)});
  main.variable(observer("rightIcon")).define("rightIcon", ["svg"], function(svg){return(
() =>
  svg`<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>`
)});
  main.variable(observer("searchIcon")).define("searchIcon", ["svg"], function(svg){return(
() =>
  svg`<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-search"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>`
)});
  main.variable(observer("xCircleIcon")).define("xCircleIcon", ["svg"], function(svg){return(
() =>
  svg`<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x-circle"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6M9 9l6 6"/></svg>`
)});
  main.variable(observer("basicDayFormat")).define("basicDayFormat", function(){return(
d => {
  const month = (d.getMonth() + 1).toString().padStart(2, "0");
  const day = d
    .getDate()
    .toString()
    .padStart(2, "0");
  const year = d.getFullYear();
  return `${year}-${month}-${day}`;
}
)});
  main.variable(observer("basicYearFormat")).define("basicYearFormat", function(){return(
d => {
  return d.getFullYear().toString();
}
)});
  main.variable(observer("mtcars")).define("mtcars", ["require"], function(require){return(
require("@observablehq/mtcars")
)});
  main.variable(observer("diamonds")).define("diamonds", ["require"], function(require){return(
require("@observablehq/diamonds")
)});
  main.variable(observer("aapl")).define("aapl", ["require"], function(require){return(
require("@observablehq/aapl")
)});
  const child1 = runtime.module(define1);
  main.import("datasets", child1);
  main.variable(observer()).define(["md"], function(md){return(
md`TODO

- Histograms?
- Sortable columns
- Automatically allow x-overflow if columns are wide
`
)});
  return main;
}
