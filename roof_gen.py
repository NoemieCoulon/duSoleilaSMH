import csv
import roof as r

dict_roofs ={}
with open('roofs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['nom']
        pdl = row['pdl']
        roof_m2 = row['roof_m2']
        potential = row['potential']
        
        roof = r.Roof(name, pdl, roof_m2, potential)
        
        dict_roofs[name] = roof