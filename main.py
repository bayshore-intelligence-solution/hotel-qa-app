# import streamlit as st
# import base64
# import os
# import json
# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# load_dotenv()

# # -------------------------------
# # Streamlit UI setup
# # -------------------------------
# st.set_page_config(page_title="Brand Standards Analyzer", page_icon="🏨")
# st.title("Brand Standards Analyzer")

# st.markdown("""
# Upload your brand standards manual and photos to analyze compliance, condition, and cleanliness issues.
# """)
# api_key = os.getenv("GEMINI_API_KEY")
# # -------------------------------
# # Input section
# # -------------------------------
# pdf_file = st.file_uploader("📄 Upload a Standards", type=["pdf"])
# image_file = st.file_uploader("🖼️ Upload an image for QA check", type=["jpg", "jpeg", "png"])

# # -------------------------------
# # Gemini QA check function
# # -------------------------------
# def call_gemini_api(image_bytes: bytes):
#     """Send image to Gemini API and get JSON compliance result."""
#     client = genai.Client(api_key=api_key)
#     model = "gemini-2.5-flash"

#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
#                 types.Part.from_text(text="I am providing one image, you have to QA it and return the reponse in the following json format and return JSON in format: {\"Compliance\": true/false, \"Description\": \"...\"}"),
#             ],
#         ),
#     ]

#     generate_content_config = types.GenerateContentConfig(
#         system_instruction=[
#             types.Part.from_text(text="""We are QA team from Hotel and Hospitality. We have to do right quality check for each and everything inside the room or exterior or food and beverages or Facilities or Administrative.

# You are very much expert on this thing. You will be receiving some images of various things from hotel room or outside the room. You have to make sure whether below things are compliant or not.

# Clean
# Hygiene
# Consistent Color
# Up to the mark

# I am giving some examples like:


# Guest Room
# ------------------------------------------
# Discolored drawer
# Prior guest item
# Damaged carpet cove base
# Stained top of bed
# Noncompliant pillow
# Missing required sink stopper
# Faded toliet seat
# Ice buildup in fridge
# Mismatched applainces
# Missing light bulb
# Discolored door
# Discolored nightstand
# Mismatched hardware
# Noncompliant terry
# dirty PTAC filters
# Discolored microwave
# sink debris
# Damaged remote
# Lampshade plastic cover
# -----------------------------------------

# Exterior
# ------------------------------------------
# Peeling striping
# Faded signage
# Discolored pole base
# Damaged window screen
# -------------------------------------------

# Food and Beverage
# -------------------------------------------
# noncompliant sugar substitute

# etc.
# """),
#         ],
#     )

#     # Generate response
#     response = client.models.generate_content(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     )

#     return response.text.strip()

# # -------------------------------
# # Submit button
# # -------------------------------
# if st.button("🔍 Submit for QA Check"):
#     if not image_file:
#         st.error("Please upload an image for QA check.")
#     else:
#         with st.spinner("Analyzing image with Gemini... ⏳"):
#             image_bytes = image_file.read()
#             result_text = call_gemini_api(image_bytes)

#         st.subheader("🧾 Response:")
#         # st.code(result_text, language="json")

#         # Try parsing JSON response
#         try:
#             if "```json" in result_text:
#                 result_text = result_text.split("```json")[1].split("```")[0].strip()
#             result_json = json.loads(result_text)
#             compliant = result_json.get("Compliance", False)
#             description = result_json.get("Description", "No description provided.")

#             if compliant:
#                 st.success(f"✅ COMPLIANT\n\n{description}")
#             else:
#                 st.error(f"🚫 NON-COMPLIANT\n\n{description}")

#         except json.JSONDecodeError:
#             st.warning("⚠️ Unable to parse JSON from API response. Please check the model output.")
#             st.text(result_text)

# # -------------------------------
# # Footer
# # -------------------------------
# st.markdown("---")
# st.caption("Powered by Gemini • Mock Hotels QA Team")


import streamlit as st
import base64
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv



# -------------------------------
# Setup & Config
# -------------------------------
load_dotenv()


APP_PASSWORD = os.getenv("APP_PASSWORD")  # This will come from .env or Streamlit Secrets

st.set_page_config(page_title="Brand Standards Analyzer", page_icon="🏨")

# Initialize session state for login
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# If not authenticated, show login input
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div style='text-align:center;'>
            <h2>🏨 Brand Standards Analyzer Access</h2>
            <p>Please enter your access token to continue.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    token_input = st.text_input("🔑 Enter Access Token:", type="password")

    if st.button("Login"):
        if token_input == APP_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Access Granted ✅")
            st.rerun()
        else:
            st.error("Invalid token. Please try again.")
    st.stop()

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="🏨 Brand Standards Analyzer",
    page_icon="🏨",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -------------------------------
# Custom CSS for professional look
# -------------------------------
st.markdown("""
<style>
    .main {
        background-color: #f9fafc;
    }
    .stApp {
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    .upload-box {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .result-card {
        background: white;
        padding: 1.2rem 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .success-card {
        border-left: 6px solid #1DB954;
    }
    .error-card {
        border-left: 6px solid #E63946;
    }
    .warning-card {
        border-left: 6px solid #FFA500;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header Section
# -------------------------------
st.title("🏨 Brand Standards Analyzer")
st.write("Analyze **hotel brand standards compliance** using AI — upload your brand standards (PDF) and an image for automatic QA review.")

st.markdown("---")

# -------------------------------
# File Upload Area
# -------------------------------
col1, col2 = st.columns(2)
with col1:
    pdf_file = st.file_uploader("📄 Upload Brand Standards (PDF)", type=["pdf"])
with col2:
    image_file = st.file_uploader("🖼️ Upload Image for QA Check", type=["jpg", "jpeg", "png"])

# -------------------------------
# Gemini Function
# -------------------------------
def call_gemini_api(image_bytes: bytes):
    """Send image to Gemini API and get JSON compliance result."""
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                types.Part.from_text(text=(
                    "I am providing one image for QA inspection. "
                    "Return JSON in format: {\"Compliance\": true/false, \"Description\": \"...\"}"
                )),
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        system_instruction=[
            types.Part.from_text(text="""
You are a Hotel QA Specialist. You will evaluate images of hotel rooms, exteriors, or F&B areas
for compliance with cleanliness, consistency, and maintenance standards.

Common non-compliance issues:
- Discolored surfaces
- Missing items (light bulbs, sink stoppers)
- Dirty fabrics or filters
- Damaged or mismatched items
- Faded signage or striping

Respond strictly in JSON format:
{"Compliance": true/false, "Description": "<reason>"}
"""),
        ],
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    )
    return response.text.strip()

# -------------------------------
# Submit Button
# -------------------------------
st.markdown("### 🧪 Run QA Check")
submit = st.button("🔍 Analyze Image")

if submit:
    if not image_file:
        st.error("Please upload an image for QA check before submitting.")
    else:
        with st.spinner("Analyzing image with Gemini... ⏳"):
            image_bytes = image_file.read()
            result_text = call_gemini_api(image_bytes)

        st.markdown("### 🧾 QA Analysis Result")

        # Parse and display result
        try:
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            result_json = json.loads(result_text)
            compliant = result_json.get("Compliance", False)
            description = result_json.get("Description", "No description provided.")

            if compliant:
                st.markdown(
                    f"""
                    <div class="result-card success-card">
                        <h4>✅ COMPLIANT</h4>
                        <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="result-card error-card">
                        <h4>🚫 NON-COMPLIANT</h4>
                        <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except json.JSONDecodeError:
            st.markdown(
                f"""
                <div class="result-card warning-card">
                    <h4>⚠️ Unable to Parse JSON</h4>
                    <p>Raw model output:</p>
                    <pre>{result_text}</pre>
                </div>
                """,
                unsafe_allow_html=True
            )

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("🌐 Powered by AI • Mock Hotels QA Team • Built with Streamlit")


