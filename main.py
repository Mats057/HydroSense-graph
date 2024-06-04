import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import tkinter as tk
import serial
import msvcrt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from colorama import init, Fore, Style
import time
import random

# Inicializar o colorama
init(autoreset=True)

# Definindo listas para armazenar os dados
temperaturas = []
ph_values = []
min_temp = 10.0
max_temp = 30.0
min_ph = 7.5
max_ph = 8.5

# Valores iniciais de temperatura e pH para o simulador
current_temperature = 20.0
current_ph = 8.0

# Função para adicionar dados
def adicionar_dados(temperatura, ph):
    temperaturas.append(temperatura)
    ph_values.append(ph)

# Função para gerar valores realistas
def generate_realistic_values(current_temp, current_ph):
    temperature_variation = random.uniform(-0.05, 0.05)
    new_temperature = current_temp + temperature_variation
    new_temperature = max(10.0, min(30.0, new_temperature))

    ph_variation = random.uniform(-0.01, 0.01)
    new_ph = current_ph + ph_variation
    new_ph = max(7.5, min(8.5, new_ph))

    return new_temperature, new_ph

# Função para coletar dados da porta serial
def coletar_dados(use_simulator=False):
    print(Fore.CYAN + "Dados de Telemetria do Arduino (Digite 'q' para sair):\n")

    if use_simulator:
        global current_temperature, current_ph
        while True:
            try:
                current_temperature, current_ph = generate_realistic_values(current_temperature, current_ph)
                data = f"{current_temperature:.2f},{current_ph:.2f}"
                temperatura, ph = map(float, data.split(','))
                if temperatura < min_temp or temperatura > max_temp or ph < min_ph or ph > max_ph:
                    print(Fore.RED + f"AVISO! DADOS FORA DO LIMITE!!!, Temperatura: {temperatura} °C, pH: {ph}")
                else:
                    print(Fore.GREEN + f"Temperatura: {temperatura} °C, pH: {ph}, Dados dentro do aceitável.")
                adicionar_dados(temperatura, ph)
                time.sleep(1)
            except ValueError:
                print(Fore.RED + "Erro ao gerar dados simulados.")
                break
            if msvcrt.kbhit():
                user_input = msvcrt.getch().decode('utf-8')
                if user_input == 'q' or user_input == 'Q':
                    break
    else:
        ser = configurar_porta_serial()
        if ser is None:
            return

        while True:
            try:
                data = ser.readline().decode('utf-8').strip()
                temperatura, ph = map(float, data.split(','))
                if temperatura < min_temp or temperatura > max_temp or ph < min_ph or ph > max_ph:
                    print(Fore.RED + f"AVISO! DADOS FORA DO LIMITE!!!, Temperatura: {temperatura} °C, pH: {ph}")
                else:
                    print(Fore.GREEN + f"Temperatura: {temperatura} °C, pH: {ph}, Dados dentro do aceitável.")
                adicionar_dados(temperatura, ph)
            except ValueError:
                print(Fore.RED + "Erro ao ler dados da porta serial.")
                break
            if msvcrt.kbhit():
                user_input = msvcrt.getch().decode('utf-8')
                if user_input == 'q' or user_input == 'Q':
                    break

        ser.close()

# Função para suavizar linhas
def suavizar_linha(x, y, num_points=1000):
    x_new = np.linspace(min(x), max(x), num_points)
    spl = make_interp_spline(x, y, k=2)
    y_smooth = spl(x_new)
    return x_new, y_smooth

# Função para mostrar os dados e gráficos
def mostrar_dados():
    if len(temperaturas) == 0 or len(ph_values) == 0:
        print(Fore.YELLOW + "Nenhum dado disponível.")
        return

    dados = pd.DataFrame({
        'Temperatura': temperaturas,
        'pH': ph_values
    })

    print(Fore.CYAN + "Dados coletados:")
    print(dados)

    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('Análise de Dados do Mar', fontsize=16, weight='bold')
    fig.patch.set_facecolor('#f0f0f0')

    x = np.arange(len(dados))
    x_smooth, temp_smooth = suavizar_linha(x, dados['Temperatura'])
    _, ph_smooth = suavizar_linha(x, dados['pH'])

    # Gráfico de Temperaturas
    axs[0].plot(x_smooth, temp_smooth, color='b', lw=2)
    axs[0].scatter(x, dados['Temperatura'], color='b', s=10, zorder=5)
    axs[0].set_title('Temperaturas do Mar', fontsize=14, weight='bold')
    axs[0].set_ylabel('Temperatura (°C)', fontsize=12)
    axs[0].grid(True, linestyle='--', alpha=0.7)
    axs[0].set_facecolor('#eafff5')
    axs[0].axhline(min_temp, color='r', linestyle='--', lw=1, label='Mín Temp')
    axs[0].axhline(max_temp, color='r', linestyle='--', lw=1, label='Máx Temp')
    axs[0].legend()

    # Gráfico de pH
    axs[1].plot(x_smooth, ph_smooth, color='g', lw=2)
    axs[1].scatter(x, dados['pH'], color='g', s=10, zorder=5)
    axs[1].set_title('pH do Mar', fontsize=14, weight='bold')
    axs[1].set_xlabel('Medição', fontsize=12)
    axs[1].set_ylabel('pH', fontsize=12)
    axs[1].grid(True, linestyle='--', alpha=0.7)
    axs[1].set_facecolor('#fff4e6')
    axs[1].axhline(min_ph, color='r', linestyle='--', lw=1, label='Mín pH')
    axs[1].axhline(max_ph, color='r', linestyle='--', lw=1, label='Máx pH')
    axs[1].legend()

    plt.tight_layout(pad=2.0)
    plt.subplots_adjust(top=0.9)

    root = tk.Tk()
    root.wm_title("Gráficos de Análise do Mar")
    root.configure(bg='#f0f0f0')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

# Função para configurar valores mínimos e máximos de temperatura e pH
def configurar_min_max():
    global min_temp, max_temp, min_ph, max_ph
    try:
        min_temp = float(input(Fore.CYAN + "Digite o valor mínimo de temperatura (°C): "))
        max_temp = float(input(Fore.CYAN + "Digite o valor máximo de temperatura (°C): "))
        min_ph = float(input(Fore.CYAN + "Digite o valor mínimo de pH: "))
        max_ph = float(input(Fore.CYAN + "Digite o valor máximo de pH: "))
        print(Fore.GREEN + "Valores mínimos e máximos configurados com sucesso.")
    except ValueError:
        print(Fore.RED + "Digite um valor numérico válido.")

# Função para configurar a porta serial
def configurar_porta_serial():
    porta_default = "COM5"
    baud_rate_default = 9600

    porta = input(Fore.CYAN + f"Digite o nome da porta serial (padrão: {porta_default}): ") or porta_default
    baud_rate = input(Fore.CYAN + f"Digite a taxa de transmissão (baud rate) (padrão: {baud_rate_default}): ") or baud_rate_default

    if not str(baud_rate).isdigit() or int(baud_rate) <= 0:
        print(Fore.RED + "Digite um valor válido para a taxa de transmissão.")
        return None

    baud_rate = int(baud_rate)
    return serial.Serial(porta, baud_rate, timeout=1)

# Função principal
if __name__ == "__main__":
    while True:
        print(Fore.CYAN + "\nMenu:")
        print(Fore.CYAN + "1. Adicionar dados (Real)")
        print(Fore.CYAN + "2. Adicionar dados (Simulador)")
        print(Fore.CYAN + "3. Mostrar dados e gráficos")
        print(Fore.CYAN + "4. Configurar valores mínimos e máximos de temperatura e pH")
        print(Fore.CYAN + "5. Limpar dados")
        print(Fore.CYAN + "6. Sair")
        opcao = input(Fore.YELLOW + "Escolha uma opção: ")

        if opcao == "1":
            coletar_dados(use_simulator=False)
        elif opcao == "2":
            coletar_dados(use_simulator=True)
        elif opcao == "3":
            mostrar_dados()
        elif opcao == "4":
            configurar_min_max()
        elif opcao == "5":
            temperaturas.clear()
            ph_values.clear()
            print(Fore.GREEN + "Dados limpos.")
        elif opcao == "6":
            break
        else:
            print(Fore.RED + "Opção inválida. Por favor, escolha uma opção válida.")
