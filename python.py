import praw
from flask import Flask, render_template, request, url_for, redirect, make_response
app = Flask(__name__,template_folder='template')

reddit = praw.Reddit(client_id='Hxc2B78UAIzCLg',
                     client_secret='cIHztQXA-iZEB-kPYU-XEtDJhkM',
                     user_agent='RedditBot v0.1 by /u/JCoelhoo',
                     username='JCoelhoo',
                     password='bacoco00')

subreddits = ['cscareerquestions', 'awww', 'careerquestions','peoplefuckingdying','leagueoflegends','Damnthatsinteresting','theoffice']

@app.route("/", methods=["POST"])
def add():
	global subreddits
	sub = request.form['sub']
	if(sub not in subreddits):
		subreddits.append(sub)
	resp = make_response(redirect(url_for("home")))
        resp.set_cookie('subs', ','.join(subreddits))
	return resp

@app.route("/reset")
def reset():
        global subreddits
        subreddits = ['cscareerquestions']
        resp = make_response(redirect(url_for("home")))
        resp.set_cookie('subs', ','.join(subreddits))
        return resp

@app.route("/")
def home():
        global subreddits
	posts=[]
	if('subs' in request.cookies):
		subreddits = request.cookies.get('subs').split(',')
	for sub in subreddits:
		subr = reddit.subreddit(sub)
		try:
			print subr.title
			array = []
			for submission in subr.hot(limit=10):
			    print "\t", submission.title, submission.thumbnail
			    if(not submission.stickied):
				array.append(submission)
			posts.append(array)
		except:
			subreddits.remove(sub)
			continue;

   	resp = make_response(render_template('index.html', posts = posts, subreddits = subreddits))
	return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2001)
