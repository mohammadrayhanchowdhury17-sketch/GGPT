import streamlit as st
import google.generativeai as genai

# Gemini API Config
genai.configure(api_key="AQ.Ab8RN6LztG4DHHuq0z61PJG4jQ1ON_l3zmiuxTxByuKIszLObA")

# Page Config (ChatGPT Look & Feel)
st.set_page_config(
    page_title="GGPT - AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Title & Styling
st.markdown("<h1 style='text-align: center; color: #10a37f;'>🤖 GGPT</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>ChatGPT style All-in-One Smart AI Assistant</p>", unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image_url" in msg:
            st.image(msg["image_url"], use_container_width=True)

# User Input Box
if prompt := st.chat_input("Ask GGPT anything or ask to generate an image..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if user wants an image (Image Generation Intent)
    lower_prompt = prompt.lower()
    if any(keyword in lower_prompt for keyword in ["image", "photo", "picture", "draw", "generate image", "ছবি", "পিকচার", "আঁকো"]):
        with st.chat_message("assistant"):
            with st.spinner("Generating image for you..."):
                formatted_prompt = prompt.replace(" ", "%20")
                img_url = f"https://image.pollinations.ai/prompt/{formatted_prompt}?width=800&height=800&nologo=true"
                st.markdown("Here is your requested image:")
                st.image(img_url, use_container_width=True)
                st.session_state.messages.append({"role": "assistant", "content": "Here is your requested image:", "image_url": img_url})
    else:
        # Standard Chatbot / Web Search Response
        with st.chat_message("assistant"):
            with st.spinner("GGPT is thinking..."):
                try:
                    # Uses Gemini with Google Search enabled
                    model = genai.GenerativeModel(
                        model_name='gemini-2.5-flash',
                        tools='google_search_retrieval'
                    )
                    res = model.generate_content(prompt)
                    st.markdown(res.text)
                    st.session_state.messages.append({"role": "assistant", "content": res.text})
                except Exception as e:
                    # Fallback standard model
                    try:
                        fallback_model = genai.GenerativeModel('gemini-2.5-flash')
                        res = fallback_model.generate_content(prompt)
                        st.markdown(res.text)
                        st.session_state.messages.append({"role": "assistant", "content": res.text})
                    except Exception as err:
                        st.error(f"Error: {err}")
