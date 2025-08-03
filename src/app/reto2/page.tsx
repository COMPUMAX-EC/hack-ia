'use client';

import { useState } from 'react';
import Header from '../../components/Header';

export default function Reto2() {
  const [companyData, setCompanyData] = useState({
    companyName: '',
    sector: '',
    yearsInBusiness: '',
    monthlyRevenue: '',
    digitalPresence: '',
    commercialReferences: ''
  });
  const [riskAssessment, setRiskAssessment] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setCompanyData({
      ...companyData,
      [e.target.name]: e.target.value
    });
  };

  const analyzeCredit = async () => {
    setIsAnalyzing(true);
    
    // Simulamos el análisis de IA
    setTimeout(() => {
      const score = Math.floor(Math.random() * 300) + 600; // Score entre 600-900
      const riskLevel = score >= 750 ? 'Bajo' : score >= 650 ? 'Medio' : 'Alto';
      const creditAmount = Math.floor(parseInt(companyData.monthlyRevenue) * 0.3);
      
      setRiskAssessment({
        creditScore: score,
        riskLevel: riskLevel,
        approvalProbability: score >= 750 ? 85 : score >= 650 ? 65 : 35,
        recommendedAmount: creditAmount,
        interestRate: score >= 750 ? 12 : score >= 650 ? 18 : 25,
        factors: {
          digitalPresence: Math.floor(Math.random() * 30) + 70,
          commercialReputation: Math.floor(Math.random() * 30) + 75,
          businessStability: Math.floor(Math.random() * 25) + 70,
          financialBehavior: Math.floor(Math.random() * 20) + 80
        },
        recommendations: [
          'Mejorar presencia digital con testimonios de clientes',
          'Documentar historial de pagos a proveedores',
          'Registrar transacciones comerciales formalmente'
        ]
      });
      setIsAnalyzing(false);
    }, 3000);
  };

  const isFormValid = companyData.companyName && companyData.sector && 
                     companyData.yearsInBusiness && companyData.monthlyRevenue;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-purple-100">
      <Header currentPage="reto2" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Evaluación Inteligente de Riesgo Financiero para PYMEs
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Utilizamos IA para evaluar el riesgo crediticio usando información alternativa, 
            democratizando el acceso al crédito para pequeñas y medianas empresas.
          </p>
        </div>

        {/* Demo Section */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* Input Form */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Datos de la Empresa
            </h2>
            
            <form className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre de la Empresa
                </label>
                <input
                  type="text"
                  name="companyName"
                  value={companyData.companyName}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                  placeholder="Ej. Distribuidora Los Andes EIRL"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sector de Actividad
                </label>
                <select
                  name="sector"
                  value={companyData.sector}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="">Seleccionar sector</option>
                  <option value="comercio">Comercio</option>
                  <option value="servicios">Servicios</option>
                  <option value="manufactura">Manufactura</option>
                  <option value="agricultura">Agricultura</option>
                  <option value="construccion">Construcción</option>
                  <option value="tecnologia">Tecnología</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Años en el Negocio
                </label>
                <input
                  type="number"
                  name="yearsInBusiness"
                  value={companyData.yearsInBusiness}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                  placeholder="Ej. 5"
                  min="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ingresos Mensuales Promedio (USD)
                </label>
                <input
                  type="number"
                  name="monthlyRevenue"
                  value={companyData.monthlyRevenue}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                  placeholder="Ej. 15000"
                  min="0"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Presencia Digital
                </label>
                <select
                  name="digitalPresence"
                  value={companyData.digitalPresence}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="">Seleccionar nivel</option>
                  <option value="alta">Alta (Redes sociales, web, reseñas)</option>
                  <option value="media">Media (Algunas redes sociales)</option>
                  <option value="baja">Baja (Presencia mínima)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Referencias Comerciales
                </label>
                <select
                  name="commercialReferences"
                  value={companyData.commercialReferences}
                  onChange={handleInputChange}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
                >
                  <option value="">Seleccionar cantidad</option>
                  <option value="muchas">Muchas (5+ proveedores/clientes)</option>
                  <option value="algunas">Algunas (2-4 referencias)</option>
                  <option value="pocas">Pocas (1-2 referencias)</option>
                </select>
              </div>

              <button
                type="button"
                onClick={analyzeCredit}
                disabled={!isFormValid || isAnalyzing}
                className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
              >
                {isAnalyzing ? 'Evaluando Riesgo...' : 'Evaluar con IA'}
              </button>
            </form>
          </div>

          {/* Results Area */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Evaluación de Riesgo
            </h2>

            {isAnalyzing && (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Analizando perfil crediticio con IA...</p>
              </div>
            )}

            {riskAssessment && !isAnalyzing && (
              <div className="space-y-6">
                {/* Credit Score */}
                <div className="text-center bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-sm font-medium text-gray-600 mb-2">SCORE CREDITICIO IA</h3>
                  <p className="text-4xl font-bold text-purple-600 mb-2">{riskAssessment.creditScore}</p>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                    riskAssessment.riskLevel === 'Bajo' ? 'bg-green-100 text-green-800' :
                    riskAssessment.riskLevel === 'Medio' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    Riesgo {riskAssessment.riskLevel}
                  </span>
                </div>

                {/* Approval Details */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-green-800 mb-1">Probabilidad de Aprobación</h4>
                    <p className="text-2xl font-bold text-green-600">{riskAssessment.approvalProbability}%</p>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-blue-800 mb-1">Tasa Sugerida</h4>
                    <p className="text-2xl font-bold text-blue-600">{riskAssessment.interestRate}%</p>
                  </div>
                </div>

                {/* Recommended Amount */}
                <div className="bg-purple-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-purple-800 mb-2">Monto Recomendado</h4>
                  <p className="text-2xl font-bold text-purple-600">
                    ${riskAssessment.recommendedAmount.toLocaleString()}
                  </p>
                  <p className="text-sm text-purple-600 mt-1">
                    Basado en capacidad de pago estimada
                  </p>
                </div>

                {/* Risk Factors */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">Factores de Evaluación</h4>
                  <div className="space-y-3">
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>Presencia Digital</span>
                        <span>{riskAssessment.factors.digitalPresence}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-purple-600 h-2 rounded-full" style={{width: `${riskAssessment.factors.digitalPresence}%`}}></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>Reputación Comercial</span>
                        <span>{riskAssessment.factors.commercialReputation}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-purple-600 h-2 rounded-full" style={{width: `${riskAssessment.factors.commercialReputation}%`}}></div>
                      </div>
                    </div>
                    <div>
                      <div className="flex justify-between text-sm mb-1">
                        <span>Estabilidad del Negocio</span>
                        <span>{riskAssessment.factors.businessStability}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-purple-600 h-2 rounded-full" style={{width: `${riskAssessment.factors.businessStability}%`}}></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Recommendations */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">Recomendaciones para Mejorar</h4>
                  <ul className="space-y-2">
                    {riskAssessment.recommendations.map((rec: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <span className="text-purple-500 mr-2">•</span>
                        <span className="text-gray-700 text-sm">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {!riskAssessment && !isAnalyzing && (
              <div className="text-center py-8 text-gray-400">
                <p>Completa el formulario para ver la evaluación de riesgo con IA</p>
              </div>
            )}
          </div>
        </div>

        {/* Alternative Data Sources */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Fuentes de Datos Alternativos
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🌐</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Presencia Digital</h3>
              <p className="text-gray-600 text-sm">Análisis de redes sociales, sitio web y reseñas online</p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤝</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Referencias Comerciales</h3>
              <p className="text-gray-600 text-sm">Historial con proveedores y clientes</p>
            </div>
            
            <div className="text-center">
              <div className="bg-yellow-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📊</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Actividad Financiera</h3>
              <p className="text-gray-600 text-sm">Patrones de transacciones y flujo de caja</p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📱</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Datos de Comportamiento</h3>
              <p className="text-gray-600 text-sm">Patrones de uso de servicios digitales</p>
            </div>
          </div>
        </div>

        {/* Impact Section */}
        <div className="bg-purple-600 text-white rounded-2xl shadow-lg p-8 text-center">
          <h2 className="text-3xl font-bold mb-6">Impacto Social</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <p className="text-4xl font-bold mb-2">40%</p>
              <p className="text-purple-100">Más PYMEs con acceso a crédito</p>
            </div>
            <div>
              <p className="text-4xl font-bold mb-2">80%</p>
              <p className="text-purple-100">Reducción en tiempo de evaluación</p>
            </div>
            <div>
              <p className="text-4xl font-bold mb-2">65%</p>
              <p className="text-purple-100">Mejor precisión en evaluación</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
