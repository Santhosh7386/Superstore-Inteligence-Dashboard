import pandas as pd
import plotly.express as px
from shiny import reactive, render
from shiny.express import ui, input
from shinywidgets import render_plotly

# ============================================================
# 1. DATA ENGINE
# ============================================================
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.strftime("%b")
df["Month_Num"] = df["Order Date"].dt.month
df["Day"] = df["Order Date"].dt.day_name()

REGIONS = sorted(df["Region"].unique().tolist())
STATES = sorted(df["State"].unique().tolist())
CATEGORIES = sorted(df["Category"].unique().tolist())
YEARS = sorted(df["Year"].unique().tolist(), reverse=True)
YEAR_CHOICES = ["All"] + [str(y) for y in YEARS]

# ============================================================
# 2. UI GLOBAL STYLING
# ============================================================
ui.page_opts(fillable=True) # Heading removed from title here

ui.head_content(
    ui.tags.style("""
        :root { --brand-main: #1e293b; --brand-accent: #2563eb; --bg-canvas: #f8fafc; }
        body { background-color: var(--bg-canvas); font-family: 'Inter', sans-serif; }
        .sidebar { background: white !important; border-right: 1px solid #e2e8f0 !important; }
        .hero-section {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: white; padding: 60px 30px; border-radius: 0 0 30px 30px;
            margin-bottom: 40px; text-align: center;
        }
        .nav-card {
            background: white; border-radius: 16px; padding: 30px;
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); transition: 0.4s;
            height: 100%; border: 1px solid #e2e8f0; display: flex; flex-direction: column;
        }
        .nav-card:hover { transform: translateY(-8px); border-color: var(--brand-accent); }
        .insight-box { background: #eff6ff; border-left: 4px solid #2563eb; padding: 15px; margin-top: 20px; font-size: 0.9rem; }
    """)
)

# ============================================================
# 3. MULTI-PAGE LAYOUT
# ============================================================
with ui.navset_hidden(id="main_tabs"):
    
    # --- PAGE: HOME ---
    with ui.nav_panel("home"):
        with ui.div(class_="hero-section"):
            ui.h1("Superstore Executive Dashboard", style="font-weight: 800; font-size: 3rem;")
            ui.p("Transform raw logistics data into actionable commercial strategy.", style="font-size: 1.2rem; opacity: 0.9;")

        with ui.layout_columns(fill=False):
            with ui.div(class_="nav-card"):
                ui.h3("🌎 Geography")
                ui.p("Identify high-growth territories and underperforming states. Essential for logistics planning and regional marketing spend.")
                ui.input_action_button("goto_geo", "Analyze Markets", class_="btn-primary mt-auto")
            
            with ui.div(class_="nav-card"):
                ui.h3("📦 Product Mix")
                ui.p("Evaluate inventory health. Understand which categories dominate your revenue stream and which sub-categories have the best margins.")
                ui.input_action_button("goto_cat", "Explore Products", class_="btn-primary mt-auto")
            
            with ui.div(class_="nav-card"):
                ui.h3("💰 Financials")
                ui.p("Audit your bottom line. Isolate loss-making products and cities to protect margins and optimize discount strategies.")
                ui.input_action_button("goto_profit", "View Financials", class_="btn-primary mt-auto")
            
            with ui.div(class_="nav-card"):
                ui.h3("⏳ Time Trends")
                ui.p("Spot seasonal cycles and year-over-year growth. Perfect for forecasting future demand and holiday staffing requirements.")
                ui.input_action_button("goto_time", "Track Trends", class_="btn-primary mt-auto")

    # --- PAGE: GEOGRAPHY ---
    with ui.nav_panel("geo"):
        with ui.layout_sidebar():
            with ui.sidebar(class_="sidebar"):
                ui.input_action_button("back_geo", "← Back Home", class_="btn-outline-dark mb-3 w-100")
                ui.input_select("geo_year", "Select Year", choices=YEAR_CHOICES)
                ui.input_select("geo_region", "Select Region", choices=["All"] + REGIONS)
                ui.hr()
                ui.markdown("""
                **Key Analysis Points:**
                * **Market Concentration:** Observe if sales are top-heavy in specific states.
                * **Profit Efficiency:** Cities in the top-right of the scatter plot are your 'Cash Cows'.
                * **Expansion Strategy:** Low-sales, high-profit cities represent untapped potential.
                """)

            ui.h2("Geographic Sales Analysis")
            with ui.layout_columns():
                with ui.card(class_="chart-card"):
                    ui.card_header("1. Sales by Region")
                    @render_plotly
                    def plot_geo_region():
                        d = filtered_geo().groupby("Region")["Sales"].sum().reset_index()
                        return px.bar(d, x="Region", y="Sales", color="Region")

                with ui.card(class_="chart-card"):
                    ui.card_header("2. Top 10 States")
                    @render_plotly
                    def plot_geo_state():
                        d = filtered_geo().groupby("State")["Sales"].sum().nlargest(10).reset_index()
                        return px.bar(d, x="Sales", y="State", orientation='h', color_discrete_sequence=['#3b82f6'])

            with ui.card(class_="chart-card"):
                ui.card_header("3. City-Level Performance (Sales vs Profit)")
                @render_plotly
                def plot_geo_city():
                    d = filtered_geo().groupby("City").agg({"Sales":"sum", "Profit":"sum"}).nlargest(30, "Sales").reset_index()
                    return px.scatter(d, x="Sales", y="Profit", text="City", size="Sales", color="Profit", color_continuous_scale="RdBu")

    # --- PAGE: CATEGORY ---
    with ui.nav_panel("cat"):
        with ui.layout_sidebar():
            with ui.sidebar(class_="sidebar"):
                ui.input_action_button("back_cat", "← Back Home", class_="btn-outline-dark mb-3 w-100")
                ui.input_select("cat_year", "Fiscal Year", choices=YEAR_CHOICES)
                ui.hr()
                ui.markdown("""
                **Inventory Insights:**
                * **Category Mix:** Balanced revenue across Furniture, Office Supplies, and Tech ensures stability.
                * **Margin Leaders:** Watch for high-revenue items with thin margins (potential for optimization).
                """)

            ui.h2("Product Category Analysis")
            with ui.layout_columns():
                with ui.card(class_="chart-card"):
                    ui.card_header("1. Category Market Share")
                    @render_plotly
                    def plot_cat_pie():
                        d = filtered_cat().groupby("Category")["Sales"].sum().reset_index()
                        return px.pie(d, values="Sales", names="Category", hole=0.4)

                with ui.card(class_="chart-card"):
                    ui.card_header("2. Sub-Category Sales")
                    @render_plotly
                    def plot_cat_sub():
                        d = filtered_cat().groupby("Sub-Category")["Sales"].sum().sort_values().reset_index()
                        return px.bar(d, x="Sales", y="Sub-Category", orientation='h')

            with ui.card(class_="chart-card"):
                ui.card_header("3. Profit Margin per Sub-Category")
                @render_plotly
                def plot_cat_margin():
                    d = filtered_cat().groupby("Sub-Category").agg({"Sales":"sum", "Profit":"sum"}).reset_index()
                    d["Margin"] = (d["Profit"] / d["Sales"]) * 100
                    return px.bar(d, x="Sub-Category", y="Margin", color="Margin", color_continuous_scale="Viridis")

    # --- PAGE: FINANCIALS ---
    with ui.nav_panel("profit"):
        with ui.layout_sidebar():
            with ui.sidebar(class_="sidebar"):
                ui.input_action_button("back_profit", "← Back Home", class_="btn-outline-dark mb-3 w-100")
                ui.input_select("prof_year", "Select Year", choices=YEAR_CHOICES)
                ui.input_select("prof_state", "Select State Focus", choices=["All"] + STATES)
                ui.input_select("prof_cat", "Select Category", choices=["All"] + CATEGORIES)
                ui.hr()
                ui.markdown("""
                **Financial Health Check:**
                * **Red Zones:** Red bars indicate sub-categories losing money. Investigate shipping or discount rates here.
                * **Scale vs Profit:** Big bubbles at the bottom of the matrix indicate high-volume products that are hurting profitability.
                """)

            ui.h2("Financial Monitoring & Profitability")
            with ui.layout_columns(fill=False):
                with ui.value_box(theme="primary"):
                    "Net Profit"
                    @render.text
                    def prof_val(): return f"${filtered_prof()['Profit'].sum():,.0f}"
                with ui.value_box(theme="info"):
                    "Sales volume"
                    @render.text
                    def prof_sales(): return f"${filtered_prof()['Sales'].sum():,.0f}"

            with ui.layout_columns():
                with ui.card(class_="chart-card"):
                    ui.card_header("1. Profit Distribution by State")
                    @render_plotly
                    def plot_prof_state_bar():
                        d = filtered_prof()
                        if input.prof_state() == "All":
                            data = d.groupby("State")["Profit"].sum().reset_index()
                            return px.bar(data.nlargest(15, "Profit"), x="Profit", y="State", orientation='h')
                        else:
                            data = d.groupby("City")["Profit"].sum().reset_index()
                            return px.bar(data, x="Profit", y="City", orientation='h', title=f"Profit in {input.prof_state()}")

                with ui.card(class_="chart-card"):
                    ui.card_header("2. Loss-Making Sub-Categories")
                    @render_plotly
                    def plot_prof_loss():
                        d = filtered_prof().groupby("Sub-Category")["Profit"].sum().reset_index()
                        losses = d[d["Profit"] < 0].sort_values("Profit")
                        return px.bar(losses, x="Profit", y="Sub-Category", color_discrete_sequence=["#ef4444"])

            with ui.card(class_="chart-card"):
                ui.card_header("3. Profitability Matrix (Product Level)")
                @render_plotly
                def plot_prof_matrix():
                    d = filtered_prof().groupby("Product Name").agg({"Sales":"sum", "Profit":"sum", "Category":"first"}).nlargest(50, "Sales").reset_index()
                    return px.scatter(d, x="Sales", y="Profit", color="Category", hover_name="Product Name", size="Sales")

    # --- PAGE: TIME ---
    with ui.nav_panel("time"):
        with ui.layout_sidebar():
            with ui.sidebar(class_="sidebar"):
                ui.input_action_button("back_time", "← Back Home", class_="btn-outline-dark mb-3 w-100")
                ui.input_select("time_year", "Compare Years", choices=YEAR_CHOICES)
                ui.hr()
                ui.markdown("""
                **Trend Forecaster:**
                * **Q4 Peak:** Usually, sales spike in Nov/Dec. Ensure inventory is ready.
                * **Day of Week:** Analyze if weekends drive B2C sales or weekdays drive B2B (Corporate) sales.
                """)

            ui.h2("Temporal Performance Trends")
            with ui.card(class_="chart-card"):
                ui.card_header("1. Monthly Revenue Velocity")
                @render_plotly
                def plot_time_trend():
                    d = filtered_time().groupby(["Year", "Month_Num", "Month"])["Sales"].sum().reset_index()
                    return px.line(d, x="Month", y="Sales", color="Year")

            with ui.layout_columns():
                with ui.card(class_="chart-card"):
                    ui.card_header("2. Sales by Day of Week")
                    @render_plotly
                    def plot_time_day():
                        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                        d = filtered_time().groupby("Day")["Sales"].sum().reindex(days).reset_index()
                        return px.bar(d, x="Day", y="Sales", color_discrete_sequence=['#8b5cf6'])

                with ui.card(class_="chart-card"):
                    ui.card_header("3. Quarterly Performance")
                    @render_plotly
                    def plot_time_quarter():
                        d = filtered_time()
                        d["Quarter"] = d["Order Date"].dt.quarter.astype(str)
                        dq = d.groupby("Quarter")["Sales"].sum().reset_index()
                        return px.bar(dq, x="Quarter", y="Sales", color="Quarter")

# ============================================================
# 4. REACTIVE FILTERS & NAVIGATION
# ============================================================

@reactive.calc
def filtered_geo():
    d = df.copy()
    if input.geo_year() != "All":
        d = d[d["Year"] == int(input.geo_year())]
    if input.geo_region() != "All":
        d = d[d["Region"] == input.geo_region()]
    return d

@reactive.calc
def filtered_cat():
    d = df.copy()
    if input.cat_year() != "All":
        d = d[d["Year"] == int(input.cat_year())]
    return d

@reactive.calc
def filtered_prof():
    d = df.copy()
    if input.prof_year() != "All":
        d = d[d["Year"] == int(input.prof_year())]
    if input.prof_state() != "All":
        d = d[d["State"] == input.prof_state()]
    if input.prof_cat() != "All":
        d = d[d["Category"] == input.prof_cat()]
    return d

@reactive.calc
def filtered_time():
    d = df.copy()
    if input.time_year() != "All":
        d = d[d["Year"] == int(input.time_year())]
    return d

# --- Navigation Logic ---
@reactive.effect
@reactive.event(input.goto_geo)
def _(): ui.update_navs("main_tabs", selected="geo")

@reactive.effect
@reactive.event(input.goto_cat)
def _(): ui.update_navs("main_tabs", selected="cat")

@reactive.effect
@reactive.event(input.goto_profit)
def _(): ui.update_navs("main_tabs", selected="profit")

@reactive.effect
@reactive.event(input.goto_time)
def _(): ui.update_navs("main_tabs", selected="time")

@reactive.effect
@reactive.event(input.back_geo, input.back_cat, input.back_profit, input.back_time)
def _(): ui.update_navs("main_tabs", selected="home")