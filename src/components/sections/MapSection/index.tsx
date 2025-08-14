'use client';

import { useRef, useState, useEffect } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';

export default function MapSection() {
  // ✅ 所有 Hooks 都在頂層，在任何條件性返回之前
  const [mounted, setMounted] = useState(false);
  const sectionRef = useRef<HTMLDivElement>(null);
  
  // 即使在 SSR 階段也要調用這些 hooks
  const { scrollYProgress } = useScroll({
    target: sectionRef,
    offset: ['start end', 'end start'],
  });

  const titleOpacity = useTransform(
    scrollYProgress,
    [0.1, 0.3, 0.4, 0.6, 0.9, 1],
    [0, 1, 1, 0.8, 0.8, 0]
  );
  
  const titleScale = useTransform(
    scrollYProgress,
    [0.1, 0.3, 0.4, 0.6],
    [0.8, 1, 0.3, 0.3]
  );

  const titleX = useTransform(
    scrollYProgress,
    [0.1, 0.4, 0.6],
    [0, 0, 350]
  );
  
  const titleY = useTransform(
    scrollYProgress,
    [0.1, 0.4, 0.6],
    [0, 0, -280]
  );

  const descriptionOpacity = useTransform(
    scrollYProgress,
    [0.1, 0.3, 0.4, 0.5],
    [0, 1, 1, 0]
  );

  const mapOpacity = useTransform(scrollYProgress, [0.4, 0.6, 1], [0, 1, 1]);
  const mapScale = useTransform(scrollYProgress, [0.4, 0.6, 1], [0.9, 1, 1]);

  // ✅ useEffect 在所有其他 hooks 之後
  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <section
      id="map-section"
      ref={sectionRef}
      className="relative overflow-hidden h-[200vh] bg-transparent"
      style={{ opacity: mounted ? 1 : 0 }} // 用樣式控制顯示
    >
      {/* 標題層 */}
      <div className="sticky top-0 h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.8, x: 0, y: 0 }}
          style={{ 
            opacity: mounted ? titleOpacity : 0, 
            scale: mounted ? titleScale : 0.8,
            x: mounted ? titleX : 0,
            y: mounted ? titleY : 0
          }}
          className="text-center px-4 w-full flex flex-col items-center justify-center"
        >
          <h2
            className="font-display text-white tracking-wider text-center"
            style={{ 
              fontSize: 'clamp(1.2rem, 6vw, 4rem)',
              lineHeight: '1.2'
            }}
          >
            Heat Island Model
          </h2>
          <motion.p
            style={{ opacity: mounted ? descriptionOpacity : 0 }}
            className="font-sans text-gray-100 font-regular tracking-wide text-center max-w-2xl mx-auto mt-4"
            style={{ 
              fontSize: 'clamp(0.8rem, 2vw, 1.8rem)',
              lineHeight: '1.4'
            }}
          >
            理解雙北十年的溫度脈動 ↔ 以植物為核心預測未來場景
          </motion.p>
        </motion.div>
      </div>

      {/* 模型層 */}
      <div className="sticky top-0 h-screen flex items-center justify-center">
        <motion.div
          style={{ 
            opacity: mounted ? mapOpacity : 0, 
            scale: mounted ? mapScale : 0.9 
          }}
          className="
            relative
            w-[90vw] h-[90vh]
            max-w-[1200px] max-h-[800px]
            rounded-3xl border border-gray-400/30
            bg-[rgba(0,0,0,0.3)] backdrop-blur-lg
            p-4
            shadow-2xl
            flex flex-col items-center justify-center
            mt-8
          "
        >
          <div className="text-center w-full">
            <h3 
              className="font-alt font-bold text-white mb-3 drop-shadow text-center"
              style={{
                fontSize: 'clamp(1.2rem, 3vw, 2.5rem)'
              }}
            >
              🗺️ 模型區域
            </h3>
            <p 
              className="font-sans text-gray-200 text-center"
              style={{
                fontSize: 'clamp(0.9rem, 2vw, 1.5rem)'
              }}
            >
              這裡將顯示互動式模型
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
