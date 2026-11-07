import streamlit as st
from src.database import stats,recent_rows
def bar(label,value,total,color):
    pct=0 if not total else max(0,min(100,value/total*100))
    st.markdown(f'<div style="margin:10px 0"><div style="display:flex;justify-content:space-between"><span>{label}</span><b>{value}</b></div><div style="height:10px;background:#e5e7eb;border-radius:20px"><div style="height:10px;width:{pct}%;background:{color};border-radius:20px"></div></div></div>',unsafe_allow_html=True)
def dashboard():
    s=stats(); a=st.columns(4); a[0].metric('AI interactions',s['interactions']); a[1].metric('Feedback received',s['feedback']); a[2].metric('Average rating',f"{s['avg']:.2f}/5" if s['feedback'] else '—'); a[3].metric('Low ratings (1–2)',s['low'])
    st.subheader('Feedback sentiment'); x,y=st.columns(2); total=max(s['feedback'],1)
    with x:
        bar('Positive',s['counts']['Positive'],total,'#16a34a'); bar('Neutral',s['counts']['Neutral'],total,'#64748b'); bar('Negative',s['counts']['Negative'],total,'#dc2626')
    with y:
        st.markdown('**How to read the dashboard**'); st.write('Average rating summarizes user scores from 1 to 5.'); st.write('Sentiment is estimated from optional comments using a small keyword heuristic.'); st.write('Low ratings flag responses for human review.')
    st.divider(); st.subheader('Latest activity')
    for r in recent_rows()[:8]:
        with st.container(border=True):
            st.markdown(f"**{r['created_at']} · {r['mode']}**"); st.write('Question: '+r['question'][:180]); st.caption(f"Rating: {r['rating']}/5 · {r['sentiment']}" if r['rating'] is not None else 'Feedback pending')
