import sqlite3
#questo file si occupa di effettuare le query al database
#la struttura delle funzioni è grossomodo sempre la stessa, ce ne sono solo tante!
def get_user_by_username(username):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM users WHERE username = ?'
    cursor.execute(sql, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if(user):
        return user
    else:
        return False

def add_user(user):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO users(username, name, surname, password, creator, profilepic) VALUES(?,?,?,?,?,?)'

    try:
        cursor.execute(sql, (user['username'], user['name'], user['surname'], user['password'], user['creator'], user['profilepic']),)
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def add_podcast(podcast):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO podcasts(title, creator, description, cover) VALUES(?,?,?,?)'

    try:
        cursor.execute(sql, (podcast['title'], podcast['creator'], podcast['description'], podcast['cover']),)
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_id(title):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT id FROM podcasts WHERE title = ?'
    cursor.execute(sql, (title,))
    id = cursor.fetchone()

    cursor.close()
    conn.close()

    return id

def add_tags(tags, title):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    id = get_id(title)

    if(tags['comedy'] == 'on'):
        tags['comedy'] = 1
    else:
        tags['comedy'] = 0

    if(tags['politics'] == 'on'):
        tags['politics'] = 1
    else:
        tags['politics'] = 0
    
    if(tags['history'] == 'on'):
        tags['history'] = 1
    else:
        tags['history'] = 0
       
    if(tags['crime'] == 'on'):
        tags['crime'] = 1
    else:
        tags['crime'] = 0

    success = False

    sql = 'INSERT INTO tags(id, comedy, politics, history, crime) VALUES(?,?,?,?,?)'

    try:
        cursor.execute(sql, (id['id'], tags['comedy'], tags['politics'], tags['history'], tags['crime']),)
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_podcast(id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcasts WHERE id = ?'
    cursor.execute(sql, (id,))
    podcast = cursor.fetchone()

    cursor.close()
    conn.close()

    return podcast

def add_episode(episode):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO episodes(podcast, title, description, date, audio) VALUES(?,?,?,?,?)'

    try:
        cursor.execute(sql, (episode['podcast'], episode['title'], episode['description'], episode['date'], episode['audio'],))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_episodes(id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM episodes WHERE podcast = ? ORDER BY date DESC'
    cursor.execute(sql, (id,))
    episodes = cursor.fetchall()

    cursor.close()
    conn.close()

    return episodes  

def get_episode(id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM episodes WHERE id = ?'
    cursor.execute(sql, (id,))
    episode = cursor.fetchall()

    cursor.close()
    conn.close()

    return episode

def get_tags(id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM tags WHERE id = ?'
    cursor.execute(sql, (id,))
    tags = cursor.fetchall()

    cursor.close()
    conn.close()

    return tags   

def get_user_podcasts(username):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM podcasts WHERE creator = ?'
    cursor.execute(sql, (username,))
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts   

def add_follow(username, id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'INSERT INTO follow(username, id) VALUES(?,?)'

    try:
        cursor.execute(sql, (username, id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_follows(username):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT * FROM follow WHERE username = ?'
    cursor.execute(sql, (username,))
    follows = cursor.fetchall()

    cursor.close()
    conn.close()

    return follows

def get_follow(username, id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT username, id FROM follow WHERE (id, username) in (SELECT id, username FROM follow WHERE id = ? AND username = ?)'
    cursor.execute(sql, (username, id,))
    check = cursor.fetchall()

    cursor.close()
    conn.close()

    return check

def remove_follow(username, id):
    conn = sqlite3.connect('aa.db')
    conn.execute("PRAGMA foreign_keys=1")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM follow WHERE username = ? AND id = ?'
    try:
        cursor.execute(sql, (username, id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def remove_episode(id):
    conn = sqlite3.connect('aa.db')
    conn.execute("PRAGMA foreign_keys=1")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM episodes WHERE id = ?'
    try:
        cursor.execute(sql, (id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def add_comment(id, username, text):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    success = False
    sql = 'INSERT INTO comments(episode, username, text) VALUES(?,?,?)'

    try:
        cursor.execute(sql, (id, username, text,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_podcast_by_episode(id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT podcast FROM episodes WHERE id = ?'
    cursor.execute(sql, (id,))
    podcast = cursor.fetchone()

    cursor.close()
    conn.close()

    return podcast

def get_comments(podcast):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT comments.id, comments.episode, comments.username, comments.text FROM comments,episodes WHERE comments.episode = episodes.id AND episodes.podcast = ?'
    cursor.execute(sql, (podcast,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return comments

def remove_podcast(id):
    conn = sqlite3.connect('aa.db')
    conn.execute("PRAGMA foreign_keys=1")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM podcasts WHERE id = ?'
    try:
        cursor.execute(sql, (id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def get_podcasts_by_tag(tag):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = 'SELECT podcasts.title, podcasts.cover, podcasts.id FROM podcasts, tags WHERE podcasts.id = tags.id AND  ' + tag +' =1'
    cursor.execute(sql)
    podcasts = cursor.fetchall()

    cursor.close()
    conn.close()

    return podcasts

def remove_comment(id):
    conn = sqlite3.connect('aa.db')
    conn.execute("PRAGMA foreign_keys=1")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'DELETE FROM comments WHERE id = ?'
    try:
        cursor.execute(sql, (id,))
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_podcast(podcast, id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE podcasts SET title = ?, description = ?, cover = ? WHERE id = ?'

    try:
        cursor.execute(sql, (podcast['title'], podcast['description'], podcast['cover'], id),)
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_tags(tags, id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if(tags['comedy'] == 'on'):
        tags['comedy'] = 1
    else:
        tags['comedy'] = 0

    if(tags['politics'] == 'on'):
        tags['politics'] = 1
    else:
        tags['politics'] = 0
    
    if(tags['history'] == 'on'):
        tags['history'] = 1
    else:
        tags['history'] = 0
       
    if(tags['crime'] == 'on'):
        tags['crime'] = 1
    else:
        tags['crime'] = 0

    success = False

    sql = 'UPDATE tags set comedy=?, politics=?, history=?, crime=? WHERE id = ?'

    try:
        cursor.execute(sql, (tags['comedy'], tags['politics'], tags['history'], tags['crime'], id),)
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_episode(episode, id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE episodes SET title = ?, description = ?, date = ? WHERE id = ?'

    try:
        cursor.execute(sql, (episode['title'], episode['description'], episode['date'], id),)
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success

def update_comment(text, id):
    conn = sqlite3.connect('aa.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    success = False
    sql = 'UPDATE comments SET text = ? WHERE id = ?'

    try:
        cursor.execute(sql, (text, id),)
        conn.commit()
        success = True
    except Exception as e:
        print('ERROR', str(e))
        # if something goes wrong: rollback
        conn.rollback()

    cursor.close()
    conn.close()

    return success