from ultralytics import YOLO
import cv2
import plotarVagas
import arduinoConective

# Parâmetros globais
THRESHHOLD_DETECTION = 0.5
CLASS_NAME = "Carro"
MODEL_PATH = "../../assets/models/yolov8s.pt"
IMAGE_PATH = "../../assets/inputs/imagemAtual6.jpeg"
WIDTH_RESIZE = 700

# Carregando o modelo YOLO
def load_model():
    return YOLO(MODEL_PATH)

# Fazendo a predição dos carros
def predict_image(model, img_array):
    return model(img_array)

# Desenhando as predições dos carros na imagem
def plot_predictions(img_array, predictions):
    # Mapeia os IDs das classes para os nomes das classes personalizadas e desenha as caixas na imagem
    for result in predictions:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
            confidence = box.conf.item()

            if confidence > THRESHHOLD_DETECTION:
                cv2.rectangle(img_array, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img_array, f"{CLASS_NAME} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return img_array

# Redimensionando a imagem para um tamanho fixo de largura de 700 pixels, mantendo a proporção
def resize_image(img_array, new_width=WIDTH_RESIZE):
    height, width, _ = img_array.shape
    new_height = int((new_width / width) * height)
    resized_image = cv2.resize(img_array, (new_width, new_height))
    return resized_image

# Função principal para analisar as predições e as vagas
def predictions_analyze():
    # Carregar o modelo
    model = load_model()

    # Carregar e processar a imagem
    frame = cv2.imread(IMAGE_PATH)
    predictions = predict_image(model, frame)
    frame_ploted = plot_predictions(frame, predictions)
    
    # Obter coordenadas das vagas
    coordinate_vagas = plotarVagas.coordinate_vagas()

    # Extraido as coordenadas dos carros detectados
    car_coordinates = []
    for result in predictions:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy.tolist()[0])
            car_coordinates.append((x1, y1, x2 - x1, y2 - y1))

    # Atualizando a imagem com as vagas e carros detectados
    frame_with_vagas = plotarVagas.plot_vagas(frame_ploted, coordinate_vagas, car_coordinates)

    # Enviando as coordenadas das vagas para o Arduino
    arduinoConective.toSendValuesVaga(coordinate_vagas, car_coordinates)

    # Redimensionando a imagem para 700 pixels de largura
    frame_resized = resize_image(frame_with_vagas, WIDTH_RESIZE)

    # Exibindo a imagem com as predições e as vagas
    cv2.imshow("Previsoes com Estacionamento com Vagas", frame_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Executar a função principal
if __name__ == "__main__":
    predictions_analyze()

