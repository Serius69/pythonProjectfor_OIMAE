import random
class Subasta:
    def __init__(self, n_postores, valor_real):
        self.n_postores = n_postores
        self.valor_real = valor_real
        self.postores = [Postor(i) for i in range(n_postores)]

class Postor:
    def __init__(self, id):
        self.id = id
        self.valoracion = 0
        self.oferta = 0

    def hacer_oferta(self, tipo_info):
        if tipo_info == "perfecta":
            self.oferta = self.valoracion
        elif tipo_info == "imperfecta":
            self.oferta = random.uniform(0.8 * self.valoracion, 1.2 * self.valoracion)
        else:  # incompleta
            self.oferta = random.uniform(0.5 * self.valoracion, 1.5 * self.valoracion)
def simular_subasta(tipo_info):
    valor_real = random.uniform(100, 1000)
    subasta = Subasta(5, valor_real)

    for postor in subasta.postores:
        if tipo_info == "perfecta":
            postor.valoracion = valor_real
        elif tipo_info == "imperfecta":
            postor.valoracion = random.uniform(0.8 * valor_real, 1.2 * valor_real)
        else:  # incompleta
            postor.valoracion = random.uniform(0.5 * valor_real, 1.5 * valor_real)

        postor.hacer_oferta(tipo_info)

    ganador = max(subasta.postores, key=lambda x: x.oferta)
    return subasta, ganador
def main():
    for tipo_info in ["perfecta", "imperfecta", "incompleta"]:
        print(f"\nSimulación de subasta con información {tipo_info}:")
        subasta, ganador = simular_subasta(tipo_info)
        print(f"Valor real del item: {subasta.valor_real:.2f}")
        print(f"Ganador: Postor {ganador.id}")
        print(f"Oferta ganadora: {ganador.oferta:.2f}")
        print("Todas las ofertas:")
        for postor in subasta.postores:
            print(f"  Postor {postor.id}: valoración = {postor.valoracion:.2f}, oferta = {postor.oferta:.2f}")

if __name__ == "__main__":
    main()