# Physical AI & Humanoid Robotics Textbook Constitution

<!--
SYNC IMPACT REPORT
==================
Version change: [INITIAL] → 1.0.0
Change type: Initial constitution creation
Added sections: All principles (7), Content Standards, Development Workflow, Governance
Modified principles: N/A (new document)
Removed sections: None

Templates requiring updates:
✅ plan-template.md - Constitution Check section references this file
✅ spec-template.md - Requirements align with content principles
✅ tasks-template.md - Task organization aligns with module structure
✅ All command files - Reference this constitution for governance

Follow-up TODOs: None - all placeholders filled
-->

## Core Principles

### I. Accessibility First
Content MUST be written at a 5th to 6th grade English reading level. Complex technical concepts MUST be explained using simple terms, analogies, and clear examples. No reader should be excluded due to language complexity. Every technical term MUST be defined on first use. Avoid jargon unless it is essential and immediately explained.

**Rationale**: This textbook targets students, beginners, and transitioning engineers who may not have deep robotics backgrounds. Accessibility ensures the widest possible audience can learn from the material without frustration.

### II. Systems Understanding Over Implementation
The book explains concepts, workflows, architectures, and robotics pipelines. It does NOT require labs, coding assignments, or hardware. All content focuses on how Physical AI systems work, how components connect, and why design decisions matter. Examples and diagrams illustrate concepts; code snippets are optional and never required to run.

**Rationale**: This is an informational textbook, not a hands-on course. Readers should understand the "what" and "why" of humanoid robotics systems without needing expensive hardware or complex lab setups.

### III. Modular Structure (NON-NEGOTIABLE)
Every module MUST be broken into multiple chapters or sections. Each module MUST contain 4,000 to 6,000 words. Chapters within a module MUST have clear learning objectives, diagrams or visuals, and concise explanations of how the component fits into the humanoid pipeline. No single chapter should overwhelm the reader.

**Rationale**: Breaking content into digestible chunks improves learning retention. Fixed word counts ensure consistency and prevent scope creep or under-developed modules.

### IV. Visual and Narrative Clarity
Each chapter MUST include diagrams, visuals, or illustrative examples. Concepts MUST be explained through narrative storytelling where appropriate (e.g., "Think of ROS 2 as the nervous system of a robot..."). Technical accuracy is paramount, but explanations prioritize clarity and engagement.

**Rationale**: Visual learners benefit from diagrams, and narratives make abstract concepts concrete. Combining both creates a richer learning experience.

### V. Consistency and Terminology Standards
All modules MUST use consistent terminology. For example, if "node" refers to a ROS 2 process in Module 1, it MUST mean the same thing throughout the book. A glossary or terminology reference MUST be maintained. Cross-references between modules MUST be accurate and helpful.

**Rationale**: Inconsistent terminology confuses readers and undermines learning. A coherent vocabulary across all modules builds confidence and understanding.

### VI. Practical Connection to Physical AI
Every concept, tool, or system explained MUST relate back to Physical AI and humanoid robotics. No purely theoretical content should exist without a clear connection to embodied intelligence. Readers should always understand: "Why does this matter for building humanoid robots?"

**Rationale**: The book's theme is AI in the physical world. Every topic must justify its inclusion by demonstrating relevance to humanoid robotics workflows.

### VII. Docusaurus and MDX Compliance
All content MUST be written in MDX format compatible with Docusaurus. Markdown syntax, frontmatter, and structure MUST follow Docusaurus conventions. Code fences, admonitions, and interactive elements MUST be used where appropriate. No content should break the Docusaurus build process.

**Rationale**: Docusaurus is the delivery platform. Non-compliant content will fail to render or degrade the reader experience. Technical correctness in formatting is as important as content accuracy.

## Content Standards

### Module Organization
Each module MUST address a specific domain within the humanoid robotics pipeline:
1. **Module 1 (ROS 2)**: The Robotic Nervous System - nodes, topics, services, rclpy, URDF
2. **Module 2 (Gazebo & Unity)**: The Digital Twin - physics simulation, sensor simulation, visualization
3. **Module 3 (NVIDIA Isaac)**: The AI-Robot Brain - Isaac Sim, Isaac ROS, VSLAM, Nav2
4. **Module 4 (VLA)**: Vision-Language-Action - Whisper, LLMs as planners, autonomous workflows

Modules MUST build on each other logically but remain independently readable where possible.

### Chapter Requirements
Every chapter MUST include:
- Clear learning objectives (3-5 bullet points stating what the reader will understand)
- At least one diagram, visual, or illustrative example
- A concise explanation of how the topic fits into the humanoid robotics pipeline
- No excessive theory; all content grounded in practical system understanding

### Quality Gates
Before a chapter is considered complete:
- Reading level verified at 5th-6th grade (use readability tools if available)
- All technical terms defined on first use
- At least one visual element included
- Word count falls within module target (4,000-6,000 words total per module)
- Cross-references verified for accuracy
- Docusaurus build succeeds without errors

## Development Workflow

### Content Creation Process
1. **Outline First**: Draft chapter outline with learning objectives before writing prose
2. **Write Clearly**: Use simple language, short sentences, active voice
3. **Illustrate**: Add diagrams or examples that clarify complex points
4. **Review**: Verify reading level, terminology consistency, and practical relevance
5. **Build Test**: Run Docusaurus build to ensure no formatting errors
6. **Iterate**: Revise based on feedback or quality gate failures

### Non-Goals (Explicitly Out of Scope)
- Step-by-step lab instructions or coding tutorials
- Hardware wiring guides or real robot deployment procedures
- Reinforcement learning implementations or mathematically dense derivations
- Interactive exercises requiring code execution
- Content targeting experts (focus remains on beginners and transitioning engineers)

### Writing Guidelines
- **Sentence length**: Prefer short sentences (15-20 words max where possible)
- **Active voice**: "The robot sends a message" not "A message is sent by the robot"
- **Analogies**: Use everyday comparisons ("ROS 2 topics are like radio channels...")
- **Definitions**: Define terms immediately ("A node is a single process that performs a specific task.")
- **Examples**: Provide concrete examples tied to humanoid robots

## Governance

This constitution supersedes all other content guidelines and practices. Any deviation from these principles MUST be documented and justified in an Architectural Decision Record (ADR).

### Amendment Process
1. Proposed changes MUST be documented with rationale and impact analysis
2. Changes affecting core principles (I-VII) require major version increment
3. Changes adding new sections or expanding guidance require minor version increment
4. Clarifications, typo fixes, or non-semantic edits require patch version increment
5. All amendments MUST update dependent templates (spec, plan, tasks) for consistency

### Compliance and Review
- All content creation MUST verify adherence to principles I-VII before completion
- Quality gates (reading level, visuals, word count, terminology) are NON-NEGOTIABLE
- Complexity or deviations MUST be justified and documented
- Use the plan-template.md Constitution Check section to validate compliance during planning

### Versioning Policy
- **MAJOR.MINOR.PATCH** format
- MAJOR: Backward-incompatible changes (e.g., removing a principle, changing scope)
- MINOR: New principles, sections, or materially expanded guidance
- PATCH: Clarifications, wording improvements, corrections

**Version**: 1.0.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04
