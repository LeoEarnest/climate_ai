'use client';

import dynamic from 'next/dynamic';
import HeroSection from '@/components/sections/HeroSection';
import DataSection from '@/components/sections/DataSection';
import EducationSection from '@/components/sections/EducationSection';
import Footer from '@/components/layout/Footer';
import FloatingBackground from '@/components/ui/FloatingBackground';

// 動態匯入 MapSection，關閉 SSR 避免 Hydration Mismatch
const MapSection = dynamic(
  () => import('@/components/sections/MapSection'),
  { ssr: false }
);

export default function Home() {
  return (
    <>
      {/* 底層背景 */}
      {/* <FloatingBackground className="fixed inset-0 z-0 pointer-events-none" /> */}

      {/* 主要內容 */}
      <main className="relative z-40 overflow-visible scroll-smooth">
        {/* 首頁區塊 */}
        <HeroSection />

        {/* 地圖區塊 */}
        <MapSection />

        {/* 資料區塊 */}
        <DataSection />

        {/* 教育區塊 */}
        <EducationSection />

        {/* 頁腳 */}
        <Footer />
      </main>
    </>
  );
}
