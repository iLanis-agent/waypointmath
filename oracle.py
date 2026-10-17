#!/usr/bin/env python3
# Waypoint Math oracle - mirrors engine.js float-for-float.
import json, math

def _fmt6(x):
    micro = math.floor(abs(x) * 1000000 + 0.5)
    s = "-" if (x < 0 and micro != 0) else ""
    whole = micro // 1000000
    frac = micro - whole * 1000000
    return f"{s}{whole}.{frac:06d}"

def _fixed1(x):
    t = math.floor(x * 10 + 0.5)
    return f"{t // 10}.{t % 10}"

def _rad(d):
    return d * math.pi / 180

def _hav_km(lat1, lon1, lat2, lon2):
    R = 6371
    p1, p2 = _rad(lat1), _rad(lat2)
    dp, dl = _rad(lat2 - lat1), _rad(lon2 - lon1)
    sd, sl = math.sin(dp / 2), math.sin(dl / 2)
    a = sd * sd + math.cos(p1) * math.cos(p2) * sl * sl
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def minutes_truth(deg, m):
    if not math.isfinite(deg) or deg < -180 or deg > 180:
        raise ValueError("degrees must be between -180 and 180")
    if not math.isfinite(m) or m < 0 or m >= 60:
        raise ValueError("minutes must be under 60")
    s = -1 if deg < 0 else 1
    dec = s * (abs(deg) + m / 60)
    deg_word = "degree" if abs(deg) == 1 else "degrees"
    min_word = "minute" if m == 1 else "minutes"
    if m == 0:
        return f"{deg} {deg_word} 0 minutes is exactly {_fmt6(dec)} in decimal - nothing to convert."
    naive = s * (abs(deg) + m / 100)
    err_km = _hav_km(dec, 0, naive, 0)
    return (f"{deg} {deg_word} {m} {min_word} is {_fmt6(dec)} in decimal - the minutes divide by 60, "
            f"not 100; misread them and the pin lands at {_fmt6(naive)}, about {_fixed1(err_km)} km off.")

def seconds_truth(deg, m, sec):
    if not math.isfinite(deg) or deg < -180 or deg > 180:
        raise ValueError("degrees must be between -180 and 180")
    if not math.isfinite(m) or m < 0 or m >= 60:
        raise ValueError("minutes must be under 60")
    if not math.isfinite(sec) or sec < 0 or sec >= 60:
        raise ValueError("seconds must be under 60")
    s = -1 if deg < 0 else 1
    dec = s * (abs(deg) + m / 60 + sec / 3600)
    deg_word = "degree" if abs(deg) == 1 else "degrees"
    min_word = "minute" if m == 1 else "minutes"
    sec_word = "second" if sec == 1 else "seconds"
    return f"{deg} {deg_word} {m} {min_word} {sec} {sec_word} is {_fmt6(dec)} in decimal degrees."

def distance_truth(lat1, lon1, lat2, lon2):
    if (not math.isfinite(lat1) or lat1 < -90 or lat1 > 90
            or not math.isfinite(lat2) or lat2 < -90 or lat2 > 90):
        raise ValueError("latitude must be between -90 and 90")
    if (not math.isfinite(lon1) or lon1 < -180 or lon1 > 180
            or not math.isfinite(lon2) or lon2 < -180 or lon2 > 180):
        raise ValueError("longitude must be between -180 and 180")
    d_km = _hav_km(lat1, lon1, lat2, lon2)
    d_mi = d_km * 0.621371
    return (f"The straight line from ({lat1}, {lon1}) to ({lat2}, {lon2}) is {_fixed1(d_km)} km - "
            f"{_fixed1(d_mi)} miles as the crow flies, longer on foot.")

CASES = [
    ("minutesTruth", (40, 26.767)),
    ("minutesTruth", (0, 45)),
    ("minutesTruth", (1, 30)),
    ("minutesTruth", (-33, 51.5)),
    ("minutesTruth", (40, 0)),
    ("minutesTruth", (40, 60)),
    ("minutesTruth", (181, 0)),
    ("secondsTruth", (40, 26, 46)),
    ("secondsTruth", (-73, 59, 7)),
    ("secondsTruth", (40, 26, 60)),
    ("distanceTruth", (32.08, 34.78, 31.25, 34.39)),
    ("distanceTruth", (40.446117, 0, 40.26767, 0)),
    ("distanceTruth", (91, 0, 0, 0)),
]

FNS = {"minutesTruth": minutes_truth, "secondsTruth": seconds_truth, "distanceTruth": distance_truth}

out = []
for name, args in CASES:
    try:
        expected = FNS[name](*args)
    except ValueError as e:
        expected = "ERR:" + str(e)
    out.append({"fn": name, "args": list(args), "expected": expected})

with open("expected.json", "w") as f:
    f.write(json.dumps(out, indent=2) + "\n")
print(f"{len(out)} cases written")
