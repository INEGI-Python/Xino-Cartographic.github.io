import os
import geopandas as geo
from shapely import Point,Polygon
from qgis.core import QgsProject, QgsVectorLayer

datos=geo.read_file("E:/Compartida/predio.xlsx")
print(datos)

geom=[Point(v.X,v.Y) for k,v in datos.iterrows()]
vertices = geo.GeoDataFrame(data=[{"id":i} for i in range(len(geom))],geometry=geom,crs=4486)
vertices["x"]=vertices.geometry.x
vertices["y"]=vertices.geometry.y
poli = geo.GeoDataFrame(data=[{"id":1}],geometry=[Polygon(geom)],crs=4486)
poli["area"]=poli.geometry.area

temp = poli.minimum_bounding_circle().buffer(20).bounds
minx, miny, maxx, maxy = temp.iloc[0]
minx-=50
maxx+=50
rect = Polygon([(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)])
print(rect)
marco = geo.GeoDataFrame(data=[{"id":1}],geometry=[rect],crs=4486)



try:
    os.mkdir("shapes")
except Exception as e:
    print(e)
poli.to_file("shapes/predio1.shp")
marco.to_file("shapes/marco1.shp")
vertices.to_file("shapes/vertices.shp")

proyecto=QgsProject.instance()
proyecto.addMapLayer(QgsVectorLayer("shapes/marco1.shp","marco"),True)
proyecto.addMapLayer(QgsVectorLayer("shapes/predio1.shp","predio1"),True)
proyecto.addMapLayer(QgsVectorLayer("shapes/vertices.shp","vertices"),True)

