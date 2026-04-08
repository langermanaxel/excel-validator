# 🚀 Excel Validator API

API backend desarrollada en Python para validar archivos Excel/CSV antes de ejecutar procesos automatizados contables.

Este proyecto simula una solución real orientada a estudios contables, permitiendo detectar errores en datos de entrada y evitar fallos en procesos automatizados.

---

## 🧠 Problema que resuelve

En soluciones de automatización contable, los archivos Excel suelen ser el punto de entrada.

Errores en estos archivos generan:

* reprocesos
* fallos en automatizaciones
* pérdida de tiempo

👉 Esta API valida los datos previamente para garantizar calidad y consistencia.

---

## ⚙️ Características principales

* ✅ Validación de archivos Excel (.xlsx) y CSV
* ✅ Validaciones de negocio (CUIT, email, campos obligatorios)
* ✅ Reglas dinámicas por cliente y proceso
* ✅ Procesamiento asíncrono con workers
* ✅ Arquitectura desacoplada (API + worker)
* ✅ Generación de reportes de errores descargables
* ✅ Persistencia de logs en base de datos
* ✅ Configuración mediante variables de entorno

---

## 🏗️ Arquitectura

Cliente → API (FastAPI) → Cola (Redis) → Worker (Celery) → DB + Reporte

* API: recibe archivos y dispara tareas
* Worker: procesa validaciones
* Redis: maneja la cola
* DB: almacena logs de ejecución

---

## 📁 Estructura del proyecto

```
app/
├── api/          # Endpoints
├── services/     # Lógica de negocio
├── domain/       # Reglas y validaciones
├── workers/      # Procesamiento async
├── core/         # Configuración, DB, logger
```

---

## 🚀 Instalación

### 1. Clonar repositorio

```
git clone <repo-url>
cd excel-validator-pro
```

### 2. Crear entorno virtual

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```
pip install -r requirements.txt
```

---

## 🔐 Variables de entorno

Crear archivo `.env`:

```
APP_NAME=Excel Validator API
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///./logs.db
LOG_LEVEL=INFO
```

---

## ▶️ Ejecución

### 1. Levantar Redis

```
redis-server
```

### 2. Levantar worker

```
celery -A app.workers.tasks worker --loglevel=info
```

### 3. Levantar API

```
uvicorn app.main:app --reload
```

---

## 📡 Uso de la API

### Validar archivo

```
POST /validate-file
```

Parámetros:

* file: archivo Excel o CSV
* process: tipo de proceso (ej: iva)
* client_id: identificador de cliente

Respuesta:

```
{
  "task_id": "12345"
}
```

---

### Consultar estado

```
GET /task-status/{task_id}
```

---

### Descargar reporte

```
GET /download-report/{filename}
```

---

## 🧪 Ejemplo de datos

| cuit        | email                                   | monto |
| ----------- | --------------------------------------- | ----- |
| 20123456789 | [test@gmail.com](mailto:test@gmail.com) | 1000  |
| 20999999999 | mal-email                               | abc   |

---

## 🧠 Decisiones de diseño

* Separación por capas (API, servicios, dominio)
* Principios SOLID aplicados
* Validaciones desacopladas y reutilizables
* Procesamiento async para escalabilidad
* Configuración externa (env)

---

## 🔒 Seguridad

* No se hardcodean credenciales
* Validación de inputs
* Manejo controlado de errores

---

## 📈 Escalabilidad

* Soporte para múltiples clientes (multi-tenant)
* Workers escalables horizontalmente
* Posibilidad de migrar a PostgreSQL fácilmente

---

## 🚀 Mejoras futuras

* Autenticación (JWT)
* Dashboard de monitoreo
* Versionado de reglas dinámico (DB)
* Integración con APIs externas (AFIP)

---

## 👨‍💻 Autor

Proyecto desarrollado como práctica de arquitectura backend orientada a automatización de procesos.

---

## 💬 Pitch (para entrevista)

Este proyecto simula una solución real de validación previa en pipelines de automatización contable.
Permite reducir errores en inputs, mejorar la eficiencia y escalar el procesamiento mediante arquitectura asíncrona.

---
