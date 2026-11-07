import streamlit as st
from src.database import init_db, save_interaction, save_feedback, stats, feedback_rows, recent_rows, csv_export
from src.ai import answer
from src.sentiment import sentiment
from src.analytics import dashboard
import google.generativeai as genai

import os

GOOGLE_API_KEY = st.secrets.get(
    "GOOGLE_API_KEY",
    os.getenv("GOOGLE_API_KEY", "")
)

if not GOOGLE_API_KEY:
    st.error("Gemini API key is missing. Check Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

model=genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title='InsightAI', page_icon='🧠', layout='wide')
init_db()
st.markdown('''<style>.block-container{padding-top:1.5rem;max-width:1400px}.hero{background:linear-gradient(115deg,#172554,#4338ca 65%,#7c3aed);padding:26px;border-radius:18px;color:white;margin-bottom:20px}.hero h1{color:white;margin:0}.hero p{color:#e0e7ff;margin:6px 0 0} [data-testid="stSidebar"]{background:#111827}[data-testid="stSidebar"] *{color:#f3f4f6}</style>''',unsafe_allow_html=True)
with st.sidebar:
    st.markdown('## 🧠 InsightAI'); st.caption('AI response quality & feedback intelligence')
    page=st.radio('WORKSPACE',['Overview','AI Assistant','Feedback Explorer','Response Evaluation'],label_visibility='collapsed')
    st.divider(); st.caption('Educational prototype. Do not enter confidential information.')
st.markdown('<div class="hero"><h1>🧠 InsightAI</h1><p>Turn AI conversations into measurable insights.</p></div>',unsafe_allow_html=True)
if page=='Overview':
    st.title('Feedback Intelligence Overview'); dashboard()
elif page=='AI Assistant':
    st.title('AI Assistant'); st.write('Ask a question, review the response, and rate its quality.')
    st.warning('Do not enter passwords, OTPs, API keys, financial details or sensitive personal information.')
    if 'messages' not in st.session_state: st.session_state.messages=[]
    for m in st.session_state.messages:
        with st.chat_message(m['role']):
            st.markdown(m['content'])
            if m.get('mode'): st.caption(m['mode'])
    prompt=st.chat_input('Ask InsightAI a question...')
    if prompt:
        with st.chat_message('user'): st.markdown(prompt)
        with st.spinner('Generating response...'):
            reply,mode=answer(prompt); iid=save_interaction(prompt,reply,mode)
        st.session_state.messages += [{'role':'user','content':prompt},{'role':'assistant','content':reply,'mode':mode}]
        st.session_state.last_id=iid; st.rerun()
    if st.session_state.get('last_id'):
        st.divider(); st.subheader('Rate the latest response')
        with st.form('feedback',clear_on_submit=True):
            rating=st.select_slider('How helpful was this answer?',options=[1,2,3,4,5],value=4)
            helpful=st.radio('Did it address your question?',['Yes','Partly','No'],horizontal=True)
            category=st.selectbox('Main feedback category',['Accuracy','Relevance','Clarity','Completeness','Tone','Other'])
            comment=st.text_area('What could be improved? (optional)')
            if st.form_submit_button('Submit feedback',type='primary'):
                label,score=sentiment(comment); save_feedback(st.session_state.last_id,rating,helpful,category,comment,label,score)
                st.session_state.last_id=None; st.success('Feedback saved. Thank you!'); st.rerun()
elif page=='Feedback Explorer':
    st.title('Feedback Explorer'); rows=feedback_rows()
    if not rows: st.info('No feedback yet. Use AI Assistant and rate a response.')
    else:
        st.write(f'{len(rows)} feedback submissions')
        for r in rows:
            with st.container(border=True):
                a,b,c=st.columns([3,1,1]); a.markdown(f"**{r['created_at']} · {r['category']}**"); b.write(f"⭐ {r['rating']}/5"); c.write(r['sentiment'])
                st.markdown('**Question:** '+r['question']); st.markdown('**AI response:** '+r['answer'][:650]);
                if r['comment']: st.write('**Comment:** '+r['comment'])
        st.download_button('Download feedback CSV',csv_export(),'insightai_feedback.csv','text/csv')
elif page=='Response Evaluation':
    st.title('Response Evaluation'); rows=recent_rows()
    if not rows: st.info('No conversations recorded yet.')
    for r in rows:
        with st.expander(f"#{r['id']} · {r['created_at']} · {r['mode']}"):
            st.markdown('**Question**'); st.write(r['question']); st.markdown('**Response**'); st.write(r['answer'])
            st.write(f"Rating: {r['rating'] if r['rating'] is not None else 'Pending'} / 5 · {r['sentiment'] or 'Not analysed'}")
            if r['comment']: st.write('Comment: '+r['comment'])
