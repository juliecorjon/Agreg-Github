r"""Interférence de deux ondes harmoniques

Description
-----------
Ce programme permet d'illustrer le principe élémentaire de l'interférence de 
deux ondes harmoniques monochromatiques. 

Attention : les deux ondes sont supposées planes, scalaires et l'interférence 
intervient le long de leur propagation comme dans un interféromètre de Michelson,
mais pas comme dans un dispositif de fentes d'Young. 

La somme des deux ondes est représentée sur la fenêtre du bas.

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Levrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2
Version de Python : 3.7
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications: 
    * v 1.0 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
    * v 1.1 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2 : 2019-05-10 Simplification du programme
"""

titre = 'Interférence de deux ondes harmoniques'

description = """Ce programme permet d'illustrer le principe élémentaire de l'interférence de deux ondes harmoniques monochromatiques. 

Attention : les deux ondes sont supposées planes, scalaires et l'interférence intervient le long de leur propagation comme dans un interféromètre de Michelson, mais pas comme dans un dispositif de fentes d'Young. 

La somme des deux ondes est représentée sur la fenêtre du bas."""

import numpy as np
import matplotlib.pyplot as plt

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button
from programmes_lecons import justify


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = {
    # Remarquer la valeur initiale de lambda : 633 nm
    'lamb': FloatSlider(value=633, description="Longeur d'onde -- $\lambda$ (nm)", min=400, max=800), 
    'phi': FloatSlider(value=0, description='Déphasage -- $\phi$ (rad)', min=-np.pi, max=np.pi),
}


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

# Creation des ondes 1 et 2
def onde(lamb, phi, x):
	return np.cos(x*2.*np.pi/lamb+phi)

#Creation de l'interference
def interference(lamb, phi, x):
	return onde(lamb, 0, x) + onde(lamb, phi, x)


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(lamb, phi):
    lamb = lamb*1E-9

    lines['A'].set_data(x*1E9, onde(lamb, 0, x))
    lines['B'].set_data(x*1E9, onde(lamb, phi, x))
    lines['somme'].set_data(x*1E9, interference(lamb, phi, x))

    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax1, ax2, ax3 = fig.subplots(3, 1, sharex=True, sharey=True, 
            gridspec_kw={'left':0.35, 'bottom':0.3, 'top':0.9, 'hspace':0.05})

lines = {}
lines['A'], = ax1.plot([], [], lw=2, color='blue')
lines['B'], = ax2.plot([], [], lw=2, color='red')
lines['somme'], = ax3.plot([], [], lw=2, color='black')

x = np.linspace(-1., 1., 1001)*1E-6

ax1.set_ylim(-2.1, 2.1)
ax3.set_xlabel('Position (nm)')
ax3.set_xlim(x.min()*1E9, x.max()*1E9)

param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.15])
reset_button = make_reset_button(param_widgets)

if __name__=='__main__':
    plt.show()

