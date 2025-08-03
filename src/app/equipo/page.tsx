'use client';

import Header from '../../components/Header';
import Image from 'next/image';
import { Globe } from 'lucide-react';

export default function Equipo() {
  const teamMembers = [
    {
      name: "Jaime Pergueza",
      role: "Full Stack Developer & Team Lead",
      expertise: "React, Node.js, IA/ML, Python",
      experience: "5+ años",
      image: "/jaime.jpeg",
      isPhoto: true,
      description: "Líder técnico especializado en desarrollo full stack y implementación de soluciones de inteligencia artificial para el sector financiero.",
      linkedin: "https://www.linkedin.com/in/jaime-pergueza-40768a375/",
      github: "https://github.com/jaimepergueza"
    },
    {
      name: "Edison López", 
      role: "Data Scientist & AI Engineer",
      expertise: "Machine Learning, Python, NLP, TensorFlow",
      experience: "4+ años",
      image: "/edison.jpeg",
      isPhoto: true,
      description: "Científico de datos con experiencia en algoritmos de aprendizaje automático y procesamiento de lenguaje natural para análisis de riesgo crediticio.",
      linkedin: "https://www.linkedin.com/in/edison-l%C3%B3pez-6b69b4343/",
      github: "https://github.com/edisonvargas"
    },
    {
      name: "Geovanny Basantes",
      role: "CISO y Project Manager",
      expertise: "Ciberseguridad, Gestión de Proyectos, DevSecOps",
      experience: "3+ años",
      image: "/geovanny.webp", 
      isPhoto: true,
      description: "Desarrollador Full Stack con 3 años de experiencia, especializado en seguridad de la información y gestión de proyectos tecnológicos.",
      linkedin: "https://www.linkedin.com/in/geovanny-basantes-0471b123a/",
      github: "https://github.com/COMPUMAX-EC",
      web: "https://compumax.tech"
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <Header currentPage="equipo" />

      <div className="max-w-6xl mx-auto px-4 py-20">
        {/* Hero Section */}
        <div className="text-center mb-20 relative">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-5">
            <div className="absolute top-10 left-20 w-24 h-24 border-2 border-blue-900 rounded-full"></div>
            <div className="absolute top-20 right-32 w-16 h-16 bg-teal-600 rounded-lg transform rotate-12"></div>
          </div>
          
          <div className="relative z-10">
            <div className="inline-block px-6 py-3 bg-gradient-to-r from-teal-100 to-blue-100 rounded-full text-blue-900 font-medium mb-6">
              Conoce a FINOVA
            </div>
            <h1 className="text-5xl font-bold text-blue-900 mb-6">
              Nuestro Equipo de <span className="text-teal-600">Innovación</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Somos un equipo multidisciplinario de desarrolladores y especialistas en IA, 
              comprometidos con crear soluciones tecnológicas innovadoras que transformen las finanzas.
            </p>
          </div>
        </div>

        {/* Team Members */}
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          {teamMembers.map((member, index) => (
            <div key={index} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="flex items-center mb-6">
                <div className="w-20 h-20 mr-6 bg-gradient-to-br from-blue-50 to-teal-50 p-3 rounded-2xl flex items-center justify-center overflow-hidden">
                  {member.isPhoto ? (
                    <Image 
                      src={member.image} 
                      alt={member.name}
                      width={80}
                      height={80}
                      className="rounded-xl object-cover w-full h-full"
                    />
                  ) : (
                    <span className="text-6xl gap-6">{member.image}</span>
                  )}
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-blue-900 mb-2">{member.name}</h3>
                  <p className="text-teal-600 font-semibold mb-1">{member.role}</p>
                  <p className="text-gray-500 text-sm">{member.experience} de experiencia</p>
                </div>
              </div>
              
              <p className="text-gray-600 mb-4">{member.description}</p>
              
              <div className="bg-gray-50 p-4 rounded-lg mb-4">
                <h4 className="font-semibold text-gray-900 mb-2">Especialidades:</h4>
                <p className="text-gray-700 text-sm">{member.expertise}</p>
              </div>

              {/* Social Links */}
              <div className="flex gap-3 justify-center">
                <a 
                  href={member.linkedin} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-center w-12 h-12 bg-white hover:bg-gray-100 rounded-full transition-colors duration-200 shadow-md border"
                  title="LinkedIn"
                >
                  <Image 
                    src="/linkedin.png" 
                    alt="LinkedIn" 
                    width={32} 
                    height={32}
                    className="object-contain"
                  />
                </a>
                <a 
                  href={member.github} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-center w-12 h-12 bg-white hover:bg-gray-100 rounded-full transition-colors duration-200 shadow-md border"
                  title="GitHub"
                >
                  <Image 
                    src="/github.png" 
                    alt="GitHub" 
                    width={32} 
                    height={32}
                    className="object-contain"
                  />
                </a>
                {member.web && (
                  <a 
                    href={member.web} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="flex items-center justify-center w-12 h-12 bg-green-600 hover:bg-green-700 text-white rounded-full transition-colors duration-200"
                    title="Sitio Web"
                  >
                    <Globe className="w-6 h-6" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Company Values */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">
            Nuestros Valores
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🚀</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Innovación</h3>
              <p className="text-gray-600 text-sm">Buscamos constantemente nuevas formas de resolver problemas complejos con tecnología de vanguardia.</p>
            </div>
            
            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤝</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Colaboración</h3>
              <p className="text-gray-600 text-sm">Trabajamos en equipo, combinando nuestras fortalezas para crear soluciones excepcionales.</p>
            </div>
            
            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Impacto</h3>
              <p className="text-gray-600 text-sm">Nos enfocamos en crear tecnología que genere un impacto positivo y real en la sociedad.</p>
            </div>
          </div>
        </div>

        {/* Technologies */}
        <div className="bg-gray-900 text-white rounded-2xl shadow-lg p-8">
          <h2 className="text-3xl font-bold mb-8 text-center">
            Stack Tecnológico
          </h2>
          
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center">
              <h4 className="font-semibold mb-4 text-blue-400">Frontend</h4>
              <div className="space-y-2 text-sm">
                <p>React / Next.js</p>
                <p>TypeScript</p>
                <p>GeminiAI GPT</p>
              </div>
            </div>
            
            <div className="text-center">
              <h4 className="font-semibold mb-4 text-yellow-400">DevOps</h4>
              <div className="space-y-2 text-sm">
                <p>GCP</p>
                
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
