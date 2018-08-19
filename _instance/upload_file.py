import os
from flask import Flask, flash, session, render_template, request, url_for, redirect, send_from_directory, session
from werkzeug import secure_filename, Response, Request

app = Flask(__name__, template_folder='.')

@app.route('/')
def upload():
	return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		return 'Your file was uploaded successfully'

if __name__ == '__main__':
	app.run(debug = True)

# UPLOAD_FOLDER = '~/_instance/uploading_here'
# ALLOWED_FILES = set(['txt'])
#
# app = Flask(__name__)
# sess = Session()
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# def allowed_file(filename):
# 	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILES
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
# 	if request.method == 'POST':
# 		if 'file' not in request.files:
# 			flash('No file part')
# 			return redirect(request.url)
# 		file =  request.files['file']
# 		if file.filename == '':
# 			flash('No selected file')
# 			return redirect(request.url)
# 		if file and allowed_file(file.filename):
# 			filename = secure_filename(file.filename)
# 			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 			return redirect(url_for('upload_file'), filename=filename)
# 	return '''
# 	<!DOCTYPE html>
# 	<html>
# 	<title>F.T.W</title>
# 	<meta name="viewport" content="width=device-width, initial-scale=1">
# 	<link rel="stylesheet" href="https://www.w3schools.com/lib/w3.css">
#
# 	<body>
#
# 	<header class="w3-container w3-teal">
# 	  <h1>F.T.W</h1>
# 	</header>
#
# 	<div class="w3-col">
# 	  <div class="w3-quarter w3-container w3-white">
#
# 	  </div>
# 	  <div class="w3-half w3-container w3-white">
# 	        <form name = "loginform" class="w3-container" action="/" method = "post">
# 			<form method=post enctype=multipart/form-data>
# 			  <input type=file name=file>
# 			  <input type=submit value=Upload>
# 			</form>
# 	</div>
# 	    <div class="w3-quarter w3-container w3-white">
# 		</div>
# 	</body>
# 	</html>
# 	'''
# if __name__ != '__main__':
# 	app.secret_key = 'super secret key'
# 	app.config['SESSION_TYPE'] = 'filesystem'
# 	sess.init_app(app)
#
# 	app.run(debug = True)
