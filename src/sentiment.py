POS={'good','great','excellent','helpful','clear','accurate','useful','thanks','love','perfect','relevant','easy','amazing','correct','complete','friendly'}
NEG={'bad','poor','wrong','incorrect','confusing','unclear','useless','irrelevant','slow','inaccurate','incomplete','missing','error','failed','difficult','unhelpful','terrible','disappointed'}
def sentiment(text):
    words=[w.strip('.,!?;:()[]{}\"\'').lower() for w in (text or '').split()]; p=sum(w in POS for w in words); n=sum(w in NEG for w in words); score=(p-n)/max(len(words),1)
    return ('Positive' if score>.015 else 'Negative' if score<-.015 else 'Neutral',round(score,4))
