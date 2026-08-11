"""ASHEN-VECTOR Data Inspector.

Inspects the configured Qlib dataset and reports:
- Number of available instruments
- Date coverage
- Available data fields
- Sample instruments
- Verification of specific symbols

Usage:
    python scripts/inspect_data.py
    python scripts/inspect_data.py --symbol SH600000
"""

import argparse
import sys
from pathlib import Path

# Add src to path for direct script execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect the ASHEN-VECTOR Qlib dataset."
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default=None,
        help="Verify a specific instrument symbol (e.g., SH600000).",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=10,
        help="Number of sample instruments to display.",
    )
    args = parser.parse_args()

    print("=" * 64)
    print("  ASHEN-VECTOR — Data Inspector")
    print("=" * 64)
    print()

    # Load settings
    from ashen_vector.config.settings import get_settings

    settings = get_settings()
    resolved_uri = settings.resolved_qlib_uri

    print(f"  Provider URI (config) : {settings.qlib_provider_uri}")
    print(f"  Provider URI (resolved): {resolved_uri}")
    print(f"  Region               : {settings.qlib_region}")
    print()

    # Check if path exists
    if not resolved_uri.exists():
        print(f"  ERROR: Provider path does not exist: {resolved_uri}")
        sys.exit(1)

    # Initialize Qlib
    from ashen_vector.data.qlib_provider import get_provider

    provider = get_provider()
    try:
        provider.initialize()
        print("  Qlib Status          : INITIALIZED")
    except Exception as e:
        print(f"  Qlib Status          : FAILED ({e})")
        sys.exit(1)
    print()

    # Discover instruments
    print("-" * 64)
    print("  INSTRUMENTS")
    print("-" * 64)

    instruments = provider.get_available_instruments()
    print(f"  Total instruments    : {len(instruments)}")
    print()

    if instruments:
        sample = sorted(instruments)[: args.sample]
        print(f"  Sample ({min(args.sample, len(instruments))}):")
        for inst in sample:
            print(f"    - {inst}")
        print()

    # Check features directory structure
    features_dir = resolved_uri / "features"
    if features_dir.exists():
        # Check what fields are available for a sample instrument
        sample_instruments = sorted(instruments)[:1] if instruments else []
        if sample_instruments:
            inst_dir = features_dir / sample_instruments[0]
            if inst_dir.exists():
                bin_files = list(inst_dir.glob("*.bin"))
                fields = sorted(set(f.stem.rsplit(".", 1)[0] for f in bin_files))
                print("-" * 64)
                print("  AVAILABLE FIELDS")
                print("-" * 64)
                print(f"  Sample instrument: {sample_instruments[0]}")
                print(f"  Field count      : {len(fields)}")
                for field in fields:
                    print(f"    - {field}")
                print()

    # Calendars
    calendars_dir = resolved_uri / "calendars"
    if calendars_dir.exists():
        cal_files = list(calendars_dir.glob("*"))
        print("-" * 64)
        print("  CALENDARS")
        print("-" * 64)
        for cal in sorted(cal_files):
            print(f"    - {cal.name}")
            # Try to read first and last lines to show date range
            try:
                with open(cal, "r") as f:
                    lines = f.readlines()
                if lines:
                    first = lines[0].strip()
                    last = lines[-1].strip()
                    print(f"      Range: {first} → {last}")
                    print(f"      Trading days: {len(lines)}")
            except Exception:
                pass
        print()

    # Verify specific symbol
    if args.symbol:
        print("-" * 64)
        print(f"  SYMBOL VERIFICATION: {args.symbol}")
        print("-" * 64)

        exists = provider.instrument_exists(args.symbol)
        print(f"  Exists: {exists}")

        if exists:
            try:
                import qlib
                from qlib.data import D

                df = D.features(
                    [args.symbol],
                    ["$open", "$high", "$low", "$close", "$volume"],
                    start_time="1990-01-01",
                    end_time="2030-12-31",
                )

                if df is not None and not df.empty:
                    # Extract date range from index
                    dates = df.index.get_level_values(1) if df.index.nlevels > 1 else df.index
                    print(f"  Data start : {dates.min().date()}")
                    print(f"  Data end   : {dates.max().date()}")
                    print(f"  Total bars : {len(df)}")
                    print()
                    print("  Latest 5 bars:")
                    print(df.tail(5).to_string())
                else:
                    print("  No data returned.")
            except Exception as e:
                print(f"  Error fetching data: {e}")
        print()

    print("=" * 64)
    print("  Inspection complete.")
    print("=" * 64)


if __name__ == "__main__":
    main()
