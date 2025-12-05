---
id: 001
title: Create Textbook Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: groww
command: /sp.constitution
labels: ["constitution", "textbook", "physical-ai", "humanoid-robotics", "docusaurus"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation only)
---

## Prompt

```text
Project Context:
Title: Physical AI & Humanoid Robotics
Theme: AI Systems in the Physical World. Embodied Intelligence.
Goal: Teach students how AI connects to physical bodies through robotics. The book explains ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action systems for humanoid robots.

Scope:
This is an informational textbook only. No labs, no coding assignments, no hardware requirements. The book explains concepts, workflows, architectures, and robotics pipelines through narrative chapters, diagrams, and examples. All content should be accessible to motivated learners with basic Python and AI knowledge.

Audience:
Students in AI, robotics beginners, and engineers transitioning into physical AI and humanoid systems.

Content Structure (Modules):
Module 1: The Robotic Nervous System (ROS 2)
- ROS 2 nodes, topics, services
- rclpy for connecting AI agents to robot controllers
- URDF fundamentals for humanoids

Module 2: The Digital Twin (Gazebo & Unity)
- Simulating physics, collisions, and environments
- Unity for visualization and interaction
- Sensor simulation: LiDAR, Depth Cameras, IMUs

Module 3: The AI-Robot Brain (NVIDIA Isaac)
- Isaac Sim for photorealistic simulation and synthetic data
- Isaac ROS for VSLAM and navigation
- Nav2 for locomotion planning in humanoids

Module 4: Vision-Language-Action (VLA)
- Whisper for voice-to-action
- Using LLMs as planners translating natural language to ROS 2 action sequences
- High-level autonomous humanoid workflow

Non-Goals:
- No step-by-step lab instructions
- No hardware wiring or real robot deployment
- No reinforcement learning implementations
- No mathematically dense derivations beyond what is needed for understanding

Constraints:
- Book format: Docusaurus, MDX
- Writing style: clear, educational, focused on systems understanding
- Diagrams allowed; code snippets optional but not required to run
- Keep content practical and accessible

Writing Rules:
- English reading level should be 5 to 6 grade
- Simplify complex topics into simple terms
- Every module should be broke down into multiple chapters/sections
- Every module should be between 4000 to 6000 words


Quality Rules:
- Each chapter must have: clear learning objectives, diagrams or visuals, and a concise explanation of how the component fits into the humanoid pipeline.
- No excessive theory; everything should relate back to "Physical AI" and humanoid systems.
- Maintain consistent terminology across modules.

Success Criteria:
- A complete Docusaurus book with 4 modules and coherent chapters
- All content aligns with the goal: bridging AI and the physical robot body
- The book can be read standalone without extra tools

Deliverable:
Generate a constitution markdown file under .specs/constitution.md following Spec-Kit Plus templates.

End of prompt.
```

## Response snapshot

Created comprehensive constitution for Physical AI & Humanoid Robotics textbook with seven core principles:

1. **Accessibility First**: 5th-6th grade reading level mandatory
2. **Systems Understanding Over Implementation**: Informational focus, no labs/hardware
3. **Modular Structure**: 4,000-6,000 words per module, broken into chapters
4. **Visual and Narrative Clarity**: Diagrams and storytelling required
5. **Consistency and Terminology Standards**: Unified vocabulary across modules
6. **Practical Connection to Physical AI**: All content ties to embodied intelligence
7. **Docusaurus and MDX Compliance**: Technical formatting correctness

Additional sections defined:
- **Content Standards**: Module organization, chapter requirements, quality gates
- **Development Workflow**: Content creation process, non-goals, writing guidelines
- **Governance**: Amendment process, compliance review, versioning policy

Version: 1.0.0 (initial ratification)

## Outcome

- ✅ Impact: Established foundational governance for textbook project with clear principles for accessibility, content structure, and quality standards
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created .specify/memory/constitution.md (v1.0.0)
- 🔁 Next prompts: Use /sp.specify to create first feature spec for Module 1 (ROS 2), then /sp.plan for implementation planning
- 🧠 Reflection: Constitution successfully captures educational textbook requirements with emphasis on accessibility (5th-6th grade reading level), modular structure (4-6k words), and systems understanding over hands-on implementation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (initial constitution creation)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate constitution principles against first module creation to ensure principles are practical and enforceable
