
CREATE TABLE IF NOT EXISTS resultados_examenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    laboratorio_id INTEGER NOT NULL,
    paciente_id INTEGER NOT NULL,
    tipo_examen TEXT NOT NULL,
    resultado TEXT NOT NULL,
    fecha_examen DATE NOT NULL,
    UNIQUE(paciente_id, tipo_examen, fecha_examen)
);

CREATE TABLE IF NOT EXISTS log_cambios_resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operacion TEXT,
    paciente_id INTEGER NOT NULL,
    tipo_examen TEXT NOT NULL,
    fecha DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER IF NOT EXISTS trg_log_resultados_insert
AFTER INSERT ON resultados_examenes
BEGIN
    INSERT INTO log_cambios_resultados (operacion, paciente_id, tipo_examen, fecha)
    VALUES ('INSERT', NEW.paciente_id, NEW.tipo_examen, NEW.fecha_examen);
END;

CREATE TRIGGER IF NOT EXISTS trg_log_resultados_update
AFTER UPDATE ON resultados_examenes
BEGIN
    INSERT INTO log_cambios_resultados (operacion, paciente_id, tipo_examen, fecha)
    VALUES ('UPDATE', NEW.paciente_id, NEW.tipo_examen, NEW.fecha_examen);
END;
