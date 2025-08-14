// src/app/layout.tsx
import './globals.css';
import type { Metadata } from 'next';
import FloatingBackground from '@/components/ui/FloatingBackground';

export const metadata: Metadata = {
  title: 'VERDISLE – Islands of Heat, Cities of Change',
  description: 'Data science art · Heat island live monitoring',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-Hant" className="scroll-smooth">
      <body suppressHydrationWarning>
        <FloatingBackground className="fixed inset-0 z-0 pointer-events-none" />
        <div className="noise-overlay" />
        <main className="relative z-10">{children}</main>
      </body>
    </html>
  );
}
