# Waypoint Math

GPS coordinate honesty. The minutes divide by 60, not 100 - and the difference is a 20-kilometer walk. Waypoint Math converts the three ways people write coordinates and measures the straight line between two pins.

## What it computes

- **The minutes truth** - degrees and decimal minutes (the geocache listing format) to decimal degrees, plus the distance cost of the classic misread (minutes treated as a decimal fraction).
- **The seconds truth** - degrees, minutes, seconds to decimal degrees.
- **The distance truth** - straight-line (great-circle) distance between two decimal-degree waypoints, in kilometers and miles.

## Boundary

Format and distance arithmetic only. Waypoint Math never judges a route, a trail, or a destination - straight lines ignore cliffs, rivers, and fences.

## Files

- `index.html` - landing page with the honesty pitch and the boundary.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic, shared by the app and the tests.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (13 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/waypointmath/
Repo: https://github.com/iLanis-agent/waypointmath
