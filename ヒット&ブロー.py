import tkinter as tk
from tkinter import messagebox
import random

class HitAndBlowGame:
    def __init__(self, root):
        self.root = root
        self.root.title("ヒット&ブロー")
        self.root.geometry("800x700")
        
        # ゲームパラメータ
        self.colors = ["赤", "青", "黄", "緑", "白", "ピンク"]
        self.color_codes = {
            "赤": "#E60000",
            "青": "#0040FF",
            "黄": "#FFDD00",
            "緑": "#00DD00",
            "白": "#F0F0F0",
            "ピンク": "#FF1493"
        }
        
        # ゲーム状態
        self.length = 4  # 当てる色の数（デフォルト）
        self.answer = random.sample(self.colors, self.length)  # 正解を選択
        self.max_attempts = 10
        self.attempts = 0
        self.selected_colors = []
        self.game_over = False
        
        self.setup_ui()
    
    def setup_ui(self):
        # タイトル
        title_label = tk.Label(self.root, text="ヒット&ブロー", font=("Arial", 24, "bold"))
        title_label.pack(pady=10)
        
        # 説明
        self.info_label = tk.Label(self.root, text=f"{self.length}色を選んで判定ボタンをクリック！\n正解を当てるまで何度でも試行できます", font=("Arial", 12))
        self.info_label.pack(pady=5)
        
        # 選択色表示エリア
        selection_frame = tk.Frame(self.root, bg="lightgray", height=100)
        selection_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(selection_frame, text="選択中:", font=("Arial", 12), bg="lightgray").pack(anchor=tk.W, padx=5, pady=5)
        
        self.selection_display = tk.Frame(selection_frame)
        self.selection_display.pack(fill=tk.X, padx=5, pady=5)

        self.color_boxes = []
        for i in range(self.length):
            # Canvasで円形の色表示を作成
            box = tk.Canvas(
                self.selection_display,
                width=80,
                height=80,
                bg=self.root.cget('bg'),
                highlightthickness=0
            )
            box.pack(side=tk.LEFT, padx=8)
            
            # 円を描画（最初は灰色）
            circle = box.create_oval(5, 5, 75, 75, fill="lightgray", outline="gray", width=2)
            self.color_boxes.append((box, circle))
        
        # リセットボタン
        reset_btn = tk.Button(selection_frame, text="リセット", command=self.reset_selection, width=10)
        reset_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        # 設定：当てる数と新しいゲーム開始
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=5)

        tk.Label(settings_frame, text="当てる数:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.length_spinbox = tk.Spinbox(settings_frame, from_=2, to=len(self.colors), width=4)
        self.length_spinbox.delete(0, tk.END)
        self.length_spinbox.insert(0, str(self.length))
        self.length_spinbox.pack(side=tk.LEFT)

        new_game_btn = tk.Button(settings_frame, text="新しいゲーム", command=self.new_game, width=12)
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # 色選択ボタン
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        button_row1 = tk.Frame(button_frame)
        button_row1.pack()
        
        button_row2 = tk.Frame(button_frame)
        button_row2.pack()
        
        self.color_buttons = []
        for i, color in enumerate(self.colors):
            parent = button_row1 if i < 3 else button_row2
            
            # Canvasで円形のボタンを作成
            canvas = tk.Canvas(
                parent,
                width=100,
                height=100,
                bg=button_frame.cget('bg'),
                highlightthickness=0
            )
            canvas.pack(side=tk.LEFT, padx=8, pady=5)
            
            # 円を描画
            text_color = "black" if color in ["黄", "ピンク", "白"] else "white"
            canvas.create_oval(
                5, 5, 95, 95,
                fill=self.color_codes[color],
                outline="black",
                width=2
            )
            
            # テキストを描画
            canvas.create_text(
                50, 50,
                text=color,
                font=("Arial", 12, "bold"),
                fill=text_color
            )
            
            # クリックイベント
            canvas.bind("<Button-1>", lambda e, c=color: self.select_color(c))
            self.color_buttons.append(canvas)
        
        # 判定ボタンと情報表示
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        judge_btn = tk.Button(
            control_frame,
            text="判定する",
            bg="lightblue",
            width=15,
            height=2,
            font=("Arial", 12),
            command=self.judge
        )
        judge_btn.pack(side=tk.LEFT, padx=10)
        
        # 試行回数表示
        self.attempt_label = tk.Label(control_frame, text=f"試行回数: {self.attempts}/{self.max_attempts}", font=("Arial", 12))
        self.attempt_label.pack(side=tk.LEFT, padx=10)
        
        # 結果表示エリア
        result_frame = tk.Frame(self.root, bg="lightyellow", height=150)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(result_frame, text="結果:", font=("Arial", 12, "bold"), bg="lightyellow").pack(anchor=tk.W, padx=5, pady=5)
        
        self.result_text = tk.Text(result_frame, height=10, width=70, font=("Arial", 12))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.config(state=tk.DISABLED)
    
    def select_color(self, color):
        if self.game_over:
            messagebox.showinfo("ゲーム終了", "ゲームが終了しています。")
            return
        
        if len(self.selected_colors) < self.length:
            self.selected_colors.append(color)
            self.update_display()
        else:
            messagebox.showwarning("選択済み", f"既に{self.length}色選択しています。判定するか、リセットしてください。")
    
    def reset_selection(self):
        self.selected_colors = []
        self.update_display()
    
    def update_display(self):
        for i, (box, circle) in enumerate(self.color_boxes):
            if i < len(self.selected_colors):
                color = self.selected_colors[i]
                box.itemconfig(circle, fill=self.color_codes[color])
            else:
                box.itemconfig(circle, fill="lightgray")
    
    def judge(self):
        if self.game_over:
            messagebox.showinfo("ゲーム終了", "ゲームが終了しています。")
            return
        
        if len(self.selected_colors) < self.length:
            messagebox.showwarning("未選択", f"{self.length}色すべて選択してください。")
            return
        
        self.attempts += 1
        self.attempt_label.config(text=f"試行回数: {self.attempts}/{self.max_attempts}")
        
        # ヒット数とブロー数を計算
        hits = sum(1 for i in range(self.length) if self.selected_colors[i] == self.answer[i])
        
        # ブローを計算：色は正しいが位置が違う
        blows = 0
        for i, color in enumerate(self.selected_colors):
            if color != self.answer[i] and color in self.answer:
                blows += 1
        
        # 結果を表示
        self.display_result(hits, blows)
        
        # 正解判定
        if hits == self.length:
            messagebox.showinfo("正解！", f"素晴らしい！{self.attempts}回で正解しました！")
            self.game_over = True
            self.show_answer()
        elif self.attempts >= self.max_attempts:
            messagebox.showinfo("ゲームオーバー", f"{self.max_attempts}回の試行回数に達しました。\nゲームオーバーです。")
            self.game_over = True
            self.show_answer()
        
        self.selected_colors = []
        self.update_display()
    
    def display_result(self, hits, blows):
        self.result_text.config(state=tk.NORMAL)
        
        # ヒット数と判定結果を表示
        result_symbols = "●" * hits + "○" * blows
        result_line = f"試行{self.attempts}: {', '.join(self.selected_colors)}\n"
        result_line += f"         結果: {result_symbols} (ヒット: {hits}, ブロー: {blows})\n"
        
        self.result_text.insert(tk.END, result_line)
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def show_answer(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, f"\n正解: {', '.join(self.answer)}\n")
        self.result_text.config(state=tk.DISABLED)

    def new_game(self):
        try:
            new_length = int(self.length_spinbox.get())
        except Exception:
            messagebox.showwarning("入力エラー", "当てる数は数値で指定してください。")
            return

        if new_length < 2 or new_length > len(self.colors):
            messagebox.showwarning("入力エラー", f"当てる数は2〜{len(self.colors)}の範囲で指定してください。")
            return

        self.length = new_length
        self.answer = random.sample(self.colors, self.length)
        self.attempts = 0
        self.selected_colors = []
        self.game_over = False

        # 更新：説明文と試行表示
        self.info_label.config(text=f"{self.length}色を選んで判定ボタンをクリック！\n正解を当てるまで何度でも試行できます")
        self.attempt_label.config(text=f"試行回数: {self.attempts}/{self.max_attempts}")

        # 選択表示の再作成
        for child in self.selection_display.winfo_children():
            child.destroy()
        self.color_boxes = []
        for i in range(self.length):
            box = tk.Canvas(
                self.selection_display,
                width=80,
                height=80,
                bg=self.root.cget('bg'),
                highlightthickness=0
            )
            box.pack(side=tk.LEFT, padx=8)
            circle = box.create_oval(5, 5, 75, 75, fill="lightgray", outline="gray", width=2)
            self.color_boxes.append((box, circle))

        # 結果欄をクリア
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = HitAndBlowGame(root)
    root.mainloop()
