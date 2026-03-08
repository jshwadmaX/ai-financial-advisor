import streamlit as st
import google.generativeai as genai

def render_chatbot_section(api_key=None):
    """
    Renders the AI Chatbot Section using Streamlit and Google Gemini array.
    This function can be imported and called in your main app.
    
    Args:
        api_key (str): Your Google Gemini API key.
    """
    # Configure Gemini API if a key is provided
    if api_key:
        genai.configure(api_key=api_key)

    # Initialize chat history in Streamlit session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # CHATBOT SECTION
    st.markdown("---")
    st.markdown("### 🤖 Ask the AI Financial Advisor")

    # Define columns for chat area and tips
    chat_col1, chat_col2 = st.columns([2, 1])

    with chat_col1:
        # Chat Display Area
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.chat_history:
                if msg.get('user'):
                    st.markdown(
                        f'<div class="user-message" style="background-color: #d1e7dd; padding: 10px; border-radius: 10px; margin-bottom: 5px; text-align: right;"><b>You:</b> {msg["user"]}</div>', 
                        unsafe_allow_html=True
                    )
                if msg.get('bot'):
                    st.markdown(
                        f'<div class="bot-message" style="background-color: #f8d7da; padding: 10px; border-radius: 10px; margin-bottom: 15px; text-align: left;"><b>Advisor:</b> {msg["bot"]}</div>', 
                        unsafe_allow_html=True
                    )

        # Chat Input
        # We use a distinct key for the text area
        user_query = st.text_area("Type your financial query...", key="chat_input", height=100)
        st.session_state.user_query = user_query

        # Action Buttons Layout
        ask_col1, ask_col2, ask_col3 = st.columns([1, 2, 1])
        with ask_col2:
            ask_btn = st.button("💬 Send Message", use_container_width=True)

        # Handle Send Message Action
        if ask_btn:
            if st.session_state.user_query.strip():
                # Add user query to chat history
                st.session_state.chat_history.append({"user": st.session_state.user_query, "bot": ""})
                
                # Fetch AI response
                with st.spinner("Analyzing your request..."):
                    try:
                        if api_key:
                            model = genai.GenerativeModel('gemini-2.0-flash')
                            # Persona prompt for the AI model
                            system_prompt = (
                                "You are a professional, highly intelligent, and helpful AI Financial Advisor. "
                                "Provide clear, data-driven, and actionable financial insights to the user. "
                                f"User question: {st.session_state.user_query}"
                            )
                            response = model.generate_content(system_prompt)
                            bot_response = response.text
                        else:
                            bot_response = "⚠️ Please provide a Gemini API Key to receive a response."
                    except Exception as e:
                        bot_response = f"❌ Failed to reach the AI model: {str(e)}"
                
                # Append bot response to history
                st.session_state.chat_history[-1]["bot"] = bot_response
                st.rerun()
            else:
                st.warning("Please type a message before sending.")

    with chat_col2:
        # Chat Tips Sidebar
        st.markdown("""
        <div class='card' style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #dee2e6;'>
            <h4 style='color: #495057;'>💡 Chat Tips</h4>
            <ul style='font-size: 0.9rem; color: #6c757d; line-height: 1.6;'>
                <li>Ask about investments</li>
                <li>Get budgeting advice</li>
                <li>Discuss debt management</li>
                <li>Plan for specific goals</li>
                <li>Understand financial terms</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Example usage (for testing this file independently)
if __name__ == "__main__":
    st.set_page_config(page_title="AI Financial Advisor Chatbot")
    st.title("Test Chatbot Section")
    # To test locally, you can call render_chatbot_section(api_key="YOUR_API_KEY")
    render_chatbot_section()
