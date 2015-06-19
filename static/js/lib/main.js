/**
 * Created by rajiv on 6/11/15.
 */

var GeoGekko = window.GeoGekko || {};

var HastensLocationsGeoJson =  [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [40.7217199, -74.0028646]
        },
        "properties": {
            "title": "Hastens SoHo",
            "description": "1714 14th St NW, Washington DC",
            "marker-color": "#fc4353",
            "marker-size": "medium",
            "marker-symbol": "store"
        }
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [40.7379194, -73.9898921]
        },
        "properties": {
            "title": "Hastens Union Square",
            "description": "155 9th St, San Francisco",
            "marker-color": "#fc4353",
            "marker-size": "medium",
            "marker-symbol": "store"
        }
    }
];

var GG = (function () {
    var _latitude;
    var _longitude;
    var _mapEngine;
    var _filters;

    var _dataLayers = [
        {
            type: 'hastens-locations',
            data: HastensLocationsGeoJson,
            active: true,
            filterable: false,
            onClick: function () {

            }
        }, {
            type: 'nyc-taxi',
            active : true,
            dataUrl: '/map/filter',
            cssIcon:  L.divIcon({
                // Specify a class name we can refer to in CSS.
                className: 'css-icon',
                // Set marker width and height
                iconSize: [2, 2]
            })
        }, {
            type: 'meetup',
            dataUrl: '/map/filter',
            active: false
        },{
            type: 'tweets',
            dataUrl: '/map/filter',
            active: false
        }
    ];

    function _showMap () {
        _mapEngine = new GeoGekko.MapEngine.Mapbox().renderMap();
    }

    function _init (lat, lon) {
        _latitude = lat;
        _longitude = lon;
        _showMap();
        _setupEvents();

        GG.filterLayer(40.7217199, -74.0028646);
    }

    function _setupEvents () {
        $('#filter').click(function () {
            GeoGekko.filterLayer(40.7217199, -74.0028646, $('#filter-form').serialize());
        })
    }

    function _showActiveLayers () {
        for (var layer in dataLayers) {
            if (layer.data) {
                _showLayer(layer);
            }
        }
    }

    function _showLayer (layer) {
        for (var feature in layer.data) {
            _mapEngine.addMarker(feature);
        }
    }

    return {
        init: function (lat, lon) {
            _init(lat, lon);
        },

        filterDataLayer: function (lat, lon, filter) {
            if (featureLayer)
                map.removeLayer(featureLayer);

            var url = '/map/filter?lat=' + lat + '&lon=' + lon;
            if (filter) {
                url += '&' + filter;
            }
            console.log(url);
            featureLayer = L.mapbox.featureLayer().loadURL(url).addTo(map);

            // Set a custom icon on each marker based on feature properties.
            featureLayer.on('layeradd', function (e) {
                var marker = e.layer,
                        feature = marker.feature;

                marker.setIcon(cssIcon);
            });

            addStoreMarkers();
        }
    };
})();

GeoGekko.MapEngine.Mapbox = function () {
    var _map;
    var _accessToken = 'pk.eyJ1IjoiOHFsYWJzIiwiYSI6IjJYcnhObFEifQ.cqWyVvIXQf0BJp6hatERmw';
    var _layers = {};

    this.renderMap = function (lat, lon) {
        L.mapbox.accessToken = _accessToken;
        _map = L.mapbox.map('map', 'mapbox.light')
            .setView([lat, lon], 13)
            .addControl(L.mapbox.geocoderControl('mapbox.places', {autocomplete: true}).on('select', function (e) {
                var lat = e.feature.center[1];
                var lon = e.feature.center[0];
                GeoGekko.filterLayer(lat, lon);
            })
        );
    }

    this.createLayer = function (layerName, geoJson) {
        _layers[layerName] = {
            geoJson: geoJson
        }
    }

    this.removeLayer = function (layerName) {

    }

    this.addMarker = function (markerJson) {
        L.marker([40.7217199, -74.0028646]).addTo(_map);  // soho
    }

    (function () {

    })();
}

GeoGekko.MapEngine..Google = function () {

    this.renderMap = function () {
        console.log('Not Implemented');
    }

    this.addMarker = function () {
        console.log('Not Implemented');
    }
}
