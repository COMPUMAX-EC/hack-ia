"""
INTEGRACIÓN API OCDS - SERCOP ECUADOR
Servicio Nacional de Contratación Pública
API de Contrataciones Abiertas Ecuador - Datos públicos oficiales
"""

import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from urllib.parse import quote
import json

class OCDSSercop:
    """
    Cliente oficial para API de Contrataciones Abiertas Ecuador (OCDS)
    URL Base: https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/
    """
    
    def __init__(self):
        self.base_url = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api"
        self.search_endpoint = f"{self.base_url}/search_ocds"
        self.record_endpoint = f"{self.base_url}/record"
        
        # Configuración de cliente HTTP
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.headers = {
            'User-Agent': 'OptimizacionLicitacionesIA/1.0 Ecuador',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Logger
        self.logger = logging.getLogger("OCDS_SERCOP")
        
    async def buscar_licitaciones(
        self, 
        year: int, 
        search: str,
        page: int = 1,
        buyer: Optional[str] = None,
        supplier: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Buscar procesos de contratación por palabra clave
        
        Parámetros:
        - year: Año del proceso (2015 - año actual)
        - search: Palabra clave (mínimo 3 caracteres)
        - page: Página de resultados (opcional)
        - buyer: Institución compradora (opcional)
        - supplier: Proveedor específico (opcional)
        """
        try:
            # Validar parámetros
            if year < 2015 or year > datetime.now().year:
                raise ValueError(f"Año debe estar entre 2015 y {datetime.now().year}")
            
            if len(search) < 3:
                raise ValueError("La búsqueda debe tener al menos 3 caracteres")
            
            # Construir parámetros
            params = {
                'year': year,
                'search': search,
                'page': page
            }
            
            if buyer and len(buyer) >= 3:
                params['buyer'] = buyer
                
            if supplier and len(supplier) >= 3:
                params['supplier'] = supplier
            
            self.logger.info(f"Buscando licitaciones: {search} ({year})")
            
            async with aiohttp.ClientSession(
                timeout=self.timeout, 
                headers=self.headers
            ) as session:
                async with session.get(self.search_endpoint, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Procesar y enriquecer resultados
                        processed_data = self._process_search_results(data)
                        
                        self.logger.info(f"Encontradas {data.get('total', 0)} licitaciones")
                        return processed_data
                    else:
                        error_msg = f"Error API OCDS: {response.status}"
                        self.logger.error(error_msg)
                        return {"error": error_msg, "total": 0, "data": []}
        
        except Exception as e:
            self.logger.error(f"Error en búsqueda OCDS: {str(e)}")
            return {"error": str(e), "total": 0, "data": []}
    
    async def obtener_proceso_completo(self, ocid: str) -> Dict[str, Any]:
        """
        Obtener información completa de un proceso por OCID
        
        Parámetros:
        - ocid: Identificador OCDS del proceso
        """
        try:
            self.logger.info(f"Obteniendo proceso completo: {ocid}")
            
            params = {'ocid': ocid}
            
            async with aiohttp.ClientSession(
                timeout=self.timeout,
                headers=self.headers
            ) as session:
                async with session.get(self.record_endpoint, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Procesar datos del proceso completo
                        processed_record = self._process_full_record(data)
                        
                        self.logger.info(f"Proceso {ocid} obtenido exitosamente")
                        return processed_record
                    else:
                        error_msg = f"Error obteniendo proceso {ocid}: {response.status}"
                        self.logger.error(error_msg)
                        return {"error": error_msg}
        
        except Exception as e:
            self.logger.error(f"Error obteniendo proceso {ocid}: {str(e)}")
            return {"error": str(e)}
    
    async def buscar_por_categoria(self, categoria: str, year: int = 2024) -> List[Dict[str, Any]]:
        """
        Buscar licitaciones por categoría específica
        """
        categorias_construccion = [
            "construccion", "obra", "infraestructura", "edificacion", 
            "carretera", "puente", "hospital", "escuela", "vial"
        ]
        
        categorias_tecnologia = [
            "software", "hardware", "sistema", "tecnologia", "informatico",
            "computadora", "servidor", "red"
        ]
        
        categorias_servicios = [
            "consultoria", "asesoria", "capacitacion", "servicio",
            "mantenimiento", "limpieza", "seguridad"
        ]
        
        # Determinar palabras clave según categoría
        if categoria.lower() in ["construccion", "obra"]:
            keywords = categorias_construccion
        elif categoria.lower() in ["tecnologia", "software"]:
            keywords = categorias_tecnologia
        elif categoria.lower() in ["servicios", "consultoria"]:
            keywords = categorias_servicios
        else:
            keywords = [categoria]
        
        # Buscar con múltiples palabras clave
        all_results = []
        
        for keyword in keywords[:3]:  # Limitar a 3 búsquedas por categoría
            result = await self.buscar_licitaciones(year=year, search=keyword)
            if result.get("data"):
                all_results.extend(result["data"])
        
        # Eliminar duplicados por OCID
        unique_results = {}
        for item in all_results:
            ocid = item.get("ocid")
            if ocid and ocid not in unique_results:
                unique_results[ocid] = item
        
        return list(unique_results.values())
    
    async def obtener_licitaciones_activas(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Obtener licitaciones activas del año actual
        """
        current_year = datetime.now().year
        
        # Buscar términos generales para obtener variedad
        search_terms = ["servicio", "obra", "bienes", "consultoria", "suministro"]
        
        all_active = []
        
        for term in search_terms:
            result = await self.buscar_licitaciones(year=current_year, search=term)
            if result.get("data"):
                all_active.extend(result["data"])
            
            # Limitar para evitar sobrecarga
            if len(all_active) >= limit * 2:
                break
        
        # Filtrar y ordenar por fecha más reciente
        unique_active = {}
        for item in all_active:
            ocid = item.get("ocid")
            if ocid and ocid not in unique_active:
                unique_active[ocid] = item
        
        # Ordenar por fecha (más recientes primero)
        sorted_active = sorted(
            unique_active.values(),
            key=lambda x: x.get("date", ""),
            reverse=True
        )
        
        return sorted_active[:limit]
    
    async def estadisticas_compras_publicas(self, year: int = 2024) -> Dict[str, Any]:
        """
        Obtener estadísticas generales de compras públicas
        """
        stats = {
            "year": year,
            "total_procesos": 0,
            "valor_total_estimado": 0,
            "por_tipo": {},
            "por_provincia": {},
            "procesos_recientes": [],
            "entidades_mas_activas": {}
        }
        
        try:
            # Buscar con términos generales
            general_search = await self.buscar_licitaciones(year=year, search="proceso")
            
            if general_search.get("data"):
                stats["total_procesos"] = general_search.get("total", 0)
                
                # Analizar tipos de proceso
                for proceso in general_search["data"][:50]:  # Muestra de 50
                    tipo = proceso.get("internal_type", "No especificado")
                    stats["por_tipo"][tipo] = stats["por_tipo"].get(tipo, 0) + 1
                    
                    # Extraer provincia del comprador
                    buyer_name = proceso.get("buyerName", "")
                    provincia = self._extraer_provincia(buyer_name)
                    stats["por_provincia"][provincia] = stats["por_provincia"].get(provincia, 0) + 1
                    
                    # Entidades más activas
                    buyer = proceso.get("buyerName", "")
                    stats["entidades_mas_activas"][buyer] = stats["entidades_mas_activas"].get(buyer, 0) + 1
                
                # Procesos más recientes
                stats["procesos_recientes"] = general_search["data"][:10]
        
        except Exception as e:
            self.logger.error(f"Error calculando estadísticas: {str(e)}")
            stats["error"] = str(e)
        
        return stats
    
    def _process_search_results(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar y enriquecer resultados de búsqueda"""
        if not data.get("data"):
            return data
        
        processed_data = data.copy()
        
        for item in processed_data["data"]:
            # Enriquecer con información adicional
            item["monto_estimado"] = self._estimar_monto(item.get("description", ""))
            item["categoria_inferred"] = self._inferir_categoria(item.get("description", ""))
            item["complejidad"] = self._evaluar_complejidad(item.get("description", ""))
            item["provincia"] = self._extraer_provincia(item.get("buyerName", ""))
            
            # Formatear fecha
            if item.get("date"):
                try:
                    date_obj = datetime.fromisoformat(item["date"].replace("Z", "+00:00"))
                    item["fecha_formateada"] = date_obj.strftime("%d/%m/%Y")
                    item["dias_desde_publicacion"] = (datetime.now() - date_obj.replace(tzinfo=None)).days
                except:
                    item["fecha_formateada"] = item["date"]
                    item["dias_desde_publicacion"] = 0
        
        return processed_data
    
    def _process_full_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Procesar registro completo de proceso OCDS"""
        if not data.get("records"):
            return data
        
        record = data["records"][0] if data["records"] else {}
        releases = record.get("releases", [])
        
        if not releases:
            return data
        
        latest_release = releases[-1]  # Último release
        
        # Extraer información clave
        processed = {
            "ocid": record.get("ocid"),
            "basic_info": {
                "title": latest_release.get("title", ""),
                "description": latest_release.get("description", ""),
                "date": latest_release.get("date"),
                "buyer": latest_release.get("buyer", {}),
                "tags": latest_release.get("tag", [])
            },
            "planning": self._extract_planning_info(latest_release),
            "tender": self._extract_tender_info(latest_release),
            "awards": self._extract_awards_info(latest_release),
            "contracts": self._extract_contracts_info(latest_release),
            "analysis": {
                "stage": self._determine_process_stage(latest_release),
                "estimated_value": self._extract_estimated_value(latest_release),
                "risk_factors": self._identify_risk_factors(latest_release),
                "recommendations": self._generate_recommendations(latest_release)
            },
            "raw_data": data  # Mantener datos originales
        }
        
        return processed
    
    def _extract_planning_info(self, release: Dict) -> Dict[str, Any]:
        """Extraer información de planificación"""
        planning = release.get("planning", {})
        return {
            "budget": planning.get("budget", {}),
            "rationale": planning.get("rationale", ""),
            "documents": planning.get("documents", [])
        }
    
    def _extract_tender_info(self, release: Dict) -> Dict[str, Any]:
        """Extraer información de licitación"""
        tender = release.get("tender", {})
        return {
            "id": tender.get("id", ""),
            "title": tender.get("title", ""),
            "description": tender.get("description", ""),
            "status": tender.get("status", ""),
            "value": tender.get("value", {}),
            "period": tender.get("tenderPeriod", {}),
            "documents": tender.get("documents", []),
            "items": tender.get("items", [])
        }
    
    def _extract_awards_info(self, release: Dict) -> List[Dict[str, Any]]:
        """Extraer información de adjudicaciones"""
        return release.get("awards", [])
    
    def _extract_contracts_info(self, release: Dict) -> List[Dict[str, Any]]:
        """Extraer información de contratos"""
        return release.get("contracts", [])
    
    def _determine_process_stage(self, release: Dict) -> str:
        """Determinar etapa del proceso"""
        tags = release.get("tag", [])
        
        if "planning" in tags and len(tags) == 1:
            return "PLANIFICACION"
        elif "tender" in tags:
            return "LICITACION_ACTIVA"
        elif "award" in tags:
            return "ADJUDICADO"
        elif "contract" in tags:
            return "CONTRATADO"
        else:
            return "DESCONOCIDO"
    
    def _extract_estimated_value(self, release: Dict) -> float:
        """Extraer valor estimado del proceso"""
        # Buscar en diferentes lugares donde puede estar el valor
        sources = [
            release.get("tender", {}).get("value", {}),
            release.get("planning", {}).get("budget", {}),
            release.get("awards", [{}])[0].get("value", {}) if release.get("awards") else {}
        ]
        
        for source in sources:
            amount = source.get("amount")
            if amount:
                try:
                    return float(amount)
                except:
                    continue
        
        return 0.0
    
    def _identify_risk_factors(self, release: Dict) -> List[str]:
        """Identificar factores de riesgo"""
        risks = []
        
        # Evaluar valor del contrato
        value = self._extract_estimated_value(release)
        if value > 5000000:  # Más de 5M USD
            risks.append("Contrato de alto valor - Requiere supervisión especial")
        
        # Evaluar plazo de licitación
        tender_period = release.get("tender", {}).get("tenderPeriod", {})
        if tender_period:
            start_date = tender_period.get("startDate")
            end_date = tender_period.get("endDate")
            if start_date and end_date:
                # Calcular días de licitación
                try:
                    start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                    end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    days = (end - start).days
                    
                    if days < 15:
                        risks.append("Plazo de licitación muy corto - Posible limitación de competencia")
                except:
                    pass
        
        # Evaluar complejidad técnica
        description = release.get("description", "").lower()
        complex_keywords = ["especializado", "complejo", "tecnología avanzada", "específico"]
        if any(keyword in description for keyword in complex_keywords):
            risks.append("Alta complejidad técnica - Requiere evaluadores especializados")
        
        return risks
    
    def _generate_recommendations(self, release: Dict) -> List[str]:
        """Generar recomendaciones específicas"""
        recommendations = []
        
        # Recomendar según etapa
        stage = self._determine_process_stage(release)
        
        if stage == "LICITACION_ACTIVA":
            recommendations.append("Revisar documentos de licitación para oportunidades de negocio")
            recommendations.append("Analizar competencia y capacidad técnica requerida")
        
        elif stage == "ADJUDICADO":
            recommendations.append("Analizar criterios de adjudicación para futuros procesos")
            recommendations.append("Estudiar propuesta ganadora como referencia")
        
        # Recomendar según valor
        value = self._extract_estimated_value(release)
        if value > 1000000:
            recommendations.append("Considerar alianzas estratégicas para contratos de alto valor")
        
        return recommendations
    
    def _estimar_monto(self, description: str) -> str:
        """Estimar monto basado en descripción"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ["hospital", "puente", "carretera", "universidad"]):
            return "Alto (>$1M)"
        elif any(word in desc_lower for word in ["escuela", "centro", "edificio", "sistema"]):
            return "Medio ($100K-$1M)"
        else:
            return "Bajo (<$100K)"
    
    def _inferir_categoria(self, description: str) -> str:
        """Inferir categoría del proceso"""
        if not description:
            return "Otros Servicios"
            
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ["construccion", "obra", "edificacion", "infraestructura"]):
            return "Construcción e Infraestructura"
        elif any(word in desc_lower for word in ["software", "sistema", "tecnologia", "informatico"]):
            return "Tecnología e Informática"
        elif any(word in desc_lower for word in ["consultoria", "asesoria", "capacitacion"]):
            return "Servicios de Consultoría"
        elif any(word in desc_lower for word in ["suministro", "adquisicion", "compra"]):
            return "Suministros y Bienes"
        else:
            return "Otros Servicios"
    
    def _evaluar_complejidad(self, description: str) -> str:
        """Evaluar complejidad del proceso"""
        desc_lower = description.lower()
        
        complex_indicators = len([
            word for word in ["especializado", "tecnico", "complejo", "especifico", "avanzado"]
            if word in desc_lower
        ])
        
        if complex_indicators >= 2:
            return "Alta"
        elif complex_indicators == 1:
            return "Media"
        else:
            return "Baja"
    
    def _extraer_provincia(self, buyer_name: str) -> str:
        """Extraer provincia del nombre del comprador"""
        provincias = [
            "AZUAY", "BOLIVAR", "CAÑAR", "CARCHI", "CHIMBORAZO", "COTOPAXI",
            "EL ORO", "ESMERALDAS", "GALAPAGOS", "GUAYAS", "IMBABURA", "LOJA",
            "LOS RIOS", "MANABI", "MORONA SANTIAGO", "NAPO", "ORELLANA",
            "PASTAZA", "PICHINCHA", "SANTA ELENA", "SANTO DOMINGO", "SUCUMBIOS",
            "TUNGURAHUA", "ZAMORA CHINCHIPE"
        ]
        
        buyer_upper = buyer_name.upper()
        
        for provincia in provincias:
            if provincia in buyer_upper:
                return provincia.title()
        
        # Casos especiales
        if "QUITO" in buyer_upper or "PICHINCHA" in buyer_upper:
            return "Pichincha"
        elif "GUAYAQUIL" in buyer_upper:
            return "Guayas"
        elif "CUENCA" in buyer_upper:
            return "Azuay"
        
        return "No identificada"


# SERVICIO INTEGRADO PARA LA API
class SERCOPIntegratedService:
    """
    Servicio integrado que combina OCDS con nuestro sistema de análisis IA
    """
    
    def __init__(self, langchain_service=None):
        self.ocds_client = OCDSSercop()
        self.langchain_service = langchain_service
        self.logger = logging.getLogger("SERCOP_Integrated")
    
    async def analizar_licitacion_ocds(self, ocid: str) -> Dict[str, Any]:
        """
        Análisis completo de una licitación usando OCDS + IA
        """
        try:
            # 1. Obtener datos completos de OCDS
            proceso_completo = await self.ocds_client.obtener_proceso_completo(ocid)
            
            if proceso_completo.get("error"):
                return {"error": f"No se pudo obtener proceso {ocid}"}
            
            # 2. Extraer contenido para análisis IA
            description = proceso_completo.get("basic_info", {}).get("description", "")
            tender_info = proceso_completo.get("tender", {})
            
            content_for_analysis = f"""
            PROCESO DE CONTRATACIÓN PÚBLICA ECUADOR
            OCID: {ocid}
            
            DESCRIPCIÓN:
            {description}
            
            INFORMACIÓN DE LICITACIÓN:
            Título: {tender_info.get('title', 'N/A')}
            Estado: {tender_info.get('status', 'N/A')}
            Valor Estimado: ${proceso_completo.get('analysis', {}).get('estimated_value', 0):,.2f}
            
            ENTIDAD COMPRADORA:
            {proceso_completo.get('basic_info', {}).get('buyer', {}).get('name', 'N/A')}
            """
            
            # 3. Análisis con IA si está disponible
            ai_analysis = {}
            if self.langchain_service:
                try:
                    ai_analysis = await self.langchain_service.analyze_licitacion_document(
                        document_content=content_for_analysis,
                        document_type="Proceso SERCOP OCDS"
                    )
                except Exception as e:
                    self.logger.warning(f"Error en análisis IA: {str(e)}")
                    ai_analysis = {"error": "Análisis IA no disponible"}
            
            # 4. Combinar resultados
            resultado_integrado = {
                "ocid": ocid,
                "datos_sercop": proceso_completo,
                "analisis_ia": ai_analysis,
                "resumen_ejecutivo": {
                    "titulo": tender_info.get("title", ""),
                    "entidad": proceso_completo.get("basic_info", {}).get("buyer", {}).get("name", ""),
                    "valor_estimado": proceso_completo.get("analysis", {}).get("estimated_value", 0),
                    "etapa": proceso_completo.get("analysis", {}).get("stage", ""),
                    "riesgos_sercop": proceso_completo.get("analysis", {}).get("risk_factors", []),
                    "score_ia": ai_analysis.get("score", 0),
                    "riesgo_ia": ai_analysis.get("risk_level", "N/A"),
                    "recomendaciones": (
                        proceso_completo.get("analysis", {}).get("recommendations", []) +
                        ai_analysis.get("recommendations", [])
                    )
                },
                "timestamp": datetime.now().isoformat()
            }
            
            return resultado_integrado
            
        except Exception as e:
            self.logger.error(f"Error en análisis integrado {ocid}: {str(e)}")
            return {"error": str(e)}
    
    async def dashboard_licitaciones_activas(self) -> Dict[str, Any]:
        """
        Dashboard con licitaciones activas del SERCOP
        """
        try:
            # Obtener licitaciones activas
            licitaciones_activas = await self.ocds_client.obtener_licitaciones_activas(limit=15)
            
            # Obtener estadísticas
            estadisticas = await self.ocds_client.estadisticas_compras_publicas()
            
            # Procesar para dashboard
            dashboard_data = {
                "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "resumen": {
                    "total_procesos_year": estadisticas.get("total_procesos", 0),
                    "procesos_activos": len(licitaciones_activas),
                    "valor_total_estimado": sum(
                        self._extract_value_safe(proc) for proc in licitaciones_activas
                    ),
                    "categorias_principales": estadisticas.get("por_tipo", {}),
                    "provincias_activas": estadisticas.get("por_provincia", {})
                },
                "licitaciones_destacadas": licitaciones_activas[:5],
                "oportunidades_construccion": [
                    proc for proc in licitaciones_activas 
                    if "construccion" in proc.get("description", "").lower() 
                    or "obra" in proc.get("description", "").lower()
                ][:3],
                "oportunidades_tecnologia": [
                    proc for proc in licitaciones_activas 
                    if any(word in proc.get("description", "").lower() 
                           for word in ["software", "sistema", "tecnologia", "informatico"])
                ][:3],
                "alertas": self._generar_alertas(licitaciones_activas),
                "metricas": {
                    "promedio_dias_licitacion": self._calcular_promedio_dias(licitaciones_activas),
                    "entidades_mas_activas": list(estadisticas.get("entidades_mas_activas", {}).keys())[:5]
                }
            }
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Error generando dashboard: {str(e)}")
            return {"error": str(e)}
    
    def _extract_value_safe(self, proceso: Dict) -> float:
        """Extraer valor de manera segura"""
        try:
            # Buscar indicadores de valor en la descripción
            description = proceso.get("description", "").lower()
            
            # Valores típicos por tipo de proyecto
            if any(word in description for word in ["hospital", "universidad", "aeropuerto"]):
                return 5000000  # $5M estimado
            elif any(word in description for word in ["escuela", "centro salud", "puente"]):
                return 1000000  # $1M estimado
            elif any(word in description for word in ["carretera", "vial", "rehabilitacion"]):
                return 3000000  # $3M estimado
            elif any(word in description for word in ["consultoria", "software", "capacitacion"]):
                return 200000   # $200K estimado
            else:
                return 500000   # $500K promedio
        except:
            return 0
    
    def _generar_alertas(self, licitaciones: List[Dict]) -> List[str]:
        """Generar alertas relevantes"""
        alertas = []
        
        # Licitaciones de alto valor
        alto_valor = [proc for proc in licitaciones if self._extract_value_safe(proc) > 2000000]
        if alto_valor:
            alertas.append(f"{len(alto_valor)} licitaciones de alto valor (>$2M) disponibles")
        
        # Licitaciones recientes
        recientes = [
            proc for proc in licitaciones 
            if proc.get("dias_desde_publicacion", 999) <= 7
        ]
        if recientes:
            alertas.append(f"{len(recientes)} licitaciones publicadas en los últimos 7 días")
        
        # Oportunidades específicas
        construccion = [
            proc for proc in licitaciones 
            if "construccion" in proc.get("description", "").lower()
        ]
        if len(construccion) >= 3:
            alertas.append(f"Alta actividad en construcción: {len(construccion)} procesos activos")
        
        return alertas
    
    def _calcular_promedio_dias(self, licitaciones: List[Dict]) -> int:
        """Calcular promedio de días desde publicación"""
        try:
            dias = [proc.get("dias_desde_publicacion", 0) for proc in licitaciones if proc.get("dias_desde_publicacion")]
            return sum(dias) // len(dias) if dias else 0
        except:
            return 0


# EJEMPLO DE USO COMPLETO
async def demo_integracion_ocds():
    """
    Demostración completa de la integración OCDS SERCOP
    """
    print("🏛️ DEMO INTEGRACIÓN API OCDS - SERCOP ECUADOR")
    print("=" * 60)
    
    # Inicializar cliente
    ocds_client = OCDSSercop()
    
    # 1. Buscar licitaciones de construcción
    print("\n🔍 BUSCANDO LICITACIONES DE CONSTRUCCIÓN 2024...")
    construccion_2024 = await ocds_client.buscar_licitaciones(
        year=2024,
        search="construccion",
        page=1
    )
    
    print(f"✅ Encontradas: {construccion_2024.get('total', 0)} licitaciones")
    
    if construccion_2024.get("data"):
        # Mostrar primeros 3 resultados
        for i, proc in enumerate(construccion_2024["data"][:3], 1):
            print(f"\n📋 {i}. {proc.get('title', 'N/A')}")
            print(f"    Entidad: {proc.get('buyerName', 'N/A')}")
            print(f"    Fecha: {proc.get('fecha_formateada', 'N/A')}")
            print(f"    Categoría: {proc.get('categoria_inferred', 'N/A')}")
            print(f"    Complejidad: {proc.get('complejidad', 'N/A')}")
            print(f"    OCID: {proc.get('ocid', 'N/A')}")
    
    # 2. Análisis detallado de un proceso
    if construccion_2024.get("data"):
        ocid_ejemplo = construccion_2024["data"][0].get("ocid")
        if ocid_ejemplo:
            print(f"\n🔍 ANÁLISIS DETALLADO: {ocid_ejemplo}")
            proceso_completo = await ocds_client.obtener_proceso_completo(ocid_ejemplo)
            
            if not proceso_completo.get("error"):
                print(f"✅ Proceso obtenido exitosamente")
                print(f"    Etapa: {proceso_completo.get('analysis', {}).get('stage', 'N/A')}")
                print(f"    Valor estimado: ${proceso_completo.get('analysis', {}).get('estimated_value', 0):,.2f}")
                
                riesgos = proceso_completo.get('analysis', {}).get('risk_factors', [])
                if riesgos:
                    print(f"    Riesgos detectados: {len(riesgos)}")
                    for riesgo in riesgos[:2]:
                        print(f"      - {riesgo}")
    
    # 3. Estadísticas generales
    print(f"\n📊 ESTADÍSTICAS COMPRAS PÚBLICAS 2024...")
    stats = await ocds_client.estadisticas_compras_publicas(2024)
    
    print(f"✅ Total procesos: {stats.get('total_procesos', 0)}")
    print(f"✅ Tipos principales:")
    for tipo, cantidad in list(stats.get('por_tipo', {}).items())[:3]:
        print(f"    - {tipo}: {cantidad}")
    
    print(f"✅ Provincias activas:")
    for provincia, cantidad in list(stats.get('por_provincia', {}).items())[:3]:
        print(f"    - {provincia}: {cantidad}")
    
    # 4. Dashboard integrado
    print(f"\n📈 GENERANDO DASHBOARD INTEGRADO...")
    servicio_integrado = SERCOPIntegratedService()
    dashboard = await servicio_integrado.dashboard_licitaciones_activas()
    
    if not dashboard.get("error"):
        resumen = dashboard.get("resumen", {})
        print(f"✅ Dashboard generado exitosamente")
        print(f"    Procesos activos: {resumen.get('procesos_activos', 0)}")
        print(f"    Valor total estimado: ${resumen.get('valor_total_estimado', 0):,.2f}")
        print(f"    Oportunidades construcción: {len(dashboard.get('oportunidades_construccion', []))}")
        print(f"    Oportunidades tecnología: {len(dashboard.get('oportunidades_tecnologia', []))}")
        
        alertas = dashboard.get("alertas", [])
        if alertas:
            print(f"    Alertas activas: {len(alertas)}")
            for alerta in alertas[:2]:
                print(f"      🚨 {alerta}")
    
    print(f"\n🎉 DEMO COMPLETADO - INTEGRACIÓN OCDS FUNCIONAL")


if __name__ == "__main__":
    # Ejecutar demo
    asyncio.run(demo_integracion_ocds())
