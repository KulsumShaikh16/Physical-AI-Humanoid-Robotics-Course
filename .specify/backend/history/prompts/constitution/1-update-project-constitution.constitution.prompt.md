---
id: 1
title: update-project-constitution
stage: constitution
date: 2025-12-15
surface: agent
model: gpt-4
feature: rag-chatbot-textbook
branch: 003-rag-chatbot-textbook
user: user
command: /sp.constitution
labels: [constitution,rag-chatbot,physical-ai,humanoid-robotics]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - E:\gemini-cli\ai-textbook\.specify\backend\.specify\memory\constitution.md
tests:
 - E:\gemini-cli\ai-textbook\.specify\backend\checklists\requirements.md
---

## Prompt

/sp.constitution Project: RAG Chatbot Development for Physical AI & Humanoid Robotics Textbook

Core principles:

User-centric responses: Provide relevant answers based only on the selected text from the book.

Efficiency in information retrieval: Enable rapid, accurate, and context-specific responses.

Clarity: Ensure that answers are clear, concise, and easy to understand for users with a basic to intermediate understanding of robotics and AI.

Comprehensiveness: Cover all major topics within the textbook content to ensure a robust question-answering system.

Key standards:

Data handling: Use Cohere API for embedding-based generation to facilitate context-aware responses.

Chatbot integration: The chatbot must operate seamlessly within the book on GitHub Pages, providing a user-friendly interaction experience.

Query specificity: The chatbot should only reference the selected section of the text when answering questions (no generative content beyond the provided data).

Response quality: Provide accurate, actionable answers with references back to the textbook content where applicable.

Constraints:

Tech Stack: Cohere API (for embeddings), Qwen CLI (for deployment), FastAPI (for handling API requests), Neon Serverless Postgres (for storage), Qdrant Cloud Free Tier (for vector search).

Data size: The chatbot should handle large textbook content efficiently. Ensure indexing and storage are optimized.

Language: English (primary), with support for translation features in future updates (e.g., Urdu).

Scalability: Ensure the system can handle multiple concurrent users without significant delays in response time.

Success criteria:

Accuracy: The chatbot provides correct, relevant answers based on the selected text.

Efficiency: Responses must be delivered within 3 seconds of user input.

User experience: Easy-to-use interface with clear instructions on how to ask questions and interact with the chatbot.

Integration: Seamless integration within the Docusaurus-based textbook and deployment on GitHub Pages.

Reliability: Ensure uptime of the chatbot with minimal errors during live usage.

Performance:

Throughput: Must be able to handle at least 100 simultaneous queries without degradation in response time.

Error handling: Implement a system to log errors and improve responses over time.

## Response snapshot

I have successfully updated the project constitution at `.specify/memory/constitution.md` with the following details:

- **New Version**: 1.0.0 (Initial version based on the RAG Chatbot project principles)
- **Bump Rationale**: This is the initial version of the constitution for the RAG Chatbot Development for Physical AI & Humanoid Robotics Textbook project, containing all project-specific principles.
- **Files Flagged for Manual Follow-up**: 
  - The RATIFICATION_DATE placeholder in the constitution file needs to be updated with the original adoption date by the project owner
- **Suggested Commit Message**: `docs: amend constitution to v1.0.0 (initial RAG Chatbot project principles)`

The constitution now includes:
- 6 Core Principles specific to the RAG Chatbot project
- Key Standards section with implementation details
- Constraints section with technical requirements
- Governance section with success criteria and performance metrics
- A Sync Impact Report at the top of the file

All validation checks have been passed, and the constitution aligns with the project requirements provided.

## Outcome

- ✅ Impact: Updated project constitution with RAG Chatbot-specific principles
- 🧪 Tests: Quality checklist created and validated
- 📁 Files: constitution.md updated in memory directory
- 🔁 Next prompts: /sp.plan, /sp.tasks, or /sp.specify for feature development
- 🧠 Reflection: Constitution now specifically guides development of the RAG Chatbot project

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All validation checks passed
- Prompt variant (if applicable): Standard /sp.constitution command
- Next experiment (smallest change to try): Begin feature planning with /sp.plan
