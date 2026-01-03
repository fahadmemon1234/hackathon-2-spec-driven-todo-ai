import React from 'react';
import Navbar from '@/components/Navbar';
import HeroSection from '@/components/HeroSection';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-luxury-background">
      <Navbar />
      <HeroSection />
    </div>
  );
};

export default HomePage;