"""Let Granny Beryl change the tutor's name, the student's name, the short name and how names are spoken."""
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, ("count", s.count(a), a[:90])
    s = s.replace(a, b)


# ---- names become settings ----
rep('const NAME = "Master Shakai Stoute";',
    'const DEFAULT_NAME = "Master Shakai Stoute", DEFAULT_SHORT = "Stoute", DEFAULT_TUTOR = "Zulu 1";\n'
    'let NAME = DEFAULT_NAME, SHORT = DEFAULT_SHORT, TUTOR = DEFAULT_TUTOR;')
rep('const PRAISE = ["Stoute, you are very smart!",', 'const PRAISE_T = ["{short}, you are very smart!",')
rep('const PERSIST = ["You cannot give up!","Failure is not final.","Stoute, you must never give up!",',
    'const PERSIST_T = ["You cannot give up!","Failure is not final.","{short}, you must never give up!",')
rep('function save(){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}',
    '''function save(){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}}
/* Names chosen in Beryl's corner */
const PRAISE=[], PERSIST=[];
function applyNames(){const st=S.settings;
  NAME=(st.studentName||DEFAULT_NAME).trim();SHORT=(st.shortName||DEFAULT_SHORT).trim();TUTOR=(st.tutorName||DEFAULT_TUTOR).trim();
  PRAISE.splice(0,PRAISE.length,...PRAISE_T.map(x=>x.replace("{short}",SHORT)));
  PERSIST.splice(0,PERSIST.length,...PERSIST_T.map(x=>x.replace("{short}",SHORT)))}
applyNames();
/* Show the chosen tutor name wherever the app says "Zulu". The product name "Zulu 1 Pro" stays. */
function brand(t){t=String(t);if(TUTOR===DEFAULT_TUTOR)return t;
  return t.replace(/Zulu 1 Pro/g,"\\u0001").replace(/Zulu Pro/g,"\\u0002")
    .replace(/Zulu 1 Ham Dog/g,TUTOR).replace(/Zulu (1|one|One)\\b/g,TUTOR).replace(/\\bZulu\\b/g,TUTOR)
    .replace(/\\u0001/g,"Zulu 1 Pro").replace(/\\u0002/g,"Zulu Pro")}''')

# ---- speech: chosen names, then "say it like" spellings ----
rep('const sayable=t=>String(t).replace(/\\bShakai\\b/g,"Shah-kye").replace(/\\bStoute\\b/g,"Stowt");',
    '''const DEFAULT_SAYAS="Shakai=Shah-kye; Stoute=Stowt";
/* Beryl writes "name=how it sounds; name=how it sounds" so the voice says names properly */
function sayAs(t){(S.settings.sayAs??DEFAULT_SAYAS).split(/[;\\n]/).map(x=>x.split("=")).filter(x=>x.length===2&&x[0].trim()&&x[1].trim())
  .forEach(([a,b])=>{t=t.replace(new RegExp("\\\\b"+a.trim().replace(/[.*+?^${}()|[\\]\\\\]/g,"\\\\$&")+"\\\\b","g"),b.trim())});return t}
const sayable=t=>sayAs(brand(String(t)));''')
rep('const SAMPLE=`Hello, Master Shakai Stoute. I am Zulu one,', 'const sampleText=()=>`Hello, ${NAME}. I am Zulu one,')
s = s.replace("speak(SAMPLE,", "speak(sampleText(),").replace("sayable(SAMPLE)", "sayable(sampleText())")
assert "SAMPLE" not in s

# ---- everything shown on screen uses the chosen names ----
rep('const panel=(c,title,body,extra="")=>`<section', 'const panel=(c,title,body,extra="")=>brand(`<section')
rep('<header><h2>${title}</h2>${extra}</header>${body}</section>`;', '<header><h2>${title}</h2>${extra}</header>${body}</section>`);')
rep('function say(text,{voice=true,mood}={}){$("#bubble").textContent=text;', 'function say(text,{voice=true,mood}={}){$("#bubble").textContent=brand(text);')
rep('function toast(t){const el=$("#toast");el.textContent=t;', 'function toast(t){const el=$("#toast");el.textContent=brand(t);')
rep('<small>Personal tutor of Master Shakai Stoute</small><h1>Zulu 1 Ham Dog Tutor <span',
    '<small id="tutorOf">Personal tutor of Master Shakai Stoute</small><h1><span id="appName">Zulu 1 Ham Dog Tutor</span> <span')
rep('Say each letter as Stoute types</label>', 'Say each letter as ${esc(SHORT)} types</label>')
rep('''confirmBox("Reset Stoute's stars to zero?",''', '''confirmBox(`Reset ${esc(SHORT)}'s stars to zero?`,''')
rep('''Morse code call sign, Z U L U 1, and "This is Zulu one calling Master Shakai Stoute".''',
    '''Morse code call sign, ${SIG.split("").join(" ")}, and "This is Zulu one calling ${esc(NAME)}".''')

# ---- signature call and Morse code follow the tutor's name ----
rep('const MORSE={Z:"--..",U:"..-",L:".-..","1":".----"};\nconst SIG="ZULU 1";\n'
    '$("#morse").innerHTML=SIG.split("").map(c=>c===" "?`<span class="mch gap"></span>`:\n'
    '  `<span class="mch"><b>${c}</b><span class="sig">${MORSE[c].split("").map(s=>`<i class="${s==="."?"dot":"dash"}"></i>`).join("")}</span></span>`).join("");',
    '''const MORSE={A:".-",B:"-...",C:"-.-.",D:"-..",E:".",F:"..-.",G:"--.",H:"....",I:"..",J:".---",K:"-.-",L:".-..",M:"--",N:"-.",O:"---",P:".--.",Q:"--.-",R:".-.",
  S:"...",T:"-",U:"..-",V:"...-",W:".--",X:"-..-",Y:"-.--",Z:"--..","0":"-----","1":".----","2":"..---","3":"...--","4":"....-","5":".....","6":"-....","7":"--...","8":"---..","9":"----."};
let SIG="ZULU 1";
/* The call sign is the tutor's name in Morse code (up to 12 letters and numbers) */
function buildMorse(){SIG=TUTOR.toUpperCase().replace(/[^A-Z0-9 ]/g,"").replace(/\\s+/g," ").trim().slice(0,12).trim()||"ZULU 1";
  const m=$("#morse");m.innerHTML=SIG.split("").map(c=>c===" "?`<span class="mch gap"></span>`:
    `<span class="mch"><b>${c}</b><span class="sig">${MORSE[c].split("").map(s=>`<i class="${s==="."?"dot":"dash"}"></i>`).join("")}</span></span>`).join("");
  m.setAttribute("aria-label",`${SIG.split("").join(" ")} in Morse code`)}
/* Fixed parts of the page that show names */
function refreshNames(){$("#tutorOf").textContent=`Personal tutor of ${NAME}`;$("#appName").textContent=brand("Zulu 1 Ham Dog Tutor");
  document.title=TUTOR===DEFAULT_TUTOR?document.title:brand("Zulu 1 Ham Dog Tutor");buildMorse();
  if(!calling&&!$("#radio").hidden&&($("#radioBtn").dataset.next||"start")==="start")$("#radioTitle").textContent=`Calling ${NAME}`}''')
rep('let calling=false;', 'let calling=false;\nrefreshNames();\nsay(`Woof! Hello ${NAME}. I am Zulu 1 Ham Dog, your very own personal tutor.`,{voice:false});')
rep('''  $("#radioTitle").textContent=mode==="start"?"Zulu 1 calling...":"Zulu 1 signing off...";
  $("#radioText").textContent="Listen to the Morse code: Z U L U 1.";''',
    '''  $("#radioTitle").textContent=brand(mode==="start"?"Zulu 1 calling...":"Zulu 1 signing off...");
  $("#radioText").textContent=`Listen to the Morse code: ${SIG.split("").join(" ")}.`;''')
rep('''    const line=mode==="start"?"This is Zulu one, calling Master Shakai Stoute.":"Zulu one out.";
    $("#radioTitle").textContent=mode==="start"?"This is Zulu One calling Master Shakai Stoute":"Zulu One out";''',
    '''    const line=mode==="start"?`This is Zulu one, calling ${NAME}.`:"Zulu one out.";
    $("#radioTitle").textContent=brand(mode==="start"?`This is Zulu One calling ${NAME}`:"Zulu One out");''')
rep('''  if(mode==="start"){$("#radioTitle").textContent="Calling Master Shakai Stoute";$("#radioText").textContent="Tap the button to start today's lesson with Zulu 1.";''',
    '''  if(mode==="start"){$("#radioTitle").textContent=`Calling ${NAME}`;$("#radioText").textContent=brand("Tap the button to start today's lesson with Zulu 1.");''')

# ---- Pro: always remove the current names too ----
rep('function scrub(t){let x=String(t);NAME_PARTS.forEach(', 'function scrub(t){let x=String(t);[...NAME_PARTS,...nameParts()].forEach(')
rep('const NAME_PARTS=', 'const nameParts=()=>[TUTOR,...NAME.replace(/^(Master|Miss|Mr|Mrs|Ms)\\s+/i,"").split(/\\s+/),SHORT].filter(x=>x&&x.length>1&&x!==DEFAULT_TUTOR);\nconst NAME_PARTS=')

# ---- Beryl's corner: the Names card ----
NAMES_JS = r'''
function namesCard(){const st=S.settings;
  return `<div class="trick" style="--c:var(--coral)"><h3>📝 Names</h3>
    <div class="grid2">
      <div class="set"><label for="nmTutor">Tutor's name</label><input id="nmTutor" class="field" maxlength="24" value="${esc(TUTOR)}"><small class="hint">The Morse code call sign spells this name.</small></div>
      <div class="set"><label for="nmStudent">Student's name</label><input id="nmStudent" class="field" maxlength="40" value="${esc(NAME)}"><small class="hint">How the tutor greets them, for example "Master Shakai Stoute".</small></div>
      <div class="set"><label for="nmShort">Short name</label><input id="nmShort" class="field" maxlength="20" value="${esc(SHORT)}"><small class="hint">Used in encouragement: "${esc(SHORT)}, you are very smart!"</small></div>
      <div class="set"><label for="nmSay">How to say the names (optional)</label><input id="nmSay" class="field" maxlength="200" placeholder="Shakai=Shah-kye; Stoute=Stowt" value="${esc(st.sayAs??DEFAULT_SAYAS)}"><small class="hint">Write a name, an equals sign, then how it sounds. Separate names with ;</small></div>
    </div>
    <div class="row"><button class="btn" style="--c:var(--coral)" id="nmSave">Save names</button><button class="btn ghost" id="nmHear">🔊 Hear it</button><button class="btn ghost" id="nmReset">Back to the original names</button></div></div>`}
function bindNames(){
  if(!$("#nmSave"))return;
  const read=()=>({tutorName:$("#nmTutor").value.trim(),studentName:$("#nmStudent").value.trim(),shortName:$("#nmShort").value.trim(),sayAs:$("#nmSay").value});
  const withNames=(v,fn)=>{const old=JSON.stringify(S.settings);Object.assign(S.settings,v);applyNames();try{fn()}finally{S.settings=JSON.parse(old);applyNames()}};
  $("#nmHear").onclick=()=>withNames(read(),()=>speak([`This is ${TUTOR}, calling ${NAME}.`,PRAISE[0]]));
  $("#nmSave").onclick=()=>{const v=read();if(!v.tutorName||!v.studentName||!v.shortName){toast("Please fill in all three names.");return}
    Object.assign(S.settings,v);save();applyNames();refreshNames();render();toast("Names saved");speak(`Hello, ${NAME}. I am ${TUTOR}, your personal tutor.`)};
  $("#nmReset").onclick=()=>confirmBox("Go back to the original names?",()=>{["tutorName","studentName","shortName","sayAs"].forEach(k=>delete S.settings[k]);
    save();applyNames();refreshNames();render();toast("Original names restored")});
}
'''
rep('/* ---------- game engine ---------- */', NAMES_JS + '\n/* ---------- game engine ---------- */')
rep('    ${proCard()}\n', '    ${namesCard()}\n    ${proCard()}\n')
rep('  beryl(){common();bindProCard();', '  beryl(){common();bindProCard();bindNames();')

open(p, "w", encoding="utf-8").write(s)
print("ok")
