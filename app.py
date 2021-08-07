from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from config import chave_secreta, url_postgresql
import yt

app = Flask(__name__)
app.secret_key = chave_secreta

app.config['SQLALCHEMY_DATABASE_URI'] = url_postgresql
db = SQLAlchemy(app)

# Class playlist para banco de dados
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_playlist = db.Column(db.String(50), nullable=False)
    titulo_playlist = db.Column(db.String(250), nullable=False)
    #instrutor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)

    def __init__(self, id_playlist, titulo_playlist,  descricao): #instrutor#
        self.id_playlist = id_playlist
        self.titulo_playlist = titulo_playlist
        #self.instrutor = instrutor
        self.descricao = descricao

# Rotas
# Rota principal
@app.route('/') 
def index():
    return render_template('index.html')
# Rota Cursos
@app.route('/courses')
def courses():
    playlist = Playlist.query.all()
    return render_template('courses.html', playlist = playlist)

# Rota sobre nós
@app.route('/about')
def about():
    return render_template('about.html')

# Adm - Adicionar - Início
@app.route('/adicionar')
def adicionar():
    return render_template('adm.html', playlist = '')

# ROTA EDITAR
@app.route('/<id>', methods=['GET', 'POST'])
def id():
    playlists = Playlist.query.all()
    playlist = playlist.query.get(id)
    return render_template('adm.html', playlist = playlist)    

# ROTA EDIT
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit():
    playlists = Playlist.query.all()
    playlist = playlist.query.get(id)
    if request.method == 'POST':
        playlist.id_playlist = request.form['id-playlist']
        playlist.titulo_playlist = request.form['titulo-playlist']
        playlist.descricao = request.form['descricao']
        db.session.commit()
        db.session.close()
        return redirect('/adm')
    return render_template('adm.html', playlist = playlist) 


@app.route('/load_playlist', methods=['GET', 'POST'])
def load_playlist():
    if request.method == 'POST':
        id_playlist = request.form['url-playlist'].split('=')[1]
        playlist_videos = yt.get_videos(id_playlist)
        return render_template('index.html', id_playlist=id_playlist, playlist_videos=playlist_videos)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        playlist = Playlist(
            request.form['id-playlist'],
            request.form['titulo-playlist'],
            request.form['descricao-playlist']
        )
        db.session.add(playlist)
        db.session.commit()
        return redirect('/courses')
    else:
        return redirect('/')
# Adm - Adicionar - Fim

# Executa o server

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)