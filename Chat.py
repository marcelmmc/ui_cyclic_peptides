import streamlit as st


def new_chat():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


with st.sidebar:
    st.sidebar.button(
        "New chat",
        on_click=new_chat,
        help="Clear chat history and start a new chat",
    )
    "[Learn more]()"

# Title
st.title("💬 Chat")
st.caption("LLM Hackathon for Materials & Chemistry - EPFL Hub")

# Info
st.info("🛠️ Chat is coming soon!")

# Chat elements
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if query := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking ..."):
            # TODO: Add our LLM here
            response = "Sorry, I don't have an answer for that yet."
        if response:
            st.write(response)
            # TODO: Add response image here
            # st.image()
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
