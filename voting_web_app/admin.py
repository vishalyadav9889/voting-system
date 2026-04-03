from flask import Blueprint, render_template, session, redirect, url_for
from utils.csv_helper import read_csv

admin = Blueprint('admin', __name__)

@admin.route('/admin/dashboard')
def dashboard():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    # Stats calculate karein
    users_df = read_csv('users.csv')
    cand_df = read_csv('candidates.csv')
    
    stats = {
        'total_voters': len(users_df[users_df['role'] == 'voter']),
        'total_candidates': len(cand_df),
        'votes_polled': int(cand_df['vote_count'].sum()) if not cand_df.empty else 0
    }
    
    # Folder structure ke hisaab se: templates/admin/dashboard.html
    return render_template('admin/dashboard.html', stats=stats)