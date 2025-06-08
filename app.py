#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template_string, request, redirect, url_for
import os
import random
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

FILENAME = 'vocab.txt'

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_vocab():
    vocab = {}
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',', 1)
                if len(parts) == 2:
                    eng, ch = parts
                    vocab[eng] = ch
    return vocab

def save_vocab(vocab):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        for eng, ch in vocab.items():
            f.write(f"{eng},{ch}\n")

vocab = load_vocab()

HTML = '''
<!doctype html>
<title>單字小工具</title>
<h1>單字小工具</h1>

{% if current_word %}
<p><b>請翻譯英文單字：</b> {{ current_word }}</p>

<form method="post" action="/check">
    <input type="hidden" name="eng" value="{{ current_word }}">
    <input type="text" name="ch_input" placeholder="輸入中文">
    <button type="submit">檢查</button>
</form>

<form method="post" action="/delete">
    <input type="hidden" name="eng" value="{{ current_word }}">
    <button type="submit">刪除</button>
</form>

<form method="get" action="/">
    <button type="submit">換一個！</button>
</form>

{% else %}
<p>無單字可顯示</p>
{% endif %}

<hr>
<h2>新增單字</h2>
<form method="post" action="/save">
    <input type="text" name="eng" placeholder="輸入英文" required>
    <input type="text" name="ch" placeholder="輸入中文" required>
    <button type="submit">儲存</button>
</form>

{% if message %}
<p><b>{{ message }}</b></p>
{% endif %}
'''

current_word = None

@app.route('/', methods=['GET'])
def index():
    global vocab, current_word
    if not vocab:
        current_word = None
    else:
        current_word = random.choice(list(vocab.keys()))
    return render_template_string(HTML, current_word=current_word, message=None)

@app.route('/save', methods=['POST'])
def save():
    global vocab
    eng = request.form.get('eng', '').strip()
    ch = request.form.get('ch', '').strip()
    if eng and ch:
        if eng in vocab:
            # 用 session 或 flash 顯示訊息會更好，但簡單起見這裡用 query string 傳訊息
            return redirect(url_for('index', message=f"單字 {eng} 已存在"))
        else:
            vocab[eng] = ch
            save_vocab(vocab)
            return redirect(url_for('index', message=f"已儲存：{eng} -> {ch}"))
    else:
        return redirect(url_for('index', message="請輸入完整的英文與中文"))
        
@app.route('/check', methods=['POST'])
def check():
    global vocab, current_word
    eng = request.form.get('eng')
    user_ch = request.form.get('ch_input', '').strip()
    if not eng or eng not in vocab:
        return redirect(url_for('index'))
    correct_ch = vocab[eng]
    similarity = util.cos_sim(model.encode(user_ch), model.encode(correct_ch)).item()

    if user_ch == correct_ch:
        msg = "🎉 恭喜答對！"
        vocab.pop(eng)
        save_vocab(vocab)
        current_word = random.choice(list(vocab.keys())) if vocab else None
    elif similarity > 0.9:
        msg = f"你的答案是：{user_ch}<b\n資料庫中的答案是：{correct_ch}\n相近率為：{similarity*100:.2f}%，視為正確並刪除。"
        vocab.pop(eng)
        save_vocab(vocab)
        current_word = random.choice(list(vocab.keys())) if vocab else None
    else:
        msg = f"答錯囉！正確答案是：{correct_ch}，相似度：{similarity*100:.2f}%"

    return render_template_string(HTML, current_word=current_word, message=msg)

@app.route('/delete', methods=['POST'])
def delete():
    global vocab, current_word
    eng = request.form.get('eng')
    if eng in vocab:
        vocab.pop(eng)
        save_vocab(vocab)
        current_word = random.choice(list(vocab.keys())) if vocab else None
        msg = f"已刪除：{eng}"
    else:
        msg = "單字不存在"
    return render_template_string(HTML, current_word=current_word, message=msg)

if __name__ == '__main__':
    app.run()


# In[5]:





# In[ ]:




