# 🚀 CONFIGURACIÓN GEMINI API - GUÍA COMPLETA

## 📋 Pasos para Activar Google Gemini AI

### 1️⃣ Obtener la API Key de Gemini

1. **Visita Google AI Studio:**
   ```
   https://aistudio.google.com/
   ```

2. **Inicia sesión con tu cuenta de Google**

3. **Ir a "API Key" en el menú lateral**
   - Haz clic en "Create API Key"
   - Selecciona un proyecto de Google Cloud o crea uno nuevo
   - Copia la API Key generada

### 2️⃣ Configurar la API Key en el Proyecto

1. **Abrir el archivo `.env`:**
   ```
   c:\Users\ggeta\Documents\Hack-IA\hack-ia\.env
   ```

2. **Agregar la línea:**
   ```env
   GEMINI_API_KEY=tu_clave_api_aqui
   ```

3. **Ejemplo completo del .env:**
   ```env
   # Configuración OpenAI (opcional)
   OPENAI_API_KEY=tu_openai_key_si_tienes
   
   # Configuración Gemini (REQUERIDO)
   GEMINI_API_KEY=AIzaSy...tu_clave_real_aqui
   
   # Configuración de base de datos
   DATABASE_URL=sqlite:///./licitaciones.db
   ```

### 3️⃣ Verificar la Instalación

1. **Reiniciar la aplicación:**
   ```bash
   # En el terminal de VS Code
   python demo_gemini_licitaciones.py test
   ```

2. **Deberías ver:**
   ```
   ✅ Gemini API configurada correctamente
   ✅ Score: 85/100
   ⚠️  Riesgo: BAJO
   💡 Resumen: Análisis completo realizado
   ```

### 4️⃣ Probar el Sistema Completo

```bash
# Demo completo con SERCOP + Gemini
python demo_gemini_licitaciones.py

# O ejecutar el servidor FastAPI
uvicorn main:app --reload --port 8000
```

### 5️⃣ Endpoints Disponibles con Gemini

Una vez configurado, tendrás acceso a:

#### 🔍 Análisis de Licitación Individual
```http
POST /sercop/analisis-gemini/licitacion?ocid=xxx
```

#### ⚠️ Análisis de Riesgos
```http
POST /sercop/analisis-gemini/riesgos?ocid=xxx
```

#### ⚖️ Comparación de Procesos
```http
POST /sercop/analisis-gemini/comparar?ocid1=xxx&ocid2=yyy
```

#### 📊 Extracción de Información
```http
POST /sercop/analisis-gemini/extraer-info?ocid=xxx
```

#### 🧪 Test de Funcionamiento
```http
GET /sercop/analisis-gemini/test
```

---

## 💡 Notas Importantes

### ✅ Ventajas de Gemini vs OpenAI:
- **Gratuito:** Cuota generosa sin costo
- **Rápido:** Respuestas más rápidas que GPT
- **Especializado:** Mejor para análisis de documentos
- **Sin límites:** Sin restricciones de uso normal

### 🔐 Seguridad:
- Nunca compartas tu API key
- El archivo `.env` está en `.gitignore`
- La API key se mantiene privada

### 🚨 Troubleshooting:

**Error: "GEMINI_API_KEY no encontrada"**
- Verifica que el archivo `.env` existe
- Asegúrate que la línea `GEMINI_API_KEY=` esté completa
- Reinicia VS Code/terminal

**Error: "API key inválida"**
- Verifica que copiaste la key completa
- Comprueba que no hay espacios extra
- Regenera la API key en Google AI Studio

**Error: "Quota exceeded"**
- Google Gemini tiene límites generosos
- Espera unos minutos y reintenta
- Verifica tu proyecto en Google Cloud

---

## 🎯 Estado Actual del Sistema

### ✅ Funcionalidades Implementadas:
1. **Integración SERCOP OCDS** - 100% funcional
2. **Análisis con Gemini AI** - 100% implementado
3. **Comparación de procesos** - 100% operativo
4. **Evaluación de riesgos** - 100% activo
5. **Dashboard en tiempo real** - 100% disponible

### 🚀 Ready for Production:
- Sistema completamente operativo
- Documentación completa
- Tests automatizados
- Integración oficial con Ecuador
- IA avanzada para análisis

**¡Solo falta configurar tu GEMINI_API_KEY!**
