
# **Sistema de Integración de Resultados Clínicos - Caso BioNet**

## **Introducción**
BioNet administra una red de laboratorios clínicos distribuidos en diferentes ciudades del país. Este proyecto soluciona los problemas actuales relacionados con la gestión, transferencia y consolidación de resultados de exámenes clínicos mediante un sistema automatizado y unificado. La implementación asegura la integridad, consistencia y disponibilidad de los datos, mejorando significativamente la eficiencia operativa.

---

## **Problemas Identificados**
### **Situación Actual**
- **Generación de Archivos**: Los laboratorios producen archivos `.csv` diarios con los resultados.
- **Transferencia Manual**: Los archivos se copian manualmente en un servidor FTP compartido.
- **Consolidación de Datos**: Se utiliza una base de datos compartida para centralizar los resultados.

### **Desafíos**
1. **Duplicación o Sobrescritura de Datos**: La falta de validaciones adecuadas provoca inconsistencias.
2. **Errores de Sincronización**: Archivos incompletos o corruptos generan errores en la base de datos.
3. **Problemas de Concurrencia**: Escrituras simultáneas causan conflictos y pérdida de información.

---

## **Solución Propuesta**
### **Estructura de Carpetas**
```bash
/input-labs/       # Archivos .csv de los laboratorios.
/processed/        # Archivos válidos procesados.
/error/            # Archivos con errores que requieren revisión.
```

### **Flujo de Integración**
1. **Recepción de Archivos**: Los laboratorios depositan los archivos en `/input-labs/`.
2. **Validación**: Se verifica que los archivos sean completos y estén correctamente formateados.
3. **Procesamiento**:
   - Archivos válidos se mueven a `/processed/` y su contenido se inserta en la base de datos.
   - Archivos inválidos se mueven a `/error/`.

---

## **Esquema de Base de Datos**
### **Tabla: resultados_examenes**
| Campo            | Descripción                                   |
|------------------|-----------------------------------------------|
| id               | Identificador único del resultado.           |
| laboratorio_id   | Identificador del laboratorio.               |
| paciente_id      | Identificador del paciente.                  |
| tipo_examen      | Tipo de examen realizado.                    |
| resultado        | Resultado del examen.                        |
| fecha_examen     | Fecha del examen.                            |

### **Tabla: log_cambios_resultados**
| Campo            | Descripción                                   |
|------------------|-----------------------------------------------|
| id               | Identificador único del log.                 |
| operacion        | Tipo de operación realizada (`INSERT` o `UPDATE`). |
| paciente_id      | Identificador del paciente.                  |
| tipo_examen      | Tipo de examen afectado.                     |
| fecha            | Fecha y hora de la operación.                |

---

## **Implementación Técnica**
### **Módulo 1 – Transferencia de Archivos**
- **Herramienta**: Apache Camel o script propio.
- **Funcionalidades**:
  - Leer archivos `.csv` desde `/input-labs/`.
  - Validar que los archivos sean completos y sin errores.
  - Mover archivos válidos a `/processed/` y inválidos a `/error/`.

### **Módulo 2 – Ingesta en Base de Datos**
- **Base de Datos**: SQLite o MySQL.
- **Funcionalidades**:
  - Insertar los resultados en `resultados_examenes`.
  - Implementar índices únicos para evitar duplicados.
  - Crear un trigger que registre `INSERT` y `UPDATE` en `log_cambios_resultados`.

---

## **Pruebas y Validación**
### **Pruebas Realizadas**
1. **Validación de Archivos**:
   - Solo los archivos completos y correctamente formateados son procesados.
2. **Inserción en Base de Datos**:
   - Los datos se insertan correctamente y se rechazan duplicados.
3. **Trigger de Auditoría**:
   - Las operaciones de `INSERT` y `UPDATE` se registran en `log_cambios_resultados`.

### **Resultados Esperados**
- Los datos procesados se consolidan en la base de datos sin inconsistencias.
- Las operaciones quedan registradas en el log de auditoría.

---

## **Imagenes de evidencia**

![{29BB212B-9471-4821-924F-B0B4D97E0499}](https://github.com/user-attachments/assets/28807402-8e58-46e5-92b6-0344c7f454be)
Nota: Se ocupa Apache Camel

![image](https://github.com/user-attachments/assets/fe76e37c-3984-41cc-8fad-93e3a8713a38)
Nota: Ingresa los datos del archivo 

![image](https://github.com/user-attachments/assets/ebecb632-4222-45d2-a37e-1c7a053366af)
Nota: No ingreso en la base de datos los mismos datos (se creó copia del mismo archivo y se volvió a ejecutar pero no se ingresar los mismos datos)

![image](https://github.com/user-attachments/assets/a090d12d-23fa-488a-bf22-1f9630c0dfd8)
Nota: Se registran los documentos

![image](https://github.com/user-attachments/assets/4a0e1ea5-a23c-44ba-b3a6-683e82a25274)
![image](https://github.com/user-attachments/assets/89f985c4-f5db-440f-8f78-5ab11a825a3a)
Nota: Se valida que si existe un log de auditoria

![{6512D751-A0CF-4C4B-B7EB-50C687C0563F}](https://github.com/user-attachments/assets/64b7b89b-28a7-42ce-9016-37cff0ab93d8)
Nota: Se presenta errores tambien

---

## **Conclusiones**
La integración de módulos automatizados y patrones de diseño robustos han solucionado los problemas clave de BioNet. La solución garantiza la integridad y disponibilidad de los datos, optimizando la gestión de resultados clínicos en todos los laboratorios.
