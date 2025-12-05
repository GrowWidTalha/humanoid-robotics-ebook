# Quickstart Guide: Creating Module 1 Content

**Audience**: Content authors creating educational chapters for Module 1
**Purpose**: Step-by-step workflow for writing, validating, and building chapters
**Last Updated**: 2025-12-04

---

## Prerequisites

Before creating content, ensure you have:

- [ ] Read the [constitution](./../../../.specify/memory/constitution.md) (understand the 7 principles)
- [ ] Reviewed [spec.md](./spec.md) (understand module learning goals)
- [ ] Read [research.md](./research.md) (understand technical decisions)
- [ ] Reviewed [data-model.md](./data-model.md) (understand content structure)
- [ ] Read chapter contracts in `contracts/` directory
- [ ] Access to Docusaurus environment (Node.js, npm installed)

---

## Step 1: Create New Chapter File

### Location
All chapters go in: `docs/module1-ros2/`

### File Naming Convention
- Format: `chapter{N}-{slug}.mdx`
- Examples:
  - `chapter1-introduction.mdx`
  - `chapter2-nodes.mdx`
  - `chapter3-communication.mdx`

### Create File
```bash
cd /mnt/d/class/humanoid-robots-book
touch docs/module1-ros2/chapter1-introduction.mdx
```

---

## Step 2: Add Frontmatter

All chapters **must** start with YAML frontmatter. Copy and customize:

```yaml
---
id: chapter1-introduction
title: "Chapter 1: Introduction to ROS 2"
sidebar_label: "Introduction"
sidebar_position: 1
description: "Discover what ROS 2 is and why it's essential for coordinating humanoid robots."
keywords: [ros2, robotics, middleware, humanoid, nervous-system, coordination]
---
```

### Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `id` | Unique identifier | `chapter1-introduction` |
| `title` | Full chapter title | `"Chapter 1: Introduction to ROS 2"` |
| `sidebar_label` | Short sidebar name | `"Introduction"` |
| `sidebar_position` | Order in sidebar (1-6) | `1` |
| `description` | One sentence summary | `"Discover what ROS 2 is..."` |
| `keywords` | SEO and search terms (5-7) | `[ros2, robotics, middleware]` |

### Special Characters
If your title includes colons `:`, **quote the entire value**:
```yaml
title: "Chapter 1: Introduction to ROS 2"  # GOOD
title: Chapter 1: Introduction to ROS 2    # BAD - will break parser
```

---

## Step 3: Write Content Following Structure

### Standard Chapter Structure

```markdown
# Chapter {N}: {Title}

## Learning Objectives

By the end of this chapter, you will be able to:

- Objective 1 (action verb + specific outcome)
- Objective 2
- Objective 3
(3-5 objectives total)

## Introduction

(2-3 paragraphs: context + what reader will learn)

## {Main Section 1}

(Core concept explanation with simple language)

:::note Key Concept
(Important definition or idea)
:::

### {Subsection}

(Detailed exploration)

**Diagram**: (Insert diagram here - see Step 4)

**Example**: (Humanoid robot scenario)

## {Main Section 2}

(Continue building knowledge)

:::tip Think About It
(Reflection question to engage reader)
:::

## Summary

(2-3 sentences reinforcing key takeaways)

:::tip Learning Checkpoint
Before moving to the next chapter, try to explain:
1. (Question related to objective 1)
2. (Question related to objective 2)
3. (Question related to objective 3)
:::
```

---

## Step 4: Add Diagrams

### Option A: Mermaid Diagrams (Recommended for Flowcharts)

Embed directly in MDX:

```markdown
```mermaid
graph LR
    A[Camera Node] -->|Image Topic| B[Vision Node]
    B -->|Object Detections| C[Navigation Node]
    C -->|Motor Commands| D[Leg Control Node]
```\u200b```

**Figure 1**: Node communication in a humanoid robot
```

### Option B: Static Images (For Complex Diagrams)

1. Create diagram (use draw.io, Figma, or hand-drawn + scan)
2. Save as PNG or SVG in `docs/module1-ros2/assets/`
3. Embed with Markdown:

```markdown
![ROS 2 Architecture](./assets/ros2-architecture.png)

**Figure 1**: ROS 2 as the robot's nervous system
```

### Diagram Requirements
- **Alt text mandatory**: Describe diagram for screen readers
- **Caption required**: Brief description below image
- **Size limit**: Max 800px wide (responsive)
- **High contrast**: Use colorblind-friendly palette
- **Simplicity**: 5-7 elements max per diagram

---

## Step 5: Use Admonitions

Docusaurus supports 5 admonition types. Use them to highlight important content:

### `:::note` - Key Concepts and Definitions
```markdown
:::note Key Concept
ROS 2 is middleware - it sits between the robot's hardware and the AI brain.
:::
```

### `:::tip` - Learning Checkpoints and Best Practices
```markdown
:::tip Learning Checkpoint
Can you explain how topics differ from services? Try answering before reading further.
:::
```

### `:::info` - Additional Context
```markdown
:::info Interesting Fact
ROS 2 was released in 2017 and is now used by thousands of robotics companies worldwide.
:::
```

### `:::warning` - Common Misconceptions
```markdown
:::warning Common Mistake
ROS 2 is **not** an operating system like Windows or Linux. It's middleware that runs on top of an OS.
:::
```

### `:::danger` - Critical Errors (Rare in Textbook)
```markdown
:::danger
(Use sparingly - mostly for informational textbooks, not critical errors)
:::
```

---

## Step 6: Define Technical Terms

**Constitution Requirement**: All technical terms **must** be defined on first use.

### In-Text Definition (First Mention)
```markdown
A **node** (an independent program that performs one specific task) sends messages to other nodes.
```

### Glossary Entry (Add to docs/glossary.md)
```markdown
## Node

**Definition**: A node is an independent program that performs one specific task in a robot system. Each node runs separately and communicates with other nodes through ROS 2.

**Example**: A camera node captures images, while a vision node processes those images to detect objects.

**First Introduced**: Module 1, Chapter 2

**Related Terms**: [Topic](#topic), [Publisher](#publisher), [Subscriber](#subscriber)
```

---

## Step 7: Validate Content Quality

### Checklist Before Publishing

- [ ] **Frontmatter**: All fields complete and valid
- [ ] **Learning Objectives**: 3-5 objectives stated at chapter start
- [ ] **Word Count**: 800-1,200 words (use `wc -w chapter.mdx`)
- [ ] **Reading Level**: 5-6 grade (verify with [Hemingway Editor](https://hemingwayapp.com/))
- [ ] **Diagrams**: At least 1 diagram included with caption and alt text
- [ ] **Examples**: 2-3 humanoid robot scenarios present
- [ ] **Terms Defined**: All technical terms defined on first mention
- [ ] **Admonitions**: At least 1 admonition used appropriately
- [ ] **Learning Checkpoint**: Reflection questions at end (:::tip)
- [ ] **No Code/Installation**: No step-by-step setup or coding tutorials
- [ ] **Glossary Updated**: New terms added to docs/glossary.md

### Readability Verification

1. Copy chapter text (without frontmatter/code blocks)
2. Paste into [Hemingway Editor](https://hemingwayapp.com/)
3. Check grade level: Should be **Grade 5 or 6**
4. Simplify any sentences marked "hard to read" (red highlights)
5. Replace complex words (purple highlights) with simpler alternatives

**Target Metrics**:
- Grade level: 5-6
- Sentences: Mostly green and yellow (avoid red)
- Adverbs: Minimize (purple highlights)

---

## Step 8: Build and Preview

### Local Development Server

1. Navigate to project root:
   ```bash
   cd /mnt/d/class/humanoid-robots-book
   ```

2. Start Docusaurus:
   ```bash
   npm start
   ```

3. Open browser to `http://localhost:3000`

4. Navigate to your chapter in sidebar

5. Verify:
   - Frontmatter renders correctly (title, sidebar position)
   - Diagrams display properly
   - Admonitions styled correctly
   - Mobile responsiveness (resize browser window)
   - Links work (internal cross-references)

### Production Build Test

Before committing, ensure production build succeeds:

```bash
npm run build
```

**Expected Output**: `Success! Generated static files in build/`

**If Errors**:
- Check frontmatter syntax (quoted strings for colons)
- Verify all image paths correct
- Ensure no unclosed code blocks or admonitions

---

## Step 9: Word Count Tracking

### Per-Chapter Word Count

```bash
# Count words in single chapter (excludes frontmatter and code)
grep -v '^---' docs/module1-ros2/chapter1-introduction.mdx | \
  grep -v '^```' | \
  wc -w
```

### Module Total Word Count

```bash
# Count words across all chapters
grep -v '^---' docs/module1-ros2/*.mdx | \
  grep -v '^```' | \
  wc -w
```

**Target**: Module total should be **4,000-6,000 words**.

---

## Step 10: Commit and Document

### Git Workflow

```bash
# Stage chapter file
git add docs/module1-ros2/chapter1-introduction.mdx

# Stage any diagrams
git add docs/module1-ros2/assets/*.png

# Commit with descriptive message
git commit -m "docs(module1): add chapter 1 - introduction to ROS 2

- Introduce ROS 2 as middleware
- Use nervous system analogy
- Include architecture diagram
- Define key terms (ROS 2, middleware, node)
- Word count: 875 words
- Reading level: Grade 5.8"

# Push to remote
git push origin 001-ros2-module
```

---

## Common Issues and Solutions

### Issue: Frontmatter Parsing Error

**Symptom**: Build fails with "Error parsing frontmatter"

**Solution**: Quote any values containing special characters (colons, brackets):
```yaml
title: "Chapter 1: Introduction"  # GOOD
description: "Learn how ROS 2 works [middleware]"  # GOOD
```

### Issue: Diagram Not Displaying

**Symptom**: Broken image icon or missing diagram

**Solutions**:
- Verify file path is relative: `./assets/diagram.png` not `/assets/diagram.png`
- Check file exists in `docs/module1-ros2/assets/`
- Ensure file extension matches (case-sensitive: `.png` not `.PNG`)

### Issue: Reading Level Too High

**Symptom**: Hemingway Editor shows Grade 8+

**Solutions**:
- Shorten sentences (split at commas or semicolons)
- Replace complex words:
  - "utilize" → "use"
  - "facilitate" → "help"
  - "comprises" → "includes"
- Use active voice: "The robot sends data" not "Data is sent by the robot"
- Add simple analogies to explain technical concepts

### Issue: Word Count Too Low/High

**Symptom**: Chapter under 800 or over 1,200 words

**Solutions**:
- **Too low**: Add more examples, expand diagram explanations, add edge cases section
- **Too high**: Remove redundancy, consolidate similar points, move advanced topics to later chapters

---

## Quality Standards Summary

| Requirement | Target | Verification Method |
|-------------|--------|---------------------|
| Word count | 800-1,200 per chapter | `wc -w` command |
| Reading level | Grade 5-6 | Hemingway Editor |
| Diagrams | 1+ per chapter | Visual inspection |
| Examples | 2-3 humanoid scenarios | Content review |
| Terms defined | All on first use | Manual review |
| Admonitions | 1+ per chapter | Content review |
| Learning objectives | 3-5 per chapter | Count bullets |
| Docusaurus build | Success | `npm run build` |
| Mobile responsive | Works on small screens | Browser resize test |

---

## Resources

### Tools
- [Hemingway Editor](https://hemingwayapp.com/) - Readability checking
- [Docusaurus Documentation](https://docusaurus.io/docs) - Official docs
- [Mermaid Live Editor](https://mermaid.live/) - Diagram prototyping
- [draw.io](https://app.diagrams.net/) - Complex diagram creation

### Internal Documentation
- [Constitution](./../../../.specify/memory/constitution.md) - Governing principles
- [Spec](./spec.md) - Module requirements
- [Research](./research.md) - Technical decisions
- [Data Model](./data-model.md) - Content structure
- [Chapter Contracts](./contracts/) - Detailed outlines

### Getting Help
- Review existing chapters as examples
- Check constitution for quality standards
- Consult chapter contracts for specific guidance
- Test locally before committing (`npm start`)

---

## Next Steps

1. Choose a chapter to write (start with Chapter 1)
2. Review that chapter's contract (`contracts/chapter1-introduction.md`)
3. Create MDX file with frontmatter
4. Write content following standard structure
5. Add diagrams and humanoid examples
6. Validate quality checklist
7. Build and preview locally
8. Commit with descriptive message
9. Move to next chapter

**Goal**: Complete all 5 chapters totaling 4,000-6,000 words, meeting all constitution principles.
