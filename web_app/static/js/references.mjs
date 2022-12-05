console.log('references.mjs');
import {getReference} from './fetcher.mjs';
import {forReferences} from './settings.mjs';

const referenceContainer = document.querySelector('.references-content');
const references = document.querySelectorAll('.reference_item');
const firstReference = document.querySelector('.reference_item');
const PREF_ID = 'reference_';
const divBefore = document.createElement('div');
divBefore.classList.add('div-before');

const divAfter = document.createElement('div');
divAfter.classList.add('div-after');

const resetActive = (element)=>{
  const active = document.querySelector('.reference_item-active');
  console.log(active);
  if (active.id === element.id){
    return;
  }
  const index = parseInt(active.id.substring(element.id.length - 1));
  if (index > 0){
      const before = document.querySelector(`#${PREF_ID}${index - 1}`);
      before.removeChild(before.querySelector('.div-before'));
      before.classList.remove('item_before_active');
    }
    const after = document.querySelector(`#${PREF_ID}${index + 1}`);
    after.removeChild(after.querySelector('.div-after'));
    after.classList.remove('item_after_active');
  active.classList.remove('reference_item-active');
}

const setActive = (element)=>{
  const index = parseInt(element.id.substring(element.id.length - 1));
  if (index > 0){
      const before = document.querySelector(`#${PREF_ID}${index - 1}`);
      before.append(divBefore);
      before.classList.add('item_before_active');
    }
    const after = document.querySelector(`#${PREF_ID}${index + 1}`);
    after.append(divAfter);
    after.classList.add('item_after_active');
    element.classList.add('reference_item-active');
}

function Table(name, fields){
  this.name = name;
  this.fields = fields;
  this._getFr = (name, elem)=>{
    if (forReferences[name][elem].width){
      return `${forReferences[name][elem].width.toString()}px`;
    }
    return `${this.fr}px`;
  }
  const clientWidth = referenceContainer.clientWidth;
  this.frsCount = 0;
  this.width = 0;
  for (let key in forReferences[name]){
    if (forReferences[name][key].width){
      this.width += forReferences[name][key].width;
    }
    else {
      this.frsCount ++;
    }
  }
  console.log(`width: ${this.width}`);
  console.log(`frsCount: ${this.frsCount}`);
  const colCount = fields.length;
  if (this.frsCount > 0 && colCount < 5){
    const widthTable = clientWidth / (colCount + 1) * colCount;
    this.fr = Math.round((widthTable - this.width) / this.frsCount);
  }
  this.templateColumns = fields.map(elem=>this._getFr(name, elem)).join(' ');
  console.log(this.templateColumns);
}

// const table = {
//   name: '',
//   fields: [],
//   templateColumns: '',
//   width: 0,
//   frsCount: 0,
//   fr: 0,
//   _getFr: (name, elem)=>{
//     if (forReferences[name][elem].width){
//       return `${forReferences[name][elem].width.toString()}px`;
//     }
//     return `${this.fr}px`;
//   },
//   init: function(name, fields){
//     this.name = name;
//     this.fields = fields;
//     const clientWidth = referenceContainer.clientWidth;
//     for (let key in forReferences[name]){
//       if (forReferences[name][key].width){
//         this.width += forReferences[name][key].width;
//       }
//       else {
//         this.frsCount ++;
//       }
//     }
//     console.log(`width: ${this.width}`);
//     console.log(`frsCount: ${this.frsCount}`);
//     const colCount = fields.length;
//     if (this.frsCount > 0 && colCount < 5){
//       const widthTable = clientWidth / (colCount + 1) * colCount;
//       this.fr = Math.round((widthTable - this.width) / this.frsCount);
//     }
//     this.templateColumns = fields.map(elem=>this._getFr(name, elem)).join(' ');
//     console.log(this.templateColumns);
//   }
// }

const createTable = (rowsCount)=>{
  const oldTable = referenceContainer.querySelector('.table_reference');
  const table = document.createElement('div');
  table.classList.add('table_reference');
  table.style['grid-template-rows'] = `repeat(${rowsCount}, 1fr)`;
  return {table: table, oldTable: oldTable};
}

const createHead = (header)=>{
  const head = document.createElement('div');
  head.classList.add('head_reference');
  const h2 = document.createElement('h2');
  h2.textContent = header;
  head.append(h2);
  return head;
}

const createRow = (table)=>{
  const row = document.createElement('div');
  row.classList.add('row_reference');
  row.style['grid-template-columns'] = table.templateColumns;
  return row;
}

const fillCaption = (table, captions)=>{
  const row = createRow(table);
  captions.forEach((caption, ind)=>{
    const cell = document.createElement('div');
    cell.classList.add('cell_reference', 'column_head');
    const h2 = document.createElement('h2');
    if (forReferences[table.name][table.fields[ind]].captionFontSize){
      h2.style.fontSize = forReferences[table.name][table.fields[ind]].captionFontSize.toString() + 'px';
    }
    h2.textContent = caption;
    cell.append(h2);
    row.append(cell);
  })
  return row;
}

const fillRow = (table, elem)=>{
  const row = createRow(table);
  elem.forEach(val=>{
    const cell = document.createElement('div');
    cell.classList.add('cell_reference');
    const p = document.createElement('p');
    p.textContent = val;
    cell.append(p);
    row.append(cell);
  })
  return row;
}

const renderReference = (json)=>{
  const tables = createTable(json.rows.length + 2);
  const table = new Table(json.name, json.fields);
  tables.table.append(createHead(json.head));
  tables.table.append(fillCaption(table, json.captions));
  json.rows.forEach(elem=>tables.table.append(fillRow(table, elem)));
  referenceContainer.replaceChild(tables.table, tables.oldTable);
  console.log(`container width = ${referenceContainer.clientWidth}`);
}

const onError = (msg)=>{
  console.log(msg);
}

const addItemClickListener = (elem)=>{
  elem.addEventListener('click', (evt)=>{
    resetActive(evt.target);
    setActive(evt.target);
    const index = evt.target.id.substring(evt.target.id.length - 1);
    const baseUrl = document.location.href;
    const url = new URL(index, baseUrl);
    console.log(url);
    getReference(url, renderReference, onError);
  })
}

references.forEach(addItemClickListener);
setActive(firstReference);