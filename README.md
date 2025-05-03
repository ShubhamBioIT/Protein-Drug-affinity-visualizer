# 🔬 Drug-Target Binding Affinity Visualizer

This is a **Streamlit-based interactive application** for visualizing drug-protein binding interactions using real-world bioinformatics data from the **BindingDB** database. It analyzes binding affinity scores (`Ki` values) and presents informative graphs to help researchers explore strong drug-target candidates.

---

## 📊 Project Overview

- **Goal**: Analyze and visualize ligand-target interactions using Ki values.
- **Data Source**: [BindingDB](https://www.bindingdb.org/)
- **Key Technologies**: Python, Pandas, NumPy, Streamlit, Matplotlib/Seaborn

---

## 🚀 Features

- 📥 Upload your own BindingDB CSV dataset.
- 📈 Visualize top ligands and their binding targets.
- 🧠 See drug-protein binding strength using intuitive scoring.
- 💾 Download sample CSV to test the app.
- 🧬 Customize or extend with machine learning later.

---

## ⚗️ Binding Affinity Scoring System

| Ki (nM) Range     | Score | Interpretation       |
|------------------|--------|----------------------|
| Ki < 10          | 100    | Very Strong Binding  |
| 10 ≤ Ki < 100    | 70     | Strong Binding       |
| 100 ≤ Ki < 1000  | 40     | Moderate Binding     |
| Ki ≥ 1000        | 10     | Weak Binding         |

> Lower Ki = Higher Binding Affinity  
> Helps identify **potent drug candidates** in drug discovery pipelines.

---

## 💡 How to Run Locally

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/bioaffinity-visualizer.git
   cd Protein-Drug-affinity-visualizer
# Protein-Drug-affinity-visualizer
