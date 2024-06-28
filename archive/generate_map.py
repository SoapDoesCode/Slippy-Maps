import folium

Home = [52.69057, -1.83225]
ToAddress = [52.69484985542316, -1.8511296619054012]

map = folium.Map(location=Home,zoom_start=15)
folium.CircleMarker(location=Home,radius=50,popup = "anyplace").add_to(map)
folium.Marker(Home,popup= "Home").add_to(map)
folium.Marker(ToAddress,popup= "New Address").add_to(map)
folium.PolyLine(locations=[Home,ToAddress],line_opacity = 0.6).add_to(map)
map.save("map.html")

# https://www.openstreetmap.org/#map=18/52.69057/-1.83225