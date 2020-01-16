from models import *

date_format = "%Y-%m-%d"

PATIENTS_FIELDS = \
    [
        dict(
            key='value',
            label='Id пациента',
        ),
        dict(
            key='text',
            label='Фамилия',
        ),

        dict(
            key=f'{Patients.__tablename__}_patient_first_name',
            label='Имя',
        ),

        dict(
            key=f'{Patients.__tablename__}_patient_age',
            label='Возраст',
        ),
    ]

CONSULTANTS_FIELDS = \
    [
        dict(
            key='value',
            label='Id консультанта',
        ),
        dict(
            key='text',
            label='Фамилия',
            

        ),
    ]

DEPARTMENTS_FIELDS = \
    [
        dict(
            key='value',
            label='Id отделения',
        ),
        dict(
            key='text',
            label='Название',

        ),
    ]

DIAGNOSES_FIELDS = \
    [
        dict(
            key='value',
            label='Id диагноза',
        ),
        dict(
            key='text',
            label='Название',
            

        ),
    ]

SICKLIST_FIELDS = \
    [
        dict(
            key=f'{SickLists.__tablename__}_id',
            label='Id',
        ),
        dict(
            key=f'{SickLists.__tablename__}_sl_date',
            label='Дата',
            

        ),
        dict(
            key=f'{Consultants.__tablename__}_consultant_name',
            label='Консультант',
            

        ),
        dict(
            key=f'{SickLists.__tablename__}_number_of_sl',
            label='Номер',
            

        ),
        dict(
            key=f'{SickLists.__tablename__}_number_of_consultation',
            label='№',
            

        ),
        dict(
            key=f'{SickLists.__tablename__}_patient_sur_name',
            label='Пациент',
            

        ),
        dict(
            key=f'{SickLists.__tablename__}_patient_age',
            label='Возраст',
            

        ),
        dict(
            key=f'{SickLists.__tablename__}_correction',
            label='Коррекция',
            

        ),
        dict(
            key=f'{Departments.__tablename__}_department_name',
            label='Отделение',
            

        ),
        dict(
            key=f'{Diagnoses.__tablename__}_diagnose_name',
            label='Диагноз',
            

        ),
        dict(
            key=f'{Reasons.__tablename__}_reason_name',
            label='Причина',
            

        ),
        dict(
            key=f'{SickLists.__tablename__}_comment',
            label='Комментарий',
            

        ),

        dict(
            key='actions',
            label='',

        ),
    ]
