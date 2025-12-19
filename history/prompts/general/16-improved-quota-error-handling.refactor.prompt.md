---
id: 16
title: Improved Quota Error Handling
stage: refactor
date: 2025-12-19
surface: agent
model: gemini-2.0-flash
feature: chatbot
branch: main
user: UNI-TECH
command: handle 429 error
labels:
  - error-handling
  - gemini
  - quota
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - e:\gemini-cli\ai-textbook\chatbot-service\src\services\generation.py
tests_yaml: |
  - manual test via chatbot UI
prompt_text: |
  chatbot show this error 
  [error message with 429 quota exceeded for gemini-2.0-flash]
response_text: |
  Identified that the `gemini-2.0-flash` model has a zero quota for the user's account. Improved error handling in `generation.py` to provide a cleaner message and recommended switching to `gemini-1.5-flash` in the `.env` file.
---

# Improved Quota Error Handling

The chatbot was displaying a raw API error when the Gemini quota was exceeded. This was especially prominent because the user appears to be using `gemini-2.0-flash`, which has limited availability/quota on the Free Tier for some accounts.

## Changes
- Updated `GenerationService` in `src/services/generation.py` to better detect and format quota-related errors.
- Recommended a model switch to `gemini-1.5-flash` for better stability on the Free Tier.
