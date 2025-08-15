'use client';

export default function Loading() {
  const text = 'LOADING';
  const colors = [
    'from-temp-low via-temp-low to-temp-low',
    'from-temp-medium via-temp-medium to-temp-medium',
    'from-temp-high via-temp-high to-temp-high',
    'from-temp-extreme via-temp-extreme to-temp-extreme',
  ];

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="flex space-x-3">
        {text.split('').map((char, idx) => (
          <span
            key={idx}
            className={`
              text-lg font-light uppercase
              tracking-wider
              leading-none
              bg-clip-text text-transparent
              bg-gradient-to-r
              ${colors[idx % colors.length]}
              animate-fadeAndFloatSm
            `}
            style={{ animationDelay: `${idx * 100}ms` }}
          >
            {char}
          </span>
        ))}
      </div>
    </div>
  );
}
