(function () {
  var chips = document.querySelectorAll(".chip");
  var query = document.getElementById("q");
  if (!query) { return; }
  var filter = "all";
  function apply() {
    var text = query.value.trim().toLowerCase();
    document.querySelectorAll("details.inv").forEach(function (row) {
      var visible = (filter === "all" || row.dataset.status === filter) && (!text || row.dataset.search.indexOf(text) !== -1);
      row.hidden = !visible;
    });
  }
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      filter = chip.dataset.f;
      chips.forEach(function (other) { other.setAttribute("aria-pressed", String(other === chip)); });
      apply();
    });
  });
  query.addEventListener("input", apply);
})();
