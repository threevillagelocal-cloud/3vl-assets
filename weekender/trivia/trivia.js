/* Three Village Trivia: one question a day, same for everyone (New York date). */
(function () {
  var box = document.getElementById('tvl-trivia');
  if (!box) return;
  var SRC = box.getAttribute('data-src') || 'trivia.json';
  var LS = 'tvlTrivia';
  function store() { try { return JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(LS, JSON.stringify(s)); } catch (e) {} }
  function nyDate(d) { // YYYY-MM-DD in New York
    var p = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', year: 'numeric', month: '2-digit', day: '2-digit' }).format(d || new Date());
    return p;
  }
  function dayNum(iso) { return Math.round(Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10)) / 864e5); }
  function ga(n, p) { try { window.gtag && gtag('event', n, p || {}); } catch (e) {} }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function untilMidnight() {
    var now = new Date(), ny = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
    var mins = (24 * 60) - (ny.getHours() * 60 + ny.getMinutes());
    var h = Math.floor(mins / 60), m = mins % 60;
    return (h ? h + 'h ' : '') + m + 'm';
  }

  function render(data) {
    var today = nyDate(), n = dayNum(today) - dayNum(data.start);
    var list = data.q, idx = ((n % list.length) + list.length) % list.length, q = list[idx];
    var s = store(), done = s.day === today ? s.pick : null;
    var streak = s.streak || 0;
    if (s.last && dayNum(today) - dayNum(s.last) > 1) streak = 0; // missed a day

    var letters = ['A', 'B', 'C', 'D'];
    var h = '<div class="tt-head"><span class="tt-badge">Three Village Trivia</span><span class="tt-day">Question of the day · #' + (n + 1) + '</span>' +
      (streak ? '<span class="tt-streak" title="Days in a row answered right">' + streak + ' day streak</span>' : '') + '</div>' +
      '<p class="tt-q">' + esc(q.q) + '</p><div class="tt-opts">';
    q.o.forEach(function (o, i) {
      var cls = 'tt-o';
      if (done !== null) { if (i === q.a) cls += ' ok'; else if (i === done) cls += ' no'; else cls += ' dim'; }
      h += '<button class="' + cls + '" data-i="' + i + '"' + (done !== null ? ' disabled' : '') + '><b>' + letters[i] + '</b><span>' + esc(o) + '</span></button>';
    });
    h += '</div>';
    if (done !== null) {
      var right = done === q.a;
      h += '<div class="tt-res ' + (right ? 'ok' : 'no') + '"><strong>' + (right ? 'You got it!' : 'Not quite. The answer is ' + esc(q.o[q.a]) + '.') + '</strong>' +
        '<p>' + esc(q.f) + '</p><div class="tt-foot"><span class="tt-next">Next question in ' + untilMidnight() + '</span>' +
        '<button class="tt-share">Challenge a neighbor</button></div></div>';
    } else {
      h += '<p class="tt-hint">Tap an answer. A new question every day.</p>';
    }
    box.innerHTML = h;

    box.querySelectorAll('.tt-o:not([disabled])').forEach(function (b) {
      b.addEventListener('click', function () {
        var pick = +b.getAttribute('data-i'), right = pick === q.a, st = store();
        var prevStreak = (st.last && dayNum(today) - dayNum(st.last) === 1) ? (st.streak || 0) : 0;
        st.day = today; st.pick = pick;
        st.streak = right ? prevStreak + 1 : 0; st.last = right ? today : st.last;
        st.played = (st.played || 0) + 1; st.right = (st.right || 0) + (right ? 1 : 0);
        save(st);
        ga('trivia_answer', { trivia_q: idx + 1, correct: right ? 1 : 0 });
        render(data);
        box.classList.add(right ? 'tt-pop' : 'tt-shake');
        setTimeout(function () { box.classList.remove('tt-pop', 'tt-shake'); }, 700);
      });
    });
    var sh = box.querySelector('.tt-share');
    if (sh) sh.addEventListener('click', function () {
      var txt = 'Three Village Trivia: ' + q.q + ' Think you know? Play today\'s question at threevillagelocal.com';
      ga('trivia_share');
      if (navigator.share) { navigator.share({ title: 'Three Village Trivia', text: txt, url: 'https://www.threevillagelocal.com/' }).catch(function () {}); }
      else if (navigator.clipboard) { navigator.clipboard.writeText(txt); sh.textContent = 'Copied! Paste it to a friend'; }
    });
  }

  if (window.TVL_TRIVIA) render(window.TVL_TRIVIA);
  else fetch(SRC).then(function (r) { return r.json(); }).then(render).catch(function () { box.style.display = 'none'; });
})();
