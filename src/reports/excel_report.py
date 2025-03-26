import pandas as pd
from database import get_session


def generate_excel_report(query, filename="reporte.xlsx"):
    """
    Genera un informe en Excel a partir de una consulta SQLAlchemy o DataFrame.
    :param query: Consulta SQLAlchemy (objeto Query) o un DataFrame.
    :param filename: Nombre del archivo Excel de salida.
    """
    session = get_session()

    # Si 'query' es una consulta SQLAlchemy, conviértela a DataFrame
    try:
        df = pd.read_sql(query.statement, session.bind)
    except AttributeError:
        # Si ya es un DataFrame
        df = query

    df.to_excel(filename, index=False)
    print(f"Reporte generado: {filename}")
