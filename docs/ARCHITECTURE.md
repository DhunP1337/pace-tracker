# Architecture

## Data model
GTFS is a set of CSVs that join like DB tables:
stops -> stop_times -> trips -> routes, filtered by calendar + calendar_dates.
Loaded into SQLite once by scripts/load_gtfs.py. All columns TEXT; casting happens in query code.

## Key finding
Campus is served by exactly ONE route: 208 (Golf Road), east and west.
Three stops: 220s0345 (campus), 220s0350 (southbound), 220n0248 (northbound).
This constrains product scope. Options: narrow departure board, or general
Pace app with campus as default view.

## Constraints
- Schedule data only, NOT real-time. Pace runs Trapeze TransitMaster; no public realtime feed.
- GTFS times exceed 24:00:00 for after-midnight service. Parse as seconds since midnight.
- calendar_dates.txt overrides calendar.txt for holidays.
- Timezone is America/Chicago with DST. Use zoneinfo.
