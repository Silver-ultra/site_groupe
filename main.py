# faire les import
from flask import Flask, render_template, session, redirect, request
import pymongo

# créer l'apilcation
app = Flask("Jeu_groupe")
app.secret_key = "Iamacoolkid"
mongo = pymongo.MongoClient("mongodb+srv://Silver:uJxPktFx7uTg3J59@cluster0.8rm9m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

@app.route("/")
def accueil() :
    if "utilisateur" in session :
        mes_utilisateurs = mongo.bddd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : session["utilisateur"]})
        print(utilisateur)
        mes_groupes = mongo.bddd.groupes
        groupes = mes_groupes.find({})
        return render_template("index.html", utilisateur = utilisateur, groupes = groupes)
    else :
        return render_template("index.html",)

@app.route('/profil')
def profil() :
    if "utilisateur" in session :
        mes_utilisateurs = mongo.bddd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : session["utilisateur"]})
        print(utilisateur)
        return render_template("profil.html", utilisateur = utilisateur)
    else :
        return redirect("/")
    
@app.route('/logout')
def logout() :
    session.clear()
    return redirect("/")

@app.route("/register", methods = ["GET", "POST"])
def register() :
    if request.method == "GET" :
        return render_template("register.html")
    else :
        # 1 : on récupère les informations entrées dans les boîtes (inputs)
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        avatar_entre = request.form["input_avatar"]
        if avatar_entre == "" :
            avatar_entre = "https://sbcf.fr/wp-content/uploads/2018/03/sbcf-default-avatar.png"
        # 2 : on gère tous les cas d'erreur
        mes_utilisateurs = mongo.bddd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_entre})
        # si le pseudo existe déjà
        if utilisateur :
            return render_template("register.html", erreur = "L'utilisateur existe déjà")
        # si aucun pseudo n'a été rentré    
        elif pseudo_entre == "" :
            return render_template("register.html", erreur = "Veuillez rentrer un pseudo")
        # si le mot de passe ne fait pas assez de caractères
        elif len(mdp_entre) < 4 :
            return render_template("register.html", erreur = "Le mot de passe doit faire au moins 4 caractères")
        else :
            # 3 : on crée le compte utilisateur
            mes_utilisateurs.insert_one({
                "pseudo" : pseudo_entre,
                "mdp" : mdp_entre,
                "avatar" : avatar_entre,
                "age" : 0,
                "nationalite" : "non précisée"
            })
            # on connecte l'utilisateur via le cookie
            session["utilisateur"] = pseudo_entre
            # on redirige vers la page d'accueil
            return redirect("/")

@app.route('/login', methods = ["GET","POST"])
def login() :
    if request.method == "GET" :
        return render_template("login.html")
    else :
        pseudo_entre = request.form["input_pseudo"]
        mdp_entre = request.form["input_mdp"]
        
        mes_utilisateurs = mongo.bddd.utilisateurs
        utilisateur = mes_utilisateurs.find_one({"pseudo" : pseudo_entre})
        #test user
        if not utilisateur :
           return render_template("login.html", erreur = "L'identifiant ou le mot de passe est incorrect")
        #test mdp
        elif mdp_entre != utilisateur["mdp"] :
            return render_template("login.html", erreur = "L'identifiant ou le mot de passe est incorrect")
        #ça fontionne
        else : 
            session["utilisateur"]= pseudo_entre
            print("test")
            return redirect("/")

@app.route("/find")
def find():
    db_utilisateurs = mongo.bddd.utilisateurs
    resultat = db_utilisateurs.find({})
    return render_template("test.html", resultat = list(resultat))

@app.route("/findone")
def findone():
    db_utilisateurs = mongo.bddd.utilisateurs
    resultat = db_utilisateurs.find_one({"pseudo" : "Erreur"})
    return render_template("test.html", resultat = resultat)

@app.route("/liste")
def jeux():
    return render_template("jeux.html")

@app.route("/admin/groupe")
def adminroute():
    db_groupe = mongo.bddd.groupes
    mes_groupes = db_groupe.find({})
    return render_template("Admin/admin_page.html", mes_groupes=list(mes_groupes))

@app.route("/supprimergroupe/<nom>")
def supprimerg(nom):
    db_groupe=mongo.bddd.groupes
    db_groupe.delete_one({"Nom": nom})
    return redirect("/admin/groupe")


# lancement de l'app
app.run(host="0.0.0.0", port="3904")