# Data Model: RAG Chatbot for Physical AI & Humanoid Robotics Textbook

## Entities

### TextbookContent
- id: UUID
- title: String
- content: Text (the actual textbook content)
- chapter: String
- section: String
- embeddings: Vector (for similarity search in Qdrant)
- metadata: JSON (additional information about the content)

### UserQuery
- id: UUID
- userId: UUID (optional, for registered users)
- sessionId: UUID
- queryText: String
- timestamp: DateTime
- source: String (web, mobile, etc.)

### ChatbotResponse
- id: UUID
- queryId: UUID (links to UserQuery)
- responseText: String
- sourceChunks: UUID[] (links to TextbookContent chunks used)
- confidence: Float (confidence level of response)
- timestamp: DateTime

### UserInteractionLog
- id: UUID
- userId: UUID
- queryId: UUID (links to UserQuery)
- responseId: UUID (links to ChatbotResponse)
- rating: Integer (optional, user rating of response)
- feedback: String (optional, user feedback)
- timestamp: DateTime

## Relationships

- UserQuery is linked to ChatbotResponse (one-to-one)
- ChatbotResponse references multiple TextbookContent chunks (many-to-many)
- UserInteractionLog links User, Query, and Response (many-to-one relationships)

## Validation Rules

- TextbookContent must not be empty
- UserQuery.queryText must be between 1 and 1000 characters
- ChatbotResponse confidence must be between 0 and 1
- UserInteractionLog rating must be between 1 and 5 if provided
