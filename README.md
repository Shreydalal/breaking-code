# Social Media Performance Analysis

## Overview

This repository contains the solution for the **Pre-Hackathon Assignment: Social Media Performance Analysis**. The task involves creating a basic analytics module using **Langflow** and **DataStax Astra DB** to analyze social media engagement data.

## Objective

The main goal is to:
1. Simulate and store engagement data in a database.
2. Analyze the performance of different post types (e.g., carousel, reels, static images).
3. Generate insights using GPT integration in Langflow.

## Tools Used

- **[DataStax Astra DB](https://www.datastax.com/)**: For database operations.
- **[Langflow](https://www.langflow.org/)**: For workflow creation and GPT integration.

## Features

1. **Engagement Data Simulation**:
   - A dataset simulating social media engagement metrics like likes, shares, and comments.
   - Data categorized by post types such as carousel, reels, and static images.

2. **Post Performance Analysis**:
   - A Langflow workflow accepts post types as input.
   - Queries Astra DB to calculate average engagement metrics for each post type.

3. **Insight Generation**:
   - Integration with GPT to provide actionable insights, such as:
     - *Carousel posts have 20% higher engagement than static posts.*
     - *Reels drive 2x more comments compared to other formats.*

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone github.com/Shreydalal/breaking-code
