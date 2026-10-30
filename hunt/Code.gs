/**
 * Three Village Local Scavenger Hunt - back end (Google Apps Script web app, bound to the "3VL Scavenger Hunt" Google Sheet).
 * Built 10/30/2026. Owner rules: 1 point per check-in, each QR counts once per player per day (Eastern time),
 * as many different QRs per day as you can find; must be near the QR (phone location); players verify their email once.
 *
 * Sheet tabs (created by setup()):
 *   Codes    code | name | type (store/sticker) | lat | lng | radius_m | active | points | notes
 *   Players  id | first | last | email | phone | created | verified | token | status | notes
 *   Scans    time | date_et | player_id | player | code | place | result | points | dist_m | acc_m | lat | lng | flag | user_agent
 *   Pending  email | first | last | phone | code_hash | expires | tries | sent
 * Script properties: ADMIN_KEY (for the "set this spot" links), SECRET (random, set by setup()).
 * Deploy: Deploy > New deployment > Web app, Execute as: Me, Who has access: Anyone.
 */
var TZ = 'America/New_York';
var DEFAULT_RADIUS = 150;        // meters (~ a block)
var MAX_ACC = 250;               // reject a location fix worse than this (meters)
var CODE_TTL_MIN = 20;           // email code lifetime
var FROM_NAME = 'Three Village Local';

function setup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var tabs = {
    Codes: ['code', 'name', 'type', 'lat', 'lng', 'radius_m', 'active', 'points', 'notes'],
    Players: ['id', 'first', 'last', 'email', 'phone', 'created', 'verified', 'token', 'status', 'notes'],
    Scans: ['time', 'date_et', 'player_id', 'player', 'code', 'place', 'result', 'points', 'dist_m', 'acc_m', 'lat', 'lng', 'flag', 'user_agent'],
    Pending: ['email', 'first', 'last', 'phone', 'code_hash', 'expires', 'tries', 'sent'],
    'Sign Requests': ['time', 'business', 'contact', 'email', 'phone', 'address', 'notes', 'status']
  };
  Object.keys(tabs).forEach(function (n) {
    var sh = ss.getSheetByName(n) || ss.insertSheet(n);
    if (sh.getLastRow() === 0) { sh.appendRow(tabs[n]); sh.setFrozenRows(1); sh.getRange(1, 1, 1, tabs[n].length).setFontWeight('bold'); }
  });
  var p = PropertiesService.getScriptProperties();
  if (!p.getProperty('SECRET')) p.setProperty('SECRET', Utilities.getUuid() + Utilities.getUuid());
  if (!p.getProperty('ADMIN_KEY')) p.setProperty('ADMIN_KEY', Utilities.getUuid().replace(/-/g, '').slice(0, 16));
  var d = ss.getSheetByName('Sheet1'); if (d && d.getLastRow() === 0 && ss.getSheets().length > 1) ss.deleteSheet(d);
  Logger.log('ADMIN_KEY = ' + p.getProperty('ADMIN_KEY'));
}

function doGet(e) { return handle_(e && e.parameter ? e.parameter : {}); }
function doPost(e) {
  var b = {};
  try { b = JSON.parse(e.postData.contents || '{}'); } catch (x) { b = {}; }
  return handle_(b);
}

function handle_(b) {
  var out;
  try {
    var a = String(b.action || '');
    if (a === 'code') out = codeInfo_(b);
    else if (a === 'start') out = start_(b);
    else if (a === 'verify') out = verify_(b);
    else if (a === 'checkin') out = checkin_(b);
    else if (a === 'me') out = me_(b);
    else if (a === 'board') out = board_();
    else if (a === 'setloc') out = setloc_(b);
    else if (a === 'request') out = request_(b);
    else if (a === 'addcode') out = addcode_(b);
    else out = { ok: false, error: 'unknown' };
  } catch (err) {
    out = { ok: false, error: 'server', detail: String(err && err.message || err) };
  }
  return ContentService.createTextOutput(JSON.stringify(out)).setMimeType(ContentService.MimeType.JSON);
}

// ---------- helpers ----------
function sh_(n) { return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(n); }
function rows_(n) { var v = sh_(n).getDataRange().getValues(); var h = v.shift(); return { h: h, v: v }; }
function obj_(h, r) { var o = {}; h.forEach(function (k, i) { o[k] = r[i]; }); return o; }
function today_() { return Utilities.formatDate(new Date(), TZ, 'yyyy-MM-dd'); }
function clean_(s, n) { return String(s == null ? '' : s).replace(/[<>]/g, '').trim().slice(0, n || 80); }
function normEmail_(s) { return String(s || '').trim().toLowerCase(); }
function hash_(s) {
  var d = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, s + '|' + PropertiesService.getScriptProperties().getProperty('SECRET'));
  return d.map(function (b) { return ('0' + (b & 255).toString(16)).slice(-2); }).join('');
}
function dist_(a1, o1, a2, o2) {
  var R = 6371000, t = Math.PI / 180, dA = (a2 - a1) * t, dO = (o2 - o1) * t;
  var x = Math.sin(dA / 2) * Math.sin(dA / 2) + Math.cos(a1 * t) * Math.cos(a2 * t) * Math.sin(dO / 2) * Math.sin(dO / 2);
  return Math.round(2 * R * Math.asin(Math.sqrt(x)));
}
function findCode_(code) {
  code = String(code || '').trim().toLowerCase();
  var r = rows_('Codes');
  for (var i = 0; i < r.v.length; i++) if (String(r.v[i][0]).trim().toLowerCase() === code) return { row: i + 2, c: obj_(r.h, r.v[i]) };
  return null;
}
function playerByToken_(tok) {
  tok = String(tok || '');
  if (tok.length < 20) return null;
  var r = rows_('Players');
  var ti = r.h.indexOf('token');
  for (var i = 0; i < r.v.length; i++) if (String(r.v[i][ti]) === tok) return { row: i + 2, p: obj_(r.h, r.v[i]) };
  return null;
}
function initials_(p) { return clean_(p.first, 30) + ' ' + (clean_(p.last, 30).charAt(0) ? clean_(p.last, 30).charAt(0).toUpperCase() + '.' : ''); }
function totals_() {   // player_id -> points (counted check-ins only)
  var r = rows_('Scans'), t = {}, pi = r.h.indexOf('player_id'), ri = r.h.indexOf('result'), pt = r.h.indexOf('points');
  r.v.forEach(function (x) { if (x[ri] === 'ok') t[x[pi]] = (t[x[pi]] || 0) + (Number(x[pt]) || 1); });
  return t;
}
function active_(c) { return c.active === true || String(c.active).toUpperCase() === 'TRUE' || String(c.active).toLowerCase() === 'yes'; }

// Bonus days (owner 10/30/2026): tab "Bonus" = date (yyyy-mm-dd, Eastern) | code ("all" = every code) | points | note
// e.g. 2026-11-07 | olde-towne-gardens | 3 | Triple points today!  -> a check-in there that day scores 3.
function bonus_(code, day) {
  var ss = SpreadsheetApp.getActiveSpreadsheet(), sh = ss.getSheetByName('Bonus');
  if (!sh) { sh = ss.insertSheet('Bonus'); sh.appendRow(['date', 'code', 'points', 'note']); sh.setFrozenRows(1); sh.getRange(1, 1, 1, 4).setFontWeight('bold'); return null; }
  var v = sh.getDataRange().getValues(); v.shift();
  code = String(code).toLowerCase();
  var best = null;
  v.forEach(function (r) {
    var d = r[0] instanceof Date ? Utilities.formatDate(r[0], TZ, 'yyyy-MM-dd') : String(r[0]).trim();
    var c = String(r[1]).trim().toLowerCase(), p = Number(r[2]);
    if (d === day && (c === code || c === 'all') && p > 0 && (!best || p > best.points)) best = { points: p, note: String(r[3] || '') };
  });
  return best;
}

// ---------- actions ----------
function codeInfo_(b) {
  var f = findCode_(b.code);
  if (!f || !active_(f.c)) return { ok: false, error: 'nocode' };
  var bon = bonus_(f.c.code, today_());
  return { ok: true, code: f.c.code, name: f.c.name, type: f.c.type, located: f.c.lat !== '' && f.c.lng !== '', bonus: bon ? bon.points : 0, bonusNote: bon ? bon.note : '' };
}

function start_(b) {
  var email = normEmail_(b.email);
  if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(email)) return { ok: false, error: 'email' };
  var first = clean_(b.first, 40), last = clean_(b.last, 40), phone = clean_(b.phone, 20).replace(/[^0-9+]/g, '');
  if (!first || !last) return { ok: false, error: 'name' };
  if (phone.replace(/\D/g, '').length < 10) return { ok: false, error: 'phone' };
  var lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    var sh = sh_('Pending'), r = rows_('Pending'), row = 0;
    for (var i = 0; i < r.v.length; i++) if (r.v[i][0] === email) { row = i + 2; break; }
    if (row) {
      var sent = new Date(r.v[row - 2][7]);
      if (new Date() - sent < 45 * 1000) return { ok: false, error: 'wait' };     // resend throttle
    }
    var code = String(Math.floor(100000 + Math.random() * 900000));
    var vals = [email, first, last, phone, hash_(email + code), new Date(Date.now() + CODE_TTL_MIN * 60000), 0, new Date()];
    if (row) sh.getRange(row, 1, 1, vals.length).setValues([vals]); else sh.appendRow(vals);
    MailApp.sendEmail({
      to: email, name: FROM_NAME,
      subject: code + ' is your Three Village Local Scavenger Hunt code',
      htmlBody: '<div style="font-family:Arial,sans-serif;max-width:480px;color:#0f2a4f">' +
        '<p style="font-size:16px">Hi ' + first + ',</p><p style="font-size:16px">Your code for the Three Village Local Scavenger Hunt is:</p>' +
        '<p style="font-size:34px;font-weight:bold;letter-spacing:6px;margin:10px 0;color:#1d5fbf">' + code + '</p>' +
        '<p style="font-size:14px;color:#3c4a5e">Type it on the check-in page. It works for ' + CODE_TTL_MIN + ' minutes. You only have to do this once on your phone.</p>' +
        '<p style="font-size:14px;color:#3c4a5e">Happy hunting!<br>Three Village Local</p></div>'
    });
  } finally { lock.releaseLock(); }
  return { ok: true };
}

function verify_(b) {
  var email = normEmail_(b.email), code = String(b.otp || '').replace(/\D/g, '');
  var lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    var sh = sh_('Pending'), r = rows_('Pending'), row = 0, p;
    for (var i = 0; i < r.v.length; i++) if (r.v[i][0] === email) { row = i + 2; p = obj_(r.h, r.v[i]); break; }
    if (!row) return { ok: false, error: 'nopending' };
    if (Number(p.tries) >= 6) return { ok: false, error: 'tries' };
    if (new Date() > new Date(p.expires)) return { ok: false, error: 'expired' };
    if (hash_(email + code) !== p.code_hash) { sh.getRange(row, 7).setValue(Number(p.tries) + 1); return { ok: false, error: 'badcode' }; }
    sh.deleteRow(row);
    // one player per email: reuse the existing player (new phone = new token, old devices keep working too? no: one token)
    var pr = rows_('Players'), ps = sh_('Players'), ei = pr.h.indexOf('email'), found = 0;
    for (var j = 0; j < pr.v.length; j++) if (String(pr.v[j][ei]).toLowerCase() === email) { found = j + 2; break; }
    var tok = Utilities.getUuid().replace(/-/g, '') + Utilities.getUuid().replace(/-/g, '');
    var pid;
    if (found) {
      pid = pr.v[found - 2][0];
      ps.getRange(found, 2, 1, 4).setValues([[p.first, p.last, email, p.phone]]);
      ps.getRange(found, 7, 1, 2).setValues([[new Date(), tok]]);
    } else {
      pid = 'P' + String(pr.v.length + 1001);
      ps.appendRow([pid, p.first, p.last, email, "'" + p.phone, new Date(), new Date(), tok, 'active', '']);
    }
    return { ok: true, token: tok, player: { id: pid, first: p.first, last: p.last } };
  } finally { lock.releaseLock(); }
}

function checkin_(b) {
  var pl = playerByToken_(b.token);
  if (!pl) return { ok: false, error: 'signin' };
  if (String(pl.p.status).toLowerCase() === 'blocked') return { ok: false, error: 'blocked' };
  var f = findCode_(b.code);
  if (!f || !active_(f.c)) return { ok: false, error: 'nocode' };
  var c = f.c, lat = Number(b.lat), lng = Number(b.lng), acc = Math.round(Number(b.acc) || 9999);
  var today = today_(), name = initials_(pl.p), ua = clean_(b.ua, 160);
  var lock = LockService.getScriptLock(); lock.waitLock(25000);
  try {
    var s = sh_('Scans');
    function log(result, pts, d, flag) {
      s.appendRow([new Date(), today, pl.p.id, pl.p.first + ' ' + pl.p.last, c.code, c.name, result, pts, d === null ? '' : d, isFinite(acc) ? acc : '', isFinite(lat) ? lat : '', isFinite(lng) ? lng : '', flag || '', ua]);
    }
    // already checked in here today? (checked BEFORE location so a repeat scan never re-counts)
    var r = rows_('Scans'), pi = r.h.indexOf('player_id'), ci = r.h.indexOf('code'), di = r.h.indexOf('date_et'), ri = r.h.indexOf('result'), ti = r.h.indexOf('time');
    var recent = 0;
    for (var i = r.v.length - 1; i >= 0; i--) {
      var x = r.v[i];
      if (x[pi] !== pl.p.id) continue;
      if (x[ri] === 'ok' && String(x[ci]).toLowerCase() === String(c.code).toLowerCase() && (x[di] instanceof Date ? Utilities.formatDate(x[di], TZ, 'yyyy-MM-dd') : String(x[di])) === today)
        return Object.assign({ ok: false, error: 'already', place: c.name }, mine_(pl.p.id));
      if (x[ri] === 'ok' && new Date() - new Date(x[ti]) < 10 * 60000) recent++;
    }
    if (!isFinite(lat) || !isFinite(lng)) { log('no_location', 0, null); return { ok: false, error: 'location' }; }
    if (acc > MAX_ACC) { log('weak_gps', 0, null); return { ok: false, error: 'weakgps', acc: acc }; }
    if (c.lat === '' || c.lng === '') { log('code_not_placed', 0, null); return { ok: false, error: 'notplaced' }; }
    var d = dist_(Number(c.lat), Number(c.lng), lat, lng), rad = Number(c.radius_m) || DEFAULT_RADIUS;
    if (d > rad + Math.min(acc, 100)) { log('too_far', 0, d); return { ok: false, error: 'far', dist: d }; }
    var bon = bonus_(c.code, today), pts = bon ? bon.points : (Number(c.points) || 1);
    log('ok', pts, d, recent >= 6 ? 'fast: ' + (recent + 1) + ' check-ins in 10 min' : '');
    return Object.assign({ ok: true, place: c.name, points: pts, bonus: bon ? bon.note || '' : '' }, mine_(pl.p.id));
  } finally { lock.releaseLock(); }
}

function mine_(pid) {
  var r = rows_('Scans'), pi = r.h.indexOf('player_id'), ri = r.h.indexOf('result'), pt = r.h.indexOf('points'), di = r.h.indexOf('date_et'), pl = r.h.indexOf('place');
  var total = 0, todayN = 0, places = {}, today = today_(), list = [];
  r.v.forEach(function (x) {
    if (x[pi] !== pid || x[ri] !== 'ok') return;
    total += Number(x[pt]) || 1;
    var dd = x[di] instanceof Date ? Utilities.formatDate(x[di], TZ, 'yyyy-MM-dd') : String(x[di]);
    if (dd === today) { todayN++; list.push(x[pl]); }
    places[x[pl]] = 1;
  });
  return { total: total, today: todayN, todayPlaces: list, spots: Object.keys(places).length };
}

function me_(b) {
  var pl = playerByToken_(b.token);
  if (!pl) return { ok: false, error: 'signin' };
  return Object.assign({ ok: true, player: { first: pl.p.first, last: pl.p.last } }, mine_(pl.p.id));
}

function board_() {
  var cache = CacheService.getScriptCache(), hit = cache.get('board');
  if (hit) return JSON.parse(hit);
  var t = totals_(), r = rows_('Players'), names = {};
  r.v.forEach(function (x) { var p = obj_(r.h, x); if (String(p.status).toLowerCase() !== 'blocked') names[p.id] = initials_(p); });
  var list = Object.keys(t).filter(function (k) { return names[k]; }).map(function (k) { return { n: names[k], p: t[k] }; })
    .sort(function (a, b) { return b.p - a.p; }).slice(0, 25);
  var out = { ok: true, board: list, players: Object.keys(names).length, updated: Utilities.formatDate(new Date(), TZ, 'MMM d, h:mm a') };
  cache.put('board', JSON.stringify(out), 60);
  return out;
}

function request_(b) {   // a local business asks for a hunt sign -> "Sign Requests" tab + email to the owner
  var biz = clean_(b.business, 80), who = clean_(b.contact, 60), email = normEmail_(b.email), phone = clean_(b.phone, 20), addr = clean_(b.address, 120), notes = clean_(b.notes, 400);
  if (!biz || !who) return { ok: false, error: 'name' };
  if (!/^[^@\s]+@[^@\s]+\.[a-z]{2,}$/i.test(email)) return { ok: false, error: 'email' };
  if (String(b.hp || '')) return { ok: true };   // bot honeypot
  var c = CacheService.getScriptCache(), k = 'rq_' + email;
  if (c.get(k)) return { ok: true };
  c.put(k, '1', 600);
  sh_('Sign Requests').appendRow([new Date(), biz, who, email, "'" + phone, addr, notes, 'new']);
  MailApp.sendEmail({ to: 'threevillagelocal@gmail.com', name: FROM_NAME, replyTo: email,
    subject: '[Scavenger Hunt] Sign request: ' + biz,
    htmlBody: '<p><b>' + biz + '</b> wants a scavenger hunt sign.</p><p>Contact: ' + who + '<br>Email: ' + email + '<br>Phone: ' + phone + '<br>Address: ' + addr + '</p><p>' + notes + '</p><p>Reply to this email to answer them. It is also in the "Sign Requests" tab of the 3VL Scavenger Hunt sheet.</p>' });
  return { ok: true };
}

function addcode_(b) {   // staff/sign builder: add or update a code row (needs ADMIN_KEY). Never moves an existing saved spot unless lat/lng are sent.
  if (String(b.key || '') !== PropertiesService.getScriptProperties().getProperty('ADMIN_KEY')) return { ok: false, error: 'key' };
  var code = String(b.code || '').trim().toLowerCase();
  if (!/^[a-z0-9-]{3,60}$/.test(code)) return { ok: false, error: 'code' };
  var f = findCode_(code), sh = sh_('Codes');
  var lat = b.lat === undefined || b.lat === '' ? null : Number(b.lat), lng = b.lng === undefined || b.lng === '' ? null : Number(b.lng);
  if (f) {
    sh.getRange(f.row, 2, 1, 2).setValues([[clean_(b.name, 80) || f.c.name, clean_(b.type, 20) || f.c.type]]);
    if (lat !== null && lng !== null) sh.getRange(f.row, 4, 1, 2).setValues([[lat, lng]]);
    return { ok: true, updated: code };
  }
  sh.appendRow([code, clean_(b.name, 80), clean_(b.type, 20) || 'store', lat === null ? '' : lat, lng === null ? '' : lng, Number(b.radius_m) || DEFAULT_RADIUS, true, Number(b.points) || 1, clean_(b.notes, 200)]);
  return { ok: true, added: code };
}

function setloc_(b) {   // owner/staff: stand at the sign or sticker, open /hunt/<code>?place=<ADMIN_KEY>, tap "Save this spot"
  if (String(b.key || '') !== PropertiesService.getScriptProperties().getProperty('ADMIN_KEY')) return { ok: false, error: 'key' };
  var f = findCode_(b.code);
  if (!f) return { ok: false, error: 'nocode' };
  var lat = Number(b.lat), lng = Number(b.lng), acc = Math.round(Number(b.acc) || 9999);
  if (!isFinite(lat) || !isFinite(lng)) return { ok: false, error: 'location' };
  if (acc > 120) return { ok: false, error: 'weakgps', acc: acc };
  var r = rows_('Codes'), li = r.h.indexOf('lat') + 1;
  sh_('Codes').getRange(f.row, li, 1, 2).setValues([[lat, lng]]);
  return { ok: true, code: f.c.code, name: f.c.name, acc: acc };
}
