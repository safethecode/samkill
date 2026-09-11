/** @typedef {{id:string,name:string,group:string,amount:string}} Ingredient */
/** @typedef {{id:string,name:string,photo:string,minutes:number,description:string,ingredients:string[],amounts:string[],steps:string[]}} Recipe */
/** @type {Ingredient[]} */
export const ingredients=[
{id:'tomato',name:'토마토',group:'채소',amount:'2개'},
{id:'egg',name:'달걀',group:'달걀·두부',amount:'4개'},
{id:'rice',name:'밥',group:'곡물',amount:'1공기'},
{id:'mushroom',name:'버섯',group:'채소',amount:'1팩'},
{id:'tofu',name:'두부',group:'달걀·두부',amount:'1모'},
{id:'onion',name:'대파',group:'채소',amount:'1대'},
{id:'spinach',name:'시금치',group:'채소',amount:'1묶음'},
{id:'carrot',name:'당근',group:'채소',amount:'1개'}];
/** @type {Recipe[]} */
export const recipes=[
{id:'tomato-rice',name:'토마토 달걀 덮밥',photo:'tomato-egg-rice.jpg',minutes:15,description:'촉촉한 달걀과 토마토를 따뜻한 밥 위에 올려요.',ingredients:['tomato','egg','rice','onion'],amounts:['1개','2개','1공기','¼대'],steps:['토마토는 한입 크기로, 대파는 잘게 썰어요. 달걀 2개에 소금 한 꼬집을 넣고 풀어요.','팬에 식용유를 두르고 달걀을 저어가며 익혀요. 달걀이 부드럽게 뭉치면 접시에 잠시 덜어둬요.','같은 팬에 대파와 토마토를 볶아요. 토마토에서 물이 나오면 간장 1작은술을 넣어요.','달걀을 다시 넣어 속까지 익힌 뒤 따뜻한 밥 위에 올려요. 취향에 따라 후추를 더해요.']},
{id:'mushroom-rice',name:'버섯 달걀 볶음밥',photo:'mushroom-egg-rice.jpg',minutes:20,description:'버섯을 먼저 노릇하게 볶아 향을 살린 한 그릇이에요.',ingredients:['mushroom','egg','rice','onion'],amounts:['½팩','1개','1공기','¼대'],steps:['버섯은 얇게, 대파는 잘게 썰어요. 달걀은 볼에 풀어둬요.','팬에 식용유를 두르고 대파와 버섯을 볶아요. 버섯의 수분이 줄 때까지 익혀요.','재료를 한쪽으로 밀고 달걀을 부어 저어요. 달걀이 익으면 밥을 넣고 고루 풀어요.','간장 1작은술과 후추로 간을 맞춰요. 밥이 전체적으로 뜨겁게 익으면 그릇에 담아요.']},
{id:'tofu-rice',name:'두부 버섯 덮밥',photo:'tofu-mushroom.jpg',minutes:20,description:'두부와 버섯에 매콤한 양념을 더해 든든하게 먹어요.',ingredients:['tofu','mushroom','rice','spinach'],amounts:['½모','½팩','1공기','한 줌'],steps:['두부는 한입 크기로 자르고 버섯과 시금치는 씻어 준비해요.','팬에 식용유를 두르고 버섯을 볶아요. 고추장 1작은술과 간장 1작은술, 물 4큰술을 넣어요.','두부와 시금치를 넣고 두부가 속까지 뜨거워질 때까지 끓여요. 간이 약하면 간장을 조금 더해요.','따뜻한 밥 위에 두부와 양념을 올려요. 두부가 부서지지 않도록 살살 옮겨 담아요.']}];
/** @param {Recipe} recipe @param {Set<string>} selected */
export function missing(recipe,selected){return recipe.ingredients.filter(id=>!selected.has(id));}
/** @param {string} id */
export function ingredientName(id){return ingredients.find(item=>item.id===id)?.name??id;}
