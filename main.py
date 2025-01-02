import pymysql
import requests
import json
import bcrypt
import uuid
import smtplib
import random
import string
import traceback
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import Flask, Response, render_template, request, send_file, url_for, session,redirect,flash
from fpdf import FPDF

otp=0
order_id=""
# appointment_id=0
pdf_name=""
appointment_id=10101012
flag=False

# def generate_appointment_id():
#     # Generate a unique ID using UUID (Universally Unique Identifier)
#     global appointment_id
#     # unique_id = uuid.uuid4()
#     appointment_id +=1
#     # # Get the current timestamp
#     # current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
#     # # Combine the timestamp and unique ID to create the appointment ID
#     # appointment_id = f"Appt_{current_time}_{unique_id}"
    
#     return appointment_id

def get_current_appointment_id():
    try:
        with open("appointment_id.txt", "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        # If the file doesn't exist or is empty, start from 1001
        return 1001

# Define a function to update and persist the current appointment ID to a file
def update_current_appointment_id(current_id):
    with open("appointment_id.txt", "w") as file:
        file.write(str(current_id))

def generate_appointment_id():
    # Get the current appointment ID from the file
    current_appointment_id = get_current_appointment_id()

    # Generate the appointment ID
    appointment_id = current_appointment_id

    # Increment the current appointment ID for the next call
    current_appointment_id += 1

    # Update and persist the new current appointment ID to the file
    update_current_appointment_id(current_appointment_id)

    return appointment_id

# Generate a random OTP
def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Send OTP via email
def send_otp_via_email(ab):
    global otp
 
  
    otp = generate_otp()

    subject = 'Your OTP'
    body = f'Your OTP is: {otp}'


    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain')) 

   
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(f'OTP sent successfully to {receiver_email}')
        return otp
    except Exception as e:
        print(f'Error: {str(e)}')
        return None

#khatm hogaya bhai sara



class PDF(FPDF):
    # def header(self):
    #     self.image('header.png', 10, 8, 190)  # Add a header image
    # #     self.set_font('Arial', 'B', 12)
    # #     self.cell(0, 10, 'Appointment Details', 0, 1, 'C')

    # def chapter_title(self, title):
    #     self.set_font('Arial', 'B', 16)
    #     self.set_fill_color(200, 200, 200)  # Gray background color
    #     self.cell(0, 12, title, 0, 1, 'L')
    #     self.ln(10)

   
    # def chapter_title1(self, title):
    #     self.set_font('Arial', 'B', 10)
    #     self.set_fill_color(200, 200, 200)  # Gray background color
    #     self.cell(0, 12, title, 0, 1, 'L')
    #     self.ln(10)

   

    # def chapter_body(self, body):
    #     self.set_font('Arial', '', 12)
    #     self.multi_cell(0, 10, body)
    #     self.ln()

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.set_fill_color(0, 123, 255)  # Blue background color
        self.set_text_color(0, 0, 0) # White text color
        self.cell(0, 12, title, 0, 1, 'L', 1)  # Add a border
        self.ln(10)

    def chapter_title1(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 200, 200)  # Gray background color
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln(10)


def create_invoice(patient_name, appointment_id, payment_status, total_amount, payment_id, hospital_name, address_hospital,doctor_name, gender, appointment_date, appointment_schedule, phone_number, patient_age):
    pdf = PDF()
    pdf.add_page()
    global pdf_name

    # Title
    pdf.chapter_title('Appointment Receipt')

    pdf.chapter_title1('Patient Name:' + patient_name)
    pdf.chapter_title1('Invoice Number:' + payment_status)
    pdf.chapter_title1('Appointment Number:' + str(appointment_id))
    pdf.chapter_title1('Payment ID:' + str(payment_id))
    pdf.chapter_title1('Hospital Name:' + str(hospital_name))
    pdf.chapter_title1('Hospital Address:' + str(address_hospital))
    pdf.chapter_title1('Doctor Name:' + str(doctor_name))
    pdf.chapter_title1('Gender:' + gender)
    pdf.chapter_title1('Appointment Date:' + appointment_date)
    pdf.chapter_title1('Appointment Schedule:' + appointment_schedule)
    pdf.chapter_title1('Phone Number:' + str(phone_number))
    pdf.chapter_title1('Patient Age:' + str(patient_age))
    pdf.ln(5)

    # Total amount
    pdf.chapter_title(f"Total Amount:Rs{total_amount:.2f}")
    name = "yash"

    # Output to a PDF file
    pdf_name=(f"{patient_name}_appointment.pdf")
    # pdf_path = "C:\\Users\\asus\\OneDrive\\Desktop\\fp\\static" + pdf_name 
    pdf.output(f"{patient_name}_appointment.pdf")
    # pdf.output(pdf_path )
    
    return "pdf generate successfully"

# if __name__ == '__main__':
    # pt_firstname=session.get('pt_firstname')
    # doctor_name1=session.get('doctor_name1')
    # pt_email=session.get('pt_email')
    # pt_phone=session.get('pt_phone')
    # pt_gender=session.get('pt_gender')
    # DOB=session.get('DOB')
    # Doctor_id=session.get('Doctor_id')
    # date=session.get('date')
    # app_time=session.get('app_time')
    # pt_name=session.get('pt_name')
    # address_hspital=session.get('address_hspital')
    # payment="successfull"
    
    # patient_name = session.get('pt_firstname')
    # appointment_number = "INV12345"
    # payment_status = "successful"
    # paid_amount = 500
    # payment_id = 1531
    # hospital_name = session.get('address_hspital')
    # doctor_name = session.get('doctor_name1')
    # gender = session.get('pt_gender')
    # appointment_date = session.get('date')
    # appointment_schedule = session.get('app_time')
    # phone_number = session.get('pt_phone')
    # patient_age = session.get('DOB')
    # patient_email=session.get('pt_email')

    # create_invoice(patient_name, appointment_number, payment_status, paid_amount, payment_id, hospital_name, doctor_name, gender, appointment_date, appointment_schedule, phone_number, patient_age)




   
 
def predict(a):
    # Load the CSV data into a Pandas DataFrame
    heart_data = pd.read_csv("heart.csv") 

    # Display basic data information
    # print("First five rows of dataset:")
    # print(heart_data.head())
    # print("\nLast five rows of dataset:")
    # print(heart_data.tail())
    # print("\nData shape:")
    # print(heart_data.shape)
    # print("\nMissing values:")
    # print(heart_data.isnull().sum())
    # print("\nStatistical measures:")
    # print(heart_data.describe())
    # print("\nDistribution of the target variable:")
    # print(heart_data['target'].value_counts())


    X = heart_data.drop(columns='target', axis=1)
    Y = heart_data['target']

  
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

    model = LogisticRegression()
    model.fit(X_train, Y_train)

   
    X_train_prediction = model.predict(X_train)
    training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
    print("Accuracy on training data:", training_data_accuracy)

    X_test_prediction = model.predict(X_test)
    test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
    print("Accuracy on test data:", test_data_accuracy)


    input_data_as_numpyarray = np.array(a,dtype=float).reshape(1, -1)
    prediction = model.predict(input_data_as_numpyarray)

    if prediction[0] == 0:
        return "The person does not of have symptoms  heart disease."
    else:
        return "The person has symptoms of  heart disease."


app = Flask(__name__)
app.secret_key = 'yash'

 
cursor = conn.cursor()

@app.route('/userlogin')
def userregister():
    global flag
    flag=False
    return render_template('userlogin.html')

@app.route('/userlogin_otp')
def userlogin_otp():
    return render_template('userlogin_otp.html')

@app.route('/doctorlogin_otp')
def doctorlogin_otp():
    return render_template('doctorlogin_otp.html')


@app.route('/userregister')
def userlogin():
    return render_template('userregister.html')

@app.route('/doctorlogin')
def doctorlogin():
    return render_template('doctorlogin.html')

@app.route('/doctorregister')
def doctorregister():
    return  render_template('doctorregister.html')

@app.route('/getappoinment')
def getappoinment():
    return render_template('getappoinment.html')


@app.route('/bookAppointment', methods=['POST','GET'])
def bookAppointment():
    global flag
    flag=False
    return render_template('appoimentdetail.html')
    # return redirect('/appointmentdeatil')
    
@app.route('/download')
def download_file():
    file_path = f'C:/Users/asus/OneDrive/Desktop/fp/{pdf_name}'
    return send_file(file_path, as_attachment=True, download_name=f'{pdf_name}')

@app.route('/success' , methods=['POST','GET'])
def success():
        global flag
        pt_firstname=session.get('pt_firstname')
        doctor_name=session.get('doctor_name')
        pt_email=session.get('pt_email')
        pt_phone=session.get('pt_phone')
        pt_gender=session.get('pt_gender')
        DOB=session.get('DOB')
        Doctor_id=session.get('Doctor_id')
        date=session.get('date')
        app_time=session.get('app_time')
        pt_name=session.get('pt_name')
        pt_name1=session.get('pt_firstname')+' '+session.get('pt_lastname')
        address_hspital=session.get('address_hspital')
        payment="successfull"
        address_hospital=session.get('address_hospital')
        
        patient_name = session.get('pt_firstname')
        appointment_number = session.get('app_id')
        payment_status = "successful"
        paid_amount = 500
        payment_id = 1531
        hospital = session.get('hospital')
        doctor_name = session.get('doctor_name1')
        gender = session.get('pt_gender')
        appointment_date = session.get('date')
        appointment_schedule = session.get('app_time')
        phone_number = session.get('pt_phone')
        patient_age = session.get('DOB')
        patient_email=session.get('pt_email')

        
        app_id1=generate_appointment_id()
        session['app_id']=app_id1
        if(flag==False):
            if(app_id1 is not None):
                if send_details_via_email():
                    if create_invoice(pt_name, app_id1, payment_status, paid_amount, payment_id, hospital,address_hospital ,doctor_name, gender, appointment_date, appointment_schedule, phone_number, patient_age):
                
                        if cursor.execute("INSERT INTO patient_appointment (patient_name, patient_age, patient_no, doctor_name, appointment_date, appointment_schedule, payment_status, patient_gender,appointment_id) VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s)",
                                        (pt_name, DOB, pt_phone, doctor_name, date, app_time, payment, pt_gender,app_id1)):
                            conn.commit()
                            flag=session['flag']=True
                            return render_template('paymentdetail.html', pt_name=pt_name, Dr_id=Doctor_id,appointment_id= app_id1,Dr_name=doctor_name,Appoinment_date=date, hospital_address=address_hspital, Appoinment_time=app_time,pdf_name=pdf_name)
            else:
                return render_template("detailconfirm.html")
        else:
            flash("you booked appointment already if you want to book another click book another button")
            return render_template("detailconfirm.html")

    
    
# @app.route('/pay')
# def pay():
#     try:
#         payment()
#         # global pt_name
#         # pt_name=session.get('pt_name')
#         pt_name=session.get('pt_name')
#         email_pt=session.get('pt_email')
#         contact_pt=session.get('pt_phone')
#         print(pt_name)
#         print(email_pt)
#         print(contact_pt)
#         return render_template('pay.html')
            
#     except Exception as e:
#         traceback.print_exc()
#         print(e)
#         return redirect("/detailconfirm")
        
        
        
@app.route('/appointmentdeatil', methods=['POST','GET'])
def appointmentdeatil():
    try:
        session['pt_firstname'] = request.form.get('firstname')
        session['pt_lastname'] = request.form.get('lastname')
        session['pt_email'] = request.form.get('email')
        session['pt_phone'] = request.form.get('phone')
        session['pt_gender'] = request.form.get('gender')
        session['DOB'] = request.form.get('DOB')
        session['Doctor_id'] = request.form.get('Doctor_id')
        session['date'] = request.form.get('date')
        session['app_time'] = request.form.get('time')
        session['pt_name']=session.get('pt_firstname')+' '+session.get('pt_lastname')
        
        pt_firstname=session.get('pt_firstname')
        pt_lastname=session.get('pt_lastname')
        pt_email=session.get('pt_email')
        pt_phone=session.get('pt_phone')
        pt_gender=session.get('pt_gender')
        DOB=session.get('DOB')
        Doctor_id=session.get('Doctor_id')
        date=session.get('date')
        app_time=session.get('app_time')
        pt_name=session.get('pt_name')
        
        

        if cursor.execute("INSERT INTO appointment_info (paient_name, patient_email, phone, pt_gender, dob, appointment_date, app_time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (pt_name, pt_email, pt_phone, pt_gender, DOB, date, app_time)):
            conn.commit()
            print("data insert successfully")
            return redirect('/detailconfirm')
        else:
            return render_template('appoimentdetail.html')
            

    except Exception as e:
        print(e)
        traceback.print_exc()

    

@app.route('/detailconfirm' ,methods=['POST','GET'])
def detailconfirm():
    
    
    pt_firstname=session.get('pt_firstname')
    head_name=session.get('pt_firstname')
    pt_lastname=session.get('pt_lastname')
    pt_email=session.get('pt_email')
    pt_phone=session.get('pt_phone')
    pt_gender=session.get('pt_gender')
    DOB=session.get('DOB')
    date=session.get('date')
    app_time=session.get('app_time')
    pt_name=session.get('pt_name')
    Doctor_id=session.get('Doctor_id')
    
    
    # session['payment_id']=request.form.get('payment_id')
    
    
    if cursor.execute("SELECT fullname FROM login_data_doctor WHERE id = %s ",(Doctor_id)):
        doctors = cursor.fetchone()
    if cursor.execute("SELECT hospital FROM login_data_doctor WHERE id = %s ",(Doctor_id)):
        hospital = cursor.fetchone()
    if cursor.execute("SELECT address FROM login_data_doctor WHERE id = %s ",(Doctor_id)):
        address = cursor.fetchone()
        
        address = address[0]
        doctors=doctors[0]
        hospital=hospital[0]
        
        
        
    doctor_name=doctors
    session['doctor_name']=doctors
    session['address_hospital']=address
    session['hospital']=hospital
    print(doctor_name)
    
    

    return render_template("detailconfirm.html",Address=address,hospital=hospital ,doctor_name=doctor_name, head_name=head_name,pt_firstname=pt_firstname, pt_lastname=pt_lastname, pt_email=pt_email, pt_phone=pt_phone, DOB=DOB, date=date, app_time=app_time, pt_gender=pt_gender)


@app.route('/')
def home():
    return render_template('homepage.html')


# @app.route('/searchdoctor' ,methods=['POST','GET'])
# def searchdoctor():
#     try:
#         specialty=request.form.get('specialty')
#         City=request.form.get('City')
        
#         session['city']=City
#         session['specialty']=specialty
#         print(specialty)
#         print(City)
        
#         if cursor.execute("SELECT * FROM login_data_doctor WHERE specialist = %s or city=%s ", (specialty ,City)):
#             return redirect('/doctor_list')
#         else:
#             flash("doctor not found", "failed")
#             return render_template('getappoinment.html')
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
    
    
    
@app.route('/searchdoctor1',methods=['GET', 'POST'])
def searchdoctor():
    
    # specialty=session.get('specialty')
    # city=session.get('city')
    # print(specialty,city,"doctor name")
    
    # user = []
    
    
    # if cursor.execute("SELECT fullname, d_email, d_number, experience, qualification, specialist, city, id FROM login_data_doctor WHERE  city = %s or  specialist= %s", (specialty,city)):
    #     user= cursor.fetchall()
    # print((("SELECT fullname, d_email, d_number, experience, qualification, specialist, city, id FROM login_data_doctor WHERE  city = {} AND  specialist= {}",(specialty,city))))
    # print(user)
    
    
    # heading = ('fullname', 'd_email', 'd_number', 'experience', 'qualification', 'specialist', 'city','id')   
    # data = user

    # return render_template("doctor_list.html", headings=heading, data=data)
    
    try:
        specialty=request.form.get('specialty')
        city=request.form.get('City')
        dr_name=request.form.get('dr_name')

        print(specialty)
        print(dr_name)
        print(city)
        
        user = []
        heading = ('fullname', 'd_email', 'd_number', 'experience', 'qualification', 'specialist', 'city','id')

        cursor.execute("SELECT fullname, d_email, d_number, experience, qualification, specialist, city, id FROM login_data_doctor WHERE specialist = %s and city = %s", (specialty, city))
        doctors = cursor.fetchall()

        if doctors:
            return render_template('doctor_list.html', doctors=doctors, headings=heading, data=doctors)
        else:
            flash("No doctors found for the given specialty and city.", "failed")
            return render_template('getappoinment.html')
    except Exception as e:
        print(e)
        traceback.print_exc()

    
    
    

@app.route('/login_validation', methods=['POST','GET'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    
    if cursor.execute("SELECT * FROM login__data WHERE email = %s", (email,)):
        user = cursor.fetchone()
        hashed_password_from_db = user[4]


        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db):
                # send_otp =send_otp_via_email()
                # if send_otp:
                    session['first_name'] = user[0]
                    session['lastname'] = user[1]
                    return render_template('userhomepage1.html')  
        else:
                flash("password not match", "failed")
                return render_template('userlogin.html')
    else:
        flash("user not found", "failed")
        return render_template('userlogin.html')
    

@app.route('/login_validation_otp', methods=['POST','GET'])
def login_validation_otp():
    email = request.form.get('email')
    
    if cursor.execute("SELECT * FROM login__data WHERE email = %s", (email,)):
        user = cursor.fetchone()
        hashed_password_from_db = user[4]

        send_otp =send_otp_via_email(email)
        if send_otp:
            # return redirect('/otp_verification')
            return render_template('otp.html')  
    else:
        flash("user not found", "failed")
        return render_template('userlogin_otp.html')
        
        
        
@app.route('/login_validation_doctor', methods=['POST','GET'])
def login_validation_doctor():
    email = request.form.get('email')
    password1 = request.form.get('password')

    if cursor.execute("SELECT * FROM login_data_doctor WHERE d_email = %s", (email,)):
        user = cursor.fetchone()
        hashed_password_from_db1 = user[8]

        if bcrypt.checkpw(password1.encode('utf-8'), hashed_password_from_db1):
                # send_otp =send_otp_via_email() 
                # if send_otp:
                    # return render_template('/doctor_home')
                    session['full_name_doctor'] = user[0]
                    session['email_doctor'] = user[1]
                    
                    # fn=session.get('first_name_doctor')
                    # ln=session.get('lastname_doctor')
                    # print(fn,ln)
                    
                    return redirect("/doctor_home")
        else:
            flash("password not match", "failed")
            return render_template('doctorlogin.html')
    else:
        flash("doctor not found", "failed")
        return render_template('doctorlogin.html')
    
    

@app.route('/login_validation_otp_doctor', methods=['POST', 'GET'])
def login_validation_otp_doctor():
    d_email = request.form.get('d_email')

    if cursor.execute("SELECT * FROM login_data_doctor WHERE d_email = %s", (d_email,)):
        user = cursor.fetchone()
        hashed_password_from_db = user[4]

        send_otp = send_otp_via_email(d_email)
        if send_otp:
            return render_template('otp_doctor.html')
        else:
            flash("Failed to send OTP", "failed")
            return render_template('doctorlogin_otp.html')
    else:
        flash("User not found", "failed")
        return render_template('doctorlogin_otp.html')




@app.route('/otp_verification', methods=['POST'])
def verify_otp():
    user_otp=request.form.get('user_otp')
    if(otp== user_otp):
        return render_template('userhomepage1.html')
    else:
        flash("invalid otp", "failed")
        return render_template('otp.html')
    
    
@app.route('/otp_verification_doctor', methods=['POST','GET'])
def verify_otp_doctor():
    doctor_otp=request.form.get('doctor_otp')
    if(otp== doctor_otp):
        return redirect("/doctor_home")
    else:
        flash("invalid otp", "failed")
        return render_template('otp_doctor.html')



@app.route('/add_user', methods=['POST'])
def add_user():
   fname=request.form.get('firstname')
   lname=request.form.get('lastname')    
   email=request.form.get('email')
   mobile=request.form.get('mobile')
   password=request.form.get('password')
   cpassword=request.form.get('confirm')
   gender=request.form.get('gender')
   
   hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

   if hashed_password == bcrypt.hashpw(cpassword.encode('utf-8'), hashed_password):
       
        cursor.execute("INSERT INTO login__data (firstname, lastname, email, mobile_no, password, gender) VALUES (%s, %s, %s, %s, %s, %s)",
                       (fname, lname, email, mobile, hashed_password, gender))
        conn.commit()
        flash("user registered successfully!", "success")
        return render_template('userregister.html')
   else:
        flash("user not registered", "success")
        return render_template('userregister.html')
    
@app.route('/add_doctor', methods=['POST','GET'])
def add_doctor():
    f_name=request.form.get('f_name')
    d_email=request.form.get('d_email')
    d_number=request.form.get('d_number')
    yoe=request.form.get('yoe')
    qualification=request.form.get('qualification')
    specialist=request.form.get('specialist')
    city=request.form.get('city')
    password=request.form.get('password')
    c_pass=request.form.get('c_pass')
    hospital_address=request.form.get('hospital_address')
    hospital_name=request.form.get('hospital_name')
    gender=request.form.get('gender')
    # id = random.randint(100, 999)
    
    d_hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if d_hashed_password == bcrypt.hashpw(c_pass.encode('utf-8'), d_hashed_password):

        cursor.execute("INSERT INTO login_data_doctor (fullname, d_email, d_number, experience, qualification, specialist, city, d_gender, password, hospital, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (f_name, d_email, d_number, yoe, qualification, specialist, city, gender, d_hashed_password, hospital_name, hospital_address))
        conn.commit()
        flash("Doctor registered successfully!", "success")
        return render_template('doctorregister.html')
    else:
        flash("failed to register check password", "failed")
        return render_template('doctorregister.html')


@app.route('/predict_data' , methods=['GET', 'POST'])
def add_patient_data():
    try:
        
        session['name']=session.get('first_name')+' '+session.get('lastname')
        session['age'] =request.form.get('age')
        session['sex'] =request.form.get('gender')
        session['cp']=request.form.get('cp')
        session['trestbps']=request.form.get('trestbps')
        session['chol']=request.form.get('chol')
        session['fbs']=request.form.get('fbs')
        session['restecg']=request.form.get('restecg')
        session['thalach']=request.form.get('thalach')
        session['exang']=request.form.get('exang')
        session['oldpeak']=request.form.get('oldpeak')
        session['slope']=request.form.get('slope')
        session['ca']=request.form.get('ca')
        session['thal']=request.form.get('thal')
        
        # cursor.execute("INSERT INTO patient_data (patient_name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        #                 (name, age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal))
        # conn.commit()
        # cursor.execute("select * from patient_data")
        # user=cursor.fetchone()
        age=session.get('age')
        sex=session.get('sex')
        cp=session.get('cp')
        trestbps=session.get('trestbps')
        chol=session.get('chol')
        fbs=session.get('fbs')
        restecg=session.get('restecg')
        thalach=session.get('thalach')
        exang=session.get('exang')
        oldpeak=session.get('oldpeak')
        slope=session.get('slope')
        ca=session.get('ca')
        thal=session.get('thal')
        
        print(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
        user_data=(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal)
        b=predict(user_data)
        # print(b)
        flash(b)
        return render_template('userhomepage.html')
   
    except Exception as e:
        print(e)
        traceback.print_exc()
        # flash("Failed to predict")
        return render_template('userhomepage.html')
    
    
@app.route('/user_homepage')
def user_homepage():
    return render_template("userhomepage1.html")


@app.route('/doctor_home',methods=['GET', 'POST'])
def doctor_home():
    
    fullname_doctor=session.get('full_name_doctor')
    print(fullname_doctor,"doctor name")
    
    user = []
    
    if cursor.execute ("SELECT * FROM patient_appointment WHERE doctor_name = %s", (fullname_doctor,)):
        user = cursor.fetchall()


    heading = ('patient_name', 'patient_age', 'patient_no', 'doctor_name', 'appointment_date', 'appointment_schedule', 'payment_status','appointment_id','Gender')
    data = user

    return render_template("doctorhomepage1.html", headings=heading, data=data,column=user)

       



if __name__ == "__main__":
    app.run(debug=True)
