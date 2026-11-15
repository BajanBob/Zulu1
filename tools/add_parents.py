"""Add a gentle, research-based note for grown-ups in Beryl's corner, and a pencil-and-paper break reminder."""
import sys
p = sys.argv[1]
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, ("count", s.count(a), a[:90])
    s = s.replace(a, b)


NOTE = r'''
    <details class="grownups">
      <summary><b>🌱 A quiet word for grown-ups</b><span class="hint"> · screens, handwriting and learning</span></summary>
      <div class="gu">
        <p>Zulu is here to help, but the best learning still happens with a pencil in hand and a grown-up close by. Here is what the research says, gently put.</p>
        <h4>✏️ Writing by hand helps letters stick</h4>
        <p>In a French study, children aged 3 to 5 copied letters for three weeks, either by hand or on a keyboard. The older children who wrote by hand recognised the letters better afterwards (<a href="https://doi.org/10.1016/j.actpsy.2004.10.019" target="_blank" rel="noopener">Longcamp and colleagues, 2005</a>). In brain scans of 4 and 5 year olds, practising letters by hand, more than typing or tracing, engaged the brain areas used later for reading (<a href="https://doi.org/10.1016/j.tine.2012.08.001" target="_blank" rel="noopener">James and Engelhardt, 2012</a>). A Norwegian study found wider brain activity when young adults wrote by hand than when they typed (<a href="https://doi.org/10.3389/fpsyg.2023.1219945" target="_blank" rel="noopener">Van der Weel and Van der Meer, 2024</a>), although other researchers have questioned how far that result goes (<a href="https://doi.org/10.3389/fpsyg.2024.1517235" target="_blank" rel="noopener">Pinet and Longcamp, 2025</a>).</p>
        <h4>⏳ How much screen time</h4>
        <p>The World Health Organization advises no sitting screen time for 1 year olds, and no more than 1 hour a day for children aged 2 to 4, with "less is better". It encourages reading and storytelling with a grown-up instead (<a href="https://www.who.int/news/item/24-04-2019-to-grow-up-healthy-children-need-to-sit-less-and-play-more" target="_blank" rel="noopener">WHO, 2019</a>). A Canadian study of 2,441 children found that more screen time at ages 2 and 3 went with lower scores on development checks at ages 3 and 5. The differences were small on average, but they appeared after the screen time, not before it (<a href="https://doi.org/10.1001/jamapediatrics.2018.5056" target="_blank" rel="noopener">Madigan and colleagues, 2019</a>).</p>
        <h4>🎁 Why slower learning can feel dull</h4>
        <p>Many children's apps are built to hold attention. A study of apps used by 3 to 5 year olds found that four in five used tricks to keep children playing, such as stickers and trophies for coming back. Parents said children often refused to hand the device back at dinner or bedtime (<a href="https://doi.org/10.1001/jamanetworkopen.2022.1764" target="_blank" rel="noopener">Radesky and colleagues, 2022</a>). After a stream of quick rewards, a book or a page of handwriting can seem slow. Zulu gives stars too, so keep sessions short and let the real prize be your praise.</p>
        <h4>📱 Older children and phones</h4>
        <p>In the 2022 international PISA tests of 15 year olds, 65% said they were distracted by digital devices in at least some maths lessons. Those distracted by classmates' devices scored 15 points lower in maths. Students who used devices for fun at school for up to an hour a day scored 49 points higher than those who used them for 5 to 7 hours (<a href="https://www.oecd.org/en/about/news/press-releases/2023/12/decline-in-educational-performance-only-partly-attributable-to-the-covid-19-pandemic.html" target="_blank" rel="noopener">OECD, 2023</a>).</p>
        <h4>💛 Small things that help</h4>
        <ul>
          <li>Keep each Zulu session to about 10 to 15 minutes. Zulu will suggest a pencil-and-paper break.</li>
          <li>After tracing a letter here, write it three times on paper with a real pencil.</li>
          <li>Sit together when you can. Say the words aloud and talk about what they mean.</li>
          <li>Read a book together every day. It counts for more than any app.</li>
          <li>Praise effort, not just stars: "You kept trying. That is how you learn."</li>
        </ul>
        <p class="hint">This is general information from published research, not medical advice. Every child is different. If you are worried about your child's development, speak to their teacher or doctor.</p>
      </div>
    </details>'''
rep('''    <p class="hint">Settings for Granny Beryl. Set the treat, choose the voice, and pick revision day.</p>''',
    '''    <p class="hint">Settings for Granny Beryl. Set the treat, choose the voice, and pick revision day.</p>''' + NOTE)

# pencil-and-paper break reminder (setting in Beryl's corner)
rep('''      <div class="set"><span class="switch"><input type="checkbox" id="echo"''',
    '''      <div class="set"><label for="breakMin">Suggest a pencil-and-paper break after</label><select id="breakMin" class="field">${[0,10,15,20,30].map(m=>`<option value="${m}" ${(S.settings.breakMin??15)==m?"selected":""}>${m?m+" minutes":"Never"}</option>`).join("")}</select></div>
      <div class="set"><span class="switch"><input type="checkbox" id="echo"''')
rep('''S.settings.echo=$("#echo").checked;save();render();toast("Settings saved")};''',
    '''S.settings.echo=$("#echo").checked;S.settings.breakMin=+$("#breakMin").value;save();render();toast("Settings saved")};''')
rep('''$("#radioBtn").dataset.next="start";''', '''$("#radioBtn").dataset.next="start";
/* After a while on screen, Zulu suggests switching to pencil and paper. */
let sessionStart=Date.now(),breakSaid=false;
setInterval(()=>{const m=S.settings.breakMin??15;if(!m||breakSaid||document.hidden||!$("#radio").hidden)return;
  if(Date.now()-sessionStart>=m*60000){breakSaid=true;
    say(`Super work, ${NAME}! Time for a pencil break. Write three of your words on paper, then show a grown-up.`,{mood:"happy"});
    toast("✏️ Pencil break! Write three words on paper.")}},30000);''')
rep('''if(n==="close"){$("#radio").hidden=true;''', '''if(n==="close"){$("#radio").hidden=true;sessionStart=Date.now();breakSaid=false;''')

# writing: nudge to paper after a good tracing
rep('''$("#wfb").innerHTML=`<div class="feedback good">⭐ Beautiful ${esc(L())}! ${pr}</div>`;''',
    '''$("#wfb").innerHTML=`<div class="feedback good">⭐ Beautiful ${esc(L())}! ${pr}<br>Now write it three times on paper with a pencil. ✏️</div>`;''')

rep('/* Radio signature call */', '''.grownups{border:3px solid var(--leaf);border-radius:18px;padding:12px 16px;background:color-mix(in srgb,var(--leaf) 8%,var(--surface))}
.grownups summary{cursor:pointer;font-size:1.05rem}
.gu{display:flex;flex-direction:column;gap:10px;margin-top:10px;max-width:68ch}
.gu h4{margin:6px 0 0;font-family:var(--display);font-size:1.1rem;color:color-mix(in srgb,var(--leaf) 70%,var(--ink))}
.gu ul{margin:0;padding-left:1.2em;display:flex;flex-direction:column;gap:4px}
.gu a{color:var(--sky)}
/* Radio signature call */''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
