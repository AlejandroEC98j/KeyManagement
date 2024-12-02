from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Modelo de Usuario
class Usuario(Base):
    __tablename__ = 'usuario'

    ID_Usuario = Column(Integer, primary_key=True, autoincrement=True)
    Nombre = Column(String(100), nullable=False)
    Correo_Electronico = Column(String(100), unique=True, nullable=False)
    Fecha_Registro = Column(DateTime, default=datetime.utcnow)

    gestores = relationship('GestorContraseñas', back_populates='usuario')
    notificaciones = relationship('SistemaNotificaciones', back_populates='usuario')

# Modelo de GestorContraseñas
class GestorContraseñas(Base):
    __tablename__ = 'gestor_contraseñas'

    ID_Gestor = Column(Integer, primary_key=True, autoincrement=True)
    ID_Usuario = Column(Integer, ForeignKey('usuario.ID_Usuario'), nullable=False)
    Nombre_Gestor = Column(String(100), nullable=False)
    Fecha_Creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship('Usuario', back_populates='gestores')
    contraseñas = relationship('Contraseña', back_populates='gestor')

# Modelo de Contraseña
class Contraseña(Base):
    __tablename__ = 'contraseña'

    ID_Contraseña = Column(Integer, primary_key=True, autoincrement=True)
    ID_Gestor = Column(Integer, ForeignKey('gestor_contraseñas.ID_Gestor'), nullable=False)
    Servicio = Column(String(100), nullable=False)
    Contraseña_Almacenada = Column(String(255), nullable=False)
    Fecha_Creacion = Column(DateTime, default=datetime.utcnow)

    gestor = relationship('GestorContraseñas', back_populates='contraseñas')
    generador = relationship('GeneradorContraseñas', back_populates='contraseña', uselist=False)

# Modelo de GeneradorContraseñas
class GeneradorContraseñas(Base):
    __tablename__ = 'generador_contraseñas'

    ID_Generador = Column(Integer, primary_key=True, autoincrement=True)
    ID_Contraseña = Column(Integer, ForeignKey('contraseña.ID_Contraseña'), nullable=False)
    Longitud = Column(Integer, nullable=False)
    Incluye_Simbolos = Column(Boolean, default=False)
    Incluye_Numeros = Column(Boolean, default=False)

    contraseña = relationship('Contraseña', back_populates='generador')

# Modelo de SistemaNotificaciones
class SistemaNotificaciones(Base):
    __tablename__ = 'sistema_notificaciones'

    ID_Sistema = Column(Integer, primary_key=True, autoincrement=True)
    ID_Usuario = Column(Integer, ForeignKey('usuario.ID_Usuario'), nullable=False)
    Servicio = Column(String(100), nullable=False)
    Preferencia_Envio = Column(String(50), nullable=False)

    usuario = relationship('Usuario', back_populates='notificaciones')
    notificaciones = relationship('Notificacion', back_populates='sistema')

# Modelo de Notificacion
class Notificacion(Base):
    __tablename__ = 'notificacion'

    ID_Notificacion = Column(Integer, primary_key=True, autoincrement=True)
    ID_Sistema = Column(Integer, ForeignKey('sistema_notificaciones.ID_Sistema'), nullable=False)
    Mensaje = Column(String(255), nullable=False)
    Fecha_Envio = Column(DateTime, default=datetime.utcnow)
    Leida = Column(Boolean, default=False)

    sistema = relationship('SistemaNotificaciones', back_populates='notificaciones')

# Configuración de la base de datos
DATABASE_URL = 'sqlite:///gestor_contraseñas.db'  # Cambia a tu conexión, por ejemplo: postgresql://user:password@localhost/dbname
engine = create_engine(DATABASE_URL, echo=True)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()
