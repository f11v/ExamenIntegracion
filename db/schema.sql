CREATE TABLE resultados_examenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    laboratorio_id INTEGER,
    paciente_id INTEGER,
    tipo_examen TEXT,
    resultado TEXT,
    fecha_examen DATE,
    UNIQUE(paciente_id, tipo_examen, fecha_examen)
);

CREATE TABLE log_cambios_resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operacion TEXT,
    paciente_id INTEGER,
    tipo_examen TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER auditoria_resultados
AFTER INSERT OR UPDATE ON resultados_examenes
FOR EACH ROW
BEGIN
    INSERT INTO log_cambios_resultados (operacion, paciente_id, tipo_examen, fecha)
    VALUES (
        CASE WHEN NEW.rowid THEN 'INSERT' ELSE 'UPDATE' END,
        NEW.paciente_id,
        NEW.tipo_examen,
        CURRENT_TIMESTAMP
    );
END;