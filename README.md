# ✈️ Automated Flight Booking System  

This project automates the process of searching and booking flights on [MakeMyTrip](https://www.makemytrip.com) using **Python** and **Playwright**.  
It was built as part of an assignment to demonstrate **web automation**, **form filling**, and **dynamic web handling**.  

---

## 🚀 Features  
- Opens MakeMyTrip automatically in a browser  
- Fills in **source**, **destination**, and **travel date**  
- Searches for available flights  
- Extracts flight details (airline, timings, price, etc.)  
- (Optional) Can be extended to proceed with booking  

---

## 🛠️ Tech Stack  
- **Python 3.12+**  
- [Microsoft Playwright](https://playwright.dev/python/) for browser automation  
- Git for version control  

---

## 📂 Project Structure  

Automated-Flight-Booking-System/
│── main.py # Main automation script
│── utils/ # Helper functions (date formatting, configs, etc.)
│── packages/ # Installed dependencies (ignored in GitHub)
│── README.md # Project documentation
│── .gitignore # Git ignore file

yaml
Copy code

---

## ⚡ Installation & Setup  

1. Clone this repository:  
   ```bash
   git clone https://github.com/PushkargithubCSE/Automated-Flight-Booking-System.git
   cd Automated-Flight-Booking-System
Create a virtual environment (recommended):

bash
Copy code
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate   # On Mac/Linux
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Install Playwright browsers:

bash
Copy code
playwright install
▶️ Usage
Run the script with your travel details:

bash
Copy code
python main.py
The script will:

Launch a browser

Open MakeMyTrip

Fill in the details (source, destination, date)

Search and display available flights

📝 Notes
Ensure you have a stable internet connection.

Website elements (selectors) may change, so minor updates might be needed.

Do not push large packages/ folder — use .gitignore.

📌 Future Improvements
Save search results to a CSV/Excel file

Add user login for booking confirmation

Support for round trips and multiple passengers

👨‍💻 Author
Pushkar Chandra
GitHub: PushkargithubCSE
