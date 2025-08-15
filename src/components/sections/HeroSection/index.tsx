'use client';
import { motion } from 'framer-motion';

export default function HeroSection() {
  const scrollToMap = () =>
    document.getElementById('map-section')?.scrollIntoView({ behavior: 'smooth' });

  return (
    <section className="min-h-screen flex flex-col items-center justify-center px-4 relative">
      {/* 大膽醒目的主標題 */}
      <motion.h1
        className="text-[clamp(3rem,8vw,6rem)] font-black text-primary mb-6"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1 }}
      >
        VERDISLE
      </motion.h1>
      {/* 簡潔副標 */}
      <motion.p
        className="text-white text-lg md:text-xl max-w-lg mb-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5, duration: 1 }}
      >
        Islands of Heat, Cities of Change
      </motion.p>
      <motion.button
        onClick={scrollToMap}
        className="text-white hover:text-primary transition text-sm md:text-base"
        animate={{ y: [0, 6, 0] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        Scroll ↓
      </motion.button>
    </section>
  );
}
