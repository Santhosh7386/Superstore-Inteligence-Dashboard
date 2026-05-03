📊 Superstore Executive Dashboard

An interactive data visualization dashboard designed to transform raw retail sales data into actionable business insights.

🚀 Project Overview

This project presents an interactive dashboard built using the Superstore dataset to analyse key business metrics such as sales, profit, product performance, and temporal trends.

The goal of this application is to support data-driven decision-making by providing clear, structured, and interactive visual insights for business users such as analysts and managers.

🌐 Live Application

👉 https://2014-2017salesdashboard.shinyapps.io/superstore_dashboard11/

📁 Dataset
Source: Superstore Dataset
Records: ~10,000 rows
Features include:
Sales, Profit, Quantity, Discount
Category, Sub-category
Region, State, City
Order Date, Ship Date
⚙️ Data Preprocessing

The dataset was cleaned and prepared using Python:

Converted date columns to datetime format
Checked and handled missing values (none found)
Removed duplicates
Created new features:
Delivery Time
Profit Margin
Performed normalization for improved analysis
📊 Dashboard Structure

The dashboard is divided into four key sections:

🌍 Geography
Sales by region
Top-performing states
City-level performance (Sales vs Profit)
📦 Product Mix
Category market share
Sub-category sales
Profit margin analysis
💰 Financials
KPI metrics (Sales & Profit)
Profit distribution by state
Loss-making sub-categories
Profitability matrix (Sales vs Profit)
⏳ Time Trends
Monthly sales trends
Sales by day of week
Quarterly performance
🎯 Key Features
Interactive filters (Year, Region, Category, State)
Multiple visualization types:
Bar charts
Line charts
Scatter plots
KPI cards
User-friendly and structured layout
Multi-page navigation for focused analysis
🧠 Key Insights
Sales performance varies significantly across regions
Technology is the highest-performing category
Some products generate losses despite high sales
Clear seasonal trends exist in sales data
✅ Advantages
Clear and intuitive dashboard design
Effective use of visualization techniques
Interactive filtering for dynamic analysis
Comprehensive coverage of business metrics
⚠️ Limitations
Focuses on descriptive analytics only
No real-time data integration
Limited advanced customization
Performance may reduce with larger datasets
🔮 Future Improvements
Integration of predictive analytics (ML models)
Real-time data connectivity
Enhanced interactivity and drill-down features
Improved UI/UX design
Mobile responsiveness
🛠️ Technologies Used
R (Shiny)
Python (Data preprocessing & EDA)
Pandas, NumPy
Matplotlib, Seaborn
📌 How to Run Locally
Clone the repository:
git clone https://github.com/your-username/superstore-dashboard.git
Open the project in RStudio
Run the Shiny app:
shiny::runApp()
📄 License

This project is for academic purposes.

🙌 Acknowledgements
Superstore dataset (public dataset for analytics practice)
Inspiration from Tableau and Power BI dashboards
⭐ If you like this project

Give it a ⭐ on GitHub!
