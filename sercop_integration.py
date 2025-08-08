"""
IMPLEMENTACIÓN ESPECÍFICA PARA PORTAL COMPRAS PÚBLICAS ECUADOR
Integración con SERCOP y validaciones gubernamentales oficiales
"""

import requests
import xmltodict
from datetime import datetime
import logging
from typing import Dict, List, Any
import asyncio
import aiohttp
from cryptography.fernet import Fernet
import jwt
import ssl
import certifi

class SERCOPIntegrationService:
    """
    Servicio de integración oficial con el Portal de Compras Públicas (SERCOP)
    """
    
    def __init__(self, config: Dict[str, str]):
        self.base_url = "https://www.compraspublicas.gob.ec"
        self.api_url = f"{self.base_url}/ProcesoContratacion/compras/"
        self.ws_url = f"{self.base_url}/WebServices/"
        
        # Credenciales oficiales
        self.username = config.get("SERCOP_USERNAME")
        self.password = config.get("SERCOP_PASSWORD")
        self.certificate_path = config.get("SERCOP_CERTIFICATE_PATH")
        self.private_key = config.get("SERCOP_PRIVATE_KEY")
        
        # Configurar autenticación
        self._setup_authentication()
        
        # Logger específico
        self.logger = logging.getLogger("SERCOP_Integration")
    
    def _setup_authentication(self):
        """Configurar autenticación con certificado digital"""
        self.session = requests.Session()
        
        # Cargar certificado digital empresarial
        if self.certificate_path:
            self.session.cert = (self.certificate_path, self.private_key)
        
        # Headers oficiales requeridos
        self.session.headers.update({
            'User-Agent': 'SistemaOptimizacionLicitaciones/1.0',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Version': '2.0'
        })
    
    async def get_active_tenders(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Obtener licitaciones activas del portal SERCOP
        """
        try:
            endpoint = f"{self.api_url}busquedaAvanzada.jsf"
            
            # Parámetros de búsqueda
            params = {
                'codigoEntidad': filters.get('entity_code', ''),
                'estadoProceso': 'PUBLICADO',
                'tipoContrato': filters.get('contract_type', 'OBRA'),
                'fechaDesde': filters.get('date_from', ''),
                'fechaHasta': filters.get('date_to', ''),
                'montoDesde': filters.get('amount_from', 0),
                'montoHasta': filters.get('amount_to', 999999999),
                'format': 'json'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, params=params, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_tender_list(data)
                    else:
                        self.logger.error(f"Error obteniendo licitaciones: {response.status}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"Error en get_active_tenders: {str(e)}")
            return []
    
    async def get_tender_documents(self, tender_code: str) -> Dict[str, List[str]]:
        """
        Descargar documentos oficiales de una licitación específica
        """
        try:
            endpoint = f"{self.api_url}documentosContrato/{tender_code}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, ssl=False) as response:
                    if response.status == 200:
                        documents_data = await response.json()
                        
                        # Organizar documentos por tipo
                        organized_docs = {
                            'pliegos': [],
                            'especificaciones': [],
                            'cronograma': [],
                            'presupuesto': [],
                            'otros': []
                        }
                        
                        for doc in documents_data.get('documentos', []):
                            doc_type = self._classify_document_type(doc['nombre'])
                            doc_url = f"{self.base_url}{doc['url']}"
                            
                            organized_docs[doc_type].append({
                                'name': doc['nombre'],
                                'url': doc_url,
                                'size': doc.get('tamaño', 0),
                                'date': doc.get('fecha', '')
                            })
                        
                        return organized_docs
                    
        except Exception as e:
            self.logger.error(f"Error obteniendo documentos: {str(e)}")
            return {}
    
    async def submit_proposal_analysis(self, tender_code: str, analysis_results: Dict[str, Any]) -> bool:
        """
        Enviar resultados del análisis de IA al portal SERCOP
        """
        try:
            endpoint = f"{self.api_url}analisisInteligente/{tender_code}"
            
            # Estructurar datos para SERCOP
            submission_data = {
                'codigoProceso': tender_code,
                'fechaAnalisis': datetime.now().isoformat(),
                'sistema': 'OptimizacionLicitacionesIA',
                'version': '1.0',
                'resultados': {
                    'cumplimientoTecnico': analysis_results.get('technical_compliance', 0),
                    'cumplimientoLegal': analysis_results.get('legal_compliance', 0),
                    'riesgosDetectados': analysis_results.get('risks', []),
                    'recomendaciones': analysis_results.get('recommendations', []),
                    'scoreGeneral': analysis_results.get('overall_score', 0),
                    'tiempoAnalisis': analysis_results.get('analysis_time', 0)
                },
                'documentosAnalizados': analysis_results.get('analyzed_documents', []),
                'certificacionIA': self._generate_ai_certification(analysis_results)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    endpoint, 
                    json=submission_data,
                    ssl=False
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            self.logger.error(f"Error enviando análisis: {str(e)}")
            return False
    
    def _parse_tender_list(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parsear lista de licitaciones del formato SERCOP"""
        tenders = []
        
        for item in data.get('procesos', []):
            tender = {
                'code': item.get('codigoProceso'),
                'title': item.get('objetoContrato'),
                'entity': item.get('entidadContratante'),
                'amount': item.get('presupuestoReferencial'),
                'deadline': item.get('fechaLimitePreguntas'),
                'status': item.get('estadoProceso'),
                'type': item.get('tipoContrato'),
                'url': f"{self.base_url}/ProcesoContratacion/compras/PC/informacionProcesoContratacion2.cpe?idSoliCompra={item.get('id')}"
            }
            tenders.append(tender)
        
        return tenders
    
    def _classify_document_type(self, document_name: str) -> str:
        """Clasificar tipo de documento según nombre"""
        name_lower = document_name.lower()
        
        if any(word in name_lower for word in ['pliego', 'condiciones', 'bases']):
            return 'pliegos'
        elif any(word in name_lower for word in ['especificacion', 'tecnica', 'requisito']):
            return 'especificaciones'
        elif any(word in name_lower for word in ['cronograma', 'plazo', 'calendario']):
            return 'cronograma'
        elif any(word in name_lower for word in ['presupuesto', 'precio', 'costo']):
            return 'presupuesto'
        else:
            return 'otros'
    
    def _generate_ai_certification(self, analysis_results: Dict[str, Any]) -> str:
        """Generar certificación digital del análisis de IA"""
        certification_data = {
            'timestamp': datetime.now().isoformat(),
            'system': 'OptimizacionLicitacionesIA',
            'version': '1.0',
            'confidence': analysis_results.get('confidence_score', 0),
            'checksum': hash(str(analysis_results))
        }
        
        # Generar JWT token como certificación
        token = jwt.encode(
            certification_data,
            self.private_key,
            algorithm='RS256'
        )
        
        return token


class GovernmentValidationService:
    """
    Servicio integrado para validaciones gubernamentales oficiales
    """
    
    def __init__(self, config: Dict[str, str]):
        self.sri_service = SRIValidationService(config)
        self.scvs_service = SCVSValidationService(config)
        self.iess_service = IESSValidationService(config)
        self.logger = logging.getLogger("Government_Validation")
    
    async def comprehensive_contractor_validation(self, ruc: str) -> Dict[str, Any]:
        """
        Validación integral de contratista con todos los organismos
        """
        try:
            # Ejecutar validaciones en paralelo
            tasks = [
                self.sri_service.validate_tax_status(ruc),
                self.scvs_service.get_company_financial_status(ruc),
                self.iess_service.validate_social_security_compliance(ruc)
            ]
            
            sri_result, scvs_result, iess_result = await asyncio.gather(*tasks)
            
            # Compilar resultado integral
            validation_result = {
                'ruc': ruc,
                'validation_date': datetime.now().isoformat(),
                'sri_validation': sri_result,
                'scvs_validation': scvs_result,
                'iess_validation': iess_result,
                'overall_status': self._determine_overall_status(sri_result, scvs_result, iess_result),
                'risk_factors': self._identify_risk_factors(sri_result, scvs_result, iess_result),
                'construction_capability': self._assess_construction_capability(scvs_result),
                'recommendations': self._generate_recommendations(sri_result, scvs_result, iess_result)
            }
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"Error en validación integral: {str(e)}")
            return {'error': str(e), 'status': 'validation_failed'}
    
    def _determine_overall_status(self, sri: Dict, scvs: Dict, iess: Dict) -> str:
        """Determinar estado general del contratista"""
        if all(result.get('status') == 'valid' for result in [sri, scvs, iess]):
            return 'APTO_PARA_CONTRATAR'
        elif any(result.get('status') == 'critical_error' for result in [sri, scvs, iess]):
            return 'NO_APTO'
        else:
            return 'REQUIERE_VERIFICACION'
    
    def _identify_risk_factors(self, sri: Dict, scvs: Dict, iess: Dict) -> List[str]:
        """Identificar factores de riesgo"""
        risks = []
        
        if sri.get('tax_arrears', 0) > 0:
            risks.append(f"Deudas tributarias: ${sri['tax_arrears']:,.2f}")
        
        if scvs.get('financial_health') == 'poor':
            risks.append("Situación financiera deficiente")
        
        if iess.get('social_security_debt', 0) > 0:
            risks.append("Deudas con IESS")
        
        return risks
    
    def _assess_construction_capability(self, scvs_data: Dict) -> Dict[str, Any]:
        """Evaluar capacidad de construcción"""
        return {
            'capital_adequacy': scvs_data.get('capital_social', 0) >= 50000,
            'financial_stability': scvs_data.get('financial_health') in ['good', 'excellent'],
            'years_in_business': scvs_data.get('years_active', 0),
            'construction_experience': scvs_data.get('construction_classification', False)
        }
    
    def _generate_recommendations(self, sri: Dict, scvs: Dict, iess: Dict) -> List[str]:
        """Generar recomendaciones basadas en validaciones"""
        recommendations = []
        
        if sri.get('status') != 'valid':
            recommendations.append("Regularizar situación tributaria antes de contratar")
        
        if scvs.get('financial_health') == 'poor':
            recommendations.append("Solicitar garantías adicionales por situación financiera")
        
        if iess.get('status') != 'compliant':
            recommendations.append("Verificar cumplimiento de obligaciones laborales")
        
        return recommendations


class SRIValidationService:
    """Servicio específico para validaciones SRI"""
    
    def __init__(self, config: Dict[str, str]):
        self.api_url = "https://srienlinea.sri.gob.ec/api/v1/"
        self.certificate_path = config.get("SRI_CERTIFICATE_PATH")
        self.session = self._setup_authenticated_session()
    
    def _setup_authenticated_session(self):
        """Configurar sesión autenticada con SRI"""
        session = requests.Session()
        if self.certificate_path:
            session.cert = self.certificate_path
        return session
    
    async def validate_tax_status(self, ruc: str) -> Dict[str, Any]:
        """Validar estado tributario en SRI"""
        try:
            endpoint = f"{self.api_url}contribuyentes/{ruc}/estado"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'valid' if data.get('activo') else 'inactive',
                            'tax_arrears': data.get('deudas_pendientes', 0),
                            'declarations_up_to_date': data.get('declaraciones_al_dia', False),
                            'registration_date': data.get('fecha_registro'),
                            'activity_code': data.get('codigo_actividad')
                        }
            
            return {'status': 'error', 'message': 'No se pudo validar en SRI'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


class SCVSValidationService:
    """Servicio específico para validaciones SCVS"""
    
    def __init__(self, config: Dict[str, str]):
        self.api_url = "https://www.supercias.gob.ec/portalscvs/api/v1/"
        self.username = config.get("SCVS_USERNAME")
        self.password = config.get("SCVS_PASSWORD")
    
    async def get_company_financial_status(self, ruc: str) -> Dict[str, Any]:
        """Obtener estado financiero de SCVS"""
        try:
            endpoint = f"{self.api_url}empresas/{ruc}/estado-financiero"
            
            auth = aiohttp.BasicAuth(self.username, self.password)
            
            async with aiohttp.ClientSession(auth=auth) as session:
                async with session.get(endpoint, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'valid',
                            'capital_social': data.get('capital_social', 0),
                            'financial_health': self._assess_financial_health(data),
                            'years_active': data.get('años_constitucion', 0),
                            'construction_classification': 'construccion' in data.get('actividad_economica', '').lower(),
                            'last_financial_statement': data.get('ultimo_estado_financiero')
                        }
            
            return {'status': 'error', 'message': 'No se pudo consultar SCVS'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _assess_financial_health(self, financial_data: Dict) -> str:
        """Evaluar salud financiera"""
        assets = financial_data.get('activos_totales', 0)
        liabilities = financial_data.get('pasivos_totales', 0)
        
        if assets > 0:
            debt_ratio = liabilities / assets
            if debt_ratio < 0.3:
                return 'excellent'
            elif debt_ratio < 0.6:
                return 'good'
            elif debt_ratio < 0.8:
                return 'fair'
            else:
                return 'poor'
        
        return 'unknown'


class IESSValidationService:
    """Servicio específico para validaciones IESS"""
    
    def __init__(self, config: Dict[str, str]):
        self.api_url = "https://www.iess.gob.ec/api/v1/"
        self.token = config.get("IESS_API_TOKEN")
    
    async def validate_social_security_compliance(self, ruc: str) -> Dict[str, Any]:
        """Validar cumplimiento de obligaciones con IESS"""
        try:
            endpoint = f"{self.api_url}empleadores/{ruc}/cumplimiento"
            
            headers = {'Authorization': f'Bearer {self.token}'}
            
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(endpoint, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'status': 'compliant' if data.get('al_dia') else 'non_compliant',
                            'social_security_debt': data.get('deuda_iess', 0),
                            'active_employees': data.get('afiliados_activos', 0),
                            'last_payment_date': data.get('ultimo_pago'),
                            'contribution_capacity': self._assess_contribution_capacity(data)
                        }
            
            return {'status': 'error', 'message': 'No se pudo consultar IESS'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _assess_contribution_capacity(self, iess_data: Dict) -> str:
        """Evaluar capacidad de aportes"""
        employees = iess_data.get('afiliados_activos', 0)
        
        if employees >= 50:
            return 'large_employer'
        elif employees >= 10:
            return 'medium_employer'
        elif employees >= 1:
            return 'small_employer'
        else:
            return 'no_employees'


# EJEMPLO DE USO INTEGRAL
async def ejemplo_integracion_completa():
    """
    Ejemplo de uso completo del sistema de integración
    """
    # Configuración
    config = {
        'SERCOP_USERNAME': 'usuario_empresa',
        'SERCOP_PASSWORD': 'password_seguro',
        'SERCOP_CERTIFICATE_PATH': '/certs/empresa.p12',
        'SERCOP_PRIVATE_KEY': '/certs/empresa.key',
        'SRI_CERTIFICATE_PATH': '/certs/sri_firma.p12',
        'SCVS_USERNAME': 'usuario_scvs',
        'SCVS_PASSWORD': 'password_scvs',
        'IESS_API_TOKEN': 'token_iess_autorizado'
    }
    
    # Inicializar servicios
    sercop_service = SERCOPIntegrationService(config)
    validation_service = GovernmentValidationService(config)
    
    # 1. Obtener licitaciones activas
    print("🔍 Obteniendo licitaciones activas...")
    active_tenders = await sercop_service.get_active_tenders({
        'contract_type': 'OBRA',
        'amount_from': 100000,
        'amount_to': 5000000
    })
    
    print(f"✅ Encontradas {len(active_tenders)} licitaciones")
    
    # 2. Analizar una licitación específica
    if active_tenders:
        tender = active_tenders[0]
        print(f"\n📋 Analizando: {tender['title']}")
        
        # Descargar documentos
        documents = await sercop_service.get_tender_documents(tender['code'])
        print(f"📄 Documentos encontrados: {sum(len(docs) for docs in documents.values())}")
        
        # 3. Validar un contratista
        test_ruc = "1791234567001"
        print(f"\n🏢 Validando contratista: {test_ruc}")
        
        validation_result = await validation_service.comprehensive_contractor_validation(test_ruc)
        print(f"📊 Estado general: {validation_result.get('overall_status')}")
        print(f"⚠️ Riesgos detectados: {len(validation_result.get('risk_factors', []))}")
        
        # 4. Simular envío de análisis
        analysis_results = {
            'technical_compliance': 92.5,
            'legal_compliance': 88.0,
            'overall_score': 90.2,
            'risks': ['Plazo ajustado', 'Especificación técnica compleja'],
            'recommendations': ['Revisar cronograma', 'Solicitar aclaraciones técnicas'],
            'analysis_time': 180,  # segundos
            'confidence_score': 94.8
        }
        
        success = await sercop_service.submit_proposal_analysis(tender['code'], analysis_results)
        print(f"📤 Análisis enviado: {'✅ Exitoso' if success else '❌ Error'}")

if __name__ == "__main__":
    # Ejecutar ejemplo completo
    asyncio.run(ejemplo_integracion_completa())
