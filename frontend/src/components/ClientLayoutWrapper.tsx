'use client';

import Header from '@/components/layout/Header';
import React from 'react';

export default function ClientLayoutWrapper({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      {children}
    </>
  );
}
