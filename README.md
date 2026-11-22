# Fact Check Assistant for Social Media Claims

## Project Overview
Fact Check Assistant is a prompt-engineering-based application designed to help users analyse social media claims using supplied evidence.

The application provides structured prompts to support evidence-based analysis and generate organised fact-checking reports.

## Objectives
- Analyse claims using supplied evidence.
- Improve prompt quality through multiple prompt versions.
- Identify supporting and contradicting evidence.
- Handle insufficient or conflicting evidence.
- Present structured fact-checking results.

## Features
- Claim and evidence input.
- Source information input.
- Three prompt versions: V1, V2 and V3.
- Final prompt generation.
- Input validation.
- Structured report display.
- Report history and downloads.
- Testing and evaluation page.

## Technologies Used
- Python
- Streamlit
- Git and GitHub
- ChatGPT for manual prompt analysis

## Project Structure
- `prompts/`: Prompt versions and final prompts.
- `code/`: Python application files.
- `test-data/`: Test inputs and saved outputs.
- `docs/`: Project diagrams and documentation.

## How to Run
1. Install Python.
2. Open the project folder in the terminal.
3. Install dependencies:

   `pip install -r code/requirements.txt`

4. Run the application:

   `python -m streamlit run code/app.py`

## Prototype Link
To be updated after the latest application is deployed.

## Team Details
**Team Name:** TestNexus  
**Team ID:** PE-B49-44  
**Batch:** B49-B64

| Member | Enrollment Number |
|---|---|
| Sidra Siddiquie | S24CSEU0547 |
| Simran Dhiman | S24CSEU0549 |
| Ishan Baliyan | S24CSEU2666 |

## Current Limitations
The current prototype uses a manual ChatGPT workflow. It does not automatically retrieve evidence or independently verify claims. History and test records are maintained within the current application session.

## Future Improvements
- Automated evidence retrieval.
- AI service integration.
- Source reliability assessment.
- Improved verification and reporting.