import 'ol/ol.css';
import './index.css';

import { Feature, Map, View } from 'ol';
import { fromLonLat } from 'ol/proj';
import { Point } from 'ol/geom';
import { Vector as VectorLayer, Tile } from 'ol/layer';
import { Vector as VectorSource, Cluster, OSM } from 'ol/source';
import { Circle, Fill, Stroke, Style, Text } from 'ol/style';
import { defaults, FullScreen } from 'ol/control';

// get the coordinates
const features = window.atlas_people_coords.map((p) => new Feature(new Point(fromLonLat([p[1], p[0]]))));
const source = new VectorSource({features});

// create a cluster from this source
const clusterSource = new Cluster({
    distance: 40,
    source,
});


// create some clusters
var clusterLayer = new VectorLayer({
    source: clusterSource,
    style: (feature) => new Style({
        image: new Circle({
            radius: 10,
            stroke: new Stroke({ color: '#fff' }),
            fill: new Fill({ color: '#3399CC' })
        }),
        text: new Text({
            text: (feature.get('features').length).toString(),
            fill: new Fill({ color: '#fff' })
        })
    }),
});

// the source for all the images is OpenStreetMap
const osmTileLayer = new Tile({ source: new OSM() });

// finally: create a map
new Map({
    layers: [osmTileLayer, clusterLayer],
    controls: defaults().extend([
        new FullScreen() 
    ]),
    target: 'map',
    view: new View({
        center: [0, 0],
        zoom: 2
    })
});