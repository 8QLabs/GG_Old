/**
 * Created by rajiv on 6/11/15.
 */

var GeoGekko = window.GeoGekko || {};
GeoGekko.MapEngine = {};

var HastensLocationsGeoJson = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [-74.0028646, 40.7217199]
        },
        "properties": {
            "title": "Hastens SoHo",
            "description": "75 Grand St, New York, NY 10013",
            "marker-color": "#1E90FF",
            "marker-size": "medium",
            "filter-start-point": true
        }
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [-73.9898921, 40.7379194]
        },
        "properties": {
            "title": "Hastens Union Square",
            "description": "876 Broadway, New York, NY 10003",
            "marker-color": "#1E90FF",
            "marker-size": "medium"
        }
    },
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [-73.96078, 40.778516]
        },
        "properties": {
            "title": "Hastens Madison Ave",
            "description": "1100 Madison Ave, New York, NY 10028",
            "marker-color": "#1E90FF",
            "marker-size": "medium"
        }
    }
];

GeoGekko.FeatureLayers = {
    'hastens-locations': {
        name: 'hastens-locations',
        data: HastensLocationsGeoJson,
        active: true,
        filterable: false,
        onClick: function () {

        }
    },
    'nyc-taxi': {
        name: 'nyc-taxi',
        active: true,
        dataUrl: '/map/filter',
        startPoint: [40.7217199, -74.0028646],  // hastens soho locations
        cssIcon: L.divIcon({
            // Specify a class name we can refer to in CSS.
            className: 'css-icon',
            // Set marker width and height
            iconSize: [2, 2]
        }),
        filterFn: function () {

        }
    },
    'meetup': {
        name: 'meetup',
        dataUrl: '/map/filter',
        active: false
    },
    'tweets': {
        name: 'tweets',
        dataUrl: '/map/filter',
        active: false
    }
};

var GG = (function () {
    var _latitude;
    var _longitude;
    var _mapEngine;

    function _showMap () {
        _mapEngine = new GeoGekko.MapEngine.Mapbox();
        _mapEngine.renderMap(_latitude, _longitude);
    }

    function _init (lat, lon) {
        _latitude = lat;
        _longitude = lon;
        _showMap();
        _setupEvents();

        _mapEngine.renderLayers(GeoGekko.FeatureLayers);
    }

    function _setupEvents () {
        $('#filter').click(function () {
            GG.filterLayer('nyc-taxi', 40.7217199, -74.0028646, $('#filter-form').serialize());
        })
    }

    return {
        init: function (lat, lon) {
            _init(lat, lon);
        },

        filterLayer: function (layerName, lat, lon, filters) {
            _mapEngine.filterLayer(layerName, lat, lon, filters);
        }
    };
})();

GeoGekko.MapEngine.Mapbox = function () {
    var _map;
    var _accessToken = 'pk.eyJ1IjoiOHFsYWJzIiwiYSI6IjJYcnhObFEifQ.cqWyVvIXQf0BJp6hatERmw';
    var _featureLayers = {};

    function resetColors(featureLayer, geoJson) {
        for (var i = 0; i < geoJson.length; i++) {
            geoJson[i].properties['marker-color'] = geoJson[i].properties['old-color'] ||
                geoJson[i].properties['marker-color'];
        }
        featureLayer.setGeoJSON(geoJson);
    }

    function _showLayer (layer) {
        if (!layer.active) return;

        if (layer.data) {
            console.log('Loading data for layer...' + layer.data);

            //find filtering start point
            for (var i = 0; i < layer.data.length; i++) {
                if (layer.data[i].properties['filter-start-point']) {
                    layer.data[i].properties['old-color'] = layer.data[i].properties['marker-color'];
                    layer.data[i].properties['marker-color'] = '#ff8888';
                }
            }

            var featureLayer = L.mapbox.featureLayer(layer.data).addTo(_map);

            featureLayer.on('click', function(e) {
                console.log(e);

                //reset markers
                for (var i = 0; i < layer.data.length; i++) {
                    layer.data[i].properties['marker-color'] = layer.data[i].properties['old-color'] ||
                        layer.data[i].properties['marker-color'];
                }
                featureLayer.setGeoJSON(layer.data);

                e.layer.feature.properties['old-color'] = e.layer.feature.properties['marker-color'];
                e.layer.feature.properties['marker-color'] = '#ff8888';
                featureLayer.setGeoJSON(layer.data);

                GG.filterLayer('nyc-taxi', e.latlng.lat, e.latlng.lng, $('#filter-form').serialize());
            });

            _featureLayers[layer.name] = featureLayer;
        }
        else if (layer.dataUrl) {
            if (layer.startPoint) {
                var lat = layer.startPoint[0];
                var lon = layer.startPoint[1];
                var url = '/map/filter?lat=' + lat + '&lon=' + lon;
                console.log(url);
                var featureLayer = L.mapbox.featureLayer(url).addTo(_map);

                if (layer.cssIcon) {
                    // Set a custom icon on each marker based on feature properties.
                    featureLayer.on('layeradd', function (e) {
                        var marker = e.layer,
                                feature = marker.feature;

                        marker.setIcon(layer.cssIcon);
                    });
                }

                _featureLayers[layer.name] = featureLayer;
            }

        }
        else {
            console.log('No way to get data for this layer....');
        }
    }

    this.filterLayer = function (layerName, lat, lon, filters) {
        var featureLayer = _featureLayers[layerName];
        if (featureLayer)
            _map.removeLayer(featureLayer);

        var url = '/map/filter?lat=' + lat + '&lon=' + lon;
        if (filters) {
            url += '&' + filters;
        }
        console.log(url);
        featureLayer = L.mapbox.featureLayer(url).addTo(_map);

        if (GeoGekko.FeatureLayers[layerName].cssIcon) {
            // Set a custom icon on each marker based on feature properties.
            featureLayer.on('layeradd', function (e) {
                var marker = e.layer,
                    feature = marker.feature;

                marker.setIcon(GeoGekko.FeatureLayers[layerName].cssIcon);
            });
        }

        _featureLayers[layerName] = featureLayer;
    }

    this.renderMap = function (lat, lon) {
        L.mapbox.accessToken = _accessToken;
        _map = L.mapbox.map('map', 'mapbox.light')
            .setView([lat, lon], 13)
            .addControl(L.mapbox.geocoderControl('mapbox.places', {autocomplete: true}).on('select', function (e) {
//                var lat = e.feature.center[1];
//                var lon = e.feature.center[0];
//                GG.filterLayer(lat, lon);
            })
        );
    }

    this.renderLayers = function (_dataLayers) {
        console.log('Rendering layers...');
        for (var i in _dataLayers) {
            _showLayer(_dataLayers[i]);
        }
    }
}
