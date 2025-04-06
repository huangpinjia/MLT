import matplotlib.pyplot as plt
from database import get_score_history

def show_score_chart():
    history = get_score_history()
    if not history:
        print("No scores yet.")
        return

    timestamps = [row[4] for row in history][::-1]
    scores = [row[2] for row in history][::-1]
    totals = [row[3] for row in history][::-1]

    percentages = [s / t * 100 for s, t in zip(scores, totals)]

    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, percentages, marker='o', linestyle='-', color='blue')
    plt.xticks(rotation=45)
    plt.ylabel("Score (%)")
    plt.title("Vocabia Score History")
    plt.tight_layout()
    plt.show()
