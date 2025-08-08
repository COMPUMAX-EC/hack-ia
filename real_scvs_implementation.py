"""
IMPLEMENTACIÓN REAL DE CONEXIÓN CON SCVS
Este archivo muestra cómo conectar realmente con la Superintendencia de Compañías, Valores y Seguros
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from typing import Dict, Any
import ssl
import urllib3

class RealSCVSService:
    """
    Servicio REAL para conectar con la SCVS del Ecuador
    """
    
    def __init__(self):
        # URLs oficiales de la SCVS
        self.base_url = "https://www.supercias.gob.ec"
        self.portal_url = "https://www.supercias.gob.ec/portalscvs/"
        self.consulta_url = "https://appscvs.supercias.gob.ec/consultaCompanias/"
        
        # Configurar sesión
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Manejar certificados SSL
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def get_company_basic_info(self, company_ruc: str) -> Dict[str, Any]:
        """
        Obtener información básica de una empresa por RUC desde SCVS
        """
        try:
            # URL de consulta pública SCVS
            search_url = f"{self.consulta_url}consultaCompanias.jsf"
            
            # Parámetros de búsqueda
            search_params = {
                'ruc': company_ruc,
                'denominacion': '',
                'tipo': 'TODAS'
            }
            
            # Hacer petición
            response = self.session.get(search_url, params=search_params, verify=False, timeout=30)
            
            if response.status_code == 200:
                return self._parse_company_info(response.text, company_ruc)
            else:
                return {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Error consultando SCVS: {str(e)}"}
    
    def get_financial_statements(self, company_ruc: str, year: int = 2023) -> Dict[str, Any]:
        """
        Obtener estados financieros oficiales desde SCVS
        """
        try:
            # URL específica para estados financieros
            financial_url = f"{self.portal_url}consulta/EstadosFinancieros.jsf"
            
            # Parámetros para estados financieros
            params = {
                'ruc': company_ruc,
                'anio': year,
                'tipoEstado': 'BALANCE_GENERAL'
            }
            
            response = self.session.get(financial_url, params=params, verify=False, timeout=45)
            
            if response.status_code == 200:
                return self._parse_financial_statements(response.text, company_ruc, year)
            else:
                return {"error": f"Estados financieros no disponibles"}
                
        except Exception as e:
            return {"error": f"Error obteniendo estados financieros: {str(e)}"}
    
    def verify_company_exists(self, company_ruc: str) -> bool:
        """
        Verificar si una empresa existe en los registros de SCVS
        """
        try:
            # Usar servicio de consulta rápida
            verify_url = f"{self.base_url}/wps/portal/Inicio/Tramites/ConsultaRapida"
            
            data = {'numeroRuc': company_ruc}
            response = self.session.post(verify_url, data=data, verify=False, timeout=20)
            
            # Buscar indicadores de empresa válida
            if "RUC encontrado" in response.text or "ACTIVA" in response.text:
                return True
            return False
            
        except:
            return False
    
    def get_company_status(self, company_ruc: str) -> Dict[str, Any]:
        """
        Obtener estado actual de la empresa (activa, inactiva, etc.)
        """
        try:
            status_url = f"{self.consulta_url}consultaCompanias.jsf"
            
            response = self.session.get(
                status_url,
                params={'ruc': company_ruc},
                verify=False,
                timeout=25
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar tabla de resultados
                status_info = self._extract_company_status(soup)
                return status_info
            
            return {"status": "unknown", "error": "No se pudo consultar"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def download_financial_file(self, company_ruc: str, year: int, file_type: str = "PDF") -> bytes:
        """
        Descargar archivo de estados financieros oficial
        """
        try:
            download_url = f"{self.portal_url}descarga/EstadosFinancieros.jsf"
            
            params = {
                'ruc': company_ruc,
                'anio': year,
                'formato': file_type,
                'tipoDocumento': 'ESTADOS_FINANCIEROS'
            }
            
            response = self.session.get(download_url, params=params, verify=False, timeout=60)
            
            if response.status_code == 200:
                return response.content
            else:
                raise Exception(f"Error descargando archivo: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Error en descarga: {str(e)}")
    
    def _parse_company_info(self, html_content: str, company_ruc: str) -> Dict[str, Any]:
        """
        Parsear información básica de la empresa desde HTML de SCVS
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar tabla de resultados de empresas
            company_table = soup.find('table', {'class': 'tableCompanies'})
            
            if company_table:
                rows = company_table.find_all('tr')[1:]  # Saltar header
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 4:
                        ruc = cols[0].text.strip()
                        if ruc == company_ruc:
                            return {
                                "ruc": ruc,
                                "name": cols[1].text.strip(),
                                "status": cols[2].text.strip(),
                                "type": cols[3].text.strip(),
                                "found": True
                            }
            
            return {"found": False, "error": "Empresa no encontrada"}
            
        except Exception as e:
            return {"found": False, "error": f"Error parsing: {str(e)}"}
    
    def _parse_financial_statements(self, html_content: str, ruc: str, year: int) -> Dict[str, Any]:
        """
        Parsear estados financieros desde HTML de SCVS
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Buscar tablas de estados financieros
            financial_tables = soup.find_all('table', {'class': 'financialData'})
            
            financial_data = {
                "balance_sheet": {},
                "income_statement": {},
                "cash_flow": {},
                "year": year,
                "ruc": ruc
            }
            
            for table in financial_tables:
                table_type = self._identify_table_type(table)
                if table_type:
                    financial_data[table_type] = self._parse_financial_table(table)
            
            return financial_data
            
        except Exception as e:
            return {"error": f"Error parsing financial data: {str(e)}"}
    
    def _extract_company_status(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """
        Extraer estado de la empresa desde HTML parseado
        """
        try:
            # Buscar elementos específicos del estado
            status_element = soup.find('span', {'class': 'companyStatus'})
            date_element = soup.find('span', {'class': 'lastUpdate'})
            
            return {
                "status": status_element.text.strip() if status_element else "unknown",
                "last_update": date_element.text.strip() if date_element else None,
                "is_active": "ACTIVA" in soup.text.upper()
            }
            
        except:
            return {"status": "unknown"}
    
    def _identify_table_type(self, table) -> str:
        """
        Identificar tipo de tabla financiera
        """
        table_text = table.text.upper()
        
        if "BALANCE" in table_text or "ACTIVO" in table_text:
            return "balance_sheet"
        elif "RESULTADO" in table_text or "INGRESO" in table_text:
            return "income_statement"
        elif "FLUJO" in table_text or "EFECTIVO" in table_text:
            return "cash_flow"
        
        return None
    
    def _parse_financial_table(self, table) -> Dict[str, float]:
        """
        Parsear tabla financiera específica
        """
        financial_items = {}
        
        try:
            rows = table.find_all('tr')[1:]  # Saltar header
            
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 2:
                    account_name = cols[0].text.strip()
                    account_value = cols[-1].text.strip()
                    
                    # Limpiar y convertir valor
                    try:
                        cleaned_value = account_value.replace(',', '').replace('$', '')
                        financial_items[account_name] = float(cleaned_value)
                    except ValueError:
                        continue
            
            return financial_items
            
        except Exception as e:
            return {"parse_error": str(e)}


# EJEMPLO DE USO REAL:
async def ejemplo_uso_real():
    """
    Ejemplo de cómo usar el servicio real de SCVS
    """
    scvs_real = RealSCVSService()
    
    company_ruc = "1791234567001"
    
    # 1. Verificar que la empresa existe
    exists = scvs_real.verify_company_exists(company_ruc)
    print(f"¿Empresa existe? {exists}")
    
    # 2. Obtener información básica
    basic_info = scvs_real.get_company_basic_info(company_ruc)
    print(f"Info básica: {basic_info}")
    
    # 3. Obtener estado actual
    status = scvs_real.get_company_status(company_ruc)
    print(f"Estado: {status}")
    
    # 4. Obtener estados financieros
    if exists:
        financial_data = scvs_real.get_financial_statements(company_ruc, 2023)
        print(f"Estados financieros: {financial_data}")


# IMPLEMENTACIÓN DE AUTENTICACIÓN OFICIAL
class SCVSAuthenticatedService:
    """
    Para acceso autenticado a datos más detallados
    """
    
    def __init__(self, api_key: str, username: str, password: str):
        self.api_key = api_key  # Requiere convenio con SCVS
        self.username = username
        self.password = password
        self.access_token = None
    
    def authenticate(self) -> bool:
        """
        Autenticarse con credenciales oficiales
        """
        try:
            auth_url = "https://api.supercias.gob.ec/auth/login"
            
            auth_data = {
                "username": self.username,
                "password": self.password,
                "api_key": self.api_key
            }
            
            response = requests.post(auth_url, json=auth_data)
            
            if response.status_code == 200:
                self.access_token = response.json().get('access_token')
                return True
            
            return False
            
        except Exception as e:
            print(f"Error autenticación: {e}")
            return False
    
    def get_official_financial_data(self, company_ruc: str) -> Dict[str, Any]:
        """
        Obtener datos oficiales con autenticación
        """
        if not self.access_token:
            raise Exception("No autenticado")
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        api_url = f"https://api.supercias.gob.ec/v1/companies/{company_ruc}/financial"
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error API: {response.status_code}")
