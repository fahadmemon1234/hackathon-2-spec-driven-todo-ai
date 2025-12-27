---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-27
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, governance, setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

```
/sp.constitution # Project Constitution: The Evolution of Todo

## Preamble
This constitution establishes the foundational principles for "The Evolution of Todo" project. As Product Architects, we leverage AI to evolve a simple todo app from a CLI to a distributed cloud-native AI system. All development adheres to spec-driven, AI-assisted workflows using Spec-Kit Plus, Claude Code, and Qwen AI. No manual coding is permitted; focus on architecture, iteration, and scalability.

## Article I: Core Principles
1. **AI-Centric Development**: All code must be generated via AI tools (Claude Code for primary implementation, Qwen for planning, validation, or alternative generations). Manual edits are limited to minor fixes documented in commit messages.
2. **Spec-Driven Approach**: Every feature starts with a formal specification using Spec-Kit Plus. Specs must be versioned and stored in /specs-history/.
3. **Clean Code and Modularity**: Adhere to PEP 8, SOLID principles, and modular design. Code structure: /src/ for modules, clear separation of concerns (e.g., UI, logic, data).
4. **Transparency and Iteration**: Document all AI prompts, responses, and iterations in CLAUDE.md and QWEN.md. Review and refine based on execution results.
5. **Scalability Focus**: Design Phase I with future phases in mind (e.g., in-memory data as a placeholder for eventual DB/cloud integration).
6. **Ethical AI Use**: Ensure AI-generated code is reviewed for security, biases, and efficiency. No proprietary or harmful content.

## Article II: Technology Stack and Tools
- **Core Language**: Python 3.13+.
- **Package Manager**: UV for environments and dependencies.
- **AI Tools**:
  - Spec-Kit Plus: For writing and managing specifications (e.g., YAML-based reqs).
  - Claude Code: Primary code generator; use for task implementation.
  - Qwen AI: For analysis, planning, or secondary code suggestions to enhance diversity.
- **Prohibited**: Direct internet access in code (except via APIs in later phases); no external libs unless justified in specs.

## Article III: Development Workflow
1. **Write Spec**: Define requirements in Spec-Kit Plus.
2. **Generate Plan**: Use Qwen/Claude to create a high-level plan and task breakdown.
3. **Implement Tasks**: Generate code per task via Claude Code; integrate Qwen for reviews.
4. **Test and Iterate**: Run in console; refine specs and regenerate as needed.
5. **Version Control**: Commit specs, code, and docs to GitHub with descriptive messages.

## Article IV: Phase I Specific Rules
- **Scope**: In-memory CLI todo app with Add, Delete, Update, View, Mark Complete.
- **Data Handling**: Volatile list/dict in memory; no persistence.
- **User Interface**: Command-line only; intuitive commands with error handling.
- **Deliverables Compliance**: Include all listed files; demo must cover all features.

## Article V: Amendments and Governance
- Amendments require spec updates and AI review.
- In hackathon context, prioritize Phase I; extend only if time allows.
- Success Metric: Functional app + documented process.
```

## Response snapshot

I have successfully updated the project constitution for "The Evolution of Todo" project. Here's what was accomplished:

1. Created a new constitution file at `.specify/memory/constitution.md` with all the specified principles and governance rules.

2. Updated the following template files to align with the new constitution:
   - `.specify/templates/plan-template.md` - Updated constitution check and technology stack sections
   - `.specify/templates/spec-template.md` - Added constitution compliance note
   - `.specify/templates/tasks-template.md` - Added constitution compliance note

3. The new constitution includes:
   - Core Principles: AI-Centric Development, Spec-Driven Approach, Clean Code and Modularity, Transparency and Iteration, Scalability Focus, Ethical AI Use
   - Technology Stack and Tools: Python 3.13+, UV package manager, AI tools (Spec-Kit Plus, Claude Code, Qwen AI)
   - Development Workflow: Spec writing, planning, implementation, testing, and version control
   - Phase I Specific Rules: In-memory CLI todo app with specific features
   - Governance: Amendment procedures and success metrics

## Outcome

- ✅ Impact: Created foundational governance document for the project
- 🧪 Tests: No tests required for this configuration task
- 📁 Files: Updated 4 files to align with the new constitution
- 🔁 Next prompts: Ready to proceed with feature specifications and implementation
- 🧠 Reflection: The constitution establishes clear principles for AI-assisted development and provides a framework for evolving the todo app from CLI to distributed system

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing Phase I features according to the new constitution