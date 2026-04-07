import cv2
import mediapipe as mp
import numpy as np
import base64

class VisionService:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )

    def analyze_frame(self, base64_image: str):
        """
        Recebe uma imagem em base64, processa via MediaPipe e retorna métricas de atenção e emoção.
        """
        try:
            # 1. Decodificar Base64 para OpenCV
            encoded_data = base64_image.split(',')[1] if ',' in base64_image else base64_image
            nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return None

            # 2. Processar Face Mesh
            results = self.face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            if not results.multi_face_landmarks:
                return {
                    "attention_score": 0.0,
                    "emotion": "Não Detectado"
                }

            face_landmarks = results.multi_face_landmarks[0]
            
            # --- MÉTRICA DE ATENÇÃO (Head Pose simplificado) ---
            # Usando landmarks fixos para estimar inclinação
            # Nariz: 1, Olho Esquerdo: 33, Olho Direito: 263
            nose = face_landmarks.landmark[1]
            eye_left = face_landmarks.landmark[33]
            eye_right = face_landmarks.landmark[263]
            
            # Se o nariz estiver centralizado horizontalmente entre os olhos, atenção é alta
            eye_dist = abs(eye_right.x - eye_left.x)
            nose_offset = abs(nose.x - (eye_left.x + eye_right.x)/2)
            
            # Normalização (quanto menor o offset, maior a atenção)
            attention = max(0.0, 1.0 - (nose_offset / (eye_dist + 1e-6)) * 2)

            # --- MÉTRICA DE EMOÇÃO (Heurísticas Landmarks) ---
            # Boca (Canto esquerdo: 61, Canto direito: 291, Topo: 13, Base: 14)
            mouth_left = face_landmarks.landmark[61]
            mouth_right = face_landmarks.landmark[291]
            mouth_top = face_landmarks.landmark[13]
            mouth_bottom = face_landmarks.landmark[14]
            
            # Distância vertical da boca (abertura)
            mouth_width = abs(mouth_right.x - mouth_left.x)
            mouth_height = abs(mouth_bottom.y - mouth_top.y)
            
            aspect_ratio = mouth_height / (mouth_width + 1e-6)
            
            if aspect_ratio > 0.4:
                emotion = "Surpresa/Frustração"
            elif mouth_right.y < mouth_left.y - 0.01 or mouth_left.y < mouth_right.y - 0.01:
                # Simetria de sorriso (simplificado)
                emotion = "Alegria"
            else:
                emotion = "Atenção"

            return {
                "attention_score": round(attention, 2),
                "emotion": emotion
            }

        except Exception as e:
            print(f"Erro no processamento visual: {e}")
            return None

# Singleton
vision_analyzer = VisionService()
