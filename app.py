import streamlit as st
import os
from agent import agent

st.set_page_config(page_title="AI Math Tutor", page_icon="🧮")
st.title("Math First-Principles Tutor")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If the historic message contains an image path snapshot, reload it
        if "image" in message:
            st.image(message["image"])

if prompt := st.chat_input("Ask a math question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Clean up any leftover plots from older sessions before running
        if os.path.exists("plot.png"):
            os.remove("plot.png")
            
        full_prompt = f"""
        Please solve this math question. 
        You must verify your algebraic logic using the 'math_verifier' tool, 
        and then output your working using the structured final_answer tool.

        CRITICAL OUTPUT STYLE FORMATTING RULES:
        1. For 'steps_working': Format it as a clear vertical bulleted or numbered list. Every step must be on a new line.
        2. Keep variable numbers clean (e.g., use '7' instead of float notation '7.0' if the value is an integer).
        3. For 'absolute_final_answer': Express it as a complete terminal assignment (e.g., 'y = 7').
        4. GRAPHING EXTRA RULE: If the user request implies visualization, graphing, or plotting, write matplotlib python code 
           to generate the plot, apply a clean professional style layout, and ALWAYS save the figure exactly to 'plot.png' 
           using `plt.savefig('plot.png')`. Do not use `plt.show()`.

        Question: {prompt}
        """
        
        response = agent.run(full_prompt)
        response_placeholder.markdown(response)
        
        # Check if the agent saved a visual plot file to disk
        message_data = {"role": "assistant", "content": response}
        if os.path.exists("plot.png"):
            st.image("plot.png")
            # Save the image path into session history so it persists through scroll refreshes
            # We rename it uniquely per message index to prevent caching issues
            saved_img_name = f"plot_step_{len(st.session_state.messages)}.png"
            os.rename("plot.png", saved_img_name)
            message_data["image"] = saved_img_name

    st.session_state.messages.append(message_data)