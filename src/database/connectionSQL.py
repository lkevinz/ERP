import pymysql


# ABRIR CONEXION
def conexionDB():
    try:
        miConexion = pymysql.connect(
            host="localhost", user="root", passwd="", db="informe_rentabilidades"
        )
        cur = miConexion.cursor()
        print("Conexión exitosa a la base de datos")
        return miConexion, cur
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None, None


#   CERRAR CONEXION
def cerrarConexion(miConexion):
    """Cierra la conexión con la base de datos."""
    if miConexion:
        miConexion.close()
        print("Conexión cerrada correctamente")
    else:
        print("No hay conexión activa para cerrar")
