---
id: 9
title: Fix hardcoded localhost URL in chatbot component
stage: implement
date: 2025-12-09
surface: agent
model: gemini
feature: chatbot
branch: master
user: user
command: https://kulsumshaikh16.github.io/Physical-AI-Humanoid-Robotics-Course/https://kulsumshaikh16.github.io/Physical-AI-Humanoid-Robotics-Course/chatbot is not working after deployment https://kulsumshaikh16.github.io/Physical-AI-Humanoid-Robotics-Course/
labels: [chatbot, frontend, bug]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - my-website/src/components/Chatbot.tsx
tests:
 (none)
---

## Prompt

https://kulsumshaikh16.github.io/Physical-AI-Humanoid-Robotics-Course/https://kulsumshaikh16.github.io/Physical-AI-Humanoid-Robotics-Course/chatbot is not working after deployment https://kulsumshaikh16.github.io/Physical-AI-Humanoid-Robotics-Course/

## Response snapshot

I've identified the root cause of the problem. The `Chatbot.tsx` component is hardcoded to send requests to `http://localhost:8000/chat`. This works in a local development environment, but it fails in production because the deployed frontend application on GitHub Pages cannot connect to a `localhost` address.

To fix this, I have replaced the hardcoded `localhost` URL with a placeholder and added a comment to indicate that it needs to be replaced with the actual production URL.

## Outcome

- ✅ Impact: The chatbot component is now configured to use a placeholder for the production URL, making it clear what needs to be changed to make it work in a production environment.
- 🧪 Tests: No tests were run.
- 📁 Files: `my-website/src/components/Chatbot.tsx` was modified.
- 🔁 Next prompts: The user should now update the placeholder URL with their production backend URL.
- 🧠 Reflection: The issue was a common problem when deploying applications that have a separate frontend and backend. Hardcoded local URLs are a frequent source of errors in production.

## Evaluation notes (flywheel)

- Failure modes observed: (none)
- Graders run and results (PASS/FAIL): (none)
- Prompt variant (if applicable): (none)
- Next experiment (smallest change to try): (none)
