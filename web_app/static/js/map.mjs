const MAP_ZOOM = 13;
const MAIN_PIN_SIZE = 52;
const COORDINATES_PRECISION = 5;
const MAP_CENTER = [56.79160,  60.63525];
const MAIN_PIN_ICON = {
  iconUrl: '../../static/img/main-pin.svg',
  iconSize: [MAIN_PIN_SIZE, MAIN_PIN_SIZE],
  iconAnchor: [MAIN_PIN_SIZE / 2, MAIN_PIN_SIZE],
};

const map = L.map('map-canvas',{
  center: MAP_CENTER,
  zoom: MAP_ZOOM
})
//let currentMarker = null;

L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  },
).addTo(map);

const mainMarker = L.marker(
  MAP_CENTER,
  {
    draggable: true,
    icon: L.icon(MAIN_PIN_ICON)
  }
);

mainMarker.addTo(map);

export{COORDINATES_PRECISION, mainMarker, MAP_CENTER}