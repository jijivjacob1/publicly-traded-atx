
atxData = [];
queryURL = 'http://localhost:5000/companies';
d3.json(queryURL,function(error,response){
    if(error) {
        console.log(error);
    }
    else {
        atxData = response;
    }
});
