from flask import Flask, render_template, redirect, request, session, flash
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
    instrutor = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    id_video1 = db.Column(db.String(50), nullable=False)

    def __init__(self, id_playlist, titulo_playlist, descricao, instrutor): #instrutor, id_video1#
        self.id_playlist = id_playlist
        self.titulo_playlist = titulo_playlist
        self.instrutor = instrutor
        self.id_video1 = yt.get_videos(id_playlist)[0][4]
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

# Rota Login
@app.route('/login')
def login():
    session['usuario_logado'] = None # Desloga o usuario
    return redirect('/courses')

# rota autenticação
@app.route('/auth', methods=['GET', 'POST']) # Rota de autenticação
def auth():
    if request.form['senha'] == 'admin': # Se a senha for 'admin' faça:
      session['usuario_logado'] = 'admin' # Adiciona um usuario na sessão
      flash('Login feito com sucesso!') # Envia mensagem de sucesso
      return redirect('/adm') # Redireciona para a rota adm
    else: # Se a senha estiver errada, faça:
      flash('Erro no login, tente novamente!')  # Envia mensagem de erro
      return redirect('/login') # Redireciona para a rota login

@app.route('/logout') # Rota para deslogar
def logout():
   session['usuario_logado'] = None # Deixa o usuario_logado vazio
   return redirect('/login') # Redireciona para a rota principal (index.html)

# Adm - Adicionar - Início
@app.route('/adicionar')
def adicionar():
    return render_template('adm.html', playlist = '')

# ROTA EDITAR
@app.route('/<id>', methods=['GET', 'POST'])
def id():
    playlists = Playlist.query.all()
    playlist = playlists.query.get(id)
    return render_template('adm.html', playlist = playlist, titulo='Editar')    

# ROTA EDIT
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    # id = id[1:-1]
    playlists = Playlist.query.all()
    playlist = Playlist.query.get(id)
    if request.method == 'POST':
        playlist.id_playlist = request.form['id-playlist'].split('=')[1]
        playlist.instrutor = request.form['instrutor']
        playlist.titulo_playlist = request.form['titulo-playlist']
        playlist.descricao = request.form['descricao-playlist']
        db.session.commit()
        db.session.close()
        return redirect('/courses')
    return render_template('adm.html', playlist = playlist, titulo='Editar') 

# rota NEW para adicionar ao banco
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        playlist = Playlist(
            request.form['id-playlist'].split('=')[1],
            request.form['titulo-playlist'],
            request.form['descricao-playlist'],
            request.form['instrutor']
        )
        db.session.add(playlist)
        db.session.commit()
        db.session.close()
        return redirect('/adicionar')
    else:
        return redirect('/adicionar')

# Rota Listar Videos da Playlist
@app.route('/video_list/<id_playlist>')
def listar_videos(id_playlist):
    id_playlist = id_playlist[1:-1]
    videos = yt.get_videos(id_playlist)
    return render_template('video_list.html', videos=videos)



# Executa o server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)