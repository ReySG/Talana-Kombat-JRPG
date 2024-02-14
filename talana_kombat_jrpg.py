import json
from itertools import zip_longest

GOLPES = {
    
}

class Personaje:
    def __init__(self, nombre, energia):
        self.nombre = nombre
        self.energia = energia
        self.golpes_personaje = []

    def agregar_movimiento(self, combinacion, energia, nombre):
        golpe = {
            'nombre': nombre,
            'combinacion': combinacion,
            'energia': energia,
        }
        self.golpes_personaje.append(golpe)
        

    def calcular_danio(self, movimiento='', golpe=''):
        if movimiento == None or golpe == None:
            return 0, f'- {self.nombre} no realiza ninguna accion\n'
        for ataque in self.golpes_personaje:
            movimiento_ataque = ataque['combinacion'].split('+')[0]
            golpe_ataque = ataque['combinacion'].split('+')[1]
            if movimiento and golpe == '':
                return 0, f'- {self.nombre} se mueve\n'
            if golpe == '':
                return 0, f'- El jugador {self.nombre} no realiza ningun golpe'
            if movimiento != '' and movimiento_ataque in movimiento and golpe == golpe_ataque:
                nombre_ataque = ataque['nombre']
                return ataque['energia'], f'- {self.nombre} realiza un {nombre_ataque}\n'
            elif golpe == 'P':
                return 1, f'- {self.nombre} lanza un puñetazo infligiendo 1 de daño\n'
            elif golpe == 'K':
                return 1, f'- {self.nombre} lanza una patada infligiendo 1 de daño\n'

        
def calcular_total_combinacion(player1, player2):
    total_combinacion_player1 = len(player1['movimientos'][0]) + len(player1['golpes'][0])
    total_combinacion_player2 = len(player2['movimientos'][0]) + len(player2['golpes'][0])
    return total_combinacion_player1 , total_combinacion_player2


def simular_combate(json_pelea):
    player1 = Personaje("Tonyn Stallone", 6)
    player2 = Personaje("Arnaldor Shuatseneguer", 6)
    
    player1.agregar_movimiento('DSD+P', 3, 'Taladoken')
    player1.agregar_movimiento('SD+K', 2, 'Remuyuken')
    
    player2.agregar_movimiento('SA+P', 3, 'Remuyuken')
    player2.agregar_movimiento('ASA+K', 2, 'Taladoken')
    
    json_player1 = json_pelea['player1']
    json_player2 = json_pelea['player2']
    
    total_combinacion_player1, total_combinacion_player2 = calcular_total_combinacion(json_player1, json_player2)
    primer_turno = 1
    texto = 'RESULTADOS:\n'
    
    # Determinar quién comienza primero
    if total_combinacion_player1 < total_combinacion_player2:
        texto += "+ El jugador 1 (Tonyn Stallone) comienza primero.\n"
    elif total_combinacion_player1 > total_combinacion_player2:
        primer_turno = 2
        texto += "- El jugador 2 (Arnaldor Shuatseneguer) comienza primero.\n"
    else:
        texto += "- Hay un empate en el total de las combinaciones. El jugador 1 (Tonyn Stallone) comienza primero por default.\n"

    for movimiento_player1, golpe_player1, movimiento_player2, golpe_player2 in zip_longest(
        json_player1["movimientos"], json_player1["golpes"],
        json_player2["movimientos"], json_player2["golpes"]):

        if primer_turno == 2:
            danio_player2, comentario2 = player2.calcular_danio(movimiento_player2, golpe_player2)
            danio_player1, comentario1 = player1.calcular_danio(movimiento_player1, golpe_player1)
            
            texto += comentario2
            texto += comentario1
            primer_turno = 0
        else:
            danio_player1, comentario1 = player1.calcular_danio(movimiento_player1, golpe_player1)
            danio_player2, comentario2 = player2.calcular_danio(movimiento_player2, golpe_player2)
            
            texto += comentario1
            texto += comentario2
            
        player1.energia -= danio_player2
        player2.energia -= danio_player1
        
        if player2.energia <= 0:
            texto += f"- {player2.nombre} logra dejar sin energia a su oponente y aún le queda {player2.energia} de energía\n"
            return texto
        elif player1.energia <= 0:
            texto +=  f"- {player1.nombre} logra dejar sin energia a su oponente y aún le queda {player1.energia} de energía\n"
            return texto

    if player1.energia == player2.energia:
        texto +=  f"- Empate de la pelea {max(player1.energia, 0)} - {player2.energia}\n"
        return texto
    elif player1.energia > player2.energia:
        ganador = player1
        perdedor = player2
    elif player2.energia > player1.energia:
        ganador = player2
        perdedor = player1
    texto +=  f"- Finaliza la pelea y el jugador {ganador.nombre} gana con {ganador.energia} de energía\n contra {perdedor.nombre} con {max(perdedor.energia, 0)}\n"
    return texto

def main():
    #JSONs de prueba
    json_pelea1 = '{"player1":{"movimientos":["D","DSD","S","DSD","SD"],"golpes":["K","P","","K","P"]},"player2":{"movimientos":["SA","SA","SA","ASA","SA"],"golpes":["K","","K","P","P"]}}'
    json_pelea2 = '{"player1": {"movimientos": ["SDD", "DSD", "SA", "DSD"],"golpes": ["K", "P", "K", "P"]},"player2": {"movimientos": ["DSD", "WSAW", "ASA", "", "ASA", "SA"],"golpes": ["P", "K", "K", "K", "P", "k"]}}'
    json_pelea3 = '{"player1": {"movimientos": ["DSD", "S"],"golpes": ["P", ""]},"player2": {"movimientos": ["", "ASA", "DA", "AAA", "", "SA"],"golpes": ["P", "", "P", "K", "K", "K"]}}'

    #Parsear el JSON
    json_pelea = json.loads(json_pelea3)

    #Simular el combate
    resultado = simular_combate(json_pelea)

    # # Imprimir el resultado
    print(resultado)

if __name__ == "__main__":
    main()
