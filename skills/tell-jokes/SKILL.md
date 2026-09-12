---
name: tell-jokes
description: Tell a joke when the user asks for one, or when they seem sad, frustrated, or stressed and could use a laugh
tags: [joke, funny, laugh]
keywords: [fun, funny, laugh, cheer up, lighten the mood]
default: false
status: stable
version: v0.1.0
---

# Tell jokes

## When to use this

- The user explicitly asks for a joke.
- The user seems down, frustrated, or stressed — offer to tell one before returning to the task at hand.

## Instructions

1. If the user hasn't said which type they want, ask a follow-up question on picking dad or pun jokes, so we can pick up further instruction from References.
2. Read the matching reference file below for style and tone, then write a new joke in that style — don't copy an example verbatim.
3. Keep it short. Tell one joke unless asked for more.

## References

- `references/dad-joke.md` — groan-worthy, wholesome, plays on literal meanings. Skews toward an older audience; won't land with everyone.
- `references/pun-joke.md` — pure wordplay, a double meaning is the whole joke, no setup/punchline needed.
