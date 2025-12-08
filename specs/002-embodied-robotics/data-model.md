
*   **Description**: Represents a user who can log in and personalize content.
*   **Fields**:
    *   `id` (UUID/Integer): Unique identifier for the user.
    *   `username` (String): Unique username for login.
    *   `email` (String): Unique email address.
    *   `password_hash` (String): Hashed password for security.
    *   `preferences` (JSON Object): Stores personalization settings (e.g., `{"hardware_background": "advanced", "software_background": "beginner"}`).
    *   `last_login_date` (DateTime): Timestamp of the last login.
*   **Relationships**:
    *   One-to-many with `PersonalizedChapter` (A user can have many personalized chapters).
    *   One-to-many with `ChatbotQuery` (A user can submit many chatbot queries).
*   **Validation**:
    *   `username`: Unique, minimum 3 characters.
    *   `email`: Unique, valid email format.
    *   `password_hash`: Securely stored.

### Module

*   **Description**: Represents a thematic module within the textbook.
*   **Fields**:
    *   `id` (UUID/Integer): Unique identifier for the module.
    *   `title` (String): Title of the module (e.g., "The Robotic Nervous System (ROS 2)").
    *   `description` (Text): Brief description of the module's content.
    *   `order_in_book` (Integer): Order of the module in the overall textbook structure.
*   **Relationships**:
    *   One-to-many with `Chapter` (A module contains many chapters).
*   **Validation**:
    *   `title`: Non-empty.
    *   `order_in_book`: Unique, positive integer.

### Chapter

*   **Description**: Represents a chapter within a module, containing core content.
*   **Fields**:
    *   `id` (UUID/Integer): Unique identifier for the chapter.
    *   `module_id` (UUID/Integer): Foreign key referencing the `Module` it belongs to.
    *   `title` (String): Title of the chapter.
    *   `content_en` (Text): The original English content of the chapter.
    *   `order_in_module` (Integer): Order of the chapter within its module.
*   **Relationships**:
    *   Many-to-one with `Module` (A chapter belongs to one module).
    *   One-to-many with `PersonalizedChapter` (A chapter can have many personalized versions).
    *   One-to-many with `Translation` (A chapter can have many translations).
*   **Validation**:
    *   `title`: Non-empty.
    *   `content_en`: Non-empty.
    *   `order_in_module`: Unique within its `module_id`, positive integer.

### PersonalizedChapter

*   **Description**: Stores personalized versions of chapters for specific users.
*   **Fields**:
    *   `id` (UUID/Integer): Unique identifier for the personalized chapter.
    *   `user_id` (UUID/Integer): Foreign key referencing the `User` who personalized it.
    *   `chapter_id` (UUID/Integer): Foreign key referencing the original `Chapter`.
    *   `personalized_content` (Text): AI-generated content tailored to the user's `preferences`.
    *   `last_personalized_date` (DateTime): Timestamp of the last personalization.
*   **Relationships**:
    *   Many-to-one with `User` (A personalized chapter belongs to one user).
    *   Many-to-one with `Chapter` (A personalized chapter is based on one original chapter).
*   **Validation**:
    *   `user_id`, `chapter_id`: Unique combination.
    *   `personalized_content`: Non-empty.

### Translation

*   **Description**: Stores translated versions of chapters.
*   **Fields**:
    *   `id` (UUID/Integer): Unique identifier for the translation.
    *   `chapter_id` (UUID/Integer): Foreign key referencing the original `Chapter`.
    *   `language_code` (String): ISO 639-1 code for the target language (e.g., 'ur' for Urdu).
    *   `translated_content` (Text): The content of the chapter in the target language.
    *   `last_translated_date` (DateTime): Timestamp of the last translation.
*   **Relationships**:
    *   Many-to-one with `Chapter` (A translation is for one original chapter).
*   **Validation**:
    *   `chapter_id`, `language_code`: Unique combination.
    *   `language_code`: Valid ISO 639-1 code.
    *   `translated_content`: Non-empty.

### ChatbotQuery

*   **Description**: Records user queries to the RAG chatbot and its responses.
*   **Fields**:
    *   `id` (UUID/Integer): Unique identifier for the query.
    *   `user_id` (UUID/Integer, nullable): Foreign key referencing the `User` (if logged in).
    *   `query_text` (Text): The user's input query.
    *   `response_text` (Text): The chatbot's generated response.
    *   `timestamp` (DateTime): Timestamp when the query was made.
    *   `source_references` (JSON Array of Strings): List of source document references (e.g., `["chapter-1.md", "module-2/sub-topic.md"]`).
*   **Relationships**:
    *   Many-to-one with `User` (A chatbot query can be associated with a user).
*   **Validation**:
    *   `query_text`: Non-empty.

## State Transitions

*   **Chapter Content**: Once `content_en` is set for a `Chapter`, it can be updated. This update should trigger invalidation or regeneration of associated `PersonalizedChapter` and `Translation` records, or at least mark them as outdated.
*   **User Preferences**: Changes in `User.preferences` should prompt the system to re-generate `PersonalizedChapter` content for that user, or mark existing personalized content as needing an update.
