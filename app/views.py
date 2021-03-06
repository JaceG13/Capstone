
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import *
import json

@app.route('/')
def home():
	return render_template("app.html")

@app.route('/api/register',methods =["POST"])
def signUp():
	# form = SignUpForm()
	if request.method == "POST":
		response = { "status": 'null', "data":'null', "message": 'null'}
		try:
			data = json.loads(request.data)
			print data["fname"]
			student = Student(studentID = data["id"], first_name = data["fname"], last_name = data["lname"], password = data["password"])
			print student.json
			db.session.add(student)
			db.session.commit()
		except:
			response['status'] = "error"
			response["message"]="registration error"
			return jsonify(response)
		else:
			response["status"] ="success"
			response["message"] ="successful registration"
			response["data"] = student.json
			return jsonify(response)


	return render_template("signup.html", form = form)

@app.route('/api/login', methods=["POST"])
def login():
	if request.method== "POST":
		response = { "status": 'null', "data":'null', "message": 'null'}
		data = json.loads(request.data)
		try:
			student = Student.query.filter_by(studentID = data["id"], password = data["password"]).first()
		except:
			response["status"] ="error"
			response["message"] = "error encountered trying to log in"
			return jsonify(response)
		else:
			if student:
				response["status"]="success"
				response["message"]="successful login"
				response["data"]= student.json
				return jsonify(response)
			else:
				response["status"]="error"
				response["message"]="incorrect credentials"
				return jsonify(response)


	return render_template("login.html", form = form)

@app.route("/api/submit/<studentID>", methods = ["POST"])
def submitSubjects(studentID):
	if request.method == "POST":
		response = { "status": 'null', "data":'null', "message": ''}
		if request.headers["Content-Type"] == 'csec-subjects':
			csecSubjects = json.loads(request.data)
			for sub in csecSubjects:
				result = Studied.query.filter_by(studentID=studentID, subjectName = sub['subjectName']).first()
				if result:
					print ("already added that subject")
				else:
					db.session.add(Studied(studentID = studentID,grade = sub['grade'],subjectName=sub['subjectName']))
			try:	
				db.session.commit()
			except:
				response["status"]="error"
				response["message"]="error adding subjects"
				return jsonify(response)
			else:
				response["status"]="success"
				response["message"]="subjects successfully added"
				return jsonify(response)

		if request.headers["Content-Type"] == 'cape-subjects':
			capeSubjects = json.loads(request.data)
			for sub in capeSubjects:
				subject = sub["subject"]
				print "preeeeeresuisisite"
				print subject["prerequisite"]
				print "enddddddd\n\n"
				prereqCheck = Studied.query.filter_by(studentID = studentID, subjectName = subject["prerequisite"]).first()
				result = Application.query.filter_by(studentID=studentID, subjectName = subject["name"]).first()
				if result:
					response["message"]+="already applied for "+subject["name"]+";"
					print "already applied for that subject"

				else:
					print prereqCheck
					if  prereqCheck or subject["prerequisite"]=="None":
						db.session.add(Application(studentID = studentID,subjectName=subject['name'],subjectPriority = sub["priority"]))
					else:
						response["message"]+= subject["name"]+" requires a prerequisite;"
						print ("requires a prerequisite")
			try:
				db.session.commit()
			except:
				response["status"]="error"
				response["message"]+="error applying for subjects"
				# return jsonify(response)
			else:
				response["status"]="success"
				response["message"]+="successful application;"
		return jsonify(response)
			

@app.route("/api/subjects", methods=["GET"])
def getSubjects():
	
	if request.method  == "GET":

		if request.headers['Accept'] =="csec-list":
			# returns list of csec subjects from the database to the angular front end
			sub_list = []
			subjects = Csec.query.all()
			for subject in subjects:
				sub_list.append(str(subject.subjectName))

			return jsonify(sub_list)

		if request.headers['Accept'] == "cape-list":
			# returns list of cape subjects from the database to the angular front end
			sub_list = []
			subjects = Cape.query.all()
			for subject in subjects:
				# print subject
				sub = {}
				sub["name"]= str(subject.subjectName)
				sub["prerequisite"] = str(subject.prerequisiteSubject)
				sub_list.append(sub)

			return jsonify(sub_list)

@app.route('/api/subjects/<studid>', methods = ["GET"])
def getStudentSubjects(studid):
	if request.method =="GET":
		response = { "status": 'null', "data":'null', "message": ''}
		sub_list =[]
		if request.headers['Accept'] == 'cape':
			subjects = Application.query.filter_by(studentID = studid)
			if subjects:
				
				for subject in subjects:
					sub = {}
					sub["name"] = str(subject.subjectName)
					sub["priority"] = subject.subjectPriority
					sub_list.append(sub)
				# response["status"] = 'success'
				# response["data"] = sub_list
				# response["message"]= "subjects successfully retrieved"
		if request.headers['Accept'] =='csec':
			subjects = Studied.query.filter_by(studentID = studid)
			if subjects:
				for subject in subjects:
					sub = {}
					sub["name"] = subject.subjectName
					sub["grade"] = subject.grade
					sub_list.append(sub)

		if request.headers['Accept'] == 'successful-cape':
			subjects = SuccessfulApplication.query.filter_by(studentID = studid)
			if subjects:
				
				for subject in subjects:
					sub = {}
					sub["name"] = str(subject.subjectName)
					sub_list.append(sub)
				
		response["status"] = 'success'
		response["data"] = sub_list
		response["message"]= "subjects successfully retrieved"		
		return jsonify(response)


@login_manager.user_loader
def load_user(id):
    return Student.query.get(str(id))

@app.route("/logout", methods = ["GET","POST"])
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))



#handles routing of webpages

