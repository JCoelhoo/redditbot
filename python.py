import praw
from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__,template_folder='template')

reddit = praw.Reddit(client_id='Hxc2B78UAIzCLg',
                     client_secret='cIHztQXA-iZEB-kPYU-XEtDJhkM',
                     user_agent='RedditBot v0.1 by /u/JCoelhoo',
                     username='JCoelhoo',
                     password='bacoco00')

subreddits = [reddit.subreddit('cscareerquestions'), reddit.subreddit('awww')]

@app.route("/", methods=["POST"])
def add():
	global subreddits
	sub = reddit.subreddit(request.form['sub'])
	if(sub not in subreddits):
		subreddits.append(sub)
	return redirect(url_for("home"))

@app.route("/")
def home():
        global subreddits
	posts=[]
	for sub in subreddits:
		try:
			print sub.title
			array = []
			for submission in sub.hot(limit=10):
			    print "\t", submission.title
			    if(not submission.stickied):
				array.append(submission)
			posts.append(array)
		except:
			subreddits.remove(sub)
			continue;
	return render_template('index.html', posts = posts, subreddits = subreddits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2001)
