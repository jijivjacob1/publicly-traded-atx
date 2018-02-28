window.onload=function(){
    var $totalInput = document.querySelector("#total");
    var $austinInput = document.querySelector("#austin");
    var $marketInput = document.querySelector("#market");
    $totalInput.addEventListener("click", handleTotalInputClick);
    $austinInput.addEventListener("click", handleAustinInputClick);
    $marketInput.addEventListener("click", handlemarketInputClick);
}

function handleAustinInputClick() {
    make_viz(test,"austin_staff_cnt");
}

function handlemarketInputClick() {
    make_viz(test,"marketcap");
}

function handleTotalInputClick() {
    make_viz(test,"comp_staff_cnt");
}

var test = [];

d3.csv("clean_company_list.csv", function (error, austinData) {
    if (error) return console.error(error);
    console.log(austinData);
    test = austinData;
    for (var i = 0; i < test.length; i++) {
        test[i]["austin_staff_cnt"] = parseInt(test[i]["austin_staff_cnt"]);
        test[i]["comp_staff_cnt"] = parseInt(test[i]["comp_staff_cnt"]);
        test[i]["marketcap"] = parseInt(test[i]["marketcap"]);
        console.log(test[i]);
    };

    make_viz(test,"austin_staff_cnt")
});

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
