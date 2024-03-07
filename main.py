import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta

class ThirdTimeApp:
    def __init__(self, root):
        self.root = root
        self.mode = "initial"  # 'initial', 'working', 'breaking' のいずれか
        self.start_time = time.time()
        self.break_time_accumulated = 0
        self.break_end_expected_time = None
        self.remaining_break_time = 0
        self.break_time_accumulated_last = 0

        self.root.title("Third Time Tracker")

        #-- 画面構成
        self.mode_label = ttk.Label(self.root, text="Welcome! Press 'Start Working' to begin.", font=("Arial", 16))
        self.mode_label.pack(pady=10)

        self.timer_label = ttk.Label(self.root, text="00:00:00", font=("Arial", 24))
        self.timer_label.pack(pady=10)

        self.break_time_label = ttk.Label(self.root, text="Break Time: --:--:--", font=("Arial", 14))
        self.break_time_label.pack(pady=5)

        # 開始ボタン
        self.start_button = ttk.Button(self.root, text="Start Working", command=self.start_working)
        self.start_button.pack(pady=20)

        # 切り替えボタン
        self.switch_button = ttk.Button(self.root, text="Switch Mode", command=self.switch_mode)
        self.switch_button.pack(pady=20)
        self.switch_button.state(['disabled'])  # 初期状態ではスイッチボタンを無効化

    def update_timer(self):
        if self.mode == "working":
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))
            # 作業中は休憩時間を蓄積
            self.break_time_accumulated = elapsed_time / 3 + self.break_time_accumulated_last
            self.break_time_label.config(text=f"Accumulated Break Time: {timedelta(seconds=int(self.break_time_accumulated))}")

        elif self.mode == "breaking":
            self.remaining_break_time = (self.break_end_expected_time - datetime.now()).total_seconds()
            if self.remaining_break_time<=0:
                self.break_time_label.config(text="Break time is over.")
            else:
                
                self.timer_label.config(text=time.strftime('%H:%M:%S', time.gmtime(self.remaining_break_time)))
        self.root.after(1000, self.update_timer)

    def start_working(self):
        if self.mode != "working":
            self.mode = "working"
            self.mode_label.config(text="Mode: Working")
            self.start_time = time.time()
            self.switch_button.state(['!disabled'])  # 作業を開始したらスイッチボタンを有効化
            self.update_timer()

    def switch_mode(self):
        if self.mode == "working":
            self.mode = "breaking"
            self.mode_label.config(text="Mode: Breaking")
            self.break_end_expected_time = datetime.now() + timedelta(seconds=self.break_time_accumulated)
            self.break_time_label.config(text="On a break.")
            self.update_timer()

        elif self.mode == "breaking":
            self.mode = "working"
            self.mode_label.config(text="Mode: Working")
            self.start_time = time.time()  # 作業時間のカウントアップを再開
            self.break_time_accumulated = 0  # 休憩時間をリセット
            self.break_time_accumulated_last = self.remaining_break_time
            self.update_timer()

if __name__ == "__main__":
    root = tk.Tk()
    app = ThirdTimeApp(root)
    root.mainloop()
