\# Fact Check Assistant — System Architecture



```mermaid

flowchart TB

&#x20;   U\[User]

&#x20;   UI\[Streamlit User Interface]

&#x20;   VAL\[Input Validation Module]

&#x20;   PROMPT\[Prompt Generation Module]

&#x20;   LIB\[Prompt Template Files]

&#x20;   AI\[External ChatGPT Interaction - Manual]

&#x20;   REPORT\[Report Formatting Module]

&#x20;   HISTORY\[Session-based History]

&#x20;   TEST\[Testing and Evaluation Module]

&#x20;   FILES\[Text File Downloads]



&#x20;   U --> UI

&#x20;   UI --> VAL

&#x20;   VAL --> PROMPT

&#x20;   LIB --> PROMPT

&#x20;   PROMPT --> UI

&#x20;   UI --> AI

&#x20;   AI --> UI

&#x20;   UI --> REPORT

&#x20;   REPORT --> HISTORY

&#x20;   HISTORY --> FILES

&#x20;   UI --> TEST

&#x20;   TEST --> FILES

```



\## Architecture Description



The system uses a modular Python and Streamlit architecture. The interface receives user inputs, the validation module checks them, and the prompt generation module loads the selected prompt template. The user manually interacts with ChatGPT. Returned analysis is formatted and saved in session-based history. The testing module records manual test observations, and the application provides downloadable text files.

```



Save with \*\*Ctrl + S\*\*.



Tell me when done.

