# --- Imports ---
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fpdf import FPDF
import datetime
import plotly.graph_objects as go
import base64
import warnings
import json
import random
import string

# Import pymongo for MongoDB integration
from pymongo import MongoClient

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/medical1"
client = MongoClient(MONGO_URI)
db = client.get_database()
users_collection = db['users']

# New collections for predictions
diabetes_predictions_collection = db['diabetes_predictions']
heart_predictions_collection = db['heart_predictions']
parkinsons_predictions_collection = db['parkinsons_predictions']

# Functions to save prediction data
def save_diabetes_prediction(email, input_data, prediction, proba, risk_level):
    diabetes_predictions_collection.insert_one({
        'email': email,
        'input_data': input_data,
        'prediction': int(prediction),
        'probability': float(proba),
        'risk_level': risk_level,
        'timestamp': datetime.datetime.now()
    })

def save_heart_prediction(email, input_data, prediction, proba, risk_level):
    heart_predictions_collection.insert_one({
        'email': email,
        'input_data': input_data,
        'prediction': int(prediction),
        'probability': float(proba),
        'risk_level': risk_level,
        'timestamp': datetime.datetime.now()
    })

def save_parkinsons_prediction(email, input_data, prediction, proba, risk_level):
    parkinsons_predictions_collection.insert_one({
        'email': email,
        'input_data': input_data,
        'prediction': int(prediction),
        'probability': float(proba),
        'risk_level': risk_level,
        'timestamp': datetime.datetime.now()
    })

# --- 3D Animated Health Toys Background ---
def set_3d_health_toys_bg():
    st.markdown(
        '''
        <style>
        .stApp {
            position: relative;
            min-height: 100vh;
            overflow: hidden;
            background: linear-gradient(135deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
        }
        .health-toys-bg {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 0;
            pointer-events: none;
        }
        .main .block-container, .sidebar .sidebar-content {
            position: relative;
            z-index: 1;
        }
        </style>
        <svg class="health-toys-bg" width="100%" height="100%" viewBox="0 0 1920 1080" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g>
                <g>
                    <circle cx="300" cy="200" r="50" fill="#FF6F91">
                        <animate attributeName="cy" values="200;400;200" dur="8s" repeatCount="indefinite"/>
                    </circle>
                    <rect x="1200" y="700" width="80" height="40" rx="20" fill="#6FCF97">
                        <animate attributeName="x" values="1200;1400;1200" dur="10s" repeatCount="indefinite"/>
                    </rect>
                    <ellipse cx="900" cy="300" rx="40" ry="20" fill="#FFD166">
                        <animate attributeName="cx" values="900;1100;900" dur="7s" repeatCount="indefinite"/>
                    </ellipse>
                    <!-- Heart icon -->
                    <path d="M600 600 C600 570, 650 570, 650 600 C650 630, 600 650, 600 700 C600 650, 550 630, 550 600 C550 570, 600 570, 600 600 Z" fill="#EB5757">
                        <animateTransform attributeName="transform" type="translate" values="0 0; 0 50; 0 0" dur="6s" repeatCount="indefinite"/>
                    </path>
                    <!-- Stethoscope icon (simplified) -->
                    <path d="M1600 300 Q1620 350 1600 400 Q1580 450 1600 500" stroke="#2D9CDB" stroke-width="10" fill="none">
                        <animateTransform attributeName="transform" type="translate" values="0 0; -100 100; 0 0" dur="12s" repeatCount="indefinite"/>
                    </path>
                    <!-- Pill icon -->
                    <rect x="400" y="800" width="100" height="40" rx="20" fill="#BB6BD9">
                        <animate attributeName="y" values="800;900;800" dur="9s" repeatCount="indefinite"/>
                    </rect>
                </g>
                <!-- Funny/healthcare icons -->
                <!-- Ambulance -->
                <g>
                    <rect x="-200" y="950" width="120" height="50" rx="15" fill="#fff" stroke="#333" stroke-width="4">
                        <animate attributeName="x" values="-200;2100;-200" dur="18s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="-180" y="970" width="40" height="30" rx="8" fill="#E63946">
                        <animate attributeName="x" values="-180;2080;-180" dur="18s" repeatCount="indefinite"/>
                    </rect>
                    <circle cx="-170" cy="1010" r="10" fill="#333">
                        <animate attributeName="cx" values="-170;2110;-170" dur="18s" repeatCount="indefinite"/>
                    </circle>
                    <circle cx="-100" cy="1010" r="10" fill="#333">
                        <animate attributeName="cx" values="-100;2180;-100" dur="18s" repeatCount="indefinite"/>
                    </circle>
                    <!-- Red cross on ambulance -->
                    <rect x="-150" y="970" width="10" height="30" fill="#E63946">
                        <animate attributeName="x" values="-150;2100;-150" dur="18s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="-160" y="980" width="30" height="10" fill="#E63946">
                        <animate attributeName="x" values="-160;2090;-160" dur="18s" repeatCount="indefinite"/>
                    </rect>
                </g>
                <!-- Bandage (bouncing) -->
                <rect x="1700" y="100" width="100" height="30" rx="15" fill="#F9C74F" stroke="#333" stroke-width="3">
                    <animate attributeName="y" values="100;200;100" dur="7s" repeatCount="indefinite"/>
                </rect>
                <rect x="1730" y="110" width="40" height="10" rx="5" fill="#fff" stroke="#333" stroke-width="2">
                    <animate attributeName="y" values="110;210;110" dur="7s" repeatCount="indefinite"/>
                </rect>
                <!-- Syringe (rotating) -->
                <g>
                    <rect x="100" y="900" width="80" height="20" rx="8" fill="#A3CEF1">
                        <animateTransform attributeName="transform" type="rotate" from="0 140 910" to="360 140 910" dur="10s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="170" y="905" width="20" height="10" rx="3" fill="#333">
                        <animateTransform attributeName="transform" type="rotate" from="0 180 910" to="360 180 910" dur="10s" repeatCount="indefinite"/>
                    </rect>
                </g>
                <!-- Medical cross (floating) -->
                <g>
                    <rect x="1500" y="600" width="40" height="120" fill="#2D9CDB">
                        <animate attributeName="y" values="600;700;600" dur="11s" repeatCount="indefinite"/>
                    </rect>
                    <rect x="1460" y="640" width="120" height="40" fill="#2D9CDB">
                        <animate attributeName="y" values="640;740;640" dur="11s" repeatCount="indefinite"/>
                    </rect>
                </g>
            </g>
        </svg>
        ''', unsafe_allow_html=True)

set_3d_health_toys_bg()

# Suppress all warnings (including sklearn warnings)
warnings.filterwarnings('ignore')

# --- Load Models ---
try:
    diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
    parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))
except Exception as e:
    st.error("Error loading models. Please check if model files exist in the correct location.")
    st.stop()

# --- API & Email Setup ---
OPENROUTER_API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

GMAIL_USER = "vyshnaviranaveni1@gmail.com"
GMAIL_APP_PASSWORD = "wvie jtyh caot xtbk"

# --- User Management ---
USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# Replace load_users and save_users with MongoDB operations
def load_users():
    users = {}
    for user in users_collection.find():
        email = user.get('email')
        if email:
            users[email] = {
                'password': user.get('password'),
                'verified': user.get('verified', False),
                'otp': user.get('otp')
            }
    return users

def save_users(users):
    for email, data in users.items():
        users_collection.update_one(
            {'email': email},
            {'$set': {
                'password': data.get('password'),
                'verified': data.get('verified', False),
                'otp': data.get('otp')
            }},
            upsert=True
        )

def send_otp_email(email, otp):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = email
    msg['Subject'] = 'Your OTP Verification Code'
    msg.attach(MIMEText(f'Your OTP code is: {otp}', 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    server.sendmail(GMAIL_USER, email, msg.as_string())
    server.quit()

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

# --- Auth UI ---
def show_login():
    st.title('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        password = password.strip()
        user = users_collection.find_one({'email': email})
        if user and user.get('password') == password:
            if user.get('verified', False):
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success('Login successful!')
            else:
                st.warning('Please verify your email with OTP.')
                st.session_state.pending_verification = email
        else:
            st.error('Invalid credentials.')
    if st.button('Go to Signup'):
        st.session_state.page = 'signup'

    # Add forgot password clickable text
    if st.button('Forgot Password?'):
        st.session_state.page = 'forgot_password'

# New function for forgot password UI and logic
def show_forgot_password():
    st.title('Forgot Password')
    email = st.text_input('Enter your registered email')
    if st.button('Send OTP'):
        users = load_users()
        if email in users:
            otp = generate_otp()
            users[email]['otp'] = otp
            save_users(users)
            send_otp_email(email, otp)
            st.session_state.forgot_password_email = email
            st.session_state.page = 'reset_password'
            st.success('OTP sent to your email. Please check your inbox.')
        else:
            st.error('Email not registered.')
    if st.button('Back to Login'):
        st.session_state.page = 'login'

# New function for resetting password after OTP verification
def show_reset_password():
    st.title('Reset Password')
    email = st.session_state.get('forgot_password_email')
    otp_input = st.text_input('Enter OTP sent to your email')
    new_password = st.text_input('Enter new password', type='password')
    if st.button('Reset Password'):
        users = load_users()
        stored_otp = users.get(email, {}).get('otp')
        st.write(f"Debug: stored OTP = {stored_otp}, entered OTP = '{otp_input}'")
        if email and stored_otp == otp_input.strip():
            users[email]['password'] = new_password
            users[email].pop('otp', None)
            save_users(users)
            st.session_state.pop('forgot_password_email', None)
            st.session_state.page = 'login'
            st.success('Password reset successful! You can now log in.')
        else:
            st.error('Invalid OTP or email.')
    if st.button('Back to Login'):
        st.session_state.page = 'login'

def show_signup():
    st.title('Signup')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Signup'):
        user = users_collection.find_one({'email': email})
        if user:
            st.error('User already exists.')
        else:
            otp = generate_otp()
            users_collection.insert_one({
                'email': email,
                'password': password,
                'verified': False,
                'otp': otp
            })
            send_otp_email(email, otp)
            st.session_state.pending_verification = email
            st.success('OTP sent to your email. Please verify.')
    if st.button('Go to Login'):
        st.session_state.page = 'login'

def show_otp_verification():
    st.title('Verify OTP')
    email = st.session_state.get('pending_verification')
    otp_input = st.text_input('Enter OTP sent to your email')
    if st.button('Verify OTP'):
        users = load_users()
        if email and users.get(email, {}).get('otp') == otp_input:
            users[email]['verified'] = True
            users[email].pop('otp', None)
            save_users(users)
            st.session_state.pop('pending_verification', None)
            st.session_state.page = 'login'
            st.success('Email verified! You can now log in.')
        else:
            st.error('Invalid OTP.')
    if st.button('Back to Login'):
        st.session_state.page = 'login'

# --- Main App Navigation ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'login'

if not st.session_state.logged_in:
    if 'pending_verification' in st.session_state:
        show_otp_verification()
    elif st.session_state.page == 'login':
        show_login()
    elif st.session_state.page == 'signup':
        show_signup()
    elif st.session_state.page == 'forgot_password':
        show_forgot_password()
    elif st.session_state.page == 'reset_password':
        show_reset_password()
    st.stop()
# --- Main app code continues below (only if logged in) ---

# --- Sidebar Menu ---
with st.sidebar:
    selected = option_menu(
        'HealthScope AI',
        ['Diabetes Analysis', 'Heart Health Scan', 'Parkinson\'s Check', 'AI Health Assistant'],
        icons=['activity', 'heart', 'person', 'robot'],
        default_index=0
    )

# --- Helper Functions ---
def get_diabetes_prediction(input_data):
    prediction = diabetes_model.predict(input_data)[0]
    try:
        proba = diabetes_model.predict_proba(input_data)[0][1] * 100
    except AttributeError:
        proba = 90.0 if prediction == 1 else 10.0
    return prediction, proba

def get_heart_prediction(input_data):
    prediction = heart_disease_model.predict(input_data)[0]
    try:
        proba = heart_disease_model.predict_proba(input_data)[0][1] * 100
    except AttributeError:
        proba = 85.0 if prediction == 1 else 15.0
    return prediction, proba

def get_parkinsons_prediction(input_data):
    prediction = parkinsons_model.predict(input_data)[0]
    try:
        proba = parkinsons_model.predict_proba(input_data)[0][1] * 100
    except AttributeError:
        proba = 80.0 if prediction == 1 else 20.0
    return prediction, proba

def live_health_gauge(value, title, ranges):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, ranges[0]], 'color': "lightgreen"},
                {'range': [ranges[0], ranges[1]], 'color': "yellow"},
                {'range': [ranges[1], 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }))
    st.plotly_chart(fig, use_container_width=True)

def pulse_plot(proba, risk_level):
    x = np.linspace(0, 10, 100)
    if risk_level == "High":
        y = np.sin(x) * 1.5 + np.random.normal(0, 0.1, 100)
        color = "red"
    elif risk_level == "Moderate":
        y = np.sin(x) * 1.0 + np.random.normal(0, 0.05, 100)
        color = "orange"
    else:
        y = np.sin(x) * 0.5 + np.random.normal(0, 0.02, 100)
        color = "green"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', line=dict(color=color, width=4)))
    st.plotly_chart(fig)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'HealthScope AI Report', ln=True, align='C')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Courier', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

def create_pdf(content):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_body(content)
    return pdf.output(dest='S').encode('latin1')

# Add this helper function for creating styled containers
def create_results_container(title, content):
    st.markdown(f"""
        <div class="results-container">
            <h3>{title}</h3>
            {content}
        </div>
    """, unsafe_allow_html=True)

# Add these functions after the create_pdf function
def get_diabetes_suggestions(risk_level, proba):
    suggestions = {
        "Low": [
            "✅ Maintain your healthy lifestyle",
            "🥗 Continue balanced diet with whole grains and vegetables",
            "🚶‍♂️ Regular exercise (30 minutes daily)",
            "⏰ Regular health check-ups annually"
        ],
        "Moderate": [
            "⚠️ Monitor blood sugar levels regularly",
            "🥗 Reduce intake of refined carbohydrates and sugars",
            "🏃‍♂️ Increase physical activity to 45 minutes daily",
            "⚖️ Maintain healthy weight",
            "🔍 Get blood sugar tested every 6 months"
        ],
        "High": [
            "🚨 Immediate consultation with healthcare provider",
            "📊 Daily blood sugar monitoring",
            "🥗 Strict diet control - avoid sugary foods",
            "💊 Consider medication if prescribed",
            "🏃‍♂️ Regular exercise under medical supervision",
            "⚖️ Weight management program if needed"
        ]
    }
    return suggestions[risk_level]

def get_heart_suggestions(risk_level, proba):
    suggestions = {
        "Low": [
            "✅ Maintain heart-healthy lifestyle",
            "🥗 Continue balanced, low-salt diet",
            "🚶‍♂️ Regular moderate exercise",
            "😴 Adequate sleep (7-8 hours)"
        ],
        "Moderate": [
            "⚠️ Monitor blood pressure regularly",
            "🥗 Reduce saturated fats and salt intake",
            "🏃‍♂️ Structured exercise program",
            "🚭 Quit smoking if applicable",
            "😌 Stress management techniques"
        ],
        "High": [
            "🚨 Immediate cardiac consultation",
            "💊 Follow prescribed medications strictly",
            "📊 Daily blood pressure monitoring",
            "🥗 Heart-healthy diet plan",
            "⚡ Know heart attack warning signs",
            "🏥 Regular cardiac check-ups"
        ]
    }
    return suggestions[risk_level]

def get_parkinsons_suggestions(risk_level, proba):
    suggestions = {
        "Low": [
            "✅ Maintain active lifestyle",
            "🧠 Regular cognitive exercises",
            "🎵 Music and movement activities",
            "🥗 Balanced nutrition"
        ],
        "Moderate": [
            "⚠️ Regular neurological check-ups",
            "💪 Physical therapy exercises",
            "🧠 Brain-training activities",
            "😌 Stress reduction techniques",
            "🎨 Engage in fine motor activities"
        ],
        "High": [
            "🚨 Consult neurologist immediately",
            "💊 Discuss treatment options",
            "🏃‍♂️ Specialized exercise program",
            "🗣️ Speech therapy if needed",
            "🤝 Join support groups",
            "📝 Keep symptom diary"
        ]
    }
    return suggestions[risk_level]

def display_suggestions(suggestions):
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;'>
            <h4 style='color: #2c3e50; margin-bottom: 15px;'>📋 Recommended Precautions & Actions:</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
    """, unsafe_allow_html=True)
    
    for suggestion in suggestions:
        st.markdown(f"""
            <li style='margin-bottom: 10px; padding: 10px; background-color: white; 
                       border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                {suggestion}
            </li>
        """, unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

# --- Diabetes Analysis Page ---
if selected == 'Diabetes Analysis':
    with st.container():
        st.header("🩺 Real-Time Diabetes Risk Assessment")
        
        # Initialize session state for storing prediction results
        if 'diabetes_prediction' not in st.session_state:
            st.session_state.diabetes_prediction = None
            st.session_state.diabetes_proba = None
            st.session_state.diabetes_risk_level = None
            st.session_state.diabetes_report = None
        
        col1, col2 = st.columns(2)
        with col1:
            glucose = st.slider('Glucose Level', 50, 300, 120)
            bp = st.slider('Blood Pressure', 40, 180, 80)
            skin = st.slider('Skin Thickness', 0, 100, 20)
            age = st.slider('Age', 10, 100, 30)
        with col2:
            insulin = st.slider('Insulin Level', 0, 300, 80)
            bmi = st.slider('BMI', 10.0, 50.0, 23.0)
            pedigree = st.slider('Diabetes Pedigree', 0.0, 2.5, 0.5)
            pregnancies = st.slider('Pregnancies', 0, 15, 0)
            
        input_data = [[pregnancies, glucose, bp, skin, insulin, bmi, pedigree, age]]
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            predict_btn = st.button('Generate Prediction Report')
        
        if predict_btn:
            with st.spinner('Analyzing your health data...'):
                prediction, proba = get_diabetes_prediction(input_data)
                risk_level = "High" if proba > 70 else "Moderate" if proba > 40 else "Low"
                st.session_state.diabetes_prediction = prediction
                st.session_state.diabetes_proba = proba
                st.session_state.diabetes_risk_level = risk_level

                # Save prediction to database
                if st.session_state.get('user_email'):
                    save_diabetes_prediction(st.session_state.user_email, input_data, prediction, proba, risk_level)

                # Display results
                st.markdown(f"""
                    <div style='text-align: center; font-size: 1.2em; margin: 1em 0; border-radius: 10px; padding: 1em;'>
                        <strong>Prediction:</strong> {'Diabetes Detected' if prediction == 1 else 'No Diabetes'}<br>
                        <strong>Risk Level:</strong> <span style='color: {'red' if risk_level == 'High' else 'orange' if risk_level == 'Moderate' else 'green'}'>{risk_level}</span>
                    </div>
                """, unsafe_allow_html=True)
                # Display visualizations
                live_health_gauge(proba, "Diabetes Risk Meter", [40, 70])
                # Display suggestions based on risk level
                suggestions = get_diabetes_suggestions(risk_level, proba)
                display_suggestions(suggestions)
                pulse_plot(proba, risk_level)
                report_content = f"""
                Diabetes Analysis Report

                Prediction: {'Positive' if prediction == 1 else 'Negative'}
                Probability: {proba:.2f}%
                Risk Level: {risk_level}

                Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                st.session_state.diabetes_report = report_content
                # Create PDF with loading state
                with st.spinner('Preparing your report...'):
                    pdf_bytes = create_pdf(report_content)
                    st.download_button(
                        "📥 Download Detailed Report",
                        data=pdf_bytes,
                        file_name="diabetes_report.pdf",
                        mime="application/pdf"
                    )

        # Email form with improved styling
        if st.session_state.diabetes_prediction is not None:
            st.markdown("---")
            st.subheader("📧 Share Your Report")
            with st.form("email_form_diabetes"):
                recipient = st.text_input("Enter recipient's email address:")
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    submit = st.form_submit_button("Send Report")
                if submit and st.session_state.diabetes_report:
                    with st.spinner('Sending report...'):
                        try:
                            pdf_bytes = create_pdf(st.session_state.diabetes_report)
                            msg = MIMEMultipart()
                            msg['From'] = GMAIL_USER
                            msg['To'] = recipient
                            msg['Subject'] = "Your Diabetes Health Report"
                            msg.attach(MIMEText("Attached is your Diabetes Health Report.", "plain"))
                            attach = MIMEText(pdf_bytes, 'base64', 'latin1')
                            attach.add_header('Content-Disposition', 'attachment', filename='diabetes_report.pdf')
                            msg.attach(attach)

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
                            server.sendmail(GMAIL_USER, recipient, msg.as_string())
                            server.quit()

                            st.markdown("""
                                <div class='success-message'>
                                    ✅ Report successfully sent to {recipient}!
                                </div>
                            """.format(recipient=recipient), unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown("""
                                <div class='error-message'>
                                    ❌ Failed to send email: {error}
                                </div>
                            """.format(error=str(e)), unsafe_allow_html=True)

# --- Heart Health Scan Page ---
elif selected == 'Heart Health Scan':
    with st.container():
        st.header("❤ Real-Time Cardiac Risk Assessment")
        
        # Initialize session state for storing prediction results
        if 'heart_prediction' not in st.session_state:
            st.session_state.heart_prediction = None
            st.session_state.heart_proba = None
            st.session_state.heart_risk_level = None
            st.session_state.heart_report = None
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.slider('Age', 20, 100, 50)
            trestbps = st.slider('Resting Blood Pressure', 90, 200, 120)
            chol = st.slider('Cholesterol', 100, 600, 200)
            thal = st.slider('Thalassemia (0-2)', 0, 2, 1)
        with col2:
            thalach = st.slider('Max Heart Rate', 60, 220, 150)
            oldpeak = st.slider('ST Depression', 0.0, 6.0, 1.0, 0.1)
            ca = st.slider('Major vessels (0-3)', 0, 3, 0)
            slope = st.slider('Slope (0-2)', 0, 2, 1)

        sex = st.radio("Sex", ['Male', 'Female'])
        cp = st.selectbox('Chest Pain Type', ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'])
        sex_val = 1 if sex == 'Male' else 0
        cp_val = ['Typical Angina', 'Atypical Angina', 'Non-anginal Pain', 'Asymptomatic'].index(cp)

        input_data = [[age, sex_val, cp_val, trestbps, chol, 0, 0, thalach, 0, oldpeak, slope, ca, thal]]
        predict_btn = st.button('Predict')
        
        if predict_btn:
            with st.spinner('Analyzing your health data...'):
                prediction, proba = get_heart_prediction(input_data)
                risk_level = "High" if proba > 70 else "Moderate" if proba > 40 else "Low"
                st.session_state.heart_prediction = prediction
                st.session_state.heart_proba = proba
                st.session_state.heart_risk_level = risk_level

                # Save prediction to database
                if st.session_state.get('user_email'):
                    save_heart_prediction(st.session_state.user_email, input_data, prediction, proba, risk_level)

                # Display results
                st.subheader(f"Prediction: {'Heart Disease Detected' if prediction == 1 else 'No Heart Disease'}")
                live_health_gauge(proba, "Heart Disease Risk Meter", [40, 70])
                # Display suggestions based on risk level
                suggestions = get_heart_suggestions(risk_level, proba)
                display_suggestions(suggestions)
                pulse_plot(proba, risk_level)
                report_content = f"""
                Heart Health Scan Report

                Prediction: {'Positive' if prediction == 1 else 'Negative'}
                Probability: {proba:.2f}%
                Risk Level: {risk_level}

                Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                st.session_state.heart_report = report_content
                # Create PDF
                pdf_bytes = create_pdf(report_content)
                st.download_button("📥 Download Heart Health Report", data=pdf_bytes, file_name="heart_report.pdf", mime="application/pdf")

        # Email form outside the prediction button block
        if st.session_state.heart_prediction is not None:
            with st.form("email_form_heart"):
                recipient = st.text_input("Recipient Email:")
                submit = st.form_submit_button("📧 Send Report")
                if submit and st.session_state.heart_report:
                    try:
                        pdf_bytes = create_pdf(st.session_state.heart_report)
                        msg = MIMEMultipart()
                        msg['From'] = GMAIL_USER
                        msg['To'] = recipient
                        msg['Subject'] = "Your Heart Health Report"
                        msg.attach(MIMEText("Attached is your Heart Health Report.", "plain"))
                        attach = MIMEText(pdf_bytes, 'base64', 'latin1')
                        attach.add_header('Content-Disposition', 'attachment', filename='heart_report.pdf')
                        msg.attach(attach)

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
                        server.sendmail(GMAIL_USER, recipient, msg.as_string())
                        server.quit()

                        st.success(f"✅ Report sent to {recipient}!")
                    except Exception as e:
                        st.error(f"Failed to send email: {str(e)}")

# --- Parkinson's Check Page ---
elif selected == 'Parkinson\'s Check':
    with st.container():
        st.header("🧠 Real-Time Neurological Assessment")
        
        # Initialize session state for storing prediction results
        if 'parkinsons_prediction' not in st.session_state:
            st.session_state.parkinsons_prediction = None
            st.session_state.parkinsons_proba = None
            st.session_state.parkinsons_risk_level = None
            st.session_state.parkinsons_report = None
        
        col1, col2 = st.columns(2)
        with col1:
            fo = st.slider('Average Vocal Fundamental Frequency (Hz)', 80.0, 260.0, 140.0)
            fhi = st.slider('Maximum Vocal Fundamental Frequency (Hz)', 90.0, 600.0, 200.0)
            jitter = st.slider('Jitter (%)', 0.0, 0.1, 0.005, 0.001)
            shimmer = st.slider('Shimmer (dB)', 0.0, 2.0, 0.2, 0.01)
        with col2:
            hnr = st.slider('HNR (Harmonics-to-Noise Ratio)', 0.0, 40.0, 20.0)
            rpde = st.slider('RPDE (Signal Complexity)', 0.0, 1.0, 0.5)
            ppe = st.slider('PPE (Signal Variation)', 0.0, 0.5, 0.2)
            dfa = st.slider('DFA (Fractal Dimension)', 0.0, 1.0, 0.5)

        input_data = [[
            fo, fhi, (fo+fhi)/2, jitter*100, jitter*1000,
            jitter*500, jitter*500, jitter*1500, shimmer, shimmer*20,
            shimmer*4, shimmer*4, shimmer*10, shimmer*30, hnr/40, hnr/20,
            rpde, dfa, -5.0, 0.2, 2.0, ppe
        ]]
        predict_btn = st.button('Predict')
        
        if predict_btn:
            with st.spinner('Analyzing your health data...'):
                prediction, proba = get_parkinsons_prediction(input_data)
                risk_level = "High" if proba > 70 else "Moderate" if proba > 40 else "Low"
                st.session_state.parkinsons_prediction = prediction
                st.session_state.parkinsons_proba = proba
                st.session_state.parkinsons_risk_level = risk_level

                # Save prediction to database
                if st.session_state.get('user_email'):
                    save_parkinsons_prediction(st.session_state.user_email, input_data, prediction, proba, risk_level)

                # Display results
                st.subheader("Prediction: {}".format("Parkinson's Detected" if prediction == 1 else "No Parkinson's"))
                live_health_gauge(proba, "Parkinson's Risk Meter", [40, 70])
                # Display suggestions based on risk level
                suggestions = get_parkinsons_suggestions(risk_level, proba)
                display_suggestions(suggestions)
                pulse_plot(proba, risk_level)
                report_content = f"""
                Parkinson's Check Report

                Prediction: {'Positive' if prediction == 1 else 'Negative'}
                Probability: {proba:.2f}%
                Risk Level: {risk_level}

                Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                st.session_state.parkinsons_report = report_content
                # Create PDF
                pdf_bytes = create_pdf(report_content)
                st.download_button("📥 Download Parkinson Report", data=pdf_bytes, file_name="parkinsons_report.pdf", mime="application/pdf")

        # Email form outside the prediction button block
        if st.session_state.parkinsons_prediction is not None:
            with st.form("email_form_parkinsons"):
                recipient = st.text_input("Recipient Email:")
                submit = st.form_submit_button("📧 Send Report")
                if submit and st.session_state.parkinsons_report:
                    try:
                        pdf_bytes = create_pdf(st.session_state.parkinsons_report)
                        msg = MIMEMultipart()
                        msg['From'] = GMAIL_USER
                        msg['To'] = recipient
                        msg['Subject'] = "Your Parkinson's Report"
                        msg.attach(MIMEText("Attached is your Parkinson's Report.", "plain"))
                        attach = MIMEText(pdf_bytes, 'base64', 'latin1')
                        attach.add_header('Content-Disposition', 'attachment', filename='parkinsons_report.pdf')
                        msg.attach(attach)

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
                        server.sendmail(GMAIL_USER, recipient, msg.as_string())
                        server.quit()

                        st.success(f"✅ Report sent to {recipient}!")
                    except Exception as e:
                        st.error(f"Failed to send email: {str(e)}")

# --- AI Health Assistant Page ---
elif selected == 'AI Health Assistant':
    with st.container():
        st.header("🤖 AI Health Assistant")

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": "You are a helpful medical assistant."}]

        for msg in st.session_state.messages[1:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Ask a medical question...")
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)

            st.session_state.messages.append({"role": "user", "content": prompt})

            try:
                response = requests.post(API_URL, headers=HEADERS, json={"model": MODEL, "messages": st.session_state.messages})
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]

                with st.chat_message("assistant"):
                    st.markdown(reply)

                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"Failed to get response: {e}")

        # --- Chat Report Generation ---
        st.markdown("---")
        st.subheader("📄 Download or Email Chat Report")

        chat_content = ""
        for msg in st.session_state.messages[1:]:
            who = "You" if msg["role"] == "user" else "Assistant"
            chat_content += f"{who}: {msg['content']}\n\n"

        pdf_bytes = create_pdf(chat_content)
        st.download_button("📥 Download Chat Report", data=pdf_bytes, file_name="chatbot_report.pdf", mime="application/pdf")

        with st.form("email_form_chatbot"):
            recipient = st.text_input("Recipient Email:")
            submit = st.form_submit_button("📧 Send Chat Report")
            if submit:
                try:
                    msg = MIMEMultipart()
                    msg['From'] = GMAIL_USER
                    msg['To'] = recipient
                    msg['Subject'] = "Your AI Health Assistant Chat Report"
                    msg.attach(MIMEText("Please find your chat report attached.", "plain"))
                    attach = MIMEText(pdf_bytes, 'base64', 'latin1')
                    attach.add_header('Content-Disposition', 'attachment', filename='chatbot_report.pdf')
                    msg.attach(attach)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
                    server.sendmail(GMAIL_USER, recipient, msg.as_string())
                    server.quit()

                    st.success(f"✅ Chat report sent to {recipient}!")
                except Exception as e:
                    st.error(f"Failed to send email: {str(e)}")