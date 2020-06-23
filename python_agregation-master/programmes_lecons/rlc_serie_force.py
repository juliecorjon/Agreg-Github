r"""Résonance en tension d'un circuit RLC série

Description
-----------

Ce programme représente la réponse fréquencielle d'un oscillateur 
RLC série à un forçage sinusoidal en tension de 1 Vpp. 

La fenêtre de gauche permet de choisir aux bornes de quel composant 
on observe la tension. A noter qu'un choisissant la résistance R, 
on observe à un facteur près la réponse en courant du circuit. 

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2

Liste des modifications :
    * v 1.0 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
    * v 1.1 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2 : 2019-05-10 Simplification du programme
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
from numpy import pi

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button, make_log_button
from programmes_lecons import justify

titre = "Résonance en tension d'un circuit RLC série"


description = """Ce programme représente la réponse fréquencielle d'un oscillateur RLC série à un forçage sinusoidal en tension de 1 Vpp. 

La fenêtre de gauche permet de choisir aux bornes de quel composant on observe la tension. A noter qu'un choisissant la résistance R, on observe à un facteur près la réponse en courant du circuit. """


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

# Resonance en tension sur la résistance : attention, valeur complexe
def resonance_R(R, L, C, freq):
	omega = freq*2*pi
	return R/(1j*L*omega+R+1/(1j*C*omega))

# Resonance en tension sur le condensateur : attention, valeur complexe
def resonance_C(R, L, C, freq):
	omega = freq*2*pi
	return 1/(1j*C*omega)/(1j*L*omega+R+1/(1j*C*omega))

# Resonance en tension sur la bobine : attention, valeur complexe
def resonance_L(R, L, C, freq):
	omega = freq*2*pi
	return 1j*L*omega/(1j*L*omega+R+1/(1j*C*omega))


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(R, L, C):
    # Conversion en SI des sliders
    L = L*1E-3
    C = C*1E-6

    lines['R $\equiv$ I'].set_data(freq, np.absolute(resonance_R(R, L, C, freq)))
    lines['L'].set_data(freq, np.absolute(resonance_L(R, L, C, freq)))
    lines['C'].set_data(freq, np.absolute(resonance_C(R, L, C, freq)))

    lines['R $\equiv$ I - phi'].set_data(freq, np.angle(resonance_R(R, L, C, freq), deg=True))
    lines['L - phi'].set_data(freq, np.angle(resonance_L(R, L, C, freq), deg=True))
    lines['C - phi'].set_data(freq, np.angle(resonance_C(R, L, C, freq), deg=True))


    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax1, ax2 = fig.subplots(2, 1, sharex=True, 
            gridspec_kw={'left':0.35, 'bottom':0.3, 'top':0.9, 'hspace':0.08})


lines = {}
lines['R $\equiv$ I'], = ax1.plot([], [], lw=2, color='red', visible=False)
lines['L'], = ax1.plot([], [], lw=2,color='blue', visible=False)
lines['C'], = ax1.plot([], [], lw=2, color='green')

lines['R $\equiv$ I - phi'], = ax2.plot([], [], '--', color='red', visible=False)
lines['L - phi'], = ax2.plot([], [], '--',color='blue', visible=False)
lines['C - phi'], = ax2.plot([], [], '--', color='green')

freq = np.linspace(10, 10000, 1001)
ax1.axhline(0, color='k')
ax1.set_xlim(freq.min(), freq.max())
ax1.set_ylim(0.05, 5)
ax1.set_ylabel('Amplitude (V)')
ax1.grid(True)

ax2.set_ylim(-180, 180)
ax2.set_ylabel('Phase (°)')
ax2.set_xlabel('Fréquence (Hz)')
ax2.grid(True)

loc = plticker.MultipleLocator(base=90) # this locator puts ticks at regular intervals
ax2.yaxis.set_major_locator(loc)


param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.15])
choose_widget = make_choose_plot(lines, box=[0.015, 0.25, 0.2, 0.15], which=[('R $\equiv$ I', 'R $\equiv$ I - phi'), ('L', 'L - phi'), ('C', 'C - phi')])
reset_button = make_reset_button(param_widgets)
log_button =  make_log_button(ax1, ylims={'log':(5E-2, 1E1), 'linear':ax1.get_ylim()})

if __name__=='__main__':
    plt.show()




