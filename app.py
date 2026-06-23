import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 200
plt.rcParams['savefig.dpi'] = 300

from Generateur import agents
from simulateur import simuler_monte_carlo

# ===================== CONFIGURATION =====================
st.set_page_config(
    page_title="Simulateur Monte Carlo",
    page_icon="🇲🇷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== HEADER AVEC LOGO MAURITANIE =====================
import base64


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# Le logo est maintenant dans le même dossier que app.py
logo_path = "logo_mauritanie.png"
logo_b64 = get_base64_image(logo_path)

st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0 12px 0;">
<div style="flex:1;display:flex;align-items:center;gap:12px;">
<img src="data:image/png;base64,{logo_b64}" style="height:65px;">
<div>
<div style="font-size:10px;color:#6B7280;">RÉPUBLIQUE ISLAMIQUE DE MAURITANIE</div>
<div style="font-weight:700;color:#14532D;font-size:13px;">Ministère de la Fonction Publique<br>et du Travail</div>
</div>
</div>
<div style="flex:2;text-align:center;">
<h1 style="color:#14532D;margin:0;font-size:1.9rem;font-weight:800;white-space:nowrap;line-height:1.2;">Carrières des Fonctionnaires</h1>
<p style="color:#6B7280;margin:4px 0 0 0;font-size:13px;">Loi N°93-09 • DSIS / MFPT • Mauritanie</p>
</div>
<div style="flex:1;"></div>
</div>
<hr style="margin:0 0 6px 0;border:2px solid #1B8A4C;">
""", unsafe_allow_html=True)
#← TRÈS IMPORTANT, ceci doit être présent !
# ===================== CSS PERSONNALISÉ =====================

st.markdown("""
<style>

/* ---------- GLOBAL ---------- */

.stApp{
    background:#F4F6F4;
}

footer{
    visibility:hidden;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"]{
    background:#FAFBFA !important;
    border-right:1px solid #E5EAE6 !important;
    overflow:hidden !important;
}

section[data-testid="stSidebar"] .block-container{
    padding-top:0rem !important;
}

[data-testid="stSidebar"] > div:first-child{
    padding-top:0px !important;
    margin-top:-25px 
}

[data-testid="stSidebarContent"]{
    overflow-y:hidden !important;
    overflow-x:hidden !important;
}

[data-testid="stSidebar"] .stSlider{
    margin-top:-8px !important;
    margin-bottom:-8px !important;
}

[data-testid="stSidebar"] h3{
    margin-top:4px !important;
    margin-bottom:4px !important;
}

[data-testid="stSidebar"] p{
    margin-bottom:2px !important;
}

[data-testid="stSidebar"] .stMarkdown{
    margin-bottom:0px !important;
}

[data-testid="stSidebar"] p{
    margin-top:0px !important;
    margin-bottom:2px !important;
}

[data-testid="stSidebar"] .stMarkdown{
    margin-top:0px !important;
    margin-bottom:0px !important;
}

[data-testid="stSidebar"] .stSlider{
    padding-top:0px !important;
    padding-bottom:0px !important;
    margin-top:-12px !important;
    margin-bottom:-12px !important;
}

[data-testid="stSidebar"] hr{
    margin:4px 0px !important;
}

section[data-testid="stSidebar"] .block-container{
    padding-top:0rem !important;
    padding-bottom:0rem !important;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3{
    margin-top:0px !important;
    margin-bottom:2px !important;
}

/* ---------- MAIN ---------- */

/* ---------- MAIN ---------- */
.main .block-container,
.block-container,
[data-testid="stMainBlockContainer"],
[data-testid="stAppViewBlockContainer"]{
    max-width:none !important;
    padding-top:3.5rem !important;
    padding-left:1.5rem !important;
    padding-right:1.5rem !important;
    padding-bottom:1rem !important;
}



/* ---------- TITRE ---------- */

h1{
    font-size:1.5rem !important;
    font-weight:800 !important;
    color:#14532D !important;
    line-height:1.1 !important;
    margin-top:0px !important;
    margin-bottom:0px !important;
    padding-top:0px !important;
}
h2,h3{
    color:#1F2937 !important;
}

/* ---------- BUTTON ---------- */

.stButton button{
    width:100% !important;
    height:42px !important;
    border-radius:12px !important;
    background:#1B8A4C !important;
    border:none !important;
    color:white !important;
    font-size:15px !important;
    font-weight:700 !important;
    margin-top:-75px !important;
}

.stButton button:hover{
    background:#166534 !important;
}

/* ---------- SLIDER ---------- */

.stSlider [role="slider"]{
    background:#1B8A4C !important;
}

.stSlider [data-testid="stTickBar"]{
    display:none !important;
}

/* ---------- DATAFRAME ---------- */

[data-testid="stDataFrame"]{
    border-radius:20px !important;
    overflow:hidden !important;
}

/* ---------- TABS ---------- */

button[role="tab"]{
    font-size:18px !important;
    font-weight:600 !important;
}

button[role="tab"][aria-selected="true"]{
    color:#1B8A4C !important;
}

/* ---------- SCROLL ---------- */

::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-thumb{
    background:#C8D0CA;
    border-radius:10px;
}

::-webkit-scrollbar-track{
    background:#F3F4F6;
}

/* ---------- GLOBAL ---------- */
.stApp{
    background:#F4F6F4;
}

footer{
    visibility:hidden;   /* on cache SEULEMENT le footer, plus le menu */
}

/* ---------- RADIO SEGMENTED ---------- */
[data-testid="stSidebar"] [role="radiogroup"] {
    background: #EFEFEF !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    width: 100% !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    flex: 1 !important;
    text-align: center !important;
    border-radius: 10px !important;
    padding: 6px 0px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #6B7280 !important;
    background: transparent !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label[data-selected="true"],
[data-testid="stSidebar"] [data-baseweb="radio"] input:checked + div {
    background: white !important;
    color: #14532D !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.10) !important;
}

/* Cacher les cercles radio */
[data-testid="stSidebar"] [role="radiogroup"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [role="radiogroup"] svg {
    display: none !important;
}

/* Boutons projection normaux */
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    color: #6B7280 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    border-radius: 10px !important;
    border: none !important;
    box-shadow: none !important;
    height: 36px !important;
    margin-top: 0px !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: white !important;
    color: #14532D !important;
}

/* Bouton Lancer la simulation */
[data-testid="stSidebar"] .stButton:last-child button {
    background: #1B8A4C !important;
    color: white !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    height: 50px !important;
    border-radius: 14px !important;
}

[data-testid="stSidebar"] .stButton:last-child button:hover {
    background: #14532D !important;
}

/* container gris autour des boutons */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    background: #EFEFEF !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
}

</style>
""", unsafe_allow_html=True)

# ===================== CONSTANTES =====================
N_RUNS = 100
VERT  = "#1B8A4C"
ROUGE = "#C0392B"



# ===================== POPULATION INITIALE =====================
actifs_initiaux = sum(1 for a in agents if a['statut'] == 'Actif')

# ===================== SIDEBAR =====================
st.sidebar.markdown("""
<h2 style='margin-top:0px;margin-bottom:8px;'>
⚙️ Paramètres
</h2>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"👥 **Population : {actifs_initiaux:,} agents actifs**")
st.sidebar.markdown(f"🎲 **Monte Carlo : {N_RUNS} réplications**")

# -- Projection segmented control --

if 'n_annees' not in st.session_state:
    st.session_state.n_annees = 5

col_a, col_b, col_c = st.sidebar.columns(3)

options = {1: "1 an", 5: "5 ans", 10: "10 ans"}

with col_a:
    if st.button("1 an", key="btn1", use_container_width=True):
        st.session_state.n_annees = 1
with col_b:
    if st.button("5 ans", key="btn5", use_container_width=True):
        st.session_state.n_annees = 5
with col_c:
    if st.button("10 ans", key="btn10", use_container_width=True):
        st.session_state.n_annees = 10

# Afficher lequel est sélectionné avec du HTML
selected = st.session_state.n_annees
st.sidebar.markdown(f"""
<style>
/* Highlight bouton actif selon session */
</style>
<div style="
    display:flex; gap:2px;
    background:#EFEFEF; border-radius:12px; padding:4px;
    margin-top:-60px; position:relative; z-index:0; pointer-events:none;
">
    <div style="flex:1;text-align:center;padding:7px 0;border-radius:10px;font-size:13px;font-weight:{'700' if selected==1 else '600'};
        background:{'white' if selected==1 else 'transparent'};
        color:{'#14532D' if selected==1 else '#6B7280'};
        box-shadow:{'0 1px 4px rgba(0,0,0,0.12)' if selected==1 else 'none'};">
        1 an
    </div>
    <div style="flex:1;text-align:center;padding:7px 0;border-radius:10px;font-size:13px;font-weight:{'700' if selected==5 else '600'};
        background:{'white' if selected==5 else 'transparent'};
        color:{'#14532D' if selected==5 else '#6B7280'};
        box-shadow:{'0 1px 4px rgba(0,0,0,0.12)' if selected==5 else 'none'};">
        5 ans
    </div>
    <div style="flex:1;text-align:center;padding:7px 0;border-radius:10px;font-size:13px;font-weight:{'700' if selected==10 else '600'};
        background:{'white' if selected==10 else 'transparent'};
        color:{'#14532D' if selected==10 else '#6B7280'};
        box-shadow:{'0 1px 4px rgba(0,0,0,0.12)' if selected==10 else 'none'};">
        10 ans
    </div>
</div>
""", unsafe_allow_html=True)

n_annees = st.session_state.n_annees

st.sidebar.markdown("### - Mon scénario")
age_retraite_custom = st.sidebar.slider(
    "Âge de retraite",
    min_value=55, max_value=70, value=63,
    help="63 ans selon Loi 93-09 Art. 72"
)

duree_anciennete_custom = st.sidebar.slider(
    "Durée ancienneté (ans)",
    min_value=1, max_value=5, value=2,
    help="2 ans selon Loi 93-09 Art. 61"
)

nb_recrutements_custom = st.sidebar.slider(
    "Recrutements par an",
    min_value=0, max_value=1000, step=100, value=0
)

# ===================== HELPER (mise en cache) =====================
@st.cache_data(show_spinner=False)
def run_mc(_agents, n_annees, age_retraite, duree_anciennete, nb_recrutements, n_runs):
    return simuler_monte_carlo(
        _agents, n_annees,
        n_runs=n_runs,
        age_retraite=age_retraite,
        duree_anciennete=duree_anciennete,
        nb_recrutements=nb_recrutements,
    )


def serie(scen, key):
    return [r[key]['moyenne'] for r in scen]


# ===================== LANCEMENT =====================
if st.sidebar.button("▶️ Lancer la simulation",
                     type="primary",
                     use_container_width=True):

    with st.spinner(f"⏳ Simulation Monte Carlo ({N_RUNS} runs)..."):
        ref = run_mc(agents, n_annees, 63, 2, 0, N_RUNS)
        mon = run_mc(
            agents, n_annees,
            age_retraite_custom,
            duree_anciennete_custom,
            nb_recrutements_custom,
            N_RUNS,
        )

    annees = [r['annee'] for r in ref]

    parametres_modifies = (
        age_retraite_custom != 63
        or duree_anciennete_custom != 2
        or nb_recrutements_custom != 0
    )

    # ===================== CARTES DE SYNTHÈSE =====================
    st.subheader("Résultats de scénario")
    st.caption(
        f"Âge de retraite = {age_retraite_custom} ans · "
        f"Ancienneté = {duree_anciennete_custom} ans · "
        f"Recrutements = {nb_recrutements_custom}/an"
    )

    actifs_fin = mon[-1]['actifs']['moyenne']
    tot_r = sum(r['retraites']['moyenne'] for r in mon)
    tot_a = sum(r['avancements']['moyenne'] for r in mon)
    tot_p = sum(r['promotions']['moyenne'] for r in mon)

    delta_actifs = actifs_fin - actifs_initiaux
    delta_color = "#C0392B" if delta_actifs < 0 else "#6B7280"
    delta_actifs_str = f"{delta_actifs:+,.0f} depuis 2026".replace(",", " ")


    def carte(label, valeur, sous_texte, delta_rouge=False):
        couleur_sous = "#C0392B" if delta_rouge else "#6B7280"
        return f"""
        <div style="
            background:white;
            border-radius:12px;
            padding:18px 24px;
            border:1px solid #E5E7EB;
            border-left:4px solid #1B8A4C;
            box-shadow:0 1px 4px rgba(0,0,0,0.05);
        ">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px;">
                <span style="width:8px;height:8px;background:#1B8A4C;border-radius:50%;display:inline-block;"></span>
                <span style="font-size:13px;font-weight:600;color:#374151;">{label}</span>
            </div>
            <div style="font-size:2.2rem;font-weight:800;color:#111827;line-height:1.1;">
                {valeur}
            </div>
            <div style="font-size:12px;font-weight:500;color:{couleur_sous};margin-top:8px;">
                {sous_texte}
            </div>
        </div>
        """


    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    with c1:
        st.markdown(carte(
            "👥 Actifs en fin de période",
            f"{actifs_fin:,.0f}".replace(",", " "),
            f"{delta_actifs:+,.0f} depuis 2026".replace(",", " "),
            delta_rouge=(delta_actifs < 0)
        ), unsafe_allow_html=True)

    with c2:
        st.markdown(carte(
            "🏦 Retraites (total)",
            f"{tot_r:,.0f}".replace(",", " "),
            f"{tot_r / n_annees:,.0f} / an en moyenne".replace(",", " "),
        ), unsafe_allow_html=True)

    with c3:
        st.markdown(carte(
            "📈 Avancements (total)",
            f"{tot_a:,.0f}".replace(",", " "),
            f"{tot_a / n_annees:,.0f} / an en moyenne".replace(",", " "),
        ), unsafe_allow_html=True)

    with c4:
        st.markdown(carte(
            "🎖️ Promotions (total)",
            f"{tot_p:,.0f}".replace(",", " "),
            f"{tot_p / n_annees:,.0f} / an en moyenne".replace(",", " "),
        ), unsafe_allow_html=True)
    # ===================== GRAPHIQUES =====================
    st.subheader("📈 Évolution année par année")

    if parametres_modifies:
        st.caption("🟢 Vert = mon scénario   |   🔴 Rouge = référence Loi 93-09 (63 ans)")
    else:
        st.caption("🟢 Vert = mon scénario (identique à la loi actuelle)")

    def graphe_simple(titre, key, ylabel):
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#F4F6F4')

        ax.plot(annees, serie(mon, key),
                marker='o', color=VERT, linewidth=2.5,
                label="Mon scénario")

        if parametres_modifies:
            ax.plot(annees, serie(ref, key),
                    marker='o', color=ROUGE, linewidth=2,
                    linestyle='--', label="Référence (loi actuelle)")

        ax.set_xlabel("Année", fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_xticks(annees)
        ax.legend(fontsize=9)
        ax.grid(alpha=0.35, color='#FFFFFF', linewidth=1.2)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E4E9E5')
        ax.spines['bottom'].set_color('#E4E9E5')
        ax.tick_params(colors='#7C8A82', labelsize=9)
        fig.tight_layout()
        return fig


    g1, g2 = st.columns([1, 1], gap="large")
    with g1:
        st.markdown("**👥 Agents actifs**")
        st.pyplot(graphe_simple("Actifs", 'actifs', "Nombre d'agents"))
    with g2:
        st.markdown("**🏦 Départs en retraite**")
        st.pyplot(graphe_simple("Retraites", 'retraites', "Retraites / an"))

    g3, g4 = st.columns([1, 1], gap="large")
    with g3:
        st.markdown("**📈 Avancements d'échelon**")
        st.pyplot(graphe_simple("Avancements", 'avancements', "Avancements / an"))
    with g4:
        st.markdown("**🎖️ Promotions de grade**")
        st.pyplot(graphe_simple("Promotions", 'promotions', "Promotions / an"))

    # ===================== COMMENT LIRE CES GRAPHES =====================
    with st.expander("🧭 Comment lire ces graphes"):
        st.markdown(
            """
- **La ligne verte** est mon scénario, celui que je configure avec les curseurs.
- **La ligne rouge en pointillés** (visible seulement si j'ai modifié un paramètre)
  est la référence : la loi appliquée telle quelle.
- **L'axe horizontal** est le temps. **L'axe vertical** est le nombre d'agents concernés.
- Si la ligne verte **s'écarte nettement** de la rouge → mon changement a un **effet réel**.

**À retenir :**
- **Retraites** : ne dépendent que de l'âge → grandeur certaine (aucun hasard).
- **Promotions** : notes tirées au hasard → grandeur la **plus incertaine**.
- **Avancements** : presque certains ; varient via les agents promus.
- **Actifs** : baissent avec les retraites, montent avec les recrutements.
            """
        )

    # ===================== TABLEAU DÉTAILLÉ =====================
    st.subheader("📋 Tableau détaillé de mon scénario")

    tabs = st.tabs(["👥 Actifs", "🏦 Retraites", "📈 Avancements", "🎖️ Promotions"])

    for tab, key, label in zip(
        tabs,
        ['actifs', 'retraites', 'avancements', 'promotions'],
        ['Actifs', 'Retraites', 'Avancements', 'Promotions']
    ):
        with tab:
            st.markdown(f"**{label} — moyenne et incertitude ({N_RUNS} simulations)**")
            df = pd.DataFrame({
                'Année'                 : annees,
                'Moyenne'               : [round(r[key]['moyenne'], 1) for r in mon],
                'Écart-type (hasard)'   : [round(r[key]['ecart_type'], 1) for r in mon],
                'Minimum probable (p05)': [round(r[key]['p05'], 1) for r in mon],
                'Maximum probable (p95)': [round(r[key]['p95'], 1) for r in mon],
            })
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(
                "Écart-type = variation d'une simulation à l'autre (0 = aucun hasard). "
                "p05–p95 = fourchette contenant 90 % des résultats."
            )

    st.caption(
        f"Simulateur Monte Carlo ({N_RUNS} réplications) — "
        "Carrières des Fonctionnaires Mauritaniens | "
        "Loi N°93-09 | DSIS/DGFP/MFPT | Mauritanie"
    )

else:
    st.info(
        "👈 Configure les curseurs à gauche, puis clique sur "
        "**▶️ Lancer la simulation**.\n\n"
        "Les résultats correspondront exactement aux paramètres que tu auras choisis."
    )
