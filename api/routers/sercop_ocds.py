"""
ROUTERS SERCOP OCDS
Endpoints para integración con API de Contrataciones Abiertas Ecuador
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime

from ..services.langchain_service import LangChainService
from ..services.ocds_sercop_integration import OCDSSercop, SERCOPIntegratedService

router = APIRouter(prefix="/sercop", tags=["SERCOP OCDS"])

# Instancias de servicios
ocds_client = OCDSSercop()
langchain_service = LangChainService()
sercop_integrated = SERCOPIntegratedService(langchain_service)

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
    
    return recomendaciones
