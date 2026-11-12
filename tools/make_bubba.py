"""Turn the Zulu 1 tutor page into Master Bubba's Year 7-8 (KS3) edition."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    assert old in s, "not found: " + old[:80]
    s = s.replace(old, new, count)


# ---- name, storage, header ----
rep('/* Shakai is pronounced "Shaaa-Ki" and Stoute like "stout", so the voice is given those spellings */\n'
    'const sayable=t=>String(t).replace(/\\bShakai\\b/g,"Shah-kye").replace(/\\bStoute\\b/g,"Stowt");',
    '/* Names the voice should say differently go here */\nconst sayable=t=>String(t);')
s = s.replace("Master Shakai Stoute", "Master Bubba").replace("Stoute", "Bubba")
rep('<small>Personal tutor of Master Bubba</small>',
    '<small>Personal tutor of Master Bubba · Year 7 &amp; 8</small>')
rep('<title>Zulu 1 Ham Dog Tutor</title>', "<title>Bubba's Zulu 1 Tutor</title>")
rep('<meta name="apple-mobile-web-app-title" content="Zulu 1 Tutor">', '<meta name="apple-mobile-web-app-title" content="Zulu 1 Bubba">')
rep('<link rel="apple-touch-icon" href="apple-touch-icon.png">', '<link rel="apple-touch-icon" href="../apple-touch-icon.png">')
rep('const KEY="zulu1-tutor-v1";', 'const KEY="zulu1-bubba-ks3-v1";')
rep('treat:"A trip to the beach with Granny Beryl"', 'treat:"A special treat from Granny Beryl"')

# ---- KS3 word packs with meanings ----
PACKS = r'''
/* ---------- Key Stage 3 (Year 7 & 8) word packs, with meanings ---------- */
const PACKS={
 tricky:{name:"Tricky Spellings",ic:"✍️",c:"var(--coral)",words:{
  necessary:"needed; it must be done or had",separate:"to keep apart; not joined together",definitely:"without any doubt",
  accommodate:"to provide room or a place to stay",embarrass:"to make someone feel awkward or ashamed",rhythm:"a regular, repeated pattern of sounds or movements",
  conscience:"your inner sense of what is right and wrong",government:"the group of people who run a country",environment:"the surroundings in which people, animals and plants live",
  occasionally:"sometimes, but not often",recommend:"to suggest that something is good or worth doing",achieve:"to succeed in doing something after working hard",
  believe:"to accept that something is true",argument:"a reason given for or against an idea; a disagreement",beginning:"the start of something",
  disappear:"to go out of sight",immediately:"at once; straight away",sincerely:"honestly and truly; used to end a formal letter",
  restaurant:"a place where you pay to sit and eat a meal",parallel:"side by side and always the same distance apart"}},
 english:{name:"English",ic:"📚",c:"var(--grape)",words:{
  metaphor:"describing something as if it were something else, like 'the classroom was a zoo'",simile:"comparing two things using 'like' or 'as'",
  alliteration:"words close together that start with the same sound",onomatopoeia:"a word that sounds like the noise it describes, like 'buzz'",
  personification:"giving human qualities to something that is not human",adjective:"a word that describes a noun",adverb:"a word that describes a verb, often ending in 'ly'",
  conjunction:"a joining word, like 'and', 'but' or 'because'",paragraph:"a group of sentences about one idea",apostrophe:"a punctuation mark that shows missing letters or belonging",
  persuasive:"trying to make someone agree or do something",narrative:"a story, or the telling of a story",character:"a person in a story",
  chronological:"in the order that events happened",exclamation:"a sudden cry, or a sentence that shows strong feeling"}},
 maths:{name:"Maths",ic:"📐",c:"var(--sky)",words:{
  perpendicular:"meeting another line at a right angle",parallelogram:"a four-sided shape with two pairs of parallel sides",
  isosceles:"a triangle with two equal sides",equilateral:"a triangle with all three sides equal",circumference:"the distance all the way round a circle",
  diameter:"a straight line across a circle through its centre",radius:"the distance from the centre of a circle to its edge",
  perimeter:"the total distance around the outside of a shape",denominator:"the bottom number of a fraction",numerator:"the top number of a fraction",
  equation:"a number sentence where both sides are equal",probability:"how likely something is to happen",symmetry:"when one half is a mirror image of the other",
  quadrilateral:"any flat shape with four straight sides",integer:"a whole number, positive, negative or zero",average:"a typical middle value of a set of numbers"}},
 science:{name:"Science",ic:"🔬",c:"var(--leaf)",words:{
  photosynthesis:"how plants use sunlight, water and carbon dioxide to make food",chlorophyll:"the green substance in plants that absorbs light",
  respiration:"how living cells release energy from food",organism:"a living thing",molecule:"two or more atoms joined together",
  particle:"a very tiny piece of matter",evaporation:"when a liquid turns into a gas",condensation:"when a gas cools and turns into a liquid",
  friction:"a force that slows things down when surfaces rub together",gravity:"the force that pulls objects towards each other, and towards the Earth",
  nucleus:"the control centre of a cell",cytoplasm:"the jelly-like substance inside a cell",membrane:"a thin layer that controls what goes in and out of a cell",
  electricity:"energy carried by moving charged particles",experiment:"a test to find something out",hypothesis:"a prediction that can be tested",
  thermometer:"an instrument that measures temperature"}},
 history:{name:"History",ic:"🏰",c:"var(--tang)",words:{
  monarchy:"a country ruled by a king or queen",parliament:"the group of people who make the laws of a country",medieval:"from the Middle Ages, about 500 to 1500",
  conquest:"taking control of a place by force",rebellion:"a fight against the people in charge",civilisation:"a large, organised society with its own culture",
  empire:"a group of countries ruled by one ruler or country",revolution:"a big, sudden change, often overthrowing a government",
  democracy:"a system where people vote to choose their leaders",feudal:"the medieval system where land was given in return for loyalty and work",
  plague:"a deadly disease that spreads quickly",slavery:"when people are owned by others and forced to work",colony:"a land ruled by another country"}},
 geography:{name:"Geography",ic:"🌍",c:"var(--sea)",words:{
  continent:"one of the seven large areas of land on Earth",latitude:"how far north or south a place is from the Equator",
  longitude:"how far east or west a place is",erosion:"the wearing away of land by water, wind or ice",population:"the number of people living in a place",
  settlement:"a place where people live, from a farm to a city",climate:"the usual weather of a place over many years",tectonic:"to do with the plates that make up the Earth's crust",
  volcano:"an opening in the Earth's crust where lava escapes",earthquake:"a sudden shaking of the ground",tributary:"a small river that flows into a bigger one",
  meander:"a bend in a river",sustainable:"able to carry on without harming the environment",urban:"to do with towns and cities",rural:"to do with the countryside"}}
};
const PACKMEAN={};Object.values(PACKS).forEach(p=>Object.assign(PACKMEAN,p.words));
function meaningOf(w,k=WK){const m=(S.weeks[k]&&S.weeks[k].meanings)||{};return m[w]||PACKMEAN[w]||""}
let openPack=null,picked=new Set();
'''
rep('const EXAMPLES = ["because","friend","beautiful","school","night"];',
    'const EXAMPLES = ["necessary","separate","definitely","environment","photosynthesis","perpendicular"];')
rep('/* ---------- storage ---------- */', PACKS + '\n/* ---------- storage ---------- */')
rep('function week(k=WK){if(!S.weeks[k])S.weeks[k]={words:[],progress:{}};return S.weeks[k]}',
    'function week(k=WK){if(!S.weeks[k])S.weeks[k]={words:[],progress:{},meanings:{}};if(!S.weeks[k].meanings)S.weeks[k].meanings={};return S.weeks[k]}')

# ---- KS3 memory tricks, word building ----
MORPH = r'''
const MNEMO={
 necessary:`ne<b class="l">C</b>e<b class="l">SS</b>ary: one <b class="l">C</b>ollar and two <b class="l">S</b>leeves.`,
 separate:`There is <b class="l">a rat</b> in sep<b class="l">arat</b>e.`,
 definitely:`Find the word <b class="l">finite</b> hiding inside de<b class="l">finite</b>ly. No "a" anywhere!`,
 accommodate:`It is big enough to accommodate <b class="l">two Cs</b> and <b class="l">two Ms</b>: two cots and two mattresses.`,
 embarrass:`You go <b class="l">R</b>eally <b class="l">R</b>ed and feel <b class="l">S</b>o <b class="l">S</b>hy: double r, double s.`,
 rhythm:`<b class="l">R</b>hythm <b class="l">H</b>elps <b class="l">Y</b>our <b class="l">T</b>wo <b class="l">H</b>ips <b class="l">M</b>ove.`,
 conscience:`It is <b class="l">con</b> + <b class="l">science</b>: con-science.`,
 government:`The people who <b class="l">govern</b> + <b class="l">ment</b>. Say the hidden n!`,
 environment:`There is <b class="l">iron</b> in env<b class="l">iron</b>ment.`,
 occasionally:`Two <b class="l">c</b>s, one <b class="l">s</b>, two <b class="l">l</b>s: o-CC-a-S-iona-LL-y.`,
 recommend:`One <b class="l">c</b>, two <b class="l">m</b>s: re + commend.`,
 achieve:`<b class="l">i</b> before <b class="l">e</b>: ach-<b class="l">ie</b>-ve.`,
 believe:`Never be<b class="l">lie</b>ve a <b class="l">lie</b>.`,
 argument:`<b class="l">Argue</b> loses its <b class="l">e</b> before <b class="l">ment</b>: argument.`,
 beginning:`Begin + <b class="l">n</b> + ing: double the n.`,
 disappear:`<b class="l">dis</b> + <b class="l">appear</b>: one s, two ps.`,
 immediately:`<b class="l">im</b> + <b class="l">mediate</b> + <b class="l">ly</b>: two ms.`,
 sincerely:`<b class="l">sincere</b> keeps its e, then add <b class="l">ly</b>.`,
 restaurant:`<b class="l">rest</b> + <b class="l">au</b> + <b class="l">rant</b>: you rest, then rant about the food!`,
 parallel:`The two <b class="l">l</b>s in the middle stand side by side, parallel: para<b class="l">ll</b>el.`,
 parallelogram:`<b class="l">parallel</b> + <b class="l">o</b> + <b class="l">gram</b>.`,
 photosynthesis:`<b class="l">photo</b> (light) + <b class="l">synthesis</b> (putting together): making food with light.`,
 chlorophyll:`<b class="l">chloro</b> means green and <b class="l">phyll</b> means leaf: the green of the leaf.`,
 circumference:`<b class="l">circum</b> means around: circum + fer + ence.`,
 isosceles:`<b class="l">iso</b> means equal and <b class="l">sceles</b> means legs: I-SOS-CELES, two equal legs.`,
 onomatopoeia:`Chunk it: o-no-ma-to-<b class="l">poe</b>-ia. "Poe" like the poet!`,
 perpendicular:`per-<b class="l">pen</b>-dic-<b class="l">u</b>-lar: stand a pen up straight.`,
 cytoplasm:`<b class="l">cyto</b> means cell: cyto + plasm.`,
 thermometer:`<b class="l">thermo</b> (heat) + <b class="l">meter</b> (measure).`,
 democracy:`<b class="l">demo</b> (people) + <b class="l">cracy</b> (rule): rule by the people.`,
 chronological:`<b class="l">chrono</b> means time: chrono + logical.`,
 sustainable:`<b class="l">sustain</b> + <b class="l">able</b>: able to keep going.`,
 hypothesis:`<b class="l">hypo</b> (under) + <b class="l">thesis</b> (idea): an idea underneath the test.`,
 apostrophe:`a-<b class="l">pos</b>-<b class="l">tro</b>-<b class="l">phe</b>: the "phe" says "fee".`
};
const PREFIX={un:"not",dis:"not, or the opposite of",mis:"wrongly",pre:"before",sub:"under",inter:"between",trans:"across",anti:"against",
 auto:"self",micro:"very small",tele:"far away",photo:"light",bio:"life",geo:"earth",hydro:"water",super:"above or beyond",semi:"half",
 circum:"around",equ:"equal",peri:"around",mono:"one",poly:"many",therm:"heat",chrono:"time",demo:"people",over:"too much",under:"below or too little"};
const SUFFIX=[["ology","the study of"],["tion","makes a noun (a thing or an idea), said \"shun\""],["sion","makes a noun, said \"zhun\" or \"shun\""],
 ["ment","makes a noun: the result of doing something"],["ness","makes a noun: a state or quality"],["ious","means 'full of'"],["ous","means 'full of'"],
 ["able","means 'can be done'"],["ible","means 'can be done'"],["ful","means 'full of' (only one l!)"],["less","means 'without'"],
 ["ise","makes a verb (UK spelling uses -ise)"],["ity","makes a noun: a state or quality"],["ence","makes a noun"],["ance","makes a noun"],
 ["ical","means 'to do with'"],["meter","means 'measure'"],["graph","means 'written or drawn'"],["cracy","means 'rule by'"],["ly","makes an adverb: how something is done"]];
function wordParts(word){const w=word.toLowerCase(),out=[];
 const NOT_PREFIX=/^(unless|until|uniform|universe|university|unit|union|unique|united|unicorn|superb|demon|interest|interesting|substance|subtle|preach|precious|present|pressure|prepare|misery|dish|distance|distant|polite|politics|policy)$/;
 const p=NOT_PREFIX.test(w)?null:Object.keys(PREFIX).sort((a,b)=>b.length-a.length).find(k=>w.startsWith(k)&&w.length-k.length>=4);
 if(p)out.push(`Starts with <b class="l">${p}-</b>, which often means "${PREFIX[p]}".`);
 const sf=SUFFIX.find(([k])=>w.endsWith(k)&&w.length-k.length>=3);
 if(sf)out.push(`Ends with <b class="l">-${sf[0]}</b>, which ${sf[1].startsWith("makes")?sf[1]:sf[1]}.`);
 if(/our$/.test(w))out.push(`UK spelling: <b class="l">-our</b>, as in colour and honour.`);
 if(/tre$/.test(w))out.push(`UK spelling: <b class="l">-re</b>, as in centre and metre.`);
 if(!out.length)out.push(`Split it into chunks and say each part clearly: ${chunks(w).join(" · ")}.`);
 return out}
'''
rep('function tricks(word){', MORPH + 'function tricks(word){')
rep('  const w=word.toLowerCase(),out=[];\n', '  const w=word.toLowerCase(),out=[];\n  if(MNEMO[w])out.push(MNEMO[w]);\n')

# ---- home and words views ----
rep('<p>I am <b>Zulu 1 Ham Dog</b>, your personal tutor. Every week you give me your spelling words, and we learn them together with tricks, games and lots of stars.</p>',
    '<p>I am <b>Zulu 1 Ham Dog</b>, your personal tutor. Every week you give me your spelling words from school, and we master them together: spellings, meanings, word building, games and lots of stars. I also have Year 7 and 8 word packs for English, Maths, Science, History and Geography.</p>')
rep('''    <p class="hint">${weekLabel(WK)}. Type your words below. Put a comma or a new line between words.</p>
    <label for="wordInput">New words</label>
    <textarea id="wordInput" class="field" placeholder="because, friend, beautiful"></textarea>''',
    '''    <p class="hint">${weekLabel(WK)}. Type your words below, with a comma or new line between them. To add a meaning, put one word per line like this: <b>rhythm - a regular pattern of sound</b></p>
    <label for="wordInput">New words</label>
    <textarea id="wordInput" class="field" placeholder="necessary, separate, definitely&#10;photosynthesis - how plants make food using sunlight"></textarea>''')
rep('''    ${w.length?`<div class="chips">${w.map((x,i)=>`<span class="chip" style="--c:${COLORS[i%COLORS.length]}">${esc(x)} <span class="ok">''',
    '''    <div class="trick" style="--c:var(--grape)"><h3>🎒 Year 7 &amp; 8 word packs</h3>
      <p class="hint">Pick a subject, choose the words you need, and add them with their meanings.</p>
      <div class="packs">${Object.entries(PACKS).map(([k,p])=>`<button class="pk ${openPack===k?"on":""}" style="--c:${p.c}" data-pack="${k}"><span>${p.ic}</span>${p.name}</button>`).join("")}</div>
      ${openPack?`<div class="chips">${Object.keys(PACKS[openPack].words).map(x=>`<button class="pchip ${picked.has(x)?"on":""} ${w.includes(x)?"have":""}" data-pick="${x}" aria-pressed="${picked.has(x)}" title="${esc(PACKS[openPack].words[x])}">${w.includes(x)?"✓ ":""}${x}</button>`).join("")}</div>
        <div class="row"><button class="btn" style="--c:${PACKS[openPack].c}" id="addPicked" ${picked.size?"":"disabled"}>➕ Add ${picked.size} word${picked.size===1?"":"s"}</button>
        <button class="btn ghost" id="pickRandom">🎲 Pick 8 for me</button></div>`:""}
    </div>
    ${w.length?`<div class="chips">${w.map((x,i)=>`<span class="chip" style="--c:${COLORS[i%COLORS.length]}" title="${esc(meaningOf(x))}">${esc(x)} <span class="ok">''')

# ---- learn view: meaning + word building cards ----
rep('''      <div class="trick" style="--c:var(--grape)"><h3>🧠 Memory tricks</h3>''',
    '''      <div class="trick" style="--c:var(--tang)"><h3>📘 Meaning</h3>${meaningOf(word)?`<p>${esc(meaningOf(word))}</p><button class="btn ghost" id="meanW">🔊 Hear the meaning</button>`:`<p class="hint">No meaning saved yet. Look it up, then add it in My Words as <b>${esc(word)} - meaning</b>.</p>`}</div>
      <div class="trick" style="--c:var(--sea)"><h3>🧩 Word building</h3>${wordParts(word).map(t=>`<p>${t}</p>`).join("")}</div>
      <div class="trick" style="--c:var(--grape)"><h3>🧠 Memory tricks</h3>''')

# ---- games: Meaning Match + meanings in Spelling Bee ----
rep('.gamepick{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}',
    '.gamepick{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}')
rep('''      <button class="gcard" style="--c:var(--rose)" data-game="missing"><span class="ic">🕳️</span><strong>Missing Letters</strong><span>Fill the gaps and type the whole word.</span></button>''',
    '''      <button class="gcard" style="--c:var(--rose)" data-game="missing"><span class="ic">🕳️</span><strong>Missing Letters</strong><span>Fill the gaps and type the whole word.</span></button>
      <button class="gcard" style="--c:var(--grape)" data-game="meaning"><span class="ic">📘</span><strong>Meaning Match</strong><span>Read the meaning. Pick the right word.</span></button>''')
rep('const titles={bee:"🐝 Spelling Bee",scramble:"🔀 Unscramble",missing:"🕳️ Missing Letters",rev:"📝 Revision Test"};',
    'const titles={bee:"🐝 Spelling Bee",scramble:"🔀 Unscramble",missing:"🕳️ Missing Letters",meaning:"📘 Meaning Match",rev:"📝 Revision Test"};')
rep('''  if(game.type==="missing"){const n=Math.max(1,Math.round(w.length/4));''',
    '''  if(game.type==="meaning"){const pool=[...new Set([...game.queue,...Object.keys(PACKMEAN)])].filter(x=>x!==w);game.opts=shuffle([w,...shuffle(pool).slice(0,3)])}
  if(game.type==="missing"){const n=Math.max(1,Math.round(w.length/3));''')
rep('''else speak([`${NAME}, please spell: ${w}`])},250);''',
    '''else if(game.type==="meaning")speak([`Which word means: ${meaningOf(w,game.week||WK)}?`]);
    else{const m=meaningOf(w,game.week||WK);speak(m?[`${NAME}, please spell: ${w}.`,`Meaning: ${m}.`,w]:[`${NAME}, please spell: ${w}`])}},250);''')
rep('''  if(game.type==="scramble"){
    main=`<div class="built"''',
    '''  if(game.type==="meaning"){
    main=`<div class="meanq">${esc(meaningOf(w,game.week||WK))}</div>
      <div class="opts">${game.opts.map((o,i)=>`<button class="opt" style="--c:${COLORS[i%COLORS.length]}" data-opt="${esc(o)}" ${game.fb&&game.fb.next?"disabled":""}>${esc(o)}</button>`).join("")}</div>`;
  }else if(game.type==="scramble"){
    main=`<div class="built"''')
rep('''`<div class="prompt" aria-hidden="true">🐝 ${"_ ".repeat(w.length).trim()}</div>`}''',
    '''`<div class="prompt" aria-hidden="true">🐝 ${"_ ".repeat(w.length).trim()}</div>`}
      ${meaningOf(w,game.week||WK)?`<p class="hint" style="text-align:center"><b>Meaning:</b> ${esc(meaningOf(w,game.week||WK))}</p>`:""}''')
rep('''  document.querySelectorAll("[data-tile]")''',
    '''  document.querySelectorAll("[data-opt]").forEach(b=>b.onclick=()=>{speak(b.dataset.opt,{rate:1});check(b.dataset.opt)});
  document.querySelectorAll("[data-tile]")''')
rep('''  $("#hearG").onclick=()=>speak(w);''',
    '''  $("#hearG").onclick=()=>game.type==="meaning"?speak(`Which word means: ${meaningOf(w,game.week||WK)}?`):speak(w);''')
rep('''    document.querySelectorAll("[data-game]").forEach(b=>b.onclick=()=>startGame(b.dataset.game,words()));''',
    '''    document.querySelectorAll("[data-game]").forEach(b=>b.onclick=()=>{
      if(b.dataset.game==="meaning"){const list=words().filter(x=>meaningOf(x));
        if(!list.length){say(`${NAME}, none of this week's words has a meaning yet. Add meanings in My Words, or use a word pack.`,{mood:"think"});return}
        startGame("meaning",list);return}
      startGame(b.dataset.game,words())});''')

# ---- words binding: meanings and packs ----
rep('''    $("#addWords").onclick=()=>{const raw=$("#wordInput").value.split(/[\\s,;]+/).map(s=>s.trim().toLowerCase().replace(/[^a-z'\\-]/g,"")).filter(Boolean);
      if(!raw.length){say(`${NAME}, please type at least one word first.`);return}
      const wk=week();raw.forEach(x=>{if(!wk.words.includes(x))wk.words.push(x)});save();render();''',
    '''    $("#addWords").onclick=()=>{const wk=week(),raw=[];
      $("#wordInput").value.split(/\\n/).forEach(line=>{
        const m=line.match(/^\\s*([A-Za-z'\\-]+)\\s*(?:-|–|:|=)\\s*(.+)$/);
        if(m){const x=m[1].toLowerCase();raw.push(x);wk.meanings[x]=m[2].trim()}
        else line.split(/[\\s,;]+/).map(s=>s.trim().toLowerCase().replace(/[^a-z'\\-]/g,"")).filter(Boolean).forEach(x=>raw.push(x))});
      if(!raw.length){say(`${NAME}, please type at least one word first.`);return}
      raw.forEach(x=>{if(!wk.words.includes(x))wk.words.push(x)});save();render();''')
rep('''    $("#readAll").onclick=()=>speak([`Your words this week are:`,...words().map(w=>w+".")]);''',
    '''    $("#readAll").onclick=()=>speak([`Your words this week are:`,...words().map(w=>w+".")]);
    document.querySelectorAll("[data-pack]").forEach(b=>b.onclick=()=>{openPack=openPack===b.dataset.pack?null:b.dataset.pack;picked=new Set();render()});
    document.querySelectorAll("[data-pick]").forEach(b=>b.onclick=()=>{const x=b.dataset.pick;picked.has(x)?picked.delete(x):picked.add(x);render()});
    const ap=$("#addPicked");if(ap)ap.onclick=()=>{const wk=week(),n=[...picked].filter(x=>!wk.words.includes(x));n.forEach(x=>wk.words.push(x));
      picked=new Set();save();render();say(`Brilliant, ${NAME}! I added ${n.length} ${PACKS[openPack].name} word${n.length===1?"":"s"} with their meanings.`,{mood:"happy"})};
    const pr=$("#pickRandom");if(pr)pr.onclick=()=>{const have=week().words;picked=new Set(shuffle(Object.keys(PACKS[openPack].words).filter(x=>!have.includes(x))).slice(0,8));render()};''')
rep('''S.weeks[WK]={words:[],progress:{}};''', '''S.weeks[WK]={words:[],progress:{},meanings:{}};''')

# ---- learn binding ----
rep('''    $("#sayW").onclick=()=>speak(word);''',
    '''    $("#sayW").onclick=()=>speak(word);
    const mw=$("#meanW");if(mw)mw.onclick=()=>speak([word+".",meaningOf(word)]);''')

# ---- revision recap includes meanings ----
rep('''...words().map(w=>`${w}. ${spellOut(w)}. ${w}.`)],{rate:.8});''',
    '''...words().map(w=>`${w}. ${spellOut(w)}. ${w}.${meaningOf(w)?" It means: "+meaningOf(w)+".":""}`)],{rate:.8});''')

# ---- help text ----
rep('''<p>Each week, type the new spelling words and tap <b>Add words</b>.</p>''',
    '''<p>Each week, type your spelling words from school, or pick words from the Year 7 &amp; 8 subject packs. Add meanings with a dash.</p>''')
rep('''<p>Hear each word, clap the chunks, and read the memory tricks and silly stories.</p>''',
    '''<p>Hear each word and its meaning, see how the word is built from prefixes, roots and suffixes, and read the memory tricks.</p>''')
rep('''<p>Play Spelling Bee, Unscramble and Missing Letters. Zulu says each letter you type and reads back your answer.</p>''',
    '''<p>Play Spelling Bee, Unscramble, Missing Letters and Meaning Match. Zulu says each letter you type and reads back your answer.</p>''')

# ---- styles for packs and meaning game ----
rep('/* Radio signature call */', '''.packs{display:flex;flex-wrap:wrap;gap:8px}
.pk{--c:var(--sea);border:3px solid var(--c);background:var(--surface);color:var(--ink);border-radius:14px;padding:8px 14px;font-family:var(--display);font-weight:800;font-size:1.05rem;display:inline-flex;gap:6px;align-items:center}
.pk.on{background:var(--c);color:#fff}
.pchip{border:2px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:6px 14px;font-weight:700}
.pchip.on{background:var(--grape);border-color:var(--grape);color:#fff}
.pchip.have{opacity:.55}
.meanq{font-family:var(--display);font-size:clamp(1.3rem,4.5vw,1.8rem);font-weight:700;text-align:center;background:color-mix(in srgb,var(--grape) 12%,var(--surface));border:3px solid var(--grape);border-radius:18px;padding:16px}
.opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.opt{--c:var(--sea);border:0;border-radius:16px;background:var(--c);color:#fff;font-family:var(--display);font-weight:800;font-size:1.3rem;padding:14px 8px;box-shadow:0 4px 0 color-mix(in srgb,var(--c) 68%,#000);overflow-wrap:anywhere}
.opt[disabled]{opacity:.5}
@media (max-width:420px){.opts{grid-template-columns:1fr}}
/* Radio signature call */''')

open(dst, "w", encoding="utf-8").write(s)
print("ok", len(s))
