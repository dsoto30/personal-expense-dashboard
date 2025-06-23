import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Replaced the ML model with the extensive rule-based dictionary.
CATEGORY_RULES = {
    'Dining': [
        'restaurant', 'cafe', 'bistro', 'grill', 'diner', 'eatery', 'bar & grill',
        'pub', 'sushi', 'pizza', 'tacos', 'coffee', 'bakery', 'deli', 'meal',
        'dining', 'lunch', 'dinner', 'breakfast', 'brunch', 'takeout', 'takeaway',
        'foodpanda', 'eat', 'brewery', 'steakhouse', 'teriyaki', 'juice bar',
        'ice cream', 'yogurt', 'mcdonald\'s', 'starbucks', 'burger king', 'subway',
        'taco bell', 'kfc', 'pizza hut', 'domino\'s', 'chipotle', 'panera bread',
        'dunkin\'', 'wendy\'s', 'chick-fil-a', 'arby\'s', 'popeyes', 'doordash',
        'grubhub', 'uber eats', 'postmates', 'seamless', 'the cheesecake factory',
        'olive garden', 'red lobster', 'applebee\'s', 'ihop', 'denny\'s', 'tgi fridays',
        'buffalo wild wings', "taco", "jack in the box", "carl's jr", "little ca", "raising canes"
    ],
    'Entertainment': [
        'entertainment', 'theater', 'cinema', 'movies', 'concert', 'ticket', 'show',
        'event', 'stadium', 'arena', 'museum', 'gallery', 'park', 'amusement',
        'bowling', 'golf', 'club', 'bar', 'lounge', 'nightclub', 'live music',
        'festival', 'gaming', 'arcade', 'sports', 'streaming', 'subscription',
        'netflix', 'hulu', 'disney+', 'spotify', 'apple music', 'youtube premium',
        'hbo max', 'amazon prime video', 'fandango', 'ticketmaster', 'live nation',
        'seatgeek', 'amc theatres', 'regal cinemas', 'cinemark', 'topgolf',
        'dave & buster\'s', 'espn+', 'peacock', 'paramount+', 'siriusxm', 'audible',
        'steam games', 'playstation', 'xbox', 'nintendo', "chatgpt"
    ],
    'Transportation': [
        'transport', 'transit', 'taxi', 'cab', 'ride', 'lyft', 'uber', 'ola',
        'grab', 'didi', 'bus', 'subway', 'metro', 'train', 'rail', 'airline',
        'flight', 'airways', 'gas', 'fuel', 'petrol', 'station', 'parking',
        'garage', 'toll', 'rental car', 'scooter', 'bike share', 'mta', 'bart',
        'amtrak', 'greyhound', 'spirit airlines', 'american air', 'delta air',
        'united air', 'southwest air', 'jetblue', 'alaska air', 'hertz', 'avis',
        'enterprise', 'national car rental', 'shell', 'chevron', 'mobil', 'exxon',
        'bp', '76', 'sunoco', 'lime', 'bird', 'citibike', 'fastrak', 'ez-pass'
    ],
    'Groceries': [
        'grocery', 'market', 'supermarket', 'produce', 'organic', 'farm',
        'butcher', 'seafood', 'groceries', 'kroger', 'safeway', 'albertsons',
        'publix', 'trader joe\'s', 'whole foods', 'walmart neighborhood market',
        'target grocery', 'costco', 'sam\'s club', 'aldi', 'lidl', 'sprouts',
        'instacart', 'shipt', 'freshdirect', 'amazon fresh', 'ralphs', 'vons',
        'harris teeter', 'wegmans', 'food lion', 'giant', 'stop & shop', 'food4less',
    ],
    'Shopping': [
        'shop', 'store', 'boutique', 'retail', 'department store', 'clothing',
        'apparel', 'shoes', 'accessories', 'electronics', 'books', 'gifts',
        'home goods', 'furniture', 'pharmacy', 'drugstore', 'mall', 'outlet',
        'purchase', 'order', 'amazon', 'amzn', 'target', 'walmart', 'best buy',
        'apple', 'microsoft store', 'macy\'s', 'nordstrom', 'kohl\'s', 'j.c. penney',
        'gap', 'old navy', 'banana republic', 'h&m', 'zara', 'uniqlo', 'sephora',
        'ulta', 'cvs', 'walgreens', 'rite aid', 'the home depot', 'lowe\'s',
        'ikea', 'bed bath & beyond', 'etsy', 'ebay', 'nike', 'adidas'
    ],
    'Money Transfers': [
        'venmo', 'cash app', 'zelle', 'paypal', 'xoom', 'sent', 'received', 'p2p',
        'e-transfer', 'wire', 'remittance', 'deposit', 'withdrawal', 'atm',
        'western union', 'moneygram', 'wise', 'remitly', 'worldremit',
        'popmoney', 'google pay', 'apple cash', 'transfer', "irs", "internet payment", "cashback"
    ],
    "Investments": ["robinhood", "etrade", "fidelity", "vanguard", "schwab", "td ameritrade", "merrill lynch", "interactive brokers", "sofi invest", "acorns", "stash", "wealthfront", "betterment", "crypto", "bitcoin", "ethereum", "coinbase", "binance", "kraken"],
    "Loan": ["student ln", "discover e-payment"]
}

# 2. Replaced the complex model prediction with a simple, fast, rule-based function.
def category_prediction(description: str) -> str:
    """
    Categorizes a transaction based on a set of rules.
    """
    if not isinstance(description, str):
        return 'Uncategorized'

    lower_description = description.lower()

    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in lower_description:
                return category

    return 'Uncategorized'


st.set_page_config(page_title="Personal Expense Dashboard", page_icon="🧾")

def parse_wells_fargo(file) -> any:
    try:
        df = pd.read_csv(file, header=None, names=["Date", "Amount", "Status", "Check_Number", "Description"], dtype=str)
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce").dt.date
        df["Amount"] = (
            df["Amount"]
            .str.replace(r"[$,]", "", regex=True)
            .astype(float)
        )
        
        df["Type"] = df["Amount"].apply(lambda x: "expense" if x < 0 else "surplus")
        # The new categorization function is called here
        df["Category"] = df["Description"].apply(lambda x: category_prediction(x) if pd.notna(x) else "Uncategorized")
        
        df = df.drop(columns=["Status", "Check_Number"])
        
        return df
    except Exception as e:
        st.error(f"Error parsing Wells Fargo CSV: {e}")
        return None
    
def parse_discover_csv(file) -> any:
    try:
        df = pd.read_csv(file, dtype=str)
        df = df.drop(columns=["Post Date", "Category"])
        df = df.rename(columns={"Trans. Date": "Date"})
        df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce").dt.date
        df["Amount"] = (
            df["Amount"]
            .str.replace(r"[$,]", "", regex=True)
            .astype(float)
        )
        
        df["Type"] = df["Amount"].apply(lambda x: "expense" if x > 0 else "surplus")
        # 3. Added the categorization to the Discover parser as well.
        df["Category"] = df["Description"].apply(lambda x: category_prediction(x) if pd.notna(x) else "Uncategorized")

        return df 
    except Exception as e:
        st.error(f"Error reading Discover CSV: {e}")
        return None

def start_dashboard():
    st.title("Personal Finance Dashboard")
    bank = st.selectbox("Select Your Bank", ["Wells Fargo", "Discover"])
    statement = st.file_uploader("Please Upload Your Monthly Statements", type=['csv'])

    df = None
    if statement is not None:
        if bank == "Wells Fargo":
            df = parse_wells_fargo(statement)
        elif bank == "Discover":
            df = parse_discover_csv(statement)

    if df is not None:
        st.write("### Transaction Data")
        st.dataframe(df)

        total_expenses = df[df["Type"] == "expense"]["Amount"].sum()
        total_surplus = df[df["Type"] == "surplus"]["Amount"].sum()

        st.write(f"**Total Expenses:** ${abs(total_expenses):.2f}")
        st.write(f"**Total Surplus:** ${total_surplus:.2f}")

        st.write("### Expense Breakdown")
        expense_df = df[df['Type'] == 'expense'].copy()
        expense_df['Amount'] = expense_df['Amount'].abs()
        category_expenses = expense_df.groupby('Category')['Amount'].sum().reset_index()

        fig_pie = px.pie(category_expenses, values='Amount', names='Category', title='Expense by Category')
        st.plotly_chart(fig_pie)
        
        fig_bar = px.bar(df, x="Date", y="Amount", color="Type", title="Daily Transactions")
        st.plotly_chart(fig_bar)


if __name__ == "__main__":
    start_dashboard()
