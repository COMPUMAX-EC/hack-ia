# 🚀 FINOVA API

API backend para el sistema FINOVA - Soluciones de IA para análisis de licitaciones y evaluación crediticia de PYMEs.

## 📋 Características

- **Análisis de Licitaciones IA**: Procesamiento automático de documentos de licitación
- **Evaluación Crediticia IA**: Análisis de riesgo crediticio para PYMEs usando datos alternativos
- **API RESTful**: Endpoints bien documentados con FastAPI
- **Validación de Datos**: Usando Pydantic para validación robusta
- **Documentación Automática**: Swagger UI integrado

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Python 3.11+**: Lenguaje de programación

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/COMPUMAX-EC/hack-ia.git
   cd hack-ia
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**:
   ```bash
   # Windows
   venv\\Scripts\\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar .env según sea necesario
   ```

6. **Iniciar la API**:
   ```bash
   python start_api.py
   ```

## 📚 Uso de la API

### Endpoints Principales

#### 🏥 Health Check
```
GET /api/v1/health
```
Verifica el estado de la API.

#### 📄 Análisis de Licitaciones

**Analizar documento**:
```
POST /api/v1/licitaciones/analyze
```

**Subir archivo**:
```
POST /api/v1/licitaciones/upload
```

**Historial de análisis**:
```
GET /api/v1/licitaciones/history
```

#### 💰 Evaluación Crediticia

**Análisis completo**:
```
POST /api/v1/credito/analyze
```

**Puntuación rápida**:
```
POST /api/v1/credito/quick-score
```

**Factores de riesgo**:
```
GET /api/v1/credito/risk-factors
```

**Estadísticas**:
```
GET /api/v1/credito/statistics
```

### Ejemplos de Uso

#### Análisis de Licitación
```python
import requests

# Analizar documento de licitación
data = {
    "document_content": "Contenido del documento de licitación...",
    "document_type": "Propuesta Técnica",
    "priority": "high"
}

response = requests.post("http://localhost:8000/api/v1/licitaciones/analyze", json=data)
result = response.json()

print(f"Puntuación: {result['score']}")
print(f"Nivel de riesgo: {result['risk_level']}")
print(f"Recomendaciones: {result['recommendations']}")
```

#### Evaluación Crediticia
```python
import requests

# Datos de la empresa
company_data = {
    "company_name": "TechStart PYME",
    "business_type": "Tecnología y Software",
    "years_in_business": "3 años",
    "monthly_revenue": "15000",
    "digital_presence": "Buena presencia en redes sociales",
    "commercial_references": "Referencias comerciales sólidas"
}

data = {
    "company_data": company_data,
    "requested_amount": 50000,
    "loan_purpose": "Expansión de negocio"
}

response = requests.post("http://localhost:8000/api/v1/credito/analyze", json=data)
result = response.json()

print(f"Puntuación crediticia: {result['risk_assessment']['credit_score']}")
print(f"Probabilidad de aprobación: {result['risk_assessment']['approval_probability']}%")
print(f"Monto recomendado: {result['risk_assessment']['recommended_amount']}")
```

## 📖 Documentación Interactiva

Una vez que la API esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Estructura del Proyecto

```
api/
├── main.py                 # Aplicación principal de FastAPI
├── models/                 # Modelos de datos Pydantic
│   ├── licitaciones.py    # Modelos para licitaciones
│   └── credito.py         # Modelos para crédito
├── routers/               # Endpoints de la API
│   ├── health.py          # Health checks
│   ├── licitaciones.py    # Endpoints de licitaciones
│   └── credito.py         # Endpoints de crédito
└── services/              # Lógica de negocio
    ├── licitaciones_service.py
    └── credito_service.py
```

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```env
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,https://hack-ia.vercel.app
```

## 🚀 Despliegue

### Desarrollo Local
```bash
python start_api.py
```

### Producción
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### Docker (Futuro)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📊 Métricas y Monitoreo

La API incluye endpoints para monitoreo:

- `/api/v1/health` - Estado de la API
- `/api/v1/credito/statistics` - Estadísticas de análisis

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Email: soporte@finova.com
- GitHub Issues: [Crear Issue](https://github.com/COMPUMAX-EC/hack-ia/issues)

---

**FINOVA** - Democratizando el acceso a servicios financieros con IA 🚀
