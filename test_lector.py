from datos_satelites import XLSXLectorSatelite

lector = XLSXLectorSatelite("datos3.xlsx")

satelites = lector.read_data()

for s in satelites:
    print(f"Satélite ID: {s.id}")
    print(f"Cantidad de datos: {len(s.datos)}")

    count_outer_visible = sum(1 for datos in s.datos if datos.is_visible_outer)
    print(f"Cantidad de datos con is_visible_outer=True: {count_outer_visible}")

    count_inner_visible = sum(1 for datos in s.datos if datos.is_visible_inner)
    print(f"Cantidad de datos con is_visible_inner=True: {count_inner_visible}")