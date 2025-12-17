---
id: 16
title: Lower chatbot confidence threshold
stage: implement
date: 2025-12-18
surface: agent
model: gemini-1.5-pro
feature: rag-chatbot
branch: 004-rag-chatbot-textbook
user: USER
command: diagnose and fix chatbot refusal
labels: ["rag", "confidence", "refactor"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - src/api/chatbot_router.py
tests:
  - tools/diagnose_scores.py
---

## Prompt

I'm not confident enough in the available textbook sections to answer that accurately. Could you rephrase or ask about a specific chapter?
Sources:
Chapter 1 - Historical Context (Page 45)
Preface - Introduction to Physical AI (Page 1)
Control - Inverse Kinematics (Page 88)

## Response snapshot

I've analyzed the issue where the chatbot refuses to answer despite finding relevant chapters. diagnostic tests show that for queries like "Chapter 1", the match score is around 0.23, which is below the currently hardcoded 0.25 threshold. I've prepared an implementation plan to lower this threshold and make the chatbot more helpful.

## Outcome

- ✅ Impact: Lowered confidence threshold from 0.25 to 0.15 in `src/api/chatbot_router.py`.
- 🧪 Tests: Ran `tools/diagnose_scores.py` to verify match scores for common queries.
- 📁 Files: Modified `src/api/chatbot_router.py`.
- 🔁 Next prompts: User confirmed the fix, but then reported it was still not working.
- 🧠 Reflection: The embedding scores for direct chapter queries were slightly below the initial threshold, causing unnecessary refusals.

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
