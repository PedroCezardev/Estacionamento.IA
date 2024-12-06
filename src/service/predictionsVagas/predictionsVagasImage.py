import cv2
import numpy as np

def img_view(img, title_view):
    cv2.imshow(title_view, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_rectangles_by_q_lines(q_lines):
    rectangles = []
    for i in range(0, len(q_lines) - 1):
        x_min = min(q_lines[i][0], q_lines[i][2])
        x_max = max(q_lines[i+1][0], q_lines[i+1][2])
        y_min = min(q_lines[i][1], q_lines[i+1][1])
        y_max = max(q_lines[i][3], q_lines[i+1][3])
        rectangles.append(((x_min, y_min), (x_max, y_max)))
    return rectangles

def plot_all_q_rectangles(image, rectangles_q1, rectangles_q2):
    # Desenhar os retângulos
    for rect in rectangles_q1:
        cv2.rectangle(image, rect[0], rect[1], (0, 0, 255), 2)
    for rect in rectangles_q2:
        cv2.rectangle(image, rect[0], rect[1], (0, 0, 255), 2)
    return image

def get_q_lines(image, vertical_lines):
    q1_lines = []
    q2_lines = []
    if vertical_lines is not None:
        for line in vertical_lines:
            x1, y1, x2, y2 = line
            if y2 < image.shape[0] // 2 and y1 < image.shape[0] // 2:
                q1_lines.append(line)
            else:
                q2_lines.append(line)
    return q1_lines, q2_lines

def separate_lines(lines):
    # Separar linhas horizontais e verticais
    horizontal_lines = []
    vertical_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi  # Ângulo em graus
            if -10 <= angle <= 10:  # Linhas horizontais
                horizontal_lines.append((x1, y1, x2, y2))
            elif 80 <= abs(angle) <= 100:  # Linhas verticais
                vertical_lines.append((x1, y1, x2, y2))
    return horizontal_lines, vertical_lines

def detect_parking_spaces(image_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    image = cv2.resize(image, (512, 512))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Suavizar a imagem
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)
    img_view(blurred, "Suavizada")

    _, binary = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

    # Detectar bordas
    edges = cv2.Canny(binary, 50, 150)
    img_view(edges, "Bordas")

    # Detectar linhas usando a Transformada de Hough
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=80)

    _, vertical_lines = separate_lines(lines)

    q1_lines, q2_lines = get_q_lines(image, vertical_lines)
    q1_lines = sorted(q1_lines, key=lambda x: x[0])
    q2_lines = sorted(q2_lines, key=lambda x: x[0])

    rectangles_q1 = get_rectangles_by_q_lines(q1_lines)
    rectangles_q2 = get_rectangles_by_q_lines(q2_lines)

    image = plot_all_q_rectangles(image, rectangles_q1, rectangles_q2)

    img_view(image, "Saida")

# Caminho para a imagem de entrada
image_path = "../../../assets/inputs/imagemAtual1.jpeg"
detect_parking_spaces(image_path)
