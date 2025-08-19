
class Provider:
    def __init__(self, id:int, nombre: str, servicio: str, ubicacion:str, calificacion: str):
        self.id =id
        self.name = nombre
        self.service = servicio
        self.location = ubicacion
        self.rating = calificacion
        return

    def __str__(self):
        return f"[{self.id}] {self.name} - {self.service} - {self.location} - ⭐{self.rating}"
