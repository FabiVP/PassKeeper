import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QWidget, QListWidget
)
from PyQt6.QtCore import Qt
from src.logica.passkeeperF import PasswordManager, Controlador, Service , Notificacion

class LoginDialog(QDialog):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.setWindowTitle("Inicio de Sesión")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        # Campos de entrada de usuario y contraseña
        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # Botón para abrir la pantalla de creación de cuenta
        self.signup_button = QPushButton("Crear Cuenta")
        self.signup_button.clicked.connect(self.open_signup_dialog)
        layout.addWidget(self.signup_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.controlador.gestionar_sesion_usuario(username, password):
            QMessageBox.information(self, "Bienvenido", f"Inicio de sesión exitoso. Bienvenido, {username}!")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def open_signup_dialog(self):
        # Abre la pantalla de creación de cuenta
        signup_dialog = SignupDialog(self.controlador)
        signup_dialog.exec()

class SignupDialog(QDialog):
    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador
        self.setWindowTitle("Crear Cuenta")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        # Campos de entrada de usuario y contraseña para crear cuenta
        self.new_username_label = QLabel("Nuevo Usuario:")
        self.new_username_input = QLineEdit()
        layout.addWidget(self.new_username_label)
        layout.addWidget(self.new_username_input)

        self.new_password_label = QLabel("Contraseña:")
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)

        # Botón para crear la cuenta
        self.create_account_button = QPushButton("Registrar")
        self.create_account_button.clicked.connect(self.create_account)
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)

    def create_account(self):
        username = self.new_username_input.text()
        password = self.new_password_input.text()
        if username and password:
            try:
                self.controlador.password_manager.create_user(username, password)
                QMessageBox.information(self, "Cuenta creada", f"Cuenta creada exitosamente para {username}.")
                self.accept()  # Cierra el diálogo de creación de cuenta
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo crear la cuenta: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar un usuario y una contraseña para crear una cuenta.")

class AddPasswordDialog(QDialog):
    def __init__(self, controlador, user_id):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.setWindowTitle("Añadir Contraseña")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.service_label = QLabel("Servicio:")
        self.service_input = QLineEdit()
        layout.addWidget(self.service_label)
        layout.addWidget(self.service_input)

        self.username_label = QLabel("Usuario:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Contraseña:")
        self.password_input = QLineEdit()
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.add_button = QPushButton("Añadir")
        self.add_button.clicked.connect(self.add_password)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_password(self):
        service = self.service_input.text()
        username = self.username_input.text()
        password = self.password_input.text()
        if service and username and password:
            self.controlador.gestionar_nuevos_servicios(self.user_id, service, username, password)
            QMessageBox.information(self, "Éxito", "Contraseña añadida correctamente")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")

class EditPasswordDialog(QDialog):
    def __init__(self, controlador, user_id):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.setWindowTitle("Editar Contraseña")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.service_label = QLabel("Servicio:")
        self.service_input = QLineEdit()
        layout.addWidget(self.service_label)
        layout.addWidget(self.service_input)

        self.new_password_label = QLabel("Nueva Contraseña:")
        self.new_password_input = QLineEdit()
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)

        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.edit_password)
        layout.addWidget(self.edit_button)

        self.setLayout(layout)

    def edit_password(self):
        service = self.service_input.text()
        new_password = self.new_password_input.text()
        if service and new_password:
            self.controlador.password_manager.edit_service(self.user_id, service, new_password)
            QMessageBox.information(self, "Éxito", "Contraseña actualizada correctamente")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")

class DeletePasswordDialog(QDialog):
    def __init__(self, controlador, user_id):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.setWindowTitle("Eliminar Contraseña")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.service_label = QLabel("Servicio:")
        self.service_input = QLineEdit()
        layout.addWidget(self.service_label)
        layout.addWidget(self.service_input)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_password)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def delete_password(self):
        service = self.service_input.text()
        if service:
            # Busca el servicio y elimina la contraseña
            self.controlador.password_manager.session.query(Service).filter_by(user_id=self.user_id, service=service).delete()
            self.controlador.password_manager.session.commit()
            QMessageBox.information(self, "Éxito", "Contraseña eliminada correctamente")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Debe ingresar el nombre del servicio")

class ViewServicesDialog(QDialog):
    def __init__(self, controlador, user_id):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.setWindowTitle("Ver Servicios")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.service_list = QListWidget()
        services = self.controlador.password_manager.list_services(self.user_id)
        for service, username in services:
            self.service_list.addItem(f"Servicio: {service}, Usuario: {username}")
        layout.addWidget(self.service_list)

        self.setLayout(layout)


class ViewNotificationsDialog(QDialog):
    def __init__(self, controlador, user_id):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.setWindowTitle("Ver Notificaciones")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.notifications_list = QListWidget()

        # Recupera las notificaciones de la base de datos
        notificaciones = self.controlador.password_manager.session.query(Notificacion).filter_by(
            user_id=self.user_id).all()
        for notificacion in notificaciones:
            # Muestra la fecha y mensaje de la notificación
            self.notifications_list.addItem(f"{notificacion.fecha_envio}: {notificacion.mensaje}")

        layout.addWidget(self.notifications_list)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, controlador, user_id):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.setWindowTitle("Gestor de Contraseñas")
        self.setFixedSize(400, 300)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Botones para gestionar contraseñas y notificaciones
        self.add_password_button = QPushButton("Añadir Contraseña")
        self.add_password_button.clicked.connect(self.open_add_password_dialog)
        layout.addWidget(self.add_password_button)

        self.edit_password_button = QPushButton("Editar Contraseña")
        self.edit_password_button.clicked.connect(self.open_edit_password_dialog)
        layout.addWidget(self.edit_password_button)

        self.delete_password_button = QPushButton("Eliminar Contraseña")
        self.delete_password_button.clicked.connect(self.open_delete_password_dialog)
        layout.addWidget(self.delete_password_button)

        self.view_services_button = QPushButton("Ver Servicios")
        self.view_services_button.clicked.connect(self.open_view_services_dialog)
        layout.addWidget(self.view_services_button)

        self.notifications_button = QPushButton("Ver Notificaciones")
        self.notifications_button.clicked.connect(self.open_view_notifications_dialog)
        layout.addWidget(self.notifications_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_add_password_dialog(self):
        dialog = AddPasswordDialog(self.controlador, self.user_id)
        dialog.exec()

    def open_edit_password_dialog(self):
        dialog = EditPasswordDialog(self.controlador, self.user_id)
        dialog.exec()

    def open_delete_password_dialog(self):
        dialog = DeletePasswordDialog(self.controlador, self.user_id)
        dialog.exec()

    def open_view_services_dialog(self):
        dialog = ViewServicesDialog(self.controlador, self.user_id)
        dialog.exec()

    def open_view_notifications_dialog(self):
        dialog = ViewNotificationsDialog(self.controlador, self.user_id)
        dialog.exec()

def main():
    app = QApplication(sys.argv)
    password_manager = PasswordManager()
    controlador = Controlador(password_manager)

    login_dialog = LoginDialog(controlador)
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        user_id = 1  # Deberías obtener el ID real del usuario autenticado
        main_window = MainWindow(controlador, user_id)
        main_window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()