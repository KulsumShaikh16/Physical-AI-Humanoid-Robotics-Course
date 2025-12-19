---
id: 17
title: Guide to Start Frontend and Backend
stage: misc
date: 2025-12-19
surface: agent
model: gemini-2.0-flash
feature: general
branch: main
user: UNI-TECH
command: start services
labels:
  - setup
  - troubleshooting
  - localhost
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - e:\gemini-cli\ai-textbook\my-website\package.json
  - e:\gemini-cli\ai-textbook\chatbot-service\src\api\main.py
tests_yaml: |
  - manual verification of localhost:3000
prompt_text: |
  [Image showing localhost:3000 connection refused]
response_text: |
  Provided instructions to start both the Docusaurus frontend (npm start) and the FastAPI backend (uvicorn).
---

# Guide to Start Frontend and Backend

The user encountered a `CONNECTION_REFUSED` error on `localhost:3000`, indicating the local servers are not running.

## Instructions provided:
1. Start Backend: `cd chatbot-service`, `uvicorn src.api.main:app --reload`
2. Start Frontend: `cd my-website`, `npm start`
