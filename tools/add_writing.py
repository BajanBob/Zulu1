"""Add the Writing module (letter formation + letter sounds) and clearer standard English speech."""
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, ("count", s.count(a), a[:90])
    s = s.replace(a, b)


# ---------- clearer standard English speech ----------
rep('''function speak(parts,{cancel=true,rate,onend}={}){
  if(window.AndroidTTS){
    const list=Array.isArray(parts)?parts:[parts];''',
'''/* Standard English, spoken clearly: each sentence becomes its own utterance, so the voice
   pauses between sentences instead of running them together. */
function clauses(parts){const out=[];(Array.isArray(parts)?parts:[parts]).forEach(t=>{
  const m=String(t).match(/[^.!?]+[.!?]*/g);(m||[String(t)]).forEach(x=>{x=x.trim();if(x)out.push(x)})});return out.length?out:[""]}
function speak(parts,{cancel=true,rate,onend}={}){
  parts=clauses(parts);
  if(window.AndroidTTS){
    const list=parts;''')
rep('''  const v=pickVoice(),list=Array.isArray(parts)?parts:[parts];
  if(keep.length>20)''', '''  const v=pickVoice(),list=parts;
  if(keep.length>60)''')
rep('''if(keep.length>60)keep.splice(0,keep.length-20);''', '''if(keep.length>60)keep.splice(0,keep.length-60);''')
rep('''u.lang=v?v.lang:"en-GB";''', '''u.lang="en-GB";''')
rep('''const spellOut=w=>w.toUpperCase().split("").join(", ");''',
'''/* British letter names, so Z is "zed" and H is "aitch" even on a voice that would say "zee" */
const LETTER_SAY={h:"Aitch",z:"Zed"};
const letterName=c=>LETTER_SAY[String(c).toLowerCase()]||String(c).toUpperCase();
const spellOut=w=>String(w).split("").filter(c=>/[a-z]/i.test(c)).map(letterName).join(". ");''')
rep('''speak(c.toUpperCase(),{rate:1})});''', '''speak(letterName(c),{rate:1})});''')
rep('''speak(`The next letter is ${w[i].toUpperCase()}`)};''', '''speak(`The next letter is ${letterName(w[i])}.`)};''')
rep('''rate:0.9, voice''', '''rate:0.85, voice''')

# ---------- nav: nine tiles (3 x 3 on a phone) ----------
rep('''.nav{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
@media (max-width:620px){.nav{grid-template-columns:repeat(4,1fr);gap:8px}}''',
'''.nav{display:grid;grid-template-columns:repeat(9,minmax(0,1fr));gap:8px}
.nav .tile{font-size:.92rem}
@media (max-width:760px){.nav{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.nav .tile{font-size:1rem}}''')
rep('''--rose:#F25CA8; --sky:#3F8CFF;''', '''--rose:#F25CA8; --sky:#3F8CFF; --mint:#12A58C;''')
rep('''    <button class="tile" style="--c:var(--tang)" data-view="learn"><span class="ic">💡</span>Learn</button>''',
'''    <button class="tile" style="--c:var(--tang)" data-view="learn"><span class="ic">💡</span>Learn</button>
    <button class="tile" style="--c:var(--mint)" data-view="writing"><span class="ic">✍️</span>Writing</button>''')
rep('''beryl:`This is Granny Beryl's corner.`,''',
    '''beryl:`This is Granny Beryl's corner.`,writing:`Let us practise writing and hearing our letters, ${NAME}.`,''')
rep('''const V={home,wordsView,learn,games,revision,rewards,beryl,help}''', '''const V={home,wordsView,learn,games,revision,rewards,beryl,help,writing}''')
rep('''      <button class="btn" style="--c:var(--coral)" id="chunkW">👏 Clap chunks</button></div>''',
'''      <button class="btn" style="--c:var(--coral)" id="chunkW">👏 Clap chunks</button>
      <button class="btn" style="--c:var(--mint)" id="lettersW">🐣 Letter by letter</button></div>''')
rep('''    $("#sayW").onclick=()=>speak(word);''',
'''    $("#sayW").onclick=()=>speak(word);
    const lw=$("#lettersW");if(lw)lw.onclick=()=>{WR.mode="words";WR.word=word;go("writing");sayLetters(word)};''')

# ---------- the Writing module ----------
MODULE = r'''
/* ---------- Writing: forming letters, and hearing letters ----------
   Letters sit on four lines like a UK handwriting book, in a 100 x 115 box:
   top line y=10, middle line y=45, base line y=80, tail line y=105.
   Each letter is a list of strokes (SVG paths) drawn in order. */
const C_SHAPE="M66,50 C60,43 44,43 37,52 C31,60 32,72 39,78 C46,83 60,82 66,74";
const BOWL="L35,62 C35,52 42,45 51,45 C61,45 67,53 67,62 C67,73 60,80 51,80 C43,80 36,75 35,68";
const HUMP="C38,48 45,45 50,45 C58,45 65,50 65,60 L65,80";
const STROKES={
 a:[C_SHAPE,"M67,45 L67,80"], b:["M35,10 L35,80 "+BOWL], c:[C_SHAPE], d:[C_SHAPE,"M67,10 L67,80"],
 e:["M34,63 L67,63 C67,50 58,45 50,45 C40,45 33,53 33,63 C33,74 41,80 51,80 C58,80 63,77 66,73"],
 f:["M64,16 C60,10 50,9 46,15 C44,19 44,24 44,30 L44,80","M34,45 L58,45"], g:[C_SHAPE,"M67,45 L67,98 C67,110 45,110 38,102"],
 h:["M35,10 L35,80 L35,58 "+HUMP], i:["M50,45 L50,80","M50,30 L50,31"], j:["M55,45 L55,98 C55,108 42,108 38,100","M55,30 L55,31"],
 k:["M37,10 L37,80","M62,45 L37,66 L63,80"], l:["M50,10 L50,80"],
 m:["M28,45 L28,80 L28,57 C30,48 36,45 40,45 C46,45 50,50 50,58 L50,80 L50,57 C52,48 58,45 62,45 C68,45 72,50 72,58 L72,80"],
 n:["M35,45 L35,80 L35,58 "+HUMP], o:["M66,50 C60,43 44,43 37,52 C31,60 32,72 39,78 C46,83 60,83 65,76 C70,68 70,56 66,50"],
 p:["M35,45 L35,105 "+BOWL], q:[C_SHAPE,"M67,45 L67,105"], r:["M38,45 L38,80 L38,60 C40,50 50,44 62,47"],
 s:["M64,50 C60,45 52,44 46,45 C38,47 36,55 42,59 C48,63 60,62 64,68 C68,75 60,81 50,80 C43,80 37,78 35,74"],
 t:["M47,22 L47,74 C47,80 55,82 60,78","M37,45 L60,45"], u:["M35,45 L35,68 C35,77 41,80 49,80 C57,80 65,75 65,65 L65,45 L65,80"],
 v:["M33,45 L50,80 L67,45"], w:["M25,45 L37,80 L50,52 L63,80 L75,45"], x:["M35,45 L65,80","M65,45 L35,80"],
 y:["M35,45 L35,66 C35,76 42,80 49,80 C57,80 65,75 65,66 L65,45 L65,98 C65,108 48,110 40,102"], z:["M35,45 L65,45 L35,80 L65,80"],
 A:["M50,10 L30,80","M50,10 L70,80","M37,56 L63,56"],
 B:["M33,10 L33,80","M33,10 L52,10 C62,10 66,17 66,26 C66,35 60,43 52,43 L33,43","M52,43 C64,43 70,51 70,61 C70,72 62,80 52,80 L33,80"],
 C:["M68,22 C62,12 54,10 49,10 C36,10 30,25 30,45 C30,65 36,80 49,80 C56,80 63,76 68,68"],
 D:["M33,10 L33,80","M33,10 L48,10 C62,10 70,25 70,45 C70,65 62,80 48,80 L33,80"],
 E:["M35,10 L35,80","M35,10 L65,10","M35,45 L60,45","M35,80 L65,80"], F:["M35,10 L35,80","M35,10 L65,10","M35,45 L60,45"],
 G:["M68,22 C62,12 54,10 49,10 C36,10 30,25 30,45 C30,65 36,80 49,80 C56,80 63,76 68,68 L68,50 L54,50"],
 H:["M33,10 L33,80","M67,10 L67,80","M33,45 L67,45"], I:["M50,10 L50,80","M38,10 L62,10","M38,80 L62,80"],
 J:["M60,10 L60,64 C60,76 54,80 47,80 C40,80 36,76 34,70"], K:["M35,10 L35,80","M66,10 L35,52","M46,40 L67,80"],
 L:["M35,10 L35,80 L65,80"], M:["M28,80 L28,10 L50,52 L72,10 L72,80"], N:["M32,80 L32,10 L68,80 L68,10"],
 O:["M50,10 C36,10 30,26 30,45 C30,64 36,80 50,80 C64,80 70,64 70,45 C70,26 64,10 50,10"],
 P:["M33,10 L33,80","M33,10 L52,10 C63,10 68,18 68,28 C68,38 62,46 52,46 L33,46"],
 Q:["M50,10 C36,10 30,26 30,45 C30,64 36,80 50,80 C64,80 70,64 70,45 C70,26 64,10 50,10","M55,64 L72,84"],
 R:["M33,10 L33,80","M33,10 L52,10 C63,10 68,18 68,28 C68,38 62,46 52,46 L33,46","M50,46 L68,80"],
 S:["M66,20 C61,12 55,10 49,10 C39,10 32,16 32,26 C32,36 42,40 50,44 C59,48 68,52 68,63 C68,74 60,80 50,80 C42,80 35,77 31,69"],
 T:["M50,10 L50,80","M30,10 L70,10"], U:["M32,10 L32,58 C32,72 40,80 50,80 C60,80 68,72 68,58 L68,10"],
 V:["M30,10 L50,80 L70,10"], W:["M24,10 L36,80 L50,32 L64,80 L76,10"], X:["M32,10 L68,80","M68,10 L32,80"],
 Y:["M32,10 L50,45 L50,80","M68,10 L50,45"], Z:["M32,10 L68,10 L32,80 L68,80"]
};
/* UK letter families and a spoken tip for each small letter */
const TIP={
 a:"Curly caterpillar letter. Go round like a c, then up and down.", b:"Ladder letter. Down the long ladder, back up, and round.",
 c:"Curly caterpillar letter. Start at the top and curl round.", d:"Curly caterpillar letter. Round like a c, up tall, then down.",
 e:"Curly caterpillar letter. Go across the middle, then curl round.", f:"Curly caterpillar letter. Over the top, down, then cross it.",
 g:"Curly caterpillar letter. Round like a c, up, then down under the line and hook.", h:"One-armed robot letter. Down tall, back up, and over the hump.",
 i:"Ladder letter. Go down, then add the dot.", j:"Ladder letter. Down below the line, hook, then add the dot.",
 k:"One-armed robot letter. Down tall, then in and out.", l:"Ladder letter. Start at the top and go straight down.",
 m:"One-armed robot letter. Down, up and over, up and over again.", n:"One-armed robot letter. Down, back up, and over.",
 o:"Curly caterpillar letter. Start at the top and go all the way round.", p:"One-armed robot letter. Down under the line, back up, and round.",
 q:"Curly caterpillar letter. Round like a c, up, then straight down under the line.", r:"One-armed robot letter. Down, back up, and over a little.",
 s:"Curly caterpillar letter. Curl back, then forward, like a snake.", t:"Ladder letter. Down and flick, then cross it.",
 u:"Ladder letter. Down, round, up, and down.", v:"Zigzag monster letter. Down to the line and back up.",
 w:"Zigzag monster letter. Down, up, down, up.", x:"Zigzag monster letter. One line down this way, one line down that way.",
 y:"Ladder letter. Down, round, up, then down under the line and hook.", z:"Zigzag monster letter. Across, down to the corner, and across."
};
/* Letter sounds: B says buh, B is for ball. Vowels and long sounds are taught by their word. */
const PHONICS={a:["","apple","🍎"],b:["buh","ball","⚽"],c:["kuh","cat","🐱"],d:["duh","dog","🐶"],e:["","egg","🥚"],f:["","fish","🐟"],
 g:["guh","goat","🐐"],h:["huh","hat","🎩"],i:["","insect","🐞"],j:["juh","jet","✈️"],k:["kuh","kite","🪁"],l:["","lion","🦁"],
 m:["","moon","🌙"],n:["","net","🥅"],o:["","octopus","🐙"],p:["puh","pig","🐷"],q:["kwuh","queen","👑"],r:["","rabbit","🐰"],
 s:["","sun","☀️"],t:["tuh","tiger","🐯"],u:["","umbrella","☂️"],v:["","van","🚐"],w:["wuh","web","🕸️"],x:["","box","📦"],
 y:["yuh","yellow","💛"],z:["","zebra","🦓"]};
function letterLines(c){const l=c.toLowerCase(),U=letterName(l),[snd,word]=PHONICS[l]||["",""];
  return [`${U}.`,...(snd?[`${U} says ${snd}.`]:[]),word?(l==="x"?`${U} is at the end of ${word}.`:`${U} is for ${word}.`):""].filter(Boolean)}
const WR={mode:"write",upper:false,letter:"a",word:null,ink:[],active:-1};
const ABC="abcdefghijklmnopqrstuvwxyz".split("");
function sayLetters(word,i=0){const w=String(word).toLowerCase().replace(/[^a-z]/g,"");
  if(i>=w.length){WR.active=-1;paintActive();speak([`${w.split("").map(letterName).join(". ")}.`,`That spells ${w}.`],{cancel:false});return}
  WR.active=i;paintActive();speak(letterLines(w[i]),{cancel:i===0,rate:Math.min(S.settings.rate,.85),onend:()=>{if(view==="writing"&&WR.word===word)sayLetters(word,i+1)}})}
function paintActive(){document.querySelectorAll("[data-wl]").forEach(b=>b.classList.toggle("now",+b.dataset.wl===WR.active))}

function writing(){
  const tabs=`<div class="wtabs" role="tablist">
    <button class="wtab ${WR.mode==="write"?"on":""}" data-wmode="write">✍️ Write letters</button>
    <button class="wtab ${WR.mode==="abc"?"on":""}" data-wmode="abc">🔤 Letter sounds</button>
    <button class="wtab ${WR.mode==="words"?"on":""}" data-wmode="words">🐣 Letters in my words</button></div>`;
  let body="";
  if(WR.mode==="write"){
    const L=WR.upper?WR.letter.toUpperCase():WR.letter, strokes=STROKES[L]||[], ph=PHONICS[WR.letter]||["","",""];
    const tip=WR.upper?`Capital ${letterName(L)} has ${strokes.length} stroke${strokes.length>1?"s":""}. Start at the green dot and follow the numbers.`:TIP[WR.letter];
    body=`<div class="row"><button class="wtab ${WR.upper?"":"on"}" data-case="lower">abc small letters</button><button class="wtab ${WR.upper?"on":""}" data-case="upper">ABC capital letters</button></div>
    <div class="abc">${ABC.map(c=>`<button class="ab ${c===WR.letter?"on":""}" data-wletter="${c}" aria-label="Letter ${letterName(c)}">${WR.upper?c.toUpperCase():c}</button>`).join("")}</div>
    <div class="wgrid">
      <div class="pad" id="pad">
        <svg viewBox="0 0 100 115" aria-hidden="true">
          <line x1="2" x2="98" y1="10" y2="10" class="gl"/><line x1="2" x2="98" y1="45" y2="45" class="gl dash"/>
          <line x1="2" x2="98" y1="80" y2="80" class="gl base"/><line x1="2" x2="98" y1="105" y2="105" class="gl dash"/>
          ${strokes.map(d=>`<path d="${d}" class="road"/>`).join("")}
          ${strokes.map((d,i)=>`<path d="${d}" class="demo" data-demo="${i}"/>`).join("")}
          <g id="dots"></g>
        </svg>
        <canvas id="ink" aria-label="Writing pad. Trace the letter here."></canvas>
      </div>
      <div class="wside">
        <div class="bigl"><span>${esc(L)}</span><span class="emo">${ph[2]}</span></div>
        <p class="wtip"><b>How to write it:</b> ${esc(tip)}</p>
        <div class="row"><button class="btn" style="--c:var(--mint)" id="showMe">▶ Show me</button><button class="btn" style="--c:var(--sea)" id="hearL">🔊 Hear it</button></div>
        <div class="row"><button class="btn ghost" id="clearInk">🧽 Clear</button><button class="btn big" style="--c:var(--leaf)" id="doneInk">✅ I'm done</button></div>
        <div class="row"><button class="btn ghost" id="prevL" aria-label="Previous letter">◀</button><button class="btn ghost" id="nextL" aria-label="Next letter">Next letter ▶</button></div>
        <div id="wfb" aria-live="polite"></div>
      </div>
    </div>`;
  }else if(WR.mode==="abc"){
    body=`<p class="hint">Tap a letter to hear its name, its sound and a word that starts with it.</p>
    <div class="cards">${ABC.map((c,i)=>`<button class="lcard" style="--c:${COLORS[i%COLORS.length]}" data-say-letter="${c}"><b>${c.toUpperCase()}${c}</b><span class="emo">${PHONICS[c][2]}</span><small>${PHONICS[c][1]}</small></button>`).join("")}</div>
    <button class="btn big" style="--c:var(--mint)" id="singABC">🎵 Say the whole alphabet</button>`;
  }else{
    const w=words();if(!WR.word||!w.includes(WR.word))WR.word=w[0];
    const ww=WR.word.toLowerCase().replace(/[^a-z]/g,"");
    body=`<p class="hint">Pick a word. Zulu says each letter, its sound, and a word that starts with it. Tap any letter to hear it again.</p>
    <div class="chips">${w.map((x,i)=>`<button class="pchip ${x===WR.word?"on":""}" data-wword="${esc(x)}">${esc(x)}</button>`).join("")}</div>
    <div class="wltiles">${ww.split("").map((c,i)=>`<button class="wlt" style="--c:${COLORS[i%COLORS.length]}" data-wl="${i}"><b>${c}</b><span>${(PHONICS[c]||["","",""])[2]}</span></button>`).join("")}</div>
    <div class="row" style="justify-content:center"><button class="btn big" style="--c:var(--mint)" id="soundOut">▶ Letter by letter</button>
    <button class="btn" style="--c:var(--sea)" id="sayWord">🔊 Say the word</button><button class="btn ghost" id="writeFirst">✍️ Write the first letter</button></div>`;
  }
  return panel("var(--mint)","Writing &amp; Letter Sounds",tabs+body);
}

/* the writing pad: finger or mouse ink, kept in letter-box units so it survives resizing */
function padSetup(){
  const pad=$("#pad"),cv=$("#ink");if(!pad||!cv)return;
  const svg=pad.querySelector("svg"),paths=[...svg.querySelectorAll("path.road")];
  $("#dots").innerHTML=paths.map((p,i)=>{const a=p.getPointAtLength(0);
    return `<circle cx="${a.x}" cy="${a.y}" r="4.2" class="sdot"/><text x="${a.x}" y="${a.y+1.6}" class="snum">${i+1}</text>`}).join("");
  const fit=()=>{const r=pad.getBoundingClientRect(),dpr=window.devicePixelRatio||1;cv.width=Math.round(r.width*dpr);cv.height=Math.round(r.height*dpr);draw()};
  const draw=()=>{const g=cv.getContext("2d"),k=cv.width/100;g.clearRect(0,0,cv.width,cv.height);
    g.lineCap="round";g.lineJoin="round";g.lineWidth=4.5*k;g.strokeStyle=getComputedStyle(document.documentElement).getPropertyValue("--sky").trim()||"#3F8CFF";
    WR.ink.forEach(st=>{g.beginPath();st.forEach((q,i)=>i?g.lineTo(q[0]*k,q[1]*k):g.moveTo(q[0]*k,q[1]*k));if(st.length===1)g.lineTo(st[0][0]*k+.1,st[0][1]*k);g.stroke()})};
  const pt=e=>{const r=cv.getBoundingClientRect();return [(e.clientX-r.left)/r.width*100,(e.clientY-r.top)/r.height*115]};
  let cur=null;
  cv.onpointerdown=e=>{e.preventDefault();try{cv.setPointerCapture(e.pointerId)}catch(_){}cur=[pt(e)];WR.ink.push(cur);draw()};
  cv.onpointermove=e=>{if(!cur)return;cur.push(pt(e));draw()};
  cv.onpointerup=cv.onpointercancel=()=>{cur=null};
  fit();window.onresize=()=>{if(view==="writing"&&$("#ink"))fit()};
  WR.redraw=draw;
}
/* how much of the letter was traced, and how much of the ink stayed on the letter */
function scoreInk(){
  const paths=[...document.querySelectorAll("#pad path.road")],model=[];
  paths.forEach(p=>{const n=p.getTotalLength();for(let d=0;d<=n;d+=2){const a=p.getPointAtLength(d);model.push([a.x,a.y])}});
  const ink=WR.ink.flat();if(!ink.length||!model.length)return {cover:0,neat:0};
  const near=(a,list,r)=>list.some(b=>(a[0]-b[0])**2+(a[1]-b[1])**2<=r*r);
  return {cover:model.filter(m=>near(m,ink,7.5)).length/model.length, neat:ink.filter(q=>near(q,model,9)).length/ink.length};
}
function animateStrokes(){
  const demos=[...document.querySelectorAll("#pad path.demo")],reduce=matchMedia("(prefers-reduced-motion: reduce)").matches;
  demos.forEach(p=>{const n=p.getTotalLength();p.style.strokeDasharray=n;p.style.strokeDashoffset=n;p.style.opacity=1});
  let i=0;const next=()=>{if(i>=demos.length)return;const p=demos[i++],n=p.getTotalLength();
    if(reduce){p.style.strokeDashoffset=0;next();return}
    const t0=performance.now(),dur=Math.max(500,n*14);
    const step=t=>{const k=Math.min(1,(t-t0)/dur);p.style.strokeDashoffset=n*(1-k);if(k<1)requestAnimationFrame(step);else setTimeout(next,250)};requestAnimationFrame(step)};
  next();
}
'''
rep('/* ---------- game engine ---------- */', MODULE + '\n/* ---------- game engine ---------- */')

BIND = r'''  writing(){common();
    document.querySelectorAll("[data-wmode]").forEach(b=>b.onclick=()=>{WR.mode=b.dataset.wmode;WR.ink=[];stopSpeech();render()});
    if(WR.mode==="write"){
      const L=()=>WR.upper?WR.letter.toUpperCase():WR.letter;
      document.querySelectorAll("[data-case]").forEach(b=>b.onclick=()=>{WR.upper=b.dataset.case==="upper";WR.ink=[];render();speak(letterLines(WR.letter)[0])});
      document.querySelectorAll("[data-wletter]").forEach(b=>b.onclick=()=>{WR.letter=b.dataset.wletter;WR.ink=[];render();speak(letterLines(WR.letter))});
      padSetup();
      $("#showMe").onclick=()=>{animateStrokes();speak([WR.upper?`Capital ${letterName(L())}.`:`${letterName(L())}.`,WR.upper?`Start at the green dot, and follow the numbers.`:TIP[WR.letter]])};
      $("#hearL").onclick=()=>speak(letterLines(WR.letter));
      $("#clearInk").onclick=()=>{WR.ink=[];WR.redraw&&WR.redraw();$("#wfb").innerHTML=""};
      $("#doneInk").onclick=()=>{const r=scoreInk();
        if(r.cover>=.7&&r.neat>=.6){ding();burst();addStars(1);const pr=rand(PRAISE);
          $("#wfb").innerHTML=`<div class="feedback good">⭐ Beautiful ${esc(L())}! ${pr}</div>`;say(pr,{voice:false,mood:"happy"});speak([`Beautiful ${letterName(L())}!`,pr])}
        else{boop();const pe=rand(PERSIST),why=r.cover<.7?"Try to trace the whole grey letter.":"Try to keep your line on the grey letter.";
          $("#wfb").innerHTML=`<div class="feedback bad">${why} ${pe}</div>`;say(pe,{voice:false,mood:"think"});speak([why,pe])}};
      const mv=d=>{const i=(ABC.indexOf(WR.letter)+d+26)%26;WR.letter=ABC[i];WR.ink=[];render();speak(letterLines(WR.letter))};
      $("#prevL").onclick=()=>mv(-1);$("#nextL").onclick=()=>mv(1);
    }else if(WR.mode==="abc"){
      document.querySelectorAll("[data-say-letter]").forEach(b=>b.onclick=()=>speak(letterLines(b.dataset.sayLetter)));
      $("#singABC").onclick=()=>speak(ABC.map(c=>letterName(c)+"."),{rate:.8});
    }else{
      document.querySelectorAll("[data-wword]").forEach(b=>b.onclick=()=>{WR.word=b.dataset.wword;render();sayLetters(WR.word)});
      document.querySelectorAll("[data-wl]").forEach(b=>b.onclick=()=>{const w=WR.word.toLowerCase().replace(/[^a-z]/g,"");WR.active=+b.dataset.wl;paintActive();speak(letterLines(w[WR.active]))});
      $("#soundOut").onclick=()=>sayLetters(WR.word);
      $("#sayWord").onclick=()=>speak(WR.word);
      $("#writeFirst").onclick=()=>{const c=WR.word.toLowerCase().replace(/[^a-z]/g,"")[0];if(!c)return;WR.mode="write";WR.letter=c;WR.upper=false;WR.ink=[];render();speak(letterLines(c))};
    }
  },
'''
rep('''  help(){common();''', BIND + '''  help(){common();''')

CSS = '''/* Writing module */
.wtabs{display:flex;flex-wrap:wrap;gap:8px}
.wtab{border:3px solid var(--mint);background:var(--surface);color:var(--ink);border-radius:14px;padding:8px 14px;font-family:var(--display);font-weight:800;font-size:1.05rem}
.wtab.on{background:var(--mint);color:#fff}
.abc{display:flex;flex-wrap:wrap;gap:6px}
.ab{width:44px;height:48px;border-radius:12px;border:2px solid var(--line);background:var(--surface);color:var(--ink);font-family:"Andika",var(--body);font-size:1.5rem;font-weight:700}
.ab.on{background:var(--mint);border-color:var(--mint);color:#fff}
.wgrid{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:16px;align-items:start}
@media (max-width:640px){.wgrid{grid-template-columns:1fr}}
.pad{position:relative;width:100%;max-width:440px;aspect-ratio:100/115;background:#FFFDF6;border:4px solid var(--mint);border-radius:20px;overflow:hidden;justify-self:center;touch-action:none}
.pad svg,.pad canvas{position:absolute;inset:0;width:100%;height:100%}
.pad canvas{touch-action:none;cursor:crosshair}
.gl{stroke:#9DB7D5;stroke-width:.6}.gl.dash{stroke-dasharray:2 2}.gl.base{stroke:#E0526A;stroke-width:.9}
.road{fill:none;stroke:#D9DEE8;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.demo{fill:none;stroke:#F25CA8;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;opacity:0}
.sdot{fill:#1E9E55}.snum{fill:#fff;font:700 5px sans-serif;text-anchor:middle}
.wside{display:flex;flex-direction:column;gap:12px;min-width:0}
.bigl{display:flex;align-items:center;gap:14px;font-family:"Andika",var(--body);font-size:5rem;line-height:1;color:var(--mint);font-weight:700}
.bigl .emo,.lcard .emo{font-family:system-ui,sans-serif}
.bigl .emo{font-size:3rem}
.wtip{font-size:1.1rem}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:10px}
.lcard{--c:var(--sea);border:3px solid var(--c);background:color-mix(in srgb,var(--c) 12%,var(--surface));color:var(--ink);border-radius:18px;padding:10px 6px;display:flex;flex-direction:column;align-items:center;gap:2px}
.lcard b{font-family:"Andika",var(--body);font-size:1.9rem;color:color-mix(in srgb,var(--c) 75%,var(--ink))}
.lcard .emo{font-size:1.8rem}.lcard small{font-weight:700;color:var(--muted)}
.wltiles{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.wlt{--c:var(--sea);width:72px;border:0;border-radius:16px;background:var(--c);color:#fff;padding:8px 0;display:flex;flex-direction:column;align-items:center;box-shadow:0 4px 0 color-mix(in srgb,var(--c) 68%,#000);transition:transform .15s}
.wlt b{font-family:"Andika",var(--body);font-size:2.6rem;line-height:1.1}
.wlt span{font-size:1.4rem}
.wlt.now{transform:translateY(-8px) scale(1.12);outline:4px solid var(--ink);outline-offset:2px}
/* Radio signature call */'''
rep('/* Radio signature call */', CSS)
rep('family=Baloo+2:wght@600;700;800&family=Atkinson+Hyperlegible:wght@400;700',
    'family=Baloo+2:wght@600;700;800&family=Atkinson+Hyperlegible:wght@400;700&family=Andika:wght@400;700')

# help card
rep('''      <div class="trick" style="--c:var(--grape)"><h3>4. 📚 Revision</h3>''',
'''      <div class="trick" style="--c:var(--mint)"><h3>✍️ Writing</h3><p>Trace letters on the handwriting lines. Tap <b>Show me</b> to watch how each letter is formed, then trace it and tap <b>I'm done</b>. <b>Letter sounds</b> says each letter's name and sound.</p></div>
      <div class="trick" style="--c:var(--grape)"><h3>4. 📚 Revision</h3>''')

open(p, "w", encoding="utf-8").write(s)
print("ok")
