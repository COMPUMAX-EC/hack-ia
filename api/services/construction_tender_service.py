from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import re
import requests
from dataclasses import dataclass
from .langchain_service import LangChainService

@dataclass
class DocumentSection:
    """Representa una sección de documento analizada"""
    section_type: str
    content: str
    compliance_score: float
    risk_level: str
    issues: List[str]
    recommendations: List[str]

@dataclass
class ContractorValidation:
    """Validación de contratista"""
    ruc: str
    company_name: str
    is_valid: bool
    legal_status: str
    can_perform_construction: bool
    risk_factors: List[str]
    
@dataclass
class ProposalComparison:
    """Comparación entre propuestas"""
    proposal_id: str
    company_name: str
    overall_score: float
    technical_score: float
    economic_score: float
    legal_score: float
    total_budget: float
    timeline_days: int
    compliance_percentage: float
    risk_level: str
    
class ConstructionTenderService:
    """
    Servicio especializado para optimización de procesos de licitación en construcción
    Reto 1 - Viamatica
    """
    
    def __init__(self):
        self.langchain_service = LangChainService()
        self.processed_documents = []
        self.proposals_database = []
        
        # Configuración específica para construcción
        self.construction_keywords = {
            'materials': ['cemento', 'acero', 'hierro', 'hormigón', 'concreto', 'arena', 'grava', 'ladrillo'],
            'processes': ['excavación', 'cimentación', 'estructura', 'acabados', 'instalaciones'],
            'regulations': ['código de construcción', 'normas sísmicas', 'permisos municipales', 'seguridad industrial'],
            'timeline': ['cronograma', 'plazo', 'entrega', 'hitos', 'fases'],
            'quality': ['calidad', 'especificaciones', 'normas', 'certificaciones', 'ensayos']
        }
        
        # Pesos para evaluación
        self.evaluation_weights = {
            'technical': 0.40,  # Aspectos técnicos (40%)
            'economic': 0.35,   # Propuesta económica (35%)  
            'legal': 0.15,     # Cumplimiento legal (15%)
            'timeline': 0.10    # Cronograma (10%)
        }
    
    async def analyze_tender_document(
        self, 
        document_content: str, 
        document_type: str,
        filename: str = None
    ) -> Dict[str, Any]:
        """
        Análisis integral de documento de licitación
        """
        try:
            print(f"Analizando documento: {document_type}")
            
            # 1. Clasificación automática del documento
            classified_type = self._classify_document(document_content)
            
            # 2. Extracción de secciones clave
            sections = self._extract_key_sections(document_content, classified_type)
            
            # 3. Análisis con IA
            ai_analysis = await self._ai_document_analysis(document_content, classified_type)
            
            # 4. Validación de cumplimiento
            compliance_check = self._check_compliance(sections, classified_type)
            
            # 5. Detección de riesgos
            risk_assessment = self._assess_risks(sections, ai_analysis)
            
            # 6. Extracción de datos económicos (si aplica)
            economic_data = self._extract_economic_data(document_content)
            
            # 7. Análisis de cronograma
            timeline_analysis = self._analyze_timeline(document_content)
            
            result = {
                "status": "success",
                "document_info": {
                    "filename": filename,
                    "type": classified_type,
                    "original_type": document_type,
                    "analysis_timestamp": datetime.now().isoformat(),
                    "word_count": len(document_content.split())
                },
                "sections_analysis": [section.__dict__ for section in sections],
                "ai_insights": ai_analysis,
                "compliance": compliance_check,
                "risk_assessment": risk_assessment,
                "economic_analysis": economic_data,
                "timeline_analysis": timeline_analysis,
                "overall_score": self._calculate_overall_score(sections, compliance_check, risk_assessment),
                "recommendations": self._generate_recommendations(sections, risk_assessment, compliance_check)
            }
            
            # Guardar en base de datos interna
            self.processed_documents.append(result)
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error analizando documento: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def _classify_document(self, content: str) -> str:
        """Clasificar tipo de documento automáticamente"""
        content_lower = content.lower()
        
        # Pliegos de condiciones
        if any(word in content_lower for word in ['pliego', 'condiciones', 'bases', 'términos de referencia']):
            return "Pliego de Condiciones"
        
        # Propuestas técnicas
        elif any(word in content_lower for word in ['propuesta técnica', 'especificaciones técnicas', 'metodología']):
            return "Propuesta Técnica"
        
        # Propuestas económicas  
        elif any(word in content_lower for word in ['propuesta económica', 'presupuesto', 'cotización', 'precios unitarios']):
            return "Propuesta Económica"
        
        # Contratos
        elif any(word in content_lower for word in ['contrato', 'acuerdo', 'convenio', 'cláusulas']):
            return "Contrato"
        
        # Documentos legales
        elif any(word in content_lower for word in ['garantía', 'fianza', 'póliza', 'certificado']):
            return "Documento Legal"
        
        else:
            return "Documento General"
    
    def _extract_key_sections(self, content: str, doc_type: str) -> List[DocumentSection]:
        """Extraer y analizar secciones clave del documento"""
        sections = []
        
        if doc_type == "Pliego de Condiciones":
            sections.extend(self._extract_pliego_sections(content))
        elif doc_type == "Propuesta Técnica":
            sections.extend(self._extract_technical_sections(content))
        elif doc_type == "Propuesta Económica":
            sections.extend(self._extract_economic_sections(content))
        elif doc_type == "Contrato":
            sections.extend(self._extract_contract_sections(content))
        else:
            sections.extend(self._extract_general_sections(content))
        
        return sections
    
    def _extract_pliego_sections(self, content: str) -> List[DocumentSection]:
        """Extraer secciones de pliego de condiciones"""
        sections = []
        
        # Sección: Especificaciones técnicas
        tech_content = self._extract_section_content(content, ['especificaciones', 'técnicas', 'materiales'])
        if tech_content:
            compliance_score = self._evaluate_technical_completeness(tech_content)
            issues = self._identify_technical_issues(tech_content)
            
            sections.append(DocumentSection(
                section_type="Especificaciones Técnicas",
                content=tech_content[:500] + "..." if len(tech_content) > 500 else tech_content,
                compliance_score=compliance_score,
                risk_level=self._determine_risk_level(compliance_score),
                issues=issues,
                recommendations=self._generate_section_recommendations("technical", issues)
            ))
        
        # Sección: Condiciones económicas
        econ_content = self._extract_section_content(content, ['económicas', 'presupuesto', 'precio'])
        if econ_content:
            compliance_score = self._evaluate_economic_completeness(econ_content)
            issues = self._identify_economic_issues(econ_content)
            
            sections.append(DocumentSection(
                section_type="Condiciones Económicas",
                content=econ_content[:500] + "..." if len(econ_content) > 500 else econ_content,
                compliance_score=compliance_score,
                risk_level=self._determine_risk_level(compliance_score),
                issues=issues,
                recommendations=self._generate_section_recommendations("economic", issues)
            ))
        
        # Sección: Condiciones legales
        legal_content = self._extract_section_content(content, ['legales', 'jurídicas', 'garantías', 'multas'])
        if legal_content:
            compliance_score = self._evaluate_legal_completeness(legal_content)
            issues = self._identify_legal_issues(legal_content)
            
            sections.append(DocumentSection(
                section_type="Condiciones Legales",
                content=legal_content[:500] + "..." if len(legal_content) > 500 else legal_content,
                compliance_score=compliance_score,
                risk_level=self._determine_risk_level(compliance_score),
                issues=issues,
                recommendations=self._generate_section_recommendations("legal", issues)
            ))
        
        return sections
    
    def _extract_technical_sections(self, content: str) -> List[DocumentSection]:
        """Extraer secciones de propuesta técnica"""
        sections = []
        
        # Metodología
        methodology = self._extract_section_content(content, ['metodología', 'método', 'proceso', 'procedimiento'])
        if methodology:
            score = self._evaluate_methodology_quality(methodology)
            issues = self._identify_methodology_issues(methodology)
            
            sections.append(DocumentSection(
                section_type="Metodología",
                content=methodology[:500] + "..." if len(methodology) > 500 else methodology,
                compliance_score=score,
                risk_level=self._determine_risk_level(score),
                issues=issues,
                recommendations=self._generate_section_recommendations("methodology", issues)
            ))
        
        # Cronograma
        schedule = self._extract_section_content(content, ['cronograma', 'plazo', 'calendario', 'hitos'])
        if schedule:
            score = self._evaluate_schedule_feasibility(schedule)
            issues = self._identify_schedule_issues(schedule)
            
            sections.append(DocumentSection(
                section_type="Cronograma",
                content=schedule[:500] + "..." if len(schedule) > 500 else schedule,
                compliance_score=score,
                risk_level=self._determine_risk_level(score),
                issues=issues,
                recommendations=self._generate_section_recommendations("schedule", issues)
            ))
        
        return sections
    
    def _extract_economic_sections(self, content: str) -> List[DocumentSection]:
        """Extraer secciones de propuesta económica"""
        sections = []
        
        # Presupuesto detallado
        budget = self._extract_section_content(content, ['presupuesto', 'costo', 'precio', 'valor'])
        if budget:
            score = self._evaluate_budget_completeness(budget)
            issues = self._identify_budget_issues(budget)
            
            sections.append(DocumentSection(
                section_type="Presupuesto",
                content=budget[:500] + "..." if len(budget) > 500 else budget,
                compliance_score=score,
                risk_level=self._determine_risk_level(score),
                issues=issues,
                recommendations=self._generate_section_recommendations("budget", issues)
            ))
        
        return sections
    
    def _extract_contract_sections(self, content: str) -> List[DocumentSection]:
        """Extraer secciones de contrato"""
        sections = []
        
        # Cláusulas críticas
        critical_clauses = self._extract_section_content(content, ['garantía', 'multa', 'penalidad', 'rescisión'])
        if critical_clauses:
            score = self._evaluate_contract_risk(critical_clauses)
            issues = self._identify_contract_issues(critical_clauses)
            
            sections.append(DocumentSection(
                section_type="Cláusulas Críticas",
                content=critical_clauses[:500] + "..." if len(critical_clauses) > 500 else critical_clauses,
                compliance_score=score,
                risk_level=self._determine_risk_level(score),
                issues=issues,
                recommendations=self._generate_section_recommendations("contract", issues)
            ))
        
        return sections
    
    def _extract_general_sections(self, content: str) -> List[DocumentSection]:
        """Extraer secciones de documento general"""
        sections = []
        
        # Análisis general
        general_score = 75.0  # Score base para documentos generales
        general_issues = ["Tipo de documento no específico", "Requiere clasificación manual"]
        
        sections.append(DocumentSection(
            section_type="Análisis General",
            content=content[:500] + "..." if len(content) > 500 else content,
            compliance_score=general_score,
            risk_level="Medio",
            issues=general_issues,
            recommendations=["Clasificar documento específicamente", "Revisar contenido manualmente"]
        ))
        
        return sections
    
    async def _ai_document_analysis(self, content: str, doc_type: str) -> Dict[str, Any]:
        """Análisis del documento usando IA"""
        try:
            # Usar LangChain para análisis avanzado
            ai_result = await self.langchain_service.analyze_licitacion_document(
                document_content=content,
                document_type=doc_type
            )
            
            # Enriquecer con análisis específico de construcción
            construction_analysis = self._analyze_construction_aspects(content)
            
            return {
                "langchain_analysis": ai_result,
                "construction_specific": construction_analysis,
                "complexity_level": self._assess_document_complexity(content),
                "missing_elements": self._identify_missing_elements(content, doc_type)
            }
            
        except Exception as e:
            return {
                "error": f"Error en análisis de IA: {str(e)}",
                "fallback_analysis": self._basic_document_analysis(content)
            }
    
    def _analyze_construction_aspects(self, content: str) -> Dict[str, Any]:
        """Análisis específico para proyectos de construcción"""
        content_lower = content.lower()
        
        # Detectar materiales mencionados
        materials_found = []
        for material in self.construction_keywords['materials']:
            if material in content_lower:
                materials_found.append(material)
        
        # Detectar procesos constructivos
        processes_found = []
        for process in self.construction_keywords['processes']:
            if process in content_lower:
                processes_found.append(process)
        
        # Evaluar cumplimiento normativo
        regulations_compliance = self._check_construction_regulations(content)
        
        return {
            "materials_identified": materials_found,
            "construction_processes": processes_found,
            "regulations_compliance": regulations_compliance,
            "safety_mentions": self._count_safety_references(content),
            "quality_assurance": self._assess_quality_measures(content)
        }
    
    async def validate_contractor_ruc(self, ruc: str, company_name: str = None) -> ContractorValidation:
        """
        Validar RUC del contratista y verificar si puede realizar trabajos de construcción
        """
        try:
            # Simulación de consulta a servicios gubernamentales
            # En implementación real se conectaría con SRI, SCVS, etc.
            
            validation_result = self._simulate_ruc_validation(ruc, company_name)
            
            return ContractorValidation(
                ruc=ruc,
                company_name=validation_result["company_name"],
                is_valid=validation_result["is_valid"],
                legal_status=validation_result["legal_status"],
                can_perform_construction=validation_result["construction_authorized"],
                risk_factors=validation_result["risk_factors"]
            )
            
        except Exception as e:
            return ContractorValidation(
                ruc=ruc,
                company_name=company_name or "Desconocido",
                is_valid=False,
                legal_status="Error en validación",
                can_perform_construction=False,
                risk_factors=[f"Error al validar: {str(e)}"]
            )
    
    async def compare_proposals(self, proposal_ids: List[str]) -> Dict[str, Any]:
        """
        Comparar múltiples propuestas y generar ranking
        """
        try:
            # Obtener propuestas de la base de datos
            proposals = []
            for proposal_id in proposal_ids:
                proposal_data = self._get_proposal_by_id(proposal_id)
                if proposal_data:
                    comparison = self._analyze_proposal_for_comparison(proposal_data)
                    proposals.append(comparison)
            
            if not proposals:
                return {
                    "status": "error",
                    "message": "No se encontraron propuestas para comparar"
                }
            
            # Realizar comparación
            comparison_result = self._perform_proposal_comparison(proposals)
            
            # Generar ranking
            ranking = sorted(proposals, key=lambda x: x.overall_score, reverse=True)
            
            return {
                "status": "success",
                "comparison_timestamp": datetime.now().isoformat(),
                "proposals_analyzed": len(proposals),
                "ranking": [proposal.__dict__ for proposal in ranking],
                "comparative_analysis": comparison_result,
                "recommendations": self._generate_selection_recommendations(ranking)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error comparando propuestas: {str(e)}"
            }
    
    # Métodos auxiliares de evaluación
    def _extract_section_content(self, content: str, keywords: List[str]) -> str:
        """Extraer contenido de sección basado en palabras clave"""
        content_lower = content.lower()
        
        for keyword in keywords:
            if keyword in content_lower:
                # Buscar el contexto alrededor de la palabra clave
                start_idx = content_lower.find(keyword)
                if start_idx != -1:
                    # Extraer 500 caracteres antes y después
                    start = max(0, start_idx - 250)
                    end = min(len(content), start_idx + 750)
                    return content[start:end]
        
        return ""
    
    def _evaluate_technical_completeness(self, content: str) -> float:
        """Evaluar completitud de especificaciones técnicas"""
        score = 50.0  # Score base
        
        # Verificar presencia de elementos clave
        if 'materiales' in content.lower():
            score += 15
        if 'especificaciones' in content.lower():
            score += 15
        if 'normas' in content.lower():
            score += 10
        if 'calidad' in content.lower():
            score += 10
        
        return min(100.0, score)
    
    def _determine_risk_level(self, score: float) -> str:
        """Determinar nivel de riesgo basado en score"""
        if score >= 80:
            return "Bajo"
        elif score >= 60:
            return "Medio"
        else:
            return "Alto"
    
    def _simulate_ruc_validation(self, ruc: str, company_name: str = None) -> Dict[str, Any]:
        """Simular validación de RUC"""
        # Validación básica de formato de RUC ecuatoriano
        is_valid_format = len(ruc) == 13 and ruc.isdigit()
        
        # Simular respuesta basada en el RUC
        if is_valid_format:
            # Determinar tipo de empresa por el tercer dígito
            third_digit = int(ruc[2])
            if third_digit == 9:  # Jurídica
                legal_status = "Sociedad Anónima"
                construction_authorized = True
                risk_factors = []
            elif third_digit == 6:  # Pública
                legal_status = "Institución Pública"
                construction_authorized = True
                risk_factors = ["Requiere verificación de competencias"]
            else:
                legal_status = "Persona Natural"
                construction_authorized = False
                risk_factors = ["Persona natural no autorizada para grandes construcciones"]
        else:
            legal_status = "RUC inválido"
            construction_authorized = False
            risk_factors = ["Formato de RUC incorrecto"]
        
        return {
            "company_name": company_name or f"Empresa {ruc[-3:]}",
            "is_valid": is_valid_format,
            "legal_status": legal_status,
            "construction_authorized": construction_authorized,
            "risk_factors": risk_factors
        }
    
    # Métodos auxiliares adicionales (implementación básica)
    def _evaluate_economic_completeness(self, content: str) -> float:
        return 75.0
    
    def _evaluate_legal_completeness(self, content: str) -> float:
        return 80.0
    
    def _identify_technical_issues(self, content: str) -> List[str]:
        return ["Revisar especificaciones de materiales"]
    
    def _identify_economic_issues(self, content: str) -> List[str]:
        return ["Verificar precios unitarios"]
    
    def _identify_legal_issues(self, content: str) -> List[str]:
        return ["Revisar cláusulas de garantía"]
    
    def _generate_section_recommendations(self, section_type: str, issues: List[str]) -> List[str]:
        base_recommendations = {
            "technical": ["Completar especificaciones técnicas", "Incluir normas aplicables"],
            "economic": ["Detallar análisis de precios unitarios", "Incluir cronograma de pagos"],
            "legal": ["Revisar garantías requeridas", "Verificar cláusulas de penalidad"]
        }
        return base_recommendations.get(section_type, ["Revisar contenido de la sección"])
    
    def _check_compliance(self, sections: List[DocumentSection], doc_type: str) -> Dict[str, Any]:
        """Verificar cumplimiento general"""
        total_score = sum(section.compliance_score for section in sections) / len(sections) if sections else 0
        
        return {
            "overall_compliance": total_score,
            "sections_analyzed": len(sections),
            "compliance_level": "Alto" if total_score >= 80 else "Medio" if total_score >= 60 else "Bajo",
            "critical_issues": sum(1 for section in sections if section.risk_level == "Alto")
        }
    
    def _assess_risks(self, sections: List[DocumentSection], ai_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluar riesgos del documento"""
        high_risk_sections = [s for s in sections if s.risk_level == "Alto"]
        medium_risk_sections = [s for s in sections if s.risk_level == "Medio"]
        
        return {
            "overall_risk_level": "Alto" if high_risk_sections else "Medio" if medium_risk_sections else "Bajo",
            "risk_factors": [issue for section in sections for issue in section.issues],
            "high_risk_sections": len(high_risk_sections),
            "recommendations": ["Revisar secciones de alto riesgo", "Validar con experto legal"]
        }
    
    def _extract_economic_data(self, content: str) -> Dict[str, Any]:
        """Extraer datos económicos del documento"""
        # Buscar números que podrían ser montos
        import re
        amounts = re.findall(r'\$?[\d,]+\.?\d*', content)
        
        return {
            "amounts_found": len(amounts),
            "sample_amounts": amounts[:5] if amounts else [],
            "currency_detected": "USD" if "$" in content else "Pendiente identificar"
        }
    
    def _analyze_timeline(self, content: str) -> Dict[str, Any]:
        """Analizar cronograma en el documento"""
        timeline_keywords = ['días', 'semanas', 'meses', 'plazo', 'entrega']
        timeline_mentions = sum(1 for keyword in timeline_keywords if keyword in content.lower())
        
        return {
            "timeline_mentions": timeline_mentions,
            "has_schedule": timeline_mentions > 0,
            "schedule_detail_level": "Alto" if timeline_mentions >= 3 else "Medio" if timeline_mentions >= 1 else "Bajo"
        }
    
    def _calculate_overall_score(self, sections: List[DocumentSection], compliance: Dict[str, Any], risk: Dict[str, Any]) -> float:
        """Calcular score general del documento"""
        if not sections:
            return 50.0
        
        section_avg = sum(section.compliance_score for section in sections) / len(sections)
        compliance_score = compliance.get("overall_compliance", 50.0)
        
        # Penalizar por riesgos altos
        risk_penalty = compliance.get("critical_issues", 0) * 10
        
        final_score = (section_avg + compliance_score) / 2 - risk_penalty
        return max(0.0, min(100.0, final_score))
    
    def _generate_recommendations(self, sections: List[DocumentSection], risk: Dict[str, Any], compliance: Dict[str, Any]) -> List[str]:
        """Generar recomendaciones generales"""
        recommendations = []
        
        # Recomendaciones por sección
        for section in sections:
            if section.risk_level == "Alto":
                recommendations.append(f"Revisar urgentemente: {section.section_type}")
        
        # Recomendaciones por compliance
        if compliance.get("overall_compliance", 0) < 70:
            recommendations.append("Mejorar cumplimiento general del documento")
        
        # Recomendaciones por riesgo
        if risk.get("overall_risk_level") == "Alto":
            recommendations.append("Realizar revisión legal especializada")
        
        return recommendations[:5]  # Limitar a 5 recomendaciones principales
    
    def _check_construction_regulations(self, content: str) -> Dict[str, Any]:
        """Verificar cumplimiento de regulaciones de construcción"""
        regulations = ['código de construcción', 'normas sísmicas', 'seguridad industrial', 'permisos']
        found_regulations = [reg for reg in regulations if reg in content.lower()]
        
        return {
            "regulations_mentioned": found_regulations,
            "compliance_score": (len(found_regulations) / len(regulations)) * 100,
            "missing_regulations": [reg for reg in regulations if reg not in found_regulations]
        }
    
    def _count_safety_references(self, content: str) -> int:
        """Contar referencias a seguridad"""
        safety_keywords = ['seguridad', 'epp', 'protección', 'riesgo laboral', 'accidente']
        return sum(1 for keyword in safety_keywords if keyword in content.lower())
    
    def _assess_quality_measures(self, content: str) -> Dict[str, Any]:
        """Evaluar medidas de calidad mencionadas"""
        quality_keywords = ['control de calidad', 'ensayos', 'certificación', 'inspección']
        quality_mentions = [kw for kw in quality_keywords if kw in content.lower()]
        
        return {
            "quality_measures": quality_mentions,
            "quality_score": len(quality_mentions) * 25,  # 25 puntos por cada medida
            "has_quality_plan": len(quality_mentions) >= 2
        }
    
    def _assess_document_complexity(self, content: str) -> str:
        """Evaluar complejidad del documento"""
        word_count = len(content.split())
        
        if word_count > 5000:
            return "Alta"
        elif word_count > 2000:
            return "Media"
        else:
            return "Baja"
    
    def _identify_missing_elements(self, content: str, doc_type: str) -> List[str]:
        """Identificar elementos faltantes según tipo de documento"""
        missing = []
        
        if doc_type == "Pliego de Condiciones":
            if 'cronograma' not in content.lower():
                missing.append("Cronograma detallado")
            if 'garantía' not in content.lower():
                missing.append("Requisitos de garantía")
        
        return missing
    
    def _basic_document_analysis(self, content: str) -> Dict[str, Any]:
        """Análisis básico como fallback"""
        return {
            "word_count": len(content.split()),
            "has_technical_content": any(kw in content.lower() for kw in self.construction_keywords['materials']),
            "complexity": self._assess_document_complexity(content)
        }
    
    # Métodos para comparación de propuestas
    def _get_proposal_by_id(self, proposal_id: str) -> Dict[str, Any]:
        """Obtener propuesta por ID (simulado)"""
        # En implementación real, consultaría base de datos
        return {
            "id": proposal_id,
            "company_name": f"Empresa {proposal_id}",
            "technical_score": 75.0 + (hash(proposal_id) % 20),
            "economic_data": {"budget": 100000 + (hash(proposal_id) % 50000)},
            "timeline": {"days": 90 + (hash(proposal_id) % 60)}
        }
    
    def _analyze_proposal_for_comparison(self, proposal_data: Dict[str, Any]) -> ProposalComparison:
        """Analizar propuesta para comparación"""
        return ProposalComparison(
            proposal_id=proposal_data["id"],
            company_name=proposal_data["company_name"],
            overall_score=proposal_data["technical_score"],
            technical_score=proposal_data["technical_score"],
            economic_score=75.0,  # Calculado
            legal_score=80.0,     # Calculado
            total_budget=proposal_data["economic_data"]["budget"],
            timeline_days=proposal_data["timeline"]["days"],
            compliance_percentage=85.0,
            risk_level="Medio"
        )
    
    def _perform_proposal_comparison(self, proposals: List[ProposalComparison]) -> Dict[str, Any]:
        """Realizar comparación entre propuestas"""
        if not proposals:
            return {}
        
        # Estadísticas comparativas
        budgets = [p.total_budget for p in proposals]
        timelines = [p.timeline_days for p in proposals]
        scores = [p.overall_score for p in proposals]
        
        return {
            "budget_analysis": {
                "min": min(budgets),
                "max": max(budgets),
                "avg": sum(budgets) / len(budgets),
                "range_percentage": ((max(budgets) - min(budgets)) / min(budgets)) * 100
            },
            "timeline_analysis": {
                "shortest": min(timelines),
                "longest": max(timelines),
                "avg": sum(timelines) / len(timelines)
            },
            "quality_analysis": {
                "highest_score": max(scores),
                "lowest_score": min(scores),
                "avg_score": sum(scores) / len(scores)
            }
        }
    
    def _generate_selection_recommendations(self, ranking: List[ProposalComparison]) -> List[str]:
        """Generar recomendaciones para selección"""
        if not ranking:
            return []
        
        best_proposal = ranking[0]
        recommendations = []
        
        recommendations.append(f"Propuesta recomendada: {best_proposal.company_name} (Score: {best_proposal.overall_score:.1f})")
        
        if best_proposal.risk_level == "Alto":
            recommendations.append("Realizar due diligence adicional de la empresa seleccionada")
        
        # Comparar presupuestos
        budgets = [p.total_budget for p in ranking]
        if max(budgets) / min(budgets) > 1.5:  # Diferencia > 50%
            recommendations.append("Revisar diferencias significativas en presupuestos")
        
        return recommendations
    
    # Métodos auxiliares para evaluación específica
    def _evaluate_methodology_quality(self, content: str) -> float:
        return 75.0
    
    def _identify_methodology_issues(self, content: str) -> List[str]:
        return ["Detallar metodología constructiva"]
    
    def _evaluate_schedule_feasibility(self, content: str) -> float:
        return 80.0
    
    def _identify_schedule_issues(self, content: str) -> List[str]:
        return ["Verificar factibilidad de plazos"]
    
    def _evaluate_budget_completeness(self, content: str) -> float:
        return 85.0
    
    def _identify_budget_issues(self, content: str) -> List[str]:
        return ["Incluir análisis de precios unitarios"]
    
    def _evaluate_contract_risk(self, content: str) -> float:
        return 70.0
    
    def _identify_contract_issues(self, content: str) -> List[str]:
        return ["Revisar cláusulas de penalidad", "Clarificar garantías"]
