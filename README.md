# 🍿 Netflix Data Explorer & AI Recommender

An interactive data exploration and AI-powered recommendation web app built with **Streamlit**, analyzing over 8,000 titles from the Netflix catalog. Combines classic exploratory data analysis with a content-based Machine Learning model.

---

## 📌 Overview

This project was developed as part of a Data Science portfolio. It explores the Netflix titles dataset to uncover patterns in content types, genres, and release years — and goes a step further by incorporating an NLP-based recommendation engine.

The app has two layers:
- **`aplicacionnetflix.py`** — A core Python module with data cleaning, search, and statistics functions (CLI-ready).
- **`prueba1.py`** — A full Streamlit web app that wraps the CLI logic and adds an ML recommender and interactive visualizations.

---

## 🎯 Features

### 🔍 General Search
- Search by **actor/director** or **genre** across the full Netflix catalog.
- Results are displayed in an interactive table.

### 🤖 AI Recommender (Content-Based)
- Uses **TF-IDF vectorization** on title descriptions, genres, and cast.
- Computes **Cosine Similarity** between all titles to find the closest matches.
- Recommends 5 titles most similar to the one selected by the user.

### 📊 General Statistics
- **Pie chart** — Distribution of Movies vs. TV Shows.
- **Bar chart** — Top 10 most common genres in the catalog.

### 🎲 Legacy App Features
- **Random title generator** — Picks a random title from the dataset using the core module.
- **Recommendation by duration** — Finds movies matching a user-specified runtime in minutes.

---

## 🗂️ Dataset

| File | Description |
|---|---|
| `netflix_titles.csv` | Full catalog (~8,800 titles) — source of truth for all analysis |
| `netflix_peliculas.csv` | Filtered subset: Movies only |
| `netflix_series.csv` | Filtered subset: TV Shows only |
| `netflix_short_movies.csv` | Filtered subset: Short films |

> Source: [Netflix Movies and TV Shows — Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

---

## 🧠 Machine Learning Model

The recommender is built using **scikit-learn**:

1. A `features_for_ml` column is created by concatenating `description + genres + cast`.
2. A **TF-IDF matrix** is computed from these features.
3. **Cosine Similarity** is calculated between all title vectors.
4. For a given title, the top 5 most similar titles (excluding itself) are returned.

The model is cached with `@st.cache_resource` for performance.

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install streamlit pandas numpy scikit-learn plotly
```

### 2. Launch the Streamlit app

```bash
streamlit run prueba1.py
```

### 3. (Optional) Run the CLI version

```bash
python aplicacionnetflix.py
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Core language |
| Pandas | Data loading, cleaning, and filtering |
| NumPy | Numerical operations |
| Streamlit | Interactive web app framework |
| Plotly Express | Interactive charts |
| scikit-learn | TF-IDF vectorizer & cosine similarity |

---

## 📁 Project Structure

```
NetflixData_Explorer/
├── aplicacionnetflix.py     # Core module: data cleaning + CLI functions
├── prueba1.py               # Streamlit web app
├── netflix_titles.csv       # Full Netflix dataset
├── netflix_peliculas.csv    # Movies subset
├── netflix_series.csv       # TV Shows subset
├── netflix_short_movies.csv # Short films subset
└── netflix_eda_clase.ipynb  # Exploratory data analysis notebook
```

---

## 📝 Key Findings (EDA)

- The Netflix catalog is dominated by **Movies** (~70%) vs TV Shows (~30%).
- **Dramas**, **Comedies**, and **Documentaries** are the most represented genres.
- Content additions peaked around **2018–2020**, reflecting Netflix's global expansion strategy.

---

## 👤 Author

Developed as part of a Data Science portfolio.
