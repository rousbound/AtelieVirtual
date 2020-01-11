
    var mymap = L.map('mapid').setView([-22.94, -43.18], 13);

    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', { attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors' }).addTo(mymap);


console.log(typeof(data));
var layerGroup = L.layerGroup().addTo(mymap);

function clicked(){
  layerGroup.clearLayers();
  var input_value = document.getElementById('data').value;
  for(i=0; i < busData.length; i++){
    var name = parseInt(busData[i][0]);
      if (name === parseInt(input_value)){
        let lat  = parseFloat(busData[i][1]);
        let lon  = parseFloat(busData[i][2]);
        L.marker([lat,lon]).addTo(layerGroup)
    }
  };
}

document.getElementById('btn').addEventListener('click', clicked);;


