'use client';

import { useState } from 'react';
import Header from '../../components/Header';

export default function Reto1() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const analyzeDocument = async () => {
    if (!selectedFile) return;
    
    setIsAnalyzing(true);
    
    // Simulamos el análisis de IA
    setTimeout(() => {
      setAnalysisResult({
        documentType: 'Licitación Pública de Infraestructura',
        riskLevel: 'Medio',
        technicalCompliance: 85,
        legalCompliance: 92,
        recommendations: [
          'Revisar cláusulas de penalización por retraso',
          'Verificar certificaciones técnicas del proveedor',
          'Evaluar garantías de cumplimiento'
        ],
        estimatedProcessingTime: '2.5 horas',
        traditionalTime: '8-12 horas'
      });
      setIsAnalyzing(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100">
      <Header currentPage="reto1" />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Title Section */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Optimización Inteligente en Procesos de Licitación
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Nuestra solución de IA analiza documentos de licitación automáticamente, 
            detecta riesgos y facilita la toma de decisiones informadas.
          </p>
        </div>

        {/* Demo Section */}
        <div className="grid lg:grid-cols-2 gap-8 mb-12">
          {/* Upload Area */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Análisis de Documento
            </h2>
            
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
              <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="text-gray-400 mb-4">
                  <svg className="mx-auto h-12 w-12" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                    <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
                <p className="text-gray-600 mb-2">
                  Arrastra tu documento de licitación aquí o haz clic para subir
                </p>
                <p className="text-sm text-gray-400">
                  Soporta PDF, DOCX, DOC
                </p>
              </label>
            </div>

            {selectedFile && (
              <div className="bg-blue-50 p-4 rounded-lg mb-6">
                <p className="text-blue-800 font-medium">
                  📄 {selectedFile.name}
                </p>
                <p className="text-blue-600 text-sm">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            )}

            <button
              onClick={analyzeDocument}
              disabled={!selectedFile || isAnalyzing}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors duration-200"
            >
              {isAnalyzing ? 'Analizando...' : 'Analizar con IA'}
            </button>
          </div>

          {/* Results Area */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Resultados del Análisis
            </h2>

            {isAnalyzing && (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p className="text-gray-600">Analizando documento con IA...</p>
              </div>
            )}

            {analysisResult && !isAnalyzing && (
              <div className="space-y-6">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">Tipo de Documento</h3>
                  <p className="text-gray-700">{analysisResult.documentType}</p>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-green-800 mb-1">Cumplimiento Legal</h4>
                    <p className="text-2xl font-bold text-green-600">{analysisResult.legalCompliance}%</p>
                  </div>
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-semibold text-blue-800 mb-1">Cumplimiento Técnico</h4>
                    <p className="text-2xl font-bold text-blue-600">{analysisResult.technicalCompliance}%</p>
                  </div>
                </div>

                <div className="bg-yellow-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-yellow-800 mb-2">Nivel de Riesgo</h4>
                  <span className="inline-block bg-yellow-200 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
                    {analysisResult.riskLevel}
                  </span>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 mb-3">Recomendaciones</h4>
                  <ul className="space-y-2">
                    {analysisResult.recommendations.map((rec: string, index: number) => (
                      <li key={index} className="flex items-start">
                        <span className="text-blue-500 mr-2">•</span>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-green-800 mb-2">Eficiencia</h4>
                  <p className="text-sm text-green-700">
                    <strong>Tiempo con IA:</strong> {analysisResult.estimatedProcessingTime}
                  </p>
                  <p className="text-sm text-green-700">
                    <strong>Tiempo tradicional:</strong> {analysisResult.traditionalTime}
                  </p>
                  <p className="text-sm text-green-600 font-medium mt-2">
                    ⚡ Reducción del 75% en tiempo de análisis
                  </p>
                </div>
              </div>
            )}

            {!analysisResult && !isAnalyzing && (
              <div className="text-center py-8 text-gray-400">
                <p>Sube un documento para ver los resultados del análisis de IA</p>
              </div>
            )}
          </div>
        </div>

        {/* Features Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            Características de la Solución
          </h2>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📄</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Análisis Automático</h3>
              <p className="text-gray-600 text-sm">Procesamiento inteligente de documentos legales y técnicos</p>
            </div>
            
            <div className="text-center">
              <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">⚠️</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Detección de Riesgos</h3>
              <p className="text-gray-600 text-sm">Identificación automática de cláusulas problemáticas</p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">⚖️</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Comparación Inteligente</h3>
              <p className="text-gray-600 text-sm">Evaluación objetiva entre múltiples propuestas</p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Optimización de Tiempo</h3>
              <p className="text-gray-600 text-sm">Reducción significativa en tiempos de evaluación</p>
            </div>
          </div>
        </div>

        {/* Impact Section */}
        <div className="bg-blue-600 text-white rounded-2xl shadow-lg p-8 text-center">
          <h2 className="text-3xl font-bold mb-6">Impacto Esperado</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <p className="text-4xl font-bold mb-2">75%</p>
              <p className="text-blue-100">Reducción en tiempo de análisis</p>
            </div>
            <div>
              <p className="text-4xl font-bold mb-2">90%</p>
              <p className="text-blue-100">Menos errores humanos</p>
            </div>
            <div>
              <p className="text-4xl font-bold mb-2">60%</p>
              <p className="text-blue-100">Mejora en transparencia</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
