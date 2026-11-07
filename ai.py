import os,json,urllib.request,urllib.parse,urllib.error
def demo(q):
    q=q.lower()
    if 'feedback' in q or 'rating' in q: return 'A useful feedback process collects a response rating, whether the answer solved the user’s problem, and an optional comment. InsightAI stores this feedback and summarizes patterns for improvement.'
    if 'sentiment' in q: return 'Sentiment analysis estimates the emotional tone of text. This demo uses a small word-list heuristic to label feedback positive, neutral or negative. It can miss sarcasm and context.'
    return 'Thanks for your question! This is InsightAI demo mode. Configure a Gemini API key to enable live AI-generated answers. You can still test response ratings, feedback collection, sentiment labels and analytics.'
def answer(q):
    key=os.getenv('GOOGLE_API_KEY','').strip()
    if not key: return demo(q),'Demo mode · no Gemini API key'
    model=os.getenv('GEMINI_MODEL','gemini-2.0-flash'); url=f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(key)}'
    payload={'system_instruction':{'parts':[{'text':'You are a helpful, careful AI assistant. Explain uncertainty. Never ask for passwords, OTPs, API keys or sensitive personal information.'}]},'contents':[{'role':'user','parts':[{'text':q}]}],'generationConfig':{'temperature':0.4,'maxOutputTokens':900}}
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=35) as res: data=json.loads(res.read().decode())
        return data['candidates'][0]['content']['parts'][0]['text'],f'Live response · {model}'
    except urllib.error.HTTPError as e: return f'Gemini API returned HTTP {e.code}. Check the API key and model setting.','Gemini API error'
    except Exception as e: return f'Gemini connection error: {type(e).__name__}.','Connection error'
