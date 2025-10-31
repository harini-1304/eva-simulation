import streamlit as st
import time
from datetime import datetime
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="EVA Simulation",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        padding: 20px;
    }
    h2, h3 {
        color: #ffffff;
    }
    .stSelectbox label, .stTextInput label, .stSlider label {
        color: #ffffff !important;
        font-weight: bold;
        font-size: 1.1em;
    }
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'inactive_hours' not in st.session_state:
    st.session_state.inactive_hours = 0
if 'interaction_count' not in st.session_state:
    st.session_state.interaction_count = 0
if 'alert_history' not in st.session_state:
    st.session_state.alert_history = []
if 'wellness_score' not in st.session_state:
    st.session_state.wellness_score = 85
if 'medication_taken' not in st.session_state:
    st.session_state.medication_taken = False
if 'water_intake' not in st.session_state:
    st.session_state.water_intake = 0
if 'daily_steps' not in st.session_state:
    st.session_state.daily_steps = 0

# Header with logo
st.markdown("<h1>🤖 EVA: Emotion-Aware Voice Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ffffff;'>Elder Wellness and Safety Companion</h3>", unsafe_allow_html=True)

# Sidebar for settings and info
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")
    
    # Language selection
    language = st.selectbox("🌐 Language", ["English", "Hindi", "Tamil"])
    
    # Sensitivity settings
    st.markdown("### Alert Sensitivity")
    inactivity_threshold = st.slider("Inactivity Alert (hours)", 1, 6, 2)
    
    # User profile
    st.markdown("---")
    st.markdown("## 👤 User Profile")
    user_name = st.text_input("Elder's Name", "User")
    user_age = st.number_input("Age", 60, 100, 75)
    
    st.markdown("---")
    st.markdown("### 📊 Today's Summary")
    st.metric("Wellness Score", f"{st.session_state.wellness_score}%")
    st.metric("Interactions", st.session_state.interaction_count)
    st.metric("Water Intake", f"{st.session_state.water_intake} glasses")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 User Input Panel")
    
    # Input widgets with icons
    emotion = st.selectbox(
        '😊 Select Emotion State:',
        ['neutral', 'happy', 'sad', 'anxious'],
        help="Choose the current emotional state"
    )
    
    activity = st.selectbox(
        '🚶 Select Activity State:',
        ['active', 'inactive'],
        help="Choose the current activity level"
    )
    
    user_input = st.text_input(
        '💬 User says:',
        placeholder="Type what the user is saying...",
        help="Enter verbal input from the user"
    )
    
    # Additional health inputs
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button('💊 Medicine Taken'):
            st.session_state.medication_taken = True
            st.success("✅ Medication logged!")
    
    with col_b:
        if st.button('💧 Water Intake'):
            st.session_state.water_intake += 1
            st.success(f"✅ {st.session_state.water_intake} glasses today!")
    
    # Step counter
    st.session_state.daily_steps = st.slider('👣 Daily Steps', 0, 10000, st.session_state.daily_steps, 100)
    
    # Process interaction button
    st.markdown("---")
    if st.button('🔄 Process Interaction', type="primary", use_container_width=True):
        st.session_state.interaction_count += 1
        
        # Update inactivity counter
        if activity == 'inactive':
            st.session_state.inactive_hours += 1
        else:
            st.session_state.inactive_hours = 0
        
        # Calculate wellness score
        wellness = 100
        if emotion in ['sad', 'anxious']:
            wellness -= 20
        if activity == 'inactive':
            wellness -= 10
        if not st.session_state.medication_taken:
            wellness -= 15
        if st.session_state.water_intake < 4:
            wellness -= 10
        if st.session_state.daily_steps < 2000:
            wellness -= 10
        
        st.session_state.wellness_score = max(wellness, 0)
        
        # Generate response
        response = ''
        alert = ''
        
        # Emotion-based response
        if emotion == 'sad':
            response += '💙 I sense you might be feeling down. Would you like to listen to your favorite song or call a family member?\n\n'
        elif emotion == 'anxious':
            response += '🧡 I notice you seem anxious. Let me help you relax. Would you like some breathing exercises or calming music?\n\n'
        elif emotion == 'happy':
            response += '💚 I\'m glad you\'re feeling happy today! Keep up the positive energy!\n\n'
        else:
            response += '💛 Hello! How can I assist you today?\n\n'
        
        # Activity-based response
        if activity == 'inactive' and st.session_state.inactive_hours >= inactivity_threshold:
            response += f'⚠️ You have been inactive for {st.session_state.inactive_hours} hours. Would you like to watch a chair yoga video or do some stretching?\n\n'
            alert = f'🚨 CRITICAL ALERT: Prolonged inactivity ({st.session_state.inactive_hours} hours) and emotional distress detected. Contacting family members...'
            st.session_state.alert_history.append({
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'message': alert,
                'severity': 'High'
            })
        elif activity == 'inactive':
            response += '📢 I noticed you haven\'t moved much recently. Remember to stay active for your health!\n\n'
        
        # Medication reminder
        if not st.session_state.medication_taken:
            response += '💊 Reminder: Don\'t forget to take your medication today!\n\n'
        
        # Hydration reminder
        if st.session_state.water_intake < 4:
            response += '💧 Remember to stay hydrated! Try to drink at least 8 glasses of water today.\n\n'
        
        # Step goal
        if st.session_state.daily_steps < 2000:
            response += '👣 You\'re doing great! Try to reach 2000 steps today for better health.\n\n'
        
        # User input response
        if user_input:
            response += f'📝 I heard you say: "{user_input}". I\'m here to help you with that.\n'
        
        # Display response with animation
        st.markdown("---")
        st.markdown("### 🗨️ EVA Response")
        with st.container():
            st.success(response)
        
        # Display alert if exists
        if alert:
            st.error(alert)
            st.balloons()

with col2:
    st.markdown("### 📈 Live Dashboard")
    
    # Display metrics with colors
    st.metric(
        label="🏥 Wellness Score",
        value=f"{st.session_state.wellness_score}%",
        delta=f"{st.session_state.wellness_score - 85}%"
    )
    
    st.metric(
        label="🔢 Total Interactions",
        value=st.session_state.interaction_count
    )
    
    st.metric(
        label="⏱️ Inactivity Duration",
        value=f"{st.session_state.inactive_hours} hours",
        delta=f"{st.session_state.inactive_hours - inactivity_threshold} hrs" if st.session_state.inactive_hours > 0 else "0 hrs"
    )
    
    # Emotion indicator with emojis
    emotion_emojis = {
        'happy': '😊',
        'neutral': '😐',
        'sad': '😢',
        'anxious': '😰'
    }
    st.markdown(f"### Current Emotion: {emotion_emojis.get(emotion, '⚪')} {emotion.capitalize()}")
    
    # Activity indicator
    activity_color = '🟢' if activity == 'active' else '🔴'
    st.markdown(f"### Activity: {activity_color} {activity.capitalize()}")
    
    # Health checklist
    st.markdown("### ✅ Daily Health Checklist")
    st.checkbox("💊 Medication", value=st.session_state.medication_taken, disabled=True)
    st.checkbox("💧 Hydration (4+ glasses)", value=st.session_state.water_intake >= 4, disabled=True)
    st.checkbox("👣 Steps (2000+)", value=st.session_state.daily_steps >= 2000, disabled=True)
    
    st.markdown("---")
    
    # Control buttons
    col_x, col_y = st.columns(2)
    with col_x:
        if st.button('🔄 Reset Timer'):
            st.session_state.inactive_hours = 0
            st.success("✅ Timer reset!")
    
    with col_y:
        if st.button('🗑️ Clear Data'):
            st.session_state.inactive_hours = 0
            st.session_state.interaction_count = 0
            st.session_state.alert_history = []
            st.session_state.wellness_score = 85
            st.session_state.medication_taken = False
            st.session_state.water_intake = 0
            st.session_state.daily_steps = 0
            st.success("✅ All data cleared!")

# Alert History Section
if st.session_state.alert_history:
    st.markdown("---")
    st.markdown("### 📋 Alert History")
    
    # Create DataFrame for better display
    df = pd.DataFrame(st.session_state.alert_history[-10:])  # Show last 10 alerts
    
    for idx, row in df.iterrows():
        severity_color = "🔴" if row['severity'] == 'High' else "🟡"
        st.warning(f"{severity_color} **{row['time']}** - {row['message']}")

# Footer with info
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #ffffff; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 15px;'>
        <h3>🏥 EVA - Empowering Elderly Independence with AI</h3>
        <p><strong>Healthcare Support | Home Safety | 24x7 Companionship</strong></p>
        <p>🌐 Multilingual Support | 🔒 Privacy-First | 💰 Affordable Technology</p>
    </div>
    """, unsafe_allow_html=True)
