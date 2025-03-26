import pymysql

miConexion = pymysql.connect(host='localhost', user='root', passwd='',db='informe_rentabilidades')
cur = miConexion.cursor()
print('ID de Proyectos')
cur.execute("select IdProyecto from proyectos")

for IdProyecto in cur.fetchall():
    print(IdProyecto)

miConexion.close()

