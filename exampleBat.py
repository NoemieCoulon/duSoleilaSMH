import batiment as bat
import configparser
import os
config = configparser.ConfigParser()

ini_file = []
for dirpath, dirnames, filenames in os.walk("."):
   for filename in filenames:
      if filename.endswith(".ini"):
        ini_file.append(filename)
dict_batiment = {}
for file in ini_file:
    config.read(file)
    name = config['Fixed']['nom']
    coordonnees = (float(config['Fixed']['coordonnees_gps_x']),float(config['Fixed']['coordonnees_gps_y']))
    roof_surface = config['Fixed']['surface_toit']
    prod_possible = eval(str(config['Fixed']['production_possible']))
    # Example Usage
    if prod_possible:
        pv_surface = config['Fixed']['surface_pv_dispo']
        batiment = bat.BatimentProducteur(name, coordonnees)
        batiment.__set_surface__(roof_surface, pv_surface)
    else:
       batiment = bat.Batiment(name, coordonnees, prod_possible)

    dict_batiment[name] = batiment

for name in dict_batiment:
    print('###########')
    dict_batiment[name].get_info()
    print('###########')


    # Display consumption graph
    # batiment.show_consumption()
    # batiment.show_production()