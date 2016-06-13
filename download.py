from flask import Flask,url_for,redirect,render_template,request
from werkzeug.utils import secure_filename
import os,time

app = Flask(__name__)

app.config["DEBUG"] = True
UPLOAD_FOLDER = os.path.join(os.getcwd(),'static')

@app.route("/")
def index():
	suimes,others,docs = [],[],[]
	files = os.listdir('static')
	for file in files:
		if file.endswith('.apk'):
			if file.startswith('Suime'):
				suimes.append(file)
			else:
				others.append(file)
		else:
			docs.append(file)
	suimes = sorted(suimes,key=lambda b: int(b.split('_')[2].split('.')[0]),reverse=True)
	suimes = readstat(suimes)
	others = readstat(others)
	docs = readstat(docs)
	return render_template("index.html",suimes=suimes,others=others,docs=docs)

def readstat(filelist):
	flist = []
	for name in filelist:
		file = "static/%s" %name
		size = round(os.path.getsize(file)/1024)
		size = "%s MB" %round(size/1024,2) if size >1000 else "%s KB" %size
		ctime = time.localtime(os.path.getctime(file))
		times = []
		for j in ctime[:6]:
			if j<10:
				times.append("0%s" %j)
			else:
				times.append(str(j))
		ftime = "%s-%s-%s %s:%s:%s" %(times[0],times[1],times[2],times[3],times[4],times[5])
		flist.append((name,file,size,ftime))
	return flist

@app.route("/upload",methods=["POST"])
def upload():
	try:
		f = request.files['filecontent']
		file = os.path.join(UPLOAD_FOLDER,f.filename)
		f.save(file)
	except:
		pass
	finally:
		return redirect(url_for(".index"))


if __name__ == "__main__":
	app.run("0.0.0.0",port=8888)
