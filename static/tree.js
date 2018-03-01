window.onload=function(){
    var $totalInput = document.querySelector("#total");
    var $austinInput = document.querySelector("#austin");
    var $marketInput = document.querySelector("#market");
    $totalInput.addEventListener("click", handleTotalInputClick);
    $austinInput.addEventListener("click", handleAustinInputClick);
    $marketInput.addEventListener("click", handlemarketInputClick);
    make_viz(atxData,"austin_staff_cnt");
};

function handleAustinInputClick() {
    make_viz(atxData,"austin_staff_cnt");
};

function handlemarketInputClick() {
    make_viz(atxData,"marketcap");
};

function handleTotalInputClick() {
    make_viz(atxData,"comp_staff_cnt");
};


function make_viz(data,value) {
    d3.select("#viz").html("");
    var visualization = d3plus.viz()
        .container("#viz")
        .data(data)
        .type("tree_map")
        .id("name")
        .size(value)
        .draw()
};
