// Adresa contractului (înlocuiește cu adresa reală după deploy)
const contractAddress = "0xYourContractAddress";

// ABI-ul contractului (trebuie copiat din Remix după deploy)
const contractABI = [
  {
    "constant": false,
    "inputs": [{ "name": "to", "type": "address" }, { "name": "amount", "type": "uint256" }],
    "name": "mint",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [{ "name": "from", "type": "address" }, { "name": "amount", "type": "uint256" }],
    "name": "burn",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
];

let provider;
let signer;
let contract;

// Funcție pentru conectare la MetaMask
async function connectEthereumWallet() {
  if (window.ethereum) {
    try {
      provider = new ethers.BrowserProvider(window.ethereum);
      await provider.send("eth_requestAccounts", []);
      signer = await provider.getSigner();
      contract = new ethers.Contract(contractAddress, contractABI, signer);
      document.getElementById("status").innerText = `Connected: ${await signer.getAddress()}`;
      console.log("✅ MetaMask connected:", await signer.getAddress());
    } catch (error) {
      console.error("❌ User rejected connection:", error);
      alert("MetaMask connection denied.");
    }
  } else {
    alert("❌ MetaMask not detected. Please install it!");
  }
}

// Funcție pentru a obține balanța ETH
async function getBalance() {
  if (!window.ethereum) {
    alert("MetaMask not detected!");
    return;
  }
  
  const provider = new ethers.BrowserProvider(window.ethereum);
  const signer = await provider.getSigner();
  const balance = await provider.getBalance(await signer.getAddress());

  document.getElementById("balance").innerText = `Balance: ${ethers.formatEther(balance)} ETH`;
}

// Funcție pentru a mina token-uri
async function mintTokens() {
  if (!contract) {
    alert("Please connect your wallet first!");
    return;
  }
  let amount = document.getElementById("amount").value;
  fetch("http://127.0.0.1:5000/mint", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ to: await signer.getAddress(), amount: amount }),
  })
    .then(response => response.json())
    .then(data => alert(`Minted successfully! TX: ${data.tx_hash}`))
    .catch(error => console.error("Error:", error));
}

// Funcție pentru a arde token-uri
async function burnTokens() {
  if (!contract) {
    alert("Please connect your wallet first!");
    return;
  }
  let amount = document.getElementById("amount").value;
  fetch("http://127.0.0.1:5000/burn", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ from: await signer.getAddress(), amount: amount }),
  })
    .then(response => response.json())
    .then(data => alert(`Burned successfully! TX: ${data.tx_hash}`))
    .catch(error => console.error("Error:", error));
}
