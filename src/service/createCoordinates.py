import cv2

# Função para redimensionar a imagem para um tamanho fixo de largura de 700 pixels, mantendo a proporção
def resize_image(img_array, new_width=700):
    height, width, _ = img_array.shape
    new_height = int((new_width / width) * height)  # Calcula a nova altura mantendo a proporção
    resized_image = cv2.resize(img_array, (new_width, new_height))
    return resized_image, (width / new_width), (height / new_height)

# Carrega a imagem
image_path = '../../assets/inputs/imagemAtual1.jpeg'
image = cv2.imread(image_path)

# Verifica se a imagem foi carregada corretamente
if image is None:
    print("Erro ao carregar a imagem.")
    exit()

# Redimensiona a imagem para um tamanho fixo de largura de 700 pixels, mantendo a proporção
resized_image, scale_x, scale_y = resize_image(image, 700)

# Lista para armazenar as coordenadas das vagas
vagas = []

print("Selecione os retângulos das vagas. Pressione Enter após selecionar cada retângulo. Pressione Esc para finalizar.")

# Define a janela como ajustável
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

while True:
    # Permite ao usuário selecionar a ROI (Região de Interesse)
    roi = cv2.selectROI("Image", resized_image, fromCenter=False, showCrosshair=True)
        
    # Se a ROI não foi selecionada, o usuário pressionou ESC para sair
    if roi == (0, 0, 0, 0):
        break
    
    x, y, w, h = roi
    vagas.append((int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)))  # Coordenadas originais

    # Desenha o retângulo na imagem para visualização imediata
    cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    cv2.imshow('Image', resized_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# Verifica se foram capturadas coordenadas
if len(vagas) > 0:
    # Imprime as coordenadas processadas
    for i, (x, y, w, h) in enumerate(vagas):
        print(f"Vaga {i + 1}: (x={x}, y={y}, w={w}, h={h})")

    # Mostra a imagem com os retângulos das vagas desenhados
    for (x, y, w, h) in vagas:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('Vagas de Estacionamento', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Nenhuma coordenada capturada.")

# import cv2
# import numpy as np

# # Função para redimensionar a imagem para um tamanho fixo de largura de 700 pixels, mantendo a proporção
# def resize_image(img_array, new_width=700):
#     height, width, _ = img_array.shape
#     new_height = int((new_width / width) * height)  # Calcula a nova altura mantendo a proporção
#     resized_image = cv2.resize(img_array, (new_width, new_height))
#     return resized_image, (width / new_width), (height / new_height)

# # Carrega a imagem
# image_path = '../../assets/inputs/imagemAtual1.jpeg'
# image = cv2.imread(image_path)

# # Verifica se a imagem foi carregada corretamente
# if image is None:
#     print("Erro ao carregar a imagem.")
#     exit()

# # Redimensiona a imagem para um tamanho fixo de largura de 700 pixels, mantendo a proporção
# resized_image, scale_x, scale_y = resize_image(image, 700)

# # Converte para escala de cinza
# gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# # Aplica o filtro de Canny para detectar bordas
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# # Aplica a Transformada de Hough para detectar linhas
# lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

# # Lista para armazenar coordenadas dos retângulos
# vagas = []

# # Desenha as linhas detectadas na imagem original e tenta encontrar retângulos
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         cv2.line(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
#     # Detecta contornos na imagem de bordas
#     contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:  # Se o contorno tem 4 vértices, é um retângulo
#             x, y, w, h = cv2.boundingRect(approx)
#             vagas.append((int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)))  # Coordenadas originais
#             cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# # Exibe a imagem com os retângulos detectados
# cv2.imshow('Detected Parking Slots', resized_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Verifica se foram capturadas coordenadas
# if len(vagas) > 0:
#     # Imprime as coordenadas processadas
#     for i, (x, y, w, h) in enumerate(vagas):
#         print(f"Vaga {i + 1}: (x={x}, y={y}, w={w}, h={h})")

#     # Mostra a imagem com os retângulos das vagas desenhados
#     for (x, y, w, h) in vagas:
#         cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     cv2.imshow('Vagas de Estacionamento', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print("Nenhuma coordenada capturada.")
