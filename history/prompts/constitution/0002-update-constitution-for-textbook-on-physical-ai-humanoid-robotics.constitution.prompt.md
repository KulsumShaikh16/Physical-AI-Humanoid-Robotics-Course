
---
id: 0002
title: Update Constitution for Textbook on Physical AI & Humanoid Robotics
stage: constitution
date: 2025-12-05
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: User
command: /sp.constitution
labels: ["governance", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
null
---

## Prompt

Constitution for the Textbook on Teaching Physical AI & Humanoid Robotics Course
Preamble

We, the contributors and stakeholders of the Textbook on Teaching Physical AI & Humanoid Robotics Course, hereby establish this Constitution to govern the creation, development, and deployment of a comprehensive educational resource. The textbook will focus on Physical AI and Humanoid Robotics, covering key concepts, techniques, and applications related to the integration of artificial intelligence in physical systems, particularly humanoid robots.

The content will be structured to facilitate learning for students with a background in robotics, artificial intelligence, and engineering. This textbook will be developed using an AI-driven, specification-based approach and will leverage technologies such as Docusaurus, Spec-Kit Plus, and Claude Code to ensure efficient, automated content creation and management.

This Constitution serves as the foundational document for all project activities, ensuring structured workflows, collaborative efficiency, and a unified approach to delivering high-quality content.

Article I: Purpose and Scope
Section 1: Purpose

The primary objective of this project is to create a comprehensive textbook on Physical AI & Humanoid Robotics using an AI-driven, specification-based approach. The textbook will be structured to provide both theoretical and practical knowledge, catering to students in undergraduate and graduate-level courses.

Section 2: Project Scope

Tools and Technologies:

Docusaurus: A static site generator for building, managing, and deploying the textbook content.

Spec-Kit Plus: A specification management tool to define structured requirements and drive the content creation process.

Claude Code: An AI platform for generating content based on predefined specifications.

Content Structure:

The content will be divided into chapters and sections, each adhering to a specific specification created in Spec-Kit Plus. Claude Code will automate content generation based on these specifications, ensuring alignment with the required educational objectives.

Article II: Roles and Responsibilities
Section 1: Content Creators

Content Generation: Content creators will leverage Claude Code to produce initial drafts based on the specifications outlined in Spec-Kit Plus.

Editing and Refinement: Content creators are responsible for editing the AI-generated drafts, ensuring clarity, coherence, and consistency with the project’s objectives and tone.

Quality Control: Content creators must ensure that all generated content aligns with the project's standards for accuracy, tone, and readability.

Section 2: Project Maintainers

Project Oversight: Maintainers will oversee the project, ensuring that all contributors follow the project guidelines and specifications.

Deployment: Maintainers will deploy the finalized content to GitHub Pages and ensure proper organization and accessibility.

Version Control: Maintainers will ensure proper version control, keeping track of all changes in the GitHub repository.

Section 3: Reviewers

Content Review: Reviewers will evaluate AI-generated and edited content for accuracy, relevance, and adherence to the specifications.

Feedback and Iteration: Reviewers will provide feedback to content creators, ensuring that content is refined and improved before finalization.

Article III: Core Principles and Standards
Section 1: Core Principles

Accuracy Through Primary Source Verification
All information in the textbook must be based on verified, credible sources, including peer-reviewed research papers and textbooks.

Clarity for an Academic Audience
The content must be clear and understandable for students in robotics, AI, and engineering. Complex concepts should be explained with clarity, using accessible language where necessary.

Reproducibility
Claims, experiments, and case studies must be traceable to verifiable sources, and practical examples must be reproducible by students.

Rigor
The textbook must maintain academic rigor, drawing from peer-reviewed articles, reputable textbooks, and technical papers, and presenting complex ideas in-depth with supporting data.

Section 2: Key Standards

Source Traceability
All factual statements, theories, and technical details must be traceable to reputable sources. At least 50% of the sources used must be peer-reviewed journals or academic textbooks.

Citation Format
All sources must be cited using APA style, both within the text (in-text citations) and in the references list at the end of the textbook.

Plagiarism Policy
A zero-tolerance policy for plagiarism will be enforced. The textbook must be free from any uncredited material, with every fact and data point fully cited.

Writing Clarity
The textbook must adhere to a Flesch-Kincaid readability grade level of 10-12, ensuring accessibility for students while maintaining academic rigor.

Article IV: Constraints

Word Count
The textbook will have a total word count between 30,000 and 50,000 words, including chapters, exercises, references, and an index.

Minimum Sources
The textbook must cite at least 50 sources, including a mix of peer-reviewed journal articles, academic books, and technical reports.

Format
The final version of the textbook must be delivered in PDF format, with embedded citations and a detailed table of contents. The document should be designed for easy navigation and academic use.

Article V: Success Criteria

Verification of Claims
All claims made in the textbook must be verified and cross-referenced with at least one reputable source.

Zero Plagiarism
The textbook will undergo a plagiarism check to ensure all content is original and properly cited.

Fact-Checking Review
A rigorous fact-checking review will ensure all technical claims, figures, and illustrations are verified against primary sources before publication.

Article VI: Workflow and Development Process
Section 1: Specification Creation

Spec-Kit Plus will be used to create detailed specifications, defining topics, subtopics, and key concepts for each chapter and section. Specifications will be updated as needed based on feedback from content creators, maintainers, and reviewers.

Section 2: AI-Powered Content Generation

Claude Code will be used to generate content based on the specifications. The content will be refined and customized to meet the needs of the textbook.

Section 3: Content Deployment

The finalized content will be structured using Docusaurus, with each chapter represented as markdown files. Once finalized, the content will be deployed to GitHub Pages for public access.

Article VII: Collaboration and Communication

Communication Channels
All discussions will take place through designated channels such as Slack, GitHub Discussions, or project-specific forums.

Contribution and Code of Conduct
All contributors must adhere to a professional code of conduct, collaborating respectfully and maintaining a positive working environment.

Article VIII: Amendments and Modifications

Amendment Process
This Constitution may be amended by a majority vote of project maintainers and contributors. Amendments will be documented in the project repository.

Continuous Improvement
Amendments will reflect changes in the project’s scope, tools, or workflows, ensuring that the Constitution remains relevant and useful.

Conclusion

By adhering to this Constitution, we commit to the creation of a high-quality, academically rigorous textbook on Physical AI & Humanoid Robotics that will provide students with the theoretical knowledge and practical tools necessary to succeed in the field. This Constitution ensures that the project remains focused, efficient, and aligned with its goals, promoting collaboration and excellence in content development.

## Response snapshot

The project constitution has been successfully updated to version 2.0.0. This is a major version bump due to the complete overhaul of the constitution's content and structure.

Manual Follow-up Required:
The following template files require manual review and potential updates to align with the new constitution:
* .specify/templates/plan-template.md
* .specify/templates/spec-template.md
* .specify/templates/tasks-template.md
* .specify/templates/commands/*.md

## Outcome

- ✅ Impact: Project constitution updated to v2.0.0.
- 🧪 Tests: None required.
- 📁 Files: .specify/memory/constitution.md updated.
- 🔁 Next prompts: User to review updated constitution and address manual follow-ups for template files.
- 🧠 Reflection: Successfully updated constitution and identified dependent files for alignment.

## Evaluation notes (flywheel)

- Failure modes observed: `create-phr.sh` script not found, switched to agent-native PHR creation.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Ensure `create-phr.sh` or similar script is available or documented in environment.
