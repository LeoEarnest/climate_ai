'use client';

import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

export default function EducationSection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const isInView = useInView(sectionRef, { once: true, margin: '-100px' });

  return (
    <section ref={sectionRef} className="py-20 px-4 bg-transparent relative overflow-visible">
      {/* 科技噪點層 */}
      <div className="noise-overlay"></div>

      <div className="max-w-4xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 60 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <h3 className="text-[clamp(2rem,6vw,3.5rem)] font-black text-primary mb-6">
            Urban Heat School 熱島小學堂
          </h3>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="space-y-6"
        >
          {/* 對話框 */}
          <div className="bg-gray-800 bg-opacity-50 backdrop-blur-md rounded-xl p-6 max-w-lg">
            <p className="text-white">🌿 你知道植被是如何降低城市溫度的嗎？</p>
          </div>
          
          {/* 回答框 */}
          <div className="bg-gray-700 bg-opacity-40 backdrop-blur-md rounded-xl p-6 max-w-lg ml-auto">
            <p className="text-white">請告訴我更多！</p>
          </div>
          
          {/* 解釋框 */}
          <div className="bg-gray-800 bg-opacity-50 backdrop-blur-md rounded-xl p-6 max-w-xl">
            <p className="text-white">
              植物透過蒸散作用，將水分釋放到空氣中，這個過程會吸收熱量，就像天然的冷氣機一樣。
              一棵成年樹木每天可以蒸散400公升的水，相當於五台冷氣機的降溫效果！
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
