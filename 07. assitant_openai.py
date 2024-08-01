from openai import OpenAI
import streamlit as st
import time

assistant_id='asst_S9XS5t26fdA034j3Jzeg4BO9'
# thread_id='thread_hWKae0sRWIsRgndFb14hla5t'


with st.sidebar:
    st.link_button('더 좋은 콘텐츠 후원하기', "http://toss.me/kimfl")
    
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    client = OpenAI(api_key=openai_api_key)
    
    thread_id = st.text_input("Thread ID", value='thread_hWKae0sRWIsRgndFb14hla5t')
    thread_make_btn = st.button("Create a new thread")
    if thread_make_btn:
        
        thread = client.beta.threads.create()
        thread_id=thread.id
        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("새로운 스레드가 생성되었습니다")
    
    
    
st.title("My Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "선생님에게 무엇이든 물어봐?"}]

print(f"session_state()\n {st.session_state}")
print()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

messages = []
prompt = st.chat_input()
if prompt:
    # client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    respones = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=prompt)
    
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
    
    run_id = run.id
    
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status == "completed":
            break
        else:
            time.sleep(1)
    
    # respones = client.chat.completions.create(model="gpt-3.5-turbo",\
    # messages=st.session_state.messages)
    
    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_content = thread_messages.data[0].content[0].text.value
    
    # st.session_state.assistant_content = respones.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_content})
    st.chat_message("assistant").write(assistant_content)
    
    print(st.session_state.messages)
