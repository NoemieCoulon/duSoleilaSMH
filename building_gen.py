import csv
import building as build

dict_buildings ={}
with open('batiments.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['nom']
        pdl = row['pdl']
        gps_x = float(row['gps_x'].replace(",", "."))
        gps_y = float(row['gps_y'].replace(",", "."))
        coordinates = [gps_x,gps_y]
        conso_annuelle = float(row['conso_annuelle'])
        faisabilite_prod = row['faisabilite_prod']

        # Example Usage
        if faisabilite_prod:
            roof_surface = int(row['surface_toit'])
            building = build.ProdBuilding(pdl,name, coordinates, conso_annuelle,roof_surface)
        else:
            building = build.Building(pdl,name, coordinates, conso_annuelle, faisabilite_prod)

        dict_buildings[pdl] = building