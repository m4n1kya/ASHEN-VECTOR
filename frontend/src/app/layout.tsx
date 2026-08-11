import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";
import { Search, Settings, Activity, LayoutDashboard, Target, Layers, Database, LineChart, Cpu, Zap, FolderSearch, Triangle, GripHorizontal, FlaskConical, Beaker } from "lucide-react";

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
      <body className={`${inter.variable} ${jetbrains.variable} font-sans bg-quant-bg text-quant-text-primary h-screen flex overflow-hidden`}>
        
        {/* SIDEBAR */}
        <aside className="w-56 bg-quant-sidebar border-r border-quant-border flex flex-col hidden md:flex shrink-0">
          <div className="h-14 border-b border-quant-border flex items-center px-6 gap-3">
            <Triangle className="w-4 h-4 text-quant-text-secondary fill-quant-text-secondary" />
            <span className="font-semibold text-xs tracking-widest text-quant-text-primary">ASHEN-VECTOR</span>
          </div>
          
          <nav className="flex-1 px-4 py-6 flex flex-col gap-1 overflow-y-auto">
            <SidebarItem href="/" icon={<LayoutDashboard className="w-4 h-4" />} label="OVERVIEW" active={true} />
            <SidebarItem href="#" icon={<Activity className="w-4 h-4" />} label="MARKETS" />
            <SidebarItem href="#" icon={<Target className="w-4 h-4" />} label="FACTORS" />
            <SidebarItem href="#" icon={<Zap className="w-4 h-4" />} label="SIGNALS" />
            <SidebarItem href="#" icon={<Cpu className="w-4 h-4" />} label="MODELS" />
            <SidebarItem href="#" icon={<LineChart className="w-4 h-4" />} label="RISK" />
            <SidebarItem href="/backtest" icon={<Layers className="w-4 h-4" />} label="BACKTESTING" />
            <SidebarItem href="#" icon={<FlaskConical className="w-4 h-4" />} label="EXPERIMENTS" />
          </nav>
          
          <div className="px-4 py-4 mt-auto">
            <Link href="#" className="flex items-center gap-3 px-4 py-2 text-xs font-semibold tracking-wider text-quant-text-secondary hover:text-quant-text-primary transition-colors rounded-md">
              <Settings className="w-4 h-4" />
              SETTINGS
            </Link>
          </div>
        </aside>

        <div className="flex-1 flex flex-col min-w-0">
          {/* TOPBAR */}
          <header className="h-14 border-b border-quant-border bg-quant-sidebar flex items-center justify-between px-6 shrink-0">
            <div className="flex items-center gap-2 text-xs text-quant-text-secondary tracking-widest">
              <div className="w-2 h-2 rounded-full bg-quant-up-text mr-1"></div>
              SYSTEM ONLINE
            </div>
            
            <div className="flex items-center gap-6 text-quant-text-secondary text-xs">
              <span className="hidden lg:inline">Market Dataset</span>
              
              {/* SEARCH BOX */}
              <div className="flex items-center bg-quant-bg border border-quant-border rounded-md px-3 py-1.5 w-64">
                <input 
                  type="text" 
                  placeholder="Search Instrument" 
                  className="bg-transparent border-none outline-none w-full text-quant-text-primary placeholder:text-quant-text-muted text-xs"
                />
                <span className="text-[10px] bg-quant-sidebar px-1.5 py-0.5 rounded text-quant-text-muted ml-2">AAPL</span>
              </div>
              
              <div className="flex items-center gap-1.5 cursor-pointer hover:text-quant-text-primary transition-colors">
                <Settings className="w-4 h-4" />
                <span>Settings</span>
              </div>
            </div>
          </header>
          
          {/* MAIN CONTENT */}
          <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-quant-bg">
            <div className="max-w-[1600px] mx-auto h-full">
              {children}
            </div>
          </main>
        </div>
        
      </body>
    </html>
  );
}

function SidebarItem({ href, icon, label, active = false }: { href: string, icon: React.ReactNode, label: string, active?: boolean }) {
  // In a real app, 'active' would be determined by usePathname()
  return (
    <Link href={href} className={`flex items-center gap-3 px-4 py-2.5 text-[11px] font-semibold tracking-widest transition-colors rounded-md ${active ? 'bg-quant-active text-quant-text-primary' : 'text-quant-text-secondary hover:text-quant-text-primary'}`}>
      {icon}
      {label}
    </Link>
  );
}
