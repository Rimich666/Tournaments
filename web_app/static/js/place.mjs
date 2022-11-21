const buttonPrevPhoto = document.querySelector('#prev_photo');
const buttonNextPhoto = document.querySelector('#next_photo');
const photoTrack = document.querySelector('#photo_track');
const photoInner = document.querySelector('#photo_inner');
const trackRect = photoTrack.getClientRects()[0];
const widthPhotoContainer = Math.round(trackRect.width);
const heightPhoto = Math.round(trackRect.height);
const menuPrev = document.querySelector('.photo-menu__left');
const menuNext = document.querySelector('.photo-menu__right');
const placePhotos = document.querySelector('.place-photos');
const MARGIN_PHOTO = 2;

const scrollPoints = {
  margin: 0,
  x: 0,
  points: [],
  currentPoint: 0,
  containerWidth: 0,
  append: function(width, id){
    this.x += this.margin;
    const addPoint = (w)=>{
      console.log(w);
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
  delete: function(){
    const id = this.points[this.currentPoint].id;
    const index = this.points.findIndex(elem=>elem.id === id);
    const deductible = this.points[index].width + 2 * MARGIN_PHOTO;
    this.points = this.points.filter(elem=>elem.id !== id).map((elem, ind)=>{
      if(ind < index){
        return elem;
      }
      elem.x -= deductible;
      return elem;
    });
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

const addImage = (src, id)=>{
  const div = document.createElement('div');
  const img = document.createElement('img');
  img.src = src;
  div.classList.add('photo');
  const imgName = `uktus${id}`;
  const widthPhoto = Math.round(heightPhoto / images[imgName].height * images[imgName].width);
  div.style.width = `${widthPhoto}px`;
  div.id = `place_photo_${id}`;
  div.append(img);
  console.log(`height: ${img.naturalHeight}, width: ${img.naturalWidth}`)
  photoInner.append(div);
  scrollPoints.append(widthPhoto, div.id);
}

const renderPhotos = ()=>{
  for(let i = 1; i < 7; i++){
    const imgName = `uktus${i}`;
    addImage(`../../static/src/${imgName}.jpg`, i);
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

export {scrollPoints};