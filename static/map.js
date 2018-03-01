// Create a map object
var myMap = L.map("map", {
  center: [30.26, -97.74],
  zoom: 9
});

// Add a tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?" +
  "access_token=pk.eyJ1IjoiZGF2aWR3aW5kc29yam9uZXMiLCJhIjoiY2pkaGp5NTl3MHpjcjMybzF3amJmamx4dyJ9.BiMjzvW8P7LbydGuff9qwg"
).addTo(myMap);
mapTags();
// An array containing each company name, location, etc

function mapTags() {
  console.log("mapTag");
  latlng = [];
  for (var i = 0; atxData.length; i++){
      latlng = [atxData[i].lat ,atxData[i].lng];
       L.marker(latlng)
        .bindPopup("<h4>" + atxData[i].name + "</h4>" + "<br>"+"<hr> "
           + atxData[i].address + "<br>" + atxData[i].city + ", "+ atxData[i].state+" "+ atxData[i].zip_code+"<br>"+ atxData[i].phn_nbr )
        .addTo(myMap);    
     };
};

