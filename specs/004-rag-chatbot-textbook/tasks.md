---
description: "Implementation tasks for RAG Chatbot Backend"
---

# Tasks: RAG Chatbot for Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/004-rag-chatbot-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency management.

- [ ] T001 Initialize Python project structure in `src/` <!-- id: 11 -->
- [ ] T002 Create `requirements.txt` with FastAPI, cohere, qdrant-client, psycopg2-binary, uvicorn, python-dotenv <!-- id: 12 -->
- [ ] T003 [P] Configure environment loading in `src/core/config.py` (load .env) <!-- id: 13 -->

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for database and API.

**⚠️ CRITICAL**: Must be complete before user stories to ensure data and search layers are ready.

- [ ] T004 Setup Neon Postgres connection in `src/db/neon_client.py` <!-- id: 14 -->
- [ ] T005 Setup Qdrant connection in `src/db/qdrant_client.py` <!-- id: 15 -->
- [ ] T006 Initialize FastAPI app structure in `src/api/main.py` with health checks <!-- id: 16 -->
- [ ] T007 Define Pydantic models for `TextbookContent` and `UserQuery` in `src/models/` <!-- id: 17 -->
- [ ] T008 [P] Setup logging configuration in `src/core/logging.py` <!-- id: 18 -->

**Checkpoint**: Application can connect to both databases and run a basic health check.

---

## Phase 3: User Story 1 - Ask Questions About Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Core RAG pipeline: Ingest content -> Embed -> Serve Queries.

### Implementation for User Story 1

- [ ] T009 [US1] Create ingestion service for loading textbook content in `src/services/ingestion.py` <!-- id: 19 -->
- [ ] T010 [US1] Implement Cohere embedding generation in `src/services/embedding.py` <!-- id: 20 -->
- [ ] T011 [US1] Implement vector storage logic (text to Neon, vector to Qdrant) in `src/services/storage.py` <!-- id: 21 -->
- [ ] T012 [US1] Create script to ingest initial textbook chapters `tools/ingest_textbook.py` <!-- id: 22 -->
- [ ] T013 [US1] Implement retrieval logic (search Qdrant) in `src/services/retrieval.py` <!-- id: 23 -->
- [ ] T014 [US1] Implement generation logic (LLM Response) in `src/services/generation.py` <!-- id: 24 -->
- [ ] T015 [US1] Create Chat API endpoint `POST /chat/query` in `src/api/chatbot_router.py` <!-- id: 25 -->

**Checkpoint**: User can send a POST request with a question and get a relevant text answer.

---

## Phase 4: User Story 2 - Receive Confidence Scores (Priority: P2)

**Goal**: Add confidence metrics to responses.

### Implementation for User Story 2

- [ ] T016 [US2] update `ChatbotResponse` model to include `confidence_score` <!-- id: 26 -->
- [ ] T017 [US2] Modify retrieval service to normalize and return Qdrant/Cohere similarity scores <!-- id: 27 -->
- [ ] T018 [US2] Update Chat API response to include score <!-- id: 28 -->
- [ ] T019 [US2] Add confidence threshold logic (e.g., "I'm not sure" if score < X) <!-- id: 29 -->

**Checkpoint**: API responses now include a normalized confidence score (0-1).

---

## Phase 5: User Story 3 - Review Sources (Priority: P3)

**Goal**: Transparency/Citations.

### Implementation for User Story 3

- [ ] T020 [US3] Update `TextbookContent` model to include metadata (Chapter, Section, Page) <!-- id: 30 -->
- [ ] T021 [US3] Ensure ingestion saves metadata to Qdrant payload/Neon <!-- id: 31 -->
- [ ] T022 [US3] Update retrieval service to fetch and pass metadata with chunks <!-- id: 32 -->
- [ ] T023 [US3] Update Chat API response to include list of `Source` objects <!-- id: 33 -->

**Checkpoint**: responses include a list of sources (e.g., "Chapter 3, Section 2").

---

## Phase 6: Polish & Performance

- [ ] T024 Add validation for max query length and request rate limiting <!-- id: 34 -->
- [ ] T025 Run load test script (100 concurrent requests) <!-- id: 35 -->
- [ ] T026 Verify error handling for API/DB failures <!-- id: 36 -->
