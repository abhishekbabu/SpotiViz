from flask import Flask, redirect, render_template, request, session
from app import app
from app import spotify_service

# App routes
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate')
def authenticate():
    return redirect(spotify_service.AUTH_URL)

@app.route('/callback')
def callback():
    auth_token = request.args['code']
    auth_header = spotify_service.authorize(auth_token)
    session['auth_header'] = auth_header

    return redirect('profile')

@app.route('/profile')
def profile():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # Get profile data
        profile_data = spotify_service.get_user_profile(auth_header)
        first_name = profile_data['display_name'].partition(' ')[0]
        profile_pic = profile_data['images'][0]['url']

        # Get 6 most recently played tracks
        recently_played = spotify_service.get_recently_played(auth_header)
        recent_6_tracks = recently_played["items"][0:6]

        recent_tracks = {}
        for item in recently_played["items"]:
            if item["track"]["id"] not in recent_tracks.keys():
                recent_tracks[item["track"]["id"]] = item
            if len(recent_tracks) == 6:
                break

        return render_template('profile.html', name=first_name, profile_pic=profile_pic, recent_6_tracks=recent_tracks.values())
    
    return render_template('profile.html')