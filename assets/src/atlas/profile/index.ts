
import './index.css';

async function init() {
    await import('ol/ol.css');

    const { Feature, Map, View } = await import(/* webpackChunkName: "ol" */ 'ol');
    const { fromLonLat } = await import(/* webpackChunkName: "olproj" */ 'ol/proj');
    const { Point } = await import(/* webpackChunkName: "olgeom" */ 'ol/geom');
    const { Vector: VectorLayer, Tile } = await import(/* webpackChunkName: "ollayer" */ 'ol/layer');
    const { Vector: VectorSource, OSM } = await import(/* webpackChunkName: "olsource" */ 'ol/source');
    const { Circle, Fill, Stroke, Style } = await import(/* webpackChunkName: "olstyle" */ 'ol/style');


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

}

init();