from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "voter_evm_secret"

# Files Path
DATA_DIR = 'data'
USERS_CSV = os.path.join(DATA_DIR, 'users.csv')
CANDIDATES_CSV = os.path.join(DATA_DIR, 'candidates.csv')
STATUS_FILE = os.path.join(DATA_DIR, 'status.txt')

# Setup Folders and Files on start
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(CANDIDATES_CSV):
    pd.DataFrame(columns=['id', 'name', 'symbol', 'votes']).to_csv(CANDIDATES_CSV, index=False)

if not os.path.exists(USERS_CSV):
    pd.DataFrame([["user1", "123", "No"]], columns=['username', 'password', 'has_voted']).to_csv(USERS_CSV, index=False)

def get_status():
    if not os.path.exists(STATUS_FILE): return "VOTING"
    with open(STATUS_FILE, 'r') as f: return f.read().strip()

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'Vishal' and password == 'Vishal124':
        session['user'] = 'Admin'
        return redirect(url_for('admin')) # Yahan error aa raha tha kyunki niche wala admin function missing tha

    df = pd.read_csv(USERS_CSV)
    user = df[(df['username'] == username) & (df['password'] == password)]
    
    if not user.empty:
        session['user'] = username
        if get_status() == "DECLARED":
            return redirect(url_for('results'))
        return redirect(url_for('voter'))
    
    flash("Invalid Credentials!")
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if session.get('user') != 'Admin': 
        return redirect(url_for('index'))
    df = pd.read_csv(CANDIDATES_CSV)
    return render_template('admin.html', candidates=df.to_dict('records'))

@app.route('/admin/add', methods=['POST'])
def add_candidate():
    df = pd.read_csv(CANDIDATES_CSV)
    new_id = int(df['id'].max() + 1) if not df.empty else 1
    new_row = {'id': new_id, 'name': request.form['name'], 'symbol': request.form['symbol'], 'votes': 0}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CANDIDATES_CSV, index=False)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:cid>')
def delete_candidate(cid):
    df = pd.read_csv(CANDIDATES_CSV)
    df = df[df['id'] != cid]
    df.to_csv(CANDIDATES_CSV, index=False)
    return redirect(url_for('admin'))

@app.route('/admin/declare', methods=['POST'])
def declare():
    with open(STATUS_FILE, 'w') as f:
        f.write("DECLARED")
    return redirect(url_for('results'))

@app.route('/voter')
def voter():
    if 'user' not in session: return redirect(url_for('index'))
    df = pd.read_csv(CANDIDATES_CSV)
    return render_template('voter.html', candidates=df.to_dict('records'))

@app.route('/vote/<int:cid>')
def vote(cid):
    if 'user' not in session or session['user'] == 'Admin':
        return redirect(url_for('index'))

    users_df = pd.read_csv(USERS_CSV)
    user_mask = users_df['username'] == session['user']
    
    if users_df.loc[user_mask, 'has_voted'].values[0] == 'No':
        cand_df = pd.read_csv(CANDIDATES_CSV)
        cand_df.loc[cand_df['id'] == cid, 'votes'] += 1
        cand_df.to_csv(CANDIDATES_CSV, index=False)

        users_df.loc[user_mask, 'has_voted'] = 'Yes'
        users_df.to_csv(USERS_CSV, index=False)
        flash("Vote Cast Successfully!")
    else:
        flash("You have already voted!")
    
    return redirect(url_for('index'))

@app.route('/results')
def results():
    df = pd.read_csv(CANDIDATES_CSV).sort_values(by='votes', ascending=False)
    return render_template('results.html', candidates=df.to_dict('records'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)