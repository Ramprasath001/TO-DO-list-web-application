from flask import Flask, request, redirect, render_template
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
FILE_NAME = 'todo_list.xlsx'

def load_tasks():
    if os.path.exists(FILE_NAME):
        df = pd.read_excel(FILE_NAME)
    else:
        df = pd.DataFrame(columns=['Task', 'Date', 'Time'])
    return df

def save_tasks(df):
    df.to_excel(FILE_NAME, index=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            now = datetime.now()
            date_str = now.strftime('%Y-%m-%d')
            time_str = now.strftime('%H:%M:%S')

            df = load_tasks()
            new_task = {'Task': task, 'Date': date_str, 'Time': time_str}
            df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
            save_tasks(df)
        return redirect('/')

    df = load_tasks()
    tasks = df.to_dict(orient='records')
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
