import {scrollPoints} from './place.mjs'
console.log('edit place');
const buttonAddPhoto = document.querySelector('#add_photo');
const buttonRemovePhoto = document.querySelector('#remove_photo');
const menuPhoto = document.querySelector('#menu_photo');
const photoInner = document.querySelector('#photo_inner');

console.log(scrollPoints);

menuPhoto.classList.remove('photo-menu-hide');
buttonAddPhoto.addEventListener('click', ()=>{
  console.log('Add');
});
buttonRemovePhoto.addEventListener('click', ()=>{
  const deletePhoto = document.querySelector(`#${scrollPoints.points[scrollPoints.currentPoint].id}`);
  deletePhoto.remove();
  scrollPoints.delete();
  console.log(scrollPoints.points[scrollPoints.currentPoint].id);
});
