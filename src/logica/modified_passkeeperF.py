from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import hashlib
import random
import string
from datetime import datetime, timezone

Base = declarative_base()
class PasswordManager:
    def __init__(self, db_name='password_manager.db'):
        self.engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def hash_password(self, password: str) -> str:
        """Genera un hash SHA-256 para la protección de la contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()

    def close(self):
        """Cierra la conexión con la base de datos."""
        self.session.close()

    # ------------------- Autenticación y Seguridad -------------------

    def create_user(self, username: str, password: str):
        """Registra un nuevo usuario con una contraseña segura y crea un perfil asociado."""
        password_hash = self.hash_password(password)
        new_user = User(username=username, password_hash=password_hash)
        self.session.add(new_user)
        self.session.commit()  # Guarda el usuario para que tenga un ID asignado

        # Crear un perfil asociado al nuevo usuario
        if new_user.id:  # Verifica que el usuario tenga un ID asignado
            new_profile = Perfil(nombre=f"Perfil de {username}", fecha_creacion=datetime.now().date(),
                                 user_id=new_user.id)
            self.session.add(new_profile)
            self.session.commit()
        else:
            print("Error: No se pudo crear el perfil porque el usuario no tiene un ID asignado.")

    def login(self, username: str, password: str) -> bool:
        """Inicia sesión verificando las credenciales."""
        user = self.session.query(User).filter_by(username=username).first()
        if user and user.password_hash == self.hash_password(password):
            print(f"Bienvenido, {username}!")
            return True
        return False

    def start_session(self, user_id: int):
        """Registra el inicio de sesión del usuario en la tabla Sesion."""
        new_session = Sesion(fecha_inicio=datetime.now(), user_id=user_id)
        self.session.add(new_session)
        self.session.commit()
        return new_session.id

    def end_session(self, session_id: int):
        """Registra el fin de sesión."""
        session = self.session.query(Sesion).get(session_id)
        if session:
            session.fecha_fin = datetime.now()
            self.session.commit()

    # ------------------- Gestión de Servicios -------------------

    def add_service(self, user_id: int, service: str, username: str, password: str):
        """Añade un nuevo servicio con credenciales."""
        password_hash = self.hash_password(password)
        new_service = Service(user_id=user_id, service=service, username=username, password_hash=password_hash)
        self.session.add(new_service)
        self.session.commit()

        # Añadir notificación de creación de servicio
        notificacion = Notificacion(
            mensaje=f"Servicio '{service}' añadido para el usuario '{username}'",
            fecha_envio=datetime.now(timezone.utc),
            user_id=user_id
        )
        self.session.add(notificacion)
        self.session.commit()

    def edit_service(self, user_id: int, service: str, new_password: str):
        """Edita la contraseña de un servicio existente."""
        service_record = self.session.query(Service).filter_by(user_id=user_id, service=service).first()
        if service_record:
            service_record.password_hash = self.hash_password(new_password)
            self.session.commit()

    # ------------------- Gestión de Perfiles -------------------

    def update_profile(self, user_id: int, new_username: str = None, new_password: str = None):
        """Actualiza el perfil del usuario."""
        user = self.session.get(User, user_id)
        if user:
            if new_username:
                user.username = new_username
            if new_password:
                user.password_hash = self.hash_password(new_password)
            self.session.commit()

    # ------------------- Generador de Contraseñas -------------------

    def generate_password(self, length=12) -> str:
        """Genera una contraseña segura de longitud especificada."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def list_services(self, user_id: int):
        services = self.session.query(Service).filter_by(user_id=user_id).all()
        return [(service.service, service.username) for service in services]
        """Devuelve una lista de servicios para un usuario específico."""
        services = self.session.query(Service).filter_by(user_id=user_id).all()
        return [(service.service, service.username) for service in services]

    def get_service(self, service_name: str, user_id: int):
        service = self.session.query(Service).filter_by(service=service_name, user_id=user_id).first()
        if service:
            return (service.service, service.username, service.password_hash)
        """Devuelve los detalles de un servicio específico de un usuario."""
        service = self.session.query(Service).filter_by(service=service_name, user_id=user_id).first()
        if service:
            return (service.service, service.username, service.password_hash)

    def close(self):
        """Cierra la conexión con la base de datos."""
        self.session.close()


# Definición de la clase de usuario usando SQLAlchemy

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    # Relaciones con otras tablas
    services = relationship("Service", back_populates="user")
    perfil = relationship("Perfil", uselist=False, back_populates="user")
    sesiones = relationship("Sesion", back_populates="user")
    notificaciones = relationship("Notificacion", back_populates="user")

class Service(Base):

    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    service = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now(timezone.utc)) # Añade la fecha y hora de creación
    user = relationship("User", back_populates="services")

class Perfil(Base):
    __tablename__ = 'perfil'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    fecha_creacion = Column(Date)
    preferencias = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="perfil")

class Sesion(Base):
    __tablename__ = 'sesion'
    id = Column(Integer, primary_key=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="sesiones")

class Notificacion(Base):
    __tablename__ = 'notificacion'
    id = Column(Integer, primary_key=True)
    mensaje = Column(String)
    fecha_envio = Column(DateTime, default=datetime.now(timezone.utc))  # Registra la fecha y hora de la notificación
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="notificaciones")


class Controlador:
    def __init__(self, password_manager: PasswordManager):
        self.password_manager = password_manager

    def gestionar_sesion_usuario(self, username: str, password: str) -> bool:
        """Verifica las credenciales del usuario para gestionar la sesión."""
        return self.password_manager.login(username, password)

    def gestionar_perfil(self, user_id: int, new_username: str = None, new_password: str = None):
        """Gestiona la actualización del perfil del usuario."""
        self.password_manager.update_profile(user_id, new_username, new_password)

    def gestionar_nuevos_servicios(self, user_id: int, service_name: str, username: str, password: str):
        """Añade un nuevo servicio para el usuario."""
        self.password_manager.add_service(user_id, service_name, username, password)

    def mostrar_ventana_mensaje(self, mensaje: str):
        """Simula la visualización de un mensaje en una ventana (puede integrarse con Tkinter)."""
        print(f"Mensaje: {mensaje}")

    def encriptar_contrasena(self, data: str) -> str:
        """Encripta la contraseña utilizando la clase Encriptador."""
        return Encriptador.encriptar(data)

    def desencriptar_contrasena(self, encrypted_data: str) -> str:
        """Desencripta la contraseña utilizando la clase Encriptador."""
        return Encriptador.desencriptar(encrypted_data)

class Encriptador:
    @staticmethod
    def encriptar(data: str) -> str:
        """Método simple para encriptar datos (puede mejorarse)."""
        return ''.join(chr(ord(char) + 3) for char in data)  # Ejemplo de cifrado César

    @staticmethod
    def desencriptar(encrypted_data: str) -> str:
        """Método simple para desencriptar datos (debe coincidir con el método de encriptado)."""
        return ''.join(chr(ord(char) - 3) for char in encrypted_data)



