import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { Cpu, Layers, Triangle } from "lucide-react";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

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
      <body className={`${inter.variable} ${jetbrains.variable} font-sans bg-quant-bg text-quant-text-primary h-screen flex flex-col overflow-hidden`}>
        
        {/* TOPBAR */}
        <header className="h-14 border-b border-quant-border bg-quant-sidebar flex items-center justify-between px-6 shrink-0">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-3 border-r border-quant-border pr-8 h-14">
              <img src="/logo.png" alt="Logo" className="w-5 h-5 object-contain" />
              <span className="font-semibold text-xs tracking-widest text-quant-text-primary">ASHEN-VECTOR</span>
            </div>
            
            <nav className="flex items-center gap-2">
              <TopbarItem href="/" icon={<Cpu className="w-4 h-4" />} label="MODELS" active={true} />
              <TopbarItem href="/backtest" icon={<Layers className="w-4 h-4" />} label="BACKTESTING" />
            </nav>
          </div>
          
          <div className="flex items-center gap-2 text-xs text-quant-text-secondary tracking-widest">
            <div className="w-2 h-2 rounded-full bg-quant-up-text mr-1"></div>
            SYSTEM ONLINE
          </div>
        </header>
        
        {/* MAIN CONTENT */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-quant-bg">
          <div className="max-w-[1600px] mx-auto h-full">
            {children}
          </div>
        </main>
        
      </body>
    </html>
  );
}

function TopbarItem({ href, icon, label, active = false }: { href: string, icon: React.ReactNode, label: string, active?: boolean }) {
  return (
    <Link href={href} className={`flex items-center gap-2 px-4 py-1.5 text-[11px] font-semibold tracking-widest transition-colors rounded-sm border ${active ? 'bg-quant-active text-quant-text-primary border-quant-border' : 'text-quant-text-secondary border-transparent hover:text-quant-text-primary hover:bg-quant-elevated'}`}>
      {icon}
      {label}
    </Link>
  );
}
