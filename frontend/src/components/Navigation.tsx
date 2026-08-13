"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Cpu, Layers, Home, BookOpen, Activity, ShieldAlert } from "lucide-react";

export default function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="flex items-center gap-2">
      <TopbarItem href="/dashboard" icon={<Home className="w-3.5 h-3.5" />} label="DASHBOARD" pathname={pathname} />
      <TopbarItem href="/research" icon={<BookOpen className="w-3.5 h-3.5" />} label="RESEARCH" pathname={pathname} />
      <TopbarItem href="/models" icon={<Cpu className="w-3.5 h-3.5" />} label="MODELS" pathname={pathname} />
      <TopbarItem href="/validation" icon={<Activity className="w-3.5 h-3.5" />} label="VALIDATION" pathname={pathname} />
      <TopbarItem href="/backtest" icon={<Layers className="w-3.5 h-3.5" />} label="BACKTESTING" pathname={pathname} />
      <TopbarItem href="/risk" icon={<ShieldAlert className="w-3.5 h-3.5" />} label="RISK" pathname={pathname} />
    </nav>
  );
}

function TopbarItem({ href, icon, label, pathname }: { href: string, icon: React.ReactNode, label: string, pathname: string }) {
  const active = pathname === href || (pathname.startsWith(href) && href !== '/');
  
  return (
    <Link href={href} className={`flex items-center gap-2 px-4 py-1.5 text-[11px] font-semibold tracking-widest transition-colors rounded-sm border ${active ? 'bg-quant-active text-quant-text-primary border-quant-border' : 'text-quant-text-secondary border-transparent hover:text-quant-text-primary hover:bg-quant-elevated'}`}>
      {icon}
      {label}
    </Link>
  );
}
