# God of War Workout Tracker (Flask App with Entry Management)

from flask import Flask, render_template, request, redirect, jsonify
from tracker import update_log_and_stats, get_summary_stats
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
LOG_PATH = "log.xlsx"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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

    # Load entries for display on home page (optional preview)
    if os.path.exists(LOG_PATH):
        df = pd.read_excel(LOG_PATH, engine='openpyxl')
        entries = df.to_dict(orient='records')
    else:
        entries = []

    return render_template('index.html', entries=entries)

@app.route('/entries')
def entries():
    if os.path.exists(LOG_PATH):
        df = pd.read_excel(LOG_PATH, engine='openpyxl')
        entries = df.to_dict(orient='records')
    else:
        entries = []
    return render_template('entries.html', entries=entries)

@app.route('/delete/<int:row_id>', methods=['POST'])
def delete_entry(row_id):
    if os.path.exists(LOG_PATH):
        df = pd.read_excel(LOG_PATH, engine='openpyxl')
        if 0 <= row_id < len(df):
            df = df.drop(index=row_id).reset_index(drop=True)
            df.to_excel(LOG_PATH, index=False, engine='openpyxl')
    return redirect(request.referrer or '/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard-data')
def dashboard_data():
    stats, chart = get_summary_stats(LOG_PATH)
    return jsonify({"stats": stats, "chart": chart})

if __name__ == '__main__':
    app.run(debug=True)
