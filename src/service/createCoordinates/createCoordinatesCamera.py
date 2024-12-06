import cv2

# Função para redimensionar a imagem para um tamanho fixo de largura de 700 pixels, mantendo a proporção
def resize_image(img_array, new_width=700):
    height, width, _ = img_array.shape
    new_height = int((new_width / width) * height)  # Calcula a nova altura mantendo a proporção
    resized_image = cv2.resize(img_array, (new_width, new_height))
    return resized_image, (width / new_width), (height / new_height)

# Inicia a captura da câmera (0 é o ID da câmera padrão)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao acessar a câmera.")
    exit()

# Lista para armazenar as coordenadas das vagas
vagas = []

print("Selecione os retângulos das vagas. Pressione Enter após selecionar cada retângulo. Pressione ESC para finalizar.")

# Define a janela como ajustável
cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)

while True:
    # Captura um frame da câmera
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o vídeo.")
        break

    # Redimensiona o frame para um tamanho fixo de largura de 700 pixels, mantendo a proporção
    resized_image, scale_x, scale_y = resize_image(frame, 700)

    # Permite ao usuário selecionar a ROI (Região de Interesse)
    roi = cv2.selectROI("Camera", resized_image, fromCenter=False, showCrosshair=True)

    # Se a ROI não foi selecionada, o usuário pressionou ESC para sair
    if roi == (0, 0, 0, 0):
        break
    
    x, y, w, h = roi
    vagas.append((int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)))  # Coordenadas originais

    # Desenha o retângulo na imagem para visualização imediata
    cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Exibe o frame com a seleção
    cv2.imshow("Camera", resized_image)

    # Verifica se o usuário pressionou a tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finaliza a captura da câmera
cap.release()
cv2.destroyAllWindows()

# Verifica se foram capturadas coordenadas
if len(vagas) > 0:
    # Imprime as coordenadas processadas
    for i, (x, y, w, h) in enumerate(vagas):
        print(f"Vaga {i + 1}: (x={x}, y={y}, w={w}, h={h})")
else:
    print("Nenhuma coordenada capturada.")
