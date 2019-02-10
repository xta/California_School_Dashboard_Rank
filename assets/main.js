$(function() {

    // global

    window.Schools = window.Schools || {};

    // setup map

    // LA
    var map_center = [34.0928092, -118.3286614];

    var base_layer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
    });

    Schools.Map = L.map('map', {
        center: map_center,
        zoom: 11,
        scrollWheelZoom: false,
        layers: [base_layer]
    });

    // setup school groups

    var eil_mapping = {
        'Elementary': 'Elementary',
        'Intermediate/Middle/Junior High': 'Middle',
        'High School': 'High',
        'Elementary-High Combination': 'K-12',
    }

    Schools.Groups = {};
    Object.keys(eil_mapping).forEach(function (key) {
        var value = eil_mapping[key];
        Schools.Groups[value] = [];
    })

    // get map data

    $.getJSON('./data/top_schools_2018_by_math_and_english.json', function(data) {
        var schools = data['schools'];
        handleData(schools);
    });

    // data handler

    function handleData(schools) {
        for (i = 0; i < schools.length; i++) {
            var school = schools[i];

            var coord = [parseFloat(school.latitude), parseFloat(school.longitude)];
            var name = school.school_name;
            var marker = L.marker(coord).bindPopup(name);

            var eil = school.eil_name;
            var eil_key = eil_mapping[eil];
            Schools.Groups[eil_key].push(marker);
        }

        var elementary = L.layerGroup(Schools.Groups['Elementary']);
        var middle = L.layerGroup(Schools.Groups['Middle']);
        var high = L.layerGroup(Schools.Groups['High']);
        var k_12 = L.layerGroup(Schools.Groups['K-12']);

        Schools.Map.addLayer(elementary);
        Schools.Map.addLayer(middle);
        Schools.Map.addLayer(high);
        Schools.Map.addLayer(k_12);

        var overlayMaps = {
            'Elementary': elementary,
            'Middle': middle,
            'High': high,
            'K-12': k_12,
        };

        L.control.layers(null, overlayMaps, {collapsed: false}).addTo(Schools.Map);
    }

});
