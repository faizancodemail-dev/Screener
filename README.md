# Stock Breakout Screener

A comprehensive stock screener application built with Python and Streamlit.

## Hosting on Streamlit Cloud via GitHub

This application is ready to be deployed to Streamlit Community Cloud without any code changes!

1. **Push your code to GitHub**: 
   Make sure you push this folder (`Screener`) to a GitHub repository.
2. **Include necessary folders**: 
   Ensure your `.gitignore` does not accidentally ignore the `NAMES` folder because the app needs the sector CSVs to run. Empty folders like `icons` and `data` are automatically created by the app when it boots.
3. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Click "New app"
   - Select your GitHub repository.
   - For **Main file path**, type `final.py`.
   - Click **Deploy**!

### Important Notes for Cloud Hosting
* **Data Persistence**: Streamlit Cloud regularly puts apps to "sleep". When it wakes up, any data downloaded inside the `data` folder will be cleared. You will need to click the **Download Fresh Data** button in the sidebar daily or when the app awakens to get the latest YFinance historical prices.
* **Saving Combinations**: Custom combination scans created in the app are saved to `saved_combos.json`. This file is also ephemeral on Streamlit Cloud and will reset on reboot. If you want permanent combos, save them and then commit your local `saved_combos.json` to GitHub!
* **Icons**: To display icons, add your `.png` images directly into the `icons` folder locally, and push those images to GitHub.

## Local Setup
If you want to run it locally:
```bash
pip install -r requirements.txt
streamlit run final.py
```
