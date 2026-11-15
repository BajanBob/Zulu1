# Zulu 1 Pro service

A small server that lets the Zulu 1 tutors use Claude (by Anthropic) without putting an API key on children's devices.

## What it accepts

Only these, and it drops everything else:

- a plan request: the learner's level (for example "Year 7 or 8"), the list of activities, and each spelling word with how many times it was right and wrong;
- a tip request: one spelling word and the child's misspelt attempt.

The apps remove the student's name from everything before sending. Nothing is stored on the server.

## Set it up (about 10 minutes, free Cloudflare account)

1. Create a Claude API key at https://platform.claude.com and add some credit.
2. Create a free Cloudflare account at https://dash.cloudflare.com.
3. On a computer with Node.js, open this `server` folder in a terminal and run:

   ```
   npx wrangler login
   npx wrangler secret put ANTHROPIC_API_KEY
   npx wrangler secret put ZULU_ACCESS_CODE
   npx wrangler deploy
   ```

   Paste your Claude API key, then choose an access code (any password you like).
4. Wrangler prints the service address, for example `https://zulu1-pro.yourname.workers.dev`.
5. In each tutor, open **Beryl's corner > Zulu 1 Pro**, choose **Zulu 1 Pro service**, enter the address and access code, then tap **Test connection**.

## Cost

Each plan or tip is one short request to `claude-haiku-5-5`, Anthropic's fastest, lowest-cost model.
To use a different model, set the `ZULU_MODEL` variable in `wrangler.toml`.
