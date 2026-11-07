import sqlite3, csv, io
from pathlib import Path
from datetime import datetime
DB=Path(__file__).resolve().parent.parent/'data'/'insightai.db'
def conn():
    DB.parent.mkdir(exist_ok=True); c=sqlite3.connect(DB,check_same_thread=False); c.row_factory=sqlite3.Row; return c
def init_db():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            mode TEXT,
            created_at TEXT
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id INTEGER,
            rating INTEGER,
            helpful TEXT,
            category TEXT,
            comment TEXT,
            sentiment TEXT,
            score REAL,
            created_at TEXT,
            FOREIGN KEY (interaction_id)
                REFERENCES interactions(id)
        );
        """)
def stamp(): return datetime.now().astimezone().strftime('%Y-%m-%d %H:%M')
def save_interaction(q,a,m):
    with conn() as c:
        cur=c.execute('INSERT INTO interactions(question,answer,mode,created_at) VALUES(?,?,?,?)',(q,a,m,stamp())); return cur.lastrowid
def save_feedback(i,r,h,cat,comment,label,score):
    with conn() as c: c.execute('INSERT OR REPLACE INTO feedback(interaction_id,rating,helpful,category,comment,sentiment,score,created_at) VALUES(?,?,?,?,?,?,?,?)',(i,r,h,cat,comment,label,score,stamp()))
def stats():
    with conn() as c:
        n=c.execute('SELECT COUNT(*) FROM interactions').fetchone()[0]; f=c.execute('SELECT COUNT(*) FROM feedback').fetchone()[0]; avg=c.execute('SELECT AVG(rating) FROM feedback').fetchone()[0] or 0
        counts={x:c.execute('SELECT COUNT(*) FROM feedback WHERE sentiment=?',(x,)).fetchone()[0] for x in ['Positive','Neutral','Negative']}; low=c.execute('SELECT COUNT(*) FROM feedback WHERE rating<=2').fetchone()[0]
    return {'interactions':n,'feedback':f,'avg':avg,'counts':counts,'low':low}
def feedback_rows():
    with conn() as c: return [dict(x) for x in c.execute('SELECT f.*,i.question,i.answer,i.mode FROM feedback f JOIN interactions i ON i.id=f.interaction_id ORDER BY f.id DESC')]
def recent_rows():
    with conn() as c: return [dict(x) for x in c.execute('SELECT i.*,f.rating,f.helpful,f.category,f.comment,f.sentiment FROM interactions i LEFT JOIN feedback f ON f.interaction_id=i.id ORDER BY i.id DESC LIMIT 30')]
def csv_export():
    out=io.StringIO(); rows=feedback_rows(); fields=['id','interaction_id','created_at','rating','helpful','category','comment','sentiment','score','question','answer','mode']; w=csv.DictWriter(out,fieldnames=fields,extrasaction='ignore'); w.writeheader(); w.writerows(rows); return out.getvalue().encode()
