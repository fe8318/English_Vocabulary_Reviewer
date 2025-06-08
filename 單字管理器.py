#!/usr/bin/env python
# coding: utf-8

# In[30]:


# pip install sentence-transformers


# In[32]:


from sentence_transformers import SentenceTransformer, util


# In[34]:


# pip install ipywidgets


# In[36]:


# model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


# In[63]:


"""

vec1 = model.encode("蘋果")
vec2 = model.encode("林檎")

similarity = util.cos_sim(vec1, vec2)
print(f"相似度：{similarity.item():.4f}")
"""


# In[64]:


import tkinter as tk
from tkinter import messagebox
import random
import os

FILENAME = 'vocab.txt'

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

class VocabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("單字小工具")

        self.vocab = load_vocab()
        self.current_word = None

        self.word_label = tk.Label(root, text="", font=('Arial', 20))
        self.word_label.pack(pady=10)

        self.input_eng = tk.Entry(root, font=('Arial', 14))
        self.input_eng.pack(pady=5)
        self.input_eng.insert(0, "輸入英文")

        self.input_ch = tk.Entry(root, font=('Arial', 14))
        self.input_ch.pack(pady=5)
        self.input_ch.insert(0, "輸入中文")

        # 按鈕區塊
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.save_button = tk.Button(btn_frame, text="儲存", command=self.save_word)
        self.save_button.grid(row=0, column=0, padx=5)

        self.check_button = tk.Button(btn_frame, text="檢查", command=self.check_word)
        self.check_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(btn_frame, text="刪除", command=self.delete_word)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.change_button = tk.Button(btn_frame, text="換一個！", command=self.change_word)
        self.change_button.grid(row=0, column=3, padx=5)

        self.refresh_word()

    def refresh_word(self):
        if self.vocab:
            self.current_word = random.choice(list(self.vocab.keys()))
            self.word_label.config(text=self.current_word)
        else:
            self.word_label.config(text="無單字可顯示")
            self.current_word = None

    def change_word(self):
        if not self.vocab or len(self.vocab) <= 1:
            return
        candidates = list(self.vocab.keys())
        candidates.remove(self.current_word)
        self.current_word = random.choice(candidates)
        self.word_label.config(text=self.current_word)

    def save_word(self):
        eng = self.input_eng.get().strip()
        ch = self.input_ch.get().strip()
        if eng and ch:
            if eng not in self.vocab:
                self.vocab[eng] = ch
                save_vocab(self.vocab)
                messagebox.showinfo("成功", f"已儲存：{eng} -> {ch}")
            else:
                messagebox.showwarning("重複", f"單字 {eng} 已存在")
        else:
            messagebox.showwarning("錯誤", "請輸入完整的英文與中文")

    def check_word(self):
        if not self.current_word:
            return
        user_ch = self.input_ch.get().strip()
        correct_ch = self.vocab.get(self.current_word, "")
        correct_rate = util.cos_sim(model.encode(user_ch), model.encode(correct_ch)).item()
        if user_ch == correct_ch:
            messagebox.showinfo("正確", "🎉 恭喜答對！")
            del self.vocab[self.current_word]
            save_vocab(self.vocab)
            self.refresh_word()
        elif correct_rate > 0.900:
            messagebox.showinfo("正確",  "你的答案是："+user_ch+ "\n資料庫中的答案是："+correct_ch+ "\n相近率為："+str(100*correct_rate)+"%")
            del self.vocab[self.current_word]
            save_vocab(self.vocab)
            self.refresh_word()
        else:
            self.show_wrong_answer_dialog(correct_ch, correct_rate)

    def show_wrong_answer_dialog(self, correct_ch, correct_rate):
        def confirm_wrong():
            del self.vocab[self.current_word]
            save_vocab(self.vocab)
            wrong_win.destroy()
            self.refresh_word()

        def just_close():
            wrong_win.destroy()

        wrong_win = tk.Toplevel(self.root)
        wrong_win.title("答錯囉")
        tk.Label(wrong_win, text=f"正確答案是：{correct_ch}", font=('Arial', 14)).pack(pady=10)
        tk.Label(wrong_win, text=f"相似度為：{correct_rate*100:.2f}%", font=('Arial', 14)).pack(pady=10)

        tk.Button(wrong_win, text="我的答案是對的（刪除）", command=confirm_wrong).pack(pady=5)
        tk.Button(wrong_win, text="我知道了", command=just_close).pack(pady=5)

    def delete_word(self):
        if self.current_word and self.current_word in self.vocab:
            del self.vocab[self.current_word]
            save_vocab(self.vocab)
            messagebox.showinfo("刪除", f"已刪除：{self.current_word}")
            self.refresh_word()


# In[65]:


if __name__ == "__main__":
    root = tk.Tk()
    app = VocabApp(root)
    root.mainloop()


# In[ ]:





# In[ ]:




