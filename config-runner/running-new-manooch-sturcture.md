Here is your **clean, corrected, and properly structured prompt for Claude** — clearer, more professional, and with the fixes you requested:

---

# ✅ Prompt for Claude

## Context

I have a **monorepo** with multiple frontend apps inside the `manooch-deps` directory.

I downloaded `ngrok.exe`, and it is currently located at:

```
C:\Users\PC-Kosar\Downloads\ngrok.exe
```

My:

- **ngrok Authtoken:**  
  `36qQKSps4oq9oYMXjIRgipgSgPA_YXQWXp2gpQkaoyPZ25PE`

- **ngrok static domain:**  
  `proctodaeal-zofia-symbiotically.ngrok-free.dev`

Reference setup page:  
https://dashboard.ngrok.com/get-started/setup/windows

---

# Problems to Solve

⚠️ **Important:**  
Before executing anything, create a structured plan.  
Break the work into phases and explain your approach briefly.  
Then proceed step-by-step.

---

## ✅ Problem 1 — Fix ngrok PATH & Environment Variables

Currently I must run ngrok like this:

```
C:\Users\PC-Kosar\Downloads\ngrok.exe http --url=proctodaeal-zofia-symbiotically.ngrok-free.dev
```

I want to be able to run it globally like this:

```
ngrok http --url=proctodaeal-zofia-symbiotically.ngrok-free.dev
```

### Tasks:

1. Tell me the proper permanent folder to move `ngrok.exe` into.
2. Give exact step-by-step instructions to correctly add it to Windows System `PATH`.
3. Provide the command to authenticate ngrok using my Authtoken.
4. Verify the installation.

---

## ✅ Problem 2 — Add Separate `ngrok` Commands to Each Frontend App

Inside each frontend app (inside `manooch-deps`), I want:

- A **separate `ngrok` command per app**
- Similar structure to how the root `package.json` manages scripts
- Each frontend app should expose its own local port using the static domain

When inside a frontend app, I want to run:

```
npm run ngrok
```

and have it expose that specific frontend app.

### Requirements:

- Each app must have its own `ngrok` script.
- Commands must not conflict with each other.
- Structure should be clean and scalable.
- If needed, suggest dynamic ports or environment-based configuration.

---

## ✅ Problem 3 — Improve Monorepo Management (`manooch-deps`)

The old frontend commands are no longer useful.

Recommend a better command structure for:

- Running all frontend apps together
- Running a single app
- Running all ngrok tunnels together
- Stopping everything cleanly
- Checking status
- Better development workflow overall

You may suggest:

- npm workspaces
- turbo
- concurrently
- custom CLI scripts
- or any better architecture

Design this like you are improving a production-ready monorepo.

---

# How You Should Work

1. First: Present a structured execution plan.
2. Then: Solve each problem phase-by-phase.
3. If you need to see any file (like `package.json`), ask for it.
4. You are responsible for the architecture decisions — optimize for clarity, scalability, and developer experience.

---

✅ This version is clean, structured, and gives Claude authority to self-plan while keeping your requirements precise.