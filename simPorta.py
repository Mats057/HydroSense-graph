import serial
import time
import random

# Configurar a porta serial (ajuste o nome da porta conforme necessário)
ser = serial.Serial('COM5', 9600, timeout=1)

# Valores iniciais de temperatura e pH
current_temperature = 20.0
current_ph = 8.0

def generate_realistic_values(current_temp, current_ph):
    # Gerar uma pequena variação aleatória para a temperatura
    temperature_variation = random.uniform(-0.05, 0.05)
    new_temperature = current_temp + temperature_variation
    new_temperature = max(10.0, min(30.0, new_temperature))  # Manter dentro do intervalo 10.0 a 30.0

    # Gerar uma pequena variação aleatória para o pH
    ph_variation = random.uniform(-0.01, 0.01)
    new_ph = current_ph + ph_variation
    new_ph = max(7.5, min(8.5, new_ph))  # Manter dentro do intervalo 7.5 a 8.5

    return new_temperature, new_ph

try:
    while True:
        # Gerar valores realistas
        current_temperature, current_ph = generate_realistic_values(current_temperature, current_ph)
        # Criar string no formato "temp,ph"
        data_to_send = f"{current_temperature:.2f},{current_ph:.2f}\n"
        # Enviar dados pela porta serial
        ser.write(data_to_send.encode())
        print(f"Sent: {data_to_send.strip()}")
        # Aguardar 1 segundo
        time.sleep(1)

except KeyboardInterrupt:
    # Fechar a porta serial ao interromper o programa
    ser.close()
    print("\nSerial port closed.")
