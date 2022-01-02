const walletAddress = document.getElementById("wallet-address").value;

poll();

function poll() {
  fetch(`http://localhost:8000/wallet_address?wallet_address=${walletAddress}`)
    .then(response => response.json())
    .then(json => {
      if (json["status"] === "success") {
        window.location.replace("http://localhost:8000/transactions?page=1");
      } else if (json["status"] === "in_progress") {
        setTimeout(poll, 3000);
      }
    });
}
