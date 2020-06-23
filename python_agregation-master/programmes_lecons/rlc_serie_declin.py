r"""Réponse à un échelon de tension d'un circuit RLC série

Description
------------
Ce programme représente la réponse temporelle d'un oscillateur RLC
série à un forçage en échelon de tension à l'instant t=0. 

La fenêtre de gauche permet de choisir aux bornes de quel composant
on observe la tension. A noter qu'un choisissant la résistance R, 
on observe à un facteur près la réponse en courant du circuit. 

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International


Liste des modifications: 
    * v 1.0 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
    * v 1.1 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2 : 2019-05-10 Simplification du programme
"""

import matplotlib.pyplot as plt
import numpy as np

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button, make_log_button
from programmes_lecons import justify

titre = "Réponse à un échelon de tension d'un circuit RLC série"

description = """Ce programme représente la réponse temporelle d'un oscillateur RLC série à un forçage en échelon de tension à l'instant t=0. 

La fenêtre de gauche permet de choisir aux bornes de quel composant on observe la tension. A noter qu'un choisissant la résistance R, on observe à un facteur près la réponse en courant du circuit. 
"""

#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = {
    'R' : FloatSlider(value=10, description='Résistance -- $R$ ($\Omega$)', min=1, max=30),
    'L' : FloatSlider(value=1, description='Inductance -- $L$ ($mH$)', min=0.01, max=3),
    'C' : FloatSlider(value=10, description='Capacité -- $C$ ($\mu F$)', min=0.1, max=30),
    }


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def resonance_R(R, L, C, t):
	w0 = 1/np.sqrt(L*C)
	a = R/(2*L*w0)
	delta = a**2-1

	if delta > 0 : 
		r1 = (-a+np.sqrt(delta))*w0
		r2 = (-a-np.sqrt(delta))*w0
	else:
		r1 = (-a+1j*np.sqrt(-delta))*w0
		r2 = (-a-1j*np.sqrt(-delta))*w0
	return np.real(R*C*r1*r2/(r2-r1)*(np.exp(r1*t)-np.exp(r2*t)))

# resonance_ en tension sur le condensateur : attention, valeur complexe
def resonance_C(R, L, C, t):
	w0 = 1/np.sqrt(L*C)
	a = R/(2*L*w0)
	delta = a**2-1
        
	if delta > 0 : 
		r1 = (-a+np.sqrt(delta))*w0
		r2 = (-a-np.sqrt(delta))*w0
	else:
		r1 = (-a+1j*np.sqrt(-delta))*w0
		r2 = (-a-1j*np.sqrt(-delta))*w0
	return np.real(1/(r2-r1)*(r2*np.exp(r1*t)-r1*np.exp(r2*t)))

# resonance_ en tension sur la bobine : attention, valeur complexe
def resonance_L(R, L, C, t):
	return -resonance_R(R, L, C, t)-resonance_C(R, L, C, t)


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(R, L, C):
    L = L*1E-3
    C = C*1E-6

    lines['R $\equiv$ I'].set_data(t*1E3, resonance_R(R, L, C, t))
    lines['L'].set_data(t*1E3, resonance_L(R, L, C, t))
    lines['C'].set_data(t*1E3, resonance_C(R, L, C, t))

    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.3, 0.6, 0.6])
ax.axhline(0, color='k')

lines = {}
lines['R $\equiv$ I'], = ax.plot([], [], lw=2, color='red', visible=False)
lines['L'], = ax.plot([], [], lw=2,color='blue', visible=False)
lines['C'], = ax.plot([], [], lw=2, color='green')

t = np.linspace(0., 1E-3, 1001)
ax.set_xlim(t.min(), t.max()*1E3)
ax.set_ylim(-1.1, 1.1)

ax.set_xlabel('temps (ms)')
ax.set_ylabel('Amplitude (V)')





param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.15])
choose_widget = make_choose_plot(lines, box=[0.015, 0.25, 0.2, 0.15])
reset_button = make_reset_button(param_widgets)

if __name__=='__main__':
    plt.show()




