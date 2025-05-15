from airSpace import AirSpace


asp = AirSpace()
asp.load_all('Cat_nav.txt', 'Cat_seg.txt', 'Cat_aer.txt')
print(asp)
print("Primeros puntos de navegación:", asp.nav_points[:5])
print("Primeros segmentos:", asp.nav_segments[:5])
print("Aeropuertos:", asp.nav_airports)
