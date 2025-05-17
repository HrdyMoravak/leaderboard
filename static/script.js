document.addEventListener("DOMContentLoaded", function () {
  const leaderboard = document.getElementById("leaderboard");
  const searchInput = document.getElementById("searchInput");

  let allPlayers = []; // sem uložíme všechna data

  function renderLeaderboard(filter = "") {
    leaderboard.innerHTML = "";
  
    const filtered = allPlayers
      .filter(([player]) => player.toLowerCase().includes(filter.toLowerCase()))
      .sort((a, b) => b[1] - a[1]);
  
      let displayRank = 0;       // skutečné pořadí, které se vypisuje
      let lastScore = null;      // poslední skóre pro porovnání
      
      filtered.forEach(([player, score], index) => {
        if (score !== lastScore) {
          displayRank++;         // zvyš pořadí jen když skóre je jiné než předchozí
          lastScore = score;
        }
        
        const entry = document.createElement("div");
        entry.textContent = `${displayRank}. ${player}: ${score}`;
      
        if (displayRank === 1) {
          entry.classList.add("gold");
        } else if (displayRank === 2) {
          entry.classList.add("silver");
        } else if (displayRank === 3) {
          entry.classList.add("bronze");
        }
      
        leaderboard.appendChild(entry);
      });
      
  
    if (filtered.length === 0) {
      leaderboard.textContent = "Žádný hráč neodpovídá hledání.";
    }
  }
  

  fetch("/api/scores")
      .then(response => {
          if (!response.ok) throw new Error(`Chyba při načítání dat: ${response.status}`);
          return response.json();
      })
      .then(data => {
          allPlayers = Object.entries(data);
          renderLeaderboard();
      })
      .catch(error => {
          console.error("⚠️ Chyba:", error);
          leaderboard.textContent = "Nepodařilo se načíst skóre.";
      });

  searchInput.addEventListener("input", () => {
      renderLeaderboard(searchInput.value);
  });
});
