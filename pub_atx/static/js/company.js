

function reverseString(str) {
    var newString = "";
    for (var i = str.length - 1; i >= 0; i--) {
        newString += str[i];
    }
    return newString;
}


function stripUrlTicker() {
  var url = window.location.href;
  var reversedUrl = reverseString(url);
  var slashPosition = reversedUrl.indexOf("/");
  var reversedTicker = reversedUrl.substring(0, slashPosition).toUpperCase();
  var ticker = reverseString(reversedTicker)
  return ticker;
}

ticker = stripUrlTicker();


function getTickers() {

    // Grab a reference to the dropdown select element
    var selector = document.getElementById('selDataset');

    // Get the list of tickers to populate the select options
    d3.json(`/tickers/${ticker}`, function(error, companyNames) {
        for (var i = 0; i < companyNames.length;  i++) {
            var currentOption = document.createElement('option');
            currentOption.text = companyNames[i];
            currentOption.value = companyNames[i]
            selector.appendChild(currentOption);
        }
    })
}


function getNewsArticles() {
  d3.json(`https://api.iextrading.com/1.0/stock/${ticker}/news/last/3`, function(error, json) {
    if (error) return console.warn(error);
    var pressSection = d3.select("#press-section");
    pressSection.append("div")
          .html(`<div class="row">
                  <h2 class="section-title"><span>Recent Press</span></h2> <br />
                  </div>
                  <div class="col-xs-12 col-md-1">
                  </div>
                  <div class="col-xs-12 col-md-10">
                 <div class="row">
                  <div class='article-list'> </div>
                 </div>
                 </div>
                 <div class="col-xs-12 col-md-1">
                 </div>
            `);
    json.forEach(function(article) {
      addArticleToHtml(article)
    });
  });
}



function getMonth(month) {
    var monthInt = parseInt(month);
    var monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December" ];
    monthIndex = monthInt -1
    return monthNames[monthIndex];
}

function dateTimeToStr(dateTimeObj) {
  var year = dateTimeObj.substring(0,4);
  var month = dateTimeObj.substring(5,7).replace(/^0+/, '');
  var day = dateTimeObj.substring(8,10).replace(/^0+/, '');
  var newMonth = getMonth(month)
  var dateStr = `${newMonth} ${day}, ${year}`
  return dateStr
}

function addArticleToHtml(articleJson) {
  var dateStr = dateTimeToStr(articleJson.datetime);
  var articleList = d3.select(".article-list");

  articleList.append("article")
        .html(`<div>
              <hr>
              <h4> <a href="${articleJson.url}" target="_blank"> ${articleJson.headline} </a> </h4>
              <h5> ${dateStr} </h5>
              <br />
              <p> ${articleJson.summary} </p>
              <p> Source: ${articleJson.source} </p>
              </div>
              <br />`);
}



function init() {
    getTickers();
    getNewsArticles();
}

init();


var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 650 - margin.left - margin.right,
        height = 430 - margin.top - margin.bottom;

var parseDate = d3.timeParse("%Y-%m-%d");

var x = techan.scale.financetime()
        .range([0, width]);

var y = d3.scaleLinear()
        .range([height, 0]);

var yVolume = d3.scaleLinear()
        .range([y(0), y(0.2)]);

var ohlc = techan.plot.ohlc()
        .xScale(x)
        .yScale(y);

var sma0 = techan.plot.sma()
        .xScale(x)
        .yScale(y);

var sma0Calculator = techan.indicator.sma()
        .period(10);

var sma1 = techan.plot.sma()
        .xScale(x)
        .yScale(y);

var sma1Calculator = techan.indicator.sma()
        .period(20);

var volume = techan.plot.volume()
        .accessor(ohlc.accessor())   // Set the accessor to a ohlc accessor so we get highlighted bars
        .xScale(x)
        .yScale(yVolume);

var xAxis = d3.axisBottom(x);

var yAxis = d3.axisLeft(y);

var volumeAxis = d3.axisRight(yVolume)
        .ticks(3)
        .tickFormat(d3.format(",.3s"));

var timeAnnotation = techan.plot.axisannotation()
        .axis(xAxis)
        .orient('bottom')
        .format(d3.timeFormat('%Y-%m-%d'))
        .width(65)
        .translate([0, height]);

var ohlcAnnotation = techan.plot.axisannotation()
        .axis(yAxis)
        .orient('left')
        .format(d3.format(',.2f'));

var volumeAnnotation = techan.plot.axisannotation()
        .axis(volumeAxis)
        .orient('right')
        .width(35);

var crosshair = techan.plot.crosshair()
        .xScale(x)
        .yScale(y)
        .xAnnotation(timeAnnotation)
        .yAnnotation([ohlcAnnotation, volumeAnnotation])
        .on("move", move);

var svg = d3.select("#techan-plot").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

var defs = svg.append("defs");

defs.append("clipPath")
        .attr("id", "ohlcClip")
    .append("rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", width)
        .attr("height", height);

svg = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var ohlcSelection = svg.append("g")
        .attr("class", "ohlc")
        .attr("transform", "translate(0,0)");

ohlcSelection.append("g")
        .attr("class", "volume")
        .attr("clip-path", "url(#ohlcClip)");

ohlcSelection.append("g")
        .attr("class", "candlestick")
        .attr("clip-path", "url(#ohlcClip)");

ohlcSelection.append("g")
        .attr("class", "indicator sma ma-0")
        .attr("clip-path", "url(#ohlcClip)");

ohlcSelection.append("g")
        .attr("class", "indicator sma ma-1")
        .attr("clip-path", "url(#ohlcClip)");

svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")");

svg.append("g")
        .attr("class", "y axis")
    .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Price ($)");

svg.append("g")
        .attr("class", "volume axis");

svg.append('g')
        .attr("class", "crosshair ohlc");

var coordsText = svg.append('text')
        .style("text-anchor", "end")
        .attr("class", "coords")
        .attr("x", width - 5)
        .attr("y", 15);

var feed;

d3.json(`../daily-trading-data/${ticker}`, function(error, csv) {
    var accessor = ohlc.accessor();

    plottingData = csv.map(function(d) {
        return {
            date: parseDate(d.date),
            open: +d.open,
            high: +d.high,
            low: +d.low,
            close: +d.close,
            volume: +d.volume
        };
    }).sort(function(a, b) { return d3.ascending(accessor.d(a), accessor.d(b)); });

    // Start off an initial set of data
    drawPlot(plottingData);
});

function drawPlot(data) {
    var accessor = ohlc.accessor();

    x.domain(data.map(accessor.d));
    // Show only 150 points on the plot
    x.zoomable().domain([data.length-130, data.length]);

    // Update y scale min max, only on viewable zoomable.domain()
    y.domain(techan.scale.plot.ohlc(data.slice(data.length-130, data.length)).domain());
    yVolume.domain(techan.scale.plot.volume(data.slice(data.length-130, data.length)).domain());

    // Setup a transition for all that support
    svg
//          .transition() // Disable transition for now, each is only for transitions
        .each(function() {
            var selection = d3.select(this);
            selection.select('g.x.axis').call(xAxis);
            selection.select('g.y.axis').call(yAxis);
            selection.select("g.volume.axis").call(volumeAxis);

            selection.select("g.candlestick").datum(data).call(ohlc);
            selection.select("g.sma.ma-0").datum(sma0Calculator(data)).call(sma0);
            selection.select("g.sma.ma-1").datum(sma1Calculator(data)).call(sma1);
            selection.select("g.volume").datum(data).call(volume);

            svg.select("g.crosshair.ohlc").call(crosshair);
        });

}

function move(coords) {
    coordsText.text(
            timeAnnotation.format()(coords.x) + ", " + ohlcAnnotation.format()(coords.y)
    );
}
