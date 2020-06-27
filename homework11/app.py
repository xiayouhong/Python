# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 10:51
# @Author  : xyh
from flask import Flask, request, render_template,redirect,url_for
from model.db import session,student,subject,timetable

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET'])
def signin_form():
    return render_template('form.html')

@app.route('/signin', methods=['POST'])
def signin():
    try:
        stu_id = request.form['stu_id']
        password = request.form['password']
        stulist = session.query(student).all()
        for i in stulist:
            if i.id == stu_id and i.password == password:
                return redirect(url_for('choose',stu_id = stu_id , username = i.name))

        return render_template('form.html', message='Bad username or password', stu_id = stu_id)
    except Exception as e:
        print(e)
    # finally:
    #     session.close()


@app.route('/choose/<stu_id>/<username>/',methods=['GET','POST'])
def choose(stu_id,username):
    try:
        subjects = session.query(subject).all()
        stu_timetable = session.query(timetable).filter_by(id=stu_id).one()
        stu_timelist = []
        stu_timelist.append(stu_timetable.mon)
        stu_timelist.append(stu_timetable.tue)
        stu_timelist.append(stu_timetable.wed)
        stu_timelist.append(stu_timetable.thu)
        stu_timelist.append(stu_timetable.fri)
        stu_timelist.append(stu_timetable.sat)
        stu_timelist.append(stu_timetable.sun)
        subjectlists = []
        for i in subjects:
            subjectlist = []
            subjectlist.append(i.id)
            subjectlist.append(i.sub)
            subjectlist.append(i.time)
            subjectlist.append(i.selected)
            if i.sub in stu_timelist:
                subjectlist.append('是')
            else:
                subjectlist.append('否')
            subjectlists.append(subjectlist)

        return render_template('signin-ok.html', stu_id=stu_id, subjects=subjectlists,username=username)

    except Exception as e:
        print(e)


@app.route('/select/<stu_id>/<sub_id>/',methods=['GET','POST'])
def select(stu_id,sub_id):
    try:
        sub = session.query(subject).filter_by(id=sub_id).one()
        stu_timetable = session.query(timetable).filter_by(id=stu_id).one()
        if sub.time == 'mon':
            stu_time = stu_timetable.mon
        elif sub.time == 'tue':
            stu_time = stu_timetable.tue
        elif sub.time == 'wed':
            stu_time = stu_timetable.wed
        elif sub.time == 'thu':
            stu_time = stu_timetable.thu
        elif sub.time == 'fri':
            stu_time = stu_timetable.fri
        elif sub.time == 'sat':
            stu_time = stu_timetable.sat
        else:
            stu_time = stu_timetable.sun

        if not stu_time:
            session.query(timetable).filter_by(id=stu_id).update({sub.time : sub.sub})
            session.commit()
            session.query(subject).filter_by(id=sub_id).update({'selected': sub.selected+1})
            session.commit()
        stu = session.query(student).filter_by(id = stu_id).one()
        return redirect(url_for('choose', stu_id=stu_id,username=stu.name))

    except Exception as e:
        print(e)
@app.route('/notselect/<stu_id>/<sub_id>/',methods=['GET','POST'])
def notselect(stu_id,sub_id):
    try:
        sub = session.query(subject).filter_by(id=sub_id).one()
        stu_timetable = session.query(timetable).filter_by(id=stu_id).one()
        if sub.time == 'mon':
            stu_time = stu_timetable.mon
        elif sub.time == 'tue':
            stu_time = stu_timetable.tue
        elif sub.time == 'wed':
            stu_time = stu_timetable.wed
        elif sub.time == 'thu':
            stu_time = stu_timetable.thu
        elif sub.time == 'fri':
            stu_time = stu_timetable.fri
        elif sub.time == 'sat':
            stu_time = stu_timetable.sat
        else:
            stu_time = stu_timetable.sun
        if stu_time == sub.sub:
            session.query(timetable).filter_by(id=stu_id).update({sub.time: None})
            session.commit()
            session.query(subject).filter_by(id=sub_id).update({'selected': sub.selected - 1})
            session.commit()
        stu = session.query(student).filter_by(id=stu_id).one()
        return redirect(url_for('choose', stu_id=stu_id,username=stu.name))
    except Exception as e:
        print(e)
@app.route('/main/<stu_id>/',methods = ['GET','POST'])
def main(stu_id):
    stu_timetable = session.query(timetable).filter_by(id = stu_id)
    stu = session.query(student).filter_by(id = stu_id).one()
    return  render_template('main.html',username = stu.name, timetable = stu_timetable)
if __name__ == '__main__':
    app.run(debug= 'TRUE')
    # app.run()
    session.close()