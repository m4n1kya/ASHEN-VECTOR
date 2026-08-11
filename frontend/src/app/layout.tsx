import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { Activity, LayoutDashboard, Settings } from "lucide-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ASHEN-VECTOR",
  description: "Quantitative Market Intelligence",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-ashen-black text-ashen-bone min-h-screen flex flex-col`}>
        <header className="border-b border-ashen-charcoal-light bg-ashen-charcoal/80 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="text-ashen-up w-6 h-6" />
              <span className="font-bold text-xl tracking-widest text-ashen-bone-light">ASHEN-VECTOR</span>
            </div>
            
            <nav className="flex gap-6">
              <Link href="/" className="flex items-center gap-2 text-ashen-ash-light hover:text-ashen-bone transition-colors">
                <LayoutDashboard className="w-4 h-4" />
                <span className="text-sm font-medium">Dashboard</span>
              </Link>
              <Link href="/backtest" className="flex items-center gap-2 text-ashen-ash-light hover:text-ashen-bone transition-colors">
                <Settings className="w-4 h-4" />
                <span className="text-sm font-medium">Backtest Engine</span>
              </Link>
            </nav>
          </div>
        </header>
        
        <main className="flex-1 w-full max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
