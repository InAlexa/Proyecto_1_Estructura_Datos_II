from proveedor import Provider
from arbol import ArbolBPlus

def menu():
    print("\n------------Plataforma de Servicios------------")
    print("1. Registrar proveedor")
    print("2. Buscar por servicio")
    print("3. Listar por ID")
    print("4. Listar por nombre (A → Z)")
    print("5. Listar por calificación (mayor → menor)")
    print("6. Buscar por ID")
    print("7. Ver hojas")
    print("8. Salir")

def data(tree: ArbolBPlus):
    tree.insertar(10, Provider(10, "Ana López", "Electricista", "Zona 1", "4.8"))
    tree.insertar(3,Provider(3, "Carlos Pérez", "Plomero", "Mixco", "4.5"))
    tree.insertar(21,Provider(21, "María García", "Carpintero", "Villa Nueva", "4.2"))
    tree.insertar(15,Provider(15, "Luis Ramírez", "Programador", "Zona 10", "5"))
    tree.insertar(7,Provider(7, "Sofía Morales", "Diseñador", "Zona 4", "4.9"))
    tree.insertar(30, Provider(30, "Jorge Díaz", "Electricista", "Amatitlán", "4.0"))
    tree.insertar(12, Provider(12, "Elena Castillo", "Plomero", "Zona 5", "3.8"))
    tree.insertar(18, Provider(18, "Diego Ortiz", "Programador", "Zona 15", "4.7"))
    tree.insertar(25, Provider(25, "Lucía Herrera", "Carpintero", "Zona 2", "4.3"))
    tree.insertar(5, Provider(5, "Pablo Rojas", "Electricista", "Zona 7", "4.1"))

def print_list(items):
    if not items:
        print("(No se encontraron resultados)")
        return
    for i in items:
        print(" ", i)

def main():
    tree = ArbolBPlus(orden=3)
    data(tree)

    while True:
        menu()
        op = input("Opción: ").strip()

        if op == "1":
            try:
                id_ = int(input("ID: ").strip())
                nombre = input("Nombre: ").strip()
                servicio = input("Servicio: ").strip()
                ubicacion = input("Ubicación: ").strip()

                while True:
                    try:
                        rating = float(input("Calificación (1 - 5): ").strip())
                        if 1.0 <= rating <= 5.0:
                            break
                        else:
                            print("❌ La calificación debe estar en un intervalo 1 y 5.")
                    except ValueError:
                        print("❌ Ingresa un número válido.")

                prov = Provider(id_, nombre, servicio, ubicacion, str(rating))
                tree.insertar(id_, prov)
                print("✅ insertado con exito")

            except ValueError:
                print("ID inválido.")
        elif op == "2":
            servicio = input("Servicio a buscar: ").strip()
            res = tree.buscar_por_servicio(servicio)
            print(f"Resultados para servicio '{servicio}':")
            print_list(res)
        elif op == "3":
            print("Proveedores por ID:")
            print_list(tree.listar_todos())
        elif op == "4":
            print("Proveedores por nombre (A → Z):")
            print_list(tree.listar_por_nombre())
        elif op == "5":
            print("Proveedores por calificación (mayor → menor):")
            print_list(tree.listar_por_calificacion(descendente=True))
        elif op == "6":
            try:
                id_ = int(input("ID a buscar: ").strip())
                p = tree.buscar_por_id(id_)
                if p:
                    print("Encontrado:", p)
                else:
                    print(f"No existe un proveedor con el ID: {id_}")
            except ValueError:
                print("ID inválido.")
        elif op == "7":
            tree.imprimir_hojas()
        elif op == "8":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
