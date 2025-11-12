import geopandas
import pandas

# Importing the shapefiles of Cells, Germs, Thiessen Polygons
cells = geopandas.read_file('Absolute Path/Cells.shp')
germs = geopandas.read_file('Absolute Path/Germs.shp')
thiessen_polygons = geopandas.read_file('Absolute Path/Thiessen_poly.shx')

# Adding a new column to the thiessen_polygons attributes table
thiessen_polygons['Germ_Name'] = 'to be filled later'

for index, row in thiessen_polygons.iterrows():
    for index_, row_ in germs.iterrows():
        # Acquiring the name of the corresponding germ into the attributes table of the polygons
        if row['geometry'].contains(germs.iloc[index_]['geometry']):
            thiessen_polygons.loc[index, 'Germ_Name'] = row_['Name']

# Intersecting thiessen polygons with the cells
intersect_poly = geopandas.overlay(thiessen_polygons, cells, how = 'intersection')

# Create a new column called 'Shape_Area'
intersect_poly['Shape_Area'] = intersect_poly.area/1000000

# Extracting the Cell and Area columns from the geodataframe to a new pandas dataframe
cell_areas = pandas.DataFrame(cells[['Cell', 'Area']])
cell_areas.set_index('Cell', inplace = True)

# Adding a new column to the intersect_poly attributes table
intersect_poly['weights'] = 0

# Assign the thiessen weights to the new column
for index_a, row_a in intersect_poly.iterrows():
    intersect_poly.loc[index_a, 'weights'] = row_a['Shape_Area']/(cell_areas.loc[row_a['Cell']]['Area'])

# Creating a new pandas dataframe to save the weights
weights = pandas.DataFrame(intersect_poly[['Germ_Name', 'Cell', 'weights']])
weights.to_csv('Name_of_file.csv')
