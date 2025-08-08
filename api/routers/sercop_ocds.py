"""
ROUTERS SERCOP OCDS
Endpoints para integración con API de Contrataciones Abiertas Ecuador
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging
from datetime import datetime

from ..services.langchain_service import LangChainService
from ..services.ocds_sercop_integration import OCDSSercop, SERCOPIntegratedService
from ..services.gemini_service import GeminiLicitacionesService

router = APIRouter(prefix="/sercop", tags=["SERCOP OCDS"])

# Logger
logger = logging.getLogger("SERCOP_OCDS")

# Instancias de servicios
ocds_client = OCDSSercop()
langchain_service = LangChainService()
sercop_integrated = SERCOPIntegratedService(langchain_service)
gemini_service = GeminiLicitacionesService()

@router.get("/buscar", summary="Buscar licitaciones en SERCOP")
async def buscar_licitaciones(
    year: int = Query(..., description="Año del proceso (2015-2024)", ge=2015, le=2024),
    search: str = Query(..., description="Palabra clave (mínimo 3 caracteres)", min_length=3),
    page: int = Query(1, description="Página de resultados", ge=1),
    buyer: Optional[str] = Query(None, description="Institución compradora"),
    supplier: Optional[str] = Query(None, description="Proveedor específico")
):
    """
    Buscar procesos de contratación en SERCOP por palabra clave
    
    **Ejemplo de uso:**
    - `/sercop/buscar?year=2024&search=construccion&page=1`
    - `/sercop/buscar?year=2024&search=hospital&buyer=MINISTERIO DE SALUD`
    """
    try:
        resultado = await ocds_client.buscar_licitaciones(
            year=year,
            search=search,
            page=page,
            buyer=buyer,
            supplier=supplier
        )
        
        if resultado.get("error"):
            raise HTTPException(status_code=400, detail=resultado["error"])
        
        return {
            "success": True,
            "data": resultado,
            "metadata": {
                "query": {
                    "year": year,
                    "search": search,
                    "page": page,
                    "buyer": buyer,
                    "supplier": supplier
                },
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en búsqueda SERCOP: {str(e)}")

@router.get("/proceso/{ocid}", summary="Obtener proceso completo por OCID")
async def obtener_proceso_completo(
    ocid: str,
    incluir_analisis_ia: bool = Query(True, description="Incluir análisis con IA")
):
    """
    Obtener información completa de un proceso de contratación
    
    **Parámetros:**
    - `ocid`: Identificador OCDS del proceso (ej: ocds-5wno2w-001-LICO-GPLR-2020-2805)
    - `incluir_analisis_ia`: Si incluir análisis automático con IA
    """
    try:
        if incluir_analisis_ia:
            # Análisis completo con IA
            resultado = await sercop_integrated.analizar_licitacion_ocds(ocid)
        else:
            # Solo datos OCDS
            resultado = await ocds_client.obtener_proceso_completo(ocid)
        
        if resultado.get("error"):
            raise HTTPException(status_code=404, detail=f"Proceso {ocid} no encontrado")
        
        return {
            "success": True,
            "data": resultado,
            "metadata": {
                "ocid": ocid,
                "incluye_analisis_ia": incluir_analisis_ia,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo proceso: {str(e)}")

@router.get("/categorias/{categoria}", summary="Buscar por categoría específica")
async def buscar_por_categoria(
    categoria: str,
    year: int = Query(2024, description="Año de búsqueda", ge=2015, le=2024),
    limit: int = Query(20, description="Límite de resultados", ge=1, le=100)
):
    """
    Buscar licitaciones por categoría específica
    
    **Categorías disponibles:**
    - `construccion`: Obras de construcción e infraestructura
    - `tecnologia`: Software, hardware, sistemas informáticos
    - `servicios`: Consultoría, asesoría, capacitación
    - `suministros`: Bienes, materiales, equipos
    """
    try:
        resultados = await ocds_client.buscar_por_categoria(categoria, year)
        
        # Limitar resultados
        resultados_limitados = resultados[:limit]
        
        return {
            "success": True,
            "data": {
                "categoria": categoria,
                "year": year,
                "total_encontrados": len(resultados),
                "total_retornados": len(resultados_limitados),
                "procesos": resultados_limitados
            },
            "metadata": {
                "query": {"categoria": categoria, "year": year, "limit": limit},
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error buscando por categoría: {str(e)}")

@router.get("/activas", summary="Licitaciones activas del año actual")
async def obtener_licitaciones_activas(
    limit: int = Query(20, description="Número máximo de resultados", ge=1, le=100)
):
    """
    Obtener licitaciones activas del año actual
    
    **Retorna:**
    - Procesos más recientes ordenados por fecha
    - Información enriquecida con categorías y complejidad
    - Análisis básico de cada proceso
    """
    try:
        licitaciones = await ocds_client.obtener_licitaciones_activas(limit)
        
        return {
            "success": True,
            "data": {
                "year": datetime.now().year,
                "total_activas": len(licitaciones),
                "licitaciones": licitaciones,
                "resumen_categorias": _resumir_categorias(licitaciones),
                "resumen_provincias": _resumir_provincias(licitaciones)
            },
            "metadata": {
                "limit": limit,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo licitaciones activas: {str(e)}")

@router.get("/dashboard", summary="Dashboard completo compras públicas")
async def obtener_dashboard():
    """
    Dashboard completo con métricas y licitaciones activas
    
    **Incluye:**
    - Estadísticas generales del año
    - Licitaciones destacadas
    - Oportunidades por categoría
    - Alertas y recomendaciones
    - Métricas de actividad
    """
    try:
        dashboard = await sercop_integrated.dashboard_licitaciones_activas()
        
        if dashboard.get("error"):
            raise HTTPException(status_code=500, detail=dashboard["error"])
        
        return {
            "success": True,
            "data": dashboard,
            "metadata": {
                "tipo": "dashboard_completo",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando dashboard: {str(e)}")

@router.get("/estadisticas", summary="Estadísticas generales compras públicas")
async def obtener_estadisticas(
    year: int = Query(2024, description="Año para estadísticas", ge=2015, le=2024)
):
    """
    Estadísticas generales de compras públicas por año
    
    **Incluye:**
    - Total de procesos
    - Distribución por tipo
    - Distribución por provincia
    - Entidades más activas
    - Procesos recientes
    """
    try:
        estadisticas = await ocds_client.estadisticas_compras_publicas(year)
        
        if estadisticas.get("error"):
            raise HTTPException(status_code=500, detail=estadisticas["error"])
        
        return {
            "success": True,
            "data": estadisticas,
            "metadata": {
                "year": year,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.post("/analizar-multiple", summary="Analizar múltiples procesos con IA")
async def analizar_multiples_procesos(
    ocids: List[str],
    incluir_recomendaciones: bool = Query(True, description="Incluir recomendaciones de negocio")
):
    """
    Analizar múltiples procesos de contratación con IA
    
    **Parámetros:**
    - `ocids`: Lista de identificadores OCDS
    - `incluir_recomendaciones`: Si incluir recomendaciones específicas
    
    **Máximo:** 10 procesos por solicitud
    """
    try:
        if len(ocids) > 10:
            raise HTTPException(
                status_code=400, 
                detail="Máximo 10 procesos por solicitud"
            )
        
        # Analizar en paralelo
        tareas = [
            sercop_integrated.analizar_licitacion_ocds(ocid) 
            for ocid in ocids
        ]
        
        resultados = await asyncio.gather(*tareas, return_exceptions=True)
        
        # Procesar resultados
        analisis_exitosos = []
        errores = []
        
        for i, resultado in enumerate(resultados):
            if isinstance(resultado, Exception):
                errores.append({"ocid": ocids[i], "error": str(resultado)})
            elif resultado.get("error"):
                errores.append({"ocid": ocids[i], "error": resultado["error"]})
            else:
                analisis_exitosos.append(resultado)
        
        # Generar resumen comparativo
        resumen_comparativo = _generar_resumen_comparativo(analisis_exitosos)
        
        return {
            "success": True,
            "data": {
                "total_solicitados": len(ocids),
                "exitosos": len(analisis_exitosos),
                "errores": len(errores),
                "analisis_individuales": analisis_exitosos,
                "errores_detalle": errores,
                "resumen_comparativo": resumen_comparativo
            },
            "metadata": {
                "incluye_recomendaciones": incluir_recomendaciones,
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en análisis múltiple: {str(e)}")

@router.get("/oportunidades", summary="Identificar oportunidades de negocio")
async def identificar_oportunidades(
    categoria: Optional[str] = Query(None, description="Categoría específica"),
    valor_minimo: Optional[float] = Query(None, description="Valor mínimo del contrato"),
    provincia: Optional[str] = Query(None, description="Provincia específica")
):
    """
    Identificar oportunidades de negocio específicas
    
    **Filtros disponibles:**
    - `categoria`: construccion, tecnologia, servicios, suministros
    - `valor_minimo`: Valor mínimo estimado del contrato
    - `provincia`: Provincia específica
    """
    try:
        # Obtener licitaciones activas
        licitaciones_activas = await ocds_client.obtener_licitaciones_activas(50)
        
        # Aplicar filtros
        oportunidades_filtradas = licitaciones_activas
        
        if categoria:
            oportunidades_filtradas = [
                proc for proc in oportunidades_filtradas
                if categoria.lower() in proc.get("categoria_inferred", "").lower()
            ]
        
        if valor_minimo:
            oportunidades_filtradas = [
                proc for proc in oportunidades_filtradas
                if _extraer_valor_estimado(proc) >= valor_minimo
            ]
        
        if provincia:
            oportunidades_filtradas = [
                proc for proc in oportunidades_filtradas
                if provincia.upper() in proc.get("provincia", "").upper()
            ]
        
        # Ordenar por potencial (valor estimado + recencia)
        oportunidades_ordenadas = sorted(
            oportunidades_filtradas,
            key=lambda x: (
                _extraer_valor_estimado(x),
                -x.get("dias_desde_publicacion", 999)
            ),
            reverse=True
        )
        
        # Generar recomendaciones
        recomendaciones = _generar_recomendaciones_oportunidades(oportunidades_ordenadas)
        
        return {
            "success": True,
            "data": {
                "filtros_aplicados": {
                    "categoria": categoria,
                    "valor_minimo": valor_minimo,
                    "provincia": provincia
                },
                "total_oportunidades": len(oportunidades_ordenadas),
                "oportunidades_top": oportunidades_ordenadas[:10],
                "valor_total_estimado": sum(_extraer_valor_estimado(proc) for proc in oportunidades_ordenadas),
                "recomendaciones": recomendaciones
            },
            "metadata": {
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error identificando oportunidades: {str(e)}")

# FUNCIONES AUXILIARES
def _resumir_categorias(licitaciones: List[Dict]) -> Dict[str, int]:
    """Resumir licitaciones por categoría"""
    categorias = {}
    for proc in licitaciones:
        categoria = proc.get("categoria_inferred", "Otros")
        categorias[categoria] = categorias.get(categoria, 0) + 1
    return categorias

def _resumir_provincias(licitaciones: List[Dict]) -> Dict[str, int]:
    """Resumir licitaciones por provincia"""
    provincias = {}
    for proc in licitaciones:
        provincia = proc.get("provincia", "No identificada")
        provincias[provincia] = provincias.get(provincia, 0) + 1
    return provincias

def _extraer_valor_estimado(proceso: Dict) -> float:
    """Extraer valor estimado de un proceso"""
    description = proceso.get("description", "").lower()
    
    # Valores típicos por tipo de proyecto
    if any(word in description for word in ["hospital", "universidad", "aeropuerto"]):
        return 5000000
    elif any(word in description for word in ["escuela", "centro salud", "puente"]):
        return 1000000
    elif any(word in description for word in ["carretera", "vial", "rehabilitacion"]):
        return 3000000
    elif any(word in description for word in ["consultoria", "software", "capacitacion"]):
        return 200000
    else:
        return 500000

def _generar_resumen_comparativo(analisis: List[Dict]) -> Dict[str, Any]:
    """Generar resumen comparativo de múltiples análisis"""
    if not analisis:
        return {}
    
    # Extraer scores de IA
    scores = [
        a.get("analisis_ia", {}).get("score", 0) 
        for a in analisis 
        if a.get("analisis_ia", {}).get("score")
    ]
    
    # Extraer valores estimados
    valores = [
        a.get("datos_sercop", {}).get("analysis", {}).get("estimated_value", 0)
        for a in analisis
    ]
    
    return {
        "total_procesos": len(analisis),
        "score_promedio": sum(scores) / len(scores) if scores else 0,
        "score_maximo": max(scores) if scores else 0,
        "score_minimo": min(scores) if scores else 0,
        "valor_total": sum(valores),
        "valor_promedio": sum(valores) / len(valores) if valores else 0,
        "proceso_mejor_score": max(analisis, key=lambda x: x.get("analisis_ia", {}).get("score", 0)).get("ocid") if analisis else None,
        "proceso_mayor_valor": max(analisis, key=lambda x: x.get("datos_sercop", {}).get("analysis", {}).get("estimated_value", 0)).get("ocid") if analisis else None
    }

def _generar_recomendaciones_oportunidades(oportunidades: List[Dict]) -> List[str]:
    """Generar recomendaciones basadas en oportunidades"""
    if not oportunidades:
        return ["No se encontraron oportunidades con los filtros especificados"]
    
    recomendaciones = []
    
    # Analizar oportunidades top
    top_3 = oportunidades[:3]
    
    for i, oportunidad in enumerate(top_3, 1):
        titulo = oportunidad.get("title", "")[:50] + "..."
        valor = _extraer_valor_estimado(oportunidad)
        dias = oportunidad.get("dias_desde_publicacion", 0)
        
        recomendaciones.append(
            f"Oportunidad #{i}: {titulo} - Valor: ${valor:,.0f} - Publicado hace {dias} días"
        )
    
    # Recomendaciones generales
    categorias = _resumir_categorias(oportunidades)
    categoria_principal = max(categorias.items(), key=lambda x: x[1])[0] if categorias else None
    
    if categoria_principal:
        recomendaciones.append(f"Categoría predominante: {categoria_principal} ({categorias[categoria_principal]} procesos)")
    
    valor_total = sum(_extraer_valor_estimado(proc) for proc in oportunidades)
    recomendaciones.append(f"Valor total de oportunidades: ${valor_total:,.0f}")


# ==========================================
# ENDPOINTS GEMINI AI
# ==========================================

@router.post("/analisis-gemini/licitacion")
async def analizar_licitacion_gemini(
    ocid: str = Query(..., description="Identificador OCID del proceso"),
    incluir_documentos: bool = Query(True, description="Incluir análisis de documentos")
) -> Dict[str, Any]:
    """
    Análisis completo de licitación usando Google Gemini AI
    """
    try:
        # Obtener datos del proceso
        proceso = await ocds_client.get_release_by_ocid(ocid)
        if not proceso:
            raise HTTPException(status_code=404, detail="Proceso no encontrado")
        
        # Preparar contenido para análisis
        content = f"""
        PROCESO DE CONTRATACIÓN PÚBLICA
        
        ID: {proceso.get('ocid', '')}
        Título: {proceso.get('title', '')}
        Descripción: {proceso.get('description', '')}
        
        INFORMACIÓN BÁSICA:
        - Método de contratación: {proceso.get('tender', {}).get('procurementMethod', '')}
        - Estado: {proceso.get('tender', {}).get('status', '')}
        - Entidad: {proceso.get('buyer', {}).get('name', '')}
        - Valor estimado: {proceso.get('tender', {}).get('value', {}).get('amount', 0)}
        - Moneda: {proceso.get('tender', {}).get('value', {}).get('currency', 'USD')}
        
        CRONOGRAMA:
        - Fecha publicación: {proceso.get('tender', {}).get('datePublished', '')}
        - Fecha límite consultas: {proceso.get('tender', {}).get('enquiryPeriod', {}).get('endDate', '')}
        - Fecha límite ofertas: {proceso.get('tender', {}).get('tenderPeriod', {}).get('endDate', '')}
        
        CRITERIOS DE EVALUACIÓN:
        {json.dumps(proceso.get('tender', {}).get('awardCriteria', []), indent=2)}
        
        REQUISITOS:
        {json.dumps(proceso.get('tender', {}).get('eligibilityCriteria', ''), indent=2)}
        """
        
        # Obtener documentos si se solicita
        if incluir_documentos:
            documentos = proceso.get('tender', {}).get('documents', [])
            if documentos:
                content += "\n\nDOCUMENTOS DISPONIBLES:\n"
                for doc in documentos[:5]:  # Limitar a 5 documentos
                    content += f"- {doc.get('title', 'Sin título')}: {doc.get('description', 'Sin descripción')}\n"
        
        # Análisis con Gemini
        resultado = await gemini_service.analizar_documento_licitacion(
            document_content=content,
            document_type="Proceso SERCOP"
        )
        
        # Enriquecer con datos del proceso
        resultado.update({
            "ocid": ocid,
            "titulo_proceso": proceso.get('title', ''),
            "entidad_contratante": proceso.get('buyer', {}).get('name', ''),
            "valor_proceso": proceso.get('tender', {}).get('value', {}).get('amount', 0),
            "estado_proceso": proceso.get('tender', {}).get('status', ''),
            "fecha_analisis": datetime.now().isoformat(),
            "fuente_datos": "SERCOP OCDS API + Gemini AI"
        })
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en análisis Gemini: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en análisis: {str(e)}")


@router.post("/analisis-gemini/riesgos")
async def analizar_riesgos_gemini(
    ocid: str = Query(..., description="Identificador OCID del proceso")
) -> Dict[str, Any]:
    """
    Análisis específico de riesgos usando Gemini AI
    """
    try:
        # Obtener proceso
        proceso = await ocds_client.get_release_by_ocid(ocid)
        if not proceso:
            raise HTTPException(status_code=404, detail="Proceso no encontrado")
        
        # Preparar contenido para análisis de riesgos
        tender = proceso.get('tender', {})
        valor = tender.get('value', {}).get('amount', 0)
        
        content = f"""
        ANÁLISIS DE RIESGOS - PROCESO SERCOP
        
        Proyecto: {proceso.get('title', '')}
        Valor: ${valor:,.2f} {tender.get('value', {}).get('currency', 'USD')}
        Entidad: {proceso.get('buyer', {}).get('name', '')}
        Método: {tender.get('procurementMethod', '')}
        
        ESPECIFICACIONES TÉCNICAS:
        {tender.get('description', '')}
        
        CRITERIOS DE ELEGIBILIDAD:
        {tender.get('eligibilityCriteria', '')}
        
        DOCUMENTOS REQUERIDOS:
        {json.dumps([doc.get('title', '') for doc in tender.get('documents', [])], indent=2)}
        
        CRONOGRAMA:
        - Publicación: {tender.get('datePublished', '')}
        - Fin consultas: {tender.get('enquiryPeriod', {}).get('endDate', '')}
        - Fin ofertas: {tender.get('tenderPeriod', {}).get('endDate', '')}
        """
        
        # Análisis de riesgos con Gemini
        resultado = await gemini_service.analizar_riesgos_construccion(
            document_content=content,
            project_value=valor
        )
        
        # Agregar contexto del proceso
        resultado.update({
            "ocid": ocid,
            "valor_proyecto": valor,
            "metodo_contratacion": tender.get('procurementMethod', ''),
            "entidad_contratante": proceso.get('buyer', {}).get('name', ''),
            "fecha_analisis": datetime.now().isoformat()
        })
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en análisis de riesgos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/analisis-gemini/comparar")
async def comparar_procesos_gemini(
    ocid1: str = Query(..., description="Primer proceso a comparar"),
    ocid2: str = Query(..., description="Segundo proceso a comparar"),
    criterios: Optional[List[str]] = Query(None, description="Criterios específicos de comparación")
) -> Dict[str, Any]:
    """
    Comparación inteligente entre dos procesos usando Gemini AI
    """
    try:
        # Obtener ambos procesos
        proceso1 = await ocds_client.get_release_by_ocid(ocid1)
        proceso2 = await ocds_client.get_release_by_ocid(ocid2)
        
        if not proceso1 or not proceso2:
            raise HTTPException(status_code=404, detail="Uno o ambos procesos no encontrados")
        
        # Preparar contenido de ambos procesos
        def preparar_contenido_proceso(proceso, label):
            tender = proceso.get('tender', {})
            return f"""
            {label}:
            Título: {proceso.get('title', '')}
            Entidad: {proceso.get('buyer', {}).get('name', '')}
            Valor: ${tender.get('value', {}).get('amount', 0):,.2f}
            Método: {tender.get('procurementMethod', '')}
            Descripción: {tender.get('description', '')}
            Estado: {tender.get('status', '')}
            Criterios elegibilidad: {tender.get('eligibilityCriteria', '')}
            """
        
        propuesta1 = preparar_contenido_proceso(proceso1, "PROCESO A")
        propuesta2 = preparar_contenido_proceso(proceso2, "PROCESO B")
        
        # Comparación con Gemini
        resultado = await gemini_service.comparar_propuestas(
            propuesta1=propuesta1,
            propuesta2=propuesta2,
            criterios_evaluacion=criterios
        )
        
        # Enriquecer resultado
        resultado.update({
            "proceso_a": {
                "ocid": ocid1,
                "titulo": proceso1.get('title', ''),
                "valor": proceso1.get('tender', {}).get('value', {}).get('amount', 0)
            },
            "proceso_b": {
                "ocid": ocid2,
                "titulo": proceso2.get('title', ''),
                "valor": proceso2.get('tender', {}).get('value', {}).get('amount', 0)
            },
            "fecha_comparacion": datetime.now().isoformat()
        })
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en comparación: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/analisis-gemini/extraer-info")
async def extraer_informacion_gemini(
    ocid: str = Query(..., description="Identificador OCID del proceso")
) -> Dict[str, Any]:
    """
    Extracción inteligente de información clave usando Gemini AI
    """
    try:
        # Obtener proceso
        proceso = await ocds_client.get_release_by_ocid(ocid)
        if not proceso:
            raise HTTPException(status_code=404, detail="Proceso no encontrado")
        
        # Preparar contenido completo
        tender = proceso.get('tender', {})
        buyer = proceso.get('buyer', {})
        
        content = f"""
        DOCUMENTO DE CONTRATACIÓN PÚBLICA SERCOP
        
        INFORMACIÓN GENERAL:
        ID: {proceso.get('ocid', '')}
        Título: {proceso.get('title', '')}
        Descripción: {proceso.get('description', '')}
        
        ENTIDAD CONTRATANTE:
        Nombre: {buyer.get('name', '')}
        ID: {buyer.get('id', '')}
        
        PROCEDIMIENTO:
        Método: {tender.get('procurementMethod', '')}
        Estado: {tender.get('status', '')}
        Valor: ${tender.get('value', {}).get('amount', 0):,.2f}
        Moneda: {tender.get('value', {}).get('currency', 'USD')}
        
        CRONOGRAMA:
        Fecha publicación: {tender.get('datePublished', '')}
        Período consultas: {tender.get('enquiryPeriod', {}).get('startDate', '')} - {tender.get('enquiryPeriod', {}).get('endDate', '')}
        Período ofertas: {tender.get('tenderPeriod', {}).get('startDate', '')} - {tender.get('tenderPeriod', {}).get('endDate', '')}
        
        ESPECIFICACIONES:
        {tender.get('description', '')}
        
        CRITERIOS DE ELEGIBILIDAD:
        {tender.get('eligibilityCriteria', '')}
        
        CRITERIOS DE EVALUACIÓN:
        {json.dumps(tender.get('awardCriteria', []), indent=2)}
        
        DOCUMENTOS:
        {json.dumps([{'titulo': doc.get('title', ''), 'descripcion': doc.get('description', '')} for doc in tender.get('documents', [])], indent=2)}
        
        GARANTÍAS:
        {json.dumps(tender.get('guarantee', {}), indent=2)}
        """
        
        # Extracción con Gemini
        resultado = await gemini_service.extraer_informacion_clave(content)
        
        # Validar y complementar con datos directos
        resultado.update({
            "ocid_validado": proceso.get('ocid', ''),
            "titulo_validado": proceso.get('title', ''),
            "entidad_validada": buyer.get('name', ''),
            "valor_validado": tender.get('value', {}).get('amount', 0),
            "estado_validado": tender.get('status', ''),
            "fecha_extraccion": datetime.now().isoformat(),
            "fuente": "SERCOP OCDS + Gemini AI"
        })
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en extracción: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/analisis-gemini/test")
async def test_gemini_service() -> Dict[str, Any]:
    """
    Endpoint de prueba para verificar funcionamiento de Gemini
    """
    try:
        # Documento de prueba
        test_document = """
        LICITACIÓN PÚBLICA INTERNACIONAL
        Entidad: Ministerio de Transporte y Obras Públicas
        Objeto: Construcción de puente vehicular sobre río Pastaza
        Valor referencial: $2,500,000.00 USD
        Plazo: 18 meses
        
        Requisitos principales:
        - Experiencia mínima 10 años en construcción de puentes
        - Capacidad instalada certificada
        - Personal técnico especializado
        
        Garantías requeridas:
        - Garantía fiel cumplimiento: 10% del valor del contrato
        - Garantía técnica: 24 meses
        """
        
        # Análisis de prueba
        resultado = await gemini_service.analizar_licitacion_completa(
            document_content=test_document,
            document_type="Licitación de Prueba",
            entity_name="MTOP"
        )
        
        resultado.update({
            "test_status": "SUCCESS",
            "gemini_available": not gemini_service.use_simulation,
            "fecha_test": datetime.now().isoformat()
        })
        
        return resultado
        
    except Exception as e:
        logger.error(f"Error en test Gemini: {str(e)}")
        return {
            "test_status": "ERROR",
            "error": str(e),
            "gemini_available": False,
            "fecha_test": datetime.now().isoformat()
        }
    
    return recomendaciones
