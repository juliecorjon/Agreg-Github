"""Échantillionage

Description
-----------
Ce programme a pour objectif de mettre en évidence l'effet d'échantionnage, ainsi que l'effet de filtrage sur un signal analogique.

Informations
------------
Auteurs : David Delgove, Arnaud Raoux, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2017
Version : 1.3
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.00 : 2017-06-09 Première version complète
    * v 1.10 : 2018-05-08 Ajout d'un slider pour la fréquence d'échantillonage
    * v 1.20 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.3 : 2019-05-10
"""
import numpy as np
import matplotlib.pyplot as plt

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button
from programmes_lecons import justify


titre = """Échantillionage"""

description = """Ce programme a pour objectif de mettre en évidence l'effet 
d'échantionnage, ainsi que l'effet de filtrage sur un signal analogique."""


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

frequence_signal = 10 
duree_acquisition = 1 

parameters = {
    'freq_ech': FloatSlider(value=31, description="Échantillionage -- $f_\mathrm{ech}$ (Ech/s)", max=60.0, min=5),
}



#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def signal_entree(fech, fe=frequence_signal, Tacq=duree_acquisition, amp=1): 
    '''
    fe : fréquence du signal
    fech : fréquence d'échantillonage
    Tacq : Temps d'acquisition
    amp : amplitude du signal
    '''

    Npoint = int(fech*Tacq)+1
    temps=np.arange(Npoint)/fech
    
    signal=amp*np.cos(2*np.pi*fe*temps)
    
    return temps, signal


table_vrai_signal_x, table_vrai_signal_y = signal_entree(fech = 200*frequence_signal)


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(freq_ech=35):
    #Signal échantilloné
    x, y = signal_entree(freq_ech)
    lines['Numérique'].set_data(x, y)

    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.5, .93, "Fréquence du signal :{} Hz".format(frequence_signal), 
            multialignment='left', verticalalignment='top', horizontalalignment='center')

ax = fig.add_axes([0.15, 0.2, 0.7, 0.7])

lines = {}
lines['Analogique'], = ax.plot(table_vrai_signal_x, table_vrai_signal_y , color='blue', linewidth=1, label="Analogique")
lines['Numérique'],  = ax.plot([],[], color='red', marker='o', markersize=10, linewidth=2, label="Numérique")


ax.legend(loc="upper left", bbox_to_anchor=[0, 1], ncol=2, shadow=True, fancybox=True)

ax.set_ylim(-1.3, 1.4)
ax.set_ylabel(r'U.A')
ax.set_xlabel(r't(s)')


param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.4, 0.02, 0.3, 0.04])
choose_widget = make_choose_plot(lines, box=[0.005, 0.025, 0.2, 0.10], which=['Analogique'])
reset_button = make_reset_button(param_widgets, box=[0.8, 0.02, 0.1, 0.04])


if __name__=='__main__':
    plt.show()



