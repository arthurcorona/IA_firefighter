from ultralytics import YOLO
import cv2

# Carregar o modelo YOLOv8 pré-treinado
model = YOLO("modelofuncionando.pt")

# Abrir a webcam (0 = webcam padrão)
cap = cv2.VideoCapture(0)

# Verificar se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a webcam")
    exit()

# Obter informações do vídeo
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Default para 30 se não detectar corretamente

# Definir tamanho do bloco 
cm_per_pixel = 10   # Exemplo: 1cm = 10px
block_size = cm_per_pixel * 10  # 10cm = 100px


out = cv2.VideoWriter("output_webcam_detections.mp4", cv2.VideoWriter_fourcc(*"XVID"), fps, (frame_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar frame da webcam")
        break

    # Fazer a inferência no frame
    results = model(frame)

    # Processar os resultados do YOLO
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Coordenadas da detecção

            # Desenhar a grade SOMENTE dentro da área do objeto detectado
            for x in range(x1, x2, block_size):
                for y in range(y1, y2, block_size):
                    cv2.rectangle(frame, (x, y), (x + block_size, y + block_size), (200, 200, 200), 1)

                    # Exibir coordenadas de cada bloco
                    text = f"({x},{y})"
                    cv2.putText(frame, text, (x + 2, y + 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

            # Exibir nome do objeto como "maquete"
            label = "maquete"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # Desenhar a detecção
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Mostrar o frame
    cv2.imshow("YOLOv8 - Webcam", frame)

    # Gravar o frame com detecções (opcional)
    out.write(frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar os recursos
cap.release()
out.release()
cv2.destroyAllWindows()