r"""Reflexion des ondes sonores planes harmoniques propagatives

Description
-----------
Ce programme représente l'effet d'une barrière d'amplitude du coefficient 
de reflexion $r$ sur une onde sonore plane harmonique propagative. 

La réflexion est représentée spatialement, le temps pouvant être varié indépendamment. 

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.00 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
    * v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2 : 2019-05-10
"""

import numpy as np
from numpy import pi, exp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button, make_start_stop_animation
from programmes_lecons import justify


titre = 'Reflexion des ondes sonores planes harmoniques propagatives'

description=r"""
Ce programme représente l'effet d'une barrière d'amplitude du coefficient de reflexion $r$ sur une onde sonore plane harmonique propagative. La réflexion est représentée spatialement, le temps pouvant être varié indépendamment. 

$r = \frac{Z_2-Z_1}{Z_2+Z_1}$

$t = 1 + r$
"""



#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

c = 340 # Vitesse du son en m/s

parameters = dict(
    t = FloatSlider(description='Temps -- $t$ (ms)', min=0, max=2., value=0),
    freq = FloatSlider(description='Fréquence -- $f$ (Hz)', min=500, max=1500.0, value=1000),
    amp = FloatSlider(description='Amplitude -- $A$ (V)', min=0.0, max=10.0, value=4),
#    refl = FloatSlider(description='Réflexion -- $r$', min=-1., max=1., value=0),
    Z2 = FloatSlider(description='Impedance -- $Z_2$', min=0, max=10., value=1),
    )


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def oscillation(t, x, amp, freq, refl, phase_refl=0):
    left = np.real(amp*exp(2J*pi*freq*(t-x/c))+amp*refl*exp(1J*phase_refl)*exp(2J*pi*freq*(t+x/c)))
    right = np.real(amp*(1.+refl*exp(1J*phase_refl))*exp(2J*pi*freq*(t-x/c)))
    return np.where(x<0, left, right)

x = np.linspace(-1., 1., 1001)

#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(t, freq, amp, Z2):
    refl = (Z2-1)/(1+Z2)
    t = t*1E-3
    lines['data'].set_data(x, oscillation(t, x, amp, freq, refl))
    lines['coef_refl'].set_text('r = {:4.2f}; t = {:4.2f}'.format(refl, 1+refl))
    lines['Z2'].set_text('$Z_2={:4.2f}$'.format(Z2))

    fig.canvas.draw_idle()

#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.3, 0.6, 0.6])

lines = {}
lines['data'], = ax.plot([],[], lw=2, color='red')
lines['coef_refl'] = ax.text(-.7, -9, '')
lines['Z1'] = ax.text(-.75, 9, '$Z_1=1$')
lines['Z2'] = ax.text(.75, 9, '')

ax.set_xlabel('Position (m)')
ax.set_ylabel('Amplitude (u.a.)')

ax.set_xlim(-1, 1)
ax.set_ylim(-10, 10)

ax.axvline(0, linestyle='--', color='k')


param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.45, 0.07, 0.4, 0.15])
reset_button = make_reset_button(param_widgets)

#===========================================================
# --- Animation --------------------------------------------
#===========================================================

def animation_function(val):
    param_widgets['t'].set_val((val/50)%1)

ani = animation.FuncAnimation(fig, animation_function, interval=100.0)
anim_btn = make_start_stop_animation(ani)


if __name__=='__main__':
    plt.show()  # On provoque l'affichage a l'ecran


