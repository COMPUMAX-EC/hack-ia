import Link from 'next/link';
import Image from 'next/image';

interface HeaderProps {
  currentPage?: 'inicio' | 'reto1' | 'reto2' | 'equipo';
}

export default function Header({ currentPage = 'inicio' }: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-20">
              <Image 
                src="/finova-logo.png" 
                alt="FINOVA Logo" 
                width={36}
                height={36}
                className="w-6 h-6 object-contain"
                style={{maxWidth: '36px', maxHeight: '36px'}}
              />
              <span className="text-2xl font-bold" style={{color: '#0D3B66', marginLeft: '8px'}}>FINOVA</span>
            </Link>
          </div>
          <nav className="flex gap-8">
            {currentPage === 'inicio' ? (
              <span className="font-medium" style={{color: '#1FAA59'}}>Inicio</span>
            ) : (
              <Link href="/" className="finova-nav-link">Inicio</Link>
            )}
            
            {currentPage === 'reto1' ? (
              <span className="font-medium" style={{color: '#1FAA59'}}>Licitaciones IA</span>
            ) : (
              <Link href="/reto1" className="finova-nav-link">Licitaciones IA</Link>
            )}
            
            {currentPage === 'reto2' ? (
              <span className="font-medium" style={{color: '#1FAA59'}}>Crédito PYME IA</span>
            ) : (
              <Link href="/reto2" className="finova-nav-link">Crédito PYME IA</Link>
            )}
            
            {currentPage === 'equipo' ? (
              <span className="font-medium" style={{color: '#1FAA59'}}>Equipo</span>
            ) : (
              <Link href="/equipo" className="finova-nav-link">Equipo</Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  );
}
