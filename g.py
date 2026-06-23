import matplotlib.pyplot as plt
from simulateur import simuler_monte_carlo
from Generateur import agents as agents_v3

print("\n" + "="*65)
print("VALIDATION 3 : CONVERGENCE MONTE CARLO")
print("="*65)

runs_list = [10, 25, 50, 100, 200]
moyennes = []
ecarts = []

for nr in runs_list:
    r = simuler_monte_carlo(agents_v3, 5, n_runs=nr,
                             age_retraite=63, duree_anciennete=2,
                             nb_recrutements=0)
    moyennes.append(r[1]['promotions']['moyenne'])
    ecarts.append(r[1]['promotions']['ecart_type'])
    print(f"n_runs={nr:>4} → moyenne promotions 2028 = {r[1]['promotions']['moyenne']:.1f} "
          f"(σ={r[1]['promotions']['ecart_type']:.1f})")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(runs_list, moyennes, marker='o', color='#1B8A4C', linewidth=2.5)
ax.set_xlabel("Nombre de réplications Monte Carlo")
ax.set_ylabel("Promotions moyennes (2028)")
ax.set_title("Convergence de la simulation Monte Carlo")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(r"C:\Users\pc\OneDrive\Desktop\Rapport-Stage\figures\convergence_mc.pdf",
            bbox_inches='tight', dpi=300)
print("\n✅ Graphe de convergence enregistré dans figures/")