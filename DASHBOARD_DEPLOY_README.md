# SupeRR Selector Season 2 — Dashboard Deployment

This folder is ready to deploy on Streamlit Community Cloud.

## Files required
- `app.py`
- `requirements.txt`
- `top10_batters.csv`
- `top10_bowlers.csv`
- `all_batter_scores.csv`
- `all_bowler_scores.csv`
- `sensitivity_analysis.csv`
- `audit_summary.json`

## Publish and get a public dashboard URL
1. Sign in to GitHub and create a **Public** repository, for example `suprr-selector-dashboard`.
2. Upload the files listed above to the repository's root (you can upload this ZIP's contents).
3. Open https://share.streamlit.io/ and sign in using GitHub.
4. Select **Create app**, choose your repository, branch `main`, and main file path `app.py`.
5. Click **Deploy** and wait for the app to finish building.
6. Copy the public `https://....streamlit.app` URL and paste it into the competition's dashboard-link field.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
