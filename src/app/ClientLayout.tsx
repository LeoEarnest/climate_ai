// app/ClientLayout.tsx
'use client';

import { useState, useEffect, ReactNode } from 'react';
import Loading from './loading'; // 引用 app/loading.tsx 中的 Loading 組件

export default function ClientLayout({
  children,
}: {
  children: ReactNode;
}) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // 首次進入 1.5 秒後結束載入動畫
    const timer = setTimeout(() => setIsLoading(false), 2500);
    return () => clearTimeout(timer);
  }, []);

  // 若仍在載入，顯示自訂 Loading；否則顯示子內容
  return <>{isLoading ? <Loading /> : children}</>;
}
