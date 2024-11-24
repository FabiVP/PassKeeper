import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QWidget, QListWidget, QHBoxLayout,QCheckBox, QGridLayout
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize


from src.logica.modified_passkeeperF import PasswordManager, Controlador, Service, Notificacion, Perfil, User, Sesion


class LoginDialog(QDialog):
    def __init__(self, controlador):
        super().__init__()
        self.setWindowTitle("Iniciar sesión")
        self.setFixedSize(250, 350)
        self.controlador = controlador
        self.init_ui()

    def init_ui(self):
        # Configurar el estilo de la ventana de inicio de sesión
        # Configurar el estilo de la ventana de inicio de sesión
        self.setStyleSheet("""
                    QDialog {
                            background-color: #1e1d22;  /* Fondo negro */
                            color: #FFFFFF;
                        }
                        QLabel {
                            font-size: 16px;
                            color: #FFFFFF;
                        }
                        QLineEdit {
                            background-color: #1C1C1C;
                            color: #FFFFFF;
                            border: 2px solid #555555;
                            border-radius: 5px;
                            padding: 5px;
                        }
                        QLineEdit:focus {
                            border: 2px solid #9B59B6;
                        }
                        QPushButton {
                            background-color: #9B59B6 !important;  /* Fuerza el color morado */
                            color: #FFFFFF !important;
                            border: 2px solid #9B59B6 !important;
                            border-radius: 5px;
                            padding: 10px 20px;
                        }
                """)

        # Fuente general
        font = QFont("Courier New", 10)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Imagen de fondo detrás del ícono
        background_label = QLabel(self)
        background_pixmap = QPixmap("images.jpg").scaled(
            self.width(), self.height() // 3,  # Ajusta el ancho y alto relativo
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        background_label.setPixmap(background_pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height() // 3)  # Ocupa el ancho completo
        background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ícono o imagen superior
        icon_label = QLabel()
        icon_label.setPixmap(QIcon("Perfil4.png").pixmap(90, 90))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(icon_label)

        # Campo de Email
        email_label = QLabel("Usuario")
        email_label.setFont(font)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Ingrese Usuario")
        self.email_input.setFont(font)

        # Campo de Contraseña
        password_label = QLabel("Contraseña")
        password_label.setFont(font)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Ingrese contraseña")
        self.password_input.setFont(font)

        # Botón "Crear Usuario"
        signup_button = QPushButton("Crear Usuario")
        signup_button.setFont(QFont("Courier New", 12))
        signup_button.setStyleSheet("background-color: #9B59B6; color: white; padding: 5px;")
        signup_button.clicked.connect(self.open_signup_dialog)

        # Botón de inicio de sesión
        login_button = QPushButton("Iniciar sesión")
        login_button.setFont(QFont("Courier New", 12))
        login_button.setStyleSheet("background-color: #9B59B6; color: white; padding: 5px;")
        login_button.clicked.connect(self.login)

        # Agregar widgets al layout
        main_layout.addWidget(email_label)
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(password_label)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(login_button)
        main_layout.addWidget(signup_button)  # Agregar el botón de crear usuario

        self.setLayout(main_layout)

    def login(self):
        username = self.email_input.text().strip()  # Usamos email_input en lugar de username_input
        password = self.password_input.text().strip()

        try:
            # Llamamos al método existente en el controlador para gestionar la sesión
            if self.controlador.gestionar_sesion_usuario(username, password):
                # Obtenemos al usuario desde la base de datos
                user = self.controlador.password_manager.session.query(User).filter_by(username=username).first()
                if user:
                    self.user_id = user.id  # Asignamos el ID del usuario a la instancia
                    QMessageBox.information(self, "Bienvenido", f"Inicio de sesión exitoso. Bienvenido, {username}!")
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", "No se encontró el usuario.")
            else:
                QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"Ocurrió un error inesperado: {e}")

    def closeEvent(self, event):
        """Cierra la aplicación cuando se presiona la 'X' en la ventana de inicio de sesión."""
        sys.exit(0)  # Sale de toda la aplicación


    def accept(self):
        QDialog.accept(self)  # Cambiado para evitar recursión



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
            try:
                self.controlador.gestionar_nuevos_servicios(self.user_id, service, username, password)
                QMessageBox.information(self, "Éxito", "Contraseña añadida correctamente")

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Ocurrió un error: {str(e)}")
                print(f"Error añadiendo contraseña: {e}")
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
            self.controlador.password_manager.session.query(Service).filter_by(user_id=self.user_id,
                                                                               service=service).delete()
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
class ViewSessionsDialog(QDialog):
    def __init__(self, controlador, user_id):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.setWindowTitle("Historial de Sesiones")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.sessions_list = QListWidget()

        # Recupera las sesiones desde la base de datos
        sesiones = self.controlador.password_manager.session.query(Sesion).filter_by(user_id=self.user_id).all()
        for sesion in sesiones:
            inicio = sesion.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S') if sesion.fecha_inicio else 'Desconocido'
            fin = sesion.fecha_fin.strftime('%Y-%m-%d %H:%M:%S') if sesion.fecha_fin else 'Sesión activa'
            self.sessions_list.addItem(f"Inicio: {inicio} | Fin: {fin}")

        layout.addWidget(self.sessions_list)
        self.setLayout(layout)

# Añadir la clase ProfileDialog aquí, después de DeletePasswordDialog o el último diálogo definido
class ProfileDialog(QDialog):
    def __init__(self, controlador, user_id, main_window):
        super().__init__()
        self.controlador = controlador
        self.user_id = user_id
        self.main_window = main_window
        self.session_id = self.controlador.password_manager.start_session(self.user_id)
        self.setWindowTitle("Perfil del Usuario")
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        perfil = self.controlador.password_manager.session.query(Perfil).filter_by(user_id=self.user_id).first()

        # Campos de edición
        self.name_label = QLabel("Nombre:")
        self.name_input = QLineEdit(perfil.nombre if perfil else "")
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.preferences_label = QLabel("Preferencias:")
        self.preferences_input = QLineEdit(perfil.preferencias if perfil else "")
        layout.addWidget(self.preferences_label)
        layout.addWidget(self.preferences_input)

        # Botón de guardar cambios
        self.save_button = QPushButton("Guardar Cambios")
        self.save_button.clicked.connect(self.save_profile_changes)
        layout.addWidget(self.save_button)

        # Botón de cerrar sesión
        self.logout_button = QPushButton("Cerrar Sesión")
        self.logout_button.clicked.connect(self.logout)
        layout.addWidget(self.logout_button)

        self.setLayout(layout)

    def save_profile_changes(self):
        new_name = self.name_input.text()
        new_preferences = self.preferences_input.text()

        perfil = self.controlador.password_manager.session.query(Perfil).filter_by(user_id=self.user_id).first()
        if perfil:
            perfil.nombre = new_name
            perfil.preferencias = new_preferences
            self.controlador.password_manager.session.commit()
            QMessageBox.information(self, "Éxito", "Perfil actualizado correctamente")

    def logout(self):
        """Finaliza la sesión y regresa a la pantalla de inicio."""
        if self.session_id:
            self.controlador.password_manager.end_session(self.session_id)
            self.session_id = None

        # Marca que el usuario cerró sesión en la ventana principal
        self.main_window.logout()
        self.close()

class MainWindow(QMainWindow):
        def __init__(self, controlador, user_id):
            super().__init__()
            self.controlador = controlador
            self.user_id = user_id
            self.user_logged_out = False  # Atributo inicializado para manejar el estado de cierre de sesión

            # Personaliza la ventana para ocultar el símbolo de cierre
            self.setWindowFlags(
                Qt.WindowType.Window | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint)# Deshabilita la 'X'
            self.setWindowTitle("Gestor de Contraseñas")
            self.setFixedSize(600, 500)  # Ajusta el tamaño de la ventana
            self.initUI()

        def initUI(self):
            # Estilo de fondo personalizado
            self.setStyleSheet("""
                QMainWindow {
                    background-image: url("fondo3.jpg");
                    background-repeat: no-repeat;
                    background-position: center;
                    background-size: cover;
                }
                QPushButton {
                    border: none;
                    border-radius: 40px;  /* Hacer los botones redondos */
                    background-color: #31394c;  /* Fondo blanco */
                    padding: 10px;
                    width: 80px;
                    height: 80px;
                }
                QPushButton:hover {
                    background-color: #F0F0F0;  /* Cambia ligeramente el color al pasar el mouse */
                }
            """)

            # Layout principal
            main_layout = QVBoxLayout()
            main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Layout para botones
            button_layout = QGridLayout()
            button_layout.setSpacing(20)  # Espacio entre botones

            # Crear botones circulares con íconos
            buttons = [
                {"icon": "add.png", "tooltip": "Añadir Contraseña", "action": self.open_add_password_dialog},
                {"icon": "edit.png", "tooltip": "Editar Contraseña", "action": self.open_edit_password_dialog},
                {"icon": "deletepass.png", "tooltip": "Eliminar Contraseña",
                 "action": self.open_delete_password_dialog},
                {"icon": "viewservice.png", "tooltip": "Ver Servicios",
                 "action": self.open_view_services_dialog},
                {"icon": "notifica.png", "tooltip": "Ver Notificaciones",
                 "action": self.open_view_notifications_dialog},
                {"icon": "perfil.png", "tooltip": "Ver Perfil", "action": self.open_view_profile_dialog},
                {"icon": "historialinicio.png", "tooltip": "Ver Inicios de Sesión",
                 "action": self.open_view_sessions_dialog},
            ]

            # Crear y agregar botones al layout
            for i, button_data in enumerate(buttons):
                button = QPushButton()
                button.setIcon(QIcon(button_data["icon"]))  # Establecer el ícono
                button.setIconSize(QSize(80,80))  # Ajustar tamaño del ícono
                button.setToolTip(button_data["tooltip"])  # Tooltip al pasar el mouse
                button.clicked.connect(button_data["action"])  # Conectar a la acción
                button_layout.addWidget(button, i // 4, i % 4)  # Organiza en una cuadrícula (máx. 4 columnas)

            main_layout.addLayout(button_layout)

            # Widget central
            container = QWidget()
            container.setLayout(main_layout)
            self.setCentralWidget(container)

        # Métodos para cada acción
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

        def open_view_profile_dialog(self):
            profile_dialog = ProfileDialog(self.controlador, self.user_id, main_window=self)
            profile_dialog.exec()

        def open_view_sessions_dialog(self):
            dialog = ViewSessionsDialog(self.controlador, self.user_id)
            dialog.exec()

        def logout(self):
            """Establece la bandera de cierre de sesión y cierra la ventana."""
            self.user_logged_out = True  # Marca el estado como 'cerrado'
            self.close()

def main():
    app = QApplication(sys.argv)
    password_manager = PasswordManager()
    controlador = Controlador(password_manager)

    while True:
        # Iniciar el diálogo de inicio de sesión
        login_dialog = LoginDialog(controlador)
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            user_id = login_dialog.user_id
            main_window = MainWindow(controlador, user_id)
            main_window.show()

            # Ejecutar el ciclo de eventos de la ventana principal
            app.exec()

            # Si el usuario cierra sesión, cerramos la ventana principal
            if main_window.user_logged_out:
                continue  # Volver al diálogo de inicio de sesión
            else:
                break  # Salir de la aplicación

    sys.exit(app.exec())
if __name__ == "__main__":
    main()