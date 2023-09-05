import geopandas as gpd
from shapely.geometry import Point

# Coordenadas WGS 84 UTM
easting = 562504  # Exemplo de coordenada leste
northing = 8569182  # Exemplo de coordenada norte
zona_utm = 24  # Substitua pela zona UTM desejada

# Crie um objeto Point no sistema de coordenadas WGS 84 UTM
ponto_utm = Point(easting, northing)

# Carregue o conjunto de dados geoespaciais com informações sobre os municípios
gdf_municipios = gpd.read_file('C:\\Users\savio.silva\\Downloads\\BA_Municipios_2022 (1)\\BA_Municipios_2022.shp')

# Realize a consulta no conjunto de dados geoespaciais
municipio = gdf_municipios[gdf_municipios.geometry.contains(ponto_utm)]

# Exiba informações sobre o município encontrado
if not municipio.empty:
    print("Nome do Município:", municipio['NOME_DO_MUNICIPIO'].values[0])
else:
    print("Município não encontrado para as coordenadas WGS 84 UTM fornecidas na Zona", zona_utm)
