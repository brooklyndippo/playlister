# command python3 -m flask run
# localhost:5000


from flask import Flask, render_template, request, redirect, url_for
from flask.templating import render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient()
db = client.Playlister
playlists = db.playlists
comments = db.comments

app = Flask(__name__)

# helper function to create video URLs
def video_url_creator(id_lst):
    videos = []
    for vid_id in id_lst:
        video = 'https://youtube.com/embed/' + vid_id
        videos.append(video)
    return videos


@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', playlists=playlists.find())


# NEW PLAYLIST
@app.route('/playlists/new')
def playlists_new():
    """Create a new playlist."""
    playlist = {}
    # Add the title parameter here
    return render_template('playlists_new.html', playlist=playlist, title='New Playlist')

    

# CREATE A PLAYLIST
@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    # Grab the video IDs and make a list out of them
    video_ids = request.form.get('video_ids').split()
    # call our helper function to create the list of links
    videos = video_url_creator(video_ids)
    playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids,
        'created_at': datetime.now()
    }
    playlists.insert_one(playlist)
    #upddate redirect to the new playlist
    return render_template('playlists_show.html', playlist=playlist, title='New Playlist')
    #DELTE LATER!!! return redirect(url_for('playlists_index'))

#SEE A PLAYLIST
@app.route('/playlists/<playlist_id>')
def playlists_show(playlist_id):
    """Show a single playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    playlist_comments = comments.find({'playlist_id': ObjectId(playlist_id)})
    print(playlist_comments)
    return render_template('playlists_show.html', playlist=playlist, comments=playlist_comments)

#EDIT A PLAYLIST
@app.route('/playlists/<playlist_id>/edit')
def playlists_edit(playlist_id):
    """Show the edit form for a playlist."""
    playlist = playlists.find_one({'_id': ObjectId(playlist_id)})
    # Add the title parameter here
    return render_template('playlists_edit.html', playlist=playlist, title='Edit Playlist')

#UPDATE A PLAYLIST
@app.route('/playlists/<playlist_id>', methods=['POST'])
def playlists_update(playlist_id):
    """Submit an edited playlist."""
    video_ids = request.form.get('video_ids').split()
    videos = video_url_creator(video_ids)
    # create our updated playlist
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': videos,
        'video_ids': video_ids
    }
    # set the former playlist to the new one we just updated/edited
    playlists.update_one(
        {'_id': ObjectId(playlist_id)},
        {'$set': updated_playlist})
    # take us back to the playlist's show page
    return redirect(url_for('playlists_show', playlist_id=playlist_id))

#DELETE A PLAYLIST 
@app.route('/playlists/<playlist_id>/delete', methods=['POST'])
def playlists_delete(playlist_id):
    """Delete one playlist."""
    playlists.delete_one({'_id': ObjectId(playlist_id)})
    return redirect(url_for('playlists_index'))


#COMMENTS RESOURCE ==============================

#NEW COMMENT
@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    comment = {
        'playlist_id': ObjectId(request.form.get('playlist_id')),
        'title': request.form.get('title'),
        'content': request.form.get('content'),
    }
    print(comment)
    comments.insert_one(comment)
    return redirect(url_for('playlists_show', playlist_id=request.form.get('playlist_id')))

#DESTROY A COMMENT 
@app.route('/playlists/<playlist_id>/comments/<comment_id>/delete', methods=['POST'])
def comments_delete(playlist_id, comment_id):
    """Delete one comment."""
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', playlist_id=playlist_id))


if __name__ == '__main__':
    app.run(debug=True)