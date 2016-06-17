from flask import Flask,url_for,redirect,render_template,request
from werkzeug.utils import secure_filename
import os,time,re

app = Flask(__name__)

app.config["DEBUG"] = True
UPLOAD_FOLDER = os.path.join(os.getcwd(),'static')

@app.route("/")
def index():
	newfiles,backups,files = [],[],[]
	fs = os.listdir('static')
	for file in fs:
		if file.endswith('.apk') and not re.search(r"_\d{12}",file):
			newfiles.append(file)
		elif file.endswith('.apk'):
			backups.append(file)
		else:
			files.append(file)
	backups = sorted(backups,key=lambda b: int(b.rsplit('_',1)[1].split('.')[0]),reverse=True)
	newfiles = readstat(newfiles)
	backups = readstat(backups)
	files = readstat(files)
	return render_template("index.html",newfiles=newfiles,backups=backups,files=files)

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
		prefix,suffix = f.filename.rsplit(".",1)
		if f.filename in os.listdir("static"):
			tmpstr = time.strftime("_%Y%m%d%H%M%S")
			os.system("mv %s %s" %(f.filename,os.path.join(UPLOAD_FOLDER,"%s%s.%s" %(prefix,tmpstr,suffix))))
		file = os.path.join(UPLOAD_FOLDER,f.filename)
		f.save(file)
	except Exception as e:
		print(e)
	finally:
		return redirect(url_for(".index"))

if __name__ == "__main__":
	app.run("0.0.0.0",port=8888)
