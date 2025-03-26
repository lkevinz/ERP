from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexión a MySQL. Actualiza 'usuario', 'contraseña', 'localhost', '3306' y 'erp_db' según tu configuración.
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/bd_ges_jofmar5"

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


def get_session():
    """Devuelve una sesión para interactuar con la base de datos."""
    return Session()
