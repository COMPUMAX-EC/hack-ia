import Image from "next/image";
import Link from "next/link";
import Header from "../components/Header";
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
    <div className="min-h-screen" style={{background: 'white'}}>
      <Header currentPage="inicio" />

      {/* Hero Section */}
      <section className="py-20 px-4 relative overflow-hidden" style={{background: 'white'}}>
        <div className="max-w-4xl mx-auto text-center relative z-20">
          <div className="inline-block px-6 py-3 rounded-full font-medium mb-8 shadow-lg" style={{background: 'rgba(31, 170, 89, 0.1)', color: '#0D3B66', border: '2px solid #1FAA59'}}>
            <span className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{backgroundColor: '#1FAA59'}}></div>
              Innovando hoy, transformando finanzas
            </span>
          </div>
          
          <h2 className="text-5xl font-bold mb-6" style={{color: '#0D3B66'}}>
            Código que impulsa tu futuro <span style={{color: '#1FAA59'}}>financiero</span>
          </h2>
          
          <p className="text-xl text-gray-600 leading-relaxed mb-10 max-w-3xl mx-auto">
            Desarrollamos soluciones de IA para resolver problemas críticos en licitaciones públicas 
            y evaluación crediticia, democratizando el acceso a procesos más eficientes y justos.
          </p>
          
          <div className="flex justify-center gap-4">
            <button className="px-8 py-3 text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 flex items-center gap-2" style={{background: 'linear-gradient(to right, #0D3B66, #1FAA59)'}}>
              <div className="w-4 h-4 bg-white rounded opacity-80"></div>
              Ver Soluciones
            </button>
            <button className="px-8 py-3 border-2 font-semibold rounded-lg transition-all duration-300 finova-btn-secondary" style={{borderColor: '#0D3B66', color: '#0D3B66'}}>
              Conocer Equipo
            </button>
          </div>
        </div>
      </section>

      {/* Problem Statement */}
      <section className="py-20 px-4 relative overflow-hidden" style={{background: 'rgba(31, 170, 89, 0.05)'}}>
        <div className="max-w-6xl mx-auto relative z-20">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold mb-4" style={{color: '#0D3B66'}}>
              Los Problemas Que Identificamos
            </h3>
            <p className="text-xl" style={{color: 'rgba(13, 59, 102, 0.8)'}}>Desafíos críticos que requieren soluciones innovadoras</p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8 mb-12">
            {/* Problema 1 */}
            <div className="rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 finova-shadow relative finova-dot-pattern" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #1FAA59'}}>
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6" style={{backgroundColor: '#1FAA59', color: 'white'}}>
                <FileText className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-2xl font-bold mb-4 text-center finova-accent-border" style={{color: '#0D3B66'}}>
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
            <div className="rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 finova-shadow relative finova-dot-pattern" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #0D3B66'}}>
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6" style={{backgroundColor: '#0D3B66', color: 'white'}}>
                <Building2 className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-2xl font-bold mb-4 text-center finova-accent-border" style={{color: '#0D3B66'}}>
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
      <section className="py-20 px-4 relative overflow-hidden" style={{background: 'white'}}>
        <div className="max-w-6xl mx-auto relative z-20">
          <div className="text-center mb-16">
            <h3 className="text-4xl font-bold mb-4" style={{color: '#0D3B66'}}>
              Nuestra Solución con IA
            </h3>
            <p className="text-xl" style={{color: 'rgba(13, 59, 102, 0.8)'}}>Tecnología de vanguardia para problemas financieros complejos</p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {/* Solución 1 */}
            <div className="rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid rgba(13, 59, 102, 0.2)'}}>
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6" style={{backgroundColor: '#0D3B66'}}>
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-2xl font-bold mb-4 text-center" style={{color: '#0D3B66'}}>
                IA para Licitaciones Inteligentes
              </h4>
              
              <div className="mb-6">
                <h5 className="font-semibold mb-3" style={{color: '#0D3B66'}}>Cómo lo resolvimos:</h5>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>NLP avanzado</strong> para análisis automático de documentos
                  </li>
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>Machine Learning</strong> para detección de riesgos y anomalías
                  </li>
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>Algoritmos de scoring</strong> para evaluación objetiva
                  </li>
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>Dashboard intuitivo</strong> para toma de decisiones
                  </li>
                </ul>
              </div>

              <div className="p-4 rounded-lg mb-6" style={{backgroundColor: 'rgba(31, 170, 89, 0.1)', border: '1px solid #1FAA59'}}>
                <p className="font-medium text-center" style={{color: '#0D3B66'}}>
                  <strong>Resultado:</strong> 75% menos tiempo, 90% menos errores
                </p>
              </div>

              <Link href="/reto1" className="inline-block w-full">
                <button className="w-full text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg" style={{backgroundColor: '#0D3B66'}}>
                  Ver Demo Completa
                </button>
              </Link>
            </div>

            {/* Solución 2 */}
            <div className="rounded-2xl shadow-xl p-8 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid rgba(31, 170, 89, 0.2)'}}>
              <div className="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-6" style={{backgroundColor: '#1FAA59'}}>
                <TrendingUp className="w-8 h-8 text-white" />
              </div>
              <h4 className="text-2xl font-bold mb-4 text-center" style={{color: '#0D3B66'}}>
                IA para Crédito Inclusivo
              </h4>
              
              <div className="mb-6">
                <h5 className="font-semibold mb-3" style={{color: '#0D3B66'}}>Cómo lo resolvimos:</h5>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>Datos alternativos</strong> de redes sociales y reputación digital
                  </li>
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>Análisis de comportamiento</strong> comercial y transaccional
                  </li>
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>Modelos predictivos</strong> para evaluación de riesgo
                  </li>
                  <li className="flex items-start">
                    <span className="mr-2" style={{color: '#1FAA59'}}>✓</span>
                    <strong>Scoring dinámico</strong> que se actualiza en tiempo real
                  </li>
                </ul>
              </div>

              <div className="p-4 rounded-lg mb-6" style={{backgroundColor: 'rgba(31, 170, 89, 0.1)', border: '1px solid #1FAA59'}}>
                <p className="font-medium text-center" style={{color: '#0D3B66'}}>
                  <strong>Resultado:</strong> 40% más PYMEs con acceso a crédito
                </p>
              </div>

              <Link href="/reto2" className="inline-block w-full">
                <button className="w-full text-white font-semibold py-3 px-6 rounded-lg transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg" style={{backgroundColor: '#0D3B66'}}>
                  Ver Demo Completa
                </button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Methodology */}
      <section className="py-16 px-4" style={{background: 'rgba(31, 170, 89, 0.05)'}}>
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl font-bold mb-8" style={{color: '#0D3B66'}}>
            Nuestra Metodología
          </h3>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="p-6 rounded-lg shadow" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #1FAA59'}}>
              <div className="flex justify-center mb-4">
                <Search className="w-8 h-8 text-green-600" />
              </div>
              <h4 className="font-semibold mb-2" style={{color: '#0D3B66'}}>1. Investigación</h4>
              <p className="text-gray-600 text-sm">Análisis profundo del problema y sus stakeholders</p>
            </div>
            <div className="p-6 rounded-lg shadow" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #0D3B66'}}>
              <div className="flex justify-center mb-4">
                <Brain className="w-8 h-8 text-blue-600" />
              </div>
              <h4 className="font-semibold mb-2" style={{color: '#0D3B66'}}>2. Diseño IA</h4>
              <p className="text-gray-600 text-sm">Arquitectura de modelos de machine learning especializados</p>
            </div>
            <div className="p-6 rounded-lg shadow" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #1FAA59'}}>
              <div className="flex justify-center mb-4">
                <Zap className="w-8 h-8 text-yellow-600" />
              </div>
              <h4 className="font-semibold mb-2" style={{color: '#0D3B66'}}>3. Desarrollo</h4>
              <p className="text-gray-600 text-sm">Implementación ágil con tecnologías de vanguardia</p>
            </div>
            <div className="p-6 rounded-lg shadow" style={{backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '2px solid #0D3B66'}}>
              <div className="flex justify-center mb-4">
                <BarChart3 className="w-8 h-8 text-purple-600" />
              </div>
              <h4 className="font-semibold mb-2" style={{color: '#0D3B66'}}>4. Validación</h4>
              <p className="text-gray-600 text-sm">Pruebas exhaustivas y métricas de impacto real</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 px-4" style={{background: 'white'}}>
        <div className="max-w-4xl mx-auto text-center">
          <h3 className="text-3xl font-bold mb-6" style={{color: '#0D3B66'}}>
            ¿Listo para Ver la IA en Acción?
          </h3>
          <p className="text-xl mb-8" style={{color: 'rgba(13, 59, 102, 0.8)'}}>
            Explora nuestras demos interactivas y descubre cómo la inteligencia artificial puede transformar industrias completas.
          </p>
          <div className="flex flex-col gap-4 justify-center">
            <Link href="/reto1">
              <button className="text-white font-semibold py-3 px-8 rounded-lg transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg" style={{backgroundColor: '#0D3B66'}}>
                Demo: Licitaciones Inteligentes
              </button>
            </Link>
            <Link href="/reto2">
              <button className="text-white font-semibold py-3 px-8 rounded-lg transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg" style={{backgroundColor: '#0D3B66'}}>
                Demo: Crédito Inclusivo
              </button>
            </Link>
            <Link href="/equipo">
              <button className="font-semibold py-3 px-8 rounded-lg transition-all duration-300 transform hover:-translate-y-1 hover:shadow-lg" style={{backgroundColor: 'white', color: '#0D3B66', border: '2px solid #1FAA59'}}>
                Conoce al Equipo
              </button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-4 relative overflow-hidden" style={{background: 'rgba(31, 170, 89, 0.1)'}}>
        <div className="max-w-7xl mx-auto text-center relative z-20">
          <div className="flex justify-center items-center gap-4 mb-6">
            <img 
              src="/finova-logo.png" 
              alt="FINOVA Logo" 
              className="w-12 h-12 object-contain"
            />
            <h3 className="text-2xl font-bold" style={{color: '#0D3B66'}}>FINOVA</h3>
          </div>
          <p className="mb-2 text-lg" style={{color: 'rgba(13, 59, 102, 0.9)'}}>
            Innovando hoy, transformando finanzas
          </p>
          <p style={{color: 'rgba(13, 59, 102, 0.8)'}}>
            Desarrollado con <span style={{color: '#1FAA59'}}>❤️</span> por el equipo FINOVA - Código que impulsa tu futuro financiero
          </p>
        </div>
      </footer>
    </div>
  );
}
