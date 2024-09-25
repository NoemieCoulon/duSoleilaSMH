import batiment as bat
# Example Usage
batiment_prod = bat.BatimentProducteur("Ecole Maternelle", "45.764043, 4.835659")
batiment_prod.__set_surface__(1000, 500)
batiment_prod.get_info()

# Display consumption graph
batiment_prod.show_consumption()