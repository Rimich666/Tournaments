import './map.mjs';
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
  currentPoint: -1,
  containerWidth: 0,
  scroll: false,
  first: true,
  last: true,
  width: 0,
  _setScroll: function(deductible){
    this.width += deductible;
    this.scroll = this.width > this.containerWidth;
    this.setCurrent(this.currentPoint);
    /*if (!this.scroll){
      this.onFirst();
      this.onLast();
      return;
    }
    if (this.currentPoint > 0 && this.first){
      this.first = false;
      this.onSecond();
    }
    if ((this.width - this.points[this.currentPoint].x) > this.containerWidth && this.last){
      this.last = false;
      this.onNextToLast();
    }*/
  },
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
    if (this.currentPoint < 0){
      this.currentPoint = 0;
    }
    this._setScroll(width + 2 * this.margin);
  },
  insert: function(width, id){
    const id_before = this.points[this.currentPoint].id;
    this.setCurrent(this.points.findIndex(elem=>elem.id === id_before));
    this.x = this.points[this.currentPoint].x - this.margin;
    const highArr = this.points.splice(this.currentPoint);
    this.append(width, id);
    const index = this.points.length;
    this.points = this.points.concat(highArr);
    this._recalc(index, width + 2 * MARGIN_PHOTO);
    return this.points[this.currentPoint].x;
  },
  prev: function(){
    if (this.currentPoint > 0){
      this.setCurrent(this.currentPoint - 1);
    }
    return this.points[this.currentPoint].x;
  },
  next: function(){
    if (this.currentPoint < (this.points.length - 1)){
      this.setCurrent(this.currentPoint + 1);

    }
    return this.points[this.currentPoint].x;
  },
  setCurrent: function (index){
    if (index < 0 || index >= this.points.length){
      return;
    }
    this.currentPoint = index;
    console.log(`currentPoint: ${this.currentPoint}`);
    if (this.currentPoint > 0 && this.scroll && this.first){
      this.first = false;
      this.onSecond();
    }
    if (this.currentPoint === 0 && !this.first){
      this.first = true;
      this.onFirst();
    }

    if ((this.width - this.points[this.currentPoint].x) > this.containerWidth && this.last){
      this.last = false;
      this.onNextToLast();
    }
    if ((this.width - this.points[this.currentPoint].x) <= this.containerWidth && !this.last){
      this.last = true;
      this.onLast();
    }
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
    const deductible = -(this.points[index].width + 2 * this.margin);
    this.points = this.points.filter(elem=>elem.id !== id);
    this._recalc(index, deductible);
    this._setScroll(deductible);
  },
  onFirst: ()=>{},
  onLast: ()=>{},
  onSecond: ()=>{},
  onNextToLast: ()=>{}
}

scrollPoints.margin = MARGIN_PHOTO;
scrollPoints.containerWidth = widthPhotoContainer;
scrollPoints.onFirst = ()=>{
  console.log('on first');
  menuPrev.classList.add('photo-menu-hide');
}
scrollPoints.onLast = ()=>{
  console.log('on last');
  menuNext.classList.add('photo-menu-hide');
}
scrollPoints.onSecond = ()=>{
  menuPrev.classList.remove('photo-menu-hide');
}
scrollPoints.onNextToLast = ()=>{
  menuNext.classList.remove('photo-menu-hide');
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
  placePhotos.classList.remove('place-photos-empty');
  if (scrollPoints.width() > widthPhotoContainer){
    menuNext.classList.remove('photo-menu-hide');
    menuPrev.classList.remove('photo-menu-hide');
  }
  scrollPoints.setCurrent(0);
}

//renderPhotos();

buttonNextPhoto.addEventListener('click', ()=>{
  photoTrack.scroll(scrollPoints.next(), 0)
})

buttonPrevPhoto.addEventListener('click', ()=>{
  photoTrack.scroll(scrollPoints.prev(), 0)
})

export {
  scrollPoints,
  addImage,
  getWidthPhoto,
};