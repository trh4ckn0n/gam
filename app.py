from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['VOTES'] = {}  # Dictionnaire pour compter les votes

# Vérifier les fichiers autorisés
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Page d'accueil - envoyer un selfie
@app.route('/')
def index():
    return render_template('index.html')

# Page de vote
@app.route('/vote')
def vote():
    selfies = os.listdir(app.config['UPLOAD_FOLDER'])
    # Ne garder que les fichiers valides (images)
    selfies = [selfie for selfie in selfies if allowed_file(selfie)]
    return render_template('vote.html', selfies=selfelfies)

# Page d'administration - gérer les selfies et voir les votes
@app.route('/admin')
def admin():
    selfies = os.listdir(app.config['UPLOAD_FOLDER'])
    selfies = [selfie for selfie in selfies if allowed_file(selfie)]  # Filtrer uniquement les fichiers valides
    return render_template('admin.html', selfies=selfies, votes=app.config['VOTES'])

# Gérer l'upload des selfies
@app.route('/upload', methods=['POST'])
def upload():
    if 'selfie' not in request.files:
        return redirect(request.url)
    file = request.files['selfie']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        app.config['VOTES'][filename] = 0  # Initialiser les votes à 0 pour ce selfie
        return redirect(url_for('index', message="Selfie uploaded successfully!"))
    return redirect(url_for('index', message="Invalid file type"))

# Gérer le vote
@app.route('/vote_selfie/<filename>', methods=['POST'])
def vote_selfie(filename):
    if filename in app.config['VOTES']:
        app.config['VOTES'][filename] += 1  # Incrémenter les votes pour ce selfie
    return redirect(url_for('vote'))

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
