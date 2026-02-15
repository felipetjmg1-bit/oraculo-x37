"""
Módulo Hardware Bridge - Oráculo X-37
Simula a interface entre o modelo de IA e componentes de hardware físicos (Sensores/Atuadores).
"""

import time
import random
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configuração de Logs para auditoria de hardware
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [HARDWARE_BRIDGE] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hardware_audit.log"),
        logging.StreamHandler()
    ]
)

class HardwareInterface:
    """Simula a interface física de hardware."""
    
    def __init__(self):
        self.connected = True
        self.sensors = ["temp_sensor_01", "vibration_sensor_01", "pressure_sensor_01"]
        logging.info("Interface de hardware inicializada e sensores conectados.")

    def read_sensor_data(self) -> Dict[str, float]:
        """Simula a leitura de sensores industriais."""
        if not self.connected:
            raise ConnectionError("Hardware desconectado.")
            
        # Simula dados de 10 sensores (conforme o modelo espera 10 features)
        return {f"sensor_{i}": random.uniform(-2.0, 2.0) for i in range(10)}

    def trigger_actuator(self, action: str, intensity: float):
        """Simula a ativação de um atuador físico baseado na decisão da IA."""
        logging.info(f"ATUADOR ACIONADO: Ação={action} | Intensidade={intensity:.2f}")
        return True

class OracleHardwareIntegrator:
    """Integra o Oráculo X-37 com a Interface de Hardware."""
    
    def __init__(self, oracle_instance):
        self.oracle = oracle_instance
        self.hw = HardwareInterface()
        self.running = False

    def start_monitoring(self, interval: float = 2.0, duration: int = 10):
        """Inicia o monitoramento em tempo real com tomada de decisão por IA."""
        if not self.oracle.is_trained:
            logging.error("O Oráculo precisa estar treinado para monitorar hardware.")
            return

        logging.info("Iniciando monitoramento de hardware em tempo real...")
        self.running = True
        start_time = time.time()
        
        try:
            while self.running and (time.time() - start_time < duration):
                # 1. Leitura do Hardware
                data = self.hw.read_sensor_data()
                X_input = [list(data.values())]
                
                # 2. Processamento pela IA
                prediction = self.oracle.predict(X_input)[0]
                explanation = self.oracle.explain_prediction(X_input, sample_idx=0)
                
                # 3. Ação Baseada na IA
                status = "ALERTA" if prediction == 1 else "NORMAL"
                confidence = explanation.get('confidence', 1.0)
                
                logging.info(f"Status: {status} | Confiança: {confidence:.2%}")
                
                if status == "ALERTA":
                    # Se a IA detectar anomalia, aciona o hardware de segurança
                    self.hw.trigger_actuator("EMERGENCY_SHUTDOWN", confidence)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logging.info("Monitoramento interrompido pelo usuário.")
        finally:
            self.running = False
            logging.info("Monitoramento encerrado.")

if __name__ == "__main__":
    from oracle_model import OracleX37, generate_sample_data
    
    # Setup rápido para demonstração
    print("Preparando Oráculo para integração com hardware...")
    oracle = OracleX37(model_type="classification")
    X, y = generate_sample_data(n_samples=500, n_features=10)
    oracle.train(X, y)
    
    integrator = OracleHardwareIntegrator(oracle)
    integrator.start_monitoring(interval=1.0, duration=5)
