(function () {
  function normalize(value) {
    return String(value || "")
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function fieldText(item, key) {
    var value = item[key];
    if (Array.isArray(value)) return value.join(" ");
    return value || "";
  }

  function scoreItem(item, terms) {
    var title = normalize(item.title);
    var summary = normalize(item.summary);
    var authors = normalize(fieldText(item, "authors"));
    var tags = normalize(fieldText(item, "tags") + " " + fieldText(item, "categories") + " " + fieldText(item, "projects"));
    var body = normalize([item.content, item.section, item.type, item.date].join(" "));
    var haystack = [title, summary, authors, tags, body].join(" ");
    var score = 0;

    for (var i = 0; i < terms.length; i += 1) {
      var term = terms[i];
      if (!haystack.includes(term)) return 0;
      if (title.includes(term)) score += 10;
      if (summary.includes(term)) score += 5;
      if (authors.includes(term)) score += 4;
      if (tags.includes(term)) score += 4;
      if (body.includes(term)) score += 1;
    }

    return score;
  }

  function renderResult(item) {
    var article = document.createElement("article");
    article.className = "search-result";

    var title = document.createElement("h2");
    var link = document.createElement("a");
    link.href = item.permalink;
    link.textContent = item.title;
    title.appendChild(link);

    var meta = document.createElement("p");
    meta.className = "search-meta";
    meta.textContent = [item.section, item.date].filter(Boolean).join(" / ");

    var summary = document.createElement("p");
    summary.textContent = item.summary || "";

    article.appendChild(title);
    article.appendChild(meta);
    if (summary.textContent) article.appendChild(summary);
    return article;
  }

  function initSearch() {
    var form = document.getElementById("site-search");
    if (!form) return;

    var input = document.getElementById("search-query");
    var status = document.getElementById("search-status");
    var results = document.getElementById("search-results");
    var indexUrl = form.getAttribute("data-index-url");
    var index = [];

    function runSearch(query, updateUrl) {
      var terms = normalize(query).split(/\s+/).filter(Boolean);
      results.innerHTML = "";

      if (updateUrl) {
        var next = terms.length ? "?q=" + encodeURIComponent(query) : window.location.pathname;
        window.history.replaceState(null, "", next);
      }

      if (!terms.length) {
        status.textContent = "Enter a search term.";
        return;
      }

      var matches = index
        .map(function (item) {
          return { item: item, score: scoreItem(item, terms) };
        })
        .filter(function (entry) {
          return entry.score > 0;
        })
        .sort(function (a, b) {
          if (b.score !== a.score) return b.score - a.score;
          return String(b.item.date || "").localeCompare(String(a.item.date || ""));
        })
        .slice(0, 30);

      status.textContent = matches.length + (matches.length === 1 ? " result" : " results");
      matches.forEach(function (entry) {
        results.appendChild(renderResult(entry.item));
      });
    }

    fetch(indexUrl, { credentials: "same-origin" })
      .then(function (response) {
        if (!response.ok) throw new Error("Search index unavailable");
        return response.json();
      })
      .then(function (data) {
        index = Array.isArray(data) ? data : [];
        var params = new URLSearchParams(window.location.search);
        var initial = params.get("q") || "";
        input.value = initial;
        runSearch(initial, false);
      })
      .catch(function () {
        status.textContent = "Search index unavailable.";
      });

    var timer = null;
    input.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        runSearch(input.value, true);
      }, 120);
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      runSearch(input.value, true);
    });
  }

  document.addEventListener("DOMContentLoaded", initSearch);
})();
