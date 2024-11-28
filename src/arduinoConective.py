import serial
import time
from plotarVagas import is_car_in_parking_space

def toSendValuesVaga(coordinate_vagas, car_coordinates):
    # Configuração da porta serial
    arduino = serial.Serial('COM9', 9600, timeout=1)  # Substitua 'COM3' pela porta correta do seu Arduino
    time.sleep(2)  # Tempo para estabilizar a conexão serial

    for i, space_rect in enumerate(coordinate_vagas):
        vaga_ocupada = False
        for car_rect in car_coordinates:
            if is_car_in_parking_space(car_rect, space_rect):
                vaga_ocupada = True
                break
        if vaga_ocupada:
            valor_para_enviar = i + 1  # Se a vaga está ocupada, enviar o número da vaga (1, 2, 3, 4, etc.)
            arduino.write(f'{valor_para_enviar}\n'.encode())
            print(f'Enviando {valor_para_enviar} para o Arduino (vaga ocupada)')
        else:
            print(f'Vaga {i + 1} está livre')

    arduino.close()
