import serial
import time
import random

# Configurar a porta serial (ajuste o nome da porta conforme necessário)
ser = serial.Serial('COM5', 9600, timeout=1)  # Substitua 'COM3' pelo nome da sua porta serial

def generate_random_values():
    # Gerar valores aleatórios para temperatura e pH
    temperature = round(random.uniform(10.0, 30.0), 2)  # Temperatura entre 10.0 e 30.0 graus Celsius
    ph = round(random.uniform(7.5, 8.5), 2)  # pH entre 7.5 e 8.5
    return temperature, ph

try:
    while True:
        # Gerar valores aleatórios
        temp, ph = generate_random_values()
        # Criar string no formato "temp,ph"
        data_to_send = f"{temp},{ph}\n"
        # Enviar dados pela porta serial
        ser.write(data_to_send.encode())
        print(f"Sent: {data_to_send.strip()}")
        # Aguardar 1 segundo
        time.sleep(1)

except KeyboardInterrupt:
    # Fechar a porta serial ao interromper o programa
    ser.close()
    print("\nSerial port closed.")
