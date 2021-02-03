from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

import yaml

app = Flask(__name__)
#congiure db
db=yaml.load(open('db.yaml'))
app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']

mysql= MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        userDetails=request.form
        ID=userDetails['ID']
        Fullname=userDetails['Fullname']
        email=userDetails['email']
        phone=userDetails['phone']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO employee_t (ID,Fullname,email,phone) VALUES(%s,%s,%s,%s)",(ID,Fullname,email,phone))
        mysql.connection.commit()
        cur.close()
        return redirect('/done')
    return render_template('index.html')

    
@app.route('/done')
def done():
    return render_template ('done.html')


@app.route('/delete/<string:ID>',methods =['POST','GET'])
def delete(ID):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM employee_t WHERE ID = {0}'.format(ID))
    mysql.connection.commit()
    cur.close()
    cur=mysql.connection.cursor()
    resultv=cur.execute("select * from employee_t")
    if resultv>-1:
        userDetails=cur.fetchall()
        return render_template('users.html',userDetails=userDetails)
    #return render_template ('users.html')
    

@app.route('/users')
def users():
    cur=mysql.connection.cursor()
    resultv=cur.execute("select * from employee_t")
    if resultv>-1:
        userDetails=cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__=="__main__":
    app.run(debug=True)
