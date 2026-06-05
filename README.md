# 💰 WealthAdvisor AI — Intelligent Wealth Management Assistant using LangGraph

WealthAdvisor AI is an advanced AI-powered Wealth Management Assistant built using **LangGraph, FastAPI, Alpha Vantage API, Yahoo Finance, and LLMs**.

The system can analyze stocks, evaluate portfolios, calculate SIP returns, assess investor risk profiles, and generate retirement planning recommendations.

---

# 🚀 Features

## ✅ Real-Time Stock Analysis

- Analyze live stock prices
- Fetch market data using Alpha Vantage API
- Retrieve company fundamentals using Yahoo Finance
- Generate AI-powered investment insights

## ✅ SIP Investment Calculator

- Calculate future SIP value
- Support custom investment amounts
- Support multiple investment durations
- Demonstrate compounding growth

## ✅ Portfolio Analysis

- Upload portfolio CSV files
- Analyze holdings automatically
- Calculate total portfolio value
- Detect invalid stock symbols
- Generate portfolio insights

## ✅ Risk Profile Assessment

- Analyze investor queries
- Classify investors as:
  - Conservative
  - Moderate
  - Aggressive

## ✅ Retirement Planning

- Create retirement strategies
- Suggest asset allocation
- Estimate retirement corpus
- Generate long-term wealth plans

## ✅ Intelligent Routing using LangGraph

- Dynamic workflow routing
- State-based AI execution
- Modular financial agent architecture

## ✅ FastAPI Backend

- REST API integration
- CSV upload support
- Frontend-ready architecture

---

# 🧠 Tech Stack

## AI / LLM

- LangGraph
- LangChain
- Groq LLM (Llama 3.1 8B)

## Backend

- FastAPI
- Python

## Financial Data

- Alpha Vantage API
- Yahoo Finance (yfinance)

## Data Processing

- Pandas
- Regex

## Frontend

- HTML
- CSS
- JavaScript

---

# 📂 Project Structure

```bash
WealthAdvisor-AI/
│
├──  AIWealthAgent.py
├──  uploads/
├──  .env
├──  requirements.txt
│──  README.md
├── public/
│   ├── index.html
│   ├── style.css
│   └── script.js
│

```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/WealthAdvisor-AI.git
cd WealthAdvisor-AI
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

---

# ▶️ Run Backend

```bash
uvicorn app:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

# 🌐 Run Frontend

Simply open:

```bash
index.html
```

or use Live Server in VS Code.

---

# 📡 API Endpoint

## POST `/wealth`

### Form Data

| Key | Type |
|---|---|
| query | string |
| file | CSV file (optional) |

---

# 📂 Supported Portfolio Upload

Upload a CSV file:

```csv
Ticker,Quantity
AAPL,10
MSFT,5
GOOGL,3
TSLA,2
```

---

# 🧠 LangGraph Workflow

```text
START
   ↓
Router Agent
   ↓
 ┌───────────────┬───────────────┬───────────────┬───────────────┐
 ↓               ↓               ↓               ↓
Stock         SIP          Portfolio      Retirement
 ↓               ↓               ↓               ↓
         Risk Assessment Agent
                    ↓
            Wealth Advisor Agent
                    ↓
                   END
```

---

# 💡 Example Queries

## Stock Analysis

```text
Analyze Tesla stock
```

```text
Analyze Apple stock
```

## SIP Planning

```text
Invest 5000 per month for 10 years
```

```text
Calculate SIP for 10000 for 15 years
```

## Portfolio Analysis

```text
Analyze my portfolio
```

## Retirement Planning

```text
Help me plan my retirement
```

## Risk Assessment

```text
I am a beginner investor with low risk tolerance
```


# 🔮 Future Improvements

- Real-Time Financial News
- Mutual Fund Analysis
- ETF Recommendations
- Portfolio Diversification Score
- User Authentication
- Investment Goal Tracking
- Voice-Based Financial Advisor
- Cloud Deployment
- Multi-Agent Collaboration


# 👨‍💻 Author

**Suryansh Singh**

AI & Data Science Enthusiast

Passionate about building intelligent AI systems using LangGraph, LLMs, and Financial AI Applications.

---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub!