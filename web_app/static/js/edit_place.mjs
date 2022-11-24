import './place.mjs';
import {
  scrollPoints,
  images,
  addImage,
  PREFIX,
  PREFIX_ID,
  getWidthPhoto,
  MAP_CENTER,
  MAIN_PIN_ICON,
  COORDINATES_PRECISION,
  map
} from './place.mjs'
console.log('edit place');
const buttonAddPhoto = document.querySelector('#add_photo');
const buttonRemovePhoto = document.querySelector('#remove_photo');
const menuPhoto = document.querySelector('#menu_photo');
const photoInner = document.querySelector('#photo_inner');
const inputFile = document.querySelector('#input_file');
const inputLocation = document.querySelector('#place_location');
const FILE_TYPES = ['jpg', 'jpeg', 'png', 'svg', 'ico', 'bmp', 'gif'];


console.log(scrollPoints);

menuPhoto.classList.remove('photo-menu-hide');
buttonAddPhoto.addEventListener('click', ()=>{
  inputFile.click();
});

buttonRemovePhoto.addEventListener('click', ()=>{
  const deletePhoto = document.querySelector(`#${scrollPoints.points[scrollPoints.currentPoint].id}`);
  deletePhoto.remove();
  scrollPoints.delete();
  console.log(scrollPoints.points[scrollPoints.currentPoint].id);
});

const onLoadPhoto = (evt)=>{
  const beforePhoto = document.querySelector(`#${scrollPoints.points[scrollPoints.currentPoint].id}`);
  const heightPhoto = evt.target.naturalHeight;
  const widthPhoto = evt.target.naturalWidth;
  const id = `${PREFIX_ID}${Object.keys(images).length + 1}`;
  const width = getWidthPhoto(heightPhoto, widthPhoto);
  photoInner.insertBefore(addImage(
    evt.target, id, width
    ), beforePhoto
  );
  scrollPoints.insert(getWidthPhoto(heightPhoto, widthPhoto), id);
}

const addPhoto = ()=>{
  const file = inputFile.files[0];
  const fileName = file.name.toLowerCase();
  const matches = FILE_TYPES.some((it) => fileName.endsWith(it));
  if (!matches)
  {
    return;
  }
  const img = document.createElement('img');
  img.src = URL.createObjectURL(file);
  img.addEventListener('load', onLoadPhoto);

  console.log(`add photo ${inputFile.files.length}`);
}
inputFile.addEventListener('change', addPhoto, false);

const fillAddress = (location)=>{
  inputLocation.value = `${location.lat.toFixed(COORDINATES_PRECISION)},
  ${location.lng.toFixed(COORDINATES_PRECISION)}`;
};

const mainMarker = L.marker(
  MAP_CENTER,
  {
    draggable: true,
    icon: L.icon(MAIN_PIN_ICON)
  }
);

mainMarker.addTo(map);

mainMarker.on('move', (evt) => {
  fillAddress(evt.target.getLatLng());
});

