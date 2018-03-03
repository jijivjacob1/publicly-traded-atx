// load the database into the atxData variable
atxData = [];
queryURL = 'https://atxpubliccompanies.herokuapp.com/companies';
d3.json(queryURL, function (error, response) {
    if (error) {
        console.log(error);
    }
    else {
        atxData = response;
        var $totalInput = document.querySelector("#total");
        var $austinInput = document.querySelector("#austin");
        var $marketInput = document.querySelector("#market");
        $totalInput.addEventListener("click", handleTotalInputClick);
        $austinInput.addEventListener("click", handleAustinInputClick);
        $marketInput.addEventListener("click", handlemarketInputClick);
        make_viz(atxData, "austin_staff_cnt");
        // mapTags(atxData);
        buildMap();
    }
});

// Tree Chart functions

// window.onload=function(){

// };

function handleAustinInputClick() {
    make_viz(atxData, "austin_staff_cnt");
};

function handlemarketInputClick() {
    make_viz(atxData, "marketcap");
};

function handleTotalInputClick() {
    make_viz(atxData, "comp_staff_cnt");
};

function make_viz(data, value) {
    d3.select("#viz").html("");
    var visualization = d3plus.viz()
        .container("#viz")
        .data(data)
        .type("tree_map")
        .id("name")
        .size(value)
        .draw()
};

// Map Functions

function buildMap() {
    var myMap = L.map("map", {
        center: [30.26, -97.74],
        zoom: 9
    });
    // Add a tile layer
    L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?" +
        "access_token=pk.eyJ1IjoiZGF2aWR3aW5kc29yam9uZXMiLCJhIjoiY2pkaGp5NTl3MHpjcjMybzF3amJmamx4dyJ9.BiMjzvW8P7LbydGuff9qwg"
    ).addTo(myMap);
    mapTags(atxData);
    function mapTags(atxData) {
        console.log("mapTag" + atxData);
        latlng = [];
        loadData(atxData);
        function loadData(atxData) {
            for (var i = 0; i < atxData.length; i++) {
                latlng = [atxData[i].lat, atxData[i].lng];
                console.log(atxData[i].name + " : " + i);
                L.marker(latlng)
                    .bindPopup(`<a href="https://atxpubliccompanies.herokuapp.com/company/${atxData[i].tckr}">
                                      <h4> ${atxData[i].name} </h4></a> <br>
                                ${atxData[i].sector}
                                <hr>
                                ${atxData[i].address} <br>
                                ${atxData[i].city},  ${atxData[i].state}  ${atxData[i].zip_code} <br>
                                ${atxData[i].phn_nbr}`)
                    .addTo(myMap);
            };
        };
    };
}
