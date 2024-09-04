# Job Recommendation System

## Overview
This project is a simple job recommendation system designed to match members to their ideal job based on their bios and job descriptions. The code fetches data from two public APIs (members and jobs) and uses keyword matching and location preferences to recommend jobs to each member.

## Installation Instructions

### Prerequisites
- Python 3.8+
- `requests` library (used for API requests)

### Steps to Install and Run:
Install dependencies: If you don't have the `requests` library installed, you can install it using pip:
```bash
pip install requests
```
Run the program: Simply run the `run_recommendations` Python script:
```bash
python run_recommendations.py
```
This will fetch the data from the APIs, process the member bios and job descriptions, and output job recommendations for each member.

## Problem Domain and Challenges

### Problem Description
The task was to implement a recommendation algorithm that matches members to jobs based on their bios. The provided member bios contained personal information and job preferences, while the job listings had titles and locations. The challenge was to determine the best-fit jobs for each member, considering both their keyword-based skillset or interest (inferred from the bio) and their location preferences.

### Key Challenges
- Unstructured Text Matching: One of the main challenges of this problem was extracting meaningful keywords from unstructured bio data and job titles. There was a need to parse member bios to identify key job-related words, and then match these to available job titles.

- Location Preferences: Another challenge was interpreting the location preferences expressed in the bios. Members sometimes provided nuanced preferences, such as "outside of London" or "relocate to London". Handling these distinctions in a systematic way required the implementation of a custom location preference matching system.

- Ambiguity in Bios: The bios could either have a one job keyword corresponding to one of several words in several job titles, or one that wasn't an exact word match for any of the words in the job title. As a result of this, keyword extension logic and partial matching had to be implemented to determine job relevance.

## Design Decisions and Approach

### Keyword Matching
For the keyword matching, I split job titles into individual words and used a simple word boundary regex to search for exact matches in member bios. To make the keyword matching more flexible, I added keyword extensions. For example, if a job title contained the word "designer", the matching process would also consider variations like "design" for better job-to-member alignment.

### Location Preference Handling
Location preferences posed an interesting challenge. For example, the phrase "outside of London" required a negative match (i.e., jobs not in London), while "relocate to London" indicated a preference for London-based jobs over an afore mentioned Location with a non-negative term. To handle this, I added logic to interpret these descriptors using pre-defined lists of negative and overriding positive phrases.

### Simplicity and Focus
The goal was to keep the solution simple and easy to follow while meeting the requirements. I avoided overcomplicating the logic with methods such as advanced natural language processing techniques, focusing instead on using straightforward text matching and logic-based filtering. This ensures that the recommendations are explainable and deterministic, while still being useful in real-world scenarios.