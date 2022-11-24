const buttonPrevPhoto = document.querySelector('#prev_photo');
const buttonNextPhoto = document.querySelector('#next_photo');
const photoTrack = document.querySelector('#photo_track');
const photoInner = document.querySelector('#photo_inner');
const trackRect = photoTrack.getClientRects()[0];
const widthPhotoContainer = Math.round(trackRect.width);
const menuPrev = document.querySelector('.photo-menu__left');
const menuNext = document.querySelector('.photo-menu__right');
const placePhotos = document.querySelector('.place-photos');
const mapCanvas = document.querySelector('#map-canvas');
const MARGIN_PHOTO = 2;
const PREFIX = 'uktus';
const PREFIX_ID = 'place_photo_';

const scrollPoints = {
  margin: 0,
  x: 0,
  points: [],
  currentPoint: 0,
  containerWidth: 0,
  append: function(width, id){
    this.x += this.margin;
    const addPoint = (w)=>{
      this.points.push({
        x: this.x,
        width: width,
        id: id
      });
      if (w > this.containerWidth){
        let d = 0;
        if ((w - this.containerWidth) > this.containerWidth){
          d = this.containerWidth;
        }
        else{
          d = w - this.containerWidth;
        }
        this.x += d;
        addPoint(w - d);
      }
      else{
        this.x += w
      }
    };
    addPoint(width);
    this.x += this.margin;
  },
  insert: function(width, id){
    this.x = this.points[this.currentPoint].x;
    const id_before = this.points[this.currentPoint].id;
    const highArr = this.points.splice(this.points.findIndex(elem=>elem.id === id_before));
    this.append(width, id);
    const index = this.points.length;
    this.points = this.points.concat(highArr);
    this._recalc(index + 1, width + 2 * MARGIN_PHOTO);
  },
  prev: function(){
    if (this.currentPoint > 0){
      if (this.currentPoint === (this.points.length - 1)){
        this.onNextToLast();
      }

      this.setCurrent(this.currentPoint - 1);
    }
    return this.points[this.currentPoint].x;
  },
  next: function(){
    if (this.currentPoint < (this.points.length - 1)){
      if (this.currentPoint === 0){
        this.onSecond();
      }
      this.setCurrent(this.currentPoint + 1);
    }
    return this.points[this.currentPoint].x;
  },
  setCurrent: function (index){
    this.currentPoint = index;
    if (this.currentPoint === 0){
      this.onFirst();
    }
    if (this.currentPoint === (this.points.length - 1)){
      this.onLast();
    }
  },
  width: function(){
    const last = this.points[this.points.length - 1];
    return last.width + last.x;
  },
  _recalc: function (index, deductible){
    this.points = this.points.map((elem, ind)=>{
      if(ind < index){
        return elem;
      }
      elem.x += deductible;
      return elem;
    });
  },
  delete: function(){
    const id = this.points[this.currentPoint].id;
    const index = this.points.findIndex(elem=>elem.id === id);
    this.points = this.points.filter(elem=>elem.id !== id);
    this._recalc(index,-this.points[index].width + 2 * MARGIN_PHOTO)
  },
  onFirst: ()=>{},
  onLast: ()=>{},
  onSecond: ()=>{},
  onNextToLast: ()=>{}
}

scrollPoints.margin = MARGIN_PHOTO;
scrollPoints.containerWidth = widthPhotoContainer;
scrollPoints.onFirst = ()=>{
  menuPrev.classList.add('photo-menu-hide');
}
scrollPoints.onLast = ()=>{
  menuNext.classList.add('photo-menu-hide');
}
scrollPoints.onSecond = ()=>{
  menuPrev.classList.remove('photo-menu-hide');
}
scrollPoints.onNextToLast = ()=>{
  menuNext.classList.remove('photo-menu-hide');
}

const images = {
  uktus1: {height: 960, width: 1280},
  uktus2: {height: 590, width: 839},
  uktus3: {height: 545, width: 1000},
  uktus5: {height: 637, width: 1000},
  uktus6: {height: 1440, width: 1920},
  uktus4: {height: 400, width: 1590},
}

const addImage = (img, id, widthPhoto)=>{
  const div = document.createElement('div');
  div.classList.add('photo');
  div.style.width = `${widthPhoto}px`;
  div.id = id;
  div.append(img);
  return div;
}

const getWidthPhoto = (height, width)=>{
  const heightPhoto = Math.round(trackRect.height);
  return Math.round(heightPhoto / height * width);
}

const renderPhotos = ()=>{
  for(let i = 1; i < 7; i++){
    const imgName = `${PREFIX}${i}`;
    const widthPhoto = getWidthPhoto(images[imgName].height, images[imgName].width);
    const img = document.createElement('img');
    img.src = `../../static/src/${imgName}.jpg`;
    const id = `${PREFIX_ID}${i}`
    photoInner.append(addImage(img, id, widthPhoto));
    scrollPoints.append(widthPhoto, id);
  }
  placePhotos.classList.remove('place-photos-empty')
  if (scrollPoints.width() > widthPhotoContainer){
    menuNext.classList.remove('photo-menu-hide');
    menuPrev.classList.remove('photo-menu-hide');
  }
  scrollPoints.setCurrent(0);
}

renderPhotos();

buttonNextPhoto.addEventListener('click', ()=>{
  photoTrack.scroll(scrollPoints.next(), 0)
})

buttonPrevPhoto.addEventListener('click', ()=>{
  photoTrack.scroll(scrollPoints.prev(), 0)
})

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

export {
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
};