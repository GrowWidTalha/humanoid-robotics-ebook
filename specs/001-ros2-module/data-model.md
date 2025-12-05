# Content Structure: Module 1 - ROS 2

**Date**: 2025-12-04
**Phase**: 1 - Design & Contracts
**Purpose**: Define learning flow and content entities for educational module

## Content Entities

### Module
**Definition**: Top-level learning unit covering a major robotics system or technology.

**Attributes**:
- **ID**: Unique identifier (e.g., `module1-ros2`)
- **Title**: Full descriptive name (e.g., "Module 1: The Robotic Nervous System (ROS 2)")
- **Short Title**: Sidebar/navigation label (e.g., "ROS 2")
- **Description**: 1-2 sentence summary of what readers will learn
- **Prerequisites**: Required background knowledge (e.g., "Basic Python, AI concepts")
- **Word Count Target**: 4,000-6,000 words total
- **Chapter Count**: 4-6 chapters
- **Estimated Reading Time**: 20-30 minutes total

**Example**:
```yaml
id: module1-ros2
title: "Module 1: The Robotic Nervous System (ROS 2)"
sidebar_label: "ROS 2 Fundamentals"
description: "Learn how ROS 2 connects AI brains to robot bodies through nodes, topics, and communication patterns."
prerequisites: ["Basic Python knowledge", "Understanding of AI/ML concepts"]
word_count_target: 4500
chapter_count: 5
estimated_time: "25 minutes"
```

---

### Chapter
**Definition**: Individual learning segment within a module, focused on specific concepts.

**Attributes**:
- **ID**: Unique identifier (e.g., `chapter1-introduction`)
- **Title**: Full chapter name (e.g., "Chapter 1: Introduction to ROS 2")
- **Sidebar Label**: Short navigation name (e.g., "Introduction")
- **Sidebar Position**: Order in sidebar (1-6)
- **Description**: Brief chapter summary (1 sentence)
- **Keywords**: SEO and searchability terms
- **Learning Objectives**: 3-5 measurable outcomes
- **Word Count Target**: 800-1,200 words
- **Diagram Count**: Minimum 1 per chapter
- **Examples**: Humanoid robot scenarios (2-3 per chapter)

**Example**:
```yaml
id: chapter2-nodes
title: "Chapter 2: Nodes - The Building Blocks"
sidebar_label: "Nodes"
sidebar_position: 2
description: "Understand how nodes act as independent programs coordinating robot functions."
keywords: [ros2, nodes, processes, modularity, robotics]
learning_objectives:
  - "Explain what a node is and why robots use many nodes"
  - "Describe how nodes communicate without sharing memory"
  - "Identify nodes in a humanoid robot system (camera, vision, control)"
word_count_target: 850
diagram_count: 1
examples:
  - "Camera node capturing images in humanoid head"
  - "Vision node processing object detection"
  - "Navigation node planning humanoid movement"
```

---

### Learning Objective
**Definition**: Measurable knowledge outcome readers should achieve from a chapter.

**Attributes**:
- **ID**: Unique identifier (e.g., `lo-ch2-01`)
- **Chapter**: Parent chapter reference
- **Statement**: Action verb + specific outcome (Bloom's taxonomy)
- **Level**: Remember, Understand, Apply, Analyze (for this textbook: Remember/Understand focus)
- **Verification**: How to test if objective met

**Examples**:
```yaml
# Chapter 1
- id: lo-ch1-01
  statement: "Explain what ROS 2 is and its role in humanoid robotics"
  level: Understand
  verification: "Can describe ROS 2 as middleware connecting robot components"

# Chapter 2
- id: lo-ch2-02
  statement: "Describe how nodes communicate through message passing"
  level: Understand
  verification: "Can explain publish-subscribe pattern with concrete example"

# Chapter 3
- id: lo-ch3-03
  statement: "Identify which communication pattern (topic/service/action) fits a scenario"
  level: Apply
  verification: "90% accuracy on pattern-matching scenarios"
```

---

### Diagram
**Definition**: Visual element supporting learning, embedded in chapter content.

**Attributes**:
- **ID**: Unique identifier (e.g., `diagram-ch2-node-communication`)
- **Chapter**: Parent chapter reference
- **Type**: Mermaid flowchart, static image (SVG/PNG), table
- **Title**: Descriptive caption
- **Alt Text**: Accessibility description
- **Source**: File path or Mermaid code
- **Purpose**: What concept this diagram clarifies

**Example**:
```yaml
id: diagram-ch2-node-communication
chapter: chapter2-nodes
type: mermaid
title: "Node Communication in a Humanoid Robot"
alt_text: "Flowchart showing camera node sending images to vision node, which sends detections to navigation node, which sends commands to leg control"
source: |
  ```mermaid
  graph LR
      A[Camera Node] -->|Image Topic| B[Vision Node]
      B -->|Object Detections| C[Navigation Node]
      C -->|Motor Commands| D[Leg Control Node]
  ```
purpose: "Illustrate how multiple nodes work together through topics"
```

---

### Example
**Definition**: Humanoid robot scenario illustrating a technical concept.

**Attributes**:
- **ID**: Unique identifier (e.g., `example-ch3-topic-balance`)
- **Chapter**: Parent chapter reference
- **Concept**: Which technical concept this demonstrates
- **Scenario**: 2-3 sentence narrative description
- **Connection**: How this relates to Physical AI / humanoid systems

**Example**:
```yaml
id: example-ch3-topic-balance
chapter: chapter3-communication
concept: "Topics (continuous data streams)"
scenario: "A humanoid robot has a balance sensor in its torso that constantly measures tilt. This sensor publishes tilt data 100 times per second to a 'balance_data' topic. The leg control system subscribes to this topic and adjusts leg motors to keep the robot upright."
connection: "Topics enable real-time sensor feedback essential for humanoid balance and locomotion."
```

---

### Glossary Term
**Definition**: Technical term defined in-text and referenced in centralized glossary.

**Attributes**:
- **Term**: The word or phrase being defined
- **Definition**: Simple explanation (1-2 sentences, 5-6 grade level)
- **Example**: Concrete usage in humanoid robotics context
- **First Introduced**: Module and chapter where first mentioned
- **Related Terms**: Other glossary entries to cross-reference

**Example**:
```yaml
term: "Node"
definition: "A node is an independent program that performs one specific task in a robot system. Each node runs separately and communicates with other nodes through ROS 2."
example: "A camera node captures images, while a vision node processes those images to detect objects."
first_introduced: "Module 1, Chapter 2"
related_terms: ["Topic", "Publisher", "Subscriber"]
```

---

## Learning Flow

### Overall Module Progression

```
Chapter 1: Introduction
    ↓ (Foundation: What & Why)
Chapter 2: Nodes
    ↓ (Building Blocks: Smallest Unit)
Chapter 3: Communication Patterns
    ↓ (Connections: How Nodes Interact)
Chapter 4: rclpy (AI Integration)
    ↓ (Practical Application: Python ↔ Robot)
Chapter 5: URDF (Robot Structure)
    ↓ (Physical Representation: Body Description)
[End: Reader understands ROS 2 role in humanoid pipeline]
```

### Within-Chapter Flow (Standard Pattern)

```
1. Learning Objectives (bullet list at top)
2. Introduction (2-3 paragraphs: context + preview)
3. Core Concept Explanation
   - Simple definition
   - Analogy (if applicable)
   - Why it matters for humanoid robots
4. Diagram (visual reinforcement)
5. Detailed Exploration
   - Break down into sub-concepts
   - Use admonitions for key points (:::note, :::tip)
6. Examples (2-3 humanoid scenarios)
7. Edge Cases / Common Questions (optional)
8. Summary (2-3 sentences)
9. Learning Checkpoint (:::tip with reflection question)
```

### Knowledge Dependencies

| Chapter | Depends On | Enables |
|---------|-----------|---------|
| Ch1: Introduction | None (entry point) | Understanding ROS 2 purpose |
| Ch2: Nodes | Ch1 (knows what ROS 2 is) | Understanding modularity |
| Ch3: Communication | Ch2 (knows what nodes are) | Understanding coordination |
| Ch4: rclpy | Ch2 + Ch3 (nodes + communication) | Connecting AI to robots |
| Ch5: URDF | Ch2 (node concept for simulation) | Understanding robot structure |

---

## Content Metadata Standards

### Frontmatter Template (All Chapters)

```yaml
---
id: chapter-{number}-{slug}
title: "Chapter {N}: {Full Title}"
sidebar_label: "{Short Title}"
sidebar_position: {N}
description: "{One sentence chapter summary}"
keywords: [{5-7 relevant terms}]
---
```

### Example Frontmatter (Chapter 3)

```yaml
---
id: chapter3-communication
title: "Chapter 3: Communication Patterns"
sidebar_label: "Communication"
sidebar_position: 3
description: "Learn how ROS 2 nodes communicate through topics, services, and actions."
keywords: [ros2, topics, services, actions, pub-sub, communication, robotics]
---
```

---

## Visual Element Guidelines

### Diagram Placement Rules

1. **Before complex explanation**: Introduce diagram before detailed text
2. **Adjacent to relevant text**: Never separate by more than 1 paragraph
3. **Captions required**: Every diagram has descriptive caption
4. **Alt text mandatory**: Accessibility description for screen readers

### Diagram Complexity Limits

- **Maximum elements**: 5-7 boxes/nodes per diagram
- **Maximum connections**: 6-8 arrows/edges
- **Text size**: 14px minimum (readable on mobile)
- **Colors**: High contrast, colorblind-friendly palette

### Admonition Usage Guide

| Type | Purpose | Example Use |
|------|---------|-------------|
| `:::note` | Key concepts, definitions | "ROS 2 is like the nervous system..." |
| `:::tip` | Learning checkpoints, best practices | "Can you explain how topics differ from services?" |
| `:::info` | Additional context, interesting facts | "ROS 2 was released in 2017..." |
| `:::warning` | Common misconceptions, pitfalls | "ROS 2 is NOT an operating system" |
| `:::danger` | Critical errors to avoid | (Rarely used in informational textbook) |

---

## Quality Metrics

### Per-Chapter Checklist

- [ ] Frontmatter complete and valid
- [ ] 3-5 learning objectives stated at top
- [ ] 800-1,200 word count (verified)
- [ ] 5-6 grade reading level (Flesch-Kincaid verified)
- [ ] At least 1 diagram included
- [ ] 2-3 humanoid robot examples present
- [ ] All technical terms defined on first mention
- [ ] At least 1 admonition used (note/tip/info)
- [ ] Learning checkpoint question at end (:::tip)
- [ ] No installation/code execution instructions
- [ ] Docusaurus build succeeds (no errors)

### Module-Level Validation

- [ ] Total word count: 4,000-6,000 words
- [ ] Chapter count: 4-6 chapters
- [ ] All chapters follow standard flow pattern
- [ ] Glossary entries created for all key terms
- [ ] Cross-references between chapters functional
- [ ] Diagrams consistent in style/color palette
- [ ] Mobile responsiveness verified
- [ ] All constitution principles satisfied

---

## Relationships and Dependencies

### Entity Relationship Diagram

```
Module (1)
  ├── Chapter (4-6)
  │   ├── Learning Objective (3-5 per chapter)
  │   ├── Diagram (1+ per chapter)
  │   ├── Example (2-3 per chapter)
  │   └── Glossary Term Reference (multiple)
  └── Glossary (shared across modules)
      └── Glossary Term (multiple)
```

### File Structure Mapping

```
docs/module1-ros2/
├── index.mdx                 → Module entity
├── chapter1-introduction.mdx → Chapter entity
├── chapter2-nodes.mdx        → Chapter entity
├── chapter3-communication.mdx → Chapter entity
├── chapter4-rclpy.mdx        → Chapter entity
├── chapter5-urdf.mdx         → Chapter entity
└── assets/
    └── *.png, *.svg          → Diagram entities

docs/glossary.md              → Glossary Term entities
```

---

## Summary

This data model defines the structure for educational content creation. Content entities (Module, Chapter, Learning Objective, Diagram, Example, Glossary Term) provide clear contracts for authors. Learning flow ensures progressive knowledge building. Metadata standards enable consistent Docusaurus rendering. Quality metrics enforce constitution compliance.

**Next Steps**:
1. Create chapter contracts (contracts/*.md) with detailed outlines
2. Generate quickstart.md for content authors
3. Begin content creation following these standards
