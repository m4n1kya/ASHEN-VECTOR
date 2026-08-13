import StockDetailClient from "./StockDetailClient";
import { Metadata } from "next";

export async function generateMetadata({ params }: { params: { symbol: string } }): Promise<Metadata> {
  return {
    title: `${params.symbol.toUpperCase()} | Quantitative Analysis`,
    description: "ASHEN-VECTOR Quantitative Market Intelligence",
  };
}

export default function StockDetailPage({ params }: { params: { symbol: string } }) {
  return <StockDetailClient symbol={params.symbol.toUpperCase()} />;
}
