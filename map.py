import folium
from folium.plugins import MarkerCluster
import building_gen as buildings
import roof_gen as roof
from jinja2 import Template

# Create the base map
c = folium.Map(location=[45.18, 5.76], zoom_start=15)

# Load the buildings and roofs data
dict_buildings = buildings.dict_buildings
dict_roofs = roof.dict_roofs

# Create two feature groups for the layers
group_pdl = folium.FeatureGroup(name="Compteurs").add_to(c)  # Layer for buildings

# Create separate FeatureGroups for roof potential
group_high_potential = folium.FeatureGroup(name="Potentiel élevé").add_to(c)
group_medium_potential = folium.FeatureGroup(name="Potentiel moyen").add_to(c)
group_other_potential = folium.FeatureGroup(name="Autres").add_to(c)

# Create a MarkerCluster for roofs
marker_cluster_high = MarkerCluster(name="Toits (Potentiel élevé)").add_to(group_high_potential)
marker_cluster_medium = MarkerCluster(name="Toits (Potentiel moyen)").add_to(group_medium_potential)
marker_cluster_other = MarkerCluster(name="Toits (Autres)").add_to(group_other_potential)

# Add red markers (buildings) to 'group_pdl'
for pdl in dict_buildings:
    folium.Marker(
        location=dict_buildings[pdl].coordinates,
        icon=folium.Icon(color="red"),
        popup=dict_buildings[pdl].name + " \nConso Annuelle: " + str(dict_buildings[pdl].year_consumption)
    ).add_to(group_pdl)

# Add roof markers to the appropriate marker clusters based on potential
for name in dict_roofs:
    if dict_roofs[name].pdl != "NA" and dict_roofs[name].pdl != "":
        roof_m2 = dict_roofs[name].roof_m2
        coordinates = dict_buildings[dict_roofs[name].pdl].coordinates
        popup_content = f"{dict_roofs[name].name} - Roof Surface: {roof_m2} m² - {dict_roofs[name].potential}"
        
        # Check the potential and assign the marker to the correct group
        if dict_roofs[name].potential == "Potentiel élevé":
            folium.Marker(
                location=coordinates,
                popup=popup_content,
                icon=folium.Icon(color="darkblue")
            ).add_to(marker_cluster_high)
        elif dict_roofs[name].potential == "Potentiel moyen":
            folium.Marker(
                location=coordinates,
                popup=popup_content,
                icon=folium.Icon(color="cadetblue")
            ).add_to(marker_cluster_medium)
        else:
            folium.Marker(
                location=coordinates,
                popup=popup_content,
                icon=folium.Icon(color="blue")
            ).add_to(marker_cluster_other)

# Add LayerControl to toggle between layers
folium.LayerControl().add_to(c)

# Save the map as an HTML file
c.save('maCarte.html')
