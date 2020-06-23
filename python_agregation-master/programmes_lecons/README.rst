==========================
Programmes pour les leçons
==========================

Liste des programmes disponibles
================================

* Figure de diffraction par N fentes (`diffraction_N_fentes.py <diffraction_N_fentes.py>`_)
* Diffusion de particules (`diffusion_particules.py <diffusion_particules.py>`_)
* Échantillionage (`echantillonage_filtrage.py <echantillonage_filtrage.py>`_)
* Écoulement de Couette plan (`ecoulement_couette.py <ecoulement_couette.py>`_)
* Effet tunnel (`effet_tunnel.py <effet_tunnel.py>`_)
* Interférence par des fentes d'Young (`fentes_young.py <fentes_young.py>`_)
* Interférence de deux ondes harmoniques (`interference_elementaire.py <interference_elementaire.py>`_)
* Loi de Planck (`loi_de_planck.py <loi_de_planck.py>`_)
* Orbites de Keppler (`orbites_kepler.py <orbites_kepler.py>`_)
* Oscillateur amorti (`oscillateur_amorti.py <oscillateur_amorti.py>`_)
* Écoulement de Poiseuille (`poiseuille.py <poiseuille.py>`_)
* Portrait de phase d'un pendule (`portrait_de_phase.py <portrait_de_phase.py>`_)
* Propatation d'un paquet d'onde avec dispersion (`propagation_avec_dispersion.py <propagation_avec_dispersion.py>`_)
* Déplacement de poussières dans une onde sonore (`propagation_son.py <propagation_son.py>`_)
* Déplacement de poussières dans une onde sonore (`propagation_son.py <propagation_son.py>`_)
* Puits quantique (`puits_quantique.py <puits_quantique.py>`_)
* Réponse à un échelon de tension d'un circuit RLC série (`rlc_serie_declin.py <rlc_serie_declin.py>`_)
* Résonance en tension d'un circuit RLC série (`rlc_serie_force.py <rlc_serie_force.py>`_)
* Transition liquide-vapeur pour un fluide de Van der Waals (`van_der_waals.py <van_der_waals.py>`_)


Utilisation
===========

Chaque programme est un script independant qui peut s'exécuter par exemple depuis ``spyder``.

Les programmes
==============

Voici quelques prescriptions sur l'écriture des programmes. On s'éfforcera d'utiliser
les recommendations de Python (PEP 8)

* Chaque programme commence par une chaine de documentation. Cette chaîne contient :

    * Un titre
    * Une description
    * Eventuellement un rappel des formules utilisées ou tout autre information utile (lien, ...)
    * D'autres informations (auteurs, licence, ....)

* Ensuite, l'ensembles des import. Si on souhaite avoir les bons paramètres par défaut pour
  la taille de la figure et le polices, il faut importer le module ``programmes_lecons``, 
  même si on n'utilise aucune de ses fonctions


Dans le suite, on s'efforcera de séparer le fond de la forme et de mettre le fond au début
du programme. Typiquement, un programme se sépare alors en 4 sections : 

* Les variables globales et les paramètres. Les paramètres sont des ``widget`` regroupés dans
  un dictionnaire. Les clés du dictionnaire seront les noms des variables. En général, 
  on recommande de donner des noms explicite pour une variable (par exemple ``resistance`` et
  non ``R``). Cette règle n'est pas appliqué si c'est le nom d'une variale utilisée
  habituellement en physique (dans un circuit RLC, on sait que R est la résistance)
 
* Le modèle physique : toutes les fonctions utilisées. On utilisera toujours les unités SI (sans
  préfixe) ou les unités spécifiques au problèmes. 

* Le tracé des données : une fonction sera utilisée pour tracer les données en fonctions des
  paramètres. Les arguuments sont les noms des paramètres (les clés du dictionnaire). On
  effectuera les transformation en SI au début de la fonction. 

  Cette fonction changera les données des "lignes" des plots ::

     lines['nom_de_la_ligne'].set_data(x, y)

  Les variables x et y seront en SI sans préfixe. Si le graph a des préfix, on le mettra à ce
  moment là (``set_data(x*1E3, y*1E-3)``)

* La création et la mise en page de la figure : création de la figure, des axes, des 'lignes'
  avec tous les paramètres de la mise en forme (couleur, style, ...); création des widgets et
  des autres boutons

* A la fin, le plt.show() est mis dans un ``if __name__=="__main__"`` : ceci permet d'importer
  le script comme une librairie sans afficher la figure pour faire des extractions automatiques.


Création d'une animation
========================

Voir les exemples comme : ``propagation_onde``. 


Création des pdf
================

On utilisera la commande::

   python -m utils.convert_to_pdf

Cette commander permet implicitement de faire un test simple de tous les programmes. L'assemblage de 
tous les fichiers ne fonctionera que sous Linux avec le package pdfjoin.

Informations
============

Auteurs : François Lévrier, Emmanuel Baudin, Arnaud Raoux, David Delgove, Vincent Lusset, Pierre Cladé et la prépa agreg de Montrouge

Adresse : Département de physique de l'École Normale Superieure
		24 rue Lhomond
		75005 Paris

Licence : Cette oeuvre, création, site ou texte est sous licence Creative Commons Attribution - Pas d'Utilisation Commerciale 4.0 International. Pour accéder à une copie de cette licence, merci de vous rendre à l'adresse suivante http://creativecommons.org/licenses/by-nc/4.0/ ou envoyez un courrier à Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

