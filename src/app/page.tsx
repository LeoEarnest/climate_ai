// app/page.tsx
'use client';

import ClientLayout from './ClientLayout';
import dynamic from 'next/dynamic';
import HeroSection from '@/components/sections/HeroSection';
import EducationSection from '@/components/sections/EducationSection';
import Footer from '@/components/layout/Footer';
import NoSSR from '@/components/NoSSR';
import BackgroundParticles from '@/components/BackgroundParticles';

const MapSection = dynamic(
  () => import('@/components/sections/MapSection'),
  {
    ssr: false,
    loading: () => (
      <section className="min-h-screen py-12 px-6 bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading Map...</div>
      </section>
    ),
  }
);

export default function Home() {
  return (
    <ClientLayout>
      <main className="min-h-screen text-white relative">
        {/* 僅在客戶端渲染的背景粒子 */}
        <NoSSR>
          <BackgroundParticles />
        </NoSSR>

        {/* 主要內容區塊 */}
        <div className="relative z-10">
          <HeroSection />
          <MapSection />
          <EducationSection />
          <Footer />
        </div>
      </main>
    </ClientLayout>
  );
}
