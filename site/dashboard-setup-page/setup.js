/* Company Digital Dashboards setup wizard. Data in window.TDS_CFG (build.py). NO BACKSLASHES in this file: BD strips them. */
(function () {
  var C = window.TDS_CFG, R = document.getElementById('tds');
  if (!C || !R || R.getAttribute('data-on')) return;
  R.setAttribute('data-on', '1');
  var NL = String.fromCharCode(10), CR = String.fromCharCode(13), KEY = 'tds_setup_v1', CL = 'dashboard-setup', UNS = 'Not sure, help me decide';
  var MAXUP = 30, FILES = {}, saveT = 0, prevT = 0;

  // ---------- helpers ----------
  function esc(s) { return String(s == null ? '' : s).split('&').join('&amp;').split('<').join('&lt;').split('>').join('&gt;').split('"').join('&quot;'); }
  function nw(s) {   // hyphenated words never split across lines (412/360/320 rule)
    return esc(s).split(' ').map(function (w) { return w.indexOf('-') > 0 && w.length < 30 ? '<span class="nw">' + w + '</span>' : w; }).join(' ');
  }
  function nwh(h) {   // same for trusted HTML text (keeps tags and entities)
    return String(h).split(' ').map(function (w) { return w.indexOf('-') > 0 && w.indexOf('<') < 0 && w.indexOf('=') < 0 && w.length < 30 ? '<span class="nw">' + w + '</span>' : w; }).join(' ');
  }
  function ic(n) { return C.ic[n] || ''; }
  function byId(id) { return document.getElementById(id); }
  function rid(n) {
    var a = 'abcdefghijklmnopqrstuvwxyz0123456789', s = '', r = null;
    try { r = new Uint8Array(n); crypto.getRandomValues(r); } catch (e) { r = null; }
    for (var i = 0; i < n; i++) s += a.charAt(r ? r[i] % 36 : Math.floor(Math.random() * 36));
    return s;
  }
  function ga(n, p) { try { if (window.gtag) gtag('event', n, p || {}); } catch (e) {} }
  function filled(v) {
    if (v == null || v === '' || v === false || v === 0) return false;
    if (Array.isArray(v)) return v.some(filled);
    if (typeof v === 'object') { for (var k in v) if (filled(v[k])) return true; return false; }
    return true;
  }
  function norm(s) {
    s = String(s || '').toLowerCase(); var o = '';
    for (var i = 0; i < s.length; i++) { var c = s.charAt(i); o += (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') ? c : ' '; }
    return o.split(' ').filter(Boolean).join(' ');
  }
  function okEmail(s) { s = String(s || '').trim(); var at = s.indexOf('@'); return at > 0 && s.indexOf('.', at) > at + 1 && s.indexOf(' ') < 0 && s.length > 5; }

  // ---------- state ----------
  function load() { try { var j = JSON.parse(localStorage.getItem(KEY) || 'null'); if (j && j.v === 1 && j.sid) return j; } catch (e) {} return null; }
  var S = load(), RESUMED = !!(S && S.touched);
  if (!S) S = { v: 1, sid: 'ds-' + rid(24), step: 0, a: {}, up: [], touched: 0, done: 0 };
  S.up = (S.up || []).filter(function (u) { return u && u.id; });
  S.up.forEach(function (u) { if (u.st === 'up') { u.st = 'err'; u.msg = 'Upload was interrupted'; } });
  function A(k, d) { if (S.a[k] == null) S.a[k] = d; return S.a[k]; }
  function get(p) { var o = S.a, k = p.split('.'); for (var i = 0; i < k.length; i++) { if (o == null) return undefined; o = o[k[i]]; } return o; }
  function set(p, v) {
    var o = S.a, k = p.split('.');
    for (var i = 0; i < k.length - 1; i++) { if (o[k[i]] == null || typeof o[k[i]] !== 'object') o[k[i]] = {}; o = o[k[i]]; }
    o[k[k.length - 1]] = v; touch();
  }
  function touch() { S.touched = 1; save(); prevSoon(); }
  function save(now) {
    clearTimeout(saveT);
    var f = function () {
      S.saved = Date.now();
      try { localStorage.setItem(KEY, JSON.stringify(S)); savedMsg(true); }
      catch (e) {   // storage full: drop picture thumbnails first, keep the answers
        try { S.up.forEach(function (u) { if (u.th && u.th.length > 2000) u.th = ''; }); localStorage.setItem(KEY, JSON.stringify(S)); savedMsg(true); } catch (x) { savedMsg(false); }
      }
    };
    if (now) f(); else saveT = setTimeout(f, 350);
  }
  function savedMsg(ok) {
    var el = byId('tds-saved'); if (!el) return;
    if (!ok) { el.className = 'tds-saved bad'; el.innerHTML = ic('x') + 'Couldn&#39;t save on this device'; return; }
    var t = new Date(S.saved || Date.now());
    el.className = 'tds-saved'; el.innerHTML = ic('check') + 'Saved on this device ' + esc(t.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }));
  }

  // ---------- reusable controls ----------
  function noteKey(k, v) { return k + '|' + v; }
  function notes() { return A('notes', {}); }
  function hasNote(k, v) { var n = notes()[noteKey(k, v)]; return !!(n && String(n).trim()); }
  function chips(k, opts, o) {
    o = o || {};
    if (o.unsure) opts = opts.concat([[UNS, UNS, 'help']]);
    var cur = get(k), multi = !o.single;
    var h = '<div class="chips' + (o.cls ? ' ' + o.cls : '') + '" data-k="' + esc(k) + '" data-m="' + (multi ? 1 : 0) + '"' + (o.rr ? ' data-rr="1"' : '') + (o.label ? ' role="group" aria-label="' + esc(o.label) + '"' : '') + '>';
    opts.forEach(function (x) {
      var v = typeof x === 'string' ? x : x[0], l = typeof x === 'string' ? x : x[1], icn = typeof x === 'string' ? '' : x[2];
      var on = multi ? (cur || []).indexOf(v) >= 0 : cur === v;
      h += '<span class="cw' + (on ? ' on' : '') + (hasNote(k, v) ? ' hn' : '') + (v === UNS ? ' uns' : '') + '"><button type="button" class="chip" data-v="' + esc(v) + '" aria-pressed="' + on + '">' +
        (icn ? ic(icn) : '') + '<span>' + nw(l) + '</span>' + (o.sub && o.sub[v] ? '<i>' + nw(o.sub[v]) + '</i>' : '') + '</button>' +
        (o.nonote ? '' : '<button type="button" class="cn" data-v="' + esc(v) + '" aria-label="Add a note to ' + esc(l) + '" title="Add a note">' + ic('edit') + '</button>') + '</span>';
    });
    h += '</div>';
    if (!o.nonote) h += '<div class="cnote" hidden></div>';
    return h;
  }
  function q(title, sub, body, o) {
    o = o || {};
    return '<div class="q' + (o.cls ? ' ' + o.cls : '') + '"><div class="qh"><h3>' + nw(title) + (o.after || '') + (o.req ? ' <em>required</em>' : '') + '</h3>' + (sub ? '<p>' + nwh(sub) + '</p>' : '') + '</div>' + body + '</div>';
  }
  function inp(k, label, o) {
    o = o || {};
    var v = get(k); v = v == null ? '' : v;
    return '<label class="fld' + (o.wide ? ' wide' : '') + '"><span>' + nw(label) + (o.req ? ' <em>*</em>' : '') + '</span>' +
      (o.area ? '<textarea class="in" rows="' + (o.rows || 3) + '" data-k="' + esc(k) + '" placeholder="' + esc(o.ph || '') + '" maxlength="' + (o.max || 3000) + '">' + esc(v) + '</textarea>'
        : '<input class="in" type="' + (o.type || 'text') + '" data-k="' + esc(k) + '" value="' + esc(v) + '" placeholder="' + esc(o.ph || '') + '" maxlength="' + (o.max || 200) + '"' + (o.ac ? ' autocomplete="' + o.ac + '"' : '') + (o.im ? ' inputmode="' + o.im + '"' : '') + '>') + '</label>';
  }
  function comment(id, title) {
    return '<div class="cmt"><label class="fld wide"><span>' + ic('message') + 'Comments on ' + esc(title) + ' <i>(optional)</i></span><textarea class="in" rows="2" data-k="comments.' + id + '" placeholder="Anything we should know, questions, or ideas" maxlength="3000">' + esc(get('comments.' + id) || '') + '</textarea></label></div>';
  }
  function askBtn(q2, label) { return '<button type="button" class="ask" data-ask="' + esc(q2) + '">' + ic('bot') + '<span>' + nw(label || 'Not sure? Ask our helper') + '</span></button>'; }
  function toggle(on, attrs, label) { return '<button type="button" class="tg' + (on ? ' on' : '') + '" ' + attrs + ' aria-pressed="' + !!on + '"><i></i><span>' + nw(label) + '</span></button>'; }
  function industry() { return get('about.industry') || ''; }
  function indLabel() { var r = ''; C.ind.forEach(function (x) { if (x[0] === industry()) r = x[1]; }); return industry() === 'other' ? (get('about.industry_other') || 'your business') : r; }

  // ---------- uploads ----------
  function upCount() { return S.up.filter(function (u) { return u.st !== 'err'; }).length; }
  function thumb(u) {
    return '<div class="th ' + u.st + '" data-id="' + u.id + '">' + (u.th ? '<img src="' + u.th + '" alt="' + esc(u.name || 'Upload') + '">' : '<span class="thph">' + ic('image') + '</span>') +
      (u.st === 'up' ? '<i class="spin"></i>' : '') + (u.st === 'ok' ? '<b class="ok">' + ic('check') + '</b>' : '') +
      (u.st === 'err' ? '<span class="therr">' + esc(u.msg || 'Upload failed') + (FILES[u.id] ? ' <button type="button" data-rt="' + u.id + '">Retry</button>' : '') + '</span>' : '') +
      '<button type="button" class="thx" data-rm="' + u.id + '" aria-label="Remove this picture">' + ic('x') + '</button></div>';
  }
  function upZone(g, title, tip, max, ref) {
    var items = S.up.filter(function (u) { return u.g === g && (ref ? u.ref === ref : true); });
    return '<div class="up" data-g="' + g + '"' + (ref ? ' data-ref="' + ref + '"' : '') + ' data-max="' + max + '"><label class="drop">' +
      '<input type="file" accept="image/*,.heic,.heif" ' + (max > 1 ? 'multiple ' : '') + 'data-up="' + g + '"' + (ref ? ' data-ref="' + ref + '"' : '') + '>' +
      '<span class="dic">' + ic('upload') + '</span><b>' + nw(title) + '</b><span>' + nw(tip) + '</span></label><div class="ths">' + items.map(thumb).join('') + '</div></div>';
  }
  function redrawUp(g, ref) {
    [].forEach.call(R.querySelectorAll('.up[data-g="' + g + '"]'), function (z) {
      var r2 = z.getAttribute('data-ref');
      z.querySelector('.ths').innerHTML = S.up.filter(function (u) { return u.g === g && (r2 ? u.ref === r2 : true); }).map(thumb).join('');
    });
    [].forEach.call(R.querySelectorAll('.rph[data-ref]'), function (b) {
      var u = S.up.filter(function (x) { return x.g === 'team' && x.ref === b.getAttribute('data-ref'); })[0];
      b.innerHTML = u && u.th ? '<img src="' + u.th + '" alt="">' : ic('camera');
      b.classList.toggle('has', !!u);
    });
    var pb = R.querySelector('[data-pull]');
    if (pb) { var hl = S.up.some(function (u) { return u.g === 'logo' && u.th; }); pb.disabled = !hl; if (hl) pb.removeAttribute('title'); }
    prevSoon();
  }
  function shrink(file) {
    return new Promise(function (res, rej) {
      var url = URL.createObjectURL(file), img = new Image();
      img.onload = function () {
        try {
          var w = img.naturalWidth || 800, h = img.naturalHeight || 800, sc = Math.min(1, 2400 / Math.max(w, h));
          var alpha = /png|webp|svg|gif/i.test(file.type || '') || /png|svg|webp/i.test(file.name || '');
          var out = null, type = '', qv = 0.86, cv = document.createElement('canvas');
          for (var tries = 0; tries < 8; tries++) {
            cv.width = Math.max(1, Math.round(w * sc)); cv.height = Math.max(1, Math.round(h * sc));
            var x = cv.getContext('2d');
            if (!alpha) { x.fillStyle = '#fff'; x.fillRect(0, 0, cv.width, cv.height); }
            x.drawImage(img, 0, 0, cv.width, cv.height);
            if (alpha) { out = cv.toDataURL('image/png'); type = 'image/png'; if (out.length > 4.0e6) { out = cv.toDataURL('image/webp', 0.9); type = out.indexOf('data:image/webp') === 0 ? 'image/webp' : 'image/png'; } }
            else { out = cv.toDataURL('image/jpeg', qv); type = 'image/jpeg'; }
            if (out.length <= 4.0e6) break;
            if (!alpha && qv > 0.6) qv -= 0.12; else sc *= 0.75;
          }
          var t = document.createElement('canvas'), ts = Math.min(1, 240 / Math.max(w, h));
          t.width = Math.max(1, Math.round(w * ts)); t.height = Math.max(1, Math.round(h * ts));
          var tx = t.getContext('2d');
          if (!alpha) { tx.fillStyle = '#fff'; tx.fillRect(0, 0, t.width, t.height); }
          tx.drawImage(img, 0, 0, t.width, t.height);
          var th = alpha ? t.toDataURL('image/png') : t.toDataURL('image/jpeg', 0.72);
          URL.revokeObjectURL(url);
          res({ type: type, b64: out.split(',')[1], th: th });
        } catch (e) { URL.revokeObjectURL(url); rej(e); }
      };
      img.onerror = function () {   // e.g. iPhone HEIC in a browser that can't draw it: send the original if it is small enough
        URL.revokeObjectURL(url);
        var ty = (file.type || '').toLowerCase(), nm = (file.name || '').toLowerCase();
        if (!ty && (nm.slice(-5) === '.heic' || nm.slice(-5) === '.heif')) ty = 'image/' + nm.slice(-4);
        if ((ty === 'image/heic' || ty === 'image/heif') && file.size <= 3e6) {
          var fr = new FileReader();
          fr.onload = function () { res({ type: ty, b64: String(fr.result).split(',')[1], th: '' }); };
          fr.onerror = function () { rej(new Error('read')); };
          fr.readAsDataURL(file);
        } else rej(new Error('That file type didn&#39;t open. Please use a JPG or PNG.'));
      };
      img.src = url;
    });
  }
  function sendPhoto(u, r) {
    return fetch(C.api, { method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ client: CL, session: S.sid, kind: 'photo', group: u.g, name: u.name, type: r.type, data: r.b64, hp: hp() }) })
      .then(function (x) { return x.json().catch(function () { return {}; }).then(function (j) { if (!x.ok || !j.ok) throw new Error(j.error === 'photo limit' ? 'Photo limit reached' : 'Upload failed'); return j.path; }); });
  }
  function upload(u) {
    var f = FILES[u.id]; if (!f) return;
    u.st = 'up'; u.msg = ''; redrawUp(u.g, u.ref);
    shrink(f).then(function (r) { if (r.th) u.th = r.th; redrawUp(u.g, u.ref); return sendPhoto(u, r); })
      .then(function (p) { u.path = p; u.st = 'ok'; })
      .catch(function (e) { u.st = 'err'; u.msg = String((e && e.message) || 'Upload failed').slice(0, 80); })
      .then(function () { touch(); save(true); redrawUp(u.g, u.ref); });
  }
  function addFiles(list, g, ref, max) {
    var mine = S.up.filter(function (u) { return u.g === g && (ref ? u.ref === ref : true); });
    if (ref) mine.forEach(function (u) { S.up.splice(S.up.indexOf(u), 1); });   // roster photo: one per person, replace
    var n = ref ? 0 : mine.length;
    [].slice.call(list).forEach(function (f) {
      if (n >= max) { flash('You can add up to ' + max + ' here.'); return; }
      if (upCount() >= MAXUP) { flash('That&#39;s the limit of ' + MAXUP + ' pictures for this setup. Email any extras to hello@threevillagelocal.com.'); return; }
      var nm = (f.name || '').toLowerCase();
      if ((f.type || '').indexOf('image/') !== 0 && nm.slice(-5) !== '.heic' && nm.slice(-5) !== '.heif') { flash('Pictures only, please (JPG, PNG, WEBP or HEIC).'); return; }
      var u = { id: 'u' + rid(10), g: g, ref: ref || '', name: (f.name || 'photo').slice(0, 60), st: 'up', th: '' };
      FILES[u.id] = f; S.up.push(u); n++; upload(u);
    });
    redrawUp(g, ref); touch();
  }
  function flash(m) {
    var el = byId('tds-flash'); if (!el) return;
    el.innerHTML = m; el.hidden = false; clearTimeout(el._t); el._t = setTimeout(function () { el.hidden = true; }, 5200);
  }

  // ---------- steps ----------
  var STEPS = [
    { id: 'about', t: 'About you', icon: 'store', h: 'Start with the basics.', s: 'Who you are and how to reach you. Only the business name and a way to reach you are needed to send this.' },
    { id: 'picture', t: 'The big picture', icon: 'target', h: 'What should your dashboard fix?', s: 'Tell us what eats your time today. This is how we decide what goes on your home screen.' },
    { id: 'people', t: 'People and access', icon: 'users', h: 'Who gets a dashboard?', s: 'Everyone gets their own login, and you decide what each level can see.' },
    { id: 'modules', t: 'Modules', icon: 'grid', h: 'Pick your building blocks.', s: 'Mark each one Must-have, Nice-to-have or Not needed. Not sure? That&#39;s an answer too.' },
    { id: 'integrations', t: 'Integrations', icon: 'plug', h: 'Which tools do you use today?', s: 'Keep what works. Your dashboard pulls the important numbers from the tools you already use.' },
    { id: 'brand', t: 'Look and brand', icon: 'palette', h: 'Make it look like you.', s: 'Your logo, colors and faces make it feel like your own.' },
    { id: 'numbers', t: 'Data and numbers', icon: 'chart', h: 'Which numbers matter most?', s: 'We put these front and center, and in your reports.' },
    { id: 'devices', t: 'Devices and logins', icon: 'phone', h: 'Where will you use it?', s: 'It works on every screen. This helps us design for the ones you use most.' },
    { id: 'timeline', t: 'Timeline and extras', icon: 'calendar', h: 'When, and what else?', s: 'Timing, training and anything else you want us to know.' },
    { id: 'review', t: 'Review and send', icon: 'send', h: 'Review and send.', s: 'Check everything over. Tap Edit on any section to change it.' }
  ];
  var DRAW = {};

  DRAW.about = function () {
    var inds = C.ind.map(function (x) { return [x[0], x[1], x[2]]; });
    var h = '<div class="grid2">' + inp('about.business', 'Business name', { req: 1, ac: 'organization', ph: 'e.g. Harbor Street Cafe' }) +
      inp('about.owner', 'Owner name', { req: 1, ac: 'name', ph: 'Your full name' }) +
      inp('about.email', 'Email', { req: 1, type: 'email', ac: 'email', im: 'email', ph: 'you@yourbusiness.com' }) +
      inp('about.phone', 'Phone', { type: 'tel', ac: 'tel', im: 'tel', ph: '631-555-0100' }) +
      inp('about.website', 'Website', { ac: 'url', im: 'url', ph: 'yourbusiness.com (if you have one)' }) +
      inp('about.town', 'Town', { ph: 'e.g. Setauket, Stony Brook, Port Jefferson' }) + '</div>';
    h += q('What kind of business is it?', 'We use this to suggest modules, numbers and tools that fit.', chips('about.industry', inds, { single: 1, cls: 'cards', rr: 1, nonote: 1 }) +
      (industry() === 'other' ? '<div class="grid2 mt">' + inp('about.industry_other', 'Tell us what you do', { wide: 1, ph: 'e.g. Pet grooming, dance studio, marina' }) + '</div>' : ''));
    h += q('How many locations?', '', chips('about.locations', ['1', '2', '3 to 5', '6 or more'], { single: 1, nonote: 1 }));
    h += q('Are you a Three Village Local member?', 'If you are, we may already have your logo and photos.', chips('about.member', ['Yes', 'No', 'Not sure'], { single: 1, rr: 1, nonote: 1 }) +
      (get('about.member') === 'Yes' ? '<label class="ck mt"><input type="checkbox" data-k="about.use_3vl"' + (get('about.use_3vl') ? ' checked' : '') + '><span>' + ic('check') + '</span><b>Use what you already have on Three Village Local</b><i>Your logo, photos and business info from your listing. You can still upload newer ones in Step 6.</i></label>' : ''));
    return h + comment('about', 'this section');
  };

  DRAW.picture = function () {
    var fix = ['Too many apps and logins', 'Missed calls and leads', 'Scheduling chaos', 'I don&#39;t know my numbers', 'Social media takes forever', 'Getting more reviews', 'Staff accountability',
      'Chasing invoices and payments', 'Customer follow-up', 'Paperwork and forms', 'Inventory surprises', 'Marketing I can&#39;t measure'].map(function (x) { return [x.split('&#39;').join(String.fromCharCode(39)), x.split('&#39;').join(String.fromCharCode(39))]; });
    var g = A('picture', {}); if (!Array.isArray(g.goals)) g.goals = ['', '', ''];
    var gl = ['Answer every new lead within 5 minutes', 'Know my real profit every week', 'Stop doing payroll and invoices at night'];
    var h = q('What do you want this dashboard to fix?', 'Pick as many as you like. Tap the pencil on any pick to add a note.', chips('picture.fix', fix, { unsure: 1 }));
    h += q('Your top 3 goals', 'In your own words. Short is perfect.', '<div class="goals">' + [0, 1, 2].map(function (i) {
      return '<label class="goal"><b>' + (i + 1) + '</b><input class="in" data-k="picture.goals.' + i + '" value="' + esc(g.goals[i] || '') + '" placeholder="e.g. ' + esc(gl[i]) + '" maxlength="200" aria-label="Goal ' + (i + 1) + '"></label>';
    }).join('') + '</div>');
    h += q('How do you run things today?', 'No wrong answers. Most businesses use a mix.', chips('picture.today_tools', ['Paper and notebooks', 'Spreadsheets', 'A whiteboard', 'Text messages', 'Email', 'A POS system', 'Accounting software', 'Booking software', 'A CRM', 'Several different apps', 'Mostly my memory']) +
      '<div class="mt">' + inp('picture.today', 'Walk us through a normal day (optional)', { area: 1, wide: 1, rows: 3, ph: 'e.g. Calls come in on my cell, I write jobs on a whiteboard, my bookkeeper does QuickBooks on Fridays...' }) + '</div>');
    return h + comment('picture', 'the big picture');
  };

  function roleCount(id) { return +(get('people.roles.' + id) || 0); }
  function seatsSum() { var n = 0; C.roles.forEach(function (r) { n += roleCount(r[0]); }); return n; }
  function access() {
    var acc = A('people', {}); if (!acc.access) acc.access = {};
    C.roles.forEach(function (r) { if (!acc.access[r[0]]) acc.access[r[0]] = (C.access[r[0]] || []).slice(); });
    return acc.access;
  }
  var accRole = 'manager';
  DRAW.people = function () {
    var p = A('people', {}); if (!p.roles) { p.roles = { owner: 1 }; }
    if (!Array.isArray(p.roster)) p.roster = [];
    var h = q('How many people will get a dashboard login?', 'Count everyone who needs to see or do something in it. You can always add people later.',
      chips('people.seats', ['Just me', '2 to 5', '6 to 10', '11 to 25', '26 to 50', '51 or more'], { single: 1, unsure: 1, nonote: 1 }));
    h += q('Which roles or levels do you need?', 'Set how many people are in each. Tap + or -.', '<div class="roles">' + C.roles.map(function (r) {
      var n = roleCount(r[0]);
      return '<div class="role' + (n ? ' on' : '') + '"><div><b>' + nw(r[1]) + '</b><span>' + nw(r[2]) + '</span></div><div class="stp" data-role="' + r[0] + '"><button type="button" data-d="-1" aria-label="One fewer ' + esc(r[1]) + '">-</button><input type="number" min="0" max="500" inputmode="numeric" value="' + n + '" aria-label="' + esc(r[1]) + ' logins" data-rc="' + r[0] + '"><button type="button" data-d="1" aria-label="One more ' + esc(r[1]) + '">+</button></div></div>';
    }).join('') + '</div><p class="sum" id="tds-sum">' + sumText() + '</p>' + '<div class="grid2 mt">' + inp('people.other_roles', 'Any other roles? (optional)', { wide: 1, ph: 'e.g. Seasonal crew, Office manager, Head chef' }) + '</div>');
    var ac = access(), rs = C.roles.filter(function (r) { return roleCount(r[0]) > 0; });
    if (!rs.length) rs = C.roles;
    if (!rs.some(function (r) { return r[0] === accRole; })) accRole = rs[rs.length > 1 ? 1 : 0][0];
    h += q('What should each level see?', 'We started you with what most businesses choose. Tap to change any of it.',
      '<div class="acc"><div class="acct" role="tablist" aria-label="Roles">' + rs.map(function (r) { return '<button type="button" role="tab" class="' + (r[0] === accRole ? 'on' : '') + '" data-accr="' + r[0] + '" aria-selected="' + (r[0] === accRole) + '">' + nw(r[1]) + '<i>' + ac[r[0]].length + '</i></button>'; }).join('') + '</div>' +
      '<div class="accg">' + C.areas.map(function (a) { return toggle(ac[accRole].indexOf(a[0]) >= 0, 'data-acc="' + a[0] + '"', a[1]); }).join('') + '</div>' +
      '<div class="accf"><button type="button" class="lnk" data-accreset="1">' + ic('refresh') + 'Use the recommended set</button>' + askBtn('What should my ' + (C.roles.filter(function (r) { return r[0] === accRole; })[0] || ['', 'staff'])[1] + ' be able to see in the dashboard?', 'Help me decide') + '</div></div>');
    h += q('Your team roster', 'Optional. Add people now, or skip and we set up logins later. A photo is optional too.',
      '<div class="roster" id="tds-roster">' + p.roster.map(rosterRow).join('') + '</div>' +
      '<div class="rbtns"><button type="button" class="tds-btn tds-ghost sm" data-radd="1">' + ic('plus') + 'Add a person</button>' +
      '<label class="tds-btn tds-ghost sm"><input type="file" accept=".csv,text/csv" data-csv="1" hidden>' + ic('sheet') + 'Upload a spreadsheet (CSV)</label></div>' +
      '<p class="hint">Spreadsheet columns: name, role, email. One person per row.</p>');
    return h + comment('people', 'people and access');
  };
  function sumText() {
    var n = seatsSum();
    return n ? 'Your roles add up to <b>' + n + ' login' + (n === 1 ? '' : 's') + '</b>.' : 'Add at least one role, or pick &quot;Not sure&quot; above.';
  }
  function rosterRow(r, i) {
    if (!r.id) r.id = 'r' + rid(8);
    var u = S.up.filter(function (x) { return x.g === 'team' && x.ref === r.id; })[0];
    return '<div class="rrow" data-ri="' + i + '"><label class="rph' + (u ? ' has' : '') + '" data-ref="' + r.id + '" title="Add a photo"><input type="file" accept="image/*,.heic,.heif" data-up="team" data-ref="' + r.id + '" hidden>' + (u && u.th ? '<img src="' + u.th + '" alt="">' : ic('camera')) + '</label>' +
      '<input class="in" data-k="people.roster.' + i + '.name" value="' + esc(r.name || '') + '" placeholder="Name" aria-label="Name" maxlength="80">' +
      '<select class="in" data-k="people.roster.' + i + '.role" aria-label="Role"><option value="">Role</option>' + C.roles.map(function (x) { return '<option' + (r.role === x[1] ? ' selected' : '') + '>' + esc(x[1]) + '</option>'; }).join('') + '</select>' +
      '<input class="in" type="email" data-k="people.roster.' + i + '.email" value="' + esc(r.email || '') + '" placeholder="Email (optional)" aria-label="Email" maxlength="120">' +
      '<button type="button" class="rx" data-rdel="' + i + '" aria-label="Remove this person">' + ic('x') + '</button></div>';
  }

  DRAW.modules = function () {
    var M = A('modules', {}), sug = C.sug[industry()] || [];
    var list = C.mods.slice().sort(function (a, b) { return (sug.indexOf(a[0]) >= 0 ? 0 : 1) - (sug.indexOf(b[0]) >= 0 ? 0 : 1); });
    var picked = C.mods.filter(function (m) { return M[m[0]] && (M[m[0]].p === 'must' || M[m[0]].p === 'nice'); }).length;
    var h = sug.length ? '<div class="sugbar">' + ic('sparkle') + '<p><b>Suggested for ' + nw(String(indLabel()).toLowerCase()) + '</b>We moved the modules ' + nw(String(indLabel()).toLowerCase()) + ' owners use most to the top.</p><button type="button" class="tds-btn tds-blue sm" data-sugall="1">Mark them must-have</button></div>' : '';
    h += '<p class="sum">' + (picked ? '<b>' + picked + ' picked</b> so far.' : 'Nothing picked yet.') + ' Must-haves go in your first launch; nice-to-haves can come later.</p>';
    h += '<div class="mods">' + list.map(function (m) {
      var st = M[m[0]] || {}, isS = sug.indexOf(m[0]) >= 0;
      var body = m[0] === 'automations' ? '<div class="autos">' + chips('automations.list', C.autos, { unsure: 1 }) + inp('automations.other', 'Another automation you want', { wide: 1, ph: 'e.g. Text me when a big order comes in' }) + '</div>' : '';
      return '<div class="mod' + (st.p === 'must' || st.p === 'nice' ? ' on' : '') + (st.p === 'no' ? ' off' : '') + '" data-mod="' + m[0] + '"><div class="mhd"><span class="mic">' + ic(m[3]) + '</span><div><h4>' + nw(m[1]) + (isS ? '<em>Suggested</em>' : '') + '</h4><p>' + nw(m[2]) + '</p></div></div>' + body +
        chips('modules.' + m[0] + '.p', [['must', 'Must-have'], ['nice', 'Nice-to-have'], ['no', 'Not needed'], ['unsure', 'Not sure']], { single: 1, nonote: 1, cls: 'seg', label: m[1] + ' priority' }) +
        '<details class="mc"' + (st.c ? ' open' : '') + '><summary>' + ic('message') + (st.c ? 'Your comment' : 'Add a comment') + '</summary><textarea class="in" rows="2" data-k="modules.' + m[0] + '.c" placeholder="What would you use this for?" maxlength="1500">' + esc(st.c || '') + '</textarea></details></div>';
    }).join('') + '</div>';
    h += '<div class="mt">' + askBtn('Which dashboard modules should I start with' + (industry() ? ' for a ' + indLabel() : '') + '?', 'Not sure what to pick? Ask our helper') + '</div>';
    return h + comment('modules', 'modules');
  };

  // integrations
  var TOOLS = C.tools, TIDX = {}, POPSET = {};
  Object.keys(C.pop).forEach(function (k) { C.pop[k].forEach(function (n) { POPSET[n] = 1; }); });
  TOOLS.forEach(function (t, i) { TIDX[t[0]] = i; t.n = norm(t[0]); t.x = norm(t[0] + ' ' + C.cats[t[1]] + ' ' + t[3]); });
  function logo(t, sz) {
    var hx = String(t[5] || '');
    if (t[4]) return '<span class="lg" style="--c:#' + hx + '"><i style="-webkit-mask-image:url(' + C.cdn + t[4] + '.svg);mask-image:url(' + C.cdn + t[4] + '.svg)"></i></span>';
    var letters = t[0].split(' ').slice(0, 2).map(function (w) { return w.charAt(0); }).join('').toUpperCase();
    var bg = hx.length === 6 ? '#' + hx : 'hsl(' + hx + ' 55% 42%)';
    return '<span class="lg lt" style="background:' + bg + '">' + esc(letters) + '</span>';
  }
  function isSel(n) { var T = get('integrations.tools'); return !!(T && T[n]); }
  function tile(t) {
    var on = isSel(t[0]);
    return '<button type="button" class="tool' + (on ? ' on' : '') + '" data-tool="' + esc(t[0]) + '" aria-pressed="' + on + '">' + logo(t) + '<span><b>' + nw(t[0]) + '</b><i>' + nw(C.cats[t[1]]) + '</i></span><em>' + (on ? ic('check') : ic('plus')) + '</em></button>';
  }
  function popList() {
    var k = industry(); var p = C.pop[k] || C.pop.gen;
    return p.map(function (n) { return TOOLS[TIDX[n]]; }).filter(Boolean);
  }
  function search(qs, cat) {
    var qn = norm(qs), toks = qn ? qn.split(' ') : [], out = [];
    TOOLS.forEach(function (t) {
      if (t[2] === 'B') return;
      if (cat !== '' && cat != null && String(t[1]) !== String(cat)) return;
      if (!toks.every(function (w) { return t.x.indexOf(w) >= 0; })) return;
      var sc = (t.n.indexOf(qn) === 0 ? 0 : t.n.indexOf(qn) >= 0 ? 2 : 4) + (POPSET[t[0]] ? 0 : 1);
      out.push([sc, t]);
    });
    out.sort(function (a, b) { return a[0] - b[0] || (a[1][0] < b[1][0] ? -1 : 1); });
    return out.map(function (x) { return x[1]; });
  }
  function drawResults() {
    var box = byId('tds-ires'); if (!box) return;
    var qs = (byId('tds-isrch') || {}).value || '';
    var list = qs.trim() ? search(qs, '').slice(0, 36) : popList();
    byId('tds-ilab').innerHTML = qs.trim() ? (list.length ? 'Matches' : 'No match yet. Add it under &quot;Something else&quot; below, we can usually connect it.') : 'Popular' + (industry() && C.pop[industry()] ? ' with ' + nw(String(indLabel()).toLowerCase()) + ' owners' : '');
    box.innerHTML = list.map(tile).join('');
  }
  function drawSel() {
    var box = byId('tds-isel'); if (!box) return;
    var T = A('integrations', {}); if (!T.tools) T.tools = {};
    var names = Object.keys(T.tools);
    byId('tds-icount').textContent = names.length ? '(' + names.length + ')' : '';
    box.innerHTML = names.length ? names.map(function (n) {
      var t = TOOLS[TIDX[n]] || [n, 0, 'C', '', '', '200'], v = T.tools[n] || {};
      return '<div class="sel" data-it="' + esc(n) + '"><div class="selh">' + logo(t) + '<div><b>' + nw(n) + '</b><i><span class="cx cx-' + t[2] + '">' + esc(C.conn[t[2]] || '') + '</span>' + (t[3] ? ' ' + esc(t[3]) : '') + '</i></div><button type="button" class="rx" data-tool="' + esc(n) + '" aria-label="Remove ' + esc(n) + '">' + ic('x') + '</button></div>' +
        '<div class="need" role="group" aria-label="What we need from ' + esc(n) + '"><span>We need:</span>' + [['read', 'Read only'], ['two', 'Two-way'], ['unsure', 'Not sure']].map(function (o) {
          return '<button type="button" class="' + (v.need === o[0] ? 'on' : '') + '" data-need="' + o[0] + '" aria-pressed="' + (v.need === o[0]) + '">' + nw(o[1]) + '</button>';
        }).join('') + '</div><input class="in" data-itn="1" value="' + esc(v.note || '') + '" placeholder="What do you use it for? (optional)" maxlength="300" aria-label="Comment on ' + esc(n) + '"></div>';
    }).join('') : '<p class="empty">Tap a tool above to add it. Skip this if you&#39;re not sure, we&#39;ll ask on our call.</p>';
  }
  DRAW.integrations = function () {
    var h = q('Find your tools', 'Search ' + C.ntools + ' tools, or tap the popular ones below.',
      '<label class="tds-search big">' + ic('search') + '<input type="search" id="tds-isrch" placeholder="Search, like QuickBooks or Square" aria-label="Search tools" autocomplete="off"></label>' +
      '<p class="ilab" id="tds-ilab"></p><div class="tools" id="tds-ires"></div>' +
      '<button type="button" class="lnk all" data-modal="open">' + ic('grid') + 'See all ' + C.ntools + ' integrations</button>');
    h += q('Your tools', '<b>Read only</b> means we pull your numbers in to show them. <b>Two-way</b> means the dashboard can also send changes back, like booking an appointment or creating an invoice.', '<div id="tds-isel"></div>', { after: ' <span id="tds-icount"></span>' });
    h += q('Something else?', 'Software that isn&#39;t on the list, or anything you&#39;re not sure about. If it has an export or an API, we can usually connect it.', inp('integrations.other', 'Other tools', { area: 1, wide: 1, rows: 2, ph: 'e.g. JobTread, an old Access database, our bank' }) +
      '<div class="mt">' + askBtn('How do integrations work, and what is the difference between read only and two-way?', 'How do connections work?') + '</div>');
    return h + comment('integrations', 'integrations');
  };

  DRAW.brand = function () {
    var b = A('brand', {}); if (!Array.isArray(b.colors)) b.colors = [];
    var hasLogo = S.up.some(function (u) { return u.g === 'logo' && u.th; });
    var h = get('about.use_3vl') ? '<div class="sugbar">' + ic('star') + '<p><b>We&#39;ll start with your Three Village Local photos.</b>You asked us to use your logo and photos from your listing. Upload here only if you have newer ones.</p></div>' : '';
    h += q('Your logo', 'A PNG with a clear background is best, but any picture works. Up to 3 versions.', upZone('logo', 'Add your logo', 'Tap to choose, or drop files here', 3));
    h += q('Headshots', 'You and anyone who should appear on the dashboard (team pages, welcome screen). Up to 10.', upZone('headshot', 'Add headshots', 'Tap to choose, or drop files here', 10));
    h += q('Brand colors', 'Pick up to 4. Tap a swatch to change it.', '<div class="colors" id="tds-colors">' + b.colors.map(function (c, i) {
      return '<div class="sw"><label style="background:' + esc(c) + '"><input type="color" value="' + esc(c) + '" data-ci="' + i + '" aria-label="Brand color ' + (i + 1) + '"></label><code>' + esc(c.toUpperCase()) + '</code><button type="button" class="rx" data-cdel="' + i + '" aria-label="Remove color">' + ic('x') + '</button></div>';
    }).join('') + (b.colors.length < 4 ? '<button type="button" class="swadd" data-cadd="1">' + ic('plus') + '<span>Add a color</span></button>' : '') + '</div>' +
      '<div class="cbtns"><button type="button" class="tds-btn tds-ghost sm" data-pull="1"' + (hasLogo ? '' : ' disabled title="Upload a logo first"') + '>' + ic('palette') + 'Pull colors from my logo</button>' +
      chips('brand.color_help', ['Help me pick colors'], { nonote: 1 }) + '</div>');
    h += q('Pick a style', '', chips('brand.style', [['light', 'Clean and light'], ['dark', 'Dark premium'], ['bold', 'Bold color'], ['site', 'Match my website']], { single: 1, cls: 'styles', unsure: 1, nonote: 1, sub: { light: 'Bright, airy, easy on the eyes', dark: 'Deep navy, glowing numbers', bold: 'Your brand color up front', site: 'Same look as your website' } }));
    h += '<div class="grid2 mt">' + inp('brand.name_idea', 'Dashboard name idea (optional)', { wide: 1, ph: 'e.g. ' + (get('about.business') ? String(get('about.business')).split(' ')[0] + ' HQ' : 'Harbor HQ') }) + '</div>';
    h += q('Screens you like (optional)', 'Screenshots of any app or dashboard whose look you love. Up to 5.', upZone('samples', 'Add screenshots', 'Tap to choose, or drop files here', 5));
    return h + comment('brand', 'look and brand');
  };

  DRAW.numbers = function () {
    var ik = C.kpii[industry()] || [];
    var h = q('What numbers matter most?', 'Pick the ones you&#39;d want to see first thing every morning.' + (ik.length ? ' The first few are popular with ' + nw(String(indLabel()).toLowerCase()) + ' owners.' : ''), chips('numbers.kpis', ik.concat(C.kpig), { unsure: 1 }) +
      '<div class="grid2 mt">' + inp('numbers.custom', 'Any other numbers?', { wide: 1, ph: 'e.g. How many catering orders we get on weekends' }) + '</div>');
    h += q('How often do you want a report?', '', chips('numbers.freq', ['Daily morning briefing', 'Weekly owner report by email', 'Weekly summary by text', 'Monthly report', 'Real-time alerts for big things'], { unsure: 1 }));
    h += q('Goals and targets (optional)', 'Numbers you&#39;re aiming for. We can show progress bars for these.', inp('numbers.targets', 'Your targets', { area: 1, wide: 1, rows: 3, ph: 'e.g. 40 new leads a month, 4.8 stars on Google, 20 percent more repeat customers' }));
    return h + comment('numbers', 'data and numbers');
  };

  DRAW.devices = function () {
    var h = q('Which devices will you and your team use?', '', chips('devices.devices', [['Phone', 'Phone', 'phone'], ['Tablet', 'Tablet', 'tablet'], ['Laptop', 'Laptop', 'laptop'], ['Desktop computer', 'Desktop computer', 'monitor'], ['Front-desk kiosk', 'Front-desk kiosk', 'kiosk'], ['TV screen in the shop', 'TV screen in the shop', 'tv']], { cls: 'icons', unsure: 1 }));
    h += q('How should people sign in?', 'Pick any. We recommend 2-step verification for owners and anyone who sees money.', chips('devices.signin', ['Email and password', 'Google sign-in', 'Microsoft sign-in', '2-step verification (a code on your phone)'], { unsure: 1 }));
    h += q('Who will be the admin?', 'The person who adds people, changes access and gets account emails.', '<div class="grid2">' + inp('devices.admin', 'Admin name', { ph: get('about.owner') ? String(get('about.owner')) + ' (owner)' : 'Name' }) + inp('devices.admin_email', 'Admin email', { type: 'email', im: 'email', ph: 'name@yourbusiness.com' }) + '</div>');
    return h + comment('devices', 'devices and logins');
  };

  DRAW.timeline = function () {
    var h = q('When would you like it?', '', chips('timeline.when', ['As soon as possible', 'Within 30 days', 'In 1 to 3 months', 'Just exploring for now'], { single: 1, unsure: 1 }));
    h += q('What training would help?', '', chips('timeline.training', ['Live walkthrough (in person or video call)', 'Short how-to videos', 'A written guide', 'Train my team too']));
    h += q('Ongoing updates and support?', 'New screens, reports and automations as your business grows.', chips('timeline.support', ['Yes, keep improving it', 'Maybe, tell me more', 'No, just build it'], { single: 1, unsure: 1 }));
    h += q('Anything else we can help with?', 'Other things our local team does. Pick any you&#39;d like to hear about.', chips('timeline.addons', [['AI website chatbot', 'AI website chatbot', 'bot'], ['AI-optimized website', 'AI-optimized website', 'globe'], ['Promo video', 'Promo video', 'video'], ['Social media management', 'Social media management', 'megaphone'], ['AI search optimization', 'AI search optimization', 'sparkle']], { cls: 'icons' }));
    h += q('Anything else?', '', inp('timeline.extra', 'Anything else we should know', { area: 1, wide: 1, rows: 4, ph: 'Questions, must-haves, deal-breakers, deadlines...' }));
    return h + comment('timeline', 'timeline and extras');
  };

  // ---------- payload (what we send + what the review shows) ----------
  function labelsOf(arr) { return (arr || []).filter(function (x) { return x; }); }
  function modP(p) { return { must: 'Must-have', nice: 'Nice-to-have', no: 'Not needed', unsure: 'Not sure' }[p] || ''; }
  function ups(g) { return S.up.filter(function (u) { return u.g === g && u.st === 'ok'; }).map(function (u) { return u.path; }); }
  function payload() {
    var a = S.a, ab = a.about || {}, pi = a.picture || {}, pe = a.people || {}, b = a.brand || {}, nu = a.numbers || {}, dv = a.devices || {}, tl = a.timeline || {}, it = a.integrations || {};
    var out = {};
    out.about = { business: ab.business || '', owner: ab.owner || '', email: ab.email || '', phone: ab.phone || '', website: ab.website || '',
      industry: ab.industry === 'other' ? 'Other: ' + (ab.industry_other || '') : indLabel(), town: ab.town || '', locations: ab.locations || '',
      member: ab.member || '', use_3vl: ab.member === 'Yes' && !!ab.use_3vl };
    out.picture = { 'What to fix': labelsOf(pi.fix), 'Top goals': labelsOf((pi.goals || []).map(function (x) { return String(x || '').trim(); })), 'How they run things today': labelsOf(pi.today_tools), 'A normal day': pi.today || '' };
    var roles = {}, accOut = {}, ac = pe.access || {};
    C.roles.forEach(function (r) { var n = +((pe.roles || {})[r[0]] || 0); if (n > 0) { roles[r[1]] = n; accOut[r[1]] = (ac[r[0]] || C.access[r[0]] || []).map(function (x) { var l = ''; C.areas.forEach(function (y) { if (y[0] === x) l = y[1]; }); return l; }).filter(Boolean); } });
    out.people = { 'Logins': pe.seats || '', 'Logins by role': roles, 'Total from roles': seatsSum() || '', 'Other roles': pe.other_roles || '', 'What each role sees': accOut,
      'Team roster': (pe.roster || []).filter(function (r) { return r && (r.name || r.email); }).map(function (r) {
        var u = S.up.filter(function (x) { return x.g === 'team' && x.ref === r.id && x.st === 'ok'; })[0];
        return [r.name, r.role ? '(' + r.role + ')' : '', r.email, u ? '(photo added)' : ''].filter(Boolean).join(' ');
      }) };
    var mods = {};
    C.mods.forEach(function (m) { var s = (a.modules || {})[m[0]]; if (s && (s.p || (s.c && String(s.c).trim()))) mods[m[1]] = { priority: modP(s.p), comment: s.c || '' }; });
    out.modules = mods;
    out.automations = labelsOf(((a.automations || {}).list || []).concat((a.automations || {}).other ? ['Other: ' + a.automations.other] : []));
    var tools = {};
    Object.keys(it.tools || {}).forEach(function (n) { var v = it.tools[n] || {}; tools[n] = { need: { read: 'Read only', two: 'Two-way', unsure: 'Not sure' }[v.need] || 'Not chosen', comment: v.note || '' }; });
    out.integrations = { tools: tools, other: it.other || '' };
    out.brand = { 'Logos uploaded': ups('logo'), 'Headshots uploaded': ups('headshot'), 'Colors': labelsOf(b.colors).map(function (c) { return String(c).toUpperCase(); }), 'Wants help with colors': (b.color_help || []).length ? true : '',
      'Style': { light: 'Clean and light', dark: 'Dark premium', bold: 'Bold color', site: 'Match my website' }[b.style] || b.style || '', 'Dashboard name idea': b.name_idea || '', 'Sample screens uploaded': ups('samples') };
    out.numbers = { 'Numbers that matter': labelsOf(nu.kpis), 'Other numbers': nu.custom || '', 'Reports': labelsOf(nu.freq), 'Goals and targets': nu.targets || '' };
    out.devices = { 'Devices': labelsOf(dv.devices), 'Sign-in': labelsOf(dv.signin), 'Admin': dv.admin || '', 'Admin email': dv.admin_email || '' };
    out.timeline = { 'When': tl.when || '', 'Training': labelsOf(tl.training), 'Ongoing support': tl.support || '', 'Interested in': labelsOf(tl.addons), 'Anything else': tl.extra || '' };
    var nt = {}, NM = { 'picture.fix': 'What to fix', 'picture.today_tools': 'Runs things with', 'automations.list': 'Automation', 'numbers.kpis': 'Number', 'numbers.freq': 'Report',
      'devices.devices': 'Device', 'devices.signin': 'Sign-in', 'timeline.training': 'Training', 'timeline.addons': 'Add-on', 'timeline.when': 'When', 'timeline.support': 'Support' };
    Object.keys(a.notes || {}).forEach(function (k) { var v = String(a.notes[k] || '').trim(); if (!v) return; var p = k.split('|'); nt[(NM[p[0]] || p[0]) + ': ' + p.slice(1).join('|')] = v; });
    out.notes = nt;
    var cm = {};
    STEPS.forEach(function (s) { var v = String(((a.comments || {})[s.id]) || '').trim(); if (v) cm[s.t] = v; });
    out.comments = cm;
    out.meta = { photos: S.up.filter(function (u) { return u.st === 'ok'; }).map(function (u) { return u.g + ': ' + u.path; }), page: location.pathname, started: S.started || '', form: 'v1' };
    return out;
  }
  function show(v) {
    if (Array.isArray(v)) { v = v.filter(filled); return v.length ? v.map(function (x) { return typeof x === 'object' ? show(x) : nw(x); }).join(', ') : ''; }
    if (v && typeof v === 'object') return Object.keys(v).filter(function (k) { return filled(v[k]); }).map(function (k) { return '<b>' + esc(k) + ':</b> ' + show(v[k]); }).join('; ');
    if (v === true) return 'Yes';
    return nw(v);
  }
  var RV = [['about', 0, { business: 'Business', owner: 'Owner', email: 'Email', phone: 'Phone', website: 'Website', industry: 'Industry', town: 'Town', locations: 'Locations', member: 'Three Village Local member', use_3vl: 'Use our listing photos' }],
    ['picture', 1], ['people', 2], ['modules', 3], ['integrations', 4], ['brand', 5], ['numbers', 6], ['devices', 7], ['timeline', 8]];
  DRAW.review = function () {
    var P = payload(), miss = [];
    if (!String(P.about.business).trim()) miss.push('your business name');
    if (!String(P.about.owner).trim()) miss.push('your name');
    if (!okEmail(P.about.email) && !String(P.about.phone).trim()) miss.push('an email or phone number');
    var h = '<div class="rvprev">' + preview(true) + '</div>';
    if (miss.length) h += '<div class="warn">' + ic('help') + '<p>Before you send, we still need ' + miss.join(', ') + '. <button type="button" class="lnk" data-step="0">Add it in Step 1</button></p></div>';
    RV.forEach(function (r) {
      var k = r[0], v = P[k], rows = '';
      if (k === 'modules') {
        var M = v, grp = { 'Must-have': [], 'Nice-to-have': [], 'Not sure': [], 'Not needed': [], '': [] };
        Object.keys(M).forEach(function (n) { (grp[M[n].priority] || grp['']).push(n + (M[n].comment ? ' (' + M[n].comment + ')' : '')); });
        Object.keys(grp).forEach(function (g) { if (grp[g].length) rows += '<div class="rr"><span>' + (g || 'Comments') + '</span><p>' + grp[g].map(nw).join(', ') + '</p></div>'; });
        if (P.automations.length) rows += '<div class="rr"><span>Automations</span><p>' + show(P.automations) + '</p></div>';
      } else if (k === 'integrations') {
        Object.keys(v.tools).forEach(function (n) { rows += '<div class="rr"><span>' + nw(n) + '</span><p>' + nw(v.tools[n].need) + (v.tools[n].comment ? '. ' + nw(v.tools[n].comment) : '') + '</p></div>'; });
        if (v.other) rows += '<div class="rr"><span>Something else</span><p>' + esc(v.other) + '</p></div>';
      } else {
        Object.keys(v).forEach(function (f) {
          var x = v[f]; if (!filled(x)) return;
          var lab = r[2] ? r[2][f] || f : f;
          if (f.indexOf('uploaded') > 0) { rows += '<div class="rr"><span>' + esc(lab.replace(' uploaded', '')) + '</span><p class="rth">' + S.up.filter(function (u) { return u.st === 'ok' && x.indexOf(u.path) >= 0; }).map(function (u) { return u.th ? '<img src="' + u.th + '" alt="">' : '<i>' + ic('image') + '</i>'; }).join('') + '</p></div>'; return; }
          rows += '<div class="rr"><span>' + esc(lab) + '</span><p>' + show(x) + '</p></div>';
        });
      }
      var cm = P.comments[STEPS[r[1]].t];
      if (cm) rows += '<div class="rr cm"><span>Comments</span><p>' + esc(cm) + '</p></div>';
      Object.keys(P.notes).forEach(function (nk) { var pre = nk.split(': ')[0]; if (secOfNote(pre) === k) rows += '<div class="rr cm"><span>Note</span><p><b>' + esc(nk.split(': ').slice(1).join(': ')) + ':</b> ' + esc(P.notes[nk]) + '</p></div>'; });
      h += '<div class="rv"><div class="rvh"><span class="rvi">' + ic(STEPS[r[1]].icon) + '</span><h3>' + (r[1] + 1) + '. ' + nw(STEPS[r[1]].t) + '</h3><button type="button" class="lnk" data-step="' + r[1] + '">' + ic('edit') + 'Edit</button></div>' +
        (rows || '<p class="skipd">Skipped. That&#39;s fine, we&#39;ll cover it on our call.</p>') + '</div>';
    });
    h += '<label class="ck consent"><input type="checkbox" id="tds-consent"' + (S.consent ? ' checked' : '') + '><span>' + ic('check') + '</span><b>Three Village Local may contact me about my dashboard and use what I shared here to design it.</b><i>We reply by email, usually within one business day. No pressure, no obligation.</i></label>';
    h += '<div class="sendrow"><button type="button" class="tds-btn tds-gold big" id="tds-send"' + (miss.length ? ' disabled' : '') + '>' + ic('send') + 'Send my dashboard setup</button><p id="tds-sendmsg" class="sendmsg" role="status"></p></div>';
    return h;
  };
  function secOfNote(pre) {
    return { 'What to fix': 'picture', 'Runs things with': 'picture', 'Automation': 'modules', 'Number': 'numbers', 'Report': 'numbers', 'Device': 'devices', 'Sign-in': 'devices', 'Training': 'timeline', 'Add-on': 'timeline', 'When': 'timeline', 'Support': 'timeline' }[pre] || 'timeline';
  }

  // ---------- live preview ----------
  function preview(big) {
    var a = S.a, b = a.brand || {}, ab = a.about || {}, M = a.modules || {};
    var col = (b.colors && b.colors[0]) || '#1d5fbf', name = String(b.name_idea || (ab.business ? ab.business : 'Your Business')).slice(0, 34);
    var lg = S.up.filter(function (u) { return u.g === 'logo' && u.th; })[0];
    var initials = String(ab.business || 'YB').split(' ').filter(Boolean).slice(0, 2).map(function (w) { return w.charAt(0); }).join('').toUpperCase();
    var mods = C.mods.filter(function (m) { return M[m[0]] && (M[m[0]].p === 'must' || M[m[0]].p === 'nice'); });
    if (!mods.length) mods = C.mods.filter(function (m) { return ['crm', 'calendar', 'finance', 'marketing', 'reviews', 'tasks'].indexOf(m[0]) >= 0; });
    var k = ((a.numbers || {}).kpis || []).filter(function (x) { return x !== UNS; });
    if (!k.length) k = ['Sales this week', 'New leads', 'Google rating'];
    var vals = ['+18%', '+12%', '+6%'], spark = ['M0 18 L10 14 L20 16 L30 9 L40 11 L50 4', 'M0 16 L10 17 L20 11 L30 12 L40 6 L50 7', 'M0 12 L10 10 L20 11 L30 8 L40 8 L50 5'];
    var hr = new Date().getHours(), greet = hr < 12 ? 'Good morning' : hr < 17 ? 'Good afternoon' : 'Good evening';
    var who = String(ab.owner || '').split(' ')[0];
    var st = b.style && b.style !== UNS ? b.style : 'light';
    var n = seatsSum();
    var h = '<div class="pv pv-' + st + (big ? ' pv-big' : '') + '" style="--pc:' + esc(col) + '"><div class="pvbar"><span class="pvlogo">' + (lg ? '<img src="' + lg.th + '" alt="">' : esc(initials)) + '</span><b>' + esc(name) + '</b><span class="pvrole">' + ic('users') + (n > 1 ? n + ' logins' : 'Owner view') + '</span></div>' +
      '<div class="pvbody"><div class="pvnav">' + mods.slice(0, big ? 9 : 6).map(function (m, i) { return '<span class="' + (i ? '' : 'on') + '">' + ic(m[3]) + '<em>' + esc(m[1].split(' and ')[0].split(',')[0]) + '</em></span>'; }).join('') + (mods.length > (big ? 9 : 6) ? '<span class="more">+' + (mods.length - (big ? 9 : 6)) + ' more</span>' : '') + '</div>' +
      '<div class="pvmain"><p class="pvg">' + greet + (who ? ', ' + esc(who) : '') + '</p><div class="pvk">' + k.slice(0, 3).map(function (x, i) {
        return '<div><i>' + esc(String(x).slice(0, 28)) + '</i><b>' + vals[i] + '</b><svg viewBox="0 0 50 20" preserveAspectRatio="none" aria-hidden="true"><path d="' + spark[i] + '"/></svg></div>';
      }).join('') + '</div><div class="pvch"><span style="height:40%"></span><span style="height:62%"></span><span style="height:48%"></span><span style="height:75%"></span><span style="height:58%"></span><span style="height:88%"></span><span style="height:70%"></span></div>' +
      '<div class="pvfeed"><p>' + ic('bolt') + 'Missed call texted back</p><p>' + ic('star') + 'New 5-star review</p></div></div></div></div>';
    return h;
  }
  function prevSoon() { clearTimeout(prevT); prevT = setTimeout(function () { var p = byId('tds-prev'); if (p) p.innerHTML = preview(false); }, 120); }

  // ---------- frame: rail, top, nav ----------
  function stepDone(i) {
    var id = STEPS[i].id;
    if (id === 'review') return !!S.done;
    if (id === 'modules') return filled(S.a.modules) || filled(S.a.automations);
    if (id === 'brand') return filled(S.a.brand) || S.up.some(function (u) { return u.g !== 'team'; });
    if (id === 'people') { var p = S.a.people || {}; return filled(p.seats) || filled(p.roster) || seatsSum() > 1 || filled(p.other_roles); }
    return filled(S.a[id]) || filled((S.a.comments || {})[id]);
  }
  function pct() { var n = 0; for (var i = 0; i < 9; i++) if (stepDone(i)) n++; return Math.round(n / 9 * 100); }
  function drawFrame() {
    var i = S.step, s = STEPS[i], p = pct();
    byId('tds-rail').innerHTML = '<div class="rp"><svg viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="19"/><circle cx="22" cy="22" r="19" class="v" pathLength="100" style="stroke-dashoffset:' + (100 - p) + '"/></svg><b>' + p + '%</b><span>complete</span></div>' +
      '<ol>' + STEPS.map(function (x, j) { return '<li><button type="button" data-step="' + j + '" class="' + (j === i ? 'on' : '') + (stepDone(j) ? ' done' : '') + '"' + (j === i ? ' aria-current="step"' : '') + '><b>' + (stepDone(j) && j !== i ? ic('check') : j + 1) + '</b><span>' + nw(x.t) + '</span></button></li>'; }).join('') + '</ol>' +
      '<p class="rhelp">' + ic('bot') + '<span>Stuck on anything? <button type="button" class="lnk" data-ask="I need help filling out the ' + esc(s.t) + ' step.">Ask our helper</button></span></p>';
    byId('tds-top').innerHTML = '<div class="tt"><p class="tds-eyebrow">Step ' + (i + 1) + ' of ' + STEPS.length + ' &middot; ' + nw(s.t) + '</p><button type="button" class="steps-btn" data-allsteps="1" aria-expanded="false">' + ic('list') + 'All steps</button></div>' +
      '<div class="bar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="' + p + '" aria-label="Setup progress"><i style="width:' + Math.max(4, p) + '%"></i></div>' +
      '<div class="mlist" id="tds-mlist2" hidden>' + STEPS.map(function (x, j) { return '<button type="button" data-step="' + j + '" class="' + (j === i ? 'on' : '') + (stepDone(j) ? ' done' : '') + '"><b>' + (j + 1) + '</b>' + nw(x.t) + (stepDone(j) ? ic('check') : '') + '</button>'; }).join('') + '</div>' +
      '<h2>' + nw(s.h) + '</h2><p class="lede">' + nwh(s.s) + '</p>';
    var last = i === STEPS.length - 1;
    byId('tds-nav').innerHTML = S.done && last ? '' : '<div class="nv">' + (i > 0 ? '<button type="button" class="tds-btn tds-ghost" data-nav="back">' + ic('back') + '<span>Back</span></button>' : '<span></span>') +
      (last ? '' : '<div class="nvr"><button type="button" class="lnk skip" data-nav="skip">Skip for now</button><button type="button" class="tds-btn tds-blue" data-nav="next"><span>' + (i === STEPS.length - 2 ? 'Review' : 'Continue') + '</span>' + ic('arrow') + '</button></div>') + '</div>' +
      '<div class="nvf"><span id="tds-saved" class="tds-saved"></span><button type="button" class="lnk" data-later="1">' + ic('save') + 'Save and finish later</button></div>';
    if (S.saved) savedMsg(true);
  }
  function drawStep() {
    var s = STEPS[S.step], el = byId('tds-step');
    if (S.done && s.id === 'review') { el.innerHTML = doneView(); }
    else el.innerHTML = DRAW[s.id]();
    if (s.id === 'integrations') { drawResults(); drawSel(); }
    drawFrame();
  }
  function go(n, scroll) {
    n = Math.max(0, Math.min(STEPS.length - 1, n));
    if (n !== S.step) { S.step = n; save(); ga('dash_setup_step', { step: n + 1, name: STEPS[n].id }); }
    drawStep();
    if (scroll !== false) {
      var w = byId('tds-wiz'), y = w.getBoundingClientRect().top + (window.pageYOffset || 0) - 86;
      if (Math.abs(w.getBoundingClientRect().top) > 40) window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
    }
  }
  function rerenderKeepScroll() { var y = window.pageYOffset; drawStep(); window.scrollTo(0, y); }

  // ---------- submit ----------
  function hp() { var h = byId('tds-hp'); return h ? h.value : ''; }
  function doneView() {
    var ab = S.a.about || {};
    return '<div class="done">' + '<span class="dck">' + ic('check') + '</span><h3>Thank you' + (ab.owner ? ', ' + esc(String(ab.owner).split(' ')[0]) : '') + '! We&#39;ve got everything.</h3>' +
      '<p>Your dashboard setup for <b>' + esc(ab.business || 'your business') + '</b> is with our local team.</p>' +
      '<ol class="next"><li><b>1</b><div><h4>We review your setup</h4><p>We look over your answers, tools and photos.</p></div></li><li><b>2</b><div><h4>We reach out by email</h4><p>Usually within one business day, to set up a quick call or a demo.</p></div></li><li><b>3</b><div><h4>Your custom quote and timeline</h4><p>Built around the modules and connections you picked. No pressure.</p></div></li></ol>' +
      '<div class="dbtns"><a class="tds-btn tds-blue" href="/services">See all our services</a><button type="button" class="tds-btn tds-ghost" data-restart="1">Start a new setup</button></div>' +
      '<p class="hint">Need to change something? Email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a>.</p></div>';
  }
  function submit() {
    var btn = byId('tds-send'), msg = byId('tds-sendmsg'), ck = byId('tds-consent');
    if (!ck || !ck.checked) { msg.className = 'sendmsg bad'; msg.innerHTML = 'Please tick the box above so we can contact you.'; ck && ck.focus(); return; }
    if (S.up.some(function (u) { return u.st === 'up'; })) { msg.className = 'sendmsg'; msg.innerHTML = 'Your pictures are still uploading. One moment, then press Send again.'; return; }
    btn.disabled = true; btn.innerHTML = '<i class="spin"></i>Sending...'; msg.className = 'sendmsg'; msg.innerHTML = '';
    var body = JSON.stringify({ client: CL, session: S.sid, kind: 'answers', final: true, answers: payload(), hp: hp() });
    if (body.length > 390000) { btn.disabled = false; btn.innerHTML = ic('send') + 'Send my dashboard setup'; msg.className = 'sendmsg bad'; msg.innerHTML = 'That&#39;s a lot of text. Please shorten a few of the longer comments and try again.'; return; }
    fetch(C.api, { method: 'POST', headers: { 'content-type': 'application/json' }, body: body })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || 'http ' + r.status); return j; }); })
      .then(function () { S.done = 1; S.doneAt = Date.now(); save(true); ga('dash_setup_submit', { industry: industry() || 'none' }); drawStep(); go(STEPS.length - 1); })
      .catch(function () {
        btn.disabled = false; btn.innerHTML = ic('send') + 'Try sending again';
        msg.className = 'sendmsg bad'; msg.innerHTML = 'We couldn&#39;t send it just now. Your answers are saved on this device, so nothing is lost. Please try again in a few minutes, or email <a href="mailto:hello@threevillagelocal.com">hello@threevillagelocal.com</a>.';
      });
  }

  // ---------- modal: every integration ----------
  function drawModal() {
    var qs = byId('tds-msrch').value, cat = byId('tds-mcat').value, list = search(qs, cat), by = {};
    list.forEach(function (t) { (by[t[1]] = by[t[1]] || []).push(t); });
    var h = '';
    Object.keys(by).sort(function (a, b) { return a - b; }).forEach(function (ci) {
      h += '<h3>' + esc(C.cats[ci]) + ' <i>' + by[ci].length + '</i></h3>' + by[ci].map(function (t) {
        var on = isSel(t[0]);
        return '<div class="mrow">' + logo(t) + '<div><b>' + nw(t[0]) + '</b><p>' + esc(t[3]) + '</p><span class="cx cx-' + t[2] + '">' + esc(C.conn[t[2]]) + '</span></div><button type="button" class="' + (on ? 'on' : '') + '" data-tool="' + esc(t[0]) + '" aria-pressed="' + on + '">' + (on ? ic('check') + 'Added' : ic('plus') + 'Add') + '</button></div>';
      }).join('');
    });
    byId('tds-mlist').innerHTML = h || '<p class="empty">No match. Add it under &quot;Something else&quot; and we&#39;ll look into it.</p>';
  }
  var lastFocus = null;
  function openModal() {
    var m = byId('tds-modal'), sel = byId('tds-mcat');
    if (sel.options.length < 2) C.cats.forEach(function (c, i) { if (TOOLS.some(function (t) { return t[1] === i && t[2] !== 'B'; })) { var o = document.createElement('option'); o.value = i; o.textContent = c; sel.appendChild(o); } });
    lastFocus = document.activeElement; m.hidden = false; document.documentElement.classList.add('tds-lock'); drawModal();
    setTimeout(function () { byId('tds-msrch').focus(); }, 30); ga('dash_setup_all_integrations');
  }
  function closeModal() { byId('tds-modal').hidden = true; document.documentElement.classList.remove('tds-lock'); drawSel(); drawResults(); if (lastFocus && lastFocus.focus) lastFocus.focus(); }

  function toggleTool(n) {
    var T = A('integrations', {}); if (!T.tools) T.tools = {};
    if (T.tools[n]) delete T.tools[n]; else T.tools[n] = { need: '', note: '' };
    touch();
    if (!byId('tds-modal').hidden) drawModal();
    drawSel(); drawResults();
  }

  // ---------- colors from the logo ----------
  function hex2(n) { var s = Math.max(0, Math.min(255, Math.round(n))).toString(16); return s.length < 2 ? '0' + s : s; }
  function pullColors() {
    var u = S.up.filter(function (x) { return x.g === 'logo' && x.th; })[0]; if (!u) return;
    var img = new Image();
    img.onload = function () {
      var cv = document.createElement('canvas'); cv.width = 64; cv.height = 64;
      var x = cv.getContext('2d'); x.drawImage(img, 0, 0, 64, 64);
      var d = x.getImageData(0, 0, 64, 64).data, B = {};
      for (var i = 0; i < d.length; i += 4) {
        if (d[i + 3] < 200) continue;
        var r = d[i], g = d[i + 1], b = d[i + 2];
        if (Math.min(r, g, b) > 232) continue;   // skip white background
        var key = Math.floor(r / 40) + '-' + Math.floor(g / 40) + '-' + Math.floor(b / 40);
        var o = B[key] || (B[key] = { n: 0, r: 0, g: 0, b: 0 }); o.n++; o.r += r; o.g += g; o.b += b;
      }
      var arr = Object.keys(B).map(function (k) { var o = B[k]; return { n: o.n, r: o.r / o.n, g: o.g / o.n, b: o.b / o.n, sat: Math.max(o.r, o.g, o.b) / o.n - Math.min(o.r, o.g, o.b) / o.n }; });
      arr.sort(function (a, b) { return (b.n * (1 + b.sat / 90)) - (a.n * (1 + a.sat / 90)); });
      var pick = [];
      arr.forEach(function (c) { if (pick.length >= 3) return; if (pick.every(function (p) { return Math.abs(p.r - c.r) + Math.abs(p.g - c.g) + Math.abs(p.b - c.b) > 90; })) pick.push(c); });
      if (!pick.length) { flash('We couldn&#39;t find clear colors in that logo. Pick them with the swatches, or tap &quot;Help me pick colors&quot;.'); return; }
      set('brand.colors', pick.map(function (c) { return '#' + hex2(c.r) + hex2(c.g) + hex2(c.b); }));
      rerenderKeepScroll(); flash('Colors pulled from your logo. Tap any swatch to fine-tune it.'); ga('dash_setup_pull_colors');
    };
    img.src = u.th;
  }

  // ---------- CSV roster ----------
  function readCSV(f) {
    var fr = new FileReader();
    fr.onload = function () {
      var lines = String(fr.result || '').split(CR).join('').split(NL).filter(function (l) { return l.trim(); });
      if (!lines.length) return;
      var first = lines[0].toLowerCase(), start = first.indexOf('name') >= 0 || first.indexOf('email') >= 0 ? 1 : 0;
      var cols = start ? first.split(',').map(function (c) { return norm(c); }) : ['name', 'role', 'email'];
      var ci = function (w) { for (var i = 0; i < cols.length; i++) if (cols[i].indexOf(w) >= 0) return i; return -1; };
      var iN = ci('name'), iR = ci('role') >= 0 ? ci('role') : ci('title'), iE = ci('mail');
      if (iN < 0) iN = 0;
      var p = A('people', {}); if (!Array.isArray(p.roster)) p.roster = [];
      var n = 0;
      lines.slice(start, 200).forEach(function (l) {
        var c = l.split(',').map(function (x) { return x.split('"').join('').trim(); });
        var row = { id: 'r' + rid(8), name: (c[iN] || '').slice(0, 80), role: iR >= 0 ? matchRole(c[iR] || '') : '', email: iE >= 0 ? (c[iE] || '').slice(0, 120) : '' };
        if (row.name || row.email) { p.roster.push(row); n++; }
      });
      touch(); rerenderKeepScroll(); flash(n ? 'Added ' + n + ' people from your spreadsheet.' : 'We couldn&#39;t read anyone from that file. Columns should be name, role, email.');
    };
    fr.readAsText(f);
  }
  function matchRole(s) {
    var t = norm(s); if (!t) return '';
    var m = ''; C.roles.forEach(function (r) { if (!m && (norm(r[1]).indexOf(t) >= 0 || t.indexOf(norm(r[1]).split(' ')[0]) >= 0)) m = r[1]; });
    return m;
  }

  // ---------- events ----------
  R.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('button, a[data-go], [data-modal]') : null;
    if (!t || !R.contains(t)) return;
    var d = t.dataset || {};
    if (d.ask != null) { e.preventDefault(); ga('dash_setup_ask', { step: STEPS[S.step].id }); if (window.tvaAsk) window.tvaAsk(d.ask); else if (window.tvaOpen) window.tvaOpen(); else location.href = 'mailto:hello@threevillagelocal.com?subject=Dashboard%20setup%20question'; return; }
    if (d.go === 'start') { go(S.done ? STEPS.length - 1 : S.step); var w = byId('tds-wiz'); window.scrollTo({ top: w.getBoundingClientRect().top + window.pageYOffset - 86, behavior: 'smooth' }); if (!S.started) { S.started = new Date().toISOString(); save(); } ga('dash_setup_start'); return; }
    if (d.resume) { var w2 = byId('tds-wiz'); window.scrollTo({ top: w2.getBoundingClientRect().top + window.pageYOffset - 86, behavior: 'smooth' }); return; }
    if (d.restart) { if (!confirm('Start a brand new setup? This clears the answers saved on this device.')) return; try { localStorage.removeItem(KEY); } catch (x) {} S = { v: 1, sid: 'ds-' + rid(24), step: 0, a: {}, up: [], touched: 0, done: 0 }; FILES = {}; byId('tds-resume').hidden = true; prevSoon(); go(0); return; }
    if (d.step != null) { go(+d.step); return; }
    if (d.nav === 'next' || d.nav === 'skip') { if (d.nav === 'skip') ga('dash_setup_skip', { step: STEPS[S.step].id }); go(S.step + 1); return; }
    if (d.nav === 'back') { go(S.step - 1); return; }
    if (d.later) { save(true); flash(ic('check') + '<span><b>Saved.</b> Come back to this page on this device and you&#39;ll pick up right where you left off.</span>'); return; }
    if (d.allsteps) { var ml = byId('tds-mlist2'); ml.hidden = !ml.hidden; t.setAttribute('aria-expanded', String(!ml.hidden)); return; }
    if (d.modal === 'open') { openModal(); return; }
    if (d.modal === 'close') { closeModal(); return; }
    if (d.tool != null) { toggleTool(d.tool); return; }
    if (d.need) { var it = t.closest('[data-it]').getAttribute('data-it'), T = get('integrations.tools'); if (T && T[it]) { T[it].need = T[it].need === d.need ? '' : d.need; touch(); drawSel(); } return; }
    if (d.rm) { S.up = S.up.filter(function (u) { return u.id !== d.rm; }); var z = t.closest('.th'); delete FILES[d.rm]; touch(); if (z) z.remove(); redrawUp('team'); return; }
    if (d.rt) { var u2 = S.up.filter(function (u) { return u.id === d.rt; })[0]; if (u2) upload(u2); return; }
    if (d.radd) { var p = A('people', {}); if (!Array.isArray(p.roster)) p.roster = []; p.roster.push({ id: 'r' + rid(8), name: '', role: '', email: '' }); touch(); byId('tds-roster').insertAdjacentHTML('beforeend', rosterRow(p.roster[p.roster.length - 1], p.roster.length - 1)); var ins = byId('tds-roster').lastElementChild.querySelector('input.in'); if (ins) ins.focus(); return; }
    if (d.rdel != null) { var pr = A('people', {}); var row = pr.roster.splice(+d.rdel, 1)[0]; if (row) S.up = S.up.filter(function (u) { return !(u.g === 'team' && u.ref === row.id); }); touch(); rerenderKeepScroll(); return; }
    if (d.accr) { accRole = d.accr; rerenderKeepScroll(); return; }
    if (d.acc) { var ac = access()[accRole], ix = ac.indexOf(d.acc); if (ix >= 0) ac.splice(ix, 1); else ac.push(d.acc); touch(); t.classList.toggle('on', ix < 0); t.setAttribute('aria-pressed', String(ix < 0)); var tb = R.querySelector('[data-accr="' + accRole + '"] i'); if (tb) tb.textContent = ac.length; return; }
    if (d.accreset) { access()[accRole] = (C.access[accRole] || []).slice(); touch(); rerenderKeepScroll(); return; }
    if (d.d) { var sp = t.closest('.stp'), ip = sp.querySelector('input'), nv = Math.max(0, Math.min(500, (+ip.value || 0) + (+d.d))); ip.value = nv; setRole(sp.getAttribute('data-role'), nv, sp); return; }
    if (d.sugall) { var M = A('modules', {}); (C.sug[industry()] || []).forEach(function (m) { if (!M[m]) M[m] = {}; if (!M[m].p || M[m].p === 'unsure') M[m].p = 'must'; }); touch(); rerenderKeepScroll(); flash('Suggested modules marked must-have. Change any of them below.'); return; }
    if (d.cadd) { var bc = A('brand', {}); if (!Array.isArray(bc.colors)) bc.colors = []; bc.colors.push(['#13294b', '#1d5fbf', '#ffc53d', '#16a37a'][bc.colors.length % 4]); touch(); rerenderKeepScroll(); return; }
    if (d.cdel != null) { S.a.brand.colors.splice(+d.cdel, 1); touch(); rerenderKeepScroll(); return; }
    if (d.pull) { pullColors(); return; }
    if (t.id === 'tds-send') { submit(); return; }
    if (t.classList.contains('chip')) { chipClick(t); return; }
    if (t.classList.contains('cn')) { openNote(t); return; }
    if (t.classList.contains('nd')) { var cnb = t.closest('.cnote'); cnb.hidden = true; var grp = cnb.previousElementSibling; markNotes(grp); return; }
  });
  function setRole(id, n, sp) {
    set('people.roles.' + id, n);
    var role = sp.closest('.role'); if (role) role.classList.toggle('on', n > 0);
    var s2 = byId('tds-sum'); if (s2) s2.innerHTML = sumText();
    clearTimeout(setRole._t); setRole._t = setTimeout(function () { var tabs = R.querySelector('.acct'); if (tabs) { var y = window.pageYOffset; var f = document.activeElement && document.activeElement.getAttribute('data-rc'); drawStep(); window.scrollTo(0, y); if (f) { var el = R.querySelector('[data-rc="' + f + '"]'); if (el) el.focus(); } } }, 900);
  }
  function chipClick(t) {
    var grp = t.closest('.chips'), k = grp.getAttribute('data-k'), multi = grp.getAttribute('data-m') === '1', v = t.getAttribute('data-v');
    if (multi) { var arr = (get(k) || []).slice(), ix = arr.indexOf(v); if (ix >= 0) arr.splice(ix, 1); else arr.push(v); set(k, arr); }
    else set(k, get(k) === v ? '' : v);
    var cur = get(k);
    [].forEach.call(grp.querySelectorAll('.cw'), function (w) {
      var b = w.querySelector('.chip'), on = multi ? (cur || []).indexOf(b.getAttribute('data-v')) >= 0 : cur === b.getAttribute('data-v');
      w.classList.toggle('on', on); b.setAttribute('aria-pressed', String(on));
    });
    var mod = grp.closest('.mod'); if (mod) { mod.classList.toggle('on', cur === 'must' || cur === 'nice'); mod.classList.toggle('off', cur === 'no'); }
    if (v === UNS && (multi ? (cur || []).indexOf(UNS) >= 0 : cur === UNS)) flash(ic('help') + '<span>No problem. We&#39;ll help you decide on our call, or <button type="button" class="lnk" data-ask="Can you help me decide: ' + esc(STEPS[S.step].t) + '?">ask our helper now</button>.</span>');
    if (grp.getAttribute('data-rr')) rerenderKeepScroll();
    else drawFrame();
  }
  function openNote(t) {
    var grp = t.closest('.chips'), k = grp.getAttribute('data-k'), v = t.getAttribute('data-v'), box = grp.nextElementSibling;
    if (!box || !box.classList.contains('cnote')) return;
    var nk = noteKey(k, v);
    box.innerHTML = '<label><span>' + ic('edit') + 'Note on <b>' + esc(v) + '</b></span><span class="nrow"><input class="in" data-nk="' + esc(nk) + '" value="' + esc(notes()[nk] || '') + '" maxlength="500" placeholder="Add details, like how often or who handles it"><button type="button" class="nd tds-btn tds-blue sm">Done</button></span></label>';
    box.hidden = false; box.querySelector('input').focus();
  }
  function markNotes(grp) { var k = grp.getAttribute('data-k'); [].forEach.call(grp.querySelectorAll('.cw'), function (w) { w.classList.toggle('hn', hasNote(k, w.querySelector('.chip').getAttribute('data-v'))); }); }

  R.addEventListener('input', function (e) {
    var t = e.target, d = t.dataset || {};
    if (d.k && t.type !== 'checkbox' && t.type !== 'file') { set(d.k, t.value); if (d.k.indexOf('about.') === 0 || d.k.indexOf('brand.') === 0) prevSoon(); drawFrameSoon(); return; }
    if (d.nk) { notes()[d.nk] = t.value; touch(); return; }
    if (d.itn) { var it = t.closest('[data-it]').getAttribute('data-it'), T = get('integrations.tools'); if (T && T[it]) { T[it].note = t.value; touch(); } return; }
    if (d.ci != null) { S.a.brand.colors[+d.ci] = t.value; t.parentNode.style.background = t.value; var cd = t.parentNode.parentNode.querySelector('code'); if (cd) cd.textContent = t.value.toUpperCase(); touch(); return; }
    if (d.rc) { var sp = t.closest('.stp'); setRole(d.rc, Math.max(0, Math.min(500, +t.value || 0)), sp); return; }
    if (t.id === 'tds-isrch') { drawResults(); return; }
    if (t.id === 'tds-msrch') { drawModal(); return; }
  });
  var dfT = 0; function drawFrameSoon() { clearTimeout(dfT); dfT = setTimeout(function () { var a = document.activeElement; drawRailOnly(); if (a && a.focus && document.activeElement !== a) a.focus(); }, 500); }
  function drawRailOnly() { var y = window.pageYOffset; var top = byId('tds-top'); var keepH = top.querySelector('h2') ? 1 : 0; drawFrame(); window.scrollTo(0, y); return keepH; }
  R.addEventListener('change', function (e) {
    var t = e.target, d = t.dataset || {};
    if (t.type === 'checkbox' && d.k) { set(d.k, t.checked); return; }
    if (t.tagName === 'SELECT' && d.k) { set(d.k, t.value); return; }
    if (t.id === 'tds-consent') { S.consent = t.checked; save(); return; }
    if (t.id === 'tds-mcat') { drawModal(); return; }
    if (d.up) { var z = t.closest('.up'), max = z ? +z.getAttribute('data-max') : 1; addFiles(t.files, d.up, d.ref || '', d.ref ? 1 : max); t.value = ''; return; }
    if (d.csv) { if (t.files[0]) readCSV(t.files[0]); t.value = ''; return; }
  });
  R.addEventListener('dragover', function (e) { var z = e.target.closest && e.target.closest('.drop'); if (z) { e.preventDefault(); z.classList.add('over'); } });
  R.addEventListener('dragleave', function (e) { var z = e.target.closest && e.target.closest('.drop'); if (z) z.classList.remove('over'); });
  R.addEventListener('drop', function (e) {
    var z = e.target.closest && e.target.closest('.drop'); if (!z) return; e.preventDefault(); z.classList.remove('over');
    var up = z.closest('.up'); addFiles(e.dataTransfer.files, up.getAttribute('data-g'), up.getAttribute('data-ref') || '', +up.getAttribute('data-max'));
  });
  byId('tds-modal').addEventListener('click', function (e) { if (e.target.id === 'tds-modal') closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !byId('tds-modal').hidden) closeModal(); });

  // ---------- start ----------
  var res = byId('tds-resume');
  if (S.done) {
    res.hidden = false; res.innerHTML = ic('check') + '<p><b>You&#39;ve sent your setup' + (S.a.about && S.a.about.business ? ' for ' + esc(S.a.about.business) : '') + '.</b> Our team will be in touch by email.</p><button type="button" class="lnk" data-restart="1">Start a new one</button>';
  } else if (RESUMED) {
    var nm = S.a.about && S.a.about.owner ? ', ' + String(S.a.about.owner).split(' ')[0] : '';
    res.hidden = false; res.innerHTML = ic('save') + '<p><b>Welcome back' + esc(nm) + '!</b> Your answers are saved. You&#39;re on step ' + (S.step + 1) + ', ' + esc(STEPS[S.step].t) + '.</p><button type="button" class="tds-btn tds-blue sm" data-resume="1">Continue</button><button type="button" class="lnk" data-restart="1">Start over</button>';
    var sb = R.querySelector('[data-go="start"]'); if (sb) sb.innerHTML = 'Continue my setup' + ic('arrow');
  }
  drawStep(); prevSoon();
  if (S.saved) savedMsg(true);
  window.addEventListener('pagehide', function () { save(true); });
})();
