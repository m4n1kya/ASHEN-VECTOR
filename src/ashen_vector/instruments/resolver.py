"""
Instrument resolution and mapping.
Provides mapping from Qlib raw symbols to rich Instrument objects.
"""
from typing import List, Optional
from ashen_vector.instruments.schemas import Instrument
from ashen_vector.data.instrument_service import InstrumentService
from ashen_vector.core.exceptions import InstrumentNotFoundError

# Placeholder for a future database mapping or external API
# For Phase 4, we infer metadata from the symbol if possible,
# and fallback to generic names so we don't fabricate false companies.
_HARDCODED_METADATA = {
    "SH600000": {"name": "Shanghai Pudong Development Bank Co.", "exchange": "SSE", "asset_type": "equity"},
    # Extendible for other known instruments
}

class InstrumentResolver:
    """Resolves search queries to canonical Instrument objects."""
    
    def __init__(self, service: InstrumentService):
        self.service = service
        self._cache_all_instruments = None
        
    def _build_instrument(self, symbol: str) -> Instrument:
        """Constructs a rich Instrument object for a given valid symbol."""
        if symbol in _HARDCODED_METADATA:
            meta = _HARDCODED_METADATA[symbol]
            return Instrument(
                symbol=symbol,
                name=meta["name"],
                exchange=meta["exchange"],
                asset_type=meta["asset_type"]
            )
            
        # Infer exchange from prefix if it matches Qlib convention (e.g. SH, SZ)
        exchange = "UNKNOWN"
        if symbol.startswith("SH"):
            exchange = "SSE"
        elif symbol.startswith("SZ"):
            exchange = "SZSE"
            
        return Instrument(
            symbol=symbol,
            name=symbol,  # Do not fabricate false names
            exchange=exchange,
            asset_type="equity"
        )
        
    def resolve_exact(self, symbol: str) -> Instrument:
        """Resolve an exact symbol, throwing an error if missing."""
        validated = self.service.validate_symbol(symbol)
        return self._build_instrument(validated)
        
    def search(self, query: str) -> List[Instrument]:
        """Search instruments using prefix or partial match, returning rich objects."""
        # Check against hardcoded metadata (e.g. search by name)
        normalized_query = query.strip().upper()
        results = set()
        
        # 1. Search in Qlib via service
        raw_matches = self.service.search_instruments(query)
        for sym in raw_matches:
            results.add(sym)
            
        # 2. Search in metadata dictionary values
        for sym, meta in _HARDCODED_METADATA.items():
            if normalized_query in meta["name"].upper() or normalized_query in sym:
                # Ensure it actually exists in Qlib dataset before returning
                try:
                    self.service.validate_symbol(sym)
                    results.add(sym)
                except InstrumentNotFoundError:
                    pass
                    
        return [self._build_instrument(sym) for sym in sorted(results)]
