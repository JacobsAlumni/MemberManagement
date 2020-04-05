import './index.css';

async function init() {
    await import('ol/ol.css');

    const { Feature, Map, View } = await import(/* webpackChunkName: "ol" */ "ol");
    const { fromLonLat } = await import(/* webpackChunkName: "olproj" */ 'ol/proj');
    const { Point } = await import(/* webpackChunkName: "olgeom" */ 'ol/geom');
    const { Vector: VectorLayer, Tile } = await import(/* webpackChunkName: "ollayer" */ 'ol/layer');
    const { Vector: VectorSource, Cluster, OSM } = await import(/* webpackChunkName: "olsource" */ 'ol/source');
    const { Circle, Fill, Stroke, Style, Text } = await import(/* webpackChunkName: "olstyle" */ 'ol/style');
    const { defaults, FullScreen } = await import(/* webpackChunkName: "olcontrol" */ 'ol/control');
    
    // get the coordinates
    const features = window.atlas_people_coords.map((p) => new Feature(new Point(fromLonLat([p[1], p[0]]))));
    const source = new VectorSource({features});
    
    // create a cluster from this source
    const clusterSource = new Cluster({
        distance: 40,
        source,
    });
    
    
    // create some clusters
    const clusterLayer = new VectorLayer({
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
}

init();

