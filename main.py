from Models.Neo4jDriver import *

menu = {
    1: "Afficher toutes les finales (années, pays, ...)",
    2: "Afficher toutes les équipes ayant participées aux finales",
    3: "Afficher les résultats obtenus pour une équipe donnée toutes années confondues",
    4: "Afficher le pays, la ville, le stade, les 2 équipes finalistes et le résultat pour une finale donnée"
}


def show_dict():
    print("----------------------------------")
    for k, v in menu.items():
        print(f'{k} : {v}')
    print("----------------------------------")


n = Neo4jDriver("Resources/config.json")

while True:
    show_dict()
    choice = int(input("Entrez votre choix svp: "))
    print("----------------------------------")
    if choice == 1:
        finals = n.get_finals()
        for d, i in enumerate(finals):
            print(f"{d} - Final of {i['year']}, stadium: \"{i['stadium']}\" in {i['city']} ({i['country']})")
        continue
    elif choice == 2:
        teams = n.get_final_teams()
        for d, i in enumerate(teams):
            print(f"{d} - {i['name']}")
        continue
    elif choice == 3:

        continue
    elif choice == 4:
        year = int(input("Entrez l'année de la finale svp: "))
        results = n.get_year_results(year)
        if len(results) != 0:
            if results[0]['f'] == results[1]['f']:
                r = results[0]['f']
                t1 = [results[0]['t'], results[0]['r.winner']] if results[0]['r.winner'] else [results[0]['t']]
                t2 = [results[1]['t'], results[1]['r.winner']] if results[1]['r.winner'] else [results[1]['t']]
                print(f"Final of {r['year']}, stadium: \"{r['stadium']}\" in {r['city']} (in {r['country']}),", end=" ")
                if len(t1) == 2:
                    print(f"Team {t1[0]['name']} {t1[1]} against team {t2[0]['name']}")
                else:
                    print(f"Team {t2[0]['name']} {t2[1]} against team {t1[0]['name']}")
        else:
            print("No final this year")
    else:
        break

n.driver.close()
print("\nProgram finished")
