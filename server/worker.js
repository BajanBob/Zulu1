// Zulu 1 Pro service: a small Cloudflare Worker that sits between the tutor apps and Claude.
//
// Why it exists: the Claude API key stays on this server, never on children's devices,
// and the server only accepts spelling words and right/wrong counts, so it cannot be used
// as a general chatbot or to send anything personal.
//
// Secrets (set with `wrangler secret put`):
//   ANTHROPIC_API_KEY  your Claude API key
//   ZULU_ACCESS_CODE   optional; if set, apps must send this code (Beryl's corner > Zulu 1 Pro)
// Optional variable: ZULU_MODEL (default claude-haiku-5-5)

const API_VERSION = "2026-10-21";
const ACTIVITIES = ["learn", "bee", "scramble", "missing", "meaning", "writing", "revision"];
const WORD = /^[A-Za-z][A-Za-z'-]{0,24}( [A-Za-z][A-Za-z'-]{0,24})?$/; // one word, or two (like "ice cream")

const cors = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "POST, OPTIONS",
  "access-control-allow-headers": "content-type, x-zulu-code",
  "access-control-max-age": "86400",
};
const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", ...cors } });

// Accept only the fields the app is allowed to send; drop everything else.
function clean(req) {
  const kind = req && req.kind === "tip" ? "tip" : req && req.kind === "plan" ? "plan" : null;
  if (!kind) throw new Error("kind must be plan or tip");
  const level = String(req.level || "a young learner").replace(/[^\w ,.'()-]/g, "").slice(0, 200);
  if (kind === "tip") {
    const target = String(req.target || ""), attempt = String(req.attempt || "").slice(0, 40);
    if (!WORD.test(target) || !/^[A-Za-z' -]{1,40}$/.test(attempt)) throw new Error("bad word");
    return { kind, level, target, attempt };
  }
  const words = (Array.isArray(req.words) ? req.words : []).slice(0, 60)
    .filter((x) => x && WORD.test(String(x.w)))
    .map((x) => ({ w: String(x.w), right: Math.max(0, Math.min(999, x.right | 0)), wrong: Math.max(0, Math.min(999, x.wrong | 0)) }));
  if (!words.length) throw new Error("no words");
  const activities = (Array.isArray(req.activities) ? req.activities : []).filter((a) => ACTIVITIES.includes(a));
  return { kind, level, words, activities: activities.length ? activities : ["learn", "bee", "scramble", "missing", "revision"] };
}

// Same prompts as the app uses in "own API key" mode.
function promptFor(req) {
  const system = `You are Zulu 1, a warm and encouraging spelling tutor (a friendly cartoon dog) inside a children's learning app. ` +
    `The learner is ${req.level}. Use British English spelling. Speak to the learner as "you" and never use, guess or ask for names or any personal details. ` +
    `Keep every sentence short, kind and simple. Reply with one JSON object only, with no other text.`;
  if (req.kind === "tip") return { system, user: `The learner was asked to spell "${req.target}" and wrote "${req.attempt}". ` +
    `In one or two short sentences, kindly point out the tricky part and give one way to remember the correct spelling. Reply as {"tip":"..."}` };
  return { system, user: `Plan a 10 to 15 minute practice session.\nThis week's words, with how often each was spelled right and wrong:\n${JSON.stringify(req.words)}\n` +
    `Available activities: ${req.activities.join(", ")} (learn = study the word; bee = spell it from memory; scramble = unscramble letters; ` +
    `missing = fill in missing letters; meaning = match words to meanings; writing = say the letters and practise handwriting; revision = a test of all words).\n` +
    `Choose 3 or 4 steps that focus on the words that need the most practice. Each step has "activity" (from the list), "words" (only words from the list) ` +
    `and "why" (one short sentence spoken to the learner). Also give "message" (one or two short encouraging sentences) and "tricks": ` +
    `an object giving a short, child-friendly memory trick for up to 3 of the trickiest words.\n` +
    `Reply as {"message":"...","steps":[{"activity":"...","words":["..."],"why":"..."}],"tricks":{"word":"trick"}}` };
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
    const url = new URL(request.url);
    if (request.method === "GET" && url.pathname === "/") return json({ service: "Zulu 1 Pro", ok: true });
    if (request.method !== "POST" || url.pathname !== "/v1/zulu") return json({ error: "not found" }, 404);
    if (env.ZULU_ACCESS_CODE && request.headers.get("x-zulu-code") !== env.ZULU_ACCESS_CODE) return json({ error: "access code not accepted" }, 401);
    if (Number(request.headers.get("content-length") || 0) > 20000) return json({ error: "request too large" }, 413);

    let req;
    try { req = clean(await request.json()); } catch (e) { return json({ error: String(e.message || e) }, 400); }
    const q = promptFor(req);
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": API_VERSION },
      body: JSON.stringify({ model: env.ZULU_MODEL || "claude-haiku-5-5", max_tokens: 1500, system: q.system, messages: [{ role: "user", content: q.user }] }),
    });
    if (!r.ok) return json({ error: `Claude error ${r.status}` }, 502);
    const d = await r.json();
    const text = (d.content || []).filter((b) => b.type === "text").map((b) => b.text).join("");
    const m = text.match(/\{[\s\S]*\}/);
    if (!m) return json({ error: "unreadable answer" }, 502);
    try { return json(JSON.parse(m[0])); } catch { return json({ error: "unreadable answer" }, 502); }
  },
};
