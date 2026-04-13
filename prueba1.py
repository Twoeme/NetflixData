import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import aplicacionnetflix as original_app  # Connection to your original Python script

# 1. Page Configuration
st.set_page_config(page_title="Netflix Explorer & ML Recs", page_icon="🍿", layout="wide")

# Netflix Custom CSS
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #141414;
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e50914 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #e50914 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px;
        font-weight: bold;
        transition: 0.2s ease-in;
    }
    .stButton>button:hover {
        background-color: #f40612 !important;
        transform: scale(1.05);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #333;
    }
    
    /* Dataframes / Tables */
    .stDataFrame {
        background-color: #333333;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍿 Netflix Data Explorer & AI Recommender")

# 2. Load and Clean Data (using native English dataset columns)
@st.cache_data
def load_data():
    df = pd.read_csv('netflix_titles.csv')
    
    # Fill missing values natively in english to avoid nan errors
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    df['description'] = df['description'].fillna('')
    df['listed_in'] = df['listed_in'].fillna('Unknown')
    df = df.dropna(subset=['title'])
    
    # Basic text preprocessing for the ML model 
    df['features_for_ml'] = df['description'].astype(str) + " " + df['listed_in'].astype(str) + " " + df['cast'].astype(str)
    df['title'] = df['title'].astype(str)
    df['title_lower'] = df['title'].str.lower().str.strip()
    return df

df = load_data()

# 3. Machine Learning Model (Content-Based Recommendation / TF-IDF)
@st.cache_resource
def compute_similarity_matrix(data):
    # Convert texts to vector matrix (word frequency)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(data['features_for_ml'])
    
    # Calculate cosine similarity between all vectors
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

cosine_sim = compute_similarity_matrix(df)

def get_recommendations(title, cosine_sim=cosine_sim, df=df):
    title_lower = title.lower().strip()
    
    # Search for title index
    indices = pd.Series(df.index, index=df['title_lower']).drop_duplicates()
    
    if title_lower not in indices:
        return None
        
    idx = indices[title_lower]
    
    # Select first match if there are duplicates
    if isinstance(idx, pd.Series):
        idx = idx.iloc[0]
        
    # Get similarity scores and sort them
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Top 5 recommendations (ignoring the 0 index which is the queried title itself)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    
    return df.iloc[movie_indices][['title', 'type', 'listed_in', 'description']]

# 4. Main Interface (Sidebar Menu)
menu = st.sidebar.selectbox(
    "Navigation Menu",
    ["AI Recommendations", "General Search", "General Statistics", "Original App Features"]
)

if menu == "General Search":
    st.subheader("Quick Catalog Search")
    search_type = st.radio("Search by:", ["Actor/Director", "Genre"])
    query = st.text_input("Enter your search (e.g., DiCaprio, Action):")
    
    if query:
        query = query.lower()
        if search_type == "Actor/Director":
            results = df[(df['cast'].str.lower().str.contains(query, na=False)) | 
                         (df['director'].str.lower().str.contains(query, na=False))]
        else:
            results = df[df['listed_in'].str.lower().str.contains(query, na=False)]
            
        st.write(f"Found **{len(results)}** results:")
        st.dataframe(results[['title', 'type', 'director', 'cast', 'listed_in']])

elif menu == "AI Recommendations":
    st.subheader("🤖 Smart Content Recommender AI")
    st.write("Enter the title of a movie or series you like. The NLP model will analyze descriptions, genres, and cast to suggest exact mathematical similarities.")
    
    movie_input = st.selectbox("Search and select a title:", [""] + list(df['title'].values))
    
    if movie_input:
        recs = get_recommendations(movie_input)
        if recs is not None:
            st.success(f"Applying Machine Learning (TF-IDF & Cosine Similarity)... Because you watched **{movie_input}**, we recommend:")
            for idx, row in recs.iterrows():
                st.markdown(f"### 🎬 {row['title'].title()} ({row['type'].upper()})")
                st.markdown(f"**Genre:** {row['listed_in']}")
                st.markdown(f"*{row['description']}*")
                st.markdown("---")
        else:
            st.warning("Title not found.")

elif menu == "General Statistics":
    st.subheader("Catalog Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Total Titles by Type")
        type_counts = df['type'].value_counts().reset_index()
        type_counts.columns = ['Type', 'Count']
        
        fig1 = px.pie(type_counts, names='Type', values='Count', hole=0.5,
                      color_discrete_sequence=['#e50914', '#564d4d'])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                           font=dict(color='white'), margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.write("### Top 10 Most Common Genres")
        all_genres = df['listed_in'].str.split(',').explode().str.strip()
        genre_counts = all_genres.value_counts().head(10).reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        fig2 = px.bar(genre_counts, x='Genre', y='Count', text='Count',
                      color_discrete_sequence=['#e50914'])
        fig2.update_layout(xaxis_title="", yaxis_title="",
                           paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                           font=dict(color='white'), margin=dict(t=0, b=0, l=0, r=0))
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

elif menu == "Original App Features":
    st.subheader("Legacy App Features (`aplicacionnetflix.py`)")
    st.info("This section directly imports and communicates with your original `aplicacionnetflix.py` python script! It leverages your custom code.")
    
    feature = st.radio("Select an Original Feature:", 
                       ["1. Random Title Generator", "2. Recommendations by Exact Duration"])
    
    if feature == "1. Random Title Generator":
        if st.button("Spin the Wheel! 🎲"):
            # Using your original function!
            random_movie = original_app.peliculas_al_azar(1) 
            st.write("Here is your random pick generated safely by your original logic:")
            st.dataframe(random_movie)
            
    elif feature == "2. Recommendations by Exact Duration":
        dur_input = st.number_input("Enter desired movie duration in minutes:", min_value=1, value=90)
        if st.button("Find Movie by Duration"):
            # Using your original function!
            matches = original_app.recomendaciones_por_duracion(dur_input)
            if matches is not None and not matches.empty:
                st.success("Found match directly from your custom logic!")
                st.dataframe(matches)
            else:
                st.warning("No matches found for that exact duration.")
