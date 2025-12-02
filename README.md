# E-commerce-Customer-Segmentation-RFM-Analysis-
📊 E-Commerce Customer Segmentation Dashboard (RFM Analysis)

This project performs RFM (Recency, Frequency, Monetary) analysis on e-commerce transactional data and visualizes customer segments through an interactive Streamlit dashboard. The results help businesses identify high-value customers, retention opportunities, and personalized marketing campaign targets.

🚀 Features

✔️ Automatically calculates customer Recency, Frequency, Monetary values
✔️ Generates RFM Scores and assigns behavior-based segments
✔️ Interactive dashboard with:
  • Segment distribution charts
  • RFM scatter plots
  • KPI summary metrics
  • Searchable/exportable customer table
✔️ Export customer segments for marketing platforms
✔️ Includes option to generate sample synthetic data

📁 Project Structure
File	Description
app.py	Streamlit dashboard for interactive visualization
rfm_analysis.py	Calculates RFM metrics, scores, and segments
generate_sample_data.py	Creates synthetic sample dataset
ecommerce_data.csv	Example input transactional data
RFM_Segments.csv	Output dataset containing segmented customers
requirements.txt	Dependencies required to run the project
🧪 Installation
# Clone the repository
git clone https://github.com/<username>/<repo>.git
cd <repo>

# Create virtual environment
python -m venv venv
source venv/bin/activate       # Mac / Linux
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt

📁 Sample Data (Optional)

If you don’t have a dataset, auto-generate one:

python generate_sample_data.py


This creates ecommerce_data.csv.

⚙️ Run RFM Analysis
python rfm_analysis.py --input ecommerce_data.csv --output RFM_Segments.csv


Optional parameters:

--snapshot YYYY-MM-DD     # specify custom analysis date

🖥️ Launch the Dashboard
streamlit run app.py


Then open the generated local URL:

http://localhost:8501

🧠 How RFM Works
Metric	Meaning	Measurement
Recency	How recently a customer purchased	Days since last purchase
Frequency	How often they purchase	Number of orders
Monetary	How much they spend	Total revenue from customer

Each metric is scored (1–5), combined into an RFM Score, and mapped to segments like:

🏆 Champions

💎 Loyal Customers

🕊️ New Customers

⚠️ At Risk

❄️ Lost Customers

🛍️ Potential Loyalists

📈 Use Cases

🔹 Loyalty programs
🔹 Targeted promotions
🔹 Customer retention strategies
🔹 Upsell/Cross-sell recommendations
🔹 Lifecycle-based marketing automation

🤝 Contributing

Pull requests are welcome!
If making major changes, please open an issue first to discuss.
