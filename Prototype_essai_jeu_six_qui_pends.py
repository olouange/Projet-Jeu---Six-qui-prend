#################################################################################################################################################################################
#################################   ANGE BRUNO OLOU   #########################   SPI 1   #########################################################################################
#################################################################################################################################################################################



from turtle import *
from random import *
import os
import json # ceci me permet de transformer une chaine de caractere en information utilisable telle qu'elle etait "un dictionaire ecrit sous forme chaine de caracter va etre transformer en dictionnaire normal :)"

###########################
###   Partie 1 : calcul pénalités + affichage textuel
###########################

################## 4.1.1 #####################
def nb_points_carte(carte) :                                     #fonction nb_points_carte
    liste_des_5 =[5, 15, 25, 35, 45, 65, 75, 85, 95]            #la creation des listes corportants les différentes valeurs des cartes en fontion de TdB
    liste_des_10 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    liste_des_doublet = [11, 22, 33, 44, 66, 77, 88, 99]

    if 1 <= carte <= 104 :
        if carte == 55 :
            return 7 #TdB
        elif carte in liste_des_5 :
            return 2 #TdB
        elif carte in liste_des_10 :
            return 3 #TdB
        elif carte in liste_des_doublet :
            return 5 #TdB
        else :
            return 1 #TdB



################## 4.1.2 #####################
def nb_points_tas(lcartes) :                            #fonction nb_points_carte
    lcarte = list(lcartes)                              #Copie de la liste pour eviter de la modifier
    somme = 0
    
    for carte in range (len(lcarte)) :
        valeur_carte = lcarte[carte]
        somme = somme + nb_points_carte(valeur_carte)
    return somme



################## 4.1.3 #####################
def texte_carte(carte) :                                #fonction afficher_liste_cartes
    n = nb_points_carte(carte)
    chaine = str(carte) +" ("+str(n)+")"                 #Attention !!! (Impossible de faire la somme entre 'int' et 'str')
    return chaine




################## 4.1.4 #####################
def afficher_liste_cartes(lcartes) :
    m = ""
    for carte in lcartes :
        chaine = texte_carte(carte)
        print(chaine,end = "\t")                #c'est mieux de mettre end ou sep dans le print pour eviter l'erreur!!!!
        m = m + chaine + "\t"           
    print()
    return m          
    


################## 4.1.5 #####################
def afficher_plateau(dlignes) :                                         #fonction afficher_plateau
    dligne = dict(dlignes)
    for ligne in dlignes :
        l = dligne[ligne]
        print ("Lig",ligne,":",end ="\t")                   #la tubulation permet de coller le resultat de afficher_liste_cartes(l) a la suite
        afficher_liste_cartes(l)
    dessiner_plateau(dligne)                      # Permets de dessiner les carte sur turtle



################## 4.1.6 #####################
def afficher_scores(dscores, nature = "manche") :                          #fonction afficher_scores
    dscore = dict(dscores)
    print("Scores",nature,":",end = "\n" )
    
    for nom in dscore :
        print("   " + nom,":",dscore[nom],"point(s)")
        
    print()


###########################
###   Partie 2 : initialisation de la partie + utilitaires
###########################

########## 4.2.1 #############
def generer_pioche() :
    liste_carte = []
    i = 1
    while i <= 104 :
        liste_carte.append(i)
        shuffle(liste_carte)                                # à chaque fois que j'ajoute un "i" à la liste , je melange la liste
        i = i + 1
    return liste_carte
    


########## 4.2.2 #############
def demander_nb_joueurs() :
    nb_joueurs = numinput("NJ","\nNombre de joueurs : ",10, minval = 2, maxval = 10)
    #while nb_joueurs == None :
        
    return nb_joueurs


########## 4.2.3 #############
def saisie_noms(nb_joueurs) :
    liste_des_joueurs = []
    i = 1
    while i <= nb_joueurs :
        nom = str(textinput("J","Joueur n°"+str(i)+",Entrez votre nom :"))
        
        while nom in liste_des_joueurs :
            nom = str(textinput("J","Ce nom est déjà utilisé.\nEntrez un nouveau nom :"))
        liste_des_joueurs.append(nom)
                            
        i = i + 1
    return liste_des_joueurs


########## 4.2.4 #############
def init_scores(ljoueurs) :
    ljoueur = list(ljoueurs)
    dico ={}
    for i in range (len(ljoueur)) :
        nom = ljoueur[i]
        dico[nom] = 0
    return dico



########## 4.2.5 #############
def distribuer_cartes(pioche, ljoueurs, nb_cartes = 10) :
    djeux = {}
    
    for i in range(len(ljoueurs)) :
        nom = ljoueurs[i]
        l_pour_carte = []                                           # il faut initialiser la liste à chaque fois qu'on prend un nouveau joueur
        
        j = 0
        while j < nb_cartes :
            carte = pioche[j]
            l_pour_carte.append(carte)
            pioche.pop(j)
            j = j + 1
        l_pour_carte.sort()
        djeux[nom] = l_pour_carte
    return djeux
        




########## 4.2.6 #############
def init_lignes(pioche) :
    dico = {}
    i = 1
    
    while i <= 4 :
        l = []
        l.append(pioche[0])                                             # elever le premier element a chaque fois de la liste
        pioche.pop(0)
        dico[i] = l

        i = i + 1                                           
            
    return dico
        
        
        
        

###########################
###   Partie 3 : programmer les règles du jeu + un tour
###########################

########## 4.3.1 #############
def demander_choix(nom, jeu) :
    print("Joueur",nom,"votre jeu : ")
    m = afficher_liste_cartes(jeu)
    
    nb_choisi = int(textinput("Vc","Joueur " + nom + " votre jeu : \n"+ m +"\nValeur de la carte à jouer : "))
    while not nb_choisi in jeu :
        nb_choisi= int(textinput("Vc","Cette carte n'est pas dans votre jeu !\nJoueur " + nom + " votre jeu : \n"+ m +"\nValeur de la carte à jouer : "))
    return nb_choisi




########## 4.3.2 #############
def trouver_ligne(carte, dlignes) : 
    dligne = dict(dlignes)
    numero_ligne = None
    d = 104
    for num_ligne in dligne :
        last_carte_de_ligne = dligne[num_ligne][-1]
        distance_entre_deux_nombres = carte - last_carte_de_ligne      #je calcule la distance entre le nbre choisi et la derniere carte du la ligne et je compare cette distance a chaque fois

        if  distance_entre_deux_nombres > 0 and distance_entre_deux_nombres < d :
            d = distance_entre_deux_nombres
                
            numero_ligne = num_ligne
                
    return numero_ligne 




########## 4.3.2 #############            
def ramasser_ligne(dlignes, num_ligne, carte) :
    liste_carte = dlignes[num_ligne]
    l_carte_ramasser = list(liste_carte)
    dlignes[num_ligne] = [carte]
    point_penalite = nb_points_tas(l_carte_ramasser)
    return point_penalite





########## 4.3.3 #############
def jouer_carte(carte, nom, dlignes) :
    resultat = trouver_ligne(carte, dlignes)
    point_de_penalite_ramasser = 0
    if resultat == None :
        z = nom,", vous ramassez une ligne."
        textinput("APPUI OK!",z)
        print(nom,", vous ramassez une ligne.")
        choix_ligne =int(numinput("","Quelle ligne choisissez-vous ? ",minval = 1, maxval = 4))
        while not choix_ligne in [1,2,3,4] :
            choix_ligne = int(numinput("Erreur. Quelle ligne choisissez-vous ? ",minval = 1, maxval = 4))
        f = nom,"joue la carte",carte,"sur la ligne",choix_ligne
        print(nom,"joue la carte",carte,"sur la ligne",choix_ligne)
        point_de_penalite_ramasser = ramasser_ligne(dlignes, choix_ligne, carte)
        
        b = nom,", vous ramassez",point_de_penalite_ramasser,"point(s)."
        print(nom,", vous ramassez",point_de_penalite_ramasser,"point(s).")
        textinput("APPUI OK!",str(f)+"\n"+str(b))
        dlignes[choix_ligne] = [carte]
        print()
        
    else :
        if len(dlignes[resultat]) < 5 :
            dlignes[resultat].append(carte)
            f = nom,"joue la carte",carte,"sur la ligne",resultat
            print(nom,"joue la carte",carte,"sur la ligne",resultat)
            textinput("APPUI OK!",f)
        else :
            print(nom,"joue la carte",carte,"sur la ligne",resultat )
            f = nom,"joue la carte",carte,"sur la ligne",resultat
            point_de_penalite_ramasser = ramasser_ligne(dlignes, resultat, carte)
            print(nom,", vous ramassez",point_de_penalite_ramasser,"point(s).")
            b = nom,", vous ramassez",point_de_penalite_ramasser,"point(s)."
            textinput("APPUI OK!",f+"\n"+b)
            print()
            dlignes[resultat] = [carte]
            
    afficher_plateau(dlignes)
    print()
    textinput("","Taper entree pour continuer")
    print()
    return point_de_penalite_ramasser



    
        
########## 4.3.4 #############            
def jouer_tour(djeux, dlignes) :
    dcartes = {}
    l_carte_jouer = []
    for name in djeux :
        carte_choisie = demander_choix(name, djeux[name])
        djeux[name].remove(carte_choisie)
        dcartes[carte_choisie] = name
        l_carte_jouer.append(carte_choisie)
    l_carte_jouer.sort()
    print(l_carte_jouer)
    
    print()

    dico_penal = {}
    for carte in dcartes :
        pt_penal = jouer_carte(carte, dcartes[carte], dlignes)
        dico_penal[dcartes[carte]] = pt_penal
    return dico_penal



##### Estension ####



def jouer_tour_2(djeux, dlignes) :                              # En comprenant le fonctionnement de jouer_tour, jai crée cette fonction qui est tres semblage a jouer_tour sauf qu'ici j'ai enlever la fonction qui permet de demander au joueur quelle carte jouer!
    dcartes = {}                                                # Dans ma boucle for, sachant que djeux ne contient qu'une seul carte desormais, j'ai ajusté la cette partie de la fonction de telle sorte que cette carte(la derniere et la seule restante) puisse etre prise automatiquement dans le jeu de chaque joueurs
    l_carte_jouer = []
    for name in djeux :                                          # le plus important dans cette modification ce trouve dans la fonction jouer_manche, un peu plus bas!!! 
        derniere_carte = djeux[name][0]
        #carte_choisie = demander_choix(name, djeux[name])
        djeux[name].remove(derniere_carte)
        dcartes[derniere_carte] = name
        l_carte_jouer.append(derniere_carte)
    l_carte_jouer.sort()
    print(l_carte_jouer)
    
    print()

    dico_penal = {}
    for carte in dcartes :
        pt_penal = jouer_carte(carte, dcartes[carte], dlignes)
        dico_penal[dcartes[carte]] = pt_penal
    return dico_penal
        
#####################



###########################
###   Partie 4 : programmer une manche, une partie
###########################

########## 4.4.1 #############
def incrementer_scores(score_total, score_partiel) :
    somme = 0
    for name in score_total :
        if name in score_partiel :
            somme = score_total[name] + score_partiel[name]
            score_total[name] = somme
    return score_total




########## 4.4.2 #############
def jouer_manche(ljoueurs, nb_cartes = 10) :
    initialisation_score = init_scores(ljoueurs)
    la_pioche = generer_pioche()
    le_jeu = distribuer_cartes(la_pioche, ljoueurs ,nb_cartes = nb_cartes)######################
    initialisation_ligne = init_lignes(la_pioche)
    #
    afficher_plateau(initialisation_ligne)
    #
    print()
    i = 1
    while i <= nb_cartes :
        if i != nb_cartes :
            score_des_joueurs = jouer_tour(le_jeu, initialisation_ligne)
            initialisation_score = incrementer_scores(score_des_joueurs, initialisation_score)          
        else :                                                                                          # Ici pour que le jeu ne demande pas aux joueurs de jouer les dernieres cartes et que celles ci soient automatiquement choisies, j'ai ajusté ma fonction de telle sorte que le jeu puisse demander au joueur de choisi une carte dans son jeu jusqu'à l'avant derniere carte 
            score_des_joueurs = jouer_tour_2(le_jeu, initialisation_ligne)                              # Ainsi la derniere est prise en compte grace à la fonction jouer_tour_2 dont le role est expliqué plus haut
            initialisation_score = incrementer_scores(score_des_joueurs, initialisation_score)
        i = i + 1
    return initialisation_score



    
########## 4.4.3 #############    
def fin_partie(score_tot, score_final = 66) :   ###### fonction booléenne en suppossant que phrase est True
    maxi = 0
    
    for name in score_tot :
        if score_tot[name] >= maxi :
            maxi = score_tot[name]

            
    if score_final <= maxi :
        #"Fin de la partie"
        return True
    else :
        #"La partie Continue!"
        return False


########## 4.4.4 #############
def afficher_gagnants(score_tot) :
    mini = 104
    l_win = []
    for name in score_tot :
        if score_tot[name] <= mini :
            mini = score_tot[name]

    for name in score_tot :
        if mini == score_tot[name]:
            l_win.append(name)
    a = "Le(s) gagnant(s) est (sont) :",l_win
    print("Le(s) gagnant(s) est (sont) :",l_win)
    return a
    
    

### ATTENTION !! Cette partie est tres longue , Je n'ai pas voulu créer plusieurs fonctions :D   
########## 4.4.5 #############
def jouer_partie(nb_cartes = 10 , score_final = 66) :
    #print("\n\nBienvenu au jeu du {{ Six qui prend }}\n\n")
    
    espace = ""
    while espace != " " :

        dem = demande_partie()
    
        if dem == True :
            nombre_joueur = demander_nb_joueurs()
            nom_joueur = saisie_noms(nombre_joueur)
        
            manche = init_scores(nom_joueur)
            a = False
            m = 1
            while a != True :
                print()
                print("Manche",m,"\n")
                manche_en_cour = jouer_manche(nom_joueur, nb_cartes = nb_cartes)
                manche = incrementer_scores(manche_en_cour, manche)
            
                afficher_scores(manche)
                a = fin_partie(manche, score_final = score_final)
            
                if a != True :
                    a = cont_manche(manche)
                    if a != True :
                        m = m + 1
            f= "Partie finie en",m,"manche(s).\n"
            print("Partie finie en",m,"manche(s).\n")
            u = afficher_gagnants(manche)
            textinput("APPUI ok",str(f)+"\n"+str(u))
            return manche

        elif dem == False :
            g = open("Sauvegarde")
            l_ligne = {} # ici on a donc un dictionnaire vide qui ira recuperer les sauvegardes dans le fichier ou sont les sauvegardes en attibuant a chaque sauvegarde un numero
            t = 1
            for save in g :
                sa = save.replace("\'","\"") # pour me remplacer les " ' " par des " " ". sans ce changement json ne comprendra rien!
                s = json.loads(sa)
                l_ligne[t] = s
                t = t + 1
            g.close()
            #
            #
            if l_ligne == {} :
                print("Pas de sauvegarde!!\n")
                textinput("APPUI OK","Pas de sauvegarde!!\n")
                espace = ""
            
            else :
                #
                #On doit maintenant faire appel a la fonction "selection_sauvegarde_anterieur" qui permet au joueur de choisir un sauvegarde anterieur 
                select = selection_sauvegarde_anterieur(l_ligne)
                #je copie ensuite la version normalle de la fonction jouer_partie que je modifie en supossant que grace à ""select"", j'ai deja le nombre de joueur , leur nom, ainsi que leur scores
                nombre_joueur = len(select)
                print("\nNous avons",nombre_joueur,"joueurs.")
                nom_joueur = []
                for name in select :
                    nom_joueur.append(name)
                print("Leur nom :",nom_joueur,"\n")
            
                manche = select ############## etant donner quand va utiliser les scores precedent, j'ai enlevé la fonction init_scores
                a = False
                m = 1
                while a != True :
                    print()
                    print("Manche",m,"\n")
                    manche_en_cour = jouer_manche(nom_joueur, nb_cartes = nb_cartes)
                    manche = incrementer_scores(manche_en_cour, manche)
                
                    afficher_scores(manche)
                    a = fin_partie(manche, score_final = score_final)
                
                    if a != True :
                        a = cont_manche(manche)
                        if a != True :
                            m = m + 1
                u = "Partie finie en",m,"manche(s).\n"
                print("Partie finie en",m,"manche(s).\n")
                k = afficher_gagnants(manche)
                textinput("APPUI OK!",str(u)+"\n"+str(k))
                espace = " "
                return manche
            
        elif dem == None :
            g = open("Sauvegarde","w")
            g.close()
            print("Sauvegardes supprimer!\n")
            espace = ""
            
        else :
            espace = " "



#ces fonctions font partir de l'extension
#elle me permet de demander si le joueur veut une nouvelle partie ou si il veut continuer une partie anterieur
def demande_partie():
    choix = int(textinput("\n\nBienvenu au jeu du {{ Six qui prend }}\n\n","    1°) NOUVELLE PARTIE\n    2°) CHARGER SCORES PARTIE ANTERIEURE\n    3°) SUPPRIMER SAUVEGARDE\n    4°) QUITTER JEU\nChoisir :"))
    while not choix in [1, 2, 3, 4] :
        choix = int(textinput("Choix invalide!!!\n\n"," 1°) NOUVELLE PARTIE\n 2°) CHARGER SCORES PARTIE ANTERIEURE\n 3°) SUPPRIMER SAUVEGARDE\n 4°) QUITTER JEU\nChoisir :"))
    if choix == 1 :
        return True
    elif choix == 2 :
        return False
    elif choix == 3 :
        return None
    else :
        return "quitter"


def selection_sauvegarde_anterieur(dico_des_resultats_parties_anterieures) : # cette fonction retourne un dictionnaire corespondant a une sauvegarde d'une partie anterieure
    for num in dico_des_resultats_parties_anterieures :
        print(num ,":",dico_des_resultats_parties_anterieures[num],end="\n\n")
    l = []
    for num in dico_des_resultats_parties_anterieures :
        l.append(int(num))
        
    demand_choix = int(input("Choisir une sauvegarde : "))
    
    while not demand_choix in l :
        demand_choix = int(input("\nChoix invalide!!!\n\nChoisir une sauvegarde : "))
        
    return dico_des_resultats_parties_anterieures[demand_choix]


def cont_manche(dico) : #qui demande au joueur si il desire contunier la partie en cours ou sauvegarder et Arreter
    rpp = int(textinput("","1°)Continuer la partie\n2°)Sauvegarder et Arreter\n\nChoisir : "))
    while not rpp in [1,2] :
        rpp = int(textinput("","Choix invalide!!!\n\n1°)Continuer la partie\n2°)Sauvegarder et Arreter\n   Choisir : "))
    if rpp == 1 :
        print("\n\nLa partie continue!\n\n")
        textinput("APPUI ok!","\n\nLa partie continue!\n\n")
        return False
    else :
        g = open("Sauvegarde","a+")
        g.write(str(dico)+ "\n")
        g.close()
        return True
        



    
    

###########################
###   Partie 5 : affichage graphique
###########################

########## 4.5.1 #############
def rectangle(x ,y ,largeur ,hauteur) :
    up()
    goto(x - 5, y)
    down()
    i = 1
    while i <= 2 :
        forward(largeur - 10)
        circle(-5, 90)
        forward(hauteur - 10)
        circle(-5, 90)
        i = i + 1


########## 4.5.2 #############
def couleur_TdB(nb) :
    if nb == 1 :
        couleur = "blanche"
    elif nb == 2 :
        couleur = "bleue"
    elif nb == 3 :
        couleur = "verte"
    elif nb == 5 :
        couleur = "rouge"
    elif nb == 7 :
        couleur = "jaune"
    return couleur


########## 4.5.3 #############
def noms_fichiers(couleur) :
    fich_mini = "images/mini_TdB_" + couleur + ".gif"
    fich_grand = "images/TdB_" + couleur + ".gif"
    return fich_grand, fich_mini


########## 4.5.4 #############
def dessiner_carte(carte, x ,y) :
    #
    rectangle(x ,y ,100 ,150)
    #
    nb_pt_carte = nb_points_carte(carte)
    couleur_de_carte = couleur_TdB(nb_pt_carte)
    nom_fich_grd, nom_fich_pt = noms_fichiers(couleur_de_carte)
    #
    afficher_symbole(x - 10  + 50 ,y - 10 - 75 ,nom_fich_grd)       # -10 a cause des boards courbé de rayon 5 cm
    #
    
    X = x -10 + 50
    Y = y - 10 - 10*0.02646
    n = nb_pt_carte//2    
        
    if nb_pt_carte % 2 != 0:
        afficher_symbole(X ,Y ,nom_fich_pt)
    
        n = nb_pt_carte//2
        j = 1
        while j <= n :
            X = X - 500*0.0246
            afficher_symbole(X ,Y ,nom_fich_pt)     # 1 pixel = 0.0246 cm
            j = j + 1
        #
        X = x -10 + 50
        j = 1
        while j <= n :
            X = X + 500*0.0246
            afficher_symbole(X ,Y ,nom_fich_pt)
            j = j + 1
                
    else :
        afficher_symbole(X - 250*0.0246 ,Y ,nom_fich_pt)
        afficher_symbole(X + 250*0.0246,Y ,nom_fich_pt)
         
    ecrire_xy(str(carte),x +50 - 10 ,y -125,taille = 45,couleur="purple")



########## 4.5.5 #############
def dessiner_plateau(dlignes) :
    reinitialiser_affichage()
    A = -300
    B = 350
    for ligne in dlignes :
        l = dlignes[ligne]
        ecrire_xy("Ligne " + str(ligne)+ " :" ,A - 100 ,B - 100 ,taille = 15,couleur="blue")
        for carte in l :
            dessiner_carte(carte, A ,B)
            A = A + 125
        B = B - 175
        A = -300



        
# fournie
def charger_images():
    """ Permet de charger les images correspondant aux dessins du jeu,
    en vue de l'affichage graphique en turtle"""
    couleurs_maxi = ["blanche", "bleue","verte", "rouge", "jaune"]    
    for couleur in couleurs_maxi :
        register_shape("images/TdB_" + couleur + ".gif")

    couleurs_mini = couleurs_maxi # attention : ce n'est pas une copie
    for couleur in couleurs_mini :
        register_shape("images/mini_TdB_" + couleur + ".gif")
    
    
# fournie
def reinitialiser_affichage() :
    """Efface l'affichage actuel et restaure les parametres
    de vitesse de tortue (au plus rapide) et de cacher le curseur"""
    # effacer fenetre graphique 
    reset()
    # mais on a aussi rénitialiser certains paramètres, on restaure :
    # accelerer l'affichage et cacher la tortue
    speed("fastest")
    hideturtle()

# fournie
def afficher_symbole(x,y,nom_fichier) :
    """Affiche le symbole correspondant a l'image stockee dans le fichier de nom indiqué dans
    nom_fichier. Le centre du symbole est aux coordonnees (x,y) de la fenetre.La taille du symbole est
    de 100 (en largeur) sur 50 (en hauteur)."""
    up()
    goto(x,y)
    shape(nom_fichier)
    stamp() # pour afficher le symbole (comme un tampon)
    down()
    hideturtle()

# fournie
def ecrire_xy(texte,x,y,taille=45,couleur="blue") :
    """Ecrit le texte contenu dans l'argument texte, a une position dont le centre est
    aux coordonnees (x,y)"""
    pencolor(couleur)
    up()
    goto(x,y)
    write(texte,align="center",font=("Helvetica",taille,"bold"))
    down()

    
if __name__ == "__main__" :
    ######################################################
    # la partie ci-dessous est en commentaire car elle est seulement utile
    # pour l'affichage graphique. Il faudra décommenter quand vous commencerez
    # à dessiner avec turtle

    setup(width=1100,height=800)
    charger_images()
    reinitialiser_affichage()

    #########################################################

    ## Mettez vos tests ci-dessous :
    
    liste_cart = [12, 86, 95, 67, 77]
    #liste_carte = {1 :[5, 12],2: [10, 13, 14, 17, 55],3: [20],4: [6]}
    #dico_joueur = {"titi" : [9, 99, 75 ,4], "toto" : [64, 55, 88, 11, 101]}
    #s_tot = {"tata" : 3, "titi" : 0, "toto" : 0}
    #l = ["toto", "bill" ,"rere"]
    #s_pa = {"titi" : 0, "toto" : 5,"tata" : 8}
    #afficher_gagnants(s_tot)
    #afficher_liste_cartes(liste_cart)
    #afficher_scores(s_pa, nature = "manche")
    #dico_des = {1 : {"Bill":2,"toto": 5, "Aurel" : 18},2 :{},3 : {"Bruno":59, "Fauro" :104}}
    #selection_sauvegarde_anterieur(dico_des)
    jouer_partie(nb_cartes = 2, score_final = 75)
