# 💸 Personal Expense Tracker

A clean, single-file web app to track daily expenses — built with Python and Streamlit.

---

## Features

- Add expenses with date, amount, category, and description
- View all expenses in a sortable table
- Category-wise summary with percentage share
- Bar chart and line chart for spending insights
- Filter expenses by category
- Download data as CSV
- Delete all entries with one click

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | UI framework |
| Pandas | Data handling |

---

## Project Structure

```
expense-tracker/
└── app.py          # entire app in one file
└── README.md
└── requirements.txt
```

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/RithwikYathamshetty/VRIZZLE/blob/7f60b174dd7ace29fe57e5211162722c59fa4913/app.py
cd expense-tracker
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Start the app**
```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## requirements.txt

Create a file named `requirements.txt` in the same folder with this content:

```
streamlit
pandas
```

---

## Deploy on Streamlit Cloud (Free)

Streamlit offers free hosting directly from your GitHub repo.

**Step 1 — Push your code to GitHub**

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/your-username/expense-tracker.git
git push -u origin main
```

**Step 2 — Deploy on Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repository, branch (`main`), and set the main file path to `app.py`
5. Click **"Deploy"**

Your app will be live at a public URL like:
```
https://your-username-expense-tracker-app-xxxx.streamlit.app
```

> ⚠️ Note: Streamlit Cloud uses session state only — data resets on page refresh. This is expected for this project.

## Author

**Your Name**  
[GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)
