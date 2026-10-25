# Personal Expense Tracker — FFM CIE 2

## Project
Personal Expense Tracker Using Cloud Computing. This application is developed using Python, Streamlit, Pandas and Plotly and deployed on Streamlit Community Cloud. It allows users to record income and expenses, manage budgets, view financial analytics and track transaction history through a web browser.

## Run in VS Code (Mac)
1. Download and extract the ZIP.
2. Open the extracted `Personal_Expense_Tracker` folder in VS Code.
3. Open Terminal in VS Code.
4. Create a virtual environment:
   `python3 -m venv .venv`
5. Activate it:
   `source .venv/bin/activate`
6. Install packages:
   `pip install -r requirements.txt`
7. Run:
   `streamlit run app.py`
8. Streamlit prints a local URL (usually http://localhost:8501). Open it in your browser.

## Files
- `app.py`: application source code
- `data/transactions.csv`: sample financial dataset
- `requirements.txt`: Python dependencies
- `FFM_CIE2_Project_Report.docx`: report with all eight required sections
- `FFM_CIE2_Presentation.pptx`: presentation draft

## Dataset
The included CSV is a small synthetic sample created for demonstration. It is not real banking data and has no external dataset citation. If the instructor requires an external dataset, replace or supplement it with a reliable public dataset and cite the source in the report.

## Cloud technology requirement
The Personal Expense Tracker is deployed using Streamlit Community Cloud.

**Live Application:** https://personalexpensetracker-efelgfipckbjomqwtef47t.streamlit.app

The application is developed using Python, Streamlit, Pandas and Plotly. Users can access the application through a web browser without installing the software locally.

**Storage Limitation:** The application currently uses CSV file storage. The deployed application's local file storage may not provide permanent data persistence. Cloud database or cloud storage integration can be added in the future.
## Testing
Use the test cases in the report. Record actual observed results during your run; the report's expected results are not proof of execution.

## Known limitations
- No login or multi-user account system.
- Local CSV persistence only.
- Budget is entered for the current session and is not persisted.
- Financial advice is not provided; the app is a tracking/analysis prototype.
