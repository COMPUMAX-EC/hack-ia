import Link from "next/link";
import { 
  FileText, 
  Building2, 
  Brain, 
  TrendingUp, 
  Search, 
  Zap, 
  BarChart3
} from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              <span className="text-blue-600">Dev</span>Team
            </h1>
            <nav className="flex gap-6">
              <span className="text-blue-600 font-medium">Inicio</span>
              <Link href="/reto1" className="text-gray-600 hover:text-gray-900">Licitaciones IA</Link>
              <Link href="/reto2" className="text-gray-600 hover:text-gray-900">Crédito PYME IA</Link>
              <Link href="/equipo" className="text-gray-600 hover:text-gray-900">Equipo</Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Transformando Industrias con Inteligencia Artificial
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Desarrollamos soluciones de IA para resolver problemas críticos en licitaciones públicas 
            y evaluación crediticia, democratizando el acceso a procesos más eficientes y justos.
          </p>
        </div>
      </section>

      {/* Problem Statement */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Los Problemas Que Identificamos
          </h3>
          
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Problema 1 */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileText className="w-8 h-8 text-red-600" />
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Licitaciones Ineficientes
              </h4>
              <div className="space-y-4 text-gray-600">
                <p><strong>Problema:</strong> Los procesos de licitación son largos, propensos a errores humanos y carecen de transparencia.</p>
                <p><strong>Impacto:</strong></p>
                <ul className="space-y-2 ml-4">
                  <li>• 8-12 horas para evaluar una propuesta</li>
                  <li>• 40% de errores en evaluación manual</li>
                  <li>• Falta de criterios objetivos unificados</li>
                  <li>• Retrasos en adjudicaciones importantes</li>
                </ul>
              </div>
            </div>

            {/* Problema 2 */}
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Building2 className="w-8 h-8 text-red-600" />
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                Exclusión Financiera de PYMEs
              </h4>
              <div className="space-y-4 text-gray-600">
                <p><strong>Problema:</strong> Las PYMEs no pueden acceder a créditos por falta de historial crediticio formal.</p>
                <p><strong>Impacto:</strong></p>
                <ul className="space-y-2 ml-4">
                  <li>• 60% de PYMEs sin acceso a crédito</li>
                  <li>• Evaluación basada solo en garantías</li>
                  <li>• Empresas rentables excluidas del sistema</li>
                  <li>• Limitación del crecimiento económico</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Our Solution */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Nuestra Solución con IA
          </h3>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Solución 1 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-blue-600" />
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                IA para Licitaciones Inteligentes
              </h4>
              
              <div className="mb-6">
                <h5 className="font-semibold text-gray-900 mb-3">Cómo lo resolvimos:</h5>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>NLP avanzado</strong> para análisis automático de documentos
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>Machine Learning</strong> para detección de riesgos y anomalías
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>Algoritmos de scoring</strong> para evaluación objetiva
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>Dashboard intuitivo</strong> para toma de decisiones
                  </li>
                </ul>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg mb-6">
                <p className="text-blue-800 font-medium text-center">
                  <strong>Resultado:</strong> 75% menos tiempo, 90% menos errores
                </p>
              </div>

              <Link href="/reto1" className="inline-block w-full">
                <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200">
                  Ver Demo Completa
                </button>
              </Link>
            </div>

            {/* Solución 2 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <TrendingUp className="w-8 h-8 text-purple-600" />
              </div>
              <h4 className="text-2xl font-bold text-gray-900 mb-4 text-center">
                IA para Crédito Inclusivo
              </h4>
              
              <div className="mb-6">
                <h5 className="font-semibold text-gray-900 mb-3">Cómo lo resolvimos:</h5>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>Datos alternativos</strong> de redes sociales y reputación digital
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>Análisis de comportamiento</strong> comercial y transaccional
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>Modelos predictivos</strong> para evaluación de riesgo
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <strong>Scoring dinámico</strong> que se actualiza en tiempo real
                  </li>
                </ul>
              </div>

              <div className="bg-purple-50 p-4 rounded-lg mb-6">
                <p className="text-purple-800 font-medium text-center">
                  <strong>Resultado:</strong> 40% más PYMEs con acceso a crédito
                </p>
              </div>

              <Link href="/reto2" className="inline-block w-full">
                <button className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200">
                  Ver Demo Completa
                </button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Methodology */}
      <section className="py-16 px-4 bg-gray-50">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl font-bold text-gray-900 mb-8">
            Nuestra Metodología
          </h3>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">
                <Search className="w-8 h-8 text-blue-600 mx-auto" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">1. Investigación</h4>
              <p className="text-gray-600 text-sm">Análisis profundo del problema y sus stakeholders</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">
                <Brain className="w-8 h-8 text-green-600 mx-auto" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">2. Diseño IA</h4>
              <p className="text-gray-600 text-sm">Arquitectura de modelos de machine learning especializados</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">
                <Zap className="w-8 h-8 text-yellow-600 mx-auto" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">3. Desarrollo</h4>
              <p className="text-gray-600 text-sm">Implementación ágil con tecnologías de vanguardia</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow">
              <div className="text-3xl mb-4">
                <BarChart3 className="w-8 h-8 text-purple-600 mx-auto" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">4. Validación</h4>
              <p className="text-gray-600 text-sm">Pruebas exhaustivas y métricas de impacto real</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4 bg-gray-900">
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl font-bold text-white mb-6">
            ¿Listo para Ver la IA en Acción?
          </h3>
          <p className="text-xl text-gray-300 mb-8">
            Explora nuestras demos interactivas y descubre cómo la inteligencia artificial puede transformar industrias completas.
          </p>
          <div className="flex flex-col gap-4 justify-center">
            <Link href="/reto1">
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200">
                Demo: Licitaciones Inteligentes
              </button>
            </Link>
            <Link href="/reto2">
              <button className="bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200">
                Demo: Crédito Inclusivo
              </button>
            </Link>
            <Link href="/equipo">
              <button className="bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200">
                Conoce al Equipo
              </button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-50 py-8 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-600">
            Desarrollado con ❤️ por DevTeam - Innovación en IA para el bien social
          </p>
        </div>
      </footer>
    </div>
  );
}
