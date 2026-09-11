import {z} from 'zod';
import {icons} from './icons.js';

const responseSchema=z.object({side:z.enum(['groom','bride']),name:z.string().trim().min(1).max(30),attendance:z.enum(['yes','no']),count:z.number().int().min(0).max(10),meal:z.enum(['yes','no','unsure']),savedAt:z.string().datetime()}).refine(v=>v.attendance==='no'?v.count===0:v.count>=1);
const noteSchema=z.object({id:z.string().min(1),name:z.string().trim().min(1).max(30),message:z.string().trim().min(1).max(300),date:z.string().datetime()});
const storageSchema=z.object({response:responseSchema.nullable(),notes:z.array(noteSchema).max(50)});
/** @typedef {z.infer<typeof storageSchema>} Saved */
/** @type {Saved} */
let saved={response:null,notes:[]};
const storageKey='round10-wedding-v1';
let damagedStorage=false;
/** @type {HTMLElement|null} */
let returnFocus=null;
let photoIndex=0;
let editingNote='';
let pendingDelete='';
let toastTimer=0;
const photos=[{src:'assets/wedding-portrait.png',alt:'정원에서 함께 웃는 두 사람'},{src:'assets/wedding-close.png',alt:'가까이에서 서로를 바라보는 두 사람'}];

/** @param {string} id */
function element(id){const value=document.getElementById(id);if(!(value instanceof HTMLElement))throw new Error('Missing element: '+id);return value;}
/** @param {string} id */
function dialog(id){const value=element(id);if(!(value instanceof HTMLDialogElement))throw new Error('Missing dialog: '+id);return value;}
/** @param {string} id */
function form(id){const value=element(id);if(!(value instanceof HTMLFormElement))throw new Error('Missing form: '+id);return value;}
/** @param {string} id */
function input(id){const value=element(id);if(!(value instanceof HTMLInputElement))throw new Error('Missing input: '+id);return value;}
/** @param {string} message */
function notify(message){clearTimeout(toastTimer);const box=element('toast');box.textContent=message;box.hidden=false;toastTimer=window.setTimeout(()=>{box.hidden=true;},5000);}
/** @param {string} text */
function escape(text){return text.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]??char));}

function decorate(){for(const el of document.querySelectorAll('[data-icon]')){if(!(el instanceof HTMLElement))continue;const name=z.enum(['calendar-days','map-pin','phone','message-circle','copy','share-2','chevron-down','chevron-left','chevron-right','x','check','arrow-up','music-2','volume-x','plus','minus']).safeParse(el.dataset.icon);if(name.success)el.innerHTML=icons[name.data];}}
function readSaved(){try{const raw=localStorage.getItem(storageKey);if(raw){const parsed=storageSchema.safeParse(JSON.parse(raw));if(!parsed.success)throw new Error('Invalid stored data');saved=parsed.data;}}catch{damagedStorage=true;notify('저장한 내용을 읽지 못했어요. 기존 데이터는 유지했어요.');element('storage-warning').hidden=false;}}
/** @param {Saved} next */
async function persist(next){
 if(damagedStorage)return false;
 const baseline=JSON.stringify(saved);
 const write=()=>{try{const raw=localStorage.getItem(storageKey);const latest=raw?storageSchema.parse(JSON.parse(raw)):{response:null,notes:[]};if(JSON.stringify(latest)!==baseline){saved=latest;renderNotes();renderResponse();return false;}const valid=storageSchema.parse(next);localStorage.setItem(storageKey,JSON.stringify(valid));saved=valid;return true;}catch{return false;}};
 try{if(navigator.locks)return await navigator.locks.request(storageKey,write);return write();}catch{return false;}
}

/** @param {HTMLFormElement} target @param {string} name @param {string} value */
function setValue(target,name,value){const field=target.elements.namedItem(name);if(field instanceof RadioNodeList||field instanceof HTMLInputElement||field instanceof HTMLTextAreaElement)field.value=value;}
/** @param {string} id */
function openDialog(id){returnFocus=document.activeElement instanceof HTMLElement?document.activeElement:null;if(id==='response')prepareResponse();if(id==='guest')prepareGuest();dialog(id).showModal();}
function renderResponse(){const response=saved.response;const box=element('response-summary');box.hidden=!response;element('remove-response').hidden=!response;element('respond-button').textContent=response?'저장한 응답 수정하기':'참석 여부 작성하기';if(response)box.textContent=response.attendance==='yes'?`${response.name} 님 · ${response.count}명 참석 · ${response.meal==='yes'?'식사 예정':response.meal==='no'?'식사 안 함':'식사 미정'}`:`${response.name} 님 · 참석이 어려워요`;}
function prepareResponse(){const target=form('response-form');target.reset();element('response-error').textContent='';const response=saved.response;if(response){setValue(target,'side',response.side);setValue(target,'name',response.name);setValue(target,'attendance',response.attendance);setValue(target,'count',String(Math.max(1,response.count)));setValue(target,'meal',response.meal);}syncAttendance();}
function syncAttendance(){const target=form('response-form');const attending=new FormData(target).get('attendance')==='yes';element('attending-fields').hidden=!attending;for(const field of element('attending-fields').querySelectorAll('input')){field.disabled=!attending;field.required=attending;}syncCount();}
function syncCount(){const count=input('count').valueAsNumber;const decrease=element('decrease');const increase=element('increase');if(decrease instanceof HTMLButtonElement)decrease.disabled=count<=1;if(increase instanceof HTMLButtonElement)increase.disabled=count>=10;}
form('response-form').addEventListener('change',syncAttendance);
input('count').addEventListener('input',syncCount);
element('decrease').addEventListener('click',()=>{input('count').value=String(Math.max(1,(input('count').valueAsNumber||1)-1));syncCount();});
element('increase').addEventListener('click',()=>{input('count').value=String(Math.min(10,(input('count').valueAsNumber||1)+1));syncCount();});
form('response-form').addEventListener('submit',async event=>{event.preventDefault();const data=new FormData(form('response-form'));const attending=data.get('attendance')==='yes';const parsed=responseSchema.safeParse({side:data.get('side'),name:data.get('name'),attendance:data.get('attendance'),count:attending?Number(data.get('count')):0,meal:attending?data.get('meal'):'unsure',savedAt:new Date().toISOString()});if(!parsed.success){element('response-error').textContent='성함과 참석 정보를 확인해 주세요.';return;}if(!await persist({...saved,response:parsed.data})){element('response-error').textContent='다른 창의 변경 또는 저장 제한으로 저장하지 못했어요. 입력은 유지했으니 확인 후 다시 저장해 주세요.';return;}renderResponse();dialog('response').close();notify('이 브라우저에 응답을 저장했어요. 실제 전송은 하지 않았어요.');});
element('remove-response').addEventListener('click',async()=>{if(!await persist({...saved,response:null})){element('response-error').textContent='다른 창의 변경 또는 저장 제한으로 삭제하지 못했어요. 최신 내용을 확인 후 다시 시도해 주세요.';return;}renderResponse();dialog('response').close();notify('저장한 응답을 삭제했어요.');});

function renderNotes(){const target=element('guest-notes');if(!saved.notes.length){target.innerHTML='<p class="empty-note">첫 축하의 마음을 남겨 주세요.</p>';return;}target.innerHTML=saved.notes.map(note=>`<article class="guest-note"><header><strong>${escape(note.name)}</strong><time datetime="${escape(note.date)}">${new Date(note.date).toLocaleDateString('ko-KR',{month:'long',day:'numeric'})}</time></header><p>${escape(note.message)}</p><footer><button class="button" type="button" data-edit-note="${escape(note.id)}" aria-label="${escape(note.name)}님의 축하글 수정">수정</button><button class="button" type="button" data-delete-note="${escape(note.id)}" aria-label="${escape(note.name)}님의 축하글 삭제">삭제</button></footer></article>`).join('');}
function prepareGuest(){const target=form('guest-form');target.reset();element('guest-error').textContent='';const note=saved.notes.find(n=>n.id===editingNote);element('guest-title').textContent=note?'축하글 수정하기':'축하글 남기기';if(note){setValue(target,'name',note.name);setValue(target,'message',note.message);}}
form('guest-form').addEventListener('submit',async event=>{event.preventDefault();const data=new FormData(form('guest-form'));const previous=saved.notes.find(n=>n.id===editingNote);const parsed=noteSchema.safeParse({id:previous?.id??crypto.randomUUID(),name:data.get('name'),message:data.get('message'),date:previous?.date??new Date().toISOString()});if(!parsed.success){element('guest-error').textContent='이름과 축하 메시지를 입력해 주세요.';return;}const notes=previous?saved.notes.map(n=>n.id===previous.id?parsed.data:n):[...saved.notes,parsed.data];if(notes.length>50){element('guest-error').textContent='예시 방명록은 50개까지 저장할 수 있어요.';return;}if(!await persist({...saved,notes})){element('guest-error').textContent='다른 창의 변경 또는 저장 제한으로 저장하지 못했어요. 입력한 글은 유지했으니 확인 후 다시 저장해 주세요.';return;}renderNotes();dialog('guest').close();element('write-guest').focus();notify('축하글을 이 브라우저에 저장했어요.');});
element('guest-notes').addEventListener('click',event=>{if(!(event.target instanceof Element))return;const edit=event.target.closest('[data-edit-note]');const remove=event.target.closest('[data-delete-note]');if(edit instanceof HTMLElement){editingNote=edit.dataset.editNote??'';openDialog('guest');}if(remove instanceof HTMLElement){pendingDelete=remove.dataset.deleteNote??'';openDialog('delete-note');}});
element('confirm-delete').addEventListener('click',async()=>{if(!await persist({...saved,notes:saved.notes.filter(n=>n.id!==pendingDelete)})){element('delete-error').textContent='다른 창의 변경 또는 저장 제한으로 삭제하지 못했어요. 최신 내용을 확인 후 다시 시도해 주세요.';return;}renderNotes();dialog('delete-note').close();element('write-guest').focus();notify('축하글을 삭제했어요.');});

function renderPhoto(){const photo=photos[photoIndex];const large=element('large-photo');if(large instanceof HTMLImageElement){large.src=photo.src;large.alt=photo.alt;}element('photo-count').textContent=`${photoIndex+1} / ${photos.length}`;}
/** @param {number} direction */
function changePhoto(direction){photoIndex=(photoIndex+direction+photos.length)%photos.length;renderPhoto();}
element('previous-photo').addEventListener('click',()=>changePhoto(-1));element('next-photo').addEventListener('click',()=>changePhoto(1));
dialog('photos').addEventListener('keydown',event=>{if(event.key==='ArrowRight'){event.preventDefault();changePhoto(1);}if(event.key==='ArrowLeft'){event.preventDefault();changePhoto(-1);}});
let touchStart=0;dialog('photos').addEventListener('touchstart',event=>{touchStart=event.changedTouches[0].clientX;},{passive:true});dialog('photos').addEventListener('touchend',event=>{const distance=event.changedTouches[0].clientX-touchStart;if(Math.abs(distance)>50)changePhoto(distance<0?1:-1);},{passive:true});

/** @param {string} value @param {string} message */
async function copy(value,message){try{await navigator.clipboard.writeText(value);notify(message);}catch{const field=element('copy-value');if(field instanceof HTMLTextAreaElement)field.value=value;openDialog('copy-fallback');if(field instanceof HTMLTextAreaElement){field.focus();field.select();}}}
function shareUrl(){return location.href.split('#')[0];}
element('copy-address').addEventListener('click',()=>{void copy('서울 성동구 뚝섬로 273','주소를 복사했어요.');});
element('copy-link').addEventListener('click',()=>{void copy(shareUrl(),'현재 미리보기 링크를 복사했어요.');});
element('share').addEventListener('click',async()=>{if(navigator.share&&location.protocol!=='file:'){try{await navigator.share({title:'민준과 서연의 결혼식',text:'2027년 5월 22일 토요일 오후 2시 · 예시 청첩장',url:shareUrl()});}catch(error){if(error instanceof DOMException&&error.name==='AbortError')return;await copy(shareUrl(),'현재 미리보기 링크를 복사했어요.');}}else await copy(shareUrl(),'현재 미리보기 링크를 복사했어요.');});
element('save-date').addEventListener('click',()=>{const content=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Round10//Wedding sample//KO','BEGIN:VEVENT','UID:round10-wedding-20270522@example.invalid','DTSTAMP:20260911T000000Z','DTSTART:20270522T050000Z','DTEND:20270522T070000Z','SUMMARY:민준과 서연의 결혼식 (예시)','LOCATION:서울숲 아틀리에 가든홀 (가상 예식장)','DESCRIPTION:실제 예식이 아닌 Round10 예시 일정입니다.','END:VEVENT','END:VCALENDAR',''].join('\r\n');const url=URL.createObjectURL(new Blob([content],{type:'text/calendar;charset=utf-8'}));const link=document.createElement('a');link.href=url;link.download='민준-서연-예식일정.ics';link.click();window.setTimeout(()=>URL.revokeObjectURL(url),1000);notify('일정 파일을 내려받았어요. 캘린더에서 열어 주세요.');});

function renderCalendar(){const start=new Date(Date.UTC(2027,4,1)).getUTCDay();let html='';for(let row=0;row<6;row++){html+='<tr>';for(let col=0;col<7;col++){const day=row*7+col-start+1;html+=day>=1&&day<=31?`<td><span${day===22?' class="wedding-day" aria-label="22일 토요일, 결혼식"':''}>${day}</span></td>`:'<td></td>';}html+='</tr>';}element('calendar-days').innerHTML=html;}
function renderCountdown(){const today=new Date().toLocaleDateString('sv-SE',{timeZone:'Asia/Seoul'});const days=Math.round((Date.parse('2027-05-22T00:00:00+09:00')-Date.parse(today+'T00:00:00+09:00'))/86400000);element('countdown').innerHTML=days>0?`민준과 서연의 결혼식까지 <strong>${days}일</strong> 남았어요.`:days===0?'오늘, 저희 결혼합니다.':'함께해 주신 모든 분께 감사합니다.';}

for(const modal of document.querySelectorAll('dialog')){modal.addEventListener('close',()=>{returnFocus?.focus({preventScroll:true});});modal.addEventListener('click',event=>{if(event.target!==modal)return;const rect=modal.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)modal.close();});}
document.addEventListener('click',event=>{if(!(event.target instanceof Element))return;const open=event.target.closest('[data-open]');if(open instanceof HTMLElement){if(open.dataset.open==='guest')editingNote='';openDialog(open.dataset.open??'');}const close=event.target.closest('[data-close]');if(close)close.closest('dialog')?.close();const photo=event.target.closest('[data-photo]');if(photo instanceof HTMLElement){photoIndex=z.coerce.number().int().min(0).max(1).parse(photo.dataset.photo);renderPhoto();openDialog('photos');}const account=event.target.closest('[data-copy-account]');if(account instanceof HTMLElement)void copy(account.dataset.copyAccount??'','송금용이 아닌 예시 계좌 정보를 복사했어요.');});
new IntersectionObserver(entries=>{for(const entry of entries)element('quick-nav').hidden=entry.isIntersecting;},{threshold:0}).observe(element('top'));
decorate();readSaved();renderNotes();renderResponse();renderCalendar();renderCountdown();window.setInterval(renderCountdown,60000);

new ResizeObserver(entries=>{for(const entry of entries){const height=entry.target.getBoundingClientRect().height;if(height>0)document.documentElement.style.setProperty('--dock-height',height+'px');}}).observe(element('quick-nav'));
