// Waypoint Math engine - coordinate format and distance honesty.
// Mirrored float-for-float by oracle.py; keep the op order identical.

function _fmt6(x) {
  var micro = Math.floor(Math.abs(x) * 1000000 + 0.5);
  var s = (x < 0 && micro !== 0) ? "-" : "";
  var whole = Math.floor(micro / 1000000);
  var frac = micro - whole * 1000000;
  var f = String(frac);
  while (f.length < 6) f = "0" + f;
  return s + whole + "." + f;
}

function _fixed1(x) {
  var t = Math.floor(x * 10 + 0.5);
  return Math.floor(t / 10) + "." + (t % 10);
}

function _rad(d) { return d * Math.PI / 180; }

function _havKm(lat1, lon1, lat2, lon2) {
  var R = 6371;
  var p1 = _rad(lat1), p2 = _rad(lat2);
  var dp = _rad(lat2 - lat1), dl = _rad(lon2 - lon1);
  var sd = Math.sin(dp / 2), sl = Math.sin(dl / 2);
  var a = sd * sd + Math.cos(p1) * Math.cos(p2) * sl * sl;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// The minutes truth: degrees + decimal minutes to decimal degrees,
// plus the distance cost of the classic misread (minutes as decimal).
function minutesTruth(deg, min) {
  if (!isFinite(deg) || deg < -180 || deg > 180) throw new Error("degrees must be between -180 and 180");
  if (!isFinite(min) || min < 0 || min >= 60) throw new Error("minutes must be under 60");
  var s = deg < 0 ? -1 : 1;
  var dec = s * (Math.abs(deg) + min / 60);
  var degWord = Math.abs(deg) === 1 ? "degree" : "degrees";
  var minWord = min === 1 ? "minute" : "minutes";
  if (min === 0) {
    return deg + " " + degWord + " 0 minutes is exactly " + _fmt6(dec) +
      " in decimal - nothing to convert.";
  }
  var naive = s * (Math.abs(deg) + min / 100);
  var errKm = _havKm(dec, 0, naive, 0);
  return deg + " " + degWord + " " + min + " " + minWord + " is " + _fmt6(dec) +
    " in decimal - the minutes divide by 60, not 100; misread them and the pin lands at " +
    _fmt6(naive) + ", about " + _fixed1(errKm) + " km off.";
}

// The seconds truth: degrees, minutes, seconds to decimal degrees.
function secondsTruth(deg, min, sec) {
  if (!isFinite(deg) || deg < -180 || deg > 180) throw new Error("degrees must be between -180 and 180");
  if (!isFinite(min) || min < 0 || min >= 60) throw new Error("minutes must be under 60");
  if (!isFinite(sec) || sec < 0 || sec >= 60) throw new Error("seconds must be under 60");
  var s = deg < 0 ? -1 : 1;
  var dec = s * (Math.abs(deg) + min / 60 + sec / 3600);
  var degWord = Math.abs(deg) === 1 ? "degree" : "degrees";
  var minWord = min === 1 ? "minute" : "minutes";
  var secWord = sec === 1 ? "second" : "seconds";
  return deg + " " + degWord + " " + min + " " + minWord + " " + sec + " " + secWord +
    " is " + _fmt6(dec) + " in decimal degrees.";
}

// The distance truth: straight-line (great-circle) distance between two waypoints.
function distanceTruth(lat1, lon1, lat2, lon2) {
  if (!isFinite(lat1) || lat1 < -90 || lat1 > 90 || !isFinite(lat2) || lat2 < -90 || lat2 > 90) {
    throw new Error("latitude must be between -90 and 90");
  }
  if (!isFinite(lon1) || lon1 < -180 || lon1 > 180 || !isFinite(lon2) || lon2 < -180 || lon2 > 180) {
    throw new Error("longitude must be between -180 and 180");
  }
  var dKm = _havKm(lat1, lon1, lat2, lon2);
  var dMi = dKm * 0.621371;
  return "The straight line from (" + lat1 + ", " + lon1 + ") to (" + lat2 + ", " + lon2 + ") is " +
    _fixed1(dKm) + " km - " + _fixed1(dMi) + " miles as the crow flies, longer on foot.";
}
