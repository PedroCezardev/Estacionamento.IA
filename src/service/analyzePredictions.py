import cv2
import predictionsImages as predictionsImages
import plotarVagas
import arduinoConective

# Função para analisar as predições e as vagas
def predictions_analyze():
    # Carregar e processar a imagem
    frame = cv2.imread("../../assets/inputs/imagemAtual2.jpeg")
    predictions = predictionsImages.predict_image(frame)
    frame_ploted = predictionsImages.plot_predictions(frame, predictions)
    coordinate_vagas = plotarVagas.coordinate_vagas()

    # Extrair as coordenadas dos carros detectados
    car_coordinates = []
    for result in predictions:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
            car_coordinates.append((x1, y1, x2 - x1, y2 - y1))

    # Atualizar a imagem com as vagas e carros detectados
    frame_with_vagas = plotarVagas.plot_vagas(frame_ploted, coordinate_vagas, car_coordinates)
     # Enviar os valores das vagas para o Arduino
    arduinoConective.toSendValuesVaga(coordinate_vagas, car_coordinates)

    # Exibir a imagem com as predições e as vagas
    cv2.imshow("Previsoes com Estacionamento com Vagas", frame_with_vagas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     predictions_analyze()