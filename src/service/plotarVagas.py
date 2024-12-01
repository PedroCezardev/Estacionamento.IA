import cv2
import numpy as np

# Função para desenhar as vagas na imagem
def plot_vagas(img_array, coordinate_vagas, car_coordinates):
    for space in coordinate_vagas:
        vaga_name = space[0]
        space_rect = space[1:]

        # Verifica se algum carro está dentro da vaga
        is_occupied = any(is_car_in_parking_space(car_rect, space_rect) for car_rect in car_coordinates)

        # Define a cor do retângulo: vermelho se ocupado, verde se livre
        color = (0, 0, 255) if is_occupied else (0, 255, 0)

        (x, y, w, h) = space_rect
        cv2.rectangle(img_array, (x, y), (x + w, y + h), color, 2)
        
        # Coloca o nome da vaga acima do retângulo
        cv2.putText(img_array, vaga_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return img_array

# Função para verificar se um retângulo A está 40% dentro de um retângulo B
def is_car_in_parking_space(car_rect, space_rect):
    (xA, yA, wA, hA) = car_rect
    (xB, yB, wB, hB) = space_rect

    # Calcula as coordenadas da interseção
    x_inter_left = max(xA, xB)
    y_inter_top = max(yA, yB)
    x_inter_right = min(xA + wA, xB + wB)
    y_inter_bottom = min(yA + hA, yB + hB)

    # Calcula a área da interseção
    if x_inter_right < x_inter_left or y_inter_bottom < y_inter_top:
        inter_area = 0
    else:
        inter_area = (x_inter_right - x_inter_left) * (y_inter_bottom - y_inter_top)

    # Calcula a área do retângulo do carro
    car_area = wA * hA

    # Verifica se a área da interseção é pelo menos 40% da área do retângulo do carro
    return inter_area >= 0.4 * car_area

def coordinate_vagas():
    vagasCoordinates = [
        ("vaga1", 119, 907, 332, 491),
        ("vaga2", 461, 907, 341, 475),
        ("vaga5", 806, 907, 311, 470),
        ("vaga3", 1136, 142, 300, 448),
        ("vaga4", 806, 140, 316, 448)
    ]
    return vagasCoordinates
