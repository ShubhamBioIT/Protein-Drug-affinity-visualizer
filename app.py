import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# --- Page Configuration ---
st.set_page_config(page_title="BindingDB Interaction Explorer", layout="wide")

# --- Title and Intro ---
st.title("🔬 Bioinformatics Drug-Target Interaction Explorer")
st.markdown("Upload your **BindingDB-style dataset** to explore ligand-target interaction scores based on Ki values.")

# --- Download Sample File ---
def download_sample_csv(file_path, download_name):
    with open(file_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{download_name}">📥 Download Sample CSV</a>'

st.sidebar.markdown("### 📘 Help")
st.sidebar.markdown("Upload a file containing columns: `Target Name`, `Ligand SMILES`, and `Ki (nM)`.")
st.sidebar.markdown(download_sample_csv('bindingdb_sample.csv', 'bindingdb_sample.csv'), unsafe_allow_html=True)

# --- File Upload ---
uploaded_file = st.file_uploader("📤 Upload your BindingDB CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # --- Preprocessing ---
    df['Ki (nM)'] = pd.to_numeric(df['Ki (nM)'], errors='coerce')
    df.dropna(subset=['Target Name', 'Ligand SMILES', 'Ki (nM)'], inplace=True)

    def interaction_score(ki):
        if pd.isnull(ki) or ki <= 0:
            return 0
        return round(max(0, 100 - 25 * np.log10(ki)), 2)

    df['Interaction Score'] = df['Ki (nM)'].apply(interaction_score)

    # --- Display Sample Data ---
    st.subheader("📄 Sample Dataset View")
    st.dataframe(df[['Target Name', 'Ligand SMILES', 'Ki (nM)', 'Interaction Score']].head(20), use_container_width=True)

    # --- Top 10 Targets ---
    st.subheader("🎯 Top 10 Protein Targets by Avg Interaction Score")
    top_targets = df.groupby('Target Name')['Interaction Score'].mean().reset_index()
    top_targets = top_targets.sort_values(by='Interaction Score', ascending=False).head(10)

    fig1, ax1 = plt.subplots(figsize=(12, 6), dpi=120)
    sns.barplot(data=top_targets, x='Interaction Score', y='Target Name', palette="Blues_d", ax=ax1)
    ax1.set_title("Top 10 Targets with Highest Avg Interaction Score", fontsize=14)
    ax1.set_xlabel("Average Interaction Score", fontsize=12)
    ax1.set_ylabel("Target Name", fontsize=12)
    for patch in ax1.patches:
        ax1.text(patch.get_width() + 1, patch.get_y() + 0.3, f'{patch.get_width():.1f}', fontsize=10)
    ax1.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig1)

    # --- Top 10 Ligands ---
    st.subheader("🧪 Top 10 Ligands by Avg Interaction Score")
    top_ligands = df.groupby('Ligand SMILES')['Interaction Score'].mean().reset_index()
    top_ligands = top_ligands.sort_values(by='Interaction Score', ascending=False).head(10)

    fig2, ax2 = plt.subplots(figsize=(12, 6), dpi=120)
    sns.barplot(data=top_ligands, x='Interaction Score', y='Ligand SMILES', palette="Greens_d", ax=ax2)
    ax2.set_title("Top 10 Ligands with Highest Avg Interaction Score", fontsize=14)
    ax2.set_xlabel("Average Interaction Score", fontsize=12)
    ax2.set_ylabel("Ligand SMILES", fontsize=12)
    for patch in ax2.patches:
        ax2.text(patch.get_width() + 1, patch.get_y() + 0.3, f'{patch.get_width():.1f}', fontsize=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.5)
    st.pyplot(fig2)

    # --- Swarm Plot of Score Distribution for Top 10 Targets ---
    st.subheader("🐝 Interaction Score Spread Across Top 10 Targets (Swarm Plot)")
    top_target_names = top_targets['Target Name'].tolist()
    filtered_df = df[df['Target Name'].isin(top_target_names)]

    fig3, ax3 = plt.subplots(figsize=(14, 6), dpi=120)
    sns.swarmplot(data=filtered_df, x='Target Name', y='Interaction Score', palette='husl', size=5, ax=ax3)
    ax3.set_title("Individual Interaction Scores for Top Targets", fontsize=14)
    ax3.set_xlabel("Target Name", fontsize=12)
    ax3.set_ylabel("Interaction Score", fontsize=12)
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis='y', linestyle='--', alpha=0.6)
    st.pyplot(fig3)


    # --- Score Distribution Histogram ---
    st.subheader("📈 Overall Interaction Score Distribution")
    fig4, ax4 = plt.subplots(figsize=(10, 4), dpi=120)
    sns.histplot(df['Interaction Score'], bins=20, kde=True, ax=ax4, color='purple')
    ax4.set_title("Distribution of Interaction Scores", fontsize=14)
    ax4.set_xlabel("Interaction Score")
    ax4.set_ylabel("Frequency")
    ax4.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig4)

    # --- Descriptions and Explanation ---
    st.markdown("""
---

### 🧠 Graph Descriptions

- **Top Targets**: Average scores show which proteins bind most strongly with ligands.
- **Top Ligands**: Shows which drug-like compounds have highest average binding.
- **Swarm Plot**: 
    - Shows individual interaction scores (based on Ki) for top targets.
    - Each dot = 1 ligand-protein interaction.
    - Wider spread = more variability in binding.
- **Histogram**: Helps visualize distribution of all interaction strengths.

---

### 📊 Scoring System – Based on Ki (nM)

| Ki (nM) Range     | Approx. Score     | log10(Ki)     | Interpretation              |
|------------------|-------------------|---------------|-----------------------------|
| Ki ≤ 1           | ≈ 100             | ≤ 0           | 🔥 Exceptional Binding       |
| 1 < Ki ≤ 10      | 75 – 100          | 0 – 1         | ✅ Very Strong Binding       |
| 10 < Ki ≤ 100    | 50 – 75           | 1 – 2         | ⚡ Strong Binding            |
| 100 < Ki ≤ 1000  | 25 – 50           | 2 – 3         | ⚠️ Moderate Binding          |
| Ki > 1000        | < 25              | > 3           | 🔻 Weak or No Binding        |
| Missing/Invalid  | 0                 | —             | ❌ Data Missing or Invalid   |

💡 **Score Formula**: `Score = 100 - 25 × log10(Ki)`  
📉 Lower Ki ➝ Higher Binding Affinity ➝ Higher Score

---

### 🧪 Use Cases
- Identify **potent drug candidates**
- Understand **target-ligand selectivity**
- Preprocess interaction data for **machine learning models**
- Use scores as labels in **classification/regression pipelines**

---
""")

else:
    st.warning("👆 Upload a BindingDB-style CSV file with valid `Ki (nM)` values to begin analysis.")
