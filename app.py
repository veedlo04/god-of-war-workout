# God of War Workout Tracker (Flask App with JSON API and Dashboard Route)

from flask import Flask, render_template, request, redirect, jsonify
from tracker import update_log_and_stats, get_summary_stats
from datetime import datetime

app = Flask(__name__)
LOG_PATH = "log.xlsx"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect sets and reps separately and build battle plan
        sets = request.form['sets']
        reps = request.form['reps']
        entry = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Workout Type": request.form['workout_type'],
            "Exercise": request.form['exercise'],
            "Battle Plan": f"{sets}x{reps}",
            "Weight (kg)": request.form['weight']
        }
        update_log_and_stats(entry, LOG_PATH)
        return redirect('/')

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard-data')
def dashboard_data():
    stats, chart = get_summary_stats(LOG_PATH)
    return jsonify({"stats": stats, "chart": chart})

if __name__ == '__main__':
    app.run(debug=True)
