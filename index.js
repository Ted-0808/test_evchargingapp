const $ = require("jquery");
import L from 'leaflet';

//import cp_dbContract from "./contracts.js";

// console.log(test);

var mymap = L.map('mapid').setView([48.77, 9.16], 13);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  maxZoom: 14,
  id: 'mapbox.streets',
  accessToken: 'pk.eyJ1IjoidGVkbGkiLCJhIjoiY2p0emo3NHpxMHM4MzQ0cG5wYzA1Yzg4dyJ9.qNG-ioP-iKz9YkCsQHUPdA'
}).addTo(mymap);

var cp1 = L.marker([48.77, 9.16]).addTo(mymap).on('click', cp1InfoQuery);
var cp2 = L.marker([48.80, 9.20]).addTo(mymap).on('click', cp2InfoQuery);
var cp3 = L.marker([48.82, 9.18]).addTo(mymap).on('click', cp3InfoQuery);

cp1.bindPopup("<b>Parkstrom</b><br>Occupied<br>22kW AC<br>29 cents/kWh").openPopup();
cp2.bindPopup("<b>Innogy</b><br>available<br>50kW DC<br>49 cents/kWh").openPopup();
cp3.bindPopup("<b>E.on</b><br>available<br>150kW DC<br>89 cents/kWh").openPopup();


function cp1InfoQuery() {
  $("#keyid").html(" abc");
  $("#operatorid").html(" OLI");
  $("#typeid").html(" Type 2");
  $("#powerid").html(" 22kW AC");
  $("#statusid").html(" Occuplied");
  $("#priceid").html(" 29cent/kWh");
}

function cp2InfoQuery() {
  $("#keyid").html(" abc");
  $("#operatorid").html(" LEA");
  $("#typeid").html(" CCS");
  $("#powerid").html(" 50kW DC");
  $("#statusid").html(" Available");
  $("#priceid").html(" 49cent/kWh");
}

function cp3InfoQuery() {
  $("#keyid").html(" abc");
  $("#operatorid").html(" S&C");
  $("#typeid").html(" CCS");
  $("#powerid").html(" 150kW DC");
  $("#statusid").html(" Available");
  $("#priceid").html(" 89cent/kWh");
}