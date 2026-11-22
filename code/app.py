
import streamlit as st
from pathlib import Path
from datetime import datetime

from prompts import generate_prompt, PROMPT_FILES
from validator import validate_inputs
from report import format_report, get_report_status


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Fact Check Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

    report_path = Path(__file__).resolve().parent.parent / "test-data" / "fact_check_report.txt"

    if report_path.exists():
        saved_report = report_path.read_text(encoding="utf-8")

        st.session_state.history.append({
            "date": "Previously saved",
            "claim": "Saved fact-check report",
            "verdict": "Not specified",
            "report": saved_report,
            "version": "Saved Report"
        })

if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""

if "displayed_report" not in st.session_state:
    st.session_state.displayed_report = ""

if "test_results" not in st.session_state:
    st.session_state.test_results = [
        {"id": "TC01", "scenario": "Clearly supported claim", "status": "Pass", "notes": "Prompt generated and report saved successfully."},
        {"id": "TC02", "scenario": "Contradicted claim", "status": "Pass", "notes": "The supplied evidence contradicted the claim. Verdict: FALSE."},
        {"id": "TC03", "scenario": "Partially supported claim", "status": "Pass", "notes": "The system identified the partially supported claim."},
        {"id": "TC04", "scenario": "Insufficient evidence", "status": "Pass", "notes": "The system returned UNVERIFIED."},
        {"id": "TC05", "scenario": "Conflicting evidence", "status": "Pass", "notes": "The system returned UNVERIFIED for conflicting evidence."},
        {"id": "TC06", "scenario": "Empty claim", "status": "Pass", "notes": "Validation message displayed for an empty claim."},
        {"id": "TC07", "scenario": "Empty evidence", "status": "Pass", "notes": "Validation message displayed for empty evidence."},
        {"id": "TC08", "scenario": "Very long claim", "status": "Pass", "notes": "Length validation message displayed for a claim exceeding 2000 characters."},
        {"id": "TC09", "scenario": "Missing source information", "status": "Pass", "notes": "Prompt generated successfully without optional source information."},
        {"id": "TC10", "scenario": "Compound claim", "status": "Pass", "notes": "Both statements were supported by the supplied evidence."}
    ]





# ---------------- CUSTOM DESIGN ----------------


st.markdown("""
<style>
.stApp {
    background: #101010;
    color: #F2F0EB;
}

.block-container {
    max-width: 1300px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #181818;
    border-right: 1px solid #716B58;
}

[data-testid="stSidebar"] * {
    color: #F2F0EB;
}

.hero {
    background: linear-gradient(120deg, #24231F, #514C3D);
    padding: 35px;
    border: 1px solid #81785D;
    border-radius: 18px;
    color: #FFFFFF;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}

.hero h1 {
    color: #D8CBAA !important;
    font-size: 35px;
}

.hero p {
    color: #E2DED2 !important;
    font-size: 16px;
}

.section-title {
    color: #C9B98E;
    font-size: 24px;
    font-weight: 700;
}

.stApp label,
.stApp .stMarkdown h1,
.stApp .stMarkdown h2,
.stApp .stMarkdown h3 {
    color: #D8CBAA;
}

.stTextArea textarea,
.stTextInput input {
    background: #242424 !important;
    color: #FFFFFF !important;
    border: 1px solid #81785D !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: #242424;
    border-radius: 10px;
}

div[data-testid="stMetric"] {
    background: #202020;
    border: 1px solid #716B58;
    padding: 18px;
    border-radius: 14px;
}

.stButton button,
.stDownloadButton button {
    background: #A99B78;
    color: #111111 !important;
    border-radius: 10px;
    border: 1px solid #C5B58D;
    font-weight: 700;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: #C5B58D;
    color: #000000 !important;
}

.info-card {
    background: #202020;
    border: 1px solid #716B58;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}

.stAlert {
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #A99B78;
    padding: 25px;
}
</style>
""", unsafe_allow_html=True)




# =====================================================
# SIDEBAR NAVIGATION
# =====================================================


with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding:10px 0 20px 0;">
            <div style="font-size:42px;">🔎</div>
            <h2 style="color:white; margin:0;">FactCheck</h2>
            <p style="color:#D8C5EF; font-size:13px;">
                Intelligent Claim Analysis
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    

with st.sidebar:
    st.markdown("# 🔎 FactCheck")
    st.caption("Intelligent Claim Analysis")
    st.markdown("---")

    st.markdown("## ☰ MENU")

    page_options = {
        "🏠 Dashboard": "Dashboard",
        "📝 Fact Check": "Fact Check",
        "📚 Prompt Library": "Prompt Library",
        "🕘 History": "History",
        "📊 Testing & Evaluation": "Testing & Evaluation",
        "ℹ️ About Project": "About Project"
    }

    selected_page = st.radio(
        "MAIN MENU",
        list(page_options.keys()),
        label_visibility="collapsed"
    )

    page = page_options[selected_page]

    st.markdown("---")
    st.markdown("### PROJECT")
    st.caption("Team TestNexus")
    st.caption("Team ID: PE-B49-44")
    st.caption("Milestone 2")

    st.markdown("---")
    st.caption("Fact Check Assistant")
    st.caption("Version 2.0")



# =====================================================
# HELPER FUNCTION
# =====================================================

def show_header(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )



# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    show_header(
        "🔎 Welcome to FactCheck",
        "Your intelligent workspace for evidence-based claim analysis."
    )

    st.markdown("## Your Overview")
    st.caption("A quick summary of your fact-checking activity.")

    total = len(st.session_state.history)

    true_count = sum(
        1 for item in st.session_state.history
        if item["verdict"] == "TRUE"
    )

    false_count = sum(
        1 for item in st.session_state.history
        if item["verdict"] == "FALSE"
    )

    partial_count = sum(
        1 for item in st.session_state.history
        if item["verdict"] == "PARTIALLY TRUE"
    )

    unverified_count = sum(
        1 for item in st.session_state.history
        if item["verdict"] == "UNVERIFIED"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📁 Total Reports", total)
    c2.metric("🟢 True", true_count)
    c3.metric("🔴 False", false_count)
    c4.metric("🟣 Unverified", unverified_count)

    c1, c2 = st.columns(2)

    c1.metric("🟡 Partially True", partial_count)
    c2.metric("📚 Prompt Versions", 3)

    st.markdown("---")
    st.markdown("## Explore Your Workspace")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 📝 Fact Check Workspace")
            st.write(
                "Enter a social media claim, add evidence "
                "and generate a structured verification prompt."
            )
            st.caption("Navigate using Fact Check in the sidebar.")

        with st.container(border=True):
            st.markdown("### 📚 Prompt Library")
            st.write(
                "Explore V1, V2 and V3 and understand "
                "how the prompts were improved."
            )
            st.caption("Navigate using Prompt Library in the sidebar.")

        with st.container(border=True):
            st.markdown("### 📊 Testing & Evaluation")
            st.write(
                "Review test scenarios and record actual "
                "application test outcomes."
            )
            st.caption("Navigate using Testing & Evaluation in the sidebar.")

    with col2:
        with st.container(border=True):
            st.markdown("### 🕘 Report History")
            st.write(
                "Review reports saved during your current "
                "Streamlit session."
            )
            st.caption("Navigate using History in the sidebar.")

        with st.container(border=True):
            st.markdown("### 🧠 Evidence-Based Analysis")
            st.write(
                "Compare claims with supplied evidence "
                "without adding unsupported information."
            )
            st.caption("Use the Fact Check workspace to begin.")

        with st.container(border=True):
            st.markdown("### ℹ️ About the Project")
            st.write(
                "Learn about the project objectives, "
                "technology stack and team."
            )
            st.caption("Navigate using About Project in the sidebar.")

    st.markdown("---")
    st.markdown("## Recent Activity")

    if st.session_state.history:

        for item in reversed(st.session_state.history[-5:]):

            with st.container(border=True):
                st.markdown("**" + item["claim"] + "**")
                st.caption(
                    item["date"] + "  |  " +
                    item["version"] + "  |  " +
                    item["verdict"]
                )

    else:
        st.info(
            "No activity yet. Your completed fact-check reports "
            "will appear here."
        )

    st.markdown("---")

    st.caption(
        "Statistics are based on reports saved in the current session. "
        "Verdicts are recorded from manually pasted ChatGPT responses."
    )


# =====================================================
# FACT CHECK WORKSPACE
# =====================================================


elif page == "Fact Check":
    show_header(
        "📝 Fact Check Workspace",
        "Analyse a social media claim using the evidence you provide."
    )

    st.markdown("## Enter your information")
    st.write("Provide a claim, its supporting evidence and optional source details.")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("### 🔎 Social Media Claim")
            claim = st.text_area(
                "Enter the claim",
                placeholder="Example: The Earth revolves around the Sun.",
                height=160,
                key="fact_claim"
            )

    with right:
        with st.container(border=True):
            st.markdown("### 📚 Supplied Evidence")
            evidence = st.text_area(
                "Enter the evidence",
                placeholder="Paste the information that can be used to analyse the claim.",
                height=160,
                key="fact_evidence"
            )

    with st.container(border=True):
        st.markdown("### 🔗 Source Information")
        sources = st.text_input(
            "Source name or URL (optional)",
            placeholder="Example: NASA - https://science.nasa.gov/"
        )

    st.markdown("### ⚙️ Prompt Configuration")

    col1, col2 = st.columns([2, 1])

    with col1:
        version = st.selectbox(
            "Choose a prompt version",
            list(PROMPT_FILES.keys()),
            index=2
        )

    with col2:
        st.markdown("**Selected version**")
        st.info(version)

    st.markdown("---")

    if st.button("✨ Generate Fact-Checking Prompt", use_container_width=True):
        errors = validate_inputs(claim, evidence, sources)

        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                st.session_state.generated_prompt = generate_prompt(
                    claim, evidence, sources, version
                )
                st.success("Your prompt has been generated successfully!")

            except Exception as error:
                st.error(f"Unable to generate prompt: {error}")

    if st.session_state.generated_prompt:
        st.markdown("## Generated Prompt")

        st.write(
            "Copy this prompt and submit it to ChatGPT. "
            "Then paste the returned analysis below."
        )

        st.text_area(
            "Your generated prompt",
            value=st.session_state.generated_prompt,
            height=300
        )

        st.download_button(
            "⬇️ Download Prompt",
            data=st.session_state.generated_prompt,
            file_name="fact_check_prompt.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.markdown("---")
        st.markdown("## 📋 Fact-Checking Result")

        result = st.text_area(
            "Paste the ChatGPT response here",
            placeholder="Paste the complete fact-checking response...",
            height=220,
            key="fact_result"
        )

        if st.button("Save Fact-Checking Report", use_container_width=True):
            if not result.strip():
                st.warning("Please paste a fact-checking result first.")
            else:
                formatted_result = format_report(result)

                verdict = "UNSPECIFIED"
                for line in formatted_result.splitlines():
                    if line.strip().lower().startswith("verdict:"):
                        verdict_text = line.split(":", 1)[1].strip().upper()
                        if verdict_text in [
                            "TRUE", "FALSE", "PARTIALLY TRUE", "UNVERIFIED"
                        ]:
                            verdict = verdict_text
                        break

                st.session_state.history.append({
                    "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                    "claim": claim,
                    "verdict": verdict,
                    "report": formatted_result,
                    "version": version
                })

                st.session_state.displayed_report = formatted_result
                st.success("Report saved successfully!")

    if st.session_state.displayed_report:
        st.markdown("---")
        st.markdown("## 📄 Saved Report")
        st.text_area(
            "Report",
            value=st.session_state.displayed_report,
            height=250,
            disabled=True
        )

        st.download_button(
            "⬇️ Download Report",
            data=st.session_state.displayed_report,
            file_name="fact_check_report.txt",
            mime="text/plain"
        )


# =====================================================
# PROMPT LIBRARY
# =====================================================


elif page == "Prompt Library":
    show_header(
        "📚 Prompt Library",
        "Explore, compare and download different prompt versions."
    )

    st.markdown("## Explore Prompt Versions")
    st.write(
        "Each version improves the way claims are analysed "
        "using the supplied evidence."
    )

    prompt_details = {
        "V1 - Basic": {
            "number": "01",
            "title": "Basic Prompt",
            "description": "A simple starting point for claim analysis.",
            "features": [
                "Identifies the main claim",
                "Compares claim with evidence",
                "Provides a basic verdict"
            ],
            "color": "#A99B78"
        },
        "V2 - Improved": {
            "number": "02",
            "title": "Improved Prompt",
            "description": "Adds better evidence comparison and verdict options.",
            "features": [
                "Identifies supporting evidence",
                "Identifies contradicting evidence",
                "Handles partially supported claims"
            ],
            "color": "#B9AA86"
        },
        "V3 - Advanced": {
            "number": "03",
            "title": "Advanced Prompt",
            "description": "Provides a more detailed and structured analysis.",
            "features": [
                "Breaks down compound claims",
                "Identifies evidence gaps",
                "Includes confidence levels"
            ],
            "color": "#D1C19A"
        }
    }

    card1, card2, card3 = st.columns(3)

    for card, version_name in zip(
        [card1, card2, card3],
        prompt_details.keys()
    ):
        details = prompt_details[version_name]

        with card:
            with st.container(border=True):
                st.markdown(
                    f"### {details['number']}  {details['title']}"
                )
                st.caption(version_name)
                st.write(details["description"])
                st.markdown("**Key features**")

                for feature in details["features"]:
                    st.markdown(f"- {feature}")

                st.markdown(
                    f"<p style='color:{details['color']};"
                    f"font-weight:bold;'>PROMPT VERSION "
                    f"{details['number']}</p>",
                    unsafe_allow_html=True
                )

    st.markdown("---")
    st.markdown("## 🔍 Compare Prompt Versions")

    comparison = {
        "Feature": [
            "Main claim identification",
            "Supporting evidence",
            "Contradicting evidence",
            "Partial verdict",
            "Evidence gaps",
            "Confidence level"
        ],
        "V1 - Basic": [
            "Yes", "Basic", "No", "No", "No", "No"
        ],
        "V2 - Improved": [
            "Yes", "Yes", "Yes", "Yes", "No", "No"
        ],
        "V3 - Advanced": [
            "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"
        ]
    }

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.markdown("## 📄 Prompt Explorer")

    selected_version = st.selectbox(
        "Select a prompt to explore",
        list(PROMPT_FILES.keys()),
        index=2,
        key="library_prompt_version"
    )

    prompt_path = PROMPT_FILES[selected_version]

    if prompt_path.exists():
        prompt_text = prompt_path.read_text(encoding="utf-8")

        st.success(f"{selected_version} is ready to explore.")

        with st.expander("View complete prompt", expanded=True):
            st.code(prompt_text, language="text")

        st.download_button(
            label="⬇️ Download Selected Prompt",
            data=prompt_text,
            file_name=f"{selected_version.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:
        st.error("Prompt file not found. Check your prompts folder.")

    st.markdown("---")
    st.markdown("### 💡 Prompt Development")
    st.info(
        "The three prompt versions show the development of the "
        "system from basic claim analysis to more detailed, "
        "evidence-aware analysis. The final version should be "
        "selected based on actual testing results."
    )


# =====================================================
# HISTORY
# =====================================================

elif page == "History":
    show_header(
        "🕘 Analysis History",
        "Review and download your previously saved fact-checking reports."
    )

    history = st.session_state.history

    st.markdown("## 📊 History Overview")

    total = len(history)
    true_count = sum(1 for item in history if item["verdict"] == "TRUE")
    false_count = sum(1 for item in history if item["verdict"] == "FALSE")
    partial_count = sum(
        1 for item in history if item["verdict"] == "PARTIALLY TRUE"
    )
    unverified_count = sum(
        1 for item in history if item["verdict"] == "UNVERIFIED"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Total Reports", total)
    c2.metric("TRUE", true_count)
    c3.metric("FALSE", false_count)
    c4.metric("PARTIAL", partial_count)
    c5.metric("UNVERIFIED", unverified_count)

    st.markdown("---")
    st.markdown("## 📁 Saved Reports")

    if not history:
        st.info(
            "No reports saved yet. Visit the Fact Check page "
            "to generate and save your first report."
        )

    else:
        search = st.text_input(
            "🔍 Search reports by claim",
            placeholder="Enter a word from a claim..."
        )

        filtered_history = [
            item for item in reversed(history)
            if search.lower() in item["claim"].lower()
        ]

        st.caption(f"{len(filtered_history)} report(s) found.")

        for index, item in enumerate(filtered_history):
            verdict = item.get("verdict", "UNSPECIFIED")

            with st.expander(
                f"📄 {item['claim'][:85]} — {verdict}",
                expanded=False
            ):
                st.markdown("**Claim**")
                st.write(item["claim"])

                col1, col2 = st.columns(2)

                col1.markdown("**Date saved**")
                col1.write(item["date"])

                col2.markdown("**Prompt version**")
                col2.write(item.get("version", "Not recorded"))

                st.markdown("**Verdict**")

                if verdict == "TRUE":
                    st.success(verdict)
                elif verdict == "FALSE":
                    st.error(verdict)
                elif verdict == "PARTIALLY TRUE":
                    st.warning(verdict)
                else:
                    st.info(verdict)

                st.markdown("**Full Report**")
                st.text_area(
                    "Report content",
                    value=item["report"],
                    height=200,
                    disabled=True,
                    key=f"history_report_{index}"
                )

                st.download_button(
                    "⬇️ Download This Report",
                    data=item["report"],
                    file_name=f"fact_check_report_{index + 1}.txt",
                    mime="text/plain",
                    key=f"download_history_{index}"
                )

    st.markdown("---")
    st.caption(
        "Note: History is stored in the current Streamlit session. "
        "It may reset when the session restarts."
    )



# =====================================================
# TESTING AND EVALUATION
# =====================================================


elif page == "Testing & Evaluation":
    show_header(
        "📊 Testing & Evaluation",
        "Evaluate the Fact Check Assistant using different test scenarios."
    )

    test_cases = [
        {
            "ID": "TC01",
            "Category": "Normal",
            "Test Scenario": "Clearly supported claim",
            "Input": "Earth revolves around the Sun.",
            "Expected Behaviour": "Identify supporting evidence and produce an appropriate verdict."
        },
        {
            "ID": "TC02",
            "Category": "Normal",
            "Test Scenario": "Contradicted claim",
            "Input": "The supplied evidence contradicts the claim.",
            "Expected Behaviour": "Identify contradicting evidence."
        },
        {
            "ID": "TC03",
            "Category": "Normal",
            "Test Scenario": "Partially supported claim",
            "Input": "Only one part of a compound claim is supported.",
            "Expected Behaviour": "Explain which parts are supported and unsupported."
        },
        {
            "ID": "TC04",
            "Category": "Normal",
            "Test Scenario": "Insufficient evidence",
            "Input": "A claim with unrelated or incomplete evidence.",
            "Expected Behaviour": "Use UNVERIFIED when evidence is insufficient."
        },
        {
            "ID": "TC05",
            "Category": "Normal",
            "Test Scenario": "Conflicting evidence",
            "Input": "Evidence contains both supporting and contradicting information.",
            "Expected Behaviour": "Identify the conflict and explain the uncertainty."
        },
        {
            "ID": "TC06",
            "Category": "Edge Case",
            "Test Scenario": "Empty claim",
            "Input": "Claim field is left blank.",
            "Expected Behaviour": "Show a claim validation error."
        },
        {
            "ID": "TC07",
            "Category": "Edge Case",
            "Test Scenario": "Empty evidence",
            "Input": "Evidence field is left blank.",
            "Expected Behaviour": "Show an evidence validation error."
        },
        {
            "ID": "TC08",
            "Category": "Edge Case",
            "Test Scenario": "Very long claim",
            "Input": "Claim contains more than 2000 characters.",
            "Expected Behaviour": "Reject the input with a length validation message."
        },
        {
            "ID": "TC09",
            "Category": "Edge Case",
            "Test Scenario": "Missing source information",
            "Input": "Valid claim and evidence, but no source details.",
            "Expected Behaviour": "Allow analysis because source information is optional."
        },
        {
            "ID": "TC10",
            "Category": "Normal",
            "Test Scenario": "Compound claim",
            "Input": "A claim contains multiple factual statements.",
            "Expected Behaviour": "Break the claim into smaller statements where appropriate."
        }
    ]

    st.markdown("## 📋 Test Scenario Catalogue")
    st.write(
        "The following scenarios are designed to evaluate normal "
        "inputs, insufficient evidence and edge cases."
    )

    st.dataframe(
        test_cases,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.markdown("## 📈 Test Progress")

    saved_results = st.session_state.test_results


































    total_tests = len(test_cases)
    recorded_tests = len(saved_results)
    passed_tests = sum(
        1 for item in saved_results if item["status"] == "Pass"
    )
    failed_tests = sum(
        1 for item in saved_results if item["status"] == "Fail"
    )
    review_tests = sum(
        1 for item in saved_results if item["status"] == "Needs Review"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Test Scenarios", total_tests)
    c2.metric("Recorded", recorded_tests)
    c3.metric("Passed", passed_tests)
    c4.metric("Failed", failed_tests)

    st.caption(
        f"Needs Review: {review_tests} | "
        f"Not yet recorded: {total_tests - recorded_tests}"
    )

    st.markdown("---")
    st.markdown("## ✍️ Record Actual Test Results")

    selected_test = st.selectbox(
        "Select a test case",
        [item["ID"] for item in test_cases]
    )

    current_test = next(
        item for item in test_cases
        if item["ID"] == selected_test
    )

    st.info(
        f"**{current_test['Test Scenario']}**\n\n"
        f"Expected behaviour: {current_test['Expected Behaviour']}"
    )

    with st.form("test_result_form"):
        test_status = st.selectbox(
            "Actual result",
            ["Not Run", "Pass", "Fail", "Needs Review"]
        )

        test_notes = st.text_area(
            "Observation / Evidence",
            placeholder="Describe what happened when you actually ran this test."
        )

        submit_test = st.form_submit_button(
            "Save Test Result",
            use_container_width=True
        )

        if submit_test:
            if test_status == "Not Run":
                st.warning("Run the test before recording a result.")
            elif not test_notes.strip():
                st.warning("Please enter your actual test observation.")
            else:
                existing_index = next(
                    (
                        i for i, item in enumerate(
                            st.session_state.test_results
                        )
                        if item["id"] == selected_test
                    ),
                    None
                )

                result_record = {
                    "id": selected_test,
                    "scenario": current_test["Test Scenario"],
                    "status": test_status,
                    "notes": test_notes.strip()
                }

                if existing_index is None:
                    st.session_state.test_results.append(result_record)
                else:
                    st.session_state.test_results[existing_index] = result_record

                st.success("Test result recorded successfully!")
                st.rerun()

    st.markdown("---")
    st.markdown("## 🧾 Recorded Test Results")

    if saved_results:
        st.dataframe(
            [
                {
                    "Test ID": item["id"],
                    "Scenario": item["scenario"],
                    "Actual Result": item["status"],
                    "Observation": item["notes"]
                }
                for item in saved_results
            ],
            use_container_width=True,
            hide_index=True
        )

        report_text = "\n\n".join(
            [
                f"Test ID: {item['id']}\n"
                f"Scenario: {item['scenario']}\n"
                f"Actual Result: {item['status']}\n"
                f"Observation: {item['notes']}"
                for item in saved_results
            ]
        )

        st.download_button(
            "⬇️ Download Test Results",
            data=report_text,
            file_name="fact_check_test_results.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info(
            "No actual test results have been recorded yet. "
            "Run the scenarios and record your observations here."
        )

    st.caption(
        "Note: Test scenarios are planned cases, not completed test results. "
        "Recorded results are stored in the current Streamlit session."
    )


# =====================================================
# ABOUT PROJECT
# =====================================================


elif page == "About Project":
    show_header(
        "ℹ️ About Fact Check Assistant",
        "An evidence-based application for analysing social media claims."
    )

    st.markdown("## 🎯 Project Overview")

    st.write(
        "Fact Check Assistant is a prompt-engineering-based application "
        "that helps users analyse social media claims using supplied "
        "evidence. It generates structured prompts to support clear, "
        "evidence-based analysis."
    )

    st.markdown("---")
    st.markdown("## ✨ Key Features")

    feature1, feature2 = st.columns(2)

    with feature1:
        with st.container(border=True):
            st.markdown("### 📝 Claim Analysis")
            st.write(
                "Enter a social media claim and the evidence "
                "you want to examine."
            )

        with st.container(border=True):
            st.markdown("### 📚 Prompt Library")
            st.write(
                "Explore three prompt versions, compare their "
                "features and download prompt templates."
            )

        with st.container(border=True):
            st.markdown("### 📊 Testing")
            st.write(
                "Record observations from different test scenarios "
                "and review test results."
            )

    with feature2:
        with st.container(border=True):
            st.markdown("### 🔍 Evidence-based Output")
            st.write(
                "Generate structured prompts that instruct the "
                "language model to use only supplied evidence."
            )

        with st.container(border=True):
            st.markdown("### 🕘 Report History")
            st.write(
                "Review and download reports saved during "
                "the current application session."
            )

        with st.container(border=True):
            st.markdown("### ⬇️ Downloads")
            st.write(
                "Download generated prompts, reports and "
                "recorded test results."
            )

    st.markdown("---")
    st.markdown("## 🛠️ Technology Stack")

    tech1, tech2, tech3, tech4 = st.columns(4)

    tech1.metric("Language", "Python")
    tech2.metric("Framework", "Streamlit")
    tech3.metric("Version Control", "Git")
    tech4.metric("Interface", "Web App")

    st.markdown("---")
    st.markdown("## 🏗️ Project Architecture")

    st.code(
        """
        User
          |
          v
        Streamlit Interface
          |
          v
        Input Validation
          |
          v
        Prompt Version Selection
          |
          v
        Prompt Generation
          |
          v
        User submits prompt to ChatGPT
          |
          v
        User pastes generated analysis
          |
          v
        Report Formatting and History
        """,
        language="text"
    )

    st.markdown("---")
    st.markdown("## 👥 Team TestNexus")

    st.write("**Team ID:** PE-B49-44")
    st.write("**Batch:** B49-B64")

    st.table({
        "Team Member": [
            "Sidra Siddiquie",
            "Simran Dhiman",
            "Ishan Baliyan"
        ],
        "Enrollment Number": [
            "S24CSEU0547",
            "S24CSEU0549",
            "S24CSEU2666"
        ]
    })

    st.markdown("---")
    st.markdown("## ⚠️ Current Limitations")

    st.warning(
        """
        - The application does not automatically retrieve evidence.
        - Users manually submit generated prompts to ChatGPT.
        - The application does not independently verify source authenticity.
        - History and test results are stored in the current session.
        """
    )

    st.markdown("## 🚀 Future Improvements")

    st.write(
        """
        - Integrate an AI service for automated response generation.
        - Add reliable evidence retrieval.
        - Improve source reliability assessment.
        - Add persistent report storage.
        """
    )

    st.markdown("---")
    st.markdown("### Fact Check Assistant | Milestone 2")
    st.caption("Developed by Team TestNexus")



# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        <b>🔎 Fact Check Assistant</b><br>
        Team TestNexus | PE-B49-44<br>
        Evidence-Based Prompt Engineering | Milestone 2
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style="
        margin-top: 40px;
        padding: 22px;
        text-align: center;
        background: #202020;
        border-top: 1px solid #A99B78;
        border-radius: 12px;
        color: #D8CBAA;
    ">
        <h4 style="color:#D8CBAA;">
            🔎 Fact Check Assistant
        </h4>
        <p style="margin-bottom:5px;">
            Evidence-based Claim Analysis
        </p>
        <small style="color:#A99B78;">
            Team TestNexus | PE-B49-44 | Milestone 2
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
