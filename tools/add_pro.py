"""Zulu 1 Pro: an agentic practice planner, AI memory tricks and mistake help, plus bundled fonts.

Privacy rules built into the code:
  - only spelling words and right/wrong counts (and, for a mistake, the attempted spelling) are sent;
  - every outgoing text is scrubbed of the student's names before it leaves the device;
  - nothing else (no names, ages, voices, handwriting or location) is ever sent.
"""
import base64, sys

page, fontdir = sys.argv[1], sys.argv[2]
s = open(page, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, ("count", s.count(a), a[:90])
    s = s.replace(a, b)


# ---------- bundled fonts: nothing is fetched from Google ----------
FONTS = [("Baloo 2", 600, "baloo-2"), ("Baloo 2", 700, "baloo-2"), ("Baloo 2", 800, "baloo-2"),
         ("Atkinson Hyperlegible", 400, "atkinson-hyperlegible"), ("Atkinson Hyperlegible", 700, "atkinson-hyperlegible"),
         ("Andika", 400, "andika"), ("Andika", 700, "andika")]
faces = []
for fam, w, slug in FONTS:
    path = f"{fontdir}/fontsource-{slug}-5.0.20/package/files/{slug}-latin-{w}-normal.woff2"
    b64 = base64.b64encode(open(path, "rb").read()).decode()
    faces.append(f'@font-face{{font-family:"{fam}";font-style:normal;font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{b64}) format("woff2")}}')
FONT_CSS = "<style>/* Fonts bundled in the page (SIL Open Font License), so nothing loads from outside */\n" + "\n".join(faces) + "\n</style>\n"
start = s.index('<link rel="preconnect" href="https://fonts.googleapis.com">')
end = s.index('>', s.index('<link rel="stylesheet" href="https://fonts.googleapis.com')) + 1
s = s[:start] + FONT_CSS + s[end:].lstrip("\n")

# ---------- Pro badge ----------
rep('<h1>Zulu 1 Ham Dog Tutor</h1>', '<h1>Zulu 1 Ham Dog Tutor <span class="probadge" id="proBadge" hidden>PRO</span></h1>')

PRO_JS = r'''
/* ---------- Zulu 1 Pro: the agentic coach ----------
   Zulu plans each session: it picks the words that need the most work and the activities to use,
   and starts them with one tap. The built-in planner always works offline. With Pro switched on,
   an AI model (Claude, by Anthropic) makes the plan, writes memory tricks and explains mistakes. */
const LEVEL="a young child learning to read and spell, about 5 to 8 years old, in a British English school";
const ACTIVITIES=["learn","bee","scramble","missing","writing","revision"];
const ACT={learn:["💡","Learn"],bee:["🐝","Spelling Bee"],scramble:["🔀","Unscramble"],missing:["🕳️","Missing Letters"],
  meaning:["📘","Meaning Match"],writing:["✍️","Writing"],revision:["📝","Revision test"]};
const PRO_MODEL="claude-haiku-5-5", PRO_API_VERSION="2026-10-21";
function pro(){if(!S.settings.pro)S.settings.pro={mode:"off",url:"",code:"",key:""};return S.settings.pro}
function proOn(){const p=pro();return (p.mode==="service"&&/^https:\/\//.test(p.url))||(p.mode==="key"&&p.key.length>20)}
/* Names never leave the device: every outgoing text is scrubbed first. */
const NAME_PARTS=NAME.replace(/^(Master|Miss|Mr|Mrs|Ms)\s+/i,"").split(/\s+/).filter(x=>x.length>1).concat(["Shakai","Stoute","Bubba","Elian"]);
function scrub(t){let x=String(t);NAME_PARTS.forEach(n=>{x=x.replace(new RegExp("\\b"+n.replace(/[^a-z]/gi,"")+"\\b","gi"),"the student")});return x}
const hasMeaning=w=>typeof meaningOf==="function"&&!!meaningOf(w);
function needScore(w){const p=prog(w);return p.wrong*2-p.right*1.5-(p.right>=3?10:0)}
function localPlan(){
  const w=words(),sorted=w.slice().sort((a,b)=>needScore(b)-needScore(a)),tricky=sorted.slice(0,Math.min(3,w.length));
  const steps=[];
  if(w.every(x=>prog(x).right>=3)){steps.push({activity:"revision",words:w,why:"Every word has three stars. Show what you know in the revision test!"})}
  else{
    steps.push({activity:"learn",words:tricky,why:`Look closely at ${tricky.join(", ")} first. These need the most practice.`});
    steps.push({activity:"bee",words:tricky,why:"Now spell those tricky words from memory."});
    if(ACTIVITIES.includes("meaning")&&w.some(hasMeaning))steps.push({activity:"meaning",words:w.filter(hasMeaning),why:"Match each word to its meaning."});
    else steps.push({activity:"scramble",words:w,why:"Unscramble all of this week's words."});
    if(ACTIVITIES.includes("writing"))steps.push({activity:"writing",words:[tricky[0]],why:`Say the letters of ${tricky[0]}, then write the first one neatly.`});
    else steps.push({activity:"missing",words:w,why:"Fill in the missing letters in every word."});
  }
  return {source:"local",message:"Here is my plan for today. Tap Start on each step.",steps};
}
function currentPlan(){const p=S.proPlan;return p&&p.week===WK&&p.sig===planSig()?p:localPlan()}
const planSig=()=>words().join(",");
function cleanPlan(raw){
  const w=words(),lc=w.map(x=>x.toLowerCase());
  const steps=(Array.isArray(raw&&raw.steps)?raw.steps:[]).filter(st=>st&&ACTIVITIES.includes(st.activity)).slice(0,5).map(st=>{
    let ws=(Array.isArray(st.words)?st.words:[]).map(x=>String(x).toLowerCase()).filter(x=>lc.includes(x)).map(x=>w[lc.indexOf(x)]);
    if(!ws.length)ws=w.slice();return {activity:st.activity,words:[...new Set(ws)],why:String(st.why||"").slice(0,220)}});
  if(!steps.length)throw new Error("The plan came back empty.");
  const tricks={};Object.entries((raw&&raw.tricks)||{}).forEach(([k,v])=>{const i=lc.indexOf(String(k).toLowerCase());if(i>=0)tricks[w[i]]=String(v).slice(0,240)});
  return {source:"pro",week:WK,sig:planSig(),message:String((raw&&raw.message)||"Here is your plan.").slice(0,300),steps,tricks};
}
/* What is sent: the level, the activities, and each word with its right/wrong counts. Nothing else. */
function planRequest(){return {kind:"plan",level:LEVEL,activities:ACTIVITIES,words:words().map(w=>({w:scrub(w),right:prog(w).right,wrong:prog(w).wrong}))}}
function promptFor(req){
  const system=`You are Zulu 1, a warm and encouraging spelling tutor (a friendly cartoon dog) inside a children's learning app. `+
    `The learner is ${req.level}. Use British English spelling. Speak to the learner as "you" and never use, guess or ask for names or any personal details. `+
    `Keep every sentence short, kind and simple. Reply with one JSON object only, with no other text.`;
  if(req.kind==="tip")return {system,user:`The learner was asked to spell "${req.target}" and wrote "${req.attempt}". `+
    `In one or two short sentences, kindly point out the tricky part and give one way to remember the correct spelling. Reply as {"tip":"..."}`};
  return {system,user:`Plan a 10 to 15 minute practice session.\nThis week's words, with how often each was spelled right and wrong:\n${JSON.stringify(req.words)}\n`+
    `Available activities: ${req.activities.join(", ")} (learn = study the word; bee = spell it from memory; scramble = unscramble letters; `+
    `missing = fill in missing letters; meaning = match words to meanings; writing = say the letters and practise handwriting; revision = a test of all words).\n`+
    `Choose 3 or 4 steps that focus on the words that need the most practice. Each step has "activity" (from the list), "words" (only words from the list) `+
    `and "why" (one short sentence spoken to the learner). Also give "message" (one or two short encouraging sentences) and "tricks": `+
    `an object giving a short, child-friendly memory trick for up to 3 of the trickiest words.\n`+
    `Reply as {"message":"...","steps":[{"activity":"...","words":["..."],"why":"..."}],"tricks":{"word":"trick"}}`};
}
function parseJSON(t){const m=String(t).match(/\{[\s\S]*\}/);if(!m)throw new Error("Zulu Pro sent an answer the app could not read.");return JSON.parse(m[0])}
async function askPro(req){
  const p=pro(),ctl=new AbortController(),timer=setTimeout(()=>ctl.abort(),25000);
  try{
    let r;
    if(p.mode==="service"){
      r=await fetch(p.url.replace(/\/+$/,"")+"/v1/zulu",{method:"POST",signal:ctl.signal,headers:{"content-type":"application/json","x-zulu-code":p.code||""},body:JSON.stringify(req)});
      if(!r.ok)throw new Error(r.status===401?"The access code was not accepted.":`The Pro service answered with error ${r.status}.`);
      return await r.json();
    }
    const q=promptFor(req);
    r=await fetch("https://api.anthropic.com/v1/messages",{method:"POST",signal:ctl.signal,headers:{"content-type":"application/json","x-api-key":p.key,
      "anthropic-version":PRO_API_VERSION,"anthropic-dangerous-direct-browser-access":"true"},
      body:JSON.stringify({model:PRO_MODEL,max_tokens:1500,system:q.system,messages:[{role:"user",content:q.user}]})});
    if(!r.ok)throw new Error(r.status===401?"The Claude API key was not accepted.":`Claude answered with error ${r.status}.`);
    const d=await r.json();return parseJSON((d.content||[]).filter(b=>b.type==="text").map(b=>b.text).join(""));
  }catch(e){if(e.name==="AbortError")throw new Error("Zulu Pro took too long to answer. Check the internet connection.");
    if(e instanceof TypeError)throw new Error("Zulu Pro could not connect. Check the internet connection. This preview page cannot connect, but the apps and website can.");throw e}
  finally{clearTimeout(timer)}
}
let planBusy=false;
async function makeProPlan(){
  if(planBusy)return;planBusy=true;render();say(`Let me think about the best plan for you, ${NAME}.`,{mood:"think"});
  try{S.proPlan=cleanPlan(await askPro(planRequest()));save();planBusy=false;render();
    const pl=S.proPlan;say(pl.message,{voice:false,mood:"happy"});speak([pl.message,...pl.steps.map((st,i)=>`Step ${i+1}. ${st.why}`)])}
  catch(e){planBusy=false;render();toast(e.message);say(`I will use my own plan for now, ${NAME}.`)}
}
async function proMistake(target,attempt){
  if(!proOn()||!attempt)return;
  const key=target+"|"+attempt;S.proTips=S.proTips||{};
  try{let tip=S.proTips[key];
    if(!tip){const r=await askPro({kind:"tip",level:LEVEL,target:scrub(target),attempt:scrub(attempt)});tip=String(r.tip||"").slice(0,300);if(!tip)return;S.proTips[key]=tip;save()}
    const fb=document.querySelector("#view .feedback");if(fb&&game&&cur()===target){fb.insertAdjacentHTML("beforeend",`<p class="protip">✨ ${esc(tip)}</p>`);speak(tip,{cancel:false})}
  }catch(e){}
}
function runStep(st){
  const ws=st.words.filter(x=>words().includes(x));const list=ws.length?ws:words();
  if(st.activity==="learn"){learnIdx=Math.max(0,words().indexOf(list[0]));go("learn");speak(st.why);return}
  if(st.activity==="writing"&&typeof WR!=="undefined"){WR.mode="words";WR.word=list[0];go("writing");sayLetters(list[0]);return}
  if(st.activity==="revision"){go("revision");startGame("bee",words(),{rev:true,week:usingExamples()?null:WK});game.title="📝 Revision Test";render();return}
  go("games");startGame(st.activity,list);
}
function planCard(){
  const pl=currentPlan(),on=proOn();
  return `<div class="plan"><div class="plan-h"><h3>🤖 Zulu's plan for today</h3><span class="src ${pl.source}">${pl.source==="pro"?"✨ Made by Zulu Pro":"Zulu's own plan"}</span></div>
    <p>${esc(pl.message)}</p>
    <ol class="steps">${pl.steps.map((st,i)=>{const a=ACT[st.activity]||["⭐",st.activity],ws=st.words.filter(x=>words().includes(x));
      return `<li><div class="st-main"><b>${a[0]} ${a[1]}</b><span>${esc(st.why)}</span>${ws.length&&st.activity!=="revision"?`<small>${ws.map(esc).join(" · ")}</small>`:""}</div>
      <button class="btn" style="--c:var(--leaf)" data-step="${i}">▶ Start</button></li>`}).join("")}</ol>
    <div class="row">${on?`<button class="btn" style="--c:var(--grape)" id="proPlan" ${planBusy?"disabled":""}>${planBusy?"✨ Zulu is thinking…":"✨ Ask Zulu Pro for a new plan"}</button>`
      :`<span class="hint">Switch on Zulu 1 Pro in Beryl's corner for plans made by AI.</span>`}
    <button class="btn ghost" id="hearPlan">🔊 Hear the plan</button></div></div>`;
}
function bindPlan(){
  const pl=currentPlan();
  document.querySelectorAll("[data-step]").forEach(b=>b.onclick=()=>runStep(pl.steps[+b.dataset.step]));
  const pp=$("#proPlan");if(pp)pp.onclick=makeProPlan;
  $("#hearPlan").onclick=()=>speak([pl.message,...pl.steps.map((st,i)=>`Step ${i+1}. ${st.why}`)]);
}
function proCard(){const p=pro();
  return `<div class="trick" style="--c:var(--grape)"><h3>🤖 Zulu 1 Pro</h3>
    <p>Zulu 1 Pro uses AI (Claude, by Anthropic) to plan each practice session, write new memory tricks, and explain spelling mistakes.</p>
    <p class="hint"><b>Privacy:</b> Pro sends only the spelling words, how often each was right or wrong, and a misspelt attempt when explaining a mistake. Names, ages, voices and handwriting never leave this device.</p>
    <div class="set"><label for="proMode">Connect using</label><select id="proMode" class="field">
      <option value="off" ${p.mode==="off"?"selected":""}>Off</option><option value="service" ${p.mode==="service"?"selected":""}>Zulu 1 Pro service (recommended)</option>
      <option value="key" ${p.mode==="key"?"selected":""}>My own Claude API key</option></select></div>
    <div class="set" data-pm="service" ${p.mode==="service"?"":"hidden"}><label for="proUrl">Service address</label><input id="proUrl" class="field" inputmode="url" placeholder="https://zulu1-pro.yourname.workers.dev" value="${esc(p.url)}">
      <label for="proCode">Access code</label><input id="proCode" class="field" type="password" autocomplete="off" value="${esc(p.code)}"></div>
    <div class="set" data-pm="key" ${p.mode==="key"?"":"hidden"}><label for="proKey">Claude API key</label><input id="proKey" class="field" type="password" autocomplete="off" placeholder="sk-ant-…" value="${esc(p.key)}">
      <p class="hint">The key is kept only on this device. Anyone who uses this device could find it, so the Pro service is safer for a shared tablet.</p></div>
    <div class="row"><button class="btn" style="--c:var(--grape)" id="proSave">Save Pro settings</button><button class="btn ghost" id="proTest">Test connection</button></div>
    <div id="proMsg" aria-live="polite"></div></div>`}
function bindProCard(){
  const sel=$("#proMode");if(!sel)return;
  sel.onchange=()=>document.querySelectorAll("[data-pm]").forEach(d=>d.hidden=d.dataset.pm!==sel.value);
  const read=()=>{const p=pro();p.mode=sel.value;p.url=$("#proUrl").value.trim();p.code=$("#proCode").value;p.key=$("#proKey").value.trim();save()};
  $("#proSave").onclick=()=>{read();render();toast(proOn()?"Zulu 1 Pro is on":"Zulu 1 Pro is off")};
  $("#proTest").onclick=async()=>{read();const m=$("#proMsg");
    if(!proOn()){m.innerHTML=`<div class="feedback bad">Choose how to connect and fill in the details first.</div>`;return}
    m.innerHTML=`<p class="hint">Testing…</p>`;
    try{const r=await askPro({kind:"tip",level:LEVEL,target:"because",attempt:"becuase"});
      m.innerHTML=`<div class="feedback good">✅ Connected. Zulu Pro says: ${esc(r.tip||"")}</div>`}
    catch(e){m.innerHTML=`<div class="feedback bad">${esc(e.message)}</div>`}};
}
'''
rep('/* ---------- game engine ---------- */', PRO_JS + '\n/* ---------- game engine ---------- */')

# home: plan card
rep('''    ${isRev?`<div class="example">📚 It is revision time!''', '''    ${planCard()}
    ${isRev?`<div class="example">📚 It is revision time!''')
rep('''  home:common,''', '''  home(){common();bindPlan()},''')
# render: pro badge
rep('''  $("#starCount").textContent=S.stars;
  const V=''', '''  $("#starCount").textContent=S.stars;
  const pb=$("#proBadge");if(pb)pb.hidden=!proOn();
  const V=''')
# learn: AI memory trick
rep('''<h3>🧠 Memory tricks</h3>${tricks(word).map(t=>`<p>${t}</p>`).join("")}''',
    '''<h3>🧠 Memory tricks</h3>${S.proPlan&&S.proPlan.tricks&&S.proPlan.tricks[word]?`<p class="protip">✨ ${esc(S.proPlan.tricks[word])}</p>`:""}${tricks(word).map(t=>`<p>${t}</p>`).join("")}''')
# mistakes: AI explanation after the second try
rep('''      speak([readback,`Good try. The word ${w} is spelled ${spellOut(w)}.`,pe]);''',
    '''      speak([readback,`Good try. The word ${w} is spelled ${spellOut(w)}.`,pe]);
      setTimeout(()=>proMistake(w,a),50);''')
# Beryl: Pro card
rep('''    <div class="trick" style="--c:var(--sea)"><h3>🎙️ Voice samples</h3>''', '''    ${proCard()}
    <div class="trick" style="--c:var(--sea)"><h3>🎙️ Voice samples</h3>''')
rep('''  beryl(){common();''', '''  beryl(){common();bindProCard();''')
# help
rep('''      <div class="trick" style="--c:var(--rose)"><h3>Sound tip</h3>''',
    '''      <div class="trick" style="--c:var(--grape)"><h3>🤖 Zulu's plan</h3><p>Home shows Zulu's plan for today: the words that need most practice and the games to play. Tap <b>Start</b> on each step. With Zulu 1 Pro switched on, the plan is made by AI.</p></div>
      <div class="trick" style="--c:var(--rose)"><h3>Sound tip</h3>''')
# styles
rep('/* Radio signature call */', '''.probadge{display:inline-block;vertical-align:middle;font-size:.45em;letter-spacing:.08em;padding:2px 10px;border-radius:999px;background:var(--grape);color:#fff;-webkit-text-fill-color:#fff}
.plan{border:3px solid var(--grape);border-radius:20px;padding:14px;display:flex;flex-direction:column;gap:10px;background:color-mix(in srgb,var(--grape) 7%,var(--surface))}
.plan-h{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.plan-h h3{color:var(--grape)}
.src{font-size:.85rem;font-weight:700;border-radius:999px;padding:3px 10px;background:var(--line)}
.src.pro{background:var(--grape);color:#fff}
.steps{margin:0;padding-left:1.4em;display:flex;flex-direction:column;gap:10px}
.steps li{padding-left:4px}
.steps li>*{vertical-align:middle}
.steps li{display:list-item}
.steps li .st-main{display:inline-flex;flex-direction:column;gap:2px;max-width:calc(100% - 110px);min-width:0;margin-right:8px}
.steps li .st-main small{color:var(--muted);font-weight:700;overflow-wrap:anywhere}
.steps li .btn{font-size:1rem;padding:8px 14px;float:right}
.steps li::after{content:"";display:block;clear:both}
.protip{background:color-mix(in srgb,var(--grape) 12%,var(--surface));border-radius:12px;padding:8px 12px;margin-top:6px}
/* Radio signature call */''')
open(page, "w", encoding="utf-8").write(s)
print("ok")
