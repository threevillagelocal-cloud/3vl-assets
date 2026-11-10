/* Three Village Trivia (owner 11/10/2026): a round of questions played one after another with a score at the end.
   The newest round whose start date (New York) has arrived is shown. Launch round = 10, then a new 5 every Monday.
   Progress per round is saved in this browser (localStorage). GA4: trivia_answer, trivia_done, trivia_share. */
(function () {
  var box = document.getElementById('tvl-trivia');
  if (!box) return;
  var SRC = box.getAttribute('data-src') || 'trivia.json';
  var LS = 'tvlTrivia2';
  function store() { try { return JSON.parse(localStorage.getItem(LS)) || {}; } catch (e) { return {}; } }
  function save(s) { try { localStorage.setItem(LS, JSON.stringify(s)); } catch (e) {} }
  function nyDate() { return new Intl.DateTimeFormat('en-CA', { timeZone: 'America/New_York', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date()); }
  function ga(n, p) { try { window.gtag && gtag('event', n, p || {}); } catch (e) {} }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var L = ['A', 'B', 'C', 'D'];

  function nextMonday() {
    var ny = new Date(new Date().toLocaleString('en-US', { timeZone: 'America/New_York' }));
    var d = (8 - ny.getDay()) % 7 || 7; ny.setDate(ny.getDate() + d);
    return ny.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
  }

  function start(data) {
    var today = nyDate(), rounds = (data.rounds || []).filter(function (r) { return r.start <= today; });
    if (!rounds.length) { box.style.display = 'none'; return; }
    var R = rounds[rounds.length - 1], key = R.start, N = R.q.length;
    var s = store(); if (!s[key]) s[key] = { picks: [], seen: 0 };
    var st = s[key];

    function score() { return st.picks.reduce(function (n, p, i) { return n + (p === R.q[i].a ? 1 : 0); }, 0); }

    function head(i) {
      var pct = Math.round((Math.min(i, N) / N) * 100);
      return '<div class="tt-head"><span class="tt-badge">Three Village Trivia</span><span class="tt-day">' + esc(R.title || 'This week') + '</span>' +
        (i < N ? '<span class="tt-count">Question ' + (i + 1) + ' of ' + N + '</span>' : '') +
        '</div><div class="tt-bar"><i style="width:' + pct + '%"></i></div>';
    }

    function render() {
      var i = st.seen;                      // the question on screen
      if (i >= N) return done();
      var q = R.q[i], pick = st.picks[i], answered = pick !== undefined;
      var h = head(i) + '<p class="tt-q">' + esc(q.q) + '</p><div class="tt-opts">';
      q.o.forEach(function (o, k) {
        var cls = 'tt-o';
        if (answered) { if (k === q.a) cls += ' ok'; else if (k === pick) cls += ' no'; else cls += ' dim'; }
        h += '<button class="' + cls + '" data-i="' + k + '"' + (answered ? ' disabled' : '') + '><b>' + L[k] + '</b><span>' + esc(o) + '</span></button>';
      });
      h += '</div>';
      if (answered) {
        var right = pick === q.a;
        h += '<div class="tt-res ' + (right ? 'ok' : 'no') + '"><strong>' + (right ? 'You got it!' : 'Not quite. The answer is ' + esc(q.o[q.a]) + '.') + '</strong><p>' + esc(q.f) + '</p>' +
          '<div class="tt-foot"><span class="tt-next">Score so far: ' + score() + ' of ' + (i + 1) + '</span><button class="tt-share tt-go">' + (i + 1 < N ? 'Next question &rarr;' : 'See my score &rarr;') + '</button></div></div>';
      } else {
        h += '<p class="tt-hint">Tap an answer. ' + N + ' questions this round, new ones every Monday.</p>';
      }
      box.innerHTML = h;
      box.querySelectorAll('.tt-o:not([disabled])').forEach(function (b) {
        b.addEventListener('click', function () {
          var p = +b.getAttribute('data-i'); st.picks[i] = p; save(s);
          ga('trivia_answer', { trivia_round: key, trivia_q: i + 1, correct: p === q.a ? 1 : 0 });
          render();
          box.classList.add(p === q.a ? 'tt-pop' : 'tt-shake'); setTimeout(function () { box.classList.remove('tt-pop', 'tt-shake'); }, 700);
        });
      });
      var go = box.querySelector('.tt-go');
      if (go) go.addEventListener('click', function () { st.seen = i + 1; save(s); render(); if (box.getBoundingClientRect().top < 0) box.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    }

    function done() {
      var sc = score(), msg = sc === N ? 'Perfect score! You really know Three Village.' : sc >= N * 0.7 ? 'Nice work, neighbor!' : sc >= N * 0.4 ? 'Not bad! Now you know a little more about home.' : 'Now you know a lot more about Three Village!';
      if (!st.reported) { ga('trivia_done', { trivia_round: key, score: sc, of: N }); st.reported = 1; save(s); }
      var h = head(N) + '<div class="tt-done"><div class="tt-score"><b>' + sc + '</b><span>out of ' + N + '</span></div><div><p class="tt-q" style="margin:0 0 6px">' + msg + '</p>' +
        '<p class="tt-hint" style="margin:0">New questions every Monday. Next round: ' + nextMonday() + '.</p></div></div>' +
        '<div class="tt-foot" style="margin-top:14px"><button class="tt-again">Review my answers</button><button class="tt-share">Challenge a neighbor</button></div>';
      box.innerHTML = h;
      box.querySelector('.tt-again').addEventListener('click', function () { st.seen = 0; st.review = 1; save(s); renderReview(0); });
      box.querySelector('.tt-share').addEventListener('click', function () {
        var txt = 'I got ' + sc + ' out of ' + N + ' on Three Village Trivia! Think you can beat me?';
        ga('trivia_share', { score: sc });
        if (navigator.share) navigator.share({ title: 'Three Village Trivia', text: txt, url: 'https://www.threevillagelocal.com/' }).catch(function () {});
        else if (navigator.clipboard) { navigator.clipboard.writeText(txt + ' https://www.threevillagelocal.com/'); this.textContent = 'Copied! Paste it to a friend'; }
      });
    }

    function renderReview(i) {   // step back through answered questions, then return to the score
      st.seen = i; save(s);
      if (i >= N) { st.seen = N; save(s); return done(); }
      render();
    }

    render();
  }

  if (window.TVL_TRIVIA) start(window.TVL_TRIVIA);
  else fetch(SRC).then(function (r) { return r.json(); }).then(start).catch(function () { box.style.display = 'none'; });
})();
