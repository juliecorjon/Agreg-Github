r"""Figure de diffraction par N fentes

Description
-----------
Ce programme représente la figure d'interférence obtenue lorsqu'une onde 
plane monochromatique de longueur d'onde $\lambda$ traverse un dispositif 
de $N$ fentes régulièrement espacées d'une distance $a$ (centre-centre) et de 
largeur $b$ chacunes. L'écran est positionné à une distance $D$ des fentes. 

Le résultat présenté est l'intensité lumineuse normalisée en fonction de 
la position sur l'écran pour permettre une comparaison des différentes situations.

Formules
--------
$\frac{I}{I_0} = \mathrm{sinc}^2\left(\frac{\pi bx}{\lambda D}\right)\times\frac{\sin^2(N\pi a x/\lambda D)}{N^2\sin^2(\pi ax/\lambda D)}$


Informations
------------
Auteurs : Arnaud Raoux, Emmanuel Baudin, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.3
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.0 : 2016-03-01 Première version complète
    * v 1.1 : 2016-05-02 Mise à jour de la mise en page
    * v 1.2 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.3 : 2019-01-09 Simplification du programme
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button
from programmes_lecons import justify

titre = r"Figure de diffraction par N fentes"

description = r"""Ce programme représente la figure d'interférence obtenue lorsqu'une onde 
plane monochromatique de longueur d'onde $\lambda$ traverse un dispositif 
de $N$ fentes régulièrement espacées d'une distance $a$ (centre-centre) et de 
largeur $b$ chacunes. L'écran est positionné à une distance $D$ des fentes. 

Le résultat présenté est l'intensité lumineuse normalisée en fonction de 
la position sur l'écran pour permettre une comparaison des différentes situations.

$\frac{I}{I_0} = \mathrm{sinc}^2\left(\frac{\pi bx}{\lambda D}\right)\times\frac{\sin^2(N\pi a x/\lambda D)}{N^2\sin^2(\pi ax/\lambda D)}$
"""


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = dict(
    N = IntSlider(value=2, min=2, max=30, description='Nombre de fentes -- N'),
    a = FloatSlider(value=2, min=0.1, max=10.0, description='Pas de réseau -- a (µm)'),
    b = FloatSlider(value=1, min=0.1, max=2.0, description="Taille d'une fente -- b (µm)",),
    lamb = FloatSlider(value=0.633, min=0.1, max=3., description=r"Longueur d'onde -- $\lambda_0$ (µm)"),
    D = FloatSlider(value=1, description="Distance fentes-écran -- $D$ (m)", min=.3, max=2),
#    form_fact = Checkbox(value=False, description='Facteur de forme'),
#    form_struct = Checkbox(value=False, description='Facteur de structure')
)

#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def forme(x, b, lamb, D):
    """
    Calcule le facteur de forme du reseau.
    """
    # ATTENTION : sinc(x) = sin(pi x)/(pi x)
    return (np.sinc(b*x/D/lamb))**2


def structure(x, lamb, a, N, D):
    """
    Calcule le facteur de structure du reseau.
    """
    return (np.sin(N*np.pi*a/lamb*x/D) /
            (N*np.sin(np.pi*a/lamb*x/D)))**2


def signal(x, lamb, a, N, D):
    """
    Le signal est le produit du facteur de forme et du facteur de structure.
    """
    return forme(x, b, lamb, D)*structure(x, lamb, a, N, D)


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(lamb, N, a, b, D):
    # Conversion en SI
    lamb = lamb*1E-6
    a = a*1E-6
    b = b*1E-6
    
    x = np.linspace(-1, 1, 1001) #Zone observee : +/- 1 cm

    form = forme(x, b, lamb, D)
    struct = structure(x, lamb, a, N, D)

    lines['Fonction'].set_data(x, form*struct)  # On met a jour le signal
    lines['Facteur de forme'].set_data(x, form)  # On met a jour la forme
    lines['Facteur de structure'].set_data(x, struct)  # On met a jour la structure

#    arrow_struct.set_positions((0, -0.05), (lamb*D/a, -0.05))  
#    arrow_struct_text.set_x(lamb*D/a/2)

#    arrow_forme.set_positions((-lamb*D/b/2, np.sinc(.5)**2), (lamb*D/b/2, np.sinc(.5)**2))  
#    arrow_forme_text.set_x(lamb*D/b/2)

    fig.canvas.draw_idle()

#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.3, 0.6, 0.6])

lines = {}
lines['Fonction'], = ax.plot([],[], lw=2, color='red')
lines['Facteur de forme'], = ax.plot([],[], lw=1.5, ls='--', color='blue', visible=False)
lines['Facteur de structure'], = ax.plot([], [], lw=1.5, ls='--', color='green', visible=False)

ax.set_xlabel(r"Position sur l'écran $x$")
ax.set_ylabel('Intensité lumineuse normalisee')

ax.set_xlim(-1, 1)
ax.set_ylim(-0.1, 1.2)

#arrow_struct = mpatches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='<->', mutation_scale=20)   
#ax.add_patch(arrow_struct)       
#arrow_struct_text = ax.text(0, -0.05, '$\lambda D/a$', verticalalignment='bottom', horizontalalignment='center')

#arrow_forme = mpatches.FancyArrowPatch((0, 0), (0, 0), arrowstyle='<->', mutation_scale=20)   
#ax.add_patch(arrow_forme)       
#arrow_forme_text = ax.text(0, np.sinc(0.5)**2, '$\lambda D/b$', verticalalignment='center', horizontalalignment='left')

param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.55, 0.07, 0.4, 0.15])
choose_widget = make_choose_plot(lines, box=[0.015, 0.15, 0.2, 0.15])
reset_button = make_reset_button(param_widgets)

if __name__=='__main__':
    plt.show()  # On provoque l'affichage a l'ecran
