import copy
import random
import statistics


def simuler(agents, n_annees, age_retraite=63, duree_anciennete=2,
            nb_recrutements=0, seed=None):
    """
    Une trajectoire de simulation des carrières des fonctionnaires.

    Si `seed` est fourni, le hasard est reproductible (même seed → même résultat).
    Si `seed` est None, chaque appel produit une trajectoire aléatoire différente.

    Renvoie une liste de dictionnaires (un par année) avec :
        annee, actifs, retraites, avancements, promotions
    """
    if seed is not None:
        random.seed(seed)

    # Copie profonde pour ne pas modifier les données originales
    pop = copy.deepcopy(agents)

    resultats = []

    for annee in range(n_annees):
        annee_courante = 2026 + annee + 1

        nb_retraites = 0
        nb_avancements = 0
        nb_promotions = 0
        nb_actifs = 0

        # ===================== RECRUTEMENTS =====================
        if nb_recrutements > 0:
            for j in range(nb_recrutements):
                nouvel_agent = {
                    "id_agent": len(pop) + j,
                    "age_naissance": annee_courante - 25,
                    "age_actuel": 25,
                    "corps": "Autres",
                    "grade": "Grade 2",
                    "echelon": 1,
                    "etat_service": 0,
                    "note": random.randint(0, 20),
                    "position": "En activite",
                    "anciennete_echelon": 0,
                    "age_retraite": annee_courante - 25 + 63,
                    "statut": "Actif"
                }
                pop.append(nouvel_agent)

        # ===================== SIMULATION POUR L'ANNÉE =====================
        for agent in pop:
            if agent.get("statut") == "Retraite":
                continue

            # Calcul de l'âge cette année
            age = annee_courante - agent["age_naissance"]

            # 1. RETRAITE
            if age >= age_retraite:
                agent["statut"] = "Retraite"
                nb_retraites += 1
                continue

            nb_actifs += 1

            # 2. ETAT DE SERVICE + ANCIENNETÉ ÉCHELON (pas si dispo / HC)
            if agent["position"] not in ["Disponibilite", "Hors cadres"]:
                agent["etat_service"] += 1
                agent["anciennete_echelon"] += 1

            # 3. PROMOTION GRADE (vérifiée AVANT l'avancement,
            #    seuil etat_service >= 8 aligné sur le générateur)
            promu = False
            if (agent["corps"] == "Autres" and
                    agent["grade"] == "Grade 2" and
                    agent["etat_service"] >= 8 and
                    agent["note"] >= 12):
                agent["grade"] = "Grade 1"
                agent["echelon"] = 1
                agent["anciennete_echelon"] = 0
                nb_promotions += 1
                promu = True

            # 4. AVANCEMENT D'ÉCHELON (uniquement si pas promu cette année)
            if (not promu and
                    agent["anciennete_echelon"] >= duree_anciennete and
                    agent["echelon"] < 13):
                agent["echelon"] += 1
                agent["anciennete_echelon"] = 0
                nb_avancements += 1

            # Nouvelle note pour l'année suivante
            agent["note"] = random.randint(0, 20)

        resultats.append({
            "annee": annee_courante,
            "actifs": nb_actifs,
            "retraites": nb_retraites,
            "avancements": nb_avancements,
            "promotions": nb_promotions
        })

    return resultats


def simuler_monte_carlo(agents, n_annees, n_runs=100, age_retraite=63,
                        duree_anciennete=2, nb_recrutements=0):
    """
    Vraie simulation Monte Carlo : exécute `simuler()` n_runs fois avec un seed
    différent à chaque run, puis aggrège les statistiques année par année.

    Pour chaque métrique (actifs, retraites, avancements, promotions), renvoie :
        moyenne, ecart_type, p05 (5e percentile), p50 (médiane),
        p95 (95e percentile), min, max
    """
    # ---- Collecte des trajectoires ----
    all_runs = []
    for r in range(n_runs):
        res = simuler(
            agents, n_annees,
            age_retraite=age_retraite,
            duree_anciennete=duree_anciennete,
            nb_recrutements=nb_recrutements,
            seed=r,
        )
        all_runs.append(res)

    # ---- Helper percentile par interpolation linéaire ----
    def pct(sorted_vals, p):
        k = (len(sorted_vals) - 1) * (p / 100.0)
        f = int(k)
        c = min(f + 1, len(sorted_vals) - 1)
        return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)

    # ---- Aggrégation par année ----
    aggregated = []
    for annee_idx in range(n_annees):
        year_data = {"annee": all_runs[0][annee_idx]["annee"]}
        for metric in ["actifs", "retraites", "avancements", "promotions"]:
            values = [run[annee_idx][metric] for run in all_runs]
            sorted_vals = sorted(values)
            year_data[metric] = {
                "moyenne":    round(statistics.mean(values), 1),
                "ecart_type": round(statistics.stdev(values), 1) if len(values) > 1 else 0.0,
                "p05":        round(pct(sorted_vals, 5), 1),
                "p50":        round(pct(sorted_vals, 50), 1),
                "p95":        round(pct(sorted_vals, 95), 1),
                "min":        sorted_vals[0],
                "max":        sorted_vals[-1],
            }
        aggregated.append(year_data)

    return aggregated


def afficher_mc(resultats_mc, metrique="promotions"):
    """
    Affiche un tableau d'une métrique Monte Carlo année par année.
    Exemple : afficher_mc(s0, "promotions")
    """
    print(f"\n  {metrique.upper()}")
    print(f"  {'Année':<8}{'Moyenne':>10}{'σ':>9}{'p05':>9}{'p50':>9}{'p95':>9}")
    print("  " + "-" * 54)
    for ligne in resultats_mc:
        m = ligne[metrique]
        print(f"  {ligne['annee']:<8}{m['moyenne']:>10.1f}{m['ecart_type']:>9.1f}"
              f"{m['p05']:>9.1f}{m['p50']:>9.1f}{m['p95']:>9.1f}")


def comparer_scenarios(agents, n_annees, n_runs=100):
    """
    Compare 4 scénarios en simulation Monte Carlo (n_runs réplications chacun).
    """
    print("\n=== SIMULATION NORMALE ===")
    s0 = simuler_monte_carlo(agents, n_annees, n_runs=n_runs)

    print("=== WHAT-IF 1 : Age retraite = 60 ===")
    s1 = simuler_monte_carlo(agents, n_annees, n_runs=n_runs, age_retraite=60)

    print("=== WHAT-IF 2 : Ancienneté = 3 ans ===")
    s2 = simuler_monte_carlo(agents, n_annees, n_runs=n_runs, duree_anciennete=3)

    print("=== WHAT-IF 3 : +500 recrutements/an ===")
    s3 = simuler_monte_carlo(agents, n_annees, n_runs=n_runs, nb_recrutements=500)

    return s0, s1, s2, s3