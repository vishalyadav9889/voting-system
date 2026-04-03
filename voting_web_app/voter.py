from flask import Blueprint, render_template, session, redirect, url_for
from utils.csv_helper import read_csv

voter = Blueprint('voter', __name__)

@voter.route('/voter/dashboard')
def dashboard():
    if 'user' not in session or session.get('role') != 'voter':
        return redirect(url_for('auth.login'))
    
    # User data load karein
    users_df = read_csv('users.csv')
    user_row = users_df[users_df['username'] == session['user']]
    
    if user_row.empty:
        return "User not found!"
    
    # Convert row to dictionary for easy template use
    user_info = user_row.iloc[0].to_dict()
    
    # Folder structure ke hisaab se: templates/voter/dashboard.html
    return render_template('voter/dashboard.html', user=user_info)