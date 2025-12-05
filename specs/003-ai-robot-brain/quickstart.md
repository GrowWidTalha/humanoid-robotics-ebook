# Content Creation Guidelines: Module 3 Overview

**Target Deliverable**: `docs/modules/module-3-ai-robot-brain/overview.md`
**Word Count**: 800-1000 words (STRICT requirement from spec FR-006)
**Reading Level**: 5th-6th grade (Constitution Principle I)

## Quick Reference Checklist

### Readability Requirements ✅

- [ ] **Reading Level**: 5th-6th grade (use readability tool to verify)
- [ ] **Sentence Length**: Average 12-15 words, max 20 words per sentence
- [ ] **Active Voice**: Use "The robot builds a map" not "A map is built by the robot"
- [ ] **Common Vocabulary**: Prefer simple words; define technical terms immediately
- [ ] **Paragraph Length**: 3-5 sentences per paragraph maximum
- [ ] **Conversational Tone**: Write like you're explaining to a curious friend

### Terminology Checklist ✅

**MUST define on first use** (in parentheses or immediate context):

Essential Terms:
- [ ] VSLAM / Visual SLAM
- [ ] Photorealistic simulation
- [ ] Synthetic data
- [ ] Perception
- [ ] Hardware acceleration / GPU
- [ ] Real-time processing
- [ ] Path planning / navigation planning
- [ ] Bipedal locomotion
- [ ] Sim-to-real transfer
- [ ] Sensor fusion
- [ ] Footstep planning
- [ ] Dynamic stability

Optional Mentions (brief reference okay):
- ROS2 (assume readers know from Module 1)
- Isaac Sim / Isaac ROS / Nav2 (names of tools, explain what they do)

### Prohibited Content ❌

**DO NOT include**:
- Code examples or syntax
- Installation instructions
- Hardware specifications or requirements
- API documentation
- Mathematical equations or derivations
- Step-by-step tutorials
- Troubleshooting guides
- Version-specific details (mention "Isaac Sim 5.0" but don't require it)

### Required Elements ✅

**MUST include**:
- [ ] At least one visual element (system diagram showing data flow OR reference to diagram)
- [ ] Narrative explanations using analogies
- [ ] Practical examples showing real-world benefits
- [ ] Quantifiable data (specific numbers showing performance)
- [ ] Connection to humanoid robotics throughout
- [ ] "AI-Robot Brain" metaphor woven through content
- [ ] References to all three components: Isaac Sim, Isaac ROS, Nav2

### Tone & Style Guidelines

**DO**:
- ✅ Use direct address ("Imagine you're...")
- ✅ Ask rhetorical questions to engage readers
- ✅ Provide concrete examples (9 months of data in 11 hours)
- ✅ Use relatable analogies (mental map in dark building)
- ✅ Show enthusiasm about technology
- ✅ Connect to reader experience (video games, walking)
- ✅ Use active, action-oriented language

**DON'T**:
- ❌ Use jargon without explanation
- ❌ Write in passive voice
- ❌ Include unnecessary details
- ❌ Overwhelm with technical complexity
- ❌ Use marketing hyperbole ("revolutionary," "game-changing")
- ❌ Write academically dry descriptions

## Docusaurus Formatting Guidelines

### Frontmatter Template

```yaml
---
title: "Module 3: The AI-Robot Brain (NVIDIA Isaac™)"
description: "Discover how NVIDIA Isaac Sim, Isaac ROS, and Nav2 work together as an integrated AI-Robot Brain enabling humanoid robots to perceive, learn, and navigate."
sidebar_position: 3
keywords:
  - NVIDIA Isaac
  - Isaac Sim
  - Isaac ROS
  - VSLAM
  - Nav2
  - humanoid navigation
  - synthetic data
  - robot perception
---
```

### Heading Hierarchy

```markdown
# Module 3: The AI-Robot Brain (NVIDIA Isaac™)   ← H1 (title, auto-generated from frontmatter)

## Introduction                                  ← H2 (main sections)

## Isaac Sim: Training Ground                    ← H2

### Photorealistic Simulation                    ← H3 (subsections if needed)

**Bold for emphasis**                            ← Not headings
```

**Rules**:
- One H1 per page (automatically from title)
- H2 for main sections (7 sections per outline)
- H3 sparingly for subsections (avoid if possible for 800-1000 words)
- Never skip levels (H2 → H4 is wrong)

### Admonitions (Info Boxes)

Use Docusaurus admonitions for key takeaways:

```markdown
:::tip Key Takeaway
Isaac ROS Visual SLAM achieves 250 frames per second on NVIDIA Jetson, enabling real-time perception for humanoid balance and navigation.
:::

:::note
VSLAM (Visual Simultaneous Localization and Mapping) is like creating a mental map as you explore a new building—figuring out where you are while mapping the layout, all at the same time.
:::

:::info Companies Using Isaac
Major humanoid robotics companies including Fourier Intelligence, Agility Robotics, and Sanctuary AI use NVIDIA Isaac for development.
:::
```

**When to use**:
- `::: tip` for key takeaways and important concepts
- `:::note` for analogies and explanations
- `:::info` for real-world examples and company adoption
- `:::warning` (avoid in overview—too strong)

### Inline Formatting

```markdown
**Bold** for emphasis on important terms (first use)
*Italic* for subtle emphasis (use sparingly)
`inline code` for technical terms like GPU, ROS2, API (use sparingly)
[Link text](URL) for external references

> Blockquote for important statements or definitions
```

### Lists

**Numbered lists** for sequential/ordered items:
```markdown
1. First, the robot's camera captures images
2. Then, VSLAM identifies visual features
3. Finally, the system calculates position and map
```

**Bullet lists** for non-sequential items:
```markdown
- Perception provides awareness
- Planning chooses actions
- Control executes movements
```

### Visual Elements

**System Diagram** (if creating):
- Use Mermaid diagram (Docusaurus-native) OR
- Create PNG and save to `docs/assets/module-3/isaac-pipeline-diagram.png`

**Mermaid Example**:
```markdown
```mermaid
graph LR
    A[Sensors] --> B[Isaac ROS VSLAM]
    B --> C[Nav2 Planning]
    C --> D[Robot Control]
    D --> A
```​
```

**Image Example**:
```markdown
![Isaac Platform Data Flow](../../assets/module-3/isaac-pipeline-diagram.png)
*Data flows from sensors through perception (Isaac ROS) to planning (Nav2) to control and back.*
```

## Quality Gates (Pre-Submission Checklist)

### Word Count Validation

```bash
# Count words (exclude frontmatter)
wc -w overview.md

# Target: 800-1000 words (STRICT)
# If outside range, edit to comply
```

### Readability Test

Use online tool (https://readabilityformulas.com/) or command:

```bash
# Flesch-Kincaid Grade Level Target: 5-6
# Flesch Reading Ease Target: 60-70 (Standard/Plain English)
```

**If grade level too high**:
- Shorten sentences
- Replace complex words with simpler alternatives
- Break long paragraphs into shorter ones
- Use more active voice

### Docusaurus Build Test

```bash
# Run from project root
npm run build

# Or
yarn build

# Must succeed without errors
```

**Common errors to fix**:
- Missing frontmatter closing `---`
- Broken internal links
- Unclosed admonitions
- Invalid heading hierarchy
- Syntax errors in Mermaid diagrams

## Content Writing Process (Recommended Order)

1. **Review research.md and content-outline.md** (10 minutes)
   - Familiarize with all research findings
   - Understand proposed structure and word allocations

2. **Write draft without editing** (45-60 minutes)
   - Follow outline structure
   - Write continuously, don't stop to edit
   - Include all key points from outline
   - Use placeholders for quantifiable data you'll verify later

3. **Add frontmatter and format** (10 minutes)
   - Add YAML frontmatter at top
   - Apply heading hierarchy (H2 for main sections)
   - Format bold terms, lists, quotes

4. **Insert quantifiable data** (15 minutes)
   - Verify all statistics from research.md
   - Add specific numbers (250 FPS, 9 months in 11 hours, etc.)
   - Double-check accuracy

5. **Add analogies and examples** (15 minutes)
   - Insert analogies from content-outline.md
   - Add concrete examples showing real-world benefits
   - Ensure each technical concept has supporting analogy

6. **Refine for readability** (20 minutes)
   - Check sentence length (aim for 12-15 words average)
   - Convert passive to active voice
   - Replace complex words with simpler alternatives
   - Break long paragraphs

7. **Add visual elements** (20 minutes)
   - Create or reference system diagram
   - Add admonitions for key takeaways
   - Consider embedded video (optional)

8. **Word count adjustment** (15 minutes)
   - Count words (exclude frontmatter)
   - If over 1000: cut less critical details
   - If under 800: expand examples or explanations
   - Target: 900-950 words (buffer for final edits)

9. **Readability test** (10 minutes)
   - Use online readability tool
   - Adjust until 5th-6th grade level
   - Verify Flesch Reading Ease 60-70

10. **Final polish** (20 minutes)
    - Read aloud to catch awkward phrasing
    - Verify "AI-Robot Brain" metaphor consistent
    - Check all terms defined on first use
    - Ensure smooth transitions between sections

11. **Build test** (5 minutes)
    - Run Docusaurus build
    - Fix any errors
    - Preview in browser

**Total Time**: ~3-4 hours for first draft to polished content

## Common Pitfalls to Avoid

❌ **Too Technical**: "The cuVSLAM library implements GPU-accelerated ORB feature extraction with loop closure optimization"
✅ **Just Right**: "Isaac ROS uses the GPU to process images 10 times faster than traditional methods"

❌ **Too Vague**: "Isaac Sim is a great tool for training robots"
✅ **Specific**: "Isaac Sim generated 9 months of training data in 11 hours, improving robot performance by 40%"

❌ **Passive Voice**: "Maps are built by the VSLAM system as the robot moves"
✅ **Active Voice**: "The VSLAM system builds maps as the robot moves"

❌ **Jargon Heavy**: "The sim-to-real transfer leverages domain randomization to mitigate the reality gap"
✅ **Clear**: "Robots trained in simulation work on real hardware because the simulator varies conditions to prepare for real-world differences"

❌ **No Analogy**: "VSLAM simultaneously estimates pose and reconstructs the environment"
✅ **With Analogy**: "VSLAM is like creating a mental map as you explore a dark building—figuring out where you are while mapping the layout, both at the same time"

## Success Criteria (From Spec)

Verify these before submitting:

**SC-001**: Readers can explain purpose of Isaac Sim, Isaac ROS, Nav2 in 2-3 sentences each
- ✅ Each component has clear, concise explanation

**SC-002**: Content is 800-1000 words
- ✅ Word count verified (exclude frontmatter)

**SC-003**: 90% of readers can identify which component handles simulation, perception, navigation
- ✅ Clear labels: Isaac Sim (training), Isaac ROS (perception), Nav2 (navigation)

**SC-004**: Workflow from training → perception → navigation is clear
- ✅ Integration section shows complete data flow

**SC-005**: At least two NVIDIA Isaac advantages articulated
- ✅ Hardware acceleration, unified ecosystem, sim-to-real success, company adoption

**SC-006**: Accessible to students, valuable for engineers
- ✅ 5th-6th grade reading level with technical depth

**SC-007**: Prepares for hands-on tutorials
- ✅ Conclusion previews next learning steps

## Final Validation Checklist

Before marking tasks complete:

**Content Quality**:
- [ ] 800-1000 words (strict)
- [ ] 5th-6th grade reading level
- [ ] All technical terms defined on first use
- [ ] At least one visual element present
- [ ] Analogies support complex concepts

**Technical Accuracy**:
- [ ] Isaac Sim capabilities correctly represented
- [ ] VSLAM concept properly explained
- [ ] Nav2 bipedal challenges accurate
- [ ] Integration story shows correct data flow
- [ ] All statistics verified from research.md

**Constitution Compliance**:
- [ ] Accessible language (Principle I)
- [ ] Systems understanding focus (Principle II)
- [ ] Visual/narrative clarity (Principle IV)
- [ ] Terminology consistency (Principle V)
- [ ] Physical AI connection (Principle VI)
- [ ] Docusaurus compliance (Principle VII)

**Docusaurus Integration**:
- [ ] Valid MDX format with frontmatter
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Admonitions used appropriately
- [ ] Build succeeds without errors
- [ ] Mobile-responsive rendering verified

**Spec Alignment**:
- [ ] All 10 functional requirements satisfied
- [ ] All 3 user story acceptance scenarios addressable
- [ ] Scope respected (overview only, no tutorials)
- [ ] Edge cases considered (varying reader backgrounds)

## Emergency Troubleshooting

**Word count too high (>1000)**:
1. Remove redundant phrases
2. Combine similar examples
3. Cut less critical technical details
4. Tighten transitions between sections
5. Last resort: reduce one section (prioritize Sections 2-4)

**Reading level too high (>6th grade)**:
1. Shorten longest sentences first
2. Replace complex words (utilize → use, facilitate → help)
3. Break compound sentences into simple sentences
4. Add more analogies to explain technical terms
5. Use more active voice

**Build fails**:
1. Check frontmatter has closing `---`
2. Verify heading hierarchy (no skipped levels)
3. Close all admonitions with `:::`
4. Fix broken internal links
5. Check Mermaid diagram syntax

**Content feels dry/boring**:
1. Add more analogies and examples
2. Use more direct address ("Imagine you're...")
3. Include surprising statistics
4. Ask rhetorical questions
5. Connect to reader experiences
6. Add enthusiasm (without hyperbole)

## Resources

**Readability Tools**:
- https://readabilityformulas.com/
- https://hemingwayapp.com/

**Writing Guides**:
- [Inverted Pyramid Writing](https://www.nngroup.com/articles/inverted-pyramid/)
- [Plain Language Guidelines](https://www.plainlanguage.gov/)
- [Docusaurus Markdown Features](https://docusaurus.io/docs/markdown-features)

**Reference Materials**:
- research.md (comprehensive findings)
- content-outline.md (detailed section breakdown)
- spec.md (requirements and success criteria)
- plan.md (Constitution compliance and constraints)
