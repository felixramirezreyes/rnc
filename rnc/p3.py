# -*- coding:utf-8 -*-
# Se agrega esta linea de comentario

import time, os, sys
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, String, Integer, create_engine
from sqlalchemy import DefaultClause, Sequence, UniqueConstraint
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
metadata = Base.metadata
session = scoped_session(sessionmaker())
engine = None

rncs = []
archivo_rncs_txt = ''


class RNC2(Base):
    __tablename__ = 'RNC2'
    # __table_args__ = {'extend_existing': True}
    RNC = Column(String(11), primary_key=True)
    Razon_Social = Column(String(80))
    Nombre_Comercial = Column(String(60))
    Tipo_Negocio = Column(String(60))
    Direccion_Calle = Column(String(60))
    Direccion_Numero = Column(String(50))
    Direccion_Sector = Column(String(60))
    Telefono = Column(String(15))
    Fecha_Ingreso = Column(Date(), DefaultClause('1970-01-01'))
    Estatus = Column(String(20), default='ACTIVO')
    Tipo_Regimen = Column(String(25))
    SecID = Column(Integer, autoincrement=True, primary_key=True)


# Function para inicializar la base de datos
def init_db():
    global engine
    db_uri = 'mysql://felix:felix@localhost:3306/testdb'
    engine = create_engine(db_uri)
    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    print('Conectado a -> %s - %s' % ('localhost', 'testdb'))


def abrir_archivo():
    global rncs

    with open(archivo_rncs_txt, 'r') as arch_rncs:
        datos = arch_rncs.read().split('\n')

    hora_i = time.time()

    rncs = [(r.split('|')[0], r.split('|')[1], r.split('|')[2],
             r.split('|')[3], r.split('|')[4], r.split('|')[5],
             r.split('|')[6], r.split('|')[7], r.split('|')[8],
             r.split('|')[9], r.split('|')[10]) for r in datos if len(r) > 0]

    tiempo = time.time() - hora_i
    datos = None  # Liberar menoria

    print('Tiempo en creando diccionario: {:.2f} segundos'.format(tiempo))


# Iniciar SQLAlchemy Core
# def insertar_datos(rncs):
def insertar_datos():
    global rncs
    hora_i = time.time()

    engine.execute(RNC2.__table__.insert(),
                   [dict(RNC='{}'.format(rnc),
                         Razon_Social='{}'.format(social),
                         Nombre_Comercial='{}'.format(comercial),
                         Tipo_Negocio='{}'.format(negocio),
                         Direccion_Calle='{}'.format(calle),
                         Direccion_Numero='{}'.format(numero),
                         Direccion_Sector='{}'.format(sector),
                         Telefono='{}'.format(telef),
                         Fecha_Ingreso=formatfecha(fecha), #'{}'.format(formatfecha(fecha)),
                         Estatus='{}'.format(status),
                         Tipo_Regimen='{}'.format(regimen))
                    for rnc,
                        social,
                        comercial,
                        negocio,
                        calle,
                        numero,
                        sector,
                        telef,
                        fecha,
                        status,
                        regimen in rncs])

    tiempo = time.time() - hora_i
    print('Tiempo insertando en tabla: {:.2f} segundos'.format(tiempo))


def formatfecha(fechastr):
    # if len(fechastr) > 0:
    #     d, m, a = map(int, fechastr.split('/'))
    #     fecha = datetime(a, m, d)
    #     # return datetime(int(a), int(m), int(d))
    # else:
    #     fecha = None

    try:
        d, m, a = map(int, fechastr.split('/'))
        return datetime(a, m, d)
        # return datetime(int(a), int(m), int(d))
    except:
        return None


if __name__ == '__main__':
    archivo_rncs_txt = os.path.join(os.getcwd(), r'tmp\dgii_rnc.txt')

    if not os.path.isfile(archivo_rncs_txt):
        print('Archivo a "procesar" {} no existe').format(archivo_rncs_txt)
        print('Proceso abortado!')
        sys.exit(-1)

    print('Iniciando...')

    init_db()
    abrir_archivo()

    # abrir_archivo= None
    # print('Metodo abrir_archivo - liberado de la memora')

    print('{} Registros a insrtar'.format(len(rncs)))
    insertar_datos()

    print('*Fin!!!')
