import tkinter as tk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to calculate yearly progress
def get_yearly_progress():
    now = datetime.now()
    year_start = datetime(now.year, 1, 1)
    year_end = datetime(now.year + 1, 1, 1)
    progress = (now - year_start).total_seconds() / (year_end - year_start).total_seconds() * 100
    return progress

# Function to calculate daily progress
def get_daily_progress():
    now = datetime.now()
    day_start = datetime(now.year, now.month, now.day)
    day_end = datetime(now.year, now.month, now.day, 23, 59, 59)
    progress = (now - day_start).total_seconds() / (day_end - day_start).total_seconds() * 100
    return progress

# Function to update the charts
def update_charts():
    yearly_progress = get_yearly_progress()
    daily_progress = get_daily_progress()

    # Update yearly progress bar
    yearly_ax.clear()
    yearly_ax.barh([0], [100], color='#ecf0f1', height=0.1, align='center', edgecolor='none')
    yearly_ax.barh([0], [yearly_progress], color='#3498db', height=0.1, align='center')
    yearly_ax.text(50, 0, f"Yearly:{yearly_progress:.3f}%", color="black", fontsize=12, fontweight="bold", ha="center", va="center")
    yearly_ax.axis('off')  # Hide all axes
    yearly_canvas.draw()

    # Update daily chart
    daily_ax.clear()
    daily_ax.pie(
        [daily_progress, 100 - daily_progress],
        colors=['#2ecc71', '#ecf0f1'],
        startangle=90,
        counterclock=False,
        wedgeprops={'width': 0.3}  # 设置宽度为0.3，形成圆环
    )

    # Add a gray circle at the center
    center_circle = Circle((0, 0), 0.7, color='#ecf0f1', zorder=1)  # 0.7为圆心半径
    daily_ax.add_artist(center_circle)

    daily_ax.text(0, 0, f"Daily\n{daily_progress:.3f}%", color="black", fontsize=14, fontweight="bold", ha="center", va="center")
    daily_canvas.draw()

    # Schedule the next update
    root.after(1000, update_charts)

# Create the main tkinter window
root = tk.Tk()
root.title("Progress Tracker")
root.overrideredirect(True)  # Remove window decorations
root.attributes('-topmost', True)  # Always on top
root.attributes('-transparentcolor', 'white')  # Set white background as transparent
root.geometry("300x250")  # Adjusted height
root.geometry(f"+{root.winfo_screenwidth() - root.winfo_reqwidth()}+0")  # 完全贴到右上角

root.configure(bg="white")  # Set window background to white for transparency

# Add drag functionality for the widget
def start_drag(event):
    root.x = event.x
    root.y = event.y

def do_drag(event):
    x = root.winfo_x() + event.x - root.x
    y = root.winfo_y() + event.y - root.y
    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", do_drag)

# Create yearly progress bar frame
yearly_frame = tk.Frame(root, bg="white")
yearly_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

yearly_fig, yearly_ax = plt.subplots(figsize=(6, 0.5))
yearly_fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margins
yearly_fig.patch.set_facecolor('white')  # Set bar chart background to white

yearly_canvas = FigureCanvasTkAgg(yearly_fig, master=yearly_frame)
yearly_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create daily chart frame
daily_frame = tk.Frame(root, bg="white")
daily_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

daily_fig, daily_ax = plt.subplots()
daily_fig.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margins
daily_fig.patch.set_facecolor('white')  # Set pie chart background to white

daily_canvas = FigureCanvasTkAgg(daily_fig, master=daily_frame)
daily_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Bind Escape key to close window
root.bind("<Escape>", lambda event: root.destroy())

# Update charts initially and start the loop
update_charts()

# Run the tkinter event loop
root.mainloop()