from flask import Flask, jsonify, send_from_directory, Response, request
from flask_cors import CORS
from flask.json import JSONEncoder
from datetime import date
import json
from flask_basicauth import BasicAuth
from datetime import datetime
from settings import *
from werkzeug.serving import run_simple


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.strftime(date_format)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__, static_folder='static/')
app.config['JSON_AS_ASCII'] = False
app.json_encoder = CustomJSONEncoder
CORS(app)
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_USERNAME'] = 'test'
app.config['BASIC_AUTH_PASSWORD'] = 'test'
app.config['BASIC_AUTH_FORCE'] = True


# @basic_auth.required
@app.route('/')
def index():
    return app.send_static_file("index.html")


def get_dict_from_cursor(res):
    return [dict(item.items()) for item in res]


@app.route('/<path:path>')
def static_dist(path):
    return send_from_directory("static/dist", path)


@app.route('/api/consultants')
def consultants():
    session = Session()
    res = session.execute(session.query(Consultants.id.label('value'),
                                        Consultants.consultant_name.label('text')
                                        ).order_by(Consultants.consultant_name)
                          ).fetchall()
    session.close()
    return jsonify({
        'items': get_dict_from_cursor(res),
        'fields': CONSULTANTS_FIELDS
    })


@app.route('/api/patients', methods=['GET', 'POST'])
def patients():
    session = Session()
    if request.method == 'GET':
        res = session.execute(session.query(Patients.id.label('value'),
                                            Patients.patient_sur_name.label('text'),
                                            Patients.patient_age,
                                            ).order_by(Patients.patient_sur_name)).fetchall()
        session.close()

        return jsonify({
            'items': get_dict_from_cursor(res),
            'fields': PATIENTS_FIELDS
        })
    elif request.method == 'POST':
        session.add(Patients(**request.json))
        session.commit()
        # TODO Переписать этот говнокод
        session.close()
        return Response({'result': 'Ok'}, 200)


@app.route('/api/departments')
def departments():
    session = Session()
    res = session.execute(session.query(Departments.id.label('value'),
                                        Departments.department_name.label('text'),
                                        ).order_by(Departments.department_name)).fetchall()
    session.close()
    return jsonify({
        'items': get_dict_from_cursor(res),
        'fields': DEPARTMENTS_FIELDS
    })


@app.route('/api/diagnoses')
def diagnoses():
    session = Session()
    res = session.execute(session.query(Diagnoses.id.label('value'),
                                        Diagnoses.diagnose_name.label('text'),
                                        ).order_by(Diagnoses.diagnose_name)).fetchall()
    session.close()
    return jsonify({
        'items': get_dict_from_cursor(res),
        'fields': DIAGNOSES_FIELDS
    })


@app.route('/api/csv')
def csv():
    session = Session()
    number, correction, consultant, department, diagnose = None, None, None, None, None
    patient, select_date = None, None

    if request.args.get('filter'):
        correction = json.loads(request.args.get('filter')).get('correction')
        number = json.loads(request.args.get('filter')).get('number')
        consultant = json.loads(request.args.get('filter')).get('consultant')
        department = json.loads(request.args.get('filter')).get('department')
        diagnose = json.loads(request.args.get('filter')).get('diagnose')
        patient = json.loads(request.args.get('filter')).get('patient')
        select_date = json.loads(request.args.get('filter')).get('select_date')

    s = session.query(SickLists.id,
                      SickLists.sl_date,
                      Consultants.consultant_name,
                      SickLists.number_of_sl,
                      SickLists.number_of_consultation,
                      Patients.patient_age,
                      Patients.patient_sur_name,
                      SickLists.correction,
                      Departments.department_name,
                      Diagnoses.diagnose_name,
                      Reasons.reason_name,
                      SickLists.comment,
                      ). \
        join(Consultants). \
        join(Patients). \
        join(Departments). \
        join(Diagnoses). \
        join(Reasons)

    if number is not None:
        s = s.filter(SickLists.number_of_consultation == int(number))
    if correction is not None:
        s = s.filter(SickLists.correction == int(correction))
    if consultant is not None:
        s = s.filter(SickLists.consultant_id == int(consultant))
    if department is not None:
        s = s.filter(SickLists.department_id == int(department))
    if diagnose is not None:
        s = s.filter(Diagnoses.diagnose_name.like(f"%{diagnose}%"))
    if patient is not None:
        s = s.filter(Patients.patient_sur_name.like(f"{patient}%"))
    if select_date is not None and select_date != '':
        s = s.filter(SickLists.sl_date == select_date)
    res = session.execute(s.order_by(desc(SickLists.sl_date))).fetchall()

    session.close()
    csv_data = f'{";".join([item.get("label") for item in SICKLIST_FIELDS])}\n'
    for record in get_dict_from_cursor(res):
        csv_data = f'{csv_data}{";".join(f"{item}" for item in record.values())}\n'
    return jsonify({
        'csv_data': csv_data,
    })


@app.route('/api/sick_lists', methods=['GET', 'POST', 'DELETE'])
def sick_lists():
    if request.method == 'GET':

        if request.args.get('currentPage') is not None:
            cur_page = int(request.args.get('currentPage'))
        else:
            cur_page = 1

        per_page = None
        if request.args.get('perPage') is not None:
            per_page = int(request.args.get('perPage'))

        number, correction, consultant, department, diagnose, patient, select_date = None, None, None, None, \
                                                                                     None, None, None
        if request.args.get('filter'):
            correction = json.loads(request.args.get('filter')).get('correction')
            number = json.loads(request.args.get('filter')).get('number')
            consultant = json.loads(request.args.get('filter')).get('consultant')
            department = json.loads(request.args.get('filter')).get('department')
            diagnose = json.loads(request.args.get('filter')).get('diagnose')
            patient = json.loads(request.args.get('filter')).get('patient')
            select_date = json.loads(request.args.get('filter')).get('select_date')
        session = Session()
        s = session.query(SickLists.id,
                          SickLists.sl_date,
                          SickLists.consultant_id,
                          Consultants.consultant_name,
                          SickLists.number_of_sl,
                          SickLists.number_of_consultation,
                          SickLists.patient_id,
                          Patients.patient_age,
                          Patients.patient_sur_name,
                          SickLists.correction,
                          SickLists.department_id,
                          Departments.department_name,
                          SickLists.diagnose_id,
                          Diagnoses.diagnose_name,
                          SickLists.reason_id,
                          Reasons.reason_name,
                          SickLists.comment,
                          ). \
            join(Consultants). \
            join(Patients). \
            join(Departments). \
            join(Diagnoses). \
            join(Reasons)

        if number is not None:
            s = s.filter(SickLists.number_of_consultation == int(number))
        if correction is not None:
            s = s.filter(SickLists.correction == int(correction))
        if consultant is not None:
            s = s.filter(SickLists.consultant_id == int(consultant))
        if department is not None:
            s = s.filter(SickLists.department_id == int(department))
        if diagnose is not None:
            s = s.filter(Diagnoses.diagnose_name.like(f"%{diagnose}%"))
        if patient is not None:
            s = s.filter(Patients.patient_sur_name.like(f"{patient}%"))
        if select_date is not None and select_date != '':
            s = s.filter(SickLists.sl_date == select_date)
        res = session.execute(s.order_by(desc(SickLists.sl_date))).fetchall()
        total_rows = len(res)
        if cur_page is not None and per_page is not None:
            res = res[(cur_page - 1) * per_page: cur_page * per_page]
        session.close()
        return jsonify({
            'items': get_dict_from_cursor(res),
            'fields': SICKLIST_FIELDS,
            'totalRows': total_rows
        })
    elif request.method == 'POST':
        session = Session()
        data = request.json
        # TODO Переписать этот говнокод
        column_names = SickLists.__table__.columns.keys()
        record = {}
        for key in column_names:
            value = data.get(f'{SickLists.__tablename__}_{key}')
            if value:
                record.update({key: value})
        record.update(sl_date=datetime.strptime(record.get('sl_date'), date_format).date())
        record.pop('id')
        session.add(SickLists(**record))
        session.commit()
        # TODO Переписать этот говнокод
        session.close()
        return Response({'result': 'Ok'}, 200)
    elif request.method == 'DELETE':
        session = Session()
        session.query(SickLists).filter(SickLists.id == request.json.get('id')).delete()
        session.commit()
        session.close()
        return Response({'result': 'Ok'}, 200)


if __name__ == '__main__':
    run_simple(hostname='localhost',
               port=5000,
               application=app,
               use_reloader=True,
               use_debugger=True
               )
