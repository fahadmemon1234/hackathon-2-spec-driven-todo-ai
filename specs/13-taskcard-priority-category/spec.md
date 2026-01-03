# Feature Specification: TaskCard Priority & Category Visual Display

**Feature Branch**: `13-taskcard-priority-category`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "Task 4: TaskCard UI Upgrade – Show Priority & Category Specification + Implementation # Phase II Intermediate Level – Enhance TaskCard with Priority & Category Visuals # Current Status: Task 1-3 complete (Backend supports new fields, Form sends them) You are an expert Next.js + Tailwind CSS developer with luxury UI skills. Goal for Task 4: Upgrade the TaskCard component to visually display priority and category in a premium, luxurious way consistent with the dark theme (#252525 bg, #d90429 red, #f6d72d gold). Requirements: 1. Priority Visual Indicators - Left vertical stripe (4-6px wide) on card: - High: #d90429 (deep red) - Medium: #f6d72d (gold) - Low: #666666 (subtle gray) - Priority badge (small pill inside card): - Text: HIGH / MEDIUM / LOW (uppercase) - Background: matching color with 80% opacity - Text color: white for high/medium, dark for low if needed - Position: top-right or below title 2. Category Tag - Small rounded pill/tag: - Background: #2c2c2c or subtle #f6d72d33 - Text color: #cccccc - Border optional: thin #f6d72d33 - Position: below priority or next to it - If no category: hide tag 3. Completed Task Styling - When completed: - Title strike-through - Muted opacity (70%) on whole card - Keep priority stripe visible (full opacity) - Badge/tag slightly faded 4. Layout Example (Tailwind classes) - Card base: bg-[#1e1e1e] or #2c2c2c, rounded-lg, shadow-lg, hover:scale-105 transition - Left stripe: absolute left-0 top-0 bottom-0 w-1.5 rounded-l-lg className={` ${task.priority === 'high' ? 'bg-[#d90429]' : task.priority === 'medium' ? 'bg-[#f6d72d]' : 'bg-gray-600'} `} - Priority badge: px-3 py-1 rounded-full text-xs font-bold - Category tag: px-3 py-1 rounded-full text-xs 5. Responsive & Luxury Feel - Generous spacing - Subtle hover glow (box-shadow on hover with #f6d72d) - Smooth transitions - Mobile: stripe still visible, tags stack if needed 6. Fallback - If priority missing (old tasks): default to medium stripe/badge - If category missing: no tag Refer to: @specs/ui/components.md (update TaskCard description) @frontend/CLAUDE.md Now implement Task 4 exactly as specified. Update the TaskCard component to show: - Colored left stripe based on priority - Priority badge - Category tag - Special styling for completed tasks Keep everything consistent with existing luxury dark theme. After this task, tasks will visually stand out by priority and category – app feels highly organized."
**Constitution Compliance**: All features must adhere to project constitution principles

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visual Priority Indicators (Priority: P1)

As a user, I want to see visual indicators for task priority levels (High, Medium, Low) on each task card so that I can quickly identify and focus on the most important tasks.

**Why this priority**: This is the foundational capability that enables users to visually distinguish between different priority levels at a glance, improving task management efficiency.

**Independent Test**: User can visually identify the priority level of a task by looking at the colored left stripe and priority badge on the task card.

**Acceptance Scenarios**:

1. **Given** I am viewing the task list, **When** I see a task with high priority, **Then** the task card displays a deep red left stripe and a HIGH badge.
2. **Given** I am viewing the task list, **When** I see a task with medium priority, **Then** the task card displays a gold left stripe and a MEDIUM badge.
3. **Given** I am viewing the task list, **When** I see a task with low priority, **Then** the task card displays a gray left stripe and a LOW badge.

---

### User Story 2 - Category Display (Priority: P1)

As a user, I want to see category tags on task cards so that I can quickly identify and group tasks by topic or context (work, personal, health, etc.).

**Why this priority**: This is a core organizational capability that allows users to visually categorize their tasks for better management and filtering.

**Independent Test**: User can visually identify the category of a task by looking at the category tag on the task card.

**Acceptance Scenarios**:

1. **Given** I am viewing the task list, **When** I see a task with a category, **Then** the task card displays a category tag with the appropriate text.
2. **Given** I am viewing the task list, **When** I see a task without a category, **Then** no category tag is displayed on the task card.

---

### User Story 3 - Completed Task Styling (Priority: P2)

As a user, I want completed tasks to have distinct styling so that I can easily differentiate between pending and completed tasks while still seeing their priority and category.

**Why this priority**: This improves the user experience by providing clear visual feedback for completed tasks while maintaining visibility of important metadata.

**Independent Test**: User can distinguish completed tasks from pending tasks by their styling while still seeing priority and category information.

**Acceptance Scenarios**:

1. **Given** I am viewing the task list, **When** I see a completed task, **Then** the task title has a strikethrough and the card has reduced opacity while priority indicators remain visible.
2. **Given** I am viewing the task list, **When** I see a completed task with priority/category, **Then** the priority stripe remains fully opaque while badges/tags are slightly faded.

---

### User Story 4 - Luxury Dark Theme Consistency (Priority: P2)

As a user, I want the priority and category displays to follow the luxury dark theme so that the interface feels premium and cohesive.

**Why this priority**: This enhances user satisfaction and provides a consistent, professional experience across the application.

**Independent Test**: The priority and category displays follow the luxury dark theme with appropriate colors, styling, and interactions.

**Acceptance Scenarios**:

1. **Given** I am using the application, **When** I view task cards with priority and category, **Then** they follow the luxury dark theme with appropriate colors and styling.
2. **Given** I am using the application, **When** I hover over task cards, **Then** they have subtle hover effects with the gold accent color.

---

### User Story 5 - Responsive Design (Priority: P3)

As a user, I want the priority and category displays to work well on mobile devices so that I can effectively manage tasks on any device.

**Why this priority**: This ensures accessibility across different devices and screen sizes, providing a consistent experience.

**Independent Test**: The priority and category displays are properly visible and usable on mobile devices.

**Acceptance Scenarios**:

1. **Given** I am using the application on a mobile device, **When** I view task cards, **Then** the priority stripe is still visible and category tags stack appropriately.

---

### Edge Cases

- What happens when a task has no priority value (old tasks)? The system should default to medium priority styling.
- How does the system handle tasks with no category? The system should hide the category tag.
- What happens when a task has a very long category name? The system should handle it gracefully without breaking the layout.
- How does the system handle special characters in category names?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a colored left stripe on task cards based on priority level (High: #d90429, Medium: #f6d72d, Low: #666666)
- **FR-002**: System MUST display priority badges with uppercase text (HIGH/MEDIUM/LOW) and matching background colors
- **FR-003**: System MUST display category tags as rounded pills when category is present
- **FR-004**: System MUST hide category tags when no category is present
- **FR-005**: System MUST apply strikethrough styling to completed task titles
- **FR-006**: System MUST apply reduced opacity to completed task cards while keeping priority stripes fully visible
- **FR-007**: System MUST apply luxury dark theme styling consistently across all priority and category displays
- **FR-008**: System MUST provide subtle hover effects with gold accent color on task cards
- **FR-009**: System MUST handle responsive layouts appropriately on mobile devices
- **FR-010**: System MUST default to medium priority styling for tasks without priority values

### Key Entities

- **Task**: Represents a single todo item that includes priority and category attributes to help users organize and manage their work. The priority attribute can be "high", "medium", or "low", and the category attribute is an optional string.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can identify task priority levels by visual indicators without reading text 95% of the time
- **SC-002**: Users can identify task categories by visual tags without reading text 90% of the time
- **SC-003**: Users can distinguish completed tasks from pending tasks by visual styling 98% of the time
- **SC-004**: The interface maintains visual consistency with the luxury dark theme aesthetic
- **SC-005**: Task cards display properly on mobile devices with priority and category information visible