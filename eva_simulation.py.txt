import streamlit as st

st.title('EVA Simulation: Emotion-Aware Voice Assistant for Elder Wellness and Safety')

st.write("This interactive simulation mimics EVA's behavior based on emotion and activity inputs.")

# Input widgets
emotion = st.selectbox('Select Emotion State:', ['neutral', 'happy', 'sad', 'anxious'])
activity = st.selectbox('Select Activity State:', ['active', 'inactive'])
user_input = st.text_input('User says:', '')

# Tracking inactivity duration (simple session counter)
if 'inactive_hours' not in st.session_state:
    st.session_state.inactive_hours = 0

# Update inactivity counter
if activity == 'inactive':
    st.session_state.inactive_hours += 1
else:
    st.session_state.inactive_hours = 0

# Generate EVA response
response = ''
alert = ''

if emotion in ['sad', 'anxious']:
    response += 'I sense you might be feeling down. Would you like to listen to your favorite song or call a family member?\n'
else:
    response += 'Hello! How can I assist you today?\n'

if activity == 'inactive' and st.session_state.inactive_hours >= 2:
    response += 'You have been inactive for a while. Would you like to take a short walk or some stretching?\n'
    alert = 'ALERT: Inactivity and emotional distress detected. Contacting family...'
elif activity == 'inactive':
    response += "I noticed you haven't moved much recently. Remember to stay active for your health!\n"

# Display output
st.subheader('EVA Response')
st.text(response)

if alert:
    st.subheader('Family Alert')
    st.text(alert)

# Button to reset inactivity hours
def reset_inactivity():
    st.session_state.inactive_hours = 0

if st.button('Reset Inactivity Timer'):
    reset_inactivity()

st.write("Use the controls above to simulate elder emotion and activity states and see EVA's adaptive responses.")
