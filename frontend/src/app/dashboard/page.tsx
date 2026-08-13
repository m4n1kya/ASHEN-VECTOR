import DashboardClient from "./DashboardClient";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Dashboard | ASHEN-VECTOR",
  description: "Quantitative Market Intelligence",
};

export default function DashboardPage() {
  return <DashboardClient />;
}
