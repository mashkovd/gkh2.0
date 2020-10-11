from flask import Flask, jsonify, send_from_directory, Response, request
from flask_cors import CORS
from flask.json import JSONEncoder
from datetime import date
import json
from flask_basicauth import BasicAuth
from datetime import datetime
from settings import *
from werkzeug.serving import run_simple
from contextlib import contextmanager


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as err:
        session.rollback()
        print(err)
        raise
    finally:
        session.close()


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
app.config['BASIC_AUTH_USERNAME'] = 'kurilenko'
app.config['BASIC_AUTH_PASSWORD'] = '12345'
app.config['BASIC_AUTH_FORCE'] = True


def get_dict_from_cursor(res):
    return [dict(item.items()) for item in res]


@basic_auth.required
@app.route('/')
def index():
    return app.send_static_file("index.html")


@basic_auth.required
@app.route('/dist/<path:path>')
def static_dist(path):
    return send_from_directory("static/dist", path)


@basic_auth.required
@app.route('/api/consultants')
def consultants():
    with session_scope() as session:
        res = session.execute(session.query(Consultants.id.label('value'),
                                            Consultants.consultant_name.label('text')
                                            ).order_by(Consultants.consultant_name)
                              ).fetchall()

    return jsonify({
        'items': get_dict_from_cursor(res),
        'fields': CONSULTANTS_FIELDS
    })


@basic_auth.required
@app.route('/api/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'GET':
        with session_scope() as session:
            res = session.execute(session.query(Patients.id.label('value'),
                                                Patients.patient_sur_name.label('text'),
                                                Patients.patient_age,
                                                ).order_by(Patients.patient_sur_name)).fetchall()

            return jsonify({
                'items': get_dict_from_cursor(res),
                'fields': PATIENTS_FIELDS
            })

    elif request.method == 'POST':
        with session_scope() as session:
            session.add(Patients(**request.json))

        return Response({'result': 'Ok'}, 200)


@basic_auth.required
@app.route('/api/departments', methods=['GET', 'POST'])
def departments():
    if request.method == 'GET':
        with session_scope() as session:
            res = session.execute(session.query(Departments.id.label('value'),
                                                Departments.department_name.label('text'),
                                                ).order_by(Departments.department_name)).fetchall()

        return jsonify({
            'items': get_dict_from_cursor(res),
            'fields': DEPARTMENTS_FIELDS
        })


    elif request.method == 'POST':
        with session_scope() as session:
            session.add(Departments(**request.json))

        return Response({'result': 'Ok'}, 200)


@basic_auth.required
@app.route('/api/diagnoses', methods=['GET', 'POST'])
def diagnoses():
    if request.method == 'GET':
        with session_scope() as session:
            res = session.execute(session.query(Diagnoses.id.label('value'),
                                                Diagnoses.diagnose_name.label('text'),
                                                ).order_by(Diagnoses.diagnose_name)).fetchall()

            return jsonify({
                'items': get_dict_from_cursor(res),
                'fields': DIAGNOSES_FIELDS
            })
    elif request.method == 'POST':
        with session_scope() as session:
            session.add(Diagnoses(**request.json))

            return Response({'result': 'Ok'}, 200)


@basic_auth.required
@app.route('/api/csv')
def csv():
    with session_scope() as session:
        number, correction, consultant, department, diagnose = None, None, None, None, None
        patient, select_date = None, None

        _filter = request.args.get('filter')
        if _filter:
            correction = json.loads(_filter).get('correction')
            number = json.loads(_filter).get('number')
            consultant = json.loads(_filter).get('consultant')
            department = json.loads(_filter).get('department')
            diagnose = json.loads(_filter).get('diagnose')
            patient = json.loads(_filter).get('patient')
            select_date = json.loads(_filter).get('select_date')

        s = session.query(SickLists.id,
                          SickLists.sl_date,
                          Consultants.consultant_name,
                          SickLists.number_of_sl,
                          SickLists.number_of_consultation,
                          SickLists.patient_age,
                          SickLists.patient_sur_name,
                          SickLists.correction,
                          Departments.department_name,
                          Diagnoses.diagnose_name,
                          Reasons.reason_name,
                          SickLists.comment,
                          ). \
            join(Consultants). \
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
            s = s.filter(SickLists.patient_sur_name.like(f"{patient}%"))
        if select_date is not None and select_date != '':
            s = s.filter(SickLists.sl_date == select_date)
        res = session.execute(s.order_by(desc(SickLists.sl_date))).fetchall()

        csv_data = f'{";".join([item.get("label") for item in SICKLIST_FIELDS])}\n'
        for record in get_dict_from_cursor(res):
            csv_data = f'{csv_data}{";".join(f"{item}" for item in record.values())}\n'
        return jsonify({
            'csv_data': csv_data,
        })


@basic_auth.required
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
            number_of_sl = json.loads(request.args.get('filter')).get('number_of_sl')
        with session_scope() as session:
            s = session.query(SickLists.id,
                              SickLists.sl_date,
                              SickLists.consultant_id,
                              Consultants.consultant_name,
                              SickLists.number_of_sl,
                              SickLists.number_of_consultation,
                              # SickLists.patient_id,
                              SickLists.patient_age,
                              SickLists.patient_sur_name,
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
                s = s.filter(SickLists.patient_sur_name.like(f"{patient}%"))
            if select_date is not None and select_date != '':
                s = s.filter(SickLists.sl_date == select_date)
            if number_of_sl:
                s = s.filter(SickLists.number_of_sl == int(number_of_sl))

            res = session.execute(s.order_by(desc(SickLists.sl_date))).fetchall()
            total_rows = len(res)
            if cur_page is not None and per_page is not None:
                res = res[(cur_page - 1) * per_page: cur_page * per_page]

            return jsonify({
                'items': get_dict_from_cursor(res),
                'fields': SICKLIST_FIELDS,
                'totalRows': total_rows
            })
    elif request.method == 'POST':
        with session_scope() as session:
            data = request.json

            column_names = SickLists.__table__.columns.keys()
            record = {}
            for key in column_names:
                value = data.get(f'{SickLists.__tablename__}_{key}')
                if value:
                    record.update({key: value})
            record.update(sl_date=datetime.strptime(record.get('sl_date'), date_format).date())
            if record.get('id'):
                record.pop('id')
            session.add(SickLists(**record))

            return Response({'result': 'Ok'}, 200)
    elif request.method == 'DELETE':
        with session_scope() as session:
            session.query(SickLists).filter(SickLists.id == request.json.get('id')).delete()

            return Response({'result': 'Ok'}, 200)


if __name__ == '__main__':
    run_simple(hostname='localhost',
               port=5000,
               application=app,
               use_reloader=True,
               use_debugger=True
               )
