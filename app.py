import streamlit as st
import json
import os
import re
from dotenv import load_dotenv
from google import genai

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="CareerCompass AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #888888;
        margin-bottom: 30px;
    }

    .career-card {
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #444444;
        min-height: 330px;
        background: rgba(255,255,255,0.03);
    }

    .score {
        font-size: 34px;
        font-weight: 800;
    }

    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 15px;
    }

    .roadmap-card {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #444444;
        min-height: 180px;
    }

    .footer {
        text-align: center;
        color: #888888;
        padding: 30px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 CareerCompass AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI-powered career mentor for Class 12 students</div>',
    unsafe_allow_html=True
)

st.info(
    "💡 CareerCompass analyses academic performance, interests and skills "
    "to suggest personalized career paths, identify skill gaps and create "
    "a practical learning roadmap."
)

# ============================================================
# API CHECK
# ============================================================

if not API_KEY:
    st.error(
        "⚠️ Gemini API key not found. "
        "Please make sure GEMINI_API_KEY is present in your .env file."
    )
    st.stop()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Could not initialize Gemini: {e}")
    st.stop()

# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state["result"] = None

if "student" not in st.session_state:
    st.session_state["student"] = None

# ============================================================
# STEP 1 — STUDENT PROFILE
# ============================================================

st.markdown("## 👤 Step 1 — Student Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    stream = st.selectbox(
        "Class 12 Stream",
        [
            "Science",
            "Commerce",
            "Humanities",
            "Vocational / Other"
        ]
    )

    st.markdown("### 📊 Board / Academic Results")

    maths = st.slider(
        "Mathematics (%)",
        0,
        100,
        75
    )

    science = st.slider(
        "Science (%)",
        0,
        100,
        75
    )

    english = st.slider(
        "English (%)",
        0,
        100,
        75
    )

    computer = st.slider(
        "Computer / IT (%)",
        0,
        100,
        75
    )

with col2:

    st.markdown("### ❤️ Interests")

    interests = st.multiselect(
        "Select your interests",
        [
            "Artificial Intelligence",
            "Technology",
            "Programming",
            "Research",
            "Mathematics",
            "Science",
            "Business",
            "Entrepreneurship",
            "Finance",
            "Design",
            "Medicine",
            "Law",
            "Communication",
            "Teaching",
            "Social Impact",
            "Creative Work"
        ],
        default=[
            "Technology",
            "Artificial Intelligence"
        ]
    )

    st.markdown("### 🧠 Skills")

    skills = st.multiselect(
        "Select your strongest skills",
        [
            "Problem Solving",
            "Analytical Thinking",
            "Programming",
            "Mathematical Reasoning",
            "Communication",
            "Creativity",
            "Leadership",
            "Research",
            "Teamwork",
            "Writing",
            "Data Analysis",
            "Public Speaking",
            "Entrepreneurship"
        ],
        default=[
            "Problem Solving",
            "Analytical Thinking"
        ]
    )

    career_preference = st.selectbox(
        "Preferred Career Area",
        [
            "Technology & AI",
            "Engineering",
            "Data & Analytics",
            "Business & Entrepreneurship",
            "Finance",
            "Healthcare",
            "Law",
            "Design & Creative",
            "Research",
            "Not Sure Yet"
        ]
    )

    learning_time = st.selectbox(
        "Available learning time per week",
        [
            "1–3 hours",
            "4–6 hours",
            "7–10 hours",
            "10+ hours"
        ]
    )

# ============================================================
# VALIDATION
# ============================================================

average_marks = round(
    (maths + science + english + computer) / 4,
    1
)

st.markdown("---")

st.markdown("### 📌 Profile Summary")

summary1, summary2, summary3, summary4 = st.columns(4)

with summary1:
    st.metric("Academic Average", f"{average_marks}%")

with summary2:
    st.metric("Interests", len(interests))

with summary3:
    st.metric("Skills", len(skills))

with summary4:
    st.metric("Learning Time", learning_time)

# ============================================================
# ANALYSIS BUTTON
# ============================================================

st.markdown("---")

analyze = st.button(
    "🚀 Analyse My Career",
    type="primary",
    use_container_width=True
)

# ============================================================
# AI ANALYSIS
# ============================================================

if analyze:

    if not name.strip():
        st.warning("Please enter the student's name.")
        st.stop()

    if not interests:
        st.warning("Please select at least one interest.")
        st.stop()

    if not skills:
        st.warning("Please select at least one skill.")
        st.stop()

    student_data = {
        "name": name,
        "stream": stream,
        "marks": {
            "Mathematics": maths,
            "Science": science,
            "English": english,
            "Computer_IT": computer,
            "Average": average_marks
        },
        "interests": interests,
        "skills": skills,
        "career_preference": career_preference,
        "learning_time": learning_time
    }

    # --------------------------------------------------------
    # AI PROMPT
    # --------------------------------------------------------

    profile_json = json.dumps(
        student_data,
        indent=2
    )

    prompt = """
You are CareerCompass AI.

You are an ethical AI career mentor designed for Class 12 students.

Your job is to analyse a student's:

1. Academic performance
2. Interests
3. Skills
4. Career preference
5. Available learning time

Then recommend THREE personalized career paths.

IMPORTANT RULES:

- The match score is an AI guidance score from 0-100.
- Calculate the score transparently using:
  Academic Fit = 35%
  Interest Fit = 35%
  Skill Fit = 30%
- Final Score = (Academic Fit × 0.35) + (Interest Fit × 0.35) + (Skill Fit × 0.30)
- The score is NOT a probability of success.
- Never present the score as a guarantee of career success.
- It is NOT a probability of success.
- Do not guarantee a job, salary or future outcome.
- Do not use gender, caste, religion, family income or other protected characteristics.
- Avoid biased assumptions.
- Explain why each recommendation fits the student.
- Identify realistic skill gaps.
- Recommend appropriate degrees/courses.
- Give practical next steps.
- Consider the changing job market toward 2026-2030.
- Career recommendations should be guidance, not a final decision.

Use this student profile:

""" + profile_json + """

Return ONLY valid JSON.

Use exactly this structure:

{
    "careers": [
        {
            "rank": 1,
            "name": "Career name",
            "score": 90,
            "score_breakdown": {
            "academic_fit": 90,
            "interest_fit": 92,
            "skill_fit": 88
            },
            "outlook": "Strong",
            "why_fit": "Short explanation.",
            "academic_fit": "Academic alignment.",
            "interest_fit": "Interest alignment.",
            "skill_fit": "Skill alignment.",
            "strengths": [
                "strength 1",
                "strength 2",
                "strength 3"
            ],
            "skill_gaps": [
                "skill 1",
                "skill 2",
                "skill 3"
            ],
            "courses": [
                "course or degree 1",
                "course or degree 2"
            ],
            "next_step": "One practical next step"
        },

        {
            "rank": 2,
            "name": "Career name",
            "score": 85,
            "outlook": "Strong",
            "why_fit": "Short explanation.",
            "academic_fit": "Academic alignment.",
            "interest_fit": "Interest alignment.",
            "skill_fit": "Skill alignment.",
            "strengths": [
                "strength 1",
                "strength 2",
                "strength 3"
            ],
            "skill_gaps": [
                "skill 1",
                "skill 2",
                "skill 3"
            ],
            "courses": [
                "course or degree 1",
                "course or degree 2"
            ],
            "next_step": "One practical next step"
        },

        {
            "rank": 3,
            "name": "Career name",
            "score": 80,
            "outlook": "Moderate",
            "why_fit": "Short explanation.",
            "academic_fit": "Academic alignment.",
            "interest_fit": "Interest alignment.",
            "skill_fit": "Skill alignment.",
            "strengths": [
                "strength 1",
                "strength 2",
                "strength 3"
            ],
            "skill_gaps": [
                "skill 1",
                "skill 2",
                "skill 3"
            ],
            "courses": [
                "course or degree 1",
                "course or degree 2"
            ],
            "next_step": "One practical next step"
        }
    ],

    "skill_gap_summary": [
        "skill 1",
        "skill 2",
        "skill 3",
        "skill 4",
        "skill 5"
    ],

    "roadmap": {
        "months_1_3": "Action plan",
        "months_4_6": "Action plan",
        "months_7_9": "Action plan",
        "months_10_12": "Action plan"
    },

    "final_advice": "Balanced advice for the student."
}
"""

    # --------------------------------------------------------
    # CALL GEMINI
    # --------------------------------------------------------

    with st.spinner("🧠 CareerCompass AI is analysing your profile..."):

        try:

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            response_text = response.text.strip()

            # Remove accidental markdown code fences
            response_text = re.sub(
                r"^```json\s*",
                "",
                response_text,
                flags=re.IGNORECASE
            )

            response_text = re.sub(
                r"\s*```$",
                "",
                response_text
            )

            result = json.loads(response_text)

            st.session_state["result"] = result
            st.session_state["student"] = student_data

        except json.JSONDecodeError:

            st.error(
                "The AI returned an unexpected format. "
                "Please click Analyse My Career again."
            )

            with st.expander("View AI response"):
                st.code(response.text)

        except Exception as e:

            st.error(
                f"AI analysis failed: {e}"
            )

# ============================================================
# DISPLAY RESULT
# ============================================================

if st.session_state["result"] is not None:

    result = st.session_state["result"]
    student = st.session_state["student"]

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🎯 Personalized AI Career Report</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"Career analysis completed for **{student['name']}**."
    )

    # ========================================================
    # TOP SUMMARY
    # ========================================================

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Academic Average",
            f"{student['marks']['Average']}%"
        )

    with s2:
        st.metric(
            "Top Match",
            f"{result['careers'][0]['score']}/100"
        )

    with s3:
        st.metric(
            "Career Options",
            "3"
        )

    with s4:
        st.metric(
            "AI Guidance",
            "Personalized"
        )

    # ========================================================
    # TOP 3 CAREERS
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🏆 Top Career Matches</div>',
        unsafe_allow_html=True
    )

    careers = result["careers"]

    career_columns = st.columns(3)

    medals = ["🥇", "🥈", "🥉"]

    for i, career in enumerate(careers):

        with career_columns[i]:

            st.markdown(
                f"""
                <div class="career-card">

                <h2>{medals[i]} {career['name']}</h2>

                <div class="score">
                {career['score']}/100
                </div>

                <p><b>📈 Outlook:</b> {career['outlook']}</p>

                <p>
                <b>💡 Why it fits:</b><br>
                {career['why_fit']}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # CAREER EXPLORER
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🔍 Explore Career Details</div>',
        unsafe_allow_html=True
    )

    career_names = [
        career["name"]
        for career in careers
    ]

    selected_name = st.selectbox(
        "Choose a career to explore",
        career_names
    )

    selected_career = next(
        career for career in careers
        if career["name"] == selected_name
    )

    st.markdown(
        f"## {selected_career['name']} — "
        f"{selected_career['score']}/100"
    )

    # ========================================================
    # FIT ANALYSIS
    # ========================================================

    fit1, fit2, fit3 = st.columns(3)

    with fit1:
        st.markdown("### 📚 Academic Fit")
        st.write(
            selected_career["academic_fit"]
        )

    with fit2:
        st.markdown("### ❤️ Interest Fit")
        st.write(
            selected_career["interest_fit"]
        )

    with fit3:
        st.markdown("### 🧠 Skill Fit")
        st.write(
            selected_career["skill_fit"]
        )

    # ========================================================
    # STRENGTHS AND SKILL GAPS
    # ========================================================

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.markdown("### 💪 Your Strengths")

        for strength in selected_career["strengths"]:

            st.success(
                f"✓ {strength}"
            )

    with right:

        st.markdown("### 🧩 Skills to Develop")

        for gap in selected_career["skill_gaps"]:

            st.warning(
                f"→ {gap}"
            )

    # ========================================================
    # EDUCATION
    # ========================================================

    st.markdown("---")

    st.markdown("### 🎓 Recommended Education / Courses")

    for course in selected_career["courses"]:

        st.write(
            f"🎓 **{course}**"
        )

    st.info(
        f"🚀 **Recommended next step:** "
        f"{selected_career['next_step']}"
    )

    # ========================================================
# CAREER COMPARISON
# ========================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">⚖️ Compare Career Paths</div>',
    unsafe_allow_html=True
)

st.write(
    "Not sure which path is better for you? "
    "Compare two AI-recommended careers side-by-side."
)

comparison_names = [
    career["name"]
    for career in careers
]

compare_col1, compare_col2 = st.columns(2)

with compare_col1:

    career_a_name = st.selectbox(
        "Career A",
        comparison_names,
        index=0,
        key="career_a"
    )

with compare_col2:

    career_b_name = st.selectbox(
        "Career B",
        comparison_names,
        index=1 if len(comparison_names) > 1 else 0,
        key="career_b"
    )

career_a = next(
    career for career in careers
    if career["name"] == career_a_name
)

career_b = next(
    career for career in careers
    if career["name"] == career_b_name
)

if career_a_name == career_b_name:

    st.warning(
        "Please select two different careers to compare."
    )

else:

    st.markdown("### 📊 Career Comparison")

    comparison_table = {
        "Category": [
            "AI Match Score",
            "Career Outlook",
            "Academic Fit",
            "Interest Fit",
            "Skill Fit"
        ],
        career_a["name"]: [
            f"{career_a['score']}/100",
            career_a["outlook"],
            f"{career_a['score_breakdown']['academic_fit']}/100",
            f"{career_a['score_breakdown']['interest_fit']}/100",
            f"{career_a['score_breakdown']['skill_fit']}/100"
        ],
        career_b["name"]: [
            f"{career_b['score']}/100",
            career_b["outlook"],
            f"{career_b['score_breakdown']['academic_fit']}/100",
            f"{career_b['score_breakdown']['interest_fit']}/100",
            f"{career_b['score_breakdown']['skill_fit']}/100"
        ]
    }

    st.table(comparison_table)

    st.markdown("### 💪 Strength Comparison")

    strength_col1, strength_col2 = st.columns(2)

    with strength_col1:

        st.markdown(f"#### {career_a['name']}")

        for strength in career_a["strengths"]:
            st.success(f"✓ {strength}")

    with strength_col2:

        st.markdown(f"#### {career_b['name']}")

        for strength in career_b["strengths"]:
            st.success(f"✓ {strength}")

    st.markdown("### 🧩 Skill Gap Comparison")

    gap_col1, gap_col2 = st.columns(2)

    with gap_col1:

        st.markdown(f"#### {career_a['name']}")

        for gap in career_a["skill_gaps"]:
            st.warning(f"→ {gap}")

    with gap_col2:

        st.markdown(f"#### {career_b['name']}")

        for gap in career_b["skill_gaps"]:
            st.warning(f"→ {gap}")

    # Determine the stronger match
    if career_a["score"] > career_b["score"]:

        winner = career_a["name"]
        difference = career_a["score"] - career_b["score"]

    else:

        winner = career_b["name"]
        difference = career_b["score"] - career_a["score"]

    st.info(
        f"🎯 **Based on the current student profile, "
        f"{winner} has the stronger AI match by "
        f"{difference} points.**"
    )

    st.caption(
        "This comparison is guidance, not a prediction of future success. "
        "Students should consider their own goals and explore both options."
    )

    # ========================================================
    # SKILL GAP SUMMARY
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🧩 Overall Skill-Gap Analysis</div>',
        unsafe_allow_html=True
    )

    gap_columns = st.columns(5)

    for i, skill in enumerate(
        result["skill_gap_summary"]
    ):

        with gap_columns[i]:

            st.markdown(
                f"""
                <div style="
                    padding:18px;
                    border-radius:15px;
                    border:1px solid #555;
                    text-align:center;
                    min-height:100px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                ">
                <b>{skill}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ========================================================
    # 12 MONTH ROADMAP
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🛣️ Your 12-Month Roadmap</div>',
        unsafe_allow_html=True
    )

    roadmap = result["roadmap"]

    r1, r2 = st.columns(2)

    with r1:

        st.markdown(
            f"""
            <div class="roadmap-card">

            <h3>📅 Months 1–3</h3>

            <p>{roadmap["months_1_3"]}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("")

        st.markdown(
            f"""
            <div class="roadmap-card">

            <h3>📅 Months 7–9</h3>

            <p>{roadmap["months_7_9"]}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with r2:

        st.markdown(
            f"""
            <div class="roadmap-card">

            <h3>📅 Months 4–6</h3>

            <p>{roadmap["months_4_6"]}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("")

        st.markdown(
            f"""
            <div class="roadmap-card">

            <h3>📅 Months 10–12</h3>

            <p>{roadmap["months_10_12"]}</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    # ========================================================
    # FINAL ADVICE
    # ========================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">🧭 AI Mentor\'s Final Advice</div>',
        unsafe_allow_html=True
    )

    st.info(
        result["final_advice"]
    )

    # ========================================================
    # ETHICAL AI NOTICE
    # ========================================================

    st.markdown("---")

    st.warning(
        "⚖️ **Responsible AI Notice:** CareerCompass provides "
        "personalized guidance based on the information provided. "
        "It does not predict a student's future or guarantee career "
        "success. Students should explore multiple options, verify "
        "course requirements and consult teachers, parents or "
        "career professionals before making major decisions."
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🎓 CareerCompass AI • AI Career Mentor for Class 12 Students

    <br><br>

    Built to demonstrate AI-powered personalization,
    career guidance and skill-gap analysis.

    </div>
    """,
    unsafe_allow_html=True
)