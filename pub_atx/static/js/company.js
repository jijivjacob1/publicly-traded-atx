var apiKey = "ac6hLgVewCjgjJezdjUR";


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

/**
 * Helper function to select stock data
 * Returns an array of values
 * @param {array} rows
 * @param {integer} index
 * index 0 - Date
 * index 1 - Open
 * index 2 - High
 * index 3 - Low
 * index 4 - Close
 * index 5 - Volume
 */
function unpack(rows, index) {
  return rows.map(function(row) {
    return row[index];
  });
}

function getTickers() {

    // Grab a reference to the dropdown select element
    var selector = document.getElementById('selDataset');

    // Get the list of tickers to populate the select options
    Plotly.d3.json(`/tickers/${ticker}`, function(error, companyNames) {
        for (var i = 0; i < companyNames.length;  i++) {
            var currentOption = document.createElement('option');
            currentOption.text = companyNames[i];
            currentOption.value = companyNames[i]
            selector.appendChild(currentOption);
        }
    })
}


function getMonthlData() {
  var queryUrl = `https://www.quandl.com/api/v3/datasets/WIKI/${ticker}.json?start_date=2016-10-01&end_date=2017-10-01&collapse=monthly&api_key=${apiKey}`;
    Plotly.d3.json(queryUrl, function(error, response) {
      var dates = unpack(response.dataset.data, 0);
      var openPrices = unpack(response.dataset.data, 1);
      var highPrices = unpack(response.dataset.data, 2);
      var lowPrices = unpack(response.dataset.data, 3);
      var closingPrices = unpack(response.dataset.data, 4);
      var volume = unpack(response.dataset.data, 5);
      buildTable(dates, openPrices, highPrices, lowPrices, closingPrices, volume);
    });
}


var austin_weather = [
    { date: "2018-02-01", low: 51, high: 76},
    { date: "2018-02-02", low: 47, high: 59},
    { date: "2018-02-03", low: 44, high: 59},
    { date: "2018-02-04", low: 52, high: 73},
    { date: "2018-02-05", low: 47, high: 71},
]
// YOUR CODE HERE

function buildTable(dates, openPrices, highPrices, lowPrices, closingPrices, volume) {

  d3.select("tbody")
      .selectAll("li") // dont know if this is necesssary
      .enter()
      .append("tr")
      .html(function(d) {
        return `<td> ${dates} </td>
          <td> ${openPrices} </td>
          <td> ${highPrices} </td>
          <td> ${lowPrices} </td>
          <td> ${closingPrices} </td>
          <td> ${volume} </td>`;
      });
}

function buildPlot() {

  var url = `https://www.quandl.com/api/v3/datasets/WIKI/${ticker}.json?start_date=2016-10-01&end_date=2017-10-01&api_key=${apiKey}`;

  Plotly.d3.json(url, function(error, response) {

    if (error) return console.warn(error);

    // Grab values from the response json object to build the plots
    var name = response.dataset.name;
    var stock = response.dataset.dataset_code;
    var startDate = response.dataset.start_date;
    var endDate = response.dataset.end_date;
    var dates = unpack(response.dataset.data, 0);
    var openingPrices = unpack(response.dataset.data, 1);
    var highPrices = unpack(response.dataset.data, 2);
    var lowPrices = unpack(response.dataset.data, 3);
    var closingPrices = unpack(response.dataset.data, 4);

    getMonthlData();

    var trace1 = {
      type: "scatter",
      mode: "lines",
      name: name,
      x: dates,
      y: closingPrices,
      line: {
        color: "#17BECF"
      }
    };

    // Candlestick Trace
    var trace2 = {
      type: "candlestick",
      x: dates,
      high: highPrices,
      low: lowPrices,
      open: openingPrices,
      close: closingPrices
    };

    var data = [trace1, trace2];

    var layout = {
      title: `${stock} closing prices`,
      xaxis: {
        range: [startDate, endDate],
        type: "date"
      },
      yaxis: {
        autorange: true,
        type: "linear"
      },
      showlegend: false
    };

    Plotly.newPlot("plot", data, layout);
  });
}

buildPlot();



function getNewsArticles() {
  d3.json(`https://api.iextrading.com/1.0/stock/${ticker}/news/last/3`, function(error, json) {
    if (error) return console.warn(error);
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
        .html(`<div class="wrapped-box">
              <h3> <a href="${articleJson.url}" target="_blank"> ${articleJson.headline} </a> </h3>
              <h5> ${dateStr} </h5>
              <br />
              <p> ${articleJson.summary} </p>
              <p> Source: ${articleJson.source} </p>
              </div>
              <br />`);
}

function optionChanged(newSample) {
    // Fetch new data each time a new sample is selected
    getData(newSample, updateCharts);
}


function init() {
    getTickers();
    getNewsArticles();
}

init();
