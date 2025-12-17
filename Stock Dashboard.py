import yfinance as yf
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def fetch_stock_data(symbol):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=3 * 365)
    data = yf.download(symbol, start=start_date, end=end_date, progress=False)
    if data.empty:
        return None
    return data

def get_live_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    if data.empty:
        return None
    return round(data['Close'][0], 2)

def on_enter(e):
    e.widget['background'] = "#2fa4ff"

def on_leave(e):
    e.widget['background'] = "#1f6aa5"

def show_graph():
    symbol = symbol_entry.get().upper().strip()
    if symbol == "":
        messagebox.showerror("Error", "Enter a stock symbol")
        return

    status_label.config(text="Fetching data...")
    root.update_idletasks()

    data = fetch_stock_data(symbol)
    if data is None:
        messagebox.showerror("Error", "Invalid symbol or no data")
        status_label.config(text="")
        return

    price = get_live_price(symbol)
    price_label.config(text=f"Current Price: {price if price else 'N/A'}")

    for w in graph_frame.winfo_children():
        w.destroy()

    fig1 = plt.Figure(figsize=(8.5, 4.5), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.plot(data.index, data['Close'], linewidth=1.2)
    ax1.set_title(f"{symbol} Price Trend (3 Years)")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Price")
    ax1.grid(alpha=0.3)
    fig1.tight_layout(pad=3)

    canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(pady=(10, 25))

    fig2 = plt.Figure(figsize=(8.5, 3.5), dpi=100)
    ax2 = fig2.add_subplot(111)
    ax2.bar(data.index, data['Volume'])
    ax2.set_title(f"{symbol} Trading Volume")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Volume")
    ax2.grid(alpha=0.3)
    fig2.tight_layout(pad=3)

    canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack()

    status_label.config(
        text=f"Data range: {data.index[0].date()} to {data.index[-1].date()}"
    )

root = tk.Tk()
root.title("Stock Market Dashboard")
root.geometry("1100x750")
root.configure(bg="#121212")

sidebar = tk.Frame(root, width=250, bg="#1e1e1e")
sidebar.pack(side=tk.LEFT, fill=tk.Y)

main_area = tk.Frame(root, bg="#121212")
main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Label(
    sidebar,
    text="📈 STOCK DASHBOARD",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
).pack(pady=30)

tk.Label(
    sidebar,
    text="Stock Symbol",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white"
).pack(pady=(20, 5))

symbol_entry = tk.Entry(sidebar, font=("Arial", 12), width=15)
symbol_entry.pack(pady=5)

fetch_btn = tk.Button(
    sidebar,
    text="Fetch / Refresh",
    font=("Arial", 11, "bold"),
    bg="#1f6aa5",
    fg="white",
    bd=0,
    command=show_graph
)
fetch_btn.pack(pady=15)

fetch_btn.bind("<Enter>", on_enter)
fetch_btn.bind("<Leave>", on_leave)

price_label = tk.Label(
    sidebar,
    text="Current Price: -",
    font=("Arial", 12),
    bg="#1e1e1e",
    fg="white"
)
price_label.pack(pady=10)

status_label = tk.Label(
    sidebar,
    text="",
    font=("Arial", 10),
    bg="#1e1e1e",
    fg="#4caf50",
    wraplength=220
)
status_label.pack(pady=20)

graph_frame = tk.Frame(main_area, bg="#121212")
graph_frame.pack(pady=20)

root.mainloop()
