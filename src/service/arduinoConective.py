import serial
import time
from plotarVagas import is_car_in_parking_space

def toSendValuesVaga(coordinate_vagas, car_coordinates):
    
    import serial

def toSendValuesVaga(coordinate_vagas, car_coordinates):
    try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        # Enviar os dados para o Arduino
        for vaga, carro in zip(coordinate_vagas, car_coordinates):
            arduino.write(f"{vaga},{carro}\n".encode())
        arduino.close()
    except serial.SerialException as e:
        print(f"Erro de conexão com o Arduino: {e}")
        print("Arduino não conectado. Continuando com o código...")



    
    # Configuração da porta serial
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Substitua 'COM9' pela porta correta do seu Arduino
    time.sleep(2)  # Tempo para estabilizar a conexão serial

    for i, space in enumerate(coordinate_vagas):
        vaga_id = space[0]
        space_rect = space[1:]
        vaga_ocupada = False
        for car_rect in car_coordinates:
            if is_car_in_parking_space(car_rect, space_rect):
                vaga_ocupada = True
                break
        if vaga_ocupada:
            valor_para_enviar = i + 1  # Se a vaga está ocupada, enviar o número da vaga (1, 2, 3, 4, etc.)
            print(f'Enviando {valor_para_enviar} para o Arduino (vaga {vaga_id} ocupada)')
            arduino.write(f'{valor_para_enviar}\n'.encode())
        else:
            valor_para_enviar = -(i + 1)  # Se a vaga está livre, enviar o número negativo da vaga
            print(f'Enviando {valor_para_enviar} para o Arduino (vaga {vaga_id} livre)')
            arduino.write(f'{valor_para_enviar}\n'.encode())

    arduino.close()
