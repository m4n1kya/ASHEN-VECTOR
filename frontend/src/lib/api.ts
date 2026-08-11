const API_BASE = "http://127.0.0.1:8000/api";

export async function fetchInstruments() {
  const res = await fetch(`${API_BASE}/instruments`, { cache: 'no-store' });
  if (!res.ok) throw new Error("Failed to fetch instruments");
  return res.json();
}

export async function fetchOverview(symbol: string) {
  const res = await fetch(`${API_BASE}/stocks/${symbol}/overview`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed to fetch overview for ${symbol}`);
  return res.json();
}

export async function runBacktest(data: any) {
  const res = await fetch(`${API_BASE}/backtest/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error("Failed to start backtest");
  return res.json();
}

export async function checkBacktestStatus(jobId: string) {
  const res = await fetch(`${API_BASE}/backtest/jobs/${jobId}`, { cache: 'no-store' });
  if (!res.ok) throw new Error("Failed to check backtest status");
  return res.json();
}

export async function getBacktestResult(jobId: string) {
  const res = await fetch(`${API_BASE}/backtest/jobs/${jobId}/result`, { cache: 'no-store' });
  if (!res.ok) throw new Error("Failed to fetch backtest result");
  return res.json();
}
