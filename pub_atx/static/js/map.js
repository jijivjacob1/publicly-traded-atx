// Create a map object
var myMap = L.map("map_div", {
  center: [30.26, -97.74],
  zoom: 9
});

// Add a tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
  "access_token=pk.eyJ1IjoiZGF2aWR3aW5kc29yam9uZXMiLCJhIjoiY2pkaGp5NTl3MHpjcjMybzF3amJmamx4dyJ9.BiMjzvW8P7LbydGuff9qwg"
).addTo(myMap);

// An array containing each company name, location, etc
latlng = [];
data = [];
d3.json("/companies", function (error, data) {
   if (error) return console.warn(error);
   console.log(data)
   data.forEach(function (d) {
    console.log(d)
     console.log(d.name, d.lat, d.lng);
     latlng = [d.lat ,d.lng];
     console.log(latlng);
     L.marker(latlng)
      .bindPopup("<h4>" + d.name + "</h4>" + "<br>"+"<hr> "
         + d.address + "<br>" +d.city + ", "+d.state+" "+d.zip_code+"<br>"+ d.phn_nbr )
      .addTo(myMap);    
    
   })
 });



