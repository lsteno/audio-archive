#imports
from fileinput import filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, app
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session 
import posts_dao
from posts_dao import add_tags, get_podcast, get_episodes, get_tags, get_user_podcasts, add_follow, get_follows, remove_follow, remove_episode, get_episode, update_comment
from posts_dao import add_comment, get_podcast_by_episode, get_comments, remove_podcast, get_podcasts_by_tag, remove_comment, update_podcast, update_tags, update_episode
from models import User
import os
import re
import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

#session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=2)
Session(app)

#login configuration setup
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

#landing page
@app.route('/')
def index():
    return render_template('index.html')

#login page with input control
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = posts_dao.get_user_by_username(username)

        if not user or not check_password_hash(str(user['password']), str(password)) or not username or not password:
            flash('Wrong username or password', 'danger')
            return redirect(url_for('login'))

        else:
            new = User(username=user['username'], name=user['name'], surname=user['surname'], password=user['password'], profilepic=user['profilepic'], creator=user['creator'])
            login_user(new, True)
            flash('You are logged in', 'success')
            return redirect(url_for('index'))

#user loader
@login_manager.user_loader
def load_user(username):
    try:
        user = posts_dao.get_user_by_username(username)

        new_user = User(username=user['username'], name=user['name'], surname=user['surname'], password=user['password'], profilepic=user['profilepic'], creator=user['creator'])
        return new_user

    except TypeError:
        pass

#signup page with inputcontrol
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    else:
        username = request.form.get('username')
        print(username)
        user_in_db = posts_dao.get_user_by_username(username)
        regex = re.compile('[@_!$%^&*<>?/\|}{~:]')
       
        if user_in_db:
            flash('Username already taken', 'danger')
            return redirect(url_for('signup'))

        elif((not username) or regex.search(username)):
            flash('Error with username, perhaps you used an illegal character?', 'danger')
            return redirect(url_for('signup'))
        else:
            profilepic = request.files['image']
            if profilepic and (profilepic.filename.endswith('.png') or profilepic.filename.endswith('.jpeg') or profilepic.filename.endswith('.gif') or profilepic.filename.endswith('.jpg')):
                profilepic.save('static/userimgs/' + username.lower() + 'profilepic' +'.jpg')
                profilepic = ('userimgs/' + username.lower() + 'profilepic' +'.jpg')
            else:
                profilepic = '/userimgs/profile.webp'
                flash('Something is wrong with your profile picture, try uploading another one', 'warning')

            password = request.form.get('password')
            if(len(password) < 6):
                flash('Password must have at least 6 characters', 'danger')
                return redirect(url_for('signup'))

            name = request.form.get('name')
            print(name)
            surname = request.form.get('surname')
            creator = request.form.get('creator')
            if(not creator):
                creator = 0
            
            if(name and surname):
                new_user = {"username": username, "name":name, "surname":surname, "password": generate_password_hash(password, method='sha256'), "creator":creator, "profilepic": profilepic}
            else:
                flash('All inputs must be filled out!', 'danger')
                return redirect(url_for('signup'))

            success = posts_dao.add_user(new_user)

            if success:
                flash('Utente creato correttamente', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error in user creation, try again', 'danger')

        return redirect(url_for('signup'))

#single podcast page with control over new podcast form, follow button form and episode deletion form
@app.route('/podcast/<int:id>', methods=['GET', 'POST'])
def podcast(id):
    pod = get_podcast(id)
    if request.method == 'POST': 
        if  'title' in request.form.keys():
            title = request.form.get('title')
            description = request.form.get('description')
            date = request.form.get('date')
            audio = request.files['audio']
            regex = re.compile('[@_!$%^&*<>?/\|}{~:]')
            if (title and regex.search(title) == None):
                if audio:
                    if audio.filename.endswith('.mp3'):
                        audio.save('static/podcastsep/' + title.lower().replace(" ", "").replace("-", "") + date.replace("-", "") +'.mp3')
                        audio = ('podcastsep/' + title.lower().replace(" ", "").replace("-", "") + date.replace("-", "") +'.mp3')
                    else:
                        flash('Error in audio file upload, try again with a .mp3 file', 'warning')
                        return redirect(url_for('podcast', id=pod['id']))
                else:
                    flash('Error in audio file upload, try again', 'danger')
                    return redirect(url_for('podcast', id=pod['id']))
                if(description and date):
                    if(valiDate(date)):
                        episode = {"podcast": id, "title": title, "description": description, "date": date, "audio": audio}
                        success = posts_dao.add_episode(episode)
                    else:
                        flash('Maximum date can be today!', 'warning')
                        return redirect(url_for('podcast', id=pod['id']))                        
                else:
                    flash('All inputs are required during episode creation', 'warning')
                    return redirect(url_for('podcast', id=pod['id']))

                if success:
                    flash('Episode created correctly', 'success')
                    return redirect(url_for('podcast', id=pod['id']))
                else:
                    flash('Error in podcast creation, try again', 'danger')
                    return redirect(url_for('podcast', id=pod['id']))
            else:
                flash('Special characters can\'t be used in titles', 'warning')
                return redirect(url_for('podcast', id=pod['id']))

        elif 'btnFollow' in request.form.keys():
            if request.form['btnFollow'] == 'following':
                add_follow(current_user.username, id)
                follows = get_follows(current_user.username)
                for follow in follows:
                    if (follow['id'] == id):
                        followValue = 'follow'
                        break
                return redirect(url_for('podcast', id=pod['id']))

            elif request.form['btnFollow'] == 'follow':
                remove_follow(current_user.username, id)
                return redirect(url_for('podcast', id=pod['id']))

        elif 'dotMenuDelete' in request.form.keys():
            episodeId = request.form['dotMenuDelete']
            rmEp = get_episode(episodeId)
            path = 'static/' + rmEp[0]['audio']
            os.remove(path)
            success = remove_episode(episodeId)
            if success:
                flash('Episode deleted correctly', 'success')
                return redirect(url_for('podcast', id=pod['id']))
            else:
                flash('Error in episode deletion, try again', 'warning')
                return redirect(url_for('podcast', id=pod['id']))

    else:
        comments = get_comments(pod['id'])
        tags = get_tags(pod['id'])
        episodes = get_episodes(pod['id'])
        followValue = 'follow'
        if(current_user.is_authenticated):
            follows = get_follows(current_user.username)
            for follow in follows:
                if (follow['id'] == id):
                    followValue = 'following'
                    break
        if(not current_user.is_authenticated):
            flash('Users must be logged in to play', 'warning')
        return render_template('podcast.html', pod = pod, episodes = episodes, tags = tags, followValue = followValue, comments = comments)

#route for comment creation
@app.route('/comments/new/<int:id>', methods=['POST'])
def newComment(id):
    username = current_user.username
    comment = request.form.get('text')
    success = False
    if(username and comment):
        success = add_comment(id, username,comment)

    if success:
        flash('Comment has been posted correctly', 'success')
        podcast = get_podcast_by_episode(id)
    else:
        flash('Error in comment upload: try again', 'danger')

    return redirect(url_for('podcast', id=podcast['podcast']))

#user profile page
@app.route('/user/<username>')
@login_required
def userPage(username):
    if(username != current_user.username):
        flash('You can only check your own profile!', 'warning')
        redirect(url_for('userPage', username = current_user.username))  
    podcasts = ''
    if(current_user.creator):
        podcasts = get_user_podcasts(current_user.username)

    followList = []
    follows = get_follows(current_user.username)
    for follow in follows:
        followList.append(get_podcast(follow['id']))
    return render_template('user.html', podcasts = podcasts, followList = followList)

#route for user logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You successfully logged out', 'success')
    return redirect(url_for('index'))

#route for new podcast creation
@app.route('/podcast/new', methods=['POST'])
def newPodcast():
    title = request.form.get('title')
    regex = re.compile('[@_!$%^&*<>?/\|}{~:]')
    if (title and regex.search(title) == None):
        description = request.form.get('description')
        comedy = request.form.get('comedy')
        politics = request.form.get('politics')
        history = request.form.get('history')
        crime = request.form.get('crime')
        if(comedy or politics or history or crime):
            tags = {"comedy": comedy, "politics": politics, "history": history, "crime": crime}
        else:
            flash('Choose at least one tag for your podcast', 'warning')
            return redirect(url_for('index'))            
        cover = request.files['cover']
        if cover:
            if cover.filename.endswith('.png') or cover.filename.endswith('.jpeg') or cover.filename.endswith('.gif') or cover.filename.endswith('.jpg'):
                title.replace(" ", "")
                cover.save('static/podcastsimgs/' + title.lower() + 'cover' +'.jpg')
                cover = ('podcastsimgs/' + title.lower() + 'cover' +'.jpg')
        else:
            cover = 'cover.png'
        creator = current_user.username
        if(not creator):
            flash('Error in podcast creation, try again.', 'warning')
            return redirect(url_for('index'))
        success = False
        if(description):
            podcast = {"title": title, "creator": creator, "description": description, "cover": cover}
            success = posts_dao.add_podcast(podcast)

        if success:
            flash('Podcast created correctly', 'success')
            add_tags(tags, title)
            return redirect(url_for('index'))
        else:
            flash('Error in podcast creation, try again.', 'warning')
            return redirect(url_for('index'))
    else:
        flash('Special characters can\'t be used in titles', 'warning')
        return redirect(url_for('index'))

#route to modify podcast
@app.route('/podcast/update/<int:id>', methods=['POST'])
def updatePodcast(id):
    pod = get_podcast(id)
    title = request.form.get('title')
    regex = re.compile('[@_!$%^&*<>?/\|}{~:]')
    if (title and regex.search(title) == None):
        description = request.form.get('description')
        comedy = request.form.get('comedy')
        politics = request.form.get('politics')
        history = request.form.get('history')
        crime = request.form.get('crime')
        if(comedy or politics or history or crime):
            tags = {"comedy": comedy, "politics": politics, "history": history, "crime": crime}
        else:
            flash('Choose at least one tag for your podcast', 'warning')
            return redirect(url_for('podcast', id = id))
        cover = request.files['cover']
        if cover and (cover.filename.endswith('.png') or cover.filename.endswith('.jpeg') or cover.filename.endswith('.gif')):
            title.replace(" ", "")
            cover.save('static/podcastsimgs/' + title.lower() + 'cover' +'.jpg')
            cover = ('podcastsimgs/' + title.lower() + 'cover' +'.jpg')
        else:
            cover = pod['cover']

        success = False
        if(description):
            podcast = {"title": title, "description": description, "cover": cover}
            success = update_podcast(podcast, id)

        if success:
            flash('Podcast updated correctly', 'success')
            update_tags(tags, id)
            return redirect(url_for('podcast', id = id))
        else:
            flash('Error in podcast update, try again', 'warning')
            return redirect(url_for('podcast', id = id))
    else:
        flash('Special characters can\'t be used in titles', 'warning')
        return redirect(url_for('podcast', id = id))

#route to modify single episodes in a podcast
@app.route('/episode/update/<int:id>', methods=['POST'])
def updateEpisode(id):
    title = request.form.get('title')
    description = request.form.get('description')
    date = request.form.get('date')
    episode = {"title": title, "description": description, "date": date}
    regex = re.compile('[@_!$%^&*<>?/\|}{~:]')
    success=False
    if(title and description and date and regex.search(title) == None and valiDate(date)):
        success = update_episode(episode, id)
    podId = get_podcast_by_episode(id)
    if success:
        flash('Episode updated correctly', 'success')
        return redirect(url_for('podcast', id = podId['podcast']))
    else:
        flash('Error in podcast update, try again', 'warning')
        return redirect(url_for('podcast', id = podId['podcast']))

#route to delete podcasts
@app.route('/delete/<int:id>', methods=['POST'])
def deletePodcast(id):
    episodes = get_episodes(id)
    for episode in episodes:
        path = 'static/' + episode['audio']
        os.remove(path)
        success = remove_episode(episode['id'])
    podcast = get_podcast(id)
    if(podcast['cover'] != 'cover.png'):
        path = 'static/' + podcast['cover']
        os.remove(path)
    success = remove_podcast(id)
    if success:
        flash('Podcast deleted correctly', 'success')
        return redirect(url_for('index'))
    else:
        flash('Error in episode deletion, try again', 'warning')
        return redirect(url_for('podcast', id=id))

#route to delete single comments
@app.route('/comments/delete/<int:id>', methods=['POST'])
def deleteComment(id):
    success = remove_comment(id)
    if success:
        flash('Comment deleted correctly', 'success')
        return redirect(url_for('index'))
    else:
        flash('Error in episode deletion, try again', 'warning')
        return redirect(url_for('index'))

#route to modify comments
@app.route('/comment/update/<int:id>/<int:podId>', methods=['POST'])
def updateComment(id, podId):
    commentText = request.form.get('commentText')
    success=False
    if(commentText):
        success = update_comment(commentText, id)
    if success:
        flash('Comment updated correctly', 'success')
        return redirect(url_for('podcast', id = podId))
    else:
        flash('Error in comment update, try again', 'warning')
        return redirect(url_for('podcast', id = podId))

#pages of each explore tag
@app.route('/explore/<tag>')
def explore(tag):
    podcasts = get_podcasts_by_tag(tag)
    return(render_template('explore.html', tag=tag, podcasts=podcasts))

#page for error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#function to validate dates 
def valiDate(date_text):
    try:
        past = datetime.datetime.strptime(date_text, '%Y-%m-%d')
        present = datetime.datetime.now()
        if (past.date() < present.date()):
            return True
        else:
            return False
    except ValueError:
        raise ValueError("Incorrect date format")