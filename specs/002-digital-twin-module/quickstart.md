# Quickstart Guide: Writing Module 2 Content

**Purpose**: Fast reference for content writers creating Module 2 chapters

## Essential Information

| Aspect | Requirement |
|--------|-------------|
| **Target Reading Level** | Flesch-Kincaid Grade 5.0-6.9 |
| **Total Word Count** | 4,000-6,000 words (Module total) |
| **Chapters** | 7 chapters with individual targets |
| **Visual Requirement** | Minimum 1 diagram per chapter |
| **Format** | MDX for Docusaurus v2+ |
| **Validation Tool** | Hemingway Editor (hemingwayapp.com) |

---

## Quick Chapter Reference

| Chapter | Title | Words | Key Concepts | Visual |
|---------|-------|-------|--------------|--------|
| 1 | What is a Digital Twin? | 800 | Digital Twin, simulation benefits | Physical vs digital diagram |
| 2 | Physics Simulation Basics | 900 | Physics Engine, collisions, gravity | Collision/gravity illustration |
| 3 | Gazebo for Robotics | 1000 | Gazebo Environment, ROS 2 integration | Labeled Gazebo screenshot |
| 4 | Building Environments | 900 | Environment types, terrain | Environment comparison diagram |
| 5 | Unity Visualization | 800 | Unity Scene, visual realism | Gazebo vs Unity comparison |
| 6 | Simulating Sensors | 1000 | LiDAR, Depth Cameras, IMUs | Sensor visualization |
| 7 | Pipeline Integration | 600 | Development workflow, synthesis | Pipeline flow diagram |

---

## Writing Template

### Every Chapter Must Include:

```mdx
---
title: [Chapter Title]
---

# [Chapter Title]

## Learning Objectives

After completing this chapter, you will:
- [Objective 1 - understand/recognize/identify...]
- [Objective 2 - ...]
- [Objective 3 - ...]

## [Section 1 Heading]

[Content with analogies, simple explanations, active voice...]

:::tip Learning Tip
[Helpful memory aid or best practice]
:::

![Descriptive alt text](./assets/image-name.svg)

## [Section 2 Heading]

[More content...]

:::note Connection to ROS 2
[Callback to Module 1 concept - use sparingly, 2-3 per MODULE]
:::

## Summary

[2-3 sentences recapping key points]

## What's Next

[1 sentence preview of next chapter]
```

---

## Writing Checklist (Per Chapter)

### Before Writing
- [ ] Read spec.md for chapter requirements
- [ ] Review data-model.md for concepts to cover
- [ ] Check research.md for analogy/visual guidelines
- [ ] Note word count target for this chapter

### While Writing
- [ ] Use active voice ("The robot sends" not "is sent")
- [ ] Keep sentences short (15-20 words max)
- [ ] Define technical terms on first use (parenthetical)
- [ ] Include at least one analogy per major concept
- [ ] Add visual where it clarifies complex idea
- [ ] Connect to humanoid robotics explicitly

### After Drafting
- [ ] Run through Hemingway Editor (grade 6 or below)
- [ ] Count words (within ±100 of target?)
- [ ] Verify all learning objectives addressed
- [ ] Check visual is present and described
- [ ] Validate MDX syntax (Docusaurus build test)
- [ ] Review for terminology consistency

---

## Analogy Formula

**Structure**: "Think of [technical term] like [familiar concept]. Just as [familiar concept does X], [technical term does Y]. In robotics, this means [application]."

**Examples**:
- Physics Engine = Sports referee checking rules
- LiDAR = Bat echolocation with lasers
- Digital Twin = Practice dummy for athletes

**Sources**: Use universal experiences (sports, nature, everyday objects)

---

## Technical Term Format

**First use**: "A collision mesh (a simplified 3D shape used for detecting touch) helps the physics engine..."

**Subsequent uses**: Just use "collision mesh"

**Don't**: Explain the same term twice or use undefined jargon

---

## Visual Guidelines

### Requirements
- **File format**: SVG preferred (PNG for screenshots only)
- **Size limit**: <500KB per image
- **Alt text**: Descriptive (for accessibility)
- **Annotations**: Short labels (3-5 words) directly on image

### Style
- **Colors**: Max 3-4 colors per diagram
- **Consistency**: Reuse visual metaphors (robot icon style)
- **Simplicity**: Avoid cluttered diagrams

### Storage
- Save in: `docs/module-02-digital-twin/assets/`
- Reference as: `![Alt text](./assets/filename.svg)`

---

## MDX Features to Use

### Admonitions (Callouts)

```mdx
:::tip
Highlight best practices or memory aids
:::

:::note
Module 1 callbacks or contextual notes
:::

:::info
Real-world robotics examples
:::

:::caution
Common misconceptions to avoid
:::
```

### Standard Markdown
- Headers: `##`, `###` (no `#` - reserved for title)
- Lists: `-` for bullets, `1.` for numbered
- Bold: `**text**`
- Italic: `*text*`
- Code: `` `inline code` `` or ` ```language ``` ` for blocks
- Images: `![alt](path)`
- Links: `[text](url)`

### DON'T Use
- Custom React components
- Inline JavaScript
- Complex JSX
- HTML/CSS styling

---

## Cross-Reference Guidelines

### Module 1 Callbacks (2-3 total across all chapters)

**Format**: "Remember from Module 1 that ROS 2 nodes communicate via topics? In Gazebo, sensor data flows through these same topics."

**Where**: Chapters 3 (Gazebo), 6 (Sensors), 7 (Pipeline)

### Module 3-4 Forward References (1-2 total)

**Format**: "In Module 3, we'll see how AI systems process this LiDAR data for navigation and obstacle avoidance."

**Where**: Chapters 6 (Sensors), 7 (Pipeline)

---

## Common Mistakes to Avoid

### ❌ Don't Do This
- Long sentences (>25 words)
- Passive voice ("is simulated by" → use "simulates")
- Undefined technical terms
- Pop culture references (dates content)
- Coding tutorials or installation steps
- Overly casual tone ("super cool", "awesome")
- Forgetting to connect to humanoid robotics

### ✅ Do This Instead
- Short sentences (15-20 words)
- Active voice ("Gazebo simulates...")
- Parenthetical definitions on first use
- Universal analogies (sports, nature)
- Conceptual explanations only
- Friendly but professional tone
- Explicit "Why this matters for humanoid robots"

---

## Validation Commands

### Readability Check
```bash
# Paste text into: https://hemingwayapp.com/
# Target: Grade 6 or below (grade 5 ideal)
```

### Word Count
```bash
# In docs directory:
wc -w module-02-digital-twin/01-what-is-digital-twin.mdx
```

### Docusaurus Build Test
```bash
# In repo root:
npm run build
# Should complete with no errors for Module 2 files
```

### Link Validation
```bash
# Check all internal links work
# Verify Module 1 cross-references point to real content
```

---

## Quick Reference: Key Concepts

### Chapter 1: Digital Twin
- What: Virtual replica of physical robot
- Why: Safe, fast, cheap testing
- How: Physics + geometry + sensors + behavior

### Chapter 2: Physics Engine
- What: Software calculating motion/collisions
- Key properties: Gravity, friction, collisions
- Analogy: Sports referee enforcing rules

### Chapter 3: Gazebo
- What: Primary ROS 2 simulation tool
- Features: Worlds, models, physics, ROS topics
- Use case: Algorithm testing, behavior validation

### Chapter 4: Environments
- Types: Flat, stairs, cluttered, outdoor
- Design: Match environment to test goal
- Properties: Terrain friction, material surfaces

### Chapter 5: Unity
- What: Game engine for high-fidelity visuals
- Strength: Realistic rendering, lighting
- Use case: HRI testing, visualization

### Chapter 6: Sensors
- **LiDAR**: Distance measurement (echolocation analogy)
- **Depth Camera**: 3D space understanding
- **IMU**: Orientation and acceleration for balance

### Chapter 7: Integration
- Workflow: Design → Simulate → Deploy
- Connections: Module 1 (ROS 2) ← → Module 2 (Sim) ← → Modules 3-4 (AI)
- Value: Safe development before hardware

---

## Resources

### Writing & Readability
- **Hemingway Editor**: https://hemingwayapp.com/
- **Readable.com**: https://readable.com/
- **Flesch-Kincaid Calculator**: https://readabilityformulas.com/

### Docusaurus Reference
- **Docs**: https://docusaurus.io/docs
- **MDX Syntax**: https://mdxjs.com/
- **Admonitions**: https://docusaurus.io/docs/markdown-features/admonitions

### Visual Tools
- **Excalidraw** (simple diagrams): https://excalidraw.com/
- **draw.io** (technical diagrams): https://app.diagrams.net/
- **Figma** (polished visuals): https://figma.com/

### Technical Accuracy
- **Gazebo Docs**: https://gazebosim.org/
- **Unity Robotics**: https://unity.com/solutions/automotive-transportation-manufacturing/robotics
- **ROS 2 Docs**: https://docs.ros.org/

---

## Getting Help

**Questions about**:
- **Specification requirements**: See `spec.md`
- **Content structure**: See `data-model.md`
- **Writing strategies**: See `research.md`
- **Detailed tasks**: See `tasks.md` (after `/sp.tasks`)
- **Constitution compliance**: See `.specify/memory/constitution.md`

**When stuck**: Review the spec's User Stories to remember who you're writing for and what they need to understand.
