console.log('references.mjs');
const references = document.querySelectorAll('.reference_item');
const PREF_ID = 'reference_';
const divBefore = document.createElement('div');
divBefore.classList.add('div-before');

const divAfter = document.createElement('div');
divAfter.classList.add('div-after');

const addItemClickListener = (elem)=>{
  elem.addEventListener('click', (evt)=>{
    const index = parseInt(evt.target.id.substring(evt.target.id.length - 1));
    if (index > 0){
      const before = document.querySelector(`#${PREF_ID}${index - 1}`);
      before.append(divBefore);
      before.classList.add('item_before_active');
    }
    const after = document.querySelector(`#${PREF_ID}${index + 1}`);
    after.append(divAfter);
    after.classList.add('item_after_active');
    evt.target.classList.add('reference_item-active');

  })
}

references.forEach(addItemClickListener)