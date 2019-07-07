######################################################################################################
# CONTENU DU FICHIER 4 fonctions à savoir:
#
# 1. afficher_pres_etud_au_cours(valeurs): 
#                     afficher les présence d'un étudiant à toutes les séance d'un cours donné
# 2. afficher_tdp_etud_au_cours(valeurs):
#                     afficher le taux de participation d'un étudiant à un cours donné
# 3. afficher_tdp_etud_all_cours(valeurs):
#                     affiche les taux de participation d'un étudiant à tous ses cours
# 4. afficher_tdp_all_stud_au_cours(valeurs):
#                     affiche le taux de participation de tous les étudiants à un cous donnée
###########################################################################################################

from list_data import *                         # importation du module list_data (il contient des fonctions dont on aura besoin)
from db_add import *

# ============= AFFICHER LES PRESENCES D'UN ETUDIANT A TOUTES LES SEANCES D'UN COURS ====================
def afficher_pres_etud_au_cours():
    acro = input("Veuillez saisir l'acronime du cours : ")
    mat = input("Veuillez saisir le matricule de l'etudiant : ")

    tab_pres = pres_etud_au_cours(acro,mat)     # le tableau de présences propre à l'étudiant
    pres_str = ""                               # la chaine finale qui contiendra les présences de l'étudiant
    for p in tab_pres:                          # on parcourt toutes les présences de l'étudiant une-à-une
        date, am_pm, p_a, resume = p[3], p[4], p[1], p[5] #affectation multiple de trois éléments qui font la présence
        pres_str += ("""
        -> %s %s  - %s """ % (date, am_pm, p_a))# d'un étudiant à une séance et on les ajoute à la chaine finale
        if (p_a=='A'):                          # et si l'étudiant était absent à la séance
            pres_str += """
                Résumé: %s """ % (resume)       # on ajoute aussi le résumé de la leçon faite à cette séance-là
                                                # et après voir traité toutes les présence de l'étudiant
    finaliser_affi_pres_etud(pres_str,mat,acro) # on peut maintenant finaliser l'affichage en envoyant 
                                                # la chaine finale, le matricule de l'étudiant et l'acronyme

# ============= TAUX DE PARTICIPAT D'UN ETUDIANT A UN COURS ===================================
def afficher_tdp_etud_au_cours():

    acro = input("Veuillez saisir l'acronime du cours : ")
    mat = input("Veuillez saisir le matricule de l'etudiant : ")

    tab_pres = pres_etud_au_cours(acro,mat)     # le tableau des présence de l'étudiant au cours
    tdpc     = tdpc_etud(tab_pres)              # calculs du taux de participation 
    finaliser_affi_tdpc_etud(tdpc,mat,acro)# et pour finir finalisons l'affichage

# ============= TAUX DE PARTICIPAT D'UN ETUDIANT A TOUS SES COURS===================================
def afficher_tdp_etud_all_cours(valeurs):
    """affiche les taux de participation d'un étudiant à tous ses cours"""

    mat = input("Veuillez saisir le matricule de l'etudiant : ")
    etud = find_element(f_etudiant(),mat,0)     # trouve l'étudiant dont le matricule est mat        
    entete = """
        Taux de Participation aux Cours de %s 
    Etudiant:  %s   Mat: %s   
    --------------------------------------------------------
    """                                             # chaine paramétrée
    entet_block = "    %s%sEnseignants\n    %s"     # à placer à la tête de la liste
                                                    
    print(entete % (etud[2],etud[1],etud[0]))       # on affiche l'entête et on affichage l'entête                                                 
    print(entet_block % ( b("TDPC",10), b("Cours Dispensés"), b('',50,'-'))) # de la liste   
    

    cours  = loard_data(f_cours())                  # charge tous les cours
    for num,cr in enumerate(cours):                 # parcour de chaque tuple, indice et cours
        acro = cr[0]                                # acronyme du cours
        tab_pres = pres_etud_au_cours(acro,mat)     # présences de l'étudiant au cours
        tdpc     = tdpc_etud(tab_pres)              # calculs du taux de participation au cours
        
        print("    %s%s%s " % (b(tdpc,10),b(cr[1]),cr[3]))

# ============= TAUX DE PARTICIPAT DE TOUS LES ETUDIANTS A UN COURS===================================
def afficher_tdp_all_stud_au_cours():
    acro = input("veuillez saisir l'acreonyme du cours : ")
    """affiche le taux de participation de tous les étudiants à un cous donnée"""
    entete = """
    Taux de Participation au Cours de : %s,  
    Promotion : %s 
    Enseignant: %s
    """                                         # entête principal de la liste
    entete_block = """

    -------------------------------------------------------
        N°    Mat.     TDP.   Etudiants
    -------------------------------------------------------"""# entete d'un block à reprendre après chaque 25 ligne
    ligne = """
        %s.  %s   %s   %s"""                    # le format que prendront les ligne à afficher
    # ==================================================================================

    
    etudiants = loard_data(f_etudiant())        # chargement de tous les étudiants
    for ie,etud in enumerate(etudiants):        # parcourt tous les étudiant un-à-un
        mat = etud[0]                           # matricule de l'étudiant
        tab_pres = pres_etud_au_cours(acro,mat) # les présences de l'étudiant au cours
        etud.append(tdpc_etud(tab_pres))        # le taux de participation de l'étudiant est ajouté à l'étudiant
        etudiants[ie] = etud                    # et l'étudiant est retourner dans le tableau avec son tdpc
        
    cr = find_element(f_cours(),acro,0)         # trouve le cours dont l'acronyme est acro
    print(entete % (cr[1], cr[2], cr[3]))       # on affiche l'entete de la liste
                                                
    
    for i,etud in enumerate(etudiants):
        if (i%25 == 0):                         # on n'affiche l'entête du block que si on est à 
            print(entete_block, end='')         # un indice multiple de 25, à par 0, évidemment
        text = ligne % ((i+1),etud[0],etud[-1],etud[1]) # on construit la ligne
        print(text,end='')                      # on affiche la ligne et on supprime le passage à la lige

    print("Vous avez toutes les informations!") # juste pour rire,

def ensemble_cours():
    new_tab = []

    print("Veuillez choisir les cours \nTapez ok pour choisir et non pour ne pas choisir\nstop pour mettre fin au proposition des acronyme ")
    for ligne in loard_data(f_cours()):
        print(ligne[0])
        ok = input("choix : ")
        if ok == 'ok':
            new_tab.append(ligne)
        elif ok == 'stop':
            break
    return new_tab


# ============= TAUX DE PARTICIPAT D'UN ETUDIANT A UN ENSEMBLE DES COURS===================================
def afficher_tdp_etud_ens_cours():
    mat = input("veuillez saisir le matricule de l'etudiant : ")
    etud = find_element(f_etudiant(), mat, 0)  # trouve l'étudiant dont le matricule est mat
    entete = """
            Taux de Participation aux Cours de %s 
        Etudiant:  %s   Mat: %s   
        --------------------------------------------------------
        """  # chaine paramétrée
    entet_block = "    %s%sEnseignants\n    %s"  # à placer à la tête de la liste

    print(entete % (etud[2], etud[1], etud[
        0]))  # on affiche l'entête et on affichage l'entête
    print(entet_block % (b("TDPC", 10), b("Cours Dispensés"), b('', 50, '-')))  # de la liste

    cours = ensemble_cours()  # charge tous les cours
    for num, cr in enumerate(cours):  # parcour de chaque tuple, indice et cours
        acro = cr[0]  # acronyme du cours
        tab_pres = pres_etud_au_cours(acro, mat)  # présences de l'étudiant au cours
        tdpc = tdpc_etud(tab_pres)  # calculs du taux de participation au cours

        print("    %s%s%s " % (b(tdpc, 10), b(cr[1]), cr[3]))


# ============= TAUX DE PARTICIPAT DE TOUS LES ETUDIANTS INFERIEUR OU EGALE A 75%===================================
def afficher_tdp_all_stud_inf_75():
    acro = input("veuillez saisir l'acronyme du cours : ")

    entete = """
        Taux de Participation au Cours de : %s,  
        Promotion : %s 
        Enseignant: %s
        """  # entête principal de la liste
    entete_block = """

        -------------------------------------------------------
            N°    Mat.     TDP.   Etudiants
        -------------------------------------------------------"""  # entete d'un block à reprendre après chaque 25 ligne
    ligne = """
            %s.  %s   %s   %s"""  # le format que prendront les ligne à afficher
    # ==================================================================================


    etudiants = loard_data(f_etudiant())  # chargement de tous les étudiants
    for ie, etud in enumerate(etudiants):  # parcourt tous les étudiant un-à-un
        mat = etud[0]  # matricule de l'étudiant
        tab_pres = pres_etud_au_cours(acro, mat)  # les présences de l'étudiant au cours
        etud.append(tdpc_etud(tab_pres))  # le taux de participation de l'étudiant est ajouté à l'étudiant

        if tdpc_etud_inf75(tab_pres) <=75.0:
           etudiants[ie] = etud  # et l'étudiant est retourner dans le tableau avec son tdpc
           print(tdpc_etud(tab_pres))

    cr = find_element(f_cours(), acro, 0)  # trouve le cours dont l'acronyme est acro
    print(entete % (cr[1], cr[2], cr[3]))  # on affiche l'entete de la liste

    for i, etud in enumerate(etudiants):
        if (i % 25 == 0):  # on n'affiche l'entête du block que si on est à
            print(entete_block, end='')  # un indice multiple de 25, à par 0, évidemment
        text = ligne % ((i + 1), etud[0], etud[-1], etud[1])  # on construit la ligne
        print(text, end='')  # on affiche la ligne et on supprime le passage à la lige

def jusifier_absence():
    acro = input("veuillez saisir l'acronyme du cours :")
    date = input("veuillez saisir la date de la seance :")
    am_pm = input("veui saisir AM pour l'avant-midi ou PM pour l'après-midi : ")
    mat = input("veuillez saisir le matricule de l'etudiant : ")
    tab_pres = loard_data(f_presence(acro, date, am_pm))
    i = 0
    for ligne in tab_pres:
        neww = ligne
        print(ligne[0])
        if ligne[0]==mat:
            print(ligne," SEANCE TROUVER")
            ligne[1]='P'
            print(ligne, " ABSENCE JUSTIFIER")
            break
        i=i+1
        tab_pres.remove(neww)
        tab_pres.append(ligne)
    rewrite_the_file(tab_pres,f_presence(acro, date, am_pm))