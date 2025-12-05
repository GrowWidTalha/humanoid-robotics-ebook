# Chapter Writer Skill

## Purpose
Write educational textbook chapters for the Physical AI & Humanoid Robotics textbook following established patterns for structure, style, and quality.

## When to Use This Skill
- Creating new chapter content for any module
- Revising existing chapters to match quality standards
- Ensuring consistency across educational content

## Chapter Writing Patterns

### 1. Structure Template

Every chapter must follow this exact structure:

```markdown
---
id: chapter{N}-{slug}
title: "Chapter {N}: {Title}"
sidebar_label: "{Short Label}"
sidebar_position: {N}
description: "{One-sentence chapter summary}"
keywords: [{keyword1}, {keyword2}, {keyword3}, ...]
---

# Chapter {N}: {Title}

## Learning Objectives

By the end of this chapter, you will be able to:

1. {Action verb} {specific outcome}
2. {Action verb} {specific outcome}
3. {Action verb} {specific outcome}
4. {Action verb} {specific outcome}

---

## {Section 1: Introduction/Motivation}

{Problem statement or motivation - 100-150 words}

---

## {Section 2: Core Concept}

{Main explanation - 250-350 words}

### {Subsection if needed}

{Details}

:::note Key Concept
{Critical takeaway in 1-2 sentences}
:::

---

## {Section 3: Deeper Dive}

{Extended explanation with examples - 250-350 words}

:::warning Common Misconception
{Clarify what students might misunderstand}
:::

---

## {Section 4: Real-World Examples}

{Humanoid robot examples - 150-250 words}

:::tip Practical Guidance
{Actionable advice or pattern selection guide}
:::

---

## Summary

{Recap key points - 100-150 words}

:::tip Learning Checkpoint
Before continuing, test your understanding:
1. {Question 1}
2. {Question 2}
3. {Question 3}

*Answers: 1={Answer}, 2={Answer}, 3={Answer}*
:::
```

### 2. Word Count Guidelines

**Target Range**: 850-950 words per chapter (flexible policy)
- **Minimum acceptable**: Within 2% of target minimum (833 words for 850 target)
- **Maximum acceptable**: Within 10-15% of target maximum (1,045-1,092 words for 950 target)
- **Avoid**: Excessive iteration on minor word count differences
- **Focus**: Content quality and completeness over exact counts

**Historical Chapter Lengths**:
- Chapter 1: 1,114 words (131% of 850 minimum)
- Chapter 2: 1,378 words (162% of 850 minimum)
- Chapter 3: 1,837 words (183% of 1,000 minimum)
- Chapter 4: 1,497 words (176% of 850 minimum)
- Chapter 5: 966 words (114% of 850 minimum)

**Lesson**: Chapters naturally run long due to examples. Aim for target, accept 10-20% variance.

### 3. Writing Style Rules

**Reading Level**: Grade 5-6 (Flesch-Kincaid)
- Use short sentences (10-20 words average)
- Avoid jargon or define all technical terms
- Use active voice
- Choose simple words over complex alternatives

**Tone**:
- Conversational and engaging
- Address reader as "you"
- Ask rhetorical questions to engage thinking
- Use analogies to everyday experiences
- Maintain enthusiasm without being overly casual

**Structure**:
- One idea per paragraph
- Paragraphs: 2-5 sentences
- Use transitions between sections
- Build complexity gradually

**Formatting**:
- **Bold** for term definitions on first use
- *Italic* for emphasis (sparingly)
- Lists for enumeration (not long paragraphs)
- Code blocks ONLY if showing conceptual structure (not implementation)
- NO emojis unless explicitly requested

### 4. Technical Term Handling

**First Use Pattern**:
```markdown
A **topic** is a named channel where nodes can publish data continuously.
```

**Inline Definition**: Define immediately when introduced
**Glossary Entry**: Add to docs/glossary.md with:
- Definition (1-2 sentences)
- Example (humanoid robot context)
- First Introduced: Module X, Chapter Y

**Consistency**: Use exact same terminology across chapters
- "ROS 2" (not "ROS2" or "ros2")
- "node" (lowercase for common noun)
- "publish-subscribe" (with hyphen)

### 5. Admonitions Usage

Use Docusaurus admonitions for emphasis:

**:::note Key Concept**
- Use for: Critical concepts students must understand
- Frequency: 1-2 per chapter
- Content: 1-3 sentences, crystal clear takeaway

**:::warning Common Misconception**
- Use for: Things students often misunderstand
- Frequency: 0-1 per chapter
- Content: State misconception, then correct it

**:::tip Practical Guidance**
- Use for: Decision-making guides, pattern selection, best practices
- Frequency: 1-2 per chapter
- Content: Actionable advice in bullet points

**Example**:
```markdown
:::tip Pattern Selection Guide
- **Topics**: Continuous data streams (sensor readings, camera images)
- **Services**: One-time queries (check battery, compute path)
- **Actions**: Long tasks with feedback (walk, pick up object)
:::
```

### 6. Examples and Analogies

**Every Concept Needs**:
1. **Analogy to everyday life** (first explanation)
2. **Humanoid robot example** (primary technical example)
3. **Additional example** (alternative scenario)

**Analogy Pattern**:
```markdown
Think about {everyday situation}. {How it works}. {Parallel to technical concept}.

ROS 2 {technical concept} works the same way: {mapping}
```

**Example**:
- Topics → Social media broadcasting
- Services → Asking for directions
- Actions → Food delivery tracking

**Humanoid Robot Examples Must**:
- Be concrete and visual (reader can imagine it)
- Use specific robot parts (camera, IMU, motors, legs)
- Show complete flow (sensor → processing → action)
- Connect to chapter's main concept

### 7. Learning Objectives

**Format**: "By the end of this chapter, you will be able to:"

**Action Verbs** (Bloom's Taxonomy):
- **Remember**: Identify, List, Recognize, Name
- **Understand**: Explain, Describe, Summarize, Compare
- **Apply**: Use, Demonstrate, Implement, Solve
- **Analyze**: Differentiate, Distinguish, Examine

**Rules**:
- Exactly 4 objectives per chapter
- Mix cognitive levels (2 Understand, 1 Remember, 1 Apply/Analyze)
- Be specific and measurable
- Avoid vague verbs (know, learn, understand basics)

**Good Examples**:
- "Explain what ROS 2 is and identify its role as middleware"
- "Describe the three ROS 2 communication patterns and when to use each"
- "Identify which joint type to use for different robot movements"

### 8. Visual Elements

**Mermaid Diagrams**:
- Use for: System architecture, data flow, sequences
- Keep simple: 4-6 nodes maximum
- Always include caption: "*Figure N: {Description}*"
- Place after explanation, not before

**Diagram Types**:
- `graph LR`: Linear data flow (node communication)
- `sequenceDiagram`: Message passing over time
- `flowchart`: Decision trees or processes

**Example**:
```markdown
```mermaid
graph LR
    A[Camera Node] -->|Image Topic| B[Vision Node]
    B -->|Detections| C[Navigation Node]
```

*Figure 1: Nodes communicate by passing messages through topics*
```

### 9. Cross-Referencing

**Reference Previous Chapters**:
```markdown
In Chapter {N}, you learned {concept}. Now we'll explore {next concept}.
```

**Forward References**:
```markdown
In the next chapter, you'll learn about {future topic}.
```

**Within Chapter**:
```markdown
We'll explore this communication in detail in Chapter 3.
```

**Rules**:
- Always reference by chapter number (not "previous chapter")
- Remind reader of prerequisite concept briefly
- Create logical narrative flow through the module

### 10. Learning Checkpoints

**Format**: :::tip Learning Checkpoint at end of Summary section

**Structure**:
```markdown
:::tip Learning Checkpoint
Before continuing, test your understanding:
1. {Question testing core concept}
2. {Question testing application}
3. {Question testing distinction/comparison}

*Answers: 1={Brief answer}, 2={Brief answer}, 3={Brief answer}*
:::
```

**Question Types**:
- Recall: "What is X?"
- Application: "Which pattern would you use for Y?"
- Analysis: "What's the difference between X and Y?"

**Answer Format**: Brief but complete (5-10 words)

### 11. Quality Checklist

Before considering a chapter complete, verify:

**Structure**:
- [ ] MDX frontmatter complete with all fields
- [ ] 4 learning objectives present
- [ ] Section dividers (---) used
- [ ] Summary section included
- [ ] Learning checkpoint with 3 questions

**Content**:
- [ ] Word count within acceptable range (target ±20%)
- [ ] All technical terms defined on first use
- [ ] At least 2 humanoid robot examples
- [ ] 1-2 analogies to everyday life
- [ ] Concepts build on previous chapters

**Style**:
- [ ] Grade 5-6 reading level maintained
- [ ] Active voice used throughout
- [ ] Short sentences and paragraphs
- [ ] Conversational tone (uses "you")
- [ ] No implementation code (conceptual only)

**Technical**:
- [ ] 1-2 :::note admonitions for key concepts
- [ ] 0-1 :::warning admonitions for misconceptions
- [ ] 1-2 :::tip admonitions for guidance
- [ ] Mermaid diagrams have captions
- [ ] Cross-references to other chapters

**Glossary**:
- [ ] Key terms added to docs/glossary.md
- [ ] Each term has definition, example, chapter reference
- [ ] Terminology consistent with existing chapters

### 12. Anti-Patterns (Avoid)

**Don't**:
- ❌ Write implementation code or tutorials
- ❌ Use emojis (unless user explicitly requests)
- ❌ Include specific ROS 2 commands or syntax
- ❌ Assume prior ROS 2 experience
- ❌ Use academic or overly formal language
- ❌ Create walls of text (long paragraphs)
- ❌ Skip examples for abstract concepts
- ❌ Use "we" (use "you" for reader, specific actors for examples)
- ❌ Leave technical terms undefined
- ❌ Over-iterate on minor word count differences

**Do**:
- ✅ Focus on concepts and understanding
- ✅ Use concrete, visual examples
- ✅ Define every technical term inline
- ✅ Keep language simple and clear
- ✅ Build complexity gradually
- ✅ Connect to real humanoid robot scenarios
- ✅ Test understanding with checkpoints
- ✅ Accept reasonable word count variance

## Workflow for New Chapter

### Phase 1: Planning (5 minutes)
1. Read chapter contract from tasks.md or plan.md
2. Identify: core concept, prerequisites, learning outcomes
3. Brainstorm: 2-3 humanoid robot examples, 1-2 analogies
4. Outline: 4-5 main sections with rough word allocation

### Phase 2: Writing (20-30 minutes)
1. **Frontmatter**: Fill in all metadata fields
2. **Learning Objectives**: Write 4 specific, measurable objectives
3. **Introduction**: Problem/motivation (100-150 words)
4. **Core Sections**: Explanation + examples (500-600 words total)
   - Define all technical terms inline
   - Add 1-2 :::note admonitions
   - Add 0-1 :::warning admonitions
5. **Real-World Examples**: Humanoid robot scenarios (150-250 words)
   - Add 1-2 :::tip admonitions
6. **Summary**: Recap key points (100-150 words)
7. **Learning Checkpoint**: 3 questions with answers

### Phase 3: Visual Enhancement (5-10 minutes)
1. Identify 1-2 concepts that need diagrams
2. Create Mermaid diagrams (simple, 4-6 nodes)
3. Add captions below each diagram
4. Review diagram clarity

### Phase 4: Quality Review (5-10 minutes)
1. **Word count check**: Within target ±20%?
2. **Reading level check**: Grade 5-6? (short sentences, simple words)
3. **Term check**: All technical terms defined?
4. **Example check**: 2+ humanoid robot examples?
5. **Admonition check**: 2-4 total admonitions?
6. **Cross-reference check**: References to other chapters?

### Phase 5: Glossary Update (5 minutes)
1. Identify 3-5 key terms from chapter
2. Add to docs/glossary.md if not present
3. Format: Definition, Example, "First Introduced: Module X, Chapter Y"
4. Verify alphabetical organization

### Phase 6: Integration (5 minutes)
1. Update module index with chapter link and description
2. Verify chapter appears in correct sidebar position
3. Check that frontmatter sidebar_position matches actual position
4. Update tasks.md to mark chapter tasks complete

## Example Chapter Analysis

### Chapter 3: Communication Patterns (Exemplar)

**What Made It Successful**:
- Clear structure: Introduction → 3 patterns → QoS → Summary
- Multiple examples per pattern (2 examples each for topics, services, actions)
- Consistent analogy: Social media/Directions/Delivery tracking
- Pattern comparison table in :::tip admonition
- Learning checkpoint tests pattern selection (application level)
- 979 words (97.9% of 1,000 target - within range)

**Pattern Breakdown**:
- Introduction (motivation): 150 words
- Topics section: 250 words (2 examples)
- Services section: 200 words (2 examples)
- Actions section: 200 words (2 examples)
- QoS section: 100 words
- Summary: 79 words

**Admonition Usage**:
- 1 :::note for publish-subscribe concept
- 1 :::tip for pattern selection guidance
- Total: 2 admonitions (ideal range)

**Technical Terms Defined**: Topic, publisher, subscriber, service, action, QoS, publish-subscribe pattern (7 terms)

## Common Pitfalls and Solutions

### Pitfall 1: Chapter Too Short
**Symptom**: Word count under 800 words
**Solution**: Add second example for each concept, expand analogy explanation

### Pitfall 2: Chapter Too Long
**Symptom**: Word count over 1,200 words
**Solution**: Cut redundant explanations, tighten sentences, remove tangential examples

### Pitfall 3: Too Abstract
**Symptom**: No concrete examples, reader can't visualize
**Solution**: Add specific humanoid robot scenario with sensor→AI→motor flow

### Pitfall 4: Too Technical
**Symptom**: Reading level above grade 8, complex jargon
**Solution**: Replace complex terms, break long sentences, add analogies

### Pitfall 5: Inconsistent Terminology
**Symptom**: Same concept called different names
**Solution**: Grep existing chapters for term usage, match exactly

### Pitfall 6: Missing Context
**Symptom**: Chapter doesn't connect to previous/next chapters
**Solution**: Add "In Chapter X..." references, explain prerequisites briefly

## Usage Examples

### Starting a New Chapter

**User Request**: "Write Chapter 6 about ROS 2 launch files"

**Assistant Response**:
1. Check tasks.md for chapter contract (word count, learning objectives, key concepts)
2. Plan structure: Introduction → What are launch files → Why use them → Humanoid example → Summary
3. Write following structure template
4. Add 2 humanoid robot examples (multi-node startup scenario)
5. Create 1 analogy (startup scripts, team assembly)
6. Add 1 Mermaid diagram (launch file structure)
7. Verify word count, reading level, term definitions
8. Add glossary entries for new terms
9. Update module index

### Revising an Existing Chapter

**User Request**: "Make Chapter 2 more engaging"

**Assistant Response**:
1. Read current Chapter 2
2. Identify areas to improve:
   - Add more concrete examples
   - Convert abstract explanations to analogies
   - Add :::note admonitions for key concepts
   - Simplify complex sentences
3. Maintain word count within ±10% of current
4. Verify reading level stays grade 5-6
5. Keep all existing technical accuracy

## Configuration for This Textbook

**Target Audience**:
- Students learning AI and robotics
- Engineers transitioning to Physical AI
- No prior ROS 2 experience assumed

**Educational Philosophy**:
- Concepts before implementation
- Understanding before coding
- Visual, concrete examples
- Progressive complexity

**Module Context**: Module 1 - The Robotic Nervous System (ROS 2)
- Focus: Communication and coordination
- Hardware: Humanoid robots
- AI Connection: Python-based AI systems

**Quality Standards**:
- Reading level: Grade 5-6 (Flesch-Kincaid)
- Word count flexibility: ±10-20% acceptable
- Terminology: Consistent with constitution.md and existing chapters
- Examples: Always humanoid robot context
- Accessibility: No prerequisites beyond basic programming concepts

## Integration with Project Workflow

This skill integrates with the Spec-Driven Development workflow:

1. **Constitution** → Defines principles (accessibility, visual clarity, modularity)
2. **Spec** → Defines learning outcomes and user stories
3. **Plan** → Defines chapter structure and contracts
4. **Tasks** → Breaks chapters into granular tasks
5. **Implementation** → Use this skill for actual chapter writing
6. **PHR** → Record chapter creation for learning

**When to Use This Skill**:
- During Phase 2-5 of implementation (content creation phases)
- When tasks.md shows chapter content creation tasks
- When revising chapters based on feedback

**Skill Output**:
- Complete MDX chapter file in docs/module{N}-{topic}/
- Updated glossary entries in docs/glossary.md
- Updated tasks.md with completed checkboxes
- Chapter ready for Docusaurus rendering

## Advanced Patterns

### Pattern: Layered Explanation
For complex concepts, use 3-layer approach:
1. **Analogy**: Everyday life parallel (1-2 sentences)
2. **Definition**: Technical but simple (1-2 sentences)
3. **Example**: Humanoid robot scenario (4-6 sentences)

### Pattern: Contrast for Clarity
When explaining multiple similar concepts:
1. Present each concept separately first
2. Add comparison table or :::tip with distinctions
3. Provide decision-making guidance

**Example**: Chapter 3 compared topics/services/actions with selection guide

### Pattern: Progressive Detail
Within a chapter:
1. Start with high-level overview (what it is)
2. Explain why it matters (motivation)
3. Show how it works (mechanism)
4. Provide multiple examples (application)
5. Summarize key points (consolidation)

### Pattern: Embedded Definitions
Don't break flow with "X is defined as...":
- ❌ "A node is defined as an independent program..."
- ✅ "A **node** is an independent program that..."

Bold the term, define it in same sentence, continue naturally.

## Maintenance and Updates

### When Chapters Need Revision

**Triggers for Revision**:
- User feedback indicates confusion
- Reading level test shows grade 8+ (too complex)
- Word count significantly outside range (>30% variance)
- Terminology inconsistent with other chapters
- Missing critical examples or analogies
- Cross-references broken due to chapter reorganization

**Revision Process**:
1. Read current chapter completely
2. Identify specific issues (list them)
3. Create revision plan (minimal changes to fix issues)
4. Update content
5. Re-verify quality checklist
6. Update PHR noting what was revised and why

### Consistency Maintenance

**Before Writing New Chapter**:
1. Grep existing chapters for related terminology
2. Check glossary.md for existing term definitions
3. Review previous chapter endings for forward references
4. Verify your chapter number and sidebar_position are correct

**After Writing New Chapter**:
1. Update module index.mdx with chapter summary
2. Verify previous chapter's "next chapter" reference points correctly
3. Cross-check new terminology doesn't conflict with existing
4. Update glossary with all new key terms

## Success Metrics

A successful chapter meets these criteria:

**Comprehension** (Primary Goal):
- Reader can answer learning checkpoint questions
- Reader can explain concept to someone else
- Reader can identify when to apply concept

**Accessibility** (Quality Standard):
- Grade 5-6 reading level maintained
- All technical terms defined inline
- Multiple examples provided
- Visual diagrams support understanding

**Consistency** (Integration Standard):
- Terminology matches existing chapters
- Style and tone match textbook voice
- Structure follows established template
- Cross-references are accurate

**Completeness** (Content Standard):
- Word count within acceptable range
- All contract requirements met
- Glossary entries added
- Tasks.md updated

## Version History

**v1.0** (2025-12-04): Initial skill creation based on Module 1 implementation patterns
- 5 chapters analyzed (Introduction, Nodes, Communication, rclpy, URDF)
- 6,792 total words of content examined
- Patterns extracted from Phase 2-6 implementation
- Quality standards established from actual chapter performance
