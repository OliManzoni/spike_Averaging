import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Manzoni Lab - Averaged Curves", layout="wide")

# --- GESTION DU BILINGUISME ---
st.sidebar.header("🌍 Language / Langue")
lang = st.sidebar.radio("Select Interface Language:", ["Français", "English"])

# --- DICTIONNAIRE DE TRADUCTION ---
T = {
    "title": {"Français": "Courbes Moyennées f-I & I-V", "English": "Averaged f-I & I-V Curves"},
    "subtitle": {"Français": "Analyse de Population & Excitabilité | Manzoni Lab", "English": "Population Analysis & Excitability | Manzoni Lab"},
    "upload": {"Français": "📂 1. Charger les fichiers", "English": "📂 1. Upload Files"},
    "upload_help": {"Français": "Sélectionnez plusieurs fichiers terminant par '_Sweeps.csv'", "English": "Select multiple files ending in '_Sweeps.csv'"},
    "settings": {"Français": "⚙️ 2. Paramètres Visuels", "English": "⚙️ 2. Visual Settings"},
    "err_type": {"Français": "Type d'Erreur (Ombrage)", "English": "Error Type (Shading)"},
    "err_sem": {"Français": "SEM (Erreur Standard)", "English": "SEM (Standard Error)"},
    "err_ci": {"Français": "CI (95% Confiance)", "English": "CI (95% Confidence)"},
    "tab_graphs": {"Français": "📈 Visualisation des Courbes", "English": "📈 Curve Visualization"},
    "tab_data": {"Français": "🔢 Données Moyennées (Export)", "English": "🔢 Averaged Data (Export)"},
    "tab_howto": {"Français": "📚 Mode d'Emploi (How-To)", "English": "📚 User Guide (How-To)"},
    "export_btn": {"Français": "💾 Exporter les Moyennes (CSV)", "English": "💾 Export Averages (CSV)"},
    "fi_title": {"Français": "Courbe d'Excitabilité (f-I)", "English": "Excitability Curve (f-I)"},
    "iv_title": {"Français": "Relation Courant-Voltage (I-V)", "English": "Current-Voltage Relation (I-V)"},
}

# --- EN-TÊTE INSTITUTIONNEL ---
col_l, col_r = st.columns([2, 5]) 
with col_l:
    try: 
        st.image("logo_chavis_final.png", width=360) 
    except: 
        st.info("Manzoni Lab - Neurosciences") 
with col_r:
    st.markdown(f"# {T['title'][lang]}")
    st.markdown(f"### {T['subtitle'][lang]}")

st.divider()

# --- BARRE LATÉRALE ---
st.sidebar.header(T["upload"][lang])
uploaded_files = st.sidebar.file_uploader(
    T["upload_help"][lang], 
    type=["csv"], 
    accept_multiple_files=True
)

st.sidebar.header(T["settings"][lang])
error_choice = st.sidebar.radio(
    T["err_type"][lang], 
    [T["err_sem"][lang], T["err_ci"][lang]]
)
# Définition du paramètre Seaborn en fonction du choix
err_bar_style = 'se' if error_choice == T["err_sem"][lang] else ('ci', 95)

# --- CORPS DE L'APPLICATION ---
if not uploaded_files:
    # Affiche un message d'attente stylisé
    st.info("👈 " + ("Veuillez charger vos fichiers '_Sweeps.csv' dans le menu latéral pour commencer." if lang == "Français" else "Please upload your '_Sweeps.csv' files in the sidebar to begin."))
else:
    # 1. Traitement des données
    df_list = []
    cell_count = 0
    
    for f in uploaded_files:
        # Sécurité : on ne prend que les fichiers qui semblent être des sweeps
        if "Sweeps" in f.name or "sweeps" in f.name.lower():
            df = pd.read_csv(f)
            # Ajout d'une colonne avec le nom du fichier (sans l'extension) pour identifier la cellule
            df['Cell_ID'] = f.name.replace("_Sweeps.csv", "").replace(".csv", "")
            df_list.append(df)
            cell_count += 1
            
    if not df_list:
        st.error("Aucun fichier valide trouvé. Assurez-vous qu'ils contiennent 'Sweeps' dans leur nom." if lang == "Français" else "No valid files found. Ensure they contain 'Sweeps' in the filename.")
    else:
        # Fusion de toutes les cellules en un seul DataFrame
        master_df = pd.concat(df_list, ignore_index=True)
        
        # Vérification des colonnes nécessaires (générées par le code Spike)
        required_cols = ['I_inj', 'Nb_Spikes', 'V_steady']
        if not all(col in master_df.columns for col in required_cols):
            st.error(f"Format incorrect. Les colonnes suivantes sont requises : {required_cols}")
        else:
            st.success(f"✅ {cell_count} " + ("cellules fusionnées avec succès." if lang == "Français" else "cells successfully merged."))
            
            # --- ONGLETS ---
            tab1, tab2, tab3 = st.tabs([T["tab_graphs"][lang], T["tab_data"][lang], T["tab_howto"][lang]])

            # --- ONGLET 1 : GRAPHIQUES ---
            with tab1:
                plt.style.use('seaborn-v0_8-white')
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
                
                # Sous-échantillonnage pour la courbe f-I : on ignore les courants hyperpolarisants (négatifs)
                df_depol = master_df[master_df['I_inj'] >= 0]
                
                # Graphe f-I
                sns.lineplot(
                    data=df_depol, x='I_inj', y='Nb_Spikes', 
                    errorbar=err_bar_style, err_style="band", 
                    marker='o', color='firebrick', ax=ax1, linewidth=2
                )
                ax1.set_title(T["fi_title"][lang], fontweight='bold')
                ax1.set_xlabel("Injected Current (nA/pA)")
                ax1.set_ylabel("Spike Count (Hz)")
                ax1.grid(True, linestyle='--', alpha=0.5)

                # Graphe I-V
                sns.lineplot(
                    data=master_df, x='I_inj', y='V_steady', 
                    errorbar=err_bar_style, err_style="band", 
                    marker='s', color='royalblue', ax=ax2, linewidth=2
                )
                ax2.set_title(T["iv_title"][lang], fontweight='bold')
                ax2.set_xlabel("Injected Current (nA/pA)")
                ax2.set_ylabel("Steady-State Voltage (mV)")
                ax2.grid(True, linestyle='--', alpha=0.5)
                
                sns.despine()
                st.pyplot(fig)

            # --- ONGLET 2 : DONNÉES ET EXPORT ---
            with tab2:
                # Calcul manuel des statistiques pour le tableau d'export
                st.markdown("### " + ("Données Consolideés par Échelon de Courant" if lang == "Français" else "Consolidated Data per Current Step"))
                
                # Grouper par I_inj et calculer la moyenne et l'erreur standard
                stats_df = master_df.groupby('I_inj').agg(
                    N_Cells=('Cell_ID', 'nunique'),
                    Nb_Spikes_Mean=('Nb_Spikes', 'mean'),
                    Nb_Spikes_SEM=('Nb_Spikes', 'sem'),
                    V_steady_Mean=('V_steady', 'mean'),
                    V_steady_SEM=('V_steady', 'sem')
                ).reset_index()
                
                # Calcul de l'intervalle de confiance (CI) approximatif (1.96 * SEM)
                stats_df['Nb_Spikes_95CI'] = stats_df['Nb_Spikes_SEM'] * 1.96
                stats_df['V_steady_95CI'] = stats_df['V_steady_SEM'] * 1.96
                
                # Formatage esthétique pour l'affichage (arrondi)
                display_df = stats_df.copy()
                display_cols = ['I_inj', 'N_Cells', 'Nb_Spikes_Mean', 'Nb_Spikes_SEM', 'V_steady_Mean', 'V_steady_SEM']
                st.dataframe(display_df[display_cols].style.format(precision=2), use_container_width=True)
                
                # Bouton d'export
                csv_export = stats_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=T["export_btn"][lang],
                    data=csv_export,
                    file_name="Averaged_IV_FI_ManzoniLab.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            # --- ONGLET 3 : HOW-TO (ONBOARDING) ---
            with tab3:
                if lang == "Français":
                    st.markdown("""
                    ### 🔬 Mode d'Emploi : Courbes Moyennées (Batch Plotting)
                    
                    Cette application fait suite à la pipeline d'Excitabilité individuelle (Spike Analysis). Elle sert à combiner visuellement et statistiquement les résultats de **plusieurs cellules**.
                    
                    #### 📋 Étapes d'utilisation :
                    1. **Extraction préalable :** Assurez-vous d'avoir passé vos fichiers ABF dans le code `2_⚡_Spike_Analysis.py` et d'avoir cliqué sur *Export Sweep Data*. Vous devriez avoir des fichiers nommés par exemple `WT_cell1_Sweeps.csv`, `WT_cell2_Sweeps.csv`, etc.
                    2. **Chargement :** Glissez-déposez **tous les fichiers `_Sweeps.csv`** d'une même condition (ex: tous vos WT en même temps) dans la barre latérale.
                    3. **Visualisation :** L'application va automatiquement aligner les échelons de courant (`I_inj`) et moyenner le nombre de potentiels d'action et les voltages stationnaires.
                    4. **Erreurs (SEM vs CI) :** * **SEM** représente l'erreur standard de la moyenne (préféré pour montrer la précision de votre estimation).
                        * **CI (95%)** représente l'intervalle de confiance (souvent exigé par *Science* ou *Nature* pour montrer la dispersion de la population).
                    5. **Export :** Allez dans l'onglet "Données Moyennées" pour télécharger le tableau Excel final contenant les $Moyennes \pm SEM$, prêt pour GraphPad Prism.
                    
                    **Note :** Pour la courbe f-I, l'algorithme masque automatiquement les injections de courant négatives (hyperpolarisantes) afin de garder un graphique propre démarrant à 0 pA.
                    """)
                else:
                    st.markdown("""
                    ### 🔬 How-To: Averaged Curves (Batch Plotting)
                    
                    This application acts as the final step after the individual Excitability pipeline (Spike Analysis). It is used to visually and statistically combine results from **multiple cells**.
                    
                    #### 📋 Workflow:
                    1. **Prior Extraction:** Make sure you have processed your ABF files through the `2_⚡_Spike_Analysis.py` code and clicked *Export Sweep Data*. You should have files named e.g., `WT_cell1_Sweeps.csv`, `WT_cell2_Sweeps.csv`, etc.
                    2. **Upload:** Drag and drop **all `_Sweeps.csv` files** belonging to a single experimental condition (e.g., all your WT cells at once) into the sidebar.
                    3. **Visualization:** The app automatically aligns the current steps (`I_inj`) and averages the action potential counts and steady-state voltages across all cells.
                    4. **Error Bars (SEM vs CI):** * **SEM** (Standard Error of the Mean) is preferred to show the precision of your mean estimate.
                        * **CI (95%)** (Confidence Interval) is often required by high-tier journals (*Science*, *Nature*) to display population dispersion.
                    5. **Export:** Go to the "Averaged Data" tab to download the final CSV containing $Means \pm SEM$, perfectly formatted for GraphPad Prism.
                    
                    **Note:** For the f-I curve, the algorithm automatically hides negative (hyperpolarizing) current injections to maintain a clean graph starting at 0 pA.
                    """)
