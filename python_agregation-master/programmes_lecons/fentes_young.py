r"""Interférence par des fentes d'Young

Description
-----------
Ce programme représente la figure d'interférence obtenue lorsqu'une onde plane monochromatique de longueur d'onde $\lambda$ traverse un dispositif de fentes d'Young éloignées d'une distance $a$ (centre-centre) et de largeur $w$. 
L'écran est positionné à une distance $L$ des fentes.

Formules
--------
$I = \sinc\left(\frac{kwx}{2L}\right)^2 \cos\left(\frac{kax}{2L}\right)^2$

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Levrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.0 : 2016-05-02 Première version complète 
    * v 1.1 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2 : 2019-05-10 Simplification du programme
"""

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button
from programmes_lecons import justify

titre = r"Interférence par des fentes d'Young"

description = r"""Ce programme représente la figure 
d'interférence obtenue lorsqu'une onde 
plane monochromatique de longueur d'onde 
$\lambda$ traverse un dispositif de fentes 
d'Young éloignées d'une distance $a$
(centre-centre) et de largeur $w$. 
L'écran est positionné à une distance 
$L$ des fentes.

$I = \sinc\left(\frac{kwx}{2L}\right)^2 \cos\left(\frac{kax}{2L}\right)^2$
"""

#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = {
    # Remarquer la valeur initiale de lambda : 633 nm
    'lamb': FloatSlider(value=633, description="Longueur d'onde -- $\lambda$ (nm)", min=400, max=800), 
    'a': FloatSlider(value=1.0, description='Distance entre les fentes -- $a$ (mm)', min=0.5, max=3.0),
    'w': FloatSlider(value=100, description="Largeur d'une fente -- $w$ ($\mu$m)", min=10, max=300),
    'L': FloatSlider(value=1, description="Distance fentes-écran -- $L$ (m)", min=.3, max=2),
}


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

# ATTENTION : le sinc est défini avec sin(pi*x)/(pi*x)
def enveloppe(x, k, L, a, w):
    return np.sinc(k*w*x/(2*L)/pi)**2

def fente_young(x, k, L, a, w):
    return enveloppe(x, k, L, a, w)*(np.cos(k*a*x/(2*L)))**2


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée Ã  chaque modification des paramètres
def plot_data(lamb, a, w, L):
    # Conversion en SI
    lamb = lamb*1E-9
    a = a*1E-3
    w = w*1E-6
    k = 2*np.pi/lamb
    
    x = np.linspace(-0.01, 0.01, 1001) #Zone observee : +/- 1 cm

    lines['Fente Young'].set_data(x, fente_young(x, k, L, a, w))
    lines['Enveloppe'].set_data(x, enveloppe(x, k, L, a, w))

    fig.canvas.draw_idle()

#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================
fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, description, multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.3, 0.6, 0.6])

lines = {}
lines['Fente Young'], = ax.plot([],[], lw=2, color='red')
lines['Enveloppe'],  = ax.plot([],[], lw=1, ls='--',color='red', visible=False)

ax.set_xlabel("Position sur l'écran (m)")
ax.set_ylabel('Intensité lumineuse (u.a.)')

ax.set_xlim(-0.01, 0.01)
ax.set_ylim(0, 1)

param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.15])
choose_widget = make_choose_plot(lines, box=[0.015, 0.3, 0.2, 0.15])
reset_button = make_reset_button(param_widgets)

if __name__=='__main__':
    plt.show()


