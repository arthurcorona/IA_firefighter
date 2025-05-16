from ultralytics import YOLO
import cv2
import requests
import time

# URL do ESP8266 (ajuste conforme IP real do seu ESP)
ESP8266_URL = "http://192.168.4.1/coordenada"

# Carrega o modelo de detecção de fogo
model_fogo = YOLO("best.pt")

# Inicializa a webcam com resolução reduzida para melhorar desempenho
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

if not cap.isOpened():
    print("Erro ao abrir a webcam")
    exit()

print("Webcam iniciada... Pressione 'q' para sair")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Falha ao capturar frame da webcam")
        break

    # Cronômetro para medir tempo de inferência
    start_time = time.time()
    results = model_fogo(frame, verbose=False)
    infer_time = time.time() - start_time
    print(f"Inferência: {infer_time:.2f}s")

    # Desenhar resultados no frame
    annotated_frame = results[0].plot()

    # Extrai a posição do fogo (primeira detecção, se houver)
    if results[0].boxes:
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Desenha o centro no frame
            cv2.circle(annotated_frame, (cx, cy), 5, (0, 0, 255), -1)

            # Envia coordenadas para ESP8266 (com timeout curto)
            try:
                response = requests.post(ESP8266_URL, json={"x": cx, "y": cy}, timeout=0.2)
                print(f"Enviado para ESP8266: x={cx}, y={cy}, status={response.status_code}")
            except requests.exceptions.RequestException:
                print("⚠️ Erro ao enviar para ESP8266 (fora do ar?)")

            break  # Apenas o primeiro fogo detectado

    # Mostra a imagem com anotações
    cv2.imshow("Detecção de Fogo - YOLOv8", annotated_frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberação dos recursos
cap.release()
cv2.destroyAllWindows()
print("Encerrado com sucesso.")
