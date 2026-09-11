/** @typedef {{company:string,role:string,start:string,end:string,description:string}} Experience */
/** @typedef {{school:string,major:string,start:string,end:string}} Education */
/** @typedef {{title:string,target:string,name:string,email:string,phone:string,link:string,summary:string,skills:string,job:string,experience:Experience[],education:Education[]}} Content */
/** @typedef {{id:string,label:string,date:string,content:Content}} Version */
/** @typedef {Content & {id:string,status:string,archived:boolean,updated:string,versions:Version[]}} Resume */
const storageKey='round09-resumes-v1';
/** @returns {Content} */
function blankContent(){return {title:'새 이력서',target:'',name:'',email:'',phone:'',link:'',summary:'',skills:'',job:'',experience:[],education:[]};}
/** @param {Resume} r @returns {Content} */
function contentOf(r){const {title,target,name,email,phone,link,summary,skills,job,experience,education}=r;return structuredClone({title,target,name,email,phone,link,summary,skills,job,experience,education});}
/** @param {string} title @returns {Resume} */
function newResume(title){return {...blankContent(),title,id:crypto.randomUUID(),status:'draft',archived:false,updated:new Date().toISOString(),versions:[]};}
/** @returns {Resume[]} */
function examples(){const base={...newResume('프로덕트 디자이너 · 기본'),target:'프로덕트 디자이너',name:'김하윤',email:'hayoon@example.com',phone:'010-0000-0000',link:'portfolio.example.com',summary:'복잡한 문제를 이해하기 쉬운 경험으로 바꾸는 프로덕트 디자이너입니다. 사용자 리서치부터 출시 후 개선까지 제품의 전 과정을 연결합니다.',skills:'Figma, 사용자 리서치, 프로토타이핑, 디자인 시스템',experience:[{company:'스튜디오 모아',role:'프로덕트 디자이너',start:'2023-03',end:'',description:'가입 단계의 이탈 원인을 인터뷰와 행동 데이터로 분석했습니다.\n입력 흐름을 재설계해 가입 완료율을 18% 개선했습니다.\n공통 컴포넌트 36개를 정리하고 개발팀과 사용 기준을 만들었습니다.'}],education:[{school:'한빛대학교',major:'시각디자인 학사',start:'2016-03',end:'2020-02'}]};return [base,{...structuredClone(base),id:crypto.randomUUID(),title:'커머스 제품팀 지원용',target:'커머스 · 프로덕트 디자이너',status:'ready',summary:'구매 여정의 마찰을 찾아 개선하는 프로덕트 디자이너입니다. 사용자 관찰과 실험 결과를 제품 의사결정에 연결합니다.'},{...structuredClone(base),id:crypto.randomUUID(),title:'플랫폼 디자인팀 지원용',target:'플랫폼 · UX 디자이너',summary:'여러 제품에서 일관되게 사용할 수 있는 디자인 시스템과 접근 가능한 인터랙션을 만듭니다.'}];}
const experienceSchema=z.object({company:z.string(),role:z.string(),start:z.string(),end:z.string(),description:z.string()});
const educationSchema=z.object({school:z.string(),major:z.string(),start:z.string(),end:z.string()});
const contentSchema=z.object({title:z.string(),target:z.string(),name:z.string(),email:z.string(),phone:z.string(),link:z.string(),summary:z.string(),skills:z.string(),job:z.string(),experience:z.array(experienceSchema),education:z.array(educationSchema)});
const versionSchema=z.object({id:z.string(),label:z.string(),date:z.iso.datetime(),content:contentSchema});
const resumeSchema=contentSchema.extend({id:z.string(),status:z.enum(['draft','ready']),archived:z.boolean(),updated:z.iso.datetime(),versions:z.array(versionSchema)});
const backupSchema=z.array(resumeSchema);
let storageMessage='';
/** @returns {Resume[]} */
function loadResumes(){try{const raw=localStorage.getItem(storageKey);if(raw===null)return examples();return backupSchema.parse(JSON.parse(raw));}catch{storageMessage='저장된 내용을 불러오지 못했어요. 원본 저장값은 덮어쓰지 않아요. 백업을 내려받고 브라우저 저장 공간을 확인해 주세요.';return [];}}
let resumes=loadResumes();
function persist(){try{if(storageMessage.startsWith('저장된'))return false;localStorage.setItem(storageKey,JSON.stringify(resumes));storageMessage='';return true;}catch{storageMessage='브라우저에 저장하지 못했어요. 변경 내용은 현재 화면에 남아 있어요. 백업을 내려받아 보관해 주세요.';return false;}}
/** @param {Resume} r @param {string} label */
function snapshot(r,label){r.versions.unshift({id:crypto.randomUUID(),label,date:new Date().toISOString(),content:contentOf(r)});}
/** @param {Content} a @param {Content} b */
function changes(a,b){return [['기본 정보',JSON.stringify([a.title,a.target,a.name,a.email,a.phone,a.link]),JSON.stringify([b.title,b.target,b.name,b.email,b.phone,b.link])],['소개',a.summary,b.summary],['경력',JSON.stringify(a.experience),JSON.stringify(b.experience)],['학력',JSON.stringify(a.education),JSON.stringify(b.education)],['스킬',a.skills,b.skills],['지원 공고',a.job,b.job]].filter(([,x,y])=>x!==y).map(([label])=>label);}
