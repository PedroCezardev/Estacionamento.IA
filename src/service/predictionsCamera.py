from ultralytics import YOLO
import cv2
import plotarVagas
import arduinoConective

# Parâmetros globais
THRESHHOLD_DETECTION = 0.5
CLASS_NAME = "Carro"
MODEL_PATH = "../../assets/models/yolov8s.pt"
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
def predictions_analyze_camera():
    # Carregar o modelo
    model = load_model()

    # Inicializar a captura da câmera (apenas uma vez no início)
    camera = cv2.VideoCapture(2)
    
    # Verificar se a câmera foi aberta corretamente
    if not camera.isOpened():
        print("Erro ao abrir a câmera!")
        return

    # Forçar resolução e FPS para evitar problemas
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    camera.set(cv2.CAP_PROP_FPS, 30)
    
    is_running = True

    while is_running:
        # Capturar frame da câmera
        status, frame = camera.read()

        # Verificar se o frame foi capturado corretamente
        if not status:
            print("Erro ao capturar o frame!")
            break  # Se a captura falhar, sai do loop

        # Verifique o tamanho do frame para depuração
        print(f"Frame capturado com tamanho: {frame.shape}")

        # Fazer a predição
        predictions = predict_image(model, frame)

        # Desenhar as predições na imagem
        frame_ploted = plot_predictions(frame, predictions)
        
        # Obter coordenadas das vagas
        coordinate_vagas = plotarVagas.coordinate_vagas()

        # Extraído as coordenadas dos carros detectados
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

        # Condição de parada
        if cv2.waitKey(1) & 0xff == ord('q'):
            is_running = False

    # Libera a câmera e fecha todas as janelas
    camera.release()
    cv2.destroyAllWindows()

# Executar a função principal
if __name__ == "__main__":
    predictions_analyze_camera()
