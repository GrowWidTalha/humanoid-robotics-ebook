---
id: glossary
title: "Glossary"
sidebar_label: "Glossary"
sidebar_position: 100
description: "Definitions of key terms used throughout the Physical AI & Humanoid Robotics textbook"
keywords: [glossary, definitions, terminology, ros2, robotics, ai]
---

# Glossary

This glossary defines key terms used throughout the textbook. Terms are listed alphabetically with simple definitions, examples, and references to where they're first introduced.

---

## A

### Action
**Definition**: A pattern for long-running, goal-oriented tasks with feedback. Actions allow robots to do complex jobs that take time and report progress along the way.

**Example**: When a humanoid robot receives a command to "walk forward 5 meters," it uses an action. The robot reports progress ("1 meter done... 2 meters done...") and can be stopped if needed.

**First Introduced**: Module 1, Chapter 3

---

## J

### Joint
**Definition**: A connection between two links (body parts) that defines how they can move relative to each other.

**Example**: A humanoid robot's elbow is a revolute joint that allows the forearm to rotate relative to the upper arm, like a hinge.

**First Introduced**: Module 1, Chapter 5

---

## L

### Link
**Definition**: A rigid body part of a robot that doesn't bend or flex.

**Example**: In a humanoid robot's arm, the upper arm and forearm are separate links. They're solid pieces connected by joints.

**First Introduced**: Module 1, Chapter 5

---

## M

### Middleware
**Definition**: Software that sits between different programs and helps them communicate with each other.

**Example**: ROS 2 is middleware. It helps the camera program send images to the vision program without those programs needing to know the details of how to connect.

**First Introduced**: Module 1, Chapter 1

### Modularity
**Definition**: The practice of designing systems as independent, interchangeable components where each part has one clear responsibility.

**Example**: In ROS 2, each node is modular - the camera node only handles capturing images, the vision node only processes images, and the control node only manages motors. This makes the system easier to understand and maintain.

**First Introduced**: Module 1, Chapter 2

---

## N

### Node
**Definition**: An independent program that performs one specific task in a robot system. Each node runs separately and communicates with other nodes through ROS 2.

**Example**: A camera node captures images. A vision node processes those images to detect objects. Each does one job well.

**First Introduced**: Module 1, Chapter 2

---

## C

### Client Library
**Definition**: A software library that provides an interface for programs written in a specific language to interact with a system. Client libraries translate function calls in one language to commands the system understands.

**Example**: rclpy is a client library that allows Python programs to interact with ROS 2. It translates Python function calls into ROS 2 operations like publishing messages or subscribing to topics.

**First Introduced**: Module 1, Chapter 4

---

## F

### Fault Tolerance
**Definition**: The ability of a system to continue operating even when parts of it fail. Fault-tolerant systems isolate failures to prevent them from cascading.

**Example**: In a ROS 2 humanoid robot, if the speech recognition node crashes, the robot can still walk and maintain balance because those functions run in separate nodes.

**First Introduced**: Module 1, Chapter 2

---

## P

### Process
**Definition**: An independent program running on a computer's operating system. Each process has its own memory space and cannot directly access another process's data.

**Example**: Each ROS 2 node runs as a separate process. The camera node and vision node are different processes that communicate through ROS 2 messages rather than sharing memory.

**First Introduced**: Module 1, Chapter 2

### Publisher
**Definition**: A node that sends data to a topic. Publishers put information out for any interested node to receive.

**Example**: A balance sensor node publishes tilt measurements to a "balance_data" topic 100 times per second.

**First Introduced**: Module 1, Chapter 3

---

## Q

### Quality of Service (QoS)
**Definition**: Settings that control how reliably and quickly messages are delivered between nodes. QoS lets you choose between guaranteed delivery (slower) and best-effort delivery (faster).

**Example**: A humanoid's balance sensor might use best-effort QoS because new data arrives constantly and missing one measurement isn't critical.

**First Introduced**: Module 1, Chapter 3

---

## R

### rclpy
**Definition**: The Python client library for creating ROS 2 nodes and interacting with the ROS 2 ecosystem. It's the bridge between Python AI code and robot systems.

**Example**: A PyTorch vision model uses rclpy to publish object detections that the robot's navigation system can read.

**First Introduced**: Module 1, Chapter 4

### ROS 2 (Robot Operating System 2)
**Definition**: Middleware that helps different robot programs communicate with each other. ROS 2 is not an operating system like Windows or Linux - it runs on top of an OS.

**Example**: ROS 2 lets a humanoid robot's camera send images to its vision system, which sends detections to its navigation system, which sends commands to its motors - all coordinated smoothly.

**First Introduced**: Module 1, Chapter 1

---

## S

### Service
**Definition**: A request-response communication pattern for queries. One node asks a question, another node responds.

**Example**: A navigation system might ask a battery monitor node "What's your battery level?" and receive a response like "75%".

**First Introduced**: Module 1, Chapter 3

### Subscriber
**Definition**: A node that receives data from a topic. Subscribers listen for information that publishers send.

**Example**: A leg control node subscribes to the "balance_data" topic to receive tilt measurements and adjust the humanoid's posture.

**First Introduced**: Module 1, Chapter 3

---

## T

### Topic
**Definition**: A named channel for streaming data between nodes. Topics use a publish-subscribe pattern where publishers send data and subscribers receive it.

**Example**: A "camera_images" topic carries image data from a camera node to any vision processing nodes that subscribe to it.

**First Introduced**: Module 1, Chapter 3

---

## U

### URDF (Unified Robot Description Format)
**Definition**: An XML format that describes a robot's physical structure - its links, joints, sensors, and how they're connected.

**Example**: A humanoid robot's URDF file describes its body: torso (link), shoulder joint, upper arm (link), elbow joint, forearm (link), and so on.

**First Introduced**: Module 1, Chapter 5

---

*This glossary is updated as new terms are introduced in each module. Terms marked with asterisks (*) are defined in later modules.*
