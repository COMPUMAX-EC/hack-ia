import React from 'react';

interface ByteMascotProps {
  size?: 'small' | 'medium' | 'large';
  animated?: boolean;
  className?: string;
}

export default function ByteMascot({ size = 'medium', animated = false, className = '' }: ByteMascotProps) {
  const sizeClasses = {
    small: 'w-12 h-12',
    medium: 'w-16 h-16',
    large: 'w-24 h-24'
  };

  return (
    <div className={`${sizeClasses[size]} ${className} ${animated ? 'animate-pulse' : ''} flex items-center justify-center`}>
      <svg 
        viewBox="0 0 100 100" 
        className="w-full h-full"
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Fox body */}
        <ellipse cx="50" cy="65" rx="25" ry="20" fill="#0D3B66" />
        
        {/* Fox head */}
        <circle cx="50" cy="40" r="20" fill="#0D3B66" />
        
        {/* Fox ears */}
        <path d="M35 25 L40 35 L30 35 Z" fill="#0D3B66" />
        <path d="M65 25 L70 35 L60 35 Z" fill="#0D3B66" />
        <path d="M37 27 L40 32 L34 32 Z" fill="#1FAA59" />
        <path d="M63 27 L66 32 L60 32 Z" fill="#1FAA59" />
        
        {/* Fox snout */}
        <ellipse cx="50" cy="45" rx="8" ry="6" fill="#F25C05" />
        
        {/* Fox eyes */}
        <circle cx="44" cy="37" r="3" fill="white" />
        <circle cx="56" cy="37" r="3" fill="white" />
        <circle cx="44" cy="37" r="1.5" fill="#0D3B66" />
        <circle cx="56" cy="37" r="1.5" fill="#0D3B66" />
        
        {/* Fox nose */}
        <circle cx="50" cy="43" r="1.5" fill="#0D3B66" />
        
        {/* Tech elements - circuit lines */}
        <path d="M25 70 L30 70 L32 72 L35 72" stroke="#1FAA59" strokeWidth="1" fill="none" />
        <path d="M75 70 L70 70 L68 72 L65 72" stroke="#1FAA59" strokeWidth="1" fill="none" />
        <circle cx="35" cy="72" r="1" fill="#1FAA59" />
        <circle cx="65" cy="72" r="1" fill="#1FAA59" />
        
        {/* Digital elements */}
        <rect x="20" y="55" width="3" height="3" fill="#F25C05" transform="rotate(45 21.5 56.5)" />
        <rect x="77" y="55" width="3" height="3" fill="#F25C05" transform="rotate(45 78.5 56.5)" />
        
        {/* Tail with tech pattern */}
        <path d="M25 75 Q15 70 20 60 Q25 65 30 70" fill="#0D3B66" />
        <path d="M22 67 L25 70 L20 72 Z" fill="#1FAA59" />
      </svg>
    </div>
  );
}
