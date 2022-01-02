// const endpoint = "http://localhost:8000/";
const endpoint = "https://dfk-transaction-tracker-app-mlienhkuya-uc.a.run.app/"
const walletAddress = document.getElementById("wallet-address").value;

poll();

function poll() {
  fetch(`${endpoint}wallet_address?wallet_address=${walletAddress}`)
    .then(response => response.json())
    .then(json => {
      if (json["status"] === "success") {
        window.location.replace(`${endpoint}transactions?wallet_address=${walletAddress}&page=1`);
      } else if (json["status"] === "in_progress") {
        setTimeout(poll, 3000);
      }
    });
}
