import pyxel
import random

ecran_l = 128
ecran_h = 128


# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(ecran_l, ecran_h, title="Retro game")

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 60
vaisseau_y = 60
vaisseau_l = 8
vaisseau_h = 8

# initialisation des tirs
tirs_liste = []

ennemis_liste = []



def vaisseau_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT) and x<ecran_l-vaisseau_l:
        x = x + 1

    if pyxel.btn(pyxel.KEY_LEFT) and x>0:
       x = x - 1 

    if pyxel.btn(pyxel.KEY_UP) and y>0:
       y = y - 1

    if pyxel.btn(pyxel.KEY_DOWN) and y<ecran_h-vaisseau_l:
       y = y + 1
    return x, y # retourne les coordonnées mise à jour

   
def tirs_creation(x, y, tirs_liste):
    """création d'un tir avec la barre d'espace"""
    # btnr pour eviter les tirs multiples
    if pyxel.btnr(pyxel.KEY_SPACE):
        tirs_liste.append([x, y])
    return tirs_liste


def tirs_deplacement(tirs_liste):
    """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""
    for tir in tirs_liste:
        tir[1] -= 1 # le tir se déplace vers le haut
        if  tir[1]< 0 : #le tir sort de l'écran
            tirs_liste.remove(tir)# je supprime ce tir de la liste des tirs
    return tirs_liste


def ennemis_creation(ennemis_liste):

    if pyxel.frame_count % 30 == 0:
        ennemis_liste.append([random.randrange(0, 128), 0])
    return ennemis_liste

def ennemis_maj(ennemis_liste):
    for ennemi in ennemis_liste:
        ennemi[1] += 1
        if ennemi[1] > 128 or ennemi[1] < 0:
            ennemis_liste.remove(ennemi)
    return ennemis_liste


def ennemis_suppression():
    """disparition d'un ennemi et d'un tir si contact"""
    to_remove = []  # Liste pour stocker les ennemis à supprimer
    for ennemi in ennemis_liste:
        e_x, e_y = ennemi
        for tir in tirs_liste:
            tir_x, tir_y = tir
            if e_x < tir_x + 4 and e_x + 8 >= tir_x and e_y < tir_y + 6 and e_y + 7 >= tir_y:
                to_remove.append(ennemi)  # Ajoute l'ennemi à supprimer
                tirs_liste.remove(tir) # suppression de la liste
    for ennemi in to_remove:
        ennemis_liste.remove(ennemi)  # Suppression des ennemis après la boucle



pyxel.load("images.pyxres")

# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global vaisseau_x, vaisseau_y, vaisseau_l, vaisseau_h, tirs_liste, ennemis_liste
    
    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)

    #print(pyxel.frame_count)
    
     # creation des tirs en fonction de la position du vaisseau
    tirs_liste = tirs_creation(vaisseau_x + 2, vaisseau_y - 2, tirs_liste)

     # mise a jour des positions des tirs
    tirs_liste = tirs_deplacement(tirs_liste)
    
    
    ennemis_liste = ennemis_creation(ennemis_liste)


    ennemis_liste = ennemis_maj(ennemis_liste)

    #suppression des ennemis si contact avec tir
    ennemis_suppression()


# =========================================================
# == DRAW
# =========================================================
def draw():
    """dessin des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)
    
# tirs
    for tir in tirs_liste: # je boucle sur ma liste de tirs
        pyxel.blt(tir[0], tir[1], 0, 8, 8, 4, 6)

    # vaisseau (carre 8x8)
    # x, y, largeur, hauteur, couleur
    if pyxel.frame_count%4 == 2:
        pyxel.blt(vaisseau_x, vaisseau_y, 0, 0, 0, vaisseau_l, vaisseau_h)
    else:
        pyxel.blt(vaisseau_x, vaisseau_y, 0, 8, 0, vaisseau_l, vaisseau_h)

 # ennemis
    for ennemi in ennemis_liste: # je boucle sur ma liste d’ennemis
        pyxel.blt(ennemi[0], ennemi[1], 0, 0, 9, 8, 7)


# lance le programme principal
pyxel.run(update, draw)

