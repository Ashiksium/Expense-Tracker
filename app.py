from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# A simple in-memory list to store records (use a database for persistence)
data = []

# Helper function to check if it's weekend
def is_weekend(date):
    return date.weekday() >= 5  # 5 = Saturday, 6 = Sunday

@app.route('/')
def index():
    total_earnings = sum(entry['amount'] for entry in data if entry['type'] == 'earning')
    total_weekday_expenses = sum(entry['amount'] for entry in data if entry['type'] == 'expense' and not entry['weekend'])
    total_weekend_expenses = sum(entry['amount'] for entry in data if entry['type'] == 'expense' and entry['weekend'])
    balance = total_earnings - (total_weekday_expenses + total_weekend_expenses)
    
    return render_template('index.html', data=data, total_earnings=total_earnings, 
                           total_weekday_expenses=total_weekday_expenses,
                           total_weekend_expenses=total_weekend_expenses,
                           balance=balance)

@app.route('/add', methods=['POST'])
def add_entry():
    amount = float(request.form['amount'])
    entry_type = request.form['type']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    
    entry = {
        'amount': amount,
        'type': entry_type,
        'weekend': is_weekend(date),
        'date': date.strftime('%Y-%m-%d')
    }
    
    data.append(entry)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
