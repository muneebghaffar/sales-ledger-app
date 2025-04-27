Sales by Product Dashboard
This project is an interactive dashboard that visualizes monthly sales data for hats and t-shirts, allowing users to filter and explore sales by fiscal year, customer, currency, location, and product. The backend processes raw sales data, while the frontend renders an interactive stacked bar chart using Vue.js and Chart.js.
Project Overview
The project is divided into two main components:

Backend: Processes sales data from an Excel file, aggregates it by fiscal year, and generates a JSON file for the frontend.
Frontend: Displays an interactive stacked bar chart with filtering options, color customization, and data drilldown capabilities.

Technologies Used
Backend

Python 3.8+
FastAPI: For creating the API to serve processed data.
Pandas: For data manipulation and aggregation.
OpenPyXL: For reading Excel files.
Uvicorn: ASGI server to run the FastAPI application.
python-dotenv: For environment variable management.

Frontend

Vue.js 3: Frontend framework for building the interactive UI.
Chart.js: For rendering the stacked bar chart.
Vue-Chartjs: Vue wrapper for Chart.js.
Tailwind CSS: For styling the application.
Axios: For making HTTP requests to the backend.
Vue Router: For client-side routing.
Vite: Build tool and development server for the frontend.

Folder Structure
sales-dashboard/
├── backend/
│ ├── app/
│ │ ├── data_process.py # Script to process sales data and generate JSON
│ │ └── main.py # FastAPI application to serve the data
│ ├── data-sets/
│ │ └── Sales Ledger.xlsx # Raw sales data (not included in repo)
│ ├── public/
│ │ └── data/
│ │ └── sales_data.json # Generated JSON file with processed data
│ ├── requirements.txt # Backend dependencies
│ └── .env # Environment variables (not included in repo)
├── frontend/
│ ├── src/
│ │ ├── App.vue # Main Vue component with the chart and filters
│ │ ├── assets/ # Static assets (e.g., images)
│ │ ├── components/ # Vue components (if any)
│ │ └── router/ # Vue Router configuration
│ ├── public/ # Static files served by Vite
│ ├── package.json # Frontend dependencies and scripts
│ ├── vite.config.js # Vite configuration
│ └── tailwind.config.js # Tailwind CSS configuration
└── README.md # Project documentation

Backend Logic
The backend processes sales data from Sales Ledger.xlsx and prepares it for the frontend. Key functionalities include:

Data Processing (data_process.py):

Reads sales transactions from the Excel file.
Groups transactions by fiscal year (April 1 to March 31).
Removes incomplete fiscal years (e.g., F2021, as data starts from January 2021).
Calculates LTM (Last Twelve Months: Jan 1, 2023 to Dec 31, 2023) and YTD (Year-to-Date: April 1, 2023 to Dec 31, 2023).
Aggregates sales by fiscal year, month, and product (Hats, T-Shirts).
Outputs the processed data as sales_data.json in the public/data/ directory.

API (main.py):

A FastAPI application that serves the processed sales_data.json file.
Supports filtering by customer, currency, location, and date (though filtering is primarily handled by the frontend in this implementation).

Frontend Logic
The frontend is a Vue.js application that renders an interactive stacked bar chart. Key features include:

Chart Rendering (App.vue):

Displays a stacked bar chart using Chart.js, showing monthly sales for Hats and T-Shirts.
X-axis: Months (dynamically adjusted based on period, e.g., Jan-Dec for LTM, April-Dec for YTD).
Y-axis: Sales amount in dollars with currency denomination.

Period Selection:

A dropdown to select periods (F2022, F2023, LTM Dec 23, YTD F2024).
Dynamically updates the x-axis labels based on the selected period.

Filtering:

Dropdowns for filtering by Customer, Currency, Location, and Date.
Checkboxes to filter products (Hats, T-Shirts).
Updates the chart dynamically based on selected filters.

Additional Features:

Color picker to customize bar colors.
Custom chart title with a reset button.
Toggle button to show/hide data labels on the chart.
Basic drilldown functionality (alerts on double-click; full Excel integration would require additional setup).

Installation and Setup
Prerequisites

Python 3.8+: For the backend.
Node.js 18+: For the frontend.
Git: To clone the repository.

Backend Setup

Navigate to the backend directory:
cd backend

# Create a virtual environment and activate it:
python -m venv venv
# To Run
.\venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

Install the dependencies:
pip install -r requirements.txt


Create a .env file in the backend/ directory with the following content:
SALES_LEDGER=data-sets/Sales Ledger.xlsx
JSON_OUTPUT=public/data/sales_data.json
FISCAL_YEAR_END=03-31
CURRENT_DATE=2023-12-31
CURRENCY=CAD
DENOMINATION=$

Process the sales data:
python app/data_process.py

Run the FastAPI server:
uvicorn app.main:app --reload

The backend will be available at http://localhost:8000.

Frontend Setup

Navigate to the frontend directory:
cd frontend

# Install the dependencies:
npm install

# Run the development server:
npm run dev

The frontend will be available at http://localhost:5173.

# To build for production:
npm run build

# To preview the production build:
npm run preview

Running the Project

Start the backend server (as described above).
Start the frontend development server (as described above).
Open http://localhost:5173 in your browser to view the dashboard.

Notes

Ensure the Sales Ledger.xlsx file is placed in backend/data-sets/ before running the backend.
The frontend fetches data from public/data/sales_data.json, which is generated by the backend.
For a production environment, you may need to configure CORS in the FastAPI backend to allow requests from the frontend domain.

Future Improvements

Implement server-side filtering in the FastAPI backend for better performance with large datasets.
Enhance the drilldown feature to integrate with Excel for displaying detailed transaction data.
Add error handling for missing or malformed data in the Excel file.

License
This project is for internal use and not licensed for distribution.