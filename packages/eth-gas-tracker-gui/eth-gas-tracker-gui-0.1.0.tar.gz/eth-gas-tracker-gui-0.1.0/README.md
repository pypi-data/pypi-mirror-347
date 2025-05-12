# ⛽ ETH Gas Tracker GUI (No API Key Required)

A simple and user-friendly desktop application (GUI) to track Ethereum gas prices in real-time.  
Built using Python and Tkinter with data fetched from the public API [ethgas.watch](https://ethgas.watch), so no API key is required.

---

## 🚀 Features

- 🟢 **Real-time Gas Price Fetching**  
  Get the latest Ethereum gas fees for Safe, Propose (Normal), and Fast speeds — displayed in Gwei.

- 💾 **Gas History Logging**  
  Every time you fetch gas prices, the result is saved in a local file (`gas_history.json`) for tracking.

- 📊 **Average Summary Calculation**  
  View a summary of average gas prices from your saved history.

- 🧩 **No API Key Needed**  
  Uses the public API from [ethgas.watch](https://ethgas.watch) — no sign-up or token required.

- 🖥️ **Desktop App with GUI (Tkinter)**  
  Intuitive interface built using Tkinter — no command line required to use it.

---

## 🧰 Requirements

- Python 3.x
- [requests](https://pypi.org/project/requests/) (install via pip)
- tkinter (already included in most Python distributions)

---

## 🛠️ Installation

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/gendisnanaya/ETH-Gas-Tracker-GUI.git

