# Diagram Assets for Module 1: ROS 2

This directory contains diagrams used in Module 1 chapters.

## Required Diagrams

### Chapter 1: Introduction
- **ros2-architecture.png** - ROS 2 as nervous system diagram
  - Shows sensors at top, ROS 2 layer in middle, actuators at bottom, AI brain on side
  - Arrows showing data flow: sensors → ROS 2 → AI Brain, AI Brain → ROS 2 → Actuators
  - Alt text: "Diagram showing ROS 2 as central communication layer connecting sensors at top, AI brain on side, and actuators at bottom, similar to nervous system connecting body parts"

### Chapter 2: Nodes
- **node-communication.svg** - Mermaid diagram (embedded in chapter)
  - Camera Node → Vision Node → Navigation Node → Leg Control Node

### Chapter 3: Communication Patterns
- **communication-patterns.png** - Comparison chart
  - Side-by-side comparison of topics, services, and actions

### Chapter 4: rclpy
- **ai-rclpy-hardware.svg** - Mermaid diagram (embedded in chapter)
  - Python AI → rclpy node → Robot hardware flow

### Chapter 5: URDF
- **urdf-structure.png** - Humanoid skeleton diagram
  - Shows links and joints labeled with humanoid arm structure

## Creating Diagrams

Diagrams can be created using:
- **Static images**: draw.io, Figma, hand-drawn + scan
- **Mermaid**: Text-based diagrams embedded directly in MDX (for flowcharts)

All diagrams should:
- Be high contrast for accessibility
- Include descriptive alt text
- Be max 800px wide for mobile responsiveness
- Use simple, uncluttered visuals (5-7 elements max)
