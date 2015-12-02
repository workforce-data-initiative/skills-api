var LeafletLib = LeafletLib || {};
var kmeans_global;
var colors = ['#F1433F','#F7E967','#A9CF54','#70B7BA','#3D4C53', 'white'];
var LeafletLib = {
    latmin: 90,
    latmax: -90,
    lngmin: 180,
    lngmax: -180,
    searchRadius: 805,
    defaultCity: "",
    markers: [ ],
    geojson: [ ],
    leaflet_tracts: {},
    selectedTract: "17031839100",
    viewMode: 'traveling-to',
    legend: L.control({position: 'bottomright'}),

    initialize: function(element, features, centroid, zoom, kmeans) {
      
      kmeans_global = kmeans;

      LeafletLib.map = L.map(element).setView(new L.LatLng( centroid[0], centroid[1] ), zoom);
      LeafletLib.tiles =  L.tileLayer('https://{s}.tiles.mapbox.com/v3/datamade.hn83a654/{z}/{x}/{y}.png', {
          attribution: '<a href="http://www.mapbox.com/about/maps/" target="_blank">Terms &amp; Feedback</a>'
      }).addTo(LeafletLib.map);

      LeafletLib.map.attributionControl.addAttribution('LODES data &copy; <a href="http://census.gov/">US Census Bureau</a>');

      LeafletLib.geojson = L.geoJson(features, {
        style: LeafletLib.style,
        onEachFeature: LeafletLib.onEachFeature
      }).addTo(LeafletLib.map);

      LeafletLib.geojson.eachLayer(function (layer) {
        LeafletLib.leaflet_tracts[layer.feature.properties.tract_fips] = layer._leaflet_id;
      });
    },

    tractSelected: function (e) {
      var tract_fips = e.target.feature.properties.tract_fips;
      LeafletLib.selectedTract = tract_fips;
      LeafletLib.getConnectedTracts(tract_fips);
      //$('#tract_num').val(tract_fips);
    },
    
    getConnectedTracts: function (tract_fips) {
      //$("#tract_num").val(tract_fips);
      $.getJSON( "api/census_tract/"+tract_fips+"/5", function(data) {
        census_tract_hc(data)
      });
    },

    onEachFeature: function (feature, layer) {
      layer.on({
        click: LeafletLib.tractSelected
      });
    },

    style: function(feature) {
      color_index = 5;
      if (kmeans_global[feature.properties.tract_fips]!='undefined') {
          color_index = kmeans_global[feature.properties.tract_fips]; 
      }
      return {
        weight: 0.5,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.6,
        fillColor: colors[color_index] //getColor(feature.properties['2011']['total_jobs'], jenks_cutoffs)
      };
    }
}
