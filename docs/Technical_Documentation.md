\# Technical Documentation

\## Fact Check Assistant for Social Media Claims



\*\*Team Name:\*\* TestNexus  

\*\*Team ID:\*\* PE-B49-44  

\*\*Batch:\*\* B49-B64  

\*\*Milestone:\*\* 2



\---



\## 1. Project Introduction



Fact Check Assistant is a prompt-engineering-based application developed to help users analyse social media claims using supplied evidence.



The application uses Python and Streamlit to provide a user-friendly interface. It generates structured prompts that users can submit manually to ChatGPT to obtain a fact-checking analysis.



\## 2. Technologies Used



\- \*\*Python:\*\* Main programming language.

\- \*\*Streamlit:\*\* Web application interface.

\- \*\*Git and GitHub:\*\* Version control and project repository.

\- \*\*ChatGPT:\*\* Manual generation of fact-checking responses.



\## 3. System Modules



| Module | Responsibility |

|---|---|

| User Interface | Accepts claims, evidence and source information. |

| Input Validation | Checks empty inputs and input length. |

| Prompt Generation | Loads and fills the selected prompt template. |

| Prompt Library | Stores V1, V2, V3 and the final prompt. |

| Report Management | Formats and saves returned analysis. |

| History | Displays reports saved during the current session. |

| Testing Module | Records manual test observations. |



\## 4. Prompt Engineering



Three prompt versions were developed:



\- \*\*V1 – Basic:\*\* Identifies the claim and compares it with supplied evidence.

\- \*\*V2 – Improved:\*\* Adds supporting evidence, contradicting evidence and partial verdicts.

\- \*\*V3 – Advanced:\*\* Adds compound-claim analysis, evidence gaps and confidence levels.



V3 Advanced was selected as the final prompt after manual testing.



The final prompt is stored in `prompts/final/final\_prompt.txt`.



\## 5. Testing and Evaluation



Ten test scenarios were conducted manually.



| Test ID | Scenario | Result |

|---|---|---|

| TC01 | Clearly supported claim | Pass |

| TC02 | Contradicted claim | Pass |

| TC03 | Partially supported claim | Pass |

| TC04 | Insufficient evidence | Pass |

| TC05 | Conflicting evidence | Pass |

| TC06 | Empty claim | Pass |

| TC07 | Empty evidence | Pass |

| TC08 | Very long claim | Pass |

| TC09 | Missing source information | Pass |

| TC10 | Compound claim | Pass |



The observed results and test examples are saved in the `test-data` folder.



\## 6. System Limitations



1\. Users must manually submit generated prompts to ChatGPT.

2\. The application does not automatically retrieve supporting evidence.

3\. Source authenticity is not independently verified.

4\. Report history and test results are stored in the current Streamlit session and are not permanent database records.



\## 7. Future Improvements



\- Integrate an AI service for automated response generation.

\- Add reliable evidence retrieval.

\- Introduce source reliability assessment.

\- Add permanent report storage.

\- Improve evaluation using a larger set of test cases.



\## 8. Conclusion



The Milestone 2 implementation provides a functional Streamlit prototype with multiple prompt versions, input validation, report management, history and testing features.



Manual testing demonstrated the application's prompt-generation workflow and its ability to handle different evidence scenarios. Further development can improve automation and independent verification.



\---



\*\*Developed by Team TestNexus\*\*  

\*\*Team ID: PE-B49-44\*\*



