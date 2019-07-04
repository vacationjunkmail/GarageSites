from flask import Flask, render_template, request, jsonify, g
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import datetime
import base64
import sys

from db_conn.mysql_connection import get_connection
from class_folder.send_email import gmail_connection

app = Flask(__name__)

#import RPi.GPIO as GPIO
#import time

@app.before_request
def before_request():
    #Setting up connection
    g.mysql_db = get_connection()
    #print(request.user_agent)
    #print(request.user_agent.string)
    #print(request.user_agent.platform)
    #print(request.user_agent.browser)
    #print(request.user_agent.version)
    #print('___________________________')
    #print(request.user_agent)
    #print('___________________________')
	
@app.after_request
def after_request(resp):
    #closing connection
    g.mysql_db.close_connection()
    
    return resp

@app.route('/')
def index():
   
    columns,error,data = [],[],[]
    query = '''select username from automation_db.users_db;'''
    select_user = g.mysql_db.select_query(query)

    data = select_user[1]
    columns = select_user[0]
    error = select_user[2]
    
    if len(error):
        print("Error\n**************\n{}\n**************".format(error))
        
    return render_template("index.html", users=data, columns=columns, error = len(error))
@app.route('/<route_title>/')
def getroute(route_title):
    route_name = route_title.capitalize()
    route_title = "{}.html".format(route_title)
    
    columns,error,data = [],[],[]
    
    if route_name.lower() == 'garage':
        query = '''select username from automation_db.users_db;'''
        select_user = g.mysql_db.select_query(query)

        data = select_user[1]
        columns = select_user[0]
        error = select_user[2]
    
    return render_template(route_title,title = route_name,users=data, columns=columns, error = len(error))
    
@app.route('/garage_door/', methods = ['POST'])
def garage_door():
    
    params = []
    
    query = '''select id,username,email_address from automation_db.users_db where password = %s;'''
    #params.append(request.form['pwd']);
    pwd = base64.b64encode(request.form['pwd'].encode('utf-8'))
    print(pwd)
    pwd =pwd.decode('utf-8')
    params.append(pwd)
    
    
    find_user = g.mysql_db.select_params(query,params)
    columns = find_user[0]
    data = find_user[1]
    error = find_user[2]
    
    if len(error):
        print("Error\n**************\n{}\n**************".format(error))
        msg = "Oops Something happened"
    elif len(data) == 0:
        msg = "Can not be found"
        error.append(msg)
    else:
        m = request.form['which_door'].split("_")    
        params = []
        query = '''insert into automation_db.automation_action(user_db_id,action)values(%s,%s);'''
                
        params.append(data[0]['id'])
        params.append(m[0])
        
        insert = g.mysql_db.insert_query(query,params)
        
        msg = "{} garage door action".format(m[0])
        pin = 0
    
        if request.form['which_door'] == 'left_door':
            pin = 4        
        elif request.form['which_door']:
            pin = 3
    
        if pin > 0:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(4)
            GPIO.output(pin, GPIO.HIGH)
        else:    
            msg = "An error occurred!"
    
    return jsonify(msg = msg,error = len(error))

@app.route('/relay_on/')
def relay_on():
    GPIO.setmode(GPIO.BCM)
    pin = 17
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    GPIO.output(pin, GPIO.LOW)
    
    return jsonify('On','')

@app.route('/relay_off/')
def relay_off():
    pin = 17
    time.sleep(2)
    error=[]

    try:
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        GPIO.cleanup()
        msg='Off'
    except Exception as e:
        print(e)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        GPIO.cleanup()
        msg='Off but had to go to except'
    return jsonify(msg,error)
    
@app.route('/relay/')    
def relay():
    
    #init list with pin
    PinList = [2,3,4,17]
    PinList = [17]
    for p in PinList:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.HIGH)
	
    #sleep time

    SleepTime = 10

    try:
        for p in PinList:
            GPIO.output(p, GPIO.LOW)
            print("Pin {} is on.".format(p))
            time.sleep(SleepTime)
            #High turns the pins off.
            GPIO.output(p, GPIO.HIGH)
            print("Pin {} is off.".format(p))
            time.sleep(SleepTime)
            
        GPIO.cleanup()
        print("Done all pins are off")
    except KeyboardInterrupt:
        print("\n\tCommand from Keyboard  to Quit")
        GPIO.cleanup()
    except Exception as e:
        print("An error has occured\n\t{}".format(e))
        
        GPIO.cleanup()
    return "pin"

@app.route('/camera/')
def camera():
	error = []
	d = datetime.datetime.now()
	name = "garage_{}.png".format(d.strftime("%m_%d_%Y_at_%I_%M_%S_%p"))
	camera = PiCamera()
	camera.start_preview()
	time.sleep(5)
	camera.capture("{}/{}".format(app.static_folder,name))
	camera.stop_preview() 
	camera.close()
	#print(name)
	d = d.strftime("%m-%d-%Y at %I:%M:%S %p")
	
	msg = "Garage Photo taken at {}".format(d)
	
	return jsonify(msg = d,error = len(error),pic = name)

@app.route('/forgot/',defaults={'username': 'all'})
@app.route('/forgot/<string:username>/')
def findpwd(username):
    referrer_url = request.headers.get("Referer")
    
    columns,error,data = [],[],[]
    email_to = ''
    if username == 'all':
        query = '''select id,username,email_address,password from automation_db.users_db order by id asc;'''
        select_user = g.mysql_db.select_query(query)
        email_to = select_user[1][0]['email_address']
        
    else:
        query = '''select id,username,email_address,password from automation_db.users_db where username = %s'''
        select_user = g.mysql_db.select_params(query,[username])

    data = select_user[1]
    columns = select_user[0]
    error = select_user[2]    
    
    try:    
        email_message=''
        for row in data:
            for col in columns:
                if col == 'password':
                    row[col] = base64.b64decode(row[col]).decode('utf-8')
                email_message += "{}:{}\n".format(col,row[col])
            email_message +="\n"
        
        if not len(email_to):
            email_to = data[0]['email_address']
        
        _gmail = gmail_connection()
        _gmail.send_pwd(email_to,email_message)
        print(_gmail.close_gmail())
                    
        #link = '''<a href="../../">Return</a>'''
        link = "<a href='{}'>Return</a>".format(referrer_url)
        msg = "Password sent to email on file. {}".format(link)
    except Exception as e:
        msg = "Error {} call the web developer".format(username)
        #print(e)
    
    return render_template("msg.html", msg=msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
    #Square Enix Ticket Number: 10470035
