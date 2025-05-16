from ultralytics import YOLO
import cv2

# Carregar o modelo YOLOv8 treinado para detectar fogo
model = YOLO("best.pt")

# Usar a mesma câmera usada anteriormente (0 = padrão)
cap = cv2.VideoCapture(0)

# Verificar se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a webcam")
    exit()

# Obter informações do vídeo (opcional)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30

# Configurar saída de vídeo (opcional)
out = cv2.VideoWriter("output_fogo.mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar frame da webcam")
        break

    # Fazer inferência com o modelo YOLOv8
    results = model(frame)

    # Desenhar caixas e rótulos no frame
    annotated_frame = results[0].plot()

    # Mostrar resultado na tela
    cv2.imshow("Detecção de Fogo - YOLOv8", annotated_frame)

    # Salvar o frame no vídeo (opcional)
    out.write(annotated_frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
out.release()
cv2.destroyAllWindows()
