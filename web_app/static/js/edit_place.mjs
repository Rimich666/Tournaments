import {
  scrollPoints,
  addImage,
  getWidthPhoto,
} from './place.mjs'
import {submitForm} from "./fetcher.mjs";
import {COORDINATES_PRECISION, mainMarker, MAP_CENTER} from "./map.mjs";

const buttonAddPhoto = document.querySelector('#add_photo');
const buttonRemovePhoto = document.querySelector('#remove_photo');
const menuPhoto = document.querySelector('#menu_photo');
const photoInner = document.querySelector('#photo_inner');
const photoTrack = document.querySelector('#photo_track');
const inputFile = document.querySelector('#input_file');
const inputLocation = document.querySelector('#place_location');
const FILE_TYPES = ['jpg', 'jpeg', 'png', 'svg', 'ico', 'bmp', 'gif'];
const form = document.querySelector('#place_add_form')
const PREFIX_NEW_ID = 'new_place_photo_';
const placePhotos = document.querySelector('.place-photos');

const images = {
  id: 0,
  getID: function(){
    this.id ++;
    return this.id;
  },
  added:[],
  attributes: {},
  deleted: [],
  appendAdded: function (id, attr, file){
    console.log(file);
    this.added.push({
      id: id,
      file: file
    });
    this.attributes[id] = attr;
  }
}

let placeLocation = {
  lat: MAP_CENTER[0],
  lng: MAP_CENTER[1]
}

menuPhoto.classList.remove('photo-menu-hide');
buttonAddPhoto.addEventListener('click', ()=>{
  inputFile.click();
});

buttonRemovePhoto.addEventListener('click', ()=>{
  const deletePhoto = document.querySelector(`#${scrollPoints.points[scrollPoints.currentPoint].id}`);
  deletePhoto.remove();
  scrollPoints.delete();
});

const insertPhoto = (img, width, id)=>{
  const beforePhoto = document.querySelector(`#${scrollPoints.points[scrollPoints.currentPoint].id}`);
  photoInner.insertBefore(addImage(
    img, id, width
    ), beforePhoto
  );
  photoTrack.scroll(scrollPoints.insert(width, id), 0);
}

const appendPhoto = (img, width, id)=>{
  photoInner.append(addImage(img, id, width));
  scrollPoints.append(width, id);
}

const onLoadPhoto = (evt)=>{
  const img = evt.target;
  const heightPhoto = img.naturalHeight;
  const widthPhoto = img.naturalWidth;
  const width = getWidthPhoto(heightPhoto, widthPhoto);
  const id = images.getID();
  const idDOM = `${PREFIX_NEW_ID}${id}`;
  images.appendAdded(id, {
    height: heightPhoto,
    width: widthPhoto,}, inputFile.files[0]);
  inputFile.disabled = false;
  if (scrollPoints.currentPoint < 0){
    appendPhoto(img, width, idDOM);
    placePhotos.classList.remove('place-photos-empty');
  }
  else{
    insertPhoto(img, width, idDOM);
  }
}

const addPhoto = ()=>{
  inputFile.disabled = true;
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
}
inputFile.addEventListener('change', addPhoto, false);

const fillAddress = (location)=>{
  inputLocation.value = `широта: ${location.lat.toFixed(COORDINATES_PRECISION)},
  долгота: ${location.lng.toFixed(COORDINATES_PRECISION)}`;
};

mainMarker.on('move', (evt)=>{
  fillAddress(evt.target.getLatLng());
});

mainMarker.on('dragend', (evt)=>{
  placeLocation = evt.target.getLatLng();
})

const onSuccess = (response)=>{
  return response.json()
  .then(console.log);
}

const onError = (msg)=>{
  console.log(...msg.headers);
  return msg.text()
  .then(console.log);
}

form.addEventListener('submit', (evt)=>{
  evt.preventDefault();
  const url = form.action;
  const formData = new FormData(form);
  images.added.forEach((elem)=>formData.append(elem.id,elem.file));
  formData.append('attributes', JSON.stringify(images.attributes));
  formData.set('location', JSON.stringify(placeLocation));
  submitForm(url, formData, onSuccess, onError);
});