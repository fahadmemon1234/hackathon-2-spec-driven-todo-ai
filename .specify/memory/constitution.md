<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections added
Removed sections: N/A
Templates requiring updates: 
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated  
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ reviewed
- README.md ⚠ pending
Follow-up TODOs: None
-->

# The Evolution of Todo Constitution

## Core Principles

### I. AI-Centric Development
All code must be generated via AI tools (Claude Code for primary implementation, Qwen for planning, validation, or alternative generations). Manual edits are limited to minor fixes documented in commit messages.

### II. Spec-Driven Approach
Every feature starts with a formal specification using Spec-Kit Plus. Specs must be versioned and stored in /specs-history/.

### III. Clean Code and Modularity
Adhere to PEP 8, SOLID principles, and modular design. Code structure: /src/ for modules, clear separation of concerns (e.g., UI, logic, data).

### IV. Transparency and Iteration
Document all AI prompts, responses, and iterations in CLAUDE.md and QWEN.md. Review and refine based on execution results.

### V. Scalability Focus
Design Phase I with future phases in mind (e.g., in-memory data as a placeholder for eventual DB/cloud integration).

### VI. Ethical AI Use
Ensure AI-generated code is reviewed for security, biases, and efficiency. No proprietary or harmful content.

## Technology Stack and Tools
- **Core Language**: Python 3.13+.
- **Package Manager**: UV for environments and dependencies.
- **AI Tools**:
  - Spec-Kit Plus: For writing and managing specifications (e.g., YAML-based reqs).
  - Claude Code: Primary code generator; use for task implementation.
  - Qwen AI: For analysis, planning, or secondary code suggestions to enhance diversity.
- **Prohibited**: Direct internet access in code (except via APIs in later phases); no external libs unless justified in specs.

## Development Workflow
1. **Write Spec**: Define requirements in Spec-Kit Plus.
2. **Generate Plan**: Use Qwen/Claude to create a high-level plan and task breakdown.
3. **Implement Tasks**: Generate code per task via Claude Code; integrate Qwen for reviews.
4. **Test and Iterate**: Run in console; refine specs and regenerate as needed.
5. **Version Control**: Commit specs, code, and docs to GitHub with descriptive messages.

## Phase I Specific Rules
- **Scope**: In-memory CLI todo app with Add, Delete, Update, View, Mark Complete.
- **Data Handling**: Volatile list/dict in memory; no persistence.
- **User Interface**: Command-line only; intuitive commands with error handling.
- **Deliverables Compliance**: Include all listed files; demo must cover all features.

## Governance
Amendments require spec updates and AI review. In hackathon context, prioritize Phase I; extend only if time allows. Success Metric: Functional app + documented process.

**Version**: 1.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-12-27