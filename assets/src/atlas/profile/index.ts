import 'ol/ol.css';
import './index.css';

import { Feature, Map, View } from 'ol';
import { fromLonLat } from 'ol/proj';
import { Point } from 'ol/geom';
import { Vector as VectorLayer, Tile } from 'ol/layer';
import { Vector as VectorSource, OSM } from 'ol/source';
import { Circle, Fill, Stroke, Style } from 'ol/style';


// apply the college color
const collegeEle = document.getElementById('college') as HTMLElement | null;
if (collegeEle) {
    var college = parseInt(collegeEle.getAttribute('data-college')||"0", 10);
    var collegeColor = ['', 'red', 'blue', 'green', 'yellow', 'white'][college];
    var collegeBackground = ['white', 'white', 'white', 'white', 'black', 'black'][college];
    collegeEle.style.backgroundColor = collegeColor;
    collegeEle.style.color = collegeBackground;
}

// coordinates needs
const coords = [window.alumni_profile_point[1], window.alumni_profile_point[0]];
const proj = fromLonLat(coords);
const feature = new Feature({
    geometry: new Point(proj)
});

// create a feature layer
const featureLayer = new VectorLayer({
    source: new VectorSource({ features: [feature] }),
    style: () => new Style({
        image: new Circle({
            radius: 10,
            stroke: new Stroke({ color: '#fff' }),
            fill: new Fill({ color: '#3399CC' })
        }),
    })
});

// the source for all the images is OpenStreetMap
const osmTileLayer = new Tile({ source: new OSM() });

// finally: create a map
new Map({
    layers: [osmTileLayer, featureLayer],
    target: 'map',
    view: new View({
        center: proj,
        zoom: 4,
    }),
});