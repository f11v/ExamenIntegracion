import os
import pandas as pd
from sqlalchemy import create_engine, text
import shutil

INPUT_DIR = 'processed'
PROCESSED_DIR = 'processed'
ERROR_DIR = 'error'
DB_PATH = r'C:\Users\ASUS\Downloads\bionet-camel-java-project\db\bionet.db'

# Conexión a la base de datos SQLite
engine = create_engine(f'sqlite:///{DB_PATH}')

# Verificar que el archivo CSV tenga las columnas correctas
def is_valid_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        required_cols = ['laboratorio_id', 'paciente_id', 'tipo_examen', 'resultado', 'fecha_examen']
        return all(col in df.columns for col in required_cols)
    except Exception as e:
        print(f"Error leyendo {file_path}: {e}")
        return False

# Verificar conexión a la base de datos y existencia de la tabla
def check_db_connection():
    try:
        with engine.connect() as conn:
            print("Conexión exitosa a la base de datos.")
            # Usar sqlite_master para verificar si la tabla existe
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='resultados_examenes';"))
            table_exists = result.fetchone()
            if table_exists:
                print("La tabla 'resultados_examenes' existe.")
            else:
                print("La tabla 'resultados_examenes' no existe.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")

# Procesar el archivo CSV y agregar los datos a la base de datos
def process_file(file_path):
    df = pd.read_csv(file_path)

    with engine.begin() as conn:
        for _, row in df.iterrows():
            # Verificar si ya existe un resultado para el paciente y tipo de examen en la fecha dada
            res = conn.execute(text("""
                SELECT 1 FROM resultados_examenes 
                WHERE paciente_id = :paciente_id 
                AND tipo_examen = :tipo_examen 
                AND fecha_examen = :fecha_examen
            """), {
                "paciente_id": row.paciente_id,
                "tipo_examen": row.tipo_examen,
                "fecha_examen": row.fecha_examen
            }).fetchone()

            # Si no existe, insertar el nuevo resultado
            if not res:
                try:
                    conn.execute(text("""
                        INSERT INTO resultados_examenes (
                            laboratorio_id, paciente_id, tipo_examen, resultado, fecha_examen
                        ) VALUES (
                            :laboratorio_id, :paciente_id, :tipo_examen, :resultado, :fecha_examen
                        )
                    """), row.to_dict())
                    print(f"Datos insertados para paciente {row.paciente_id} - Examen {row.tipo_examen} en {row.fecha_examen}")
                except Exception as e:
                    print(f"Error insertando datos: {e}")

# Función principal para procesar los archivos CSV en la carpeta 'processed'
def main():
    # Verificar la conexión y la tabla antes de procesar los archivos
    check_db_connection()

    for filename in os.listdir(INPUT_DIR):
        path = os.path.join(INPUT_DIR, filename)
        if filename.endswith('.csv'):
            if is_valid_csv(path):
                try:
                    process_file(path)
                    print(f"Procesado: {filename}")
                    # Mover el archivo procesado a la carpeta correspondiente
                    shutil.move(path, os.path.join(PROCESSED_DIR, filename))
                except Exception as e:
                    print(f"Error procesando {filename}: {e}")
                    shutil.move(path, os.path.join(ERROR_DIR, filename))
            else:
                print(f"Archivo inválido: {filename}")
                shutil.move(path, os.path.join(ERROR_DIR, filename))

if __name__ == "__main__":
    main()