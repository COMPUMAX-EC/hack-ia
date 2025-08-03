import { ReactNode } from 'react';
import Header from './Header';

interface LayoutProps {
  children: ReactNode;
  currentPage?: 'inicio' | 'reto1' | 'reto2' | 'equipo';
  backgroundColor?: string;
  className?: string;
}

export default function Layout({ 
  children, 
  currentPage = 'inicio', 
  backgroundColor = 'white',
  className = ''
}: LayoutProps) {
  return (
    <div className={`min-h-screen ${className}`} style={{background: backgroundColor}}>
      <Header currentPage={currentPage} />
      {children}
    </div>
  );
}
