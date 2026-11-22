\# Fact Check Assistant — System Workflow



```mermaid

flowchart TD

&#x20;   A\[User] --> B\[Streamlit Interface]

&#x20;   B --> C\[Enter Claim and Evidence]

&#x20;   C --> D\[Input Validation]

&#x20;   D --> E{Inputs Valid?}

&#x20;   E -->|No| F\[Display Validation Errors]

&#x20;   F --> C

&#x20;   E -->|Yes| G\[Select Prompt Version]

&#x20;   G --> H\[Generate Prompt]

&#x20;   H --> I\[Copy Prompt]

&#x20;   I --> J\[Submit Prompt to ChatGPT Manually]

&#x20;   J --> K\[Receive AI Analysis]

&#x20;   K --> L\[Paste Analysis into Application]

&#x20;   L --> M\[Save Fact-Checking Report]

&#x20;   M --> N\[View Report in History]

&#x20;   N --> O\[Download Report]

```



\## Workflow Description



The user enters a social media claim and supporting evidence in the Streamlit application. The application validates the inputs and generates a prompt using the selected version. The user manually submits this prompt to ChatGPT and pastes the returned analysis into the application. The report can then be saved, viewed in History and downloaded.

```



6\. Press \*\*Ctrl + S\*\*.



Tell me when saved.

