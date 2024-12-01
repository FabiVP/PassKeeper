import unittest
import os
from src.logica.passkeeperF import PasswordManager, User, Service, Perfil, Sesion, Notificacion, Encriptador, Controlador
from datetime import date
from datetime import datetime
class TestPasswordManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Inicia el PasswordManager y limpia la base de datos de prueba
        cls.manager = PasswordManager(db_name='test_password_manager.db')

        # Limpia las tablas antes de crear un nuevo usuario
        cls.manager.session.query(Notificacion).delete()
        cls.manager.session.query(Sesion).delete()
        cls.manager.session.query(Perfil).delete()
        cls.manager.session.query(Service).delete()
        cls.manager.session.query(User).delete()
        cls.manager.session.commit()

        # Ahora, crea el usuario para pruebas
        cls.manager.create_user("test_user", "secure_password")

    @classmethod
    def tearDownClass(cls):
        # Cierra la sesión y elimina la base de datos de prueba
        cls.manager.session.close()
        cls.manager.engine.dispose()
        if os.path.exists('test_password_manager.db'):
            os.remove('test_password_manager.db')

    def setUp(self):
        # Restaura la sesión en caso de transacciones previas fallidas
        self.manager.session.rollback()

        # Limpiar las tablas relacionadas antes de cada prueba
        self.manager.session.query(Notificacion).delete()
        self.manager.session.query(Sesion).delete()
        self.manager.session.query(Perfil).delete()
        self.manager.session.query(Service).delete()
        self.manager.session.query(User).filter_by(username="new_user").delete()
        self.manager.session.commit()

    def test_create_user(self):
        self.manager.create_user("new_user", "new_password")
        self.assertTrue(self.manager.login("new_user", "new_password"))

    def test_login(self):
        self.assertTrue(self.manager.login("test_user", "secure_password"))
        self.assertFalse(self.manager.login("test_user", "wrong_password"))

    def test_add_service(self):
        user_id = self.manager.session.query(User).filter_by(username="test_user").first().id
        self.manager.add_service(user_id, "TestService", "testuser", "testpassword")
        services = self.manager.list_services(user_id)
        self.assertIn(("TestService", "testuser"), services)

    def test_edit_service(self):
        user_id = self.manager.session.query(User).filter_by(username="test_user").first().id
        self.manager.add_service(user_id, "EditService", "edituser", "oldpassword")
        self.manager.edit_service(user_id, "EditService", "newpassword")
        updated_service = self.manager.get_service("EditService", user_id)
        self.assertEqual(updated_service[2], self.manager.hash_password("newpassword"))

    def test_create_and_update_profile(self):
        user_id = self.manager.session.query(User).filter_by(username="test_user").first().id
        # Crear perfil
        perfil = Perfil(nombre="Perfil 1", fecha_creacion=date.today(), preferencias="dark_mode", user_id=user_id)
        self.manager.session.add(perfil)
        self.manager.session.commit()

        # Verificar perfil creado
        perfil_db = self.manager.session.query(Perfil).filter_by(user_id=user_id).first()
        self.assertEqual(perfil_db.nombre, "Perfil 1")

        # Actualizar perfil
        perfil_db.nombre = "Perfil Actualizado"
        self.manager.session.commit()

        # Verificar actualización
        perfil_db = self.manager.session.query(Perfil).filter_by(user_id=user_id).first()
        self.assertEqual(perfil_db.nombre, "Perfil Actualizado")

    def test_create_and_manage_sessions(self):
        user_id = self.manager.session.query(User).filter_by(username="test_user").first().id
        # Crear sesión
        sesion = Sesion(fecha_inicio=date(2023,11,1),  fecha_fin=date(2023,11,2), user_id=user_id)
        self.manager.session.add(sesion)
        self.manager.session.commit()

        # Verificar que la sesión fue creada
        sesion_db = self.manager.session.query(Sesion).filter_by(user_id=user_id).first()
        self.assertEqual(sesion_db.fecha_inicio, datetime.strptime('2023-11-01', '%Y-%m-%d').date())
        self.assertEqual(sesion_db.fecha_fin, datetime.strptime('2023-11-02', '%Y-%m-%d').date())

    def test_create_and_list_notifications(self):
        user_id = self.manager.session.query(User).filter_by(username="test_user").first().id
        # Crear notificación
        notificacion = Notificacion(mensaje="Prueba de notificación", fecha_envio=datetime.strptime('2023-11-01', '%Y-%m-%d').date(), user_id=user_id)
        self.manager.session.add(notificacion)
        self.manager.session.commit()

        # Verificar que la notificación fue creada y listada correctamente
        notificaciones = self.manager.session.query(Notificacion).filter_by(user_id=user_id).all()
        self.assertEqual(len(notificaciones), 1)
        self.assertEqual(notificaciones[0].mensaje, "Prueba de notificación")

    def test_generate_password(self):
        password = self.manager.generate_password(12)
        self.assertEqual(len(password), 12)

    def test_update_profile(self):
        user_id = self.manager.session.query(User).filter_by(username="test_user").first().id
        self.manager.update_profile(user_id, new_username="updated_user", new_password="updated_password")
        self.assertTrue(self.manager.login("updated_user", "updated_password"))

    def test_encriptar(self):
        # Verifica que la encriptación funcione correctamente
        data = "contraseña123"
        encrypted_data = Encriptador.encriptar(data)
        self.assertNotEqual(data, encrypted_data)
        self.assertEqual(Encriptador.desencriptar(encrypted_data), data)

    def test_desencriptar(self):
        # Verifica que la desencriptación funcione correctamente
        encrypted_data = "frqwudvhñd456"  # Supongamos que es un dato cifrado
        original_data = Encriptador.desencriptar(encrypted_data)
        re_encrypted_data = Encriptador.encriptar(original_data)
        self.assertEqual(re_encrypted_data, encrypted_data)

class MockPasswordManager:
    def login(self, username, password):
        return username == "test_user" and password == "correct_password"

    def update_profile(self, user_id, new_username=None, new_password=None):
        return True  # Simulación de actualización exitosa

    def add_service(self, user_id, service_name, username, password):
        return True  # Simulación de adición de servicio exitosa

    def setUp(self):
        # Usa un MockPasswordManager en lugar del real para evitar acceder a la base de datos
        self.password_manager = MockPasswordManager()
        self.controlador = Controlador(self.password_manager)

    def test_gestionar_sesion_usuario(self):
        self.assertTrue(self.controlador.gestionar_sesion_usuario("test_user", "correct_password"))
        self.assertFalse(self.controlador.gestionar_sesion_usuario("test_user", "wrong_password"))

    def test_gestionar_perfil(self):
        self.assertTrue(self.controlador.gestionar_perfil(1, new_username="new_user"))

    def test_gestionar_nuevos_servicios(self):
        self.assertTrue(self.controlador.gestionar_nuevos_servicios(1, "Gmail", "user_gmail", "secure_password"))

if __name__ == "__main__":
    unittest.main()
