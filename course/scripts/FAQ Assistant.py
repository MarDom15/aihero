import streamlit as st
import asyncio
import ingest
import search
import logs

@st.cache_resource
def init_agent():
    repo_owner = "DataTalksClub"
    repo_name = "faq"
    index = ingest.index_data(repo_owner, repo_name, filter=lambda doc: "data-engineering" in doc["filename"])
    return search.init_agent(index, repo_owner, repo_name)

agent = init_agent()

st.set_page_config(page_title="AI FAQ Assistant", page_icon="🤖")
st.title("🤖 AI FAQ Assistant")
st.caption("Ask me anything about the DataTalksClub/faq repository")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = asyncio.run(agent.run(user_prompt=prompt))
        answer = response.output
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    logs.log_interaction_to_file(agent, response.new_messages())
