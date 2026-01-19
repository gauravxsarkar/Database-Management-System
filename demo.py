import streamlit as st

# Initialize page state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Home'):
        st.session_state.page = 'home'
with col2:
    if st.button('Analytics'):
        st.session_state.page = 'analytics'
with col3:
    if st.button('Settings'):
        st.session_state.page = 'settings'

# Display content based on current page
if st.session_state.page == 'home':
    st.title('Home Page')
    st.write('Welcome!')
elif st.session_state.page == 'analytics':
    st.title('Analytics')
    st.write('Your data here')
elif st.session_state.page == 'settings':
    st.title('Settings')
    st.write('Configure your app')