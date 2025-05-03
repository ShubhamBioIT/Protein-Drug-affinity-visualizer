import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64


st.set_page_config(page_title="BindingDB Interaction Explorer", layout="wide")

st.title("🔬 Bioinformatics Drug-Target Interaction Explorer")
st.markdown("Upload your BindingDB dataset to explore ligand-target interactions interactively.")

# --- Sample CSV download ---
def download_sample_csv(file_path, download_name):
    with open(file_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{download_name}">📥 Download Sample CSV</a>'
    return href

# Sample CSV download section
st.markdown("---")
st.markdown("### 📘 Need Help Getting Started?")
st.markdown(download_sample_csv('bindingdb_sample.csv', 'bindingdb_sample.csv'), unsafe_allow_html=True)
st.markdown("---")

# --- File Upload ---
uploaded_file = st.file_uploader("📤 Upload your BindingDB CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df['Ki (nM)'] = pd.to_numeric(df['Ki (nM)'], errors='coerce')
    df = df.dropna(subset=['Target Name', 'Ligand SMILES', 'Ki (nM)'])


    def interaction_score(ki):
        if pd.isnull(ki) or ki <= 0:
            return 0
        # Log-scale scoring: lower Ki gives higher score
        score = max(0, 100 - 25 * np.log10(ki))
        return round(score, 2)


    df['Interaction Score'] = df['Ki (nM)'].apply(interaction_score)

    st.subheader("📋 Sample Ki Values and Scores")
    st.dataframe(df[['Target Name', 'Ligand SMILES', 'Ki (nM)', 'Interaction Score']].head(20))

    # --- Top 10 Targets ---
    st.subheader("🎯 Top 10 Protein Targets by Avg Interaction Score")
    top_targets = df.groupby('Target Name', as_index=False)['Interaction Score'].mean()
    top_targets = top_targets.sort_values(by='Interaction Score', ascending=False).head(10)

    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_targets, x='Interaction Score', y='Target Name', palette="Blues_d", ax=ax1)
    ax1.set_title("Top 10 Targets (Avg Interaction Score)", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Average Interaction Score")
    ax1.set_ylabel("Target Name")
    for patch in ax1.patches:
        ax1.text(patch.get_width() + 1, patch.get_y() + 0.4, f'{patch.get_width():.1f}', fontsize=10)
    ax1.grid(axis='x', linestyle='--', alpha=0.6)
    st.pyplot(fig1)

    # --- Top 10 Ligands ---
    st.subheader("🧪 Top 10 Ligands by Avg Interaction Score")
    top_ligands = df.groupby('Ligand SMILES', as_index=False)['Interaction Score'].mean()
    top_ligands = top_ligands.sort_values(by='Interaction Score', ascending=False).head(10)

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.barplot(data=top_ligands, x='Interaction Score', y='Ligand SMILES', palette="Greens_d", ax=ax2)
    ax2.set_title("Top 10 Ligands (Avg Interaction Score)", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Average Interaction Score")
    ax2.set_ylabel("Ligand SMILES")
    for patch in ax2.patches:
        ax2.text(patch.get_width() + 1, patch.get_y() + 0.4, f'{patch.get_width():.1f}', fontsize=10)
    ax2.grid(axis='x', linestyle='--', alpha=0.6)
    st.pyplot(fig2)



    # --- Detailed Explanation & Scoring System ---
    st.markdown("""
### ℹ️ Graph Descriptions
- **Target Graph**: Displays top protein targets with the strongest average drug binding.
- **Ligand Graph**: Highlights ligands (drugs) with the most potent binding across multiple targets.

---

### 📊 Ki-Based Binding Affinity Scoring System
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

### 🔍 Insights
- Identify **potent drug candidates** based on Ki.
- Analyze **target-ligand selectivity** profiles.
- Useful for **drug screening**, **lead optimization**, and **machine learning pipeline preparation**.
""")


else:
    st.warning("👆 Upload a CSV file to visualize the interaction scores.")
