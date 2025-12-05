# Chapter Contracts Summary: Chapters 2-5

This document summarizes the contracts for chapters 2-5. Full detailed contracts follow the same structure as chapter1-introduction.md.

---

## Chapter 2: Nodes - The Building Blocks

**Word Count**: 850-950 words | **Sidebar Position**: 2

### Learning Objectives
1. Explain what a node is (independent program performing one task)
2. Describe why robots use multiple nodes instead of one big program
3. Identify nodes in a humanoid robot system (camera node, vision node, control node)
4. Explain how nodes communicate without sharing memory

### Key Concepts
- Node definition: Independent process/program
- Modularity: Each node has one clear job
- Isolation: Nodes don't share memory (intentional design)
- Message passing: Communication through ROS 2 topics/services

### Diagram
**Title**: "Node Communication in a Humanoid Robot"
**Type**: Mermaid flowchart
**Content**: Camera Node → Vision Node → Navigation Node → Leg Control Node (with topic labels on arrows)

### Humanoid Examples
1. **Head system**: Camera node (captures images) + Vision node (detects objects) working together
2. **Balance system**: IMU node (measures tilt) + Control node (adjusts posture)
3. **Manipulation**: Force sensor node + Gripper control node (adjust grip strength)

### Terms to Define
- Node, process, modularity, isolation, fault tolerance

---

## Chapter 3: Communication Patterns

**Word Count**: 1,000-1,200 words | **Sidebar Position**: 3

### Learning Objectives
1. Explain the three ROS 2 communication patterns: topics, services, actions
2. Identify which pattern fits different humanoid robot scenarios
3. Describe the publish-subscribe model for topics
4. Explain Quality of Service (QoS) tradeoffs (reliability vs. speed)

### Key Concepts
- **Topics**: Continuous data streams (pub-sub pattern)
  - Example: Balance sensor publishing tilt data 100Hz
- **Services**: Request-response (query current state)
  - Example: "What's your battery level?" → response
- **Actions**: Long-running tasks with feedback and cancellation
  - Example: "Walk forward 5 meters" with progress updates
- **QoS**: Reliability settings (guaranteed delivery vs. best effort)

### Diagram
**Title**: "Three Communication Patterns Compared"
**Type**: Static PNG table/comparison chart
**Content**: Side-by-side comparison showing when to use each pattern

### Humanoid Examples
1. **Topic**: Camera streaming images to vision system (continuous)
2. **Service**: Navigation asks "Am I close to obstacle?" (one-time query)
3. **Action**: "Pick up that cup" with feedback ("reaching... grasping... lifting...")

### Terms to Define
- Topic, publisher, subscriber, service, action, QoS, pub-sub pattern

---

## Chapter 4: Connecting AI with rclpy

**Word Count**: 850-950 words | **Sidebar Position**: 4

### Learning Objectives
1. Explain what rclpy is (Python client library for ROS 2)
2. Describe why Python is important for AI-robot integration
3. Explain how Python AI code becomes a ROS 2 node using rclpy
4. Identify the flow from AI model to robot hardware through ROS 2

### Key Concepts
- rclpy: Python bindings for ROS 2
- Why Python: Dominant AI/ML ecosystem (PyTorch, TensorFlow)
- AI as publisher: Vision model publishes object detections
- AI as subscriber: Planner receives sensor data, publishes commands
- Bridge concept: Python AI ↔ rclpy ↔ Robot hardware

### Diagram
**Title**: "AI-rclpy-Hardware Flow"
**Type**: Mermaid sequence diagram
**Content**: Python Vision Model → rclpy node → Object Detection Topic → rclpy node → Navigation System → Motor Commands

### Humanoid Examples
1. **Vision-based navigation**: PyTorch object detector → rclpy publishes detections → Navigation subscribes → Plans path
2. **Grasp planning**: AI predicts grip points → rclpy publishes grasp pose → Arm controller executes
3. **Voice control**: Whisper transcription → rclpy publishes text → NLU node parses intent → Action execution

### Terms to Define
- rclpy, client library, bindings, AI/ML ecosystem

---

## Chapter 5: Describing Robot Bodies (URDF)

**Word Count**: 850-950 words | **Sidebar Position**: 5

### Learning Objectives
1. Explain what URDF is (Unified Robot Description Format)
2. Describe why robots need a structured body description
3. Identify key URDF elements: links (rigid bodies) and joints (connections)
4. Explain how URDF enables simulation and motion planning

### Key Concepts
- URDF: XML format describing robot physical structure
- Purpose: Simulation, visualization, motion planning
- Links: Rigid body parts (upper arm, forearm, hand)
- Joints: Connections defining movement (revolute, prismatic, fixed)
- Joint specifications: Limits, axis of rotation, damping

### Diagram
**Title**: "Humanoid Arm URDF Structure"
**Type**: Static SVG
**Content**: Skeleton diagram of humanoid arm showing links and joints with labels (shoulder 3-DOF, elbow 1-DOF, wrist 2-DOF)

### Humanoid Examples
1. **Arm structure**: Shoulder (3 joints: pitch/roll/yaw) → Elbow (1 joint: pitch) → Wrist (2 joints: pitch/roll)
2. **Leg structure**: Hip (3-DOF) → Knee (1-DOF) → Ankle (2-DOF)
3. **Simulation use**: URDF loaded into Gazebo or Isaac Sim for testing without hardware

### Terms to Define
- URDF, link, joint, DOF (degrees of freedom), revolute, prismatic, simulation

---

## Word Count Distribution

| Chapter | Target Words | Cumulative |
|---------|-------------|------------|
| Ch1: Introduction | 850-950 | 900 |
| Ch2: Nodes | 850-950 | 1,800 |
| Ch3: Communication | 1,000-1,200 | 2,900 |
| Ch4: rclpy | 850-950 | 3,800 |
| Ch5: URDF | 850-950 | 4,700 |
| **Total** | **4,400-5,000** | **4,700 avg** |

This distribution meets the constitution requirement of 4,000-6,000 words total.

---

## Common Elements Across All Chapters

### Frontmatter Pattern
```yaml
---
id: chapter{N}-{slug}
title: "Chapter {N}: {Title}"
sidebar_label: "{Short Label}"
sidebar_position: {N}
description: "{One sentence summary}"
keywords: [{5-7 terms}]
---
```

### Standard Structure
1. Learning Objectives (3-5 bullets)
2. Introduction (context + preview)
3. Core Concept Explanation
4. Diagram (with caption and alt text)
5. Detailed Exploration
6. Humanoid Examples (2-3)
7. Summary (2-3 sentences)
8. Learning Checkpoint (:::tip with reflection questions)

### Quality Requirements
- 5-6 grade reading level (Flesch-Kincaid verified)
- All technical terms defined on first use
- At least 1 diagram per chapter
- 2-3 humanoid robot examples
- Admonitions used (:::note for concepts, :::tip for checkpoints)
- No installation or coding instructions
- Builds successfully in Docusaurus

---

## Glossary Coverage

**Total Terms to Define**: ~25-30 terms across all chapters

**Ch1**: ROS 2, middleware, node (brief)
**Ch2**: Node (full), process, modularity, isolation, fault tolerance
**Ch3**: Topic, publisher, subscriber, service, action, QoS, pub-sub
**Ch4**: rclpy, client library, bindings, AI/ML ecosystem
**Ch5**: URDF, link, joint, DOF, revolute, prismatic, simulation

All terms will be defined in-text on first use AND added to central glossary (docs/glossary.md).

---

## Next Steps

1. Use these contracts to guide content creation
2. Write each chapter following the standard structure
3. Create diagrams per specifications
4. Validate quality checklist for each chapter
5. Build glossary as terms are introduced
6. Test Docusaurus build after each chapter
