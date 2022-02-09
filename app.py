from platform import java_ver
from flask import Flask, url_for, request, session, g, jsonify
from flask.templating import render_template
# from markupsafe import te
from werkzeug.utils import redirect
from database import connect_to_database, get_database
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3 
import json

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='admin'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'crudapplication_db'):
        g.crudapplication_db.close()

def get_current_user():
    user = None
    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()
    return user


@app.route('/home')
def index():
    user = get_current_user()
    return render_template('home.html', user = user)

@app.route('/reports')
def reports():
    user = get_current_user()
    return render_template('reports.html')

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/home')
def home():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('home.html')



@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from empmasterdata ')
    allemp = emp_cur.fetchall()
    return render_template('dashboard.html', user = user, allemp = allemp)

@app.route('/employeeadddetails')
def employeeadddetails():
    user = get_current_user()
    db = get_database()
    ead_cur = db.execute('select * from empadddetails ')
    allead = ead_cur.fetchall()
    return render_template('employeeadddetails.html', user = user, allead = allead)

@app.route('/billingmasterdata')
def billingmasterdata():
    user = get_current_user()
    db = get_database()
    bmd_cur = db.execute('select * from billingmasterdata ')
    allbmd = bmd_cur.fetchall()
    return render_template('billingmasterdata.html', user = user, allbmd = allbmd)

@app.route('/costcodes')
def costcodes():
    user = get_current_user()
    db = get_database()
    cc_cur = db.execute('select * from costcode ')
    allcc = cc_cur.fetchall()
    return render_template('costcodes.html', user = user, allcc = allcc)

@app.route('/yearlyexpenses')
def yearlyexpenses():
    user = get_current_user()
    db = get_database()
    ye_cur = db.execute('select * from yearlyexp')
    allye = ye_cur.fetchall()
    return render_template('yearlyexpenses.html', user = user, allye = allye)

@app.route('/monthlyexpenses')
def monthlyexpenses():
    user = get_current_user()
    db = get_database()
    me_cur = db.execute('select * from monthlyexp')
    allme = me_cur.fetchall()
    return render_template('monthlyexpenses.html', user = user, allme = allme)

@app.route('/sowdetails')
def sowdetails():
    user = get_current_user()
    db = get_database()
    sd_cur = db.execute('select * from sowdetails')
    allsd = sd_cur.fetchall()
    return render_template('sowdetails.html', user = user, allsd = allsd)

@app.route('/billingdetails')
def billingdetails():
    user = get_current_user()
    db = get_database()
    bd_cur = db.execute('select * from billingdetails ')
    allbd = bd_cur.fetchall()
    return render_template('billingdetails.html', user = user, allbd = allbd)

@app.route('/billabilityreport')
def billabilityreport():
    db = get_database()
    br_cur = db.execute('select billingdetails.empid, billingdetails.name, billingdetails.month, billingdetails.amount, billingdetails.year, billingdetails.sowdescription, billingdetails.noofdays, billingdetails.noofhours from billingdetails INNER JOIN empadddetails ON billingdetails.empid=empadddetails.empid where billable="Yes"')
    allbr = br_cur.fetchall()
    return render_template('billabilityreport.html',allbr=allbr)

@app.route('/nonbillabilityreport')
def nonbillabilityreport():
    db = get_database()
    nbr_cur = db.execute('select empid, name, ctc from empadddetails where billable="No"')
    allnbr = nbr_cur.fetchall()
    return render_template('nonbillabilityreport.html',allnbr=allnbr)

@app.route('/monthlyexpensesreport')
def monthlyexpensesreport():
    db = get_database()
    mer_cur = db.execute('select type_m, description_m, amount_m from monthlyexp ')
    allmer = mer_cur.fetchall()
    return render_template('monthlyexpensesreport.html', allmer = allmer )

@app.route('/yearlyexpensesreport')
def yearlyexpensesreport():
    db = get_database()
    yer_cur = db.execute('select type_y, description_y, amount_y from yearlyexp ')
    allyer = yer_cur.fetchall()
    return render_template('yearlyexpensesreport.html', allyer = allyer)

@app.route('/totalexpensesreport')
def totalexpensesreport():
    
     return render_template('totalexpensesreport.html')

@app.route('/employeedetailsreport')
def employeedetailsreport():
    db = get_database()
    edr_cur = db.execute('select billingdetails.empid, billingdetails.name, billingdetails.month, billingdetails.amount, billingdetails.year, billingdetails.sowdescription, billingdetails.noofdays, billingdetails.noofhours, empadddetails.ctc from billingdetails INNER JOIN empadddetails ON billingdetails.empid=empadddetails.empid')
    alledr = edr_cur.fetchall()
    return render_template('employeedetailsreport.html', alledr = alledr)

@app.route('/addnewemployee', methods = ["POST", "GET"])
def addnewemployee():
    user = get_current_user()
    if request.method == "POST":
        empid = request.form['empid']
        name = request.form['name']
        location = request.form['location']
        startdate = request.form['startdate']
        db = get_database()
        db.execute('insert into empmasterdata  (empid, name, location, startdate) values (?,?,?,?)', [empid,name, location, startdate])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('addnewemployee.html', user = user)

@app.route('/addnewemployeeadddetails', methods = ["POST", "GET"])
def addnewemployeeadddetails():
    user = get_current_user()
    if request.method == "POST":
        print("data", request.form)
        empid = request.form['empid']
        name = request.form['name']
        ctc = request.form['ctc']
        billable = request.form['billable']
        costcodes = request.form['costcodes']
        db = get_database()
        db.execute('insert into empadddetails  (empid, name, ctc, billable, costcodes) values (?,?,?,?,?)', [empid, name, ctc, billable, costcodes])
        db.commit()
        return redirect(url_for('employeeadddetails'))
    return render_template('addnewemployeeadddetails.html', user = user)

@app.route('/addnewbillingmasterdata', methods = ["POST", "GET"])
def addnewbillingmasterdata():
    user = get_current_user()
    if request.method == "POST":
        empid= request.form['empid']
        name = request.form['name']
        clientname = request.form['clientname']
        startdate = request.form['startdate']
        billrate = request.form['billrate']
        db = get_database()
        db.execute('insert into billingmasterdata (empid, name, clientname, startdate, billrate) values (?,?,?,?,?)', [empid, name, clientname, startdate, billrate])
        db.commit()
        return redirect(url_for('billingmasterdata'))
    return render_template('addnewbillingmasterdata.html', user = user)

@app.route('/addnewcostcodes', methods = ["POST", "GET"])
def addnewcostcodes():
    user = get_current_user()
    if request.method == "POST":
        department = request.form['department']
        costcodes = request.form['costcodes']
        db = get_database()
        db.execute('insert into costcode  (costcodes, department) values (?,?)', [costcodes, department])
        db.commit()
        return redirect(url_for('costcodes'))
    return render_template('addnewcostcodes.html', user = user)

@app.route('/addnewmonthlyexp', methods = ["POST", "GET"])
def addnewmonthlyexp():
    user = get_current_user()
    if request.method == "POST":
        type_m = request.form['type_m']
        description_m = request.form['description_m']
        amount_m = request.form['amount_m']
        db = get_database()
        db.execute('insert into monthlyexp (type_m, description_m, amount_m) values (?,?,?)', [type_m, description_m, amount_m])
        db.commit()
        return redirect(url_for('monthlyexpenses'))
    return render_template('addnewmonthlyexp.html', user = user)

@app.route('/addnewyearlyexp', methods = ["POST", "GET"])
def addnewyearlyexp():
    user = get_current_user()
    if request.method == "POST":
        type_y = request.form['type_y']
        description_y = request.form['description_y']
        amount_y = request.form['amount_y']
        db = get_database()
        db.execute('insert into yearlyexp (type_y, description_y, amount_y) values (?,?,?)', [type_y, description_y, amount_y])
        db.commit()
        return redirect(url_for('yearlyexpenses'))
    return render_template('addnewyearlyexp.html', user = user)

@app.route('/addnewsowdetails', methods = ["POST", "GET"])
def addnewsowdetails():
    user = get_current_user()
    if request.method == "POST":
        clientname = request.form['clientname']
        signeddata = request.form['signeddata']
        sowdescription = request.form['sowdescription']
        sowamount = request.form['sowamount']
        year = request.form['year']
        db = get_database()
        db.execute('insert into sowdetails (clientname, signeddata, sowdescription,sowamount,year) values (?,?,?,?,?)', [clientname, signeddata, sowdescription, sowamount, year])
        db.commit()
        return redirect(url_for('sowdetails'))
    return render_template('addnewsowdetails.html', user = user)

@app.route('/addnewbillingdetails', methods = ["POST", "GET"])
def addnewbillingdetails():
    user = get_current_user()
    if request.method == "POST":
        empid = request.form['empid']
        name = request.form['name']
        month = request.form['month']
        amount = request.form['amount']
        year = request.form['year']
        sowdescription = request.form['sowdescription']
        noofdays = request.form['noofdays']
        noofhours = request.form['noofhours']
        db = get_database()
        db.execute('insert into billingdetails  (empid, name, month, amount, year, sowdescription, noofdays, noofhours) values (?,?,?,?,?,?,?,?)', [empid, name, month, amount, year, sowdescription, noofdays, noofhours])
        db.commit()
        return redirect(url_for('billingdetails'))
    return render_template('addnewbillingdetails.html', user = user)

@app.route('/fetchone/<int:slno>')
def fetchone(slno):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from empmasterdata where slno = ?', [slno])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user = user, single_emp = single_emp)

@app.route('/fetchallemp')
def fetchallemp():
    user = get_current_user()
    # db = get_database()
    conn = connect_to_database()
    emp_cur = conn.execute('select empid from empmasterdata ')
    # single_cc = cc_cur.fetchall()
    # print (single_cc)
    jsonBody= []
    for row in emp_cur:
        jsonBody.append(row[0])
        print(row[0])
    return jsonify(jsonBody)
    # return (json.dumps(single_cc))

@app.route('/fetchallempid')
def fetchallempid():
    conn = connect_to_database()
    empcount_cur = conn.execute('select count(empid) from empmasterdata')
    jsonBody= []
    for row in empcount_cur:
        jsonBody.append(row[0])
        print(row[0])
    return jsonify(jsonBody)

@app.route('/fetchoneead/<int:slno>')
def fetchoneead(slno):
    user = get_current_user()
    db = get_database()
    ead_cur = db.execute('select * from empadddetails where slno = ?', [slno])
    single_ead = ead_cur.fetchone()
    return render_template('updateemployeeadddetails.html', user = user, single_ead = single_ead)


@app.route('/fetchonebmd/<int:slno>')
def fetchonebmd(slno):
    user = get_current_user()
    db = get_database()
    bmd_cur = db.execute('select * from billingmasterdata where slno = ?', [slno])
    single_bmd = bmd_cur.fetchone()
    return render_template('updatebillingmasterdata.html', user = user, single_bmd = single_bmd)

@app.route('/fetchonecc/<int:costcodes>')
def fetchonecc(costcodes):
    user = get_current_user()
    db = get_database()
    cc_cur = db.execute('select * from costcode where costcodes = ?', [costcodes])
    single_cc = cc_cur.fetchone()
    return render_template('updatecostcodes.html', user = user, single_cc = single_cc)

@app.route('/fetchallcc')
def fetchallcc():
    user = get_current_user()
    # db = get_database()
    conn = connect_to_database()
    cc_cur = conn.execute('select costcodes from costcode ')
    # single_cc = cc_cur.fetchall()
    # print (single_cc)
    jsonBody= []
    for row in cc_cur:
        jsonBody.append(row[0])
        print(row[0])
    return jsonify(jsonBody)
    # return (json.dumps(single_cc))
    
@app.route('/fetchoneme/<int:slno>')
def fetchoneme(slno):
    user = get_current_user()
    db = get_database()
    me_cur = db.execute('select * from monthlyexp where slno = ?', [slno])
    single_me = me_cur.fetchone()
    return render_template('updatemonthlyexp.html', user = user, single_me = single_me)

@app.route('/fetchoneye/<string:type_y>')
def fetchoneye(type_y):
    user = get_current_user()
    db = get_database()
    ye_cur = db.execute('select * from yearlyexp where type_y = ?', [type_y])
    single_ye = ye_cur.fetchone()
    return render_template('updateyearlyexp.html', user = user, single_ye = single_ye)

@app.route('/fetchonesd/<string:signeddata>')
def fetchonesd(signeddata):
    user = get_current_user()
    db = get_database()
    sd_cur = db.execute('select * from sowdetails where signeddata = ?', [signeddata])
    single_sd = sd_cur.fetchone()
    return render_template('updatesowdetails.html', user = user, single_sd = single_sd)

@app.route('/fetchallsd')
def fetchallsd():
    user = get_current_user()
    # db = get_database()
    conn = connect_to_database()
    cc_cur = conn.execute('select sowdescription from sowdetails')
    # single_cc = cc_cur.fetchall()
    # print (single_cc)
    jsonBody= []
    for row in cc_cur:
        jsonBody.append(row[0])
        print(row[0])
    return jsonify(jsonBody)
    # return (json.dumps(single_cc))

@app.route('/fetchonebd/<int:slno>')
def fetchonebd(slno):
    user = get_current_user()
    db = get_database()
    bd_cur = db.execute('select * from billingdetails where slno = ?', [slno])
    single_bd = bd_cur.fetchone()
    return render_template('updatebillingdetails.html', user = user, single_bd = single_bd)

@app.route('/fetchallmer')
def fetchallmer():
    user = get_current_user()
    # db = get_database()
    conn = connect_to_database()
    mer_cur = conn.execute('select sum(amount_m) from monthlyexp ')
    # single_cc = cc_cur.fetchall()
    # print (single_cc)
    jsonBody= []
    for row in mer_cur:
        jsonBody.append(row[0])
        print(row[0])
    return jsonify(jsonBody)
    # return (json.dumps(single_cc))

@app.route('/fetchallyer')
def fetchallyer():
    user = get_current_user()
    # db = get_database()
    conn = connect_to_database()
    yer_cur = conn.execute('select sum(amount_y) from yearlyexp ')
    # single_cc = cc_cur.fetchall()
    # print (single_cc)
    jsonBody= []
    for row in yer_cur:
        jsonBody.append(row[0])
        print(row[0])
    return jsonify(jsonBody)
    # return (json.dumps(single_cc))

@app.route('/updateemployee' , methods = ["POST", "GET"])
def updateemployee():
    user = get_current_user()
    if request.method == 'POST':
        slno = request.form['slno']
        empid = request.form['empid']
        name = request.form['name']
        location = request.form['location']
        startdate = request.form['startdate']
        db = get_database()
        db.execute('update empmasterdata set empid=?, name = ?, location =? , startdate = ? where slno =?', [empid, name, location, startdate, slno])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateemployee.html', user = user)

@app.route('/updateemployeeadddetails' , methods = ["POST", "GET"])
def updateemployeeadddetails():
    user = get_current_user()
    if request.method == 'POST':
        slno = request.form['slno']
        empid = request.form['empid']
        name = request.form['name']
        ctc = request.form['ctc']
        billable = request.form['billable']
        costcodes = request.form['costcodes']
        db = get_database()
        db.execute('update empadddetails set empid=?, name = ?, ctc = ?, billable = ?, costcodes = ? where slno =?', [empid,name, ctc, billable, costcodes, slno])
        db.commit()
        return redirect(url_for('employeeadddetails'))
    return render_template('updateemployeeadddetails.html', user = user)

@app.route('/updatebillingmasterdata' , methods = ["POST", "GET"])
def updatebillingmasterdata():
    user = get_current_user()
    if request.method == 'POST':
        slno = request.form['slno']
        empid = request.form['empid']
        name = request.form['name']
        clientname = request.form['clientname']
        startdate = request.form['startdate']
        billrate = request.form['billrate']
        db = get_database()
        db.execute('update billingmasterdata set empid=?, name = ?, clientname = ?, startdate = ?, billrate = ? where slno = ?', [empid, name, clientname, startdate, billrate, slno])
        db.commit()
        return redirect(url_for('billingmasterdata'))
    return render_template('updatebillingmasterdata.html', user = user)

@app.route('/updatecostcodes' , methods = ["POST", "GET"])
def updatecostcodes():
    user = get_current_user()
    if request.method == 'POST':
        slno = request.form['slno']
        department = request.form['department']
        costcodes = request.form['costcodes']
        db = get_database()
        db.execute('update costcode set department = ?, costcodes = ? where slno =?', [department, costcodes, slno])
        db.commit()
        return redirect(url_for('costcodes'))
    return render_template('updatecostcodes.html', user = user)

@app.route('/updatemonthlyexp' , methods = ["POST", "GET"])
def updatemonthlyexp():
    user = get_current_user()
    if request.method == 'POST':

        slno = request.form['slno']
        type_m = request.form['type_m']
        description_m = request.form['description_m']
        amount_m = request.form['amount_m']
        db = get_database()
        db.execute('update monthlyexp set type_m = ?,description_m = ?, amount_m = ? where slno =?', [ type_m, description_m, amount_m, slno])
        db.commit()
        return redirect(url_for('monthlyexpenses'))
    return render_template('updatemonthlyexp.html', user = user)

@app.route('/updateyearlyexp' , methods = ["POST", "GET"])
def updateyearlyexp():
    user = get_current_user()
    if request.method == 'POST':
        slno = request.form['slno']
        type_y = request.form['type_y']
        description_y = request.form['description_y']
        amount_y = request.form['amount_y']
        db = get_database()
        db.execute('update yearlyexp set description_y = ?, amount_y = ?, type_y = ? where slno =?', [description_y, amount_y, type_y, slno])
        db.commit()
        return redirect(url_for('yearlyexpenses'))
    return render_template('updateyearlyexp.html', user = user)

@app.route('/updatesowdetails' , methods = ["POST", "GET"])
def updatesowdetails():
    user = get_current_user()
    if request.method == 'POST':
        slno = request.form['slno']
        signeddata = request.form['signeddata']
        clientname = request.form['clientname']
        sowdescription = request.form['sowdescription']
        year = request.form['year']
        sowamount = request.form['sowamount']
        db = get_database()
        db.execute('update sowdetails set clientname = ?,signeddata =?, sowdescription = ?,sowamount =?, year=? where slno = ?', [clientname,signeddata, sowdescription, sowamount, year, slno])
        db.commit()
        return redirect(url_for('sowdetails'))
    return render_template('updatesowdetails.html', user = user)

@app.route('/updatebillingdetails', methods = ["POST", "GET"])
def updatebillingdetails():
    user = get_current_user()
    if request.method == "POST":
        slno = request.form['slno']
        empid = request.form['empid']
        name = request.form['name']
        month = request.form['month']
        amount = request.form['amount']
        year = request.form['year']
        sowdescription = request.form['sowdescription']
        noofdays = request.form['noofdays']
        noofhours = request.form['noofhours']
        db = get_database()
        db.execute('update billingdetails set empid =?, name = ?, month = ?, amount = ?, year = ?, sowdescription = ?, noofdays = ?, noofhours = ? where slno =?', [empid, name, month, amount, year, sowdescription, noofdays, noofhours, slno])
        db.commit()
        return redirect(url_for('billingdetails'))
    return render_template('addnewbillingdetails.html', user = user)

@app.route('/deleteemp/<int:slno>', methods = ["GET", "POST"])
def deleteemp(slno):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from empmasterdata where slno = ?', [slno])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user = user)

@app.route('/deleteemployeeadddetails/<int:slno>', methods = ["GET", "POST"])
def deleteemployeeadddetails(slno):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from empadddetails where slno = ?', [slno])
        db.commit()
        return redirect(url_for('employeeadddetails'))
    return render_template('employeeadddetails.html', user = user)

@app.route('/deletebillingmasterdata/<int:slno>', methods = ["GET", "POST"])
def deletebillingmasterdata(slno):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from billingmasterdata where slno = ?', [slno])
        db.commit()
        return redirect(url_for('billingmasterdata'))
    return render_template('billingmasterdata.html', user = user)

@app.route('/deletecostcodes/<int:costcodes>', methods = ["GET", "POST"])
def deletecostcodes(costcodes):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from costcode where costcodes = ?', [costcodes])
        db.commit()
        return redirect(url_for('costcodes'))
    return render_template('costcodes.html', user = user)

@app.route('/deletemonthlyexp/<int:slno>', methods = ["GET", "POST"])
def deletemonthlyexp(slno):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from monthlyexp where slno = ?', [slno])
        db.commit()
        return redirect(url_for('monthlyexpenses'))
    return render_template('monthlyexpenses.html', user = user)

@app.route('/deleteyearlyexp/<string:type_y>', methods = ["GET", "POST"])
def deleteyearlyexp(type_y):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from yearlyexp where type_y = ?', [type_y])
        db.commit()
        return redirect(url_for('yearlyexpenses'))
    return render_template('yearlyexpenses.html', user = user)

@app.route('/deletesowdetails/<string:signeddata>', methods = ["GET", "POST"])
def deletesowdetails(signeddata):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from sowdetails where signeddata = ?', [signeddata])
        db.commit()
        return redirect(url_for('sowdetails'))
    return render_template('sowdetails.html', user = user)

@app.route('/deletebillingdetails/<int:slno>', methods = ["GET", "POST"])
def deletebillingdetails(slno):
    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from billingdetails where slno = ?', [slno])
        db.commit()
        return redirect(url_for('billingdetails'))
    return render_template('billingdetails.html', user = user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug = True)