'use client';

import dynamic from 'next/dynamic';
import { useEffect } from 'react';
import { weatherAPI } from '@/lib/api';

const FloatingBackground = dynamic(
  () => import('@/components/ui/FloatingBackground'),
  { ssr: false }
);

const HeroSection = dynamic(() => import('@/components/sections/HeroSection'));
const DataSection = dynamic(() => import('@/components/sections/DataSection'));
const EducationSection = dynamic(() => import('@/components/sections/EducationSection'));
const Footer = dynamic(() => import('@/components/layout/Footer'));

const MapSection = dynamic(
  () => import('@/components/sections/MapSection'),
  { 
    ssr: false,
    loading: () => <div className="min-h-screen flex items-center justify-center">載入地圖中...</div>
  }
);

export default function Home() {
  // 測試 Flask API 連接
  useEffect(() => {
    async function testAPI() {
      try {
        // 測試 API 連接
        const testResult = await weatherAPI.test();
        console.log('✅ API 連接成功:', testResult);
        
        // 測試實際資料 API（可選）
        // const weatherData = await weatherAPI.getHistoryData(2024, 1, 10, 20);
        // console.log('✅ 氣象資料:', weatherData);
        
      } catch (error) {
        console.error('❌ API 連接失敗:', error);
      }
    }

    testAPI();
  }, []);

  return (
    <>
      <FloatingBackground className="fixed inset-0 z-0 pointer-events-none" />
      
      <main className="relative z-10 overflow-x-hidden scroll-smooth min-h-screen">
        <HeroSection />
        <MapSection />
        <DataSection />
        <EducationSection />
        <Footer />
      </main>
    </>
  );
}
