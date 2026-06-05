from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import StateGraph,START,END
from typing  import TypedDict
import yfinance as yf
import re,requests,os
import pandas as pd
from fastapi import FastAPI,UploadFile,Form,File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ******************************************** LLM And Env FILE ********************************
load_dotenv()
# llm load
llm=ChatGroq(model='llama-3.1-8b-instant')

# ******************************************* FastAPI Server *********************************
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# *********************************Serve Frontend UI****************************
app.mount("/public",StaticFiles(directory='public'),name='public')
# get request from server
@app.get("/")
def serve_frontend():
    return FileResponse("public/index.html")

# ******************************************* State *******************************************
class WealthState(TypedDict):
    user_query:str
    router:str
    risk_profile:str
    stock_price:str
    portfolio_analysis:str
    sip_result:str
    retirement_plan:str
    portfolio_file:str
    final_response:str

# ****************************************** Add Nodes ***************************************
# router Node
def router_node(state: WealthState):
    query = state["user_query"].lower()
    stock_keywords = [
        "stock",
        "share",
        "tesla",
        "apple",
        "google",
        "microsoft",
        "nvidia",
        "aapl",
        "msft",
        "googl",
        "tsla",
        "nvda"
    ]

    if any(k in query for k in stock_keywords):
        return {"router": "stock"}

    elif "portfolio" in query:
        return {"router": "portfolio"}

    elif "sip" in query or "invest" in query:
        return {"router": "sip"}

    elif "retirement" in query:
        return {"router": "retirement"}

    else:
        return {"router": "general"}

# conditional statement
def route_decision(state: WealthState):

    return state["router"]

# risk Node
def risk_assesment(state:WealthState):
    query=state['user_query']
    # prompt
    prompt=f"""Classify the investor
    User Query:{query}
    
    Categories:
    Conservative
    Moderate
    Aggressive

    Return Only Categories.
"""
    response=llm.invoke(prompt).content

    return {'risk_profile':response}

# Second Node 
def stock_analysis(state:WealthState):
    query = state["user_query"].upper()
    symbol_map = {
    "TESLA": "TSLA",
    "MICROSOFT": "MSFT",
    "GOOGLE": "GOOGL",
    "ALPHABET": "GOOGL",
    "APPLE": "AAPL",
    "NVIDIA": "NVDA"
}

    symbol = "AAPL"
    for company, ticker in symbol_map.items():
        if company in query:
            symbol = ticker
            break
    
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = (
            f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        )

        response = requests.get(url, timeout=10)
        data = response.json()
        if "Global Quote" not in data:
            return {
                "stock_price":
                "Unable to fetch live stock data (Alpha Vantage limit reached or invalid symbol)"
            }

        quote:dict = data["Global Quote"]

        current_price = quote.get("05. price", "N/A")
        change = quote.get("09. change", "N/A")
        change_percent = quote.get("10. change percent", "N/A")

        # Company fundamentals from Yahoo
        stock = yf.Ticker(symbol)
        info = stock.info

        stock_data = f"""
        Company: {info.get('longName', 'N/A')}

        Symbol: {symbol}

        Live Price: ${current_price}

        Daily Change: {change}

        Change Percent: {change_percent}

        Sector: {info.get('sector', 'N/A')}

        Market Cap: {info.get('marketCap', 'N/A')}

        PE Ratio: {info.get('trailingPE', 'N/A')}
    """
        return {
            "stock_price": stock_data
        }

    except Exception as e:

        return {
            "stock_price":
            f"Unable to fetch stock data: {str(e)}"
        }
# third node
def portfolio_analysis(state:WealthState):
    try:
        file_path = state.get("portfolio_file")

        if not file_path:

            return {
                "portfolio_analysis":"No portfolio file uploaded."
            }

        df = pd.read_csv(file_path)

        total_value = 0
        valid_holdings = []
        invalid_holdings = []

        for _, row in df.iterrows():
            symbol = str(row.get("Ticker")).strip().upper()
            qty = int(row.get("Quantity", 0))

            stock = yf.Ticker(symbol)

            hist = stock.history(period="1d")

            if hist.empty:
                invalid_holdings.append(symbol)
                continue

            current_price = float(hist["Close"].iloc[-1])

            value = current_price * qty

            total_value += value

            valid_holdings.append(
                f"{symbol} | Qty:{qty} | "
                f"Price:${current_price:.2f} | "
                f"Value:${value:.2f}"
            )

        report = f"""
        \nPortfolio Value: ${total_value:.2f}\n
        Holdings: {chr(10).join(valid_holdings)}       
        \nInvalid Symbols: {', '.join(invalid_holdings) if invalid_holdings else 'None'}
        """

        return {
            "portfolio_analysis": report
        }

    except Exception as e:

        return {
            "portfolio_analysis":
            f"Portfolio Error: {str(e)}"
        }

# fourth Node
def sip_calculator(state:WealthState):
    query = state["user_query"]
    numbers = re.findall(r"\d[\d,]*", query)

    cleaned = [
        int(n.replace(",", ""))
        for n in numbers
    ]
    monthly = 1000
    years = 1

    if len(cleaned) >= 1:
        monthly = int(cleaned[0])

    if len(cleaned) >= 2:
        years = int(cleaned[1])

    annual_return = 12
    r = annual_return / 12 / 100

    n = years * 12
    future_value=(monthly * (((1+r) ** n-1) * (1+r)) / r)

    return {
        'sip_result':
            f"Monthly Investment: ₹{monthly}\n"
            f"Years: {years}\n"
            f"Future Value: ₹{future_value:,.2f}"
        }

# fifth Node
def retirement_plan(state:WealthState):
    # prompt
    prompt=f"""Create a retirement planning guide for a young investor.
Rules:
- Do Not use ** or *
- Do Not use ----
- Do not use ===.
- Keep response concise and professional

Return:
- Target Corpus
- Asset Allocation
- Suggestions

Return plain text only.
"""
    response=llm.invoke(prompt).content
    return {'retirement_plan':response}


# final node
def final_adviser(state:WealthState):
    query=state['user_query']

    prompt = f"""
You are a professional wealth advisor.

Generate a clean report.
Rules:
- No markdown
- No **
- No ----
- Do not use ===.
- No headings with lines
- Use emojis
- Keep response concise and professional
- If information is unavailable, write "Not Available"
- Do not invent stock prices.
- Do not invent market data.

Generate:

1. Executive Summary
2. Investor Profile
3. Investment Analysis
4. Risk Assessment
5. Recommended Strategy
6. Final Recommendation
7. Disclaimer

User Query:
{query}

Risk Profile:
{state.get('risk_profile','Not Available')}

Stock Analysis:
{state.get('stock_price','Not Available')}

Portfolio Analysis:
{state.get('portfolio_analysis','Not Available')}

SIP Result:
{state.get('sip_result','Not Available')}

Retirement Plan:
{state.get('retirement_plan','Not Available')}

Return plain text only.
"""
    res=llm.invoke(prompt).content
    return {'final_response':res}

# ****************************************** Graph Making **************************************
graph=StateGraph(WealthState)
# add nodes
graph.add_node('router', router_node)
graph.add_node('risk', risk_assesment)
graph.add_node('stock', stock_analysis)
graph.add_node('portfolio', portfolio_analysis)
graph.add_node('sip', sip_calculator)
graph.add_node('retirement', retirement_plan)
graph.add_node('adviser', final_adviser)
# add edges 
graph.add_edge(START,'router')
graph.add_conditional_edges(
    "router",
    route_decision,
    {
        "stock": "stock",
        "sip": "sip",
        "retirement": "retirement",
        "portfolio": "portfolio",
        "general": "risk"
    }
)
graph.add_edge('stock', 'risk')
graph.add_edge('portfolio', 'risk')
graph.add_edge('sip', 'risk')
graph.add_edge('retirement', 'risk')
graph.add_edge('risk', 'adviser')
graph.add_edge('adviser', END)

wealth=graph.compile()

# **************************************** Connect Server ***************************************
# post request
@app.post("/wealth")
def WealthQuery(
    query: str = Form(...),
    file: UploadFile = File(None)
):

    state = {
        "user_query": query
    }

    if file:

        os.makedirs("uploads", exist_ok=True)

        file_path = f"uploads/{file.filename}"

        contents = file.file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        state["portfolio_file"] = file_path

    result = wealth.invoke(state)

    return {
        "risk_profile": result.get("risk_profile", ""),

        "stock_price": result.get("stock_price", ""),

        "portfolio_analysis": result.get("portfolio_analysis", ""),

        "sip_result": result.get("sip_result", ""),

        "retirement_plan": result.get("retirement_plan", ""),

        "final_response": result.get("final_response", "")
    }
