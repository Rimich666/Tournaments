console.log('Это tournaments.js');
const ROW_HEIGHT = 36;
const GAP = 2;

const addTourButton = document.querySelector('#add_tour_button');
const addTourModal = document.querySelector('.modal-container');
const addTourSubmit = document.querySelector('#add_tour_submit');
const placeSelectButton = document.querySelector('#tour_place_select');
const tourAddForm = document.querySelector('#tour_add_form');
const placeSelectInput= document.querySelector('#tour_place');
const placesList = document.querySelector('#places_list');
const container = document.querySelector('.modal-container');

addTourButton.addEventListener('click', ()=>
  addTourModal.classList.remove('modal-container-close'));

const loadData = ()=>
  fetch(DATA_URL)
    .then((response)=>{
      if (response.ok) {
        return response.json();
      }
      throw `${response.status}, ${response.statusText}`;
    });

const getDiv = (text, tag)=>{
  const p = document.createElement('p')
  p.textContent = text;
  p.style.margin = 'auto 5%';
  const element = document.createElement(tag);
  element.classList.add('row-select_places');
  element.style.height = ROW_HEIGHT.toString();
  element.append(p);
  return element;
}

const createRow = (rec)=>{
  const element = getDiv(rec.place, 'div');
  element.id = `place_${rec.id}`;
  element.dataset.place = rec.place;
  return element;
};

const rowEventHandler = (row)=>{
  row.addEventListener('click', (evt)=>{
    const id = evt.currentTarget.id;
    placeSelectInput.dataset.id = id.slice(id.indexOf('_') + 1);
    placeSelectInput.value = evt.currentTarget.dataset.place;
    clearList();
    evt.stopPropagation();
  })
};

const clearList = ()=>{
  placesList.classList.add('popup-close');
  while (placesList.firstChild){
    placesList.removeChild(placesList.firstChild);
  }
  container.removeEventListener('click', clearList);
};

const getHeightPopup = (sizeList)=>{
  const supremum = Math.max(
    container.getClientRects()[0].bottom, tourAddForm.getClientRects()[0].bottom
    ) - placeSelectInput.getClientRects()[0].bottom;
  const height = Math.min(supremum, ((ROW_HEIGHT + GAP) * (sizeList) + GAP));
  return `${height}px`;
};

const createNewPlaceRef = ()=>{
  return getDiv('Добавить новое место', 'a');
}

const createErrorMessage = (msg)=>getDiv(msg);

const createList = (res)=>{
  const sizeList = res.length + 1;
  placesList.style.height = getHeightPopup(sizeList);
  placesList.classList.remove('popup-close');
  placesList.style.cssText += `
    grid-template-rows: repeat(${sizeList}, ${ROW_HEIGHT}px);
    padding-top: ${GAP}px;
    gap: ${GAP}px;
    `;
  res.forEach((rec)=>{
    let row = createRow(rec);
    rowEventHandler(row);
    placesList.append(row);
  })
  placesList.append(createNewPlaceRef());
  container.addEventListener('click', clearList);
};

const showError = (msg)=>{
  placesList.append(createErrorMessage(msg));
}

placeSelectButton.addEventListener('click', (evt)=>{
  evt.preventDefault();
  //console.log(evt.currentTarget);
  if (placesList.classList.contains('popup-close')){
    loadData()
      .then(createList)
      .catch(showError)
  }
  else{
    clearList();
  }
  evt.stopPropagation();
})

addTourSubmit.addEventListener('click', (evt)=>{
  evt.preventDefault();
})

//console.log(DATA_URL);
