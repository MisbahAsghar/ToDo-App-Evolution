# Evolution of Todo – Phase I (In-Memory CLI) Constitution

<!--
  SYNC IMPACT REPORT
  ==================
  Version Change: [Template] → 1.0.0

  Changes Summary:
  - Initial constitution creation for Evolution of Todo project
  - Established 5 core principles: Spec-Driven Development, Simplicity First, Excellent CLI UX,
    Type Safety & Clarity, Modular Architecture
  - Added Engineering Standards and Development Workflow sections
  - Defined governance and amendment procedures

  Modified Principles:
  - All principles are new (first version)

  Added Sections:
  - Core Principles (5 principles)
  - Engineering Standards
  - Development Workflow
  - Governance

  Removed Sections:
  - None (initial version)

  Template Consistency Check:
  ✅ .specify/templates/plan-template.md - Compatible (Constitution Check section will validate against principles)
  ✅ .specify/templates/spec-template.md - Compatible (requirements and scenarios align with UX principles)
  ✅ .specify/templates/tasks-template.md - Compatible (task structure supports modular implementation)
  ✅ .specify/templates/phr-template.prompt.md - No changes needed
  ✅ .specify/templates/adr-template.md - No changes needed

  Follow-up TODOs:
  - None
-->

## Core Principles

### I. Spec-Driven Development First

**Spec-driven development is the source of truth.** No manual code writing by humans is permitted. All code MUST be generated through the spec-driven development workflow using the `/sp.*` commands. This ensures:

- Every feature originates from a clear specification
- Implementation follows approved design artifacts
- Changes are traceable and intentional
- Quality gates are enforced at every stage

**Rationale**: Prevents ad-hoc changes, ensures consistency, and maintains a clear audit trail of all development decisions.

### II. Simplicity First

**Start simple and avoid premature complexity.** The system MUST:

- Use in-memory data structures only (no file I/O, no databases)
- Implement only features explicitly defined in specifications
- Avoid abstractions that serve hypothetical future needs
- Keep the codebase readable and maintainable

**Prohibited Complexity**:
- Adding features not defined in specs
- Creating unnecessary abstractions or design patterns
- Implementing persistence mechanisms
- Adding web frameworks, external APIs, or AI features

**Rationale**: Phase I is a foundation for learning. Overengineering at this stage creates technical debt and obscures core concepts.

### III. Excellent CLI User Experience

**The CLI interface MUST be clear, friendly, and safe.** All user interactions MUST follow these standards:

- **Numbered menus** with clear options (e.g., "1. Add Task", "2. View Tasks")
- **Status indicators** using icons (✅ completed, ⏳ pending)
- **Friendly messages** for all operations (success, error, empty states)
- **Safe input handling** with validation and error messages
- **Clean formatting** with appropriate spacing and visual separators

**Rationale**: A well-designed CLI reduces cognitive load, prevents errors, and makes the application approachable for all users.

### IV. Type Safety & Clarity

**Code MUST be clear, explicit, and well-typed.** This includes:

- Python 3.13+ type hints for function signatures and complex data structures
- Explicit variable names that convey intent
- Docstrings for non-obvious functions
- Clear error messages that help users understand what went wrong

**Rationale**: Type hints catch errors early, improve IDE support, and serve as inline documentation. Clear code reduces maintenance burden.

### V. Modular Architecture

**The codebase MUST maintain clear separation of concerns.** Required module boundaries:

- **Models** (`src/models/`) – Data structures and business entities
- **Services** (`src/services/`) – Business logic and operations
- **CLI** (`src/cli/`) – User interface and input/output
- **Main** (`src/main.py`) – Application entry point

**Dependency Rule**: CLI may import Services and Models. Services may import Models. Models are independent. No circular dependencies permitted.

**Rationale**: Modular architecture enables independent testing, makes code easier to understand, and prepares for future phases where modules may evolve independently.

## Engineering Standards

**Language & Runtime**:
- Python 3.13 or higher required
- No external dependencies beyond Python standard library for Phase I

**Code Quality**:
- All functions must have clear, single responsibilities
- Maximum function length: 50 lines (excluding docstrings)
- No global mutable state
- Error handling for all user inputs

**Testing Philosophy** (when tests are required):
- Unit tests for business logic
- Integration tests for CLI workflows
- No mocking in-memory data structures

**Entry Point**:
- Application MUST run via `python -m src.main`
- No other entry points permitted

## Development Workflow

**All development MUST follow the Spec-Driven Development workflow**:

1. **Specification** (`/sp.specify`) – Define what needs to be built
2. **Planning** (`/sp.plan`) – Design the technical approach
3. **Task Generation** (`/sp.tasks`) – Break down into actionable tasks
4. **Implementation** (`/sp.implement`) – Execute tasks systematically
5. **Commit & PR** (`/sp.git.commit_pr`) – Version control integration

**Critical Rules**:
- Never skip specification phase
- Plans must be approved before task generation
- Tasks must be approved before implementation
- All changes must go through PR review
- Constitution compliance checked at each gate

**Decision Documentation**:
- Significant architectural decisions trigger ADR suggestions
- PHRs (Prompt History Records) created for every user interaction
- All design artifacts maintained in `specs/<feature>/`

## Governance

**This constitution supersedes all other development practices and guidelines.**

**Amendment Procedure**:
- Constitution changes require explicit user consent via `/sp.constitution`
- All amendments MUST include:
  - Clear rationale for the change
  - Impact analysis on existing principles
  - Version increment (semantic versioning: MAJOR.MINOR.PATCH)
  - Sync report showing template consistency
- Major version changes require review of all existing specs

**Compliance**:
- All code reviews MUST verify constitutional compliance
- Violations MUST be documented and justified in `plan.md` Complexity Tracking table
- Unjustified complexity is grounds for rejection

**Versioning**:
- **MAJOR**: Backward-incompatible principle changes (e.g., removing a core principle)
- **MINOR**: New principles or sections added (e.g., adding security standards)
- **PATCH**: Clarifications, typo fixes, wording improvements

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
