from flask import Flask, render_template, flash, request, session, send_file
import pickle
import numpy as np
import mysql.connector
import sys
from keras.preprocessing import image

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewDoctor")
def NewDoctor():
    return render_template('NewDoctor.html')


@app.route("/DoctorLogin")
def DoctorLogin():
    return render_template('DoctorLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/DoctorInfo")
def DoctorInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb  ")
    data = cur.fetchall()
    return render_template('DoctorInfo.html', data=data)


@app.route("/ADRemove")
def ADRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cursor = conn.cursor()
    cursor.execute(
        "delete from doctortb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Doctor  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb  ")
    data = cur.fetchall()
    return render_template('DoctorInfo.html', data=data)


@app.route("/AURemove")
def AURemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cursor = conn.cursor()
    cursor.execute(
        "delete from regtb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('User  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/ADrugInfo")
def ADrugInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  apptb   ")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb   ")
    data1 = cur.fetchall()
    return render_template('ADrugInfo.html', data=data, data1=data1)


@app.route("/newdoct", methods=['GET', 'POST'])
def newdoct():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']
        specialist = request.form['Specialist']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO doctortb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + specialist + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('Doctor  Register Successfully')
        return render_template('DoctorLogin.html')


@app.route("/doctlogin", methods=['GET', 'POST'])
def doctlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['ename'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute("SELECT * from doctortb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('DoctorLogin.html', data=data)
        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('DoctorHome.html', data=data)


@app.route("/DoctorHome")
def DoctorHome():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctortb where username='" + username + "' ")
    data = cur.fetchall()
    return render_template('DoctorHome.html', data=data)


@app.route("/DAppoitmentInfo")
def DAppoitmentInfo():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
    data1 = cur.fetchall()

    return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/Accept")
def Accept():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cursor = conn.cursor()
    cursor.execute(
        "update   apptb set status='Accept' where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Appointment Status  Update  Successfully!')

    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
    data1 = cur.fetchall()

    return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/Reject")
def Reject():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cursor = conn.cursor()
    cursor.execute(
        "update apptb set status='Reject' where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Appointment Status  Update  Successfully!')

    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
    data1 = cur.fetchall()

    return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/AssignDrug")
def AssignDrug():
    id = request.args.get('id')
    st = request.args.get('st')
    session['apid'] = id
    if st == "Accept":
        return render_template('DAssignDrug.html')
    else:
        flash("Appointment Reject")
        username = session['ename']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status='waiting' ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cur = conn.cursor()
        cur.execute("SELECT * FROM apptb where DoctorName='" + username + "' and Status!='waiting' ")
        data1 = cur.fetchall()

        return render_template('DAppoitmentInfo.html', data=data, data1=data1)


@app.route("/drugs", methods=['GET', 'POST'])
def drugs():
    if request.method == 'POST':

        date = request.form['date']
        minfo = request.form['minfo']
        oinfo = request.form['oinfo']
        file = request.files['file']
        file.save("static/upload/" + file.filename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM apptb where  id='" + session['apid'] + "'")
        data = cursor.fetchone()

        if data:
            uname = data[1]
            mobile = data[2]
            email = data[3]
            dname = data[4]

        else:

            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  drugtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dname + "','" +
            minfo + "','" + oinfo + "','" + file.filename + "','" + date + "')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cur = conn.cursor()
        cur.execute("SELECT * FROM drugtb where DoctorName='" + dname + "' ")
        data = cur.fetchall()
        return render_template('DrugsInfo.html', data=data)


@app.route("/DrugsInfo")
def DrugsInfo():
    username = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM drugtb where DoctorName='" + username + "' ")
    data = cur.fetchall()
    return render_template('DrugsInfo.html', data=data)


@app.route('/download')
def download():
    id = request.args.get('id')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM drugtb where  id = '" + str(id) + "'")
    data = cursor.fetchone()
    if data:
        filename = "static\\upload\\" + data[7]

        return send_file(filename, as_attachment=True)

    else:
        return 'Incorrect username / password !'


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)



@app.route("/Heart")
def Heart():
    return render_template('Heart.html')





@app.route("/heart", methods=['GET', 'POST'])
def heart():
    if request.method == 'POST':

        Prescription = ''

        age = request.form['age']
        gender = request.form['gender']
        height = request.form['height']
        weight = request.form['weight']
        aphi = request.form['aphi']
        aplo = request.form['aplo']
        choles = request.form['choles']
        glucose = request.form['glucose']
        smoke = request.form['smoke']
        alcohol = request.form['alcohol']

        slope = request.form['slope']
        ca = request.form['ca']
        thalium = request.form['thalium']

        age = float(age)
        gender = float(gender)
        height = float(height)
        weight = float(weight)
        aphi = float(aphi)
        aplo = float(aplo)
        choles = float(choles)
        glucose = float(glucose)
        smoke = float(smoke)
        alcohol = float(alcohol)
        slope = float(slope)
        ca = float(ca)
        thalium = float(thalium)

        filename = 'Heart/heart-model.pkl'
        classifier = pickle.load(open(filename, 'rb'))

        data = np.array(
            [[age, gender, height, weight, aphi, aplo, choles, glucose, smoke, alcohol, slope, ca, thalium]])
        my_prediction = classifier.predict(data)
        Answer = ''

        if my_prediction == 1:
            Answer = session['uname']  + ' :According to our Calculations, You have Heart disease'

            msg = 'Hello:According to our Calculations, You have Heart disease '
            print('Hello:According to our Calculations, You have Heart disease')
            session['Ans'] = 'Yes'
            session['dtype'] = 'heart'


        else:
            Answer = session['uname'] + ' Congratulations!!  You DON T have Heart disease'

            if (aphi >= 100):

                Answer = session['uname']+  ' Congratulations!!  You DON T have Heart disease May be Heart Disease Will Affected In Future '
                # Prescription = 'Managing Glucose in T1D Once Had But One Treatment'
            else:
                Answer =  session['uname'] + ' Congratulations!!  You DON T have Heart disease'
                # Prescription = "Medications Names:Repaglinide(Prandin)Nateglinide (Starlix)"

            msg = 'Congratulations!!  You DON T have Heart disease'
            print('Congratulations!! You DON T have Heart disease')
            Prescription = 'Nill'
            session['Ans'] = 'No'

        return render_template('Answer1.html', data=Answer)





@app.route("/Lung")
def Lung():
    return render_template('Lung.html')


@app.route("/lung", methods=['GET', 'POST'])
def lung():
    if request.method == 'POST':
        import tensorflow as tf
        import cv2

        file = request.files['file']
        file.save('static/upload/Test.png')
        fname = 'static/upload/Test.png'
        img1 = cv2.imread('static/upload/Test.png')
        dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
        noi = 'static/upload/noi.png'

        cv2.imwrite(noi, dst)

        import warnings
        warnings.filterwarnings('ignore')

        classifierLoad = tf.keras.models.load_model('model.h5')
        test_image = image.load_img('static/upload/Test.png', target_size=(200, 200))
        test_image = np.expand_dims(test_image, axis=0)
        result = classifierLoad.predict(test_image)
        print(result)
        ind = np.argmax(result)
        out = ''
        pre = ""

        if ind == 0:
            out = 'ECG Images of Myocardial Infarction Patients'
            session['Ans'] = 'Yes'
            pre  = 'ECG Images of Myocardial Infarction Patients (240x12=2880)'

        elif ind == 1:
            out = 'ECG Images of Patient that have abnormal heartbeat'
            session['Ans'] = 'Yes'
            pre = 'ECG Images of Myocardial Infarction Patients (240x12=2880)'
        elif ind == 2:
            out = 'ECG Images of Patient that have History of MI'
            session['Ans'] = 'Yes'
            pre = 'ECG Images of Myocardial Infarction Patients (240x12=2880)'
        elif ind == 3:
            out = 'Normal Person'
            session['Ans'] = 'No'
            pre = 'ECG Images of Myocardial Infarction Patients (240x12=2880)'

        return render_template('Answer.html', result=out, org=fname, noi=noi,pre=pre)


@app.route("/ViewDoctor", methods=['GET', 'POST'])
def ViewDoctor():
    if request.method == 'POST':

        ans = session['Ans']

        if ans == 'Yes':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctortb  ")
            data = cur.fetchone()
            if data is None:
                uname = session['uname']

                flash('No Doctor Found!')
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
                cur = conn.cursor()
                cur.execute("SELECT * FROM regtb where username='" + uname + "' ")
                data = cur.fetchall()

                return render_template('UserHome.html', data=data)



            else:
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
                cur = conn.cursor()
                cur.execute("SELECT * FROM doctortb  ")
                data = cur.fetchall()
                return render_template('ViewDoctor.html', data=data)




        else:
            uname = session['uname']
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + uname + "' ")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/Appointment")
def Appointment():
    dname = request.args.get('id')
    session['dname'] = dname
    return render_template('Appointment.html')


@app.route("/appointment", methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        dname = session['dname']
        uname = session['uname']
        date = request.form['date']
        info = request.form['info']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM regtb where  UserNAme='" + uname + "'")
        data = cursor.fetchone()

        if data:
            mobile = data[3]
            email = data[2]


        else:

            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  apptb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + dname + "','" + date + "','" + info + "','waiting')")
        conn.commit()
        conn.close()

        uname = session['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
        data = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
        data1 = cur.fetchall()
        return render_template('UDrugsInfo.html', data=data, data1=data1)


@app.route("/UDrugsInfo")
def UDrugsInfo():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  apptb where username='" + uname + "'  ")
    data = cur.fetchall()
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2heartecgbd')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  drugtb where username='" + uname + "'  ")
    data1 = cur.fetchall()
    return render_template('UDrugsInfo.html', data=data, data1=data1)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
