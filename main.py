import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import tkinter as tk
import serial
import msvcrt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Gerar dados predefinidos para teste
temperaturas = []
ph_values = []
min_temp = 20.0
max_temp = 30.0
min_ph = 7.5
max_ph = 8.5

# Função para adicionar dados
def adicionar_dados(temperatura, ph):
    temperaturas.append(temperatura)
    ph_values.append(ph)
    print(f"Dados adicionados: Temperatura = {temperatura}, pH = {ph}")

def coletar_dados():
    print("Dados de Telemetria do Arduino (Digite 'q' para sair):\n")
    # Inicializar comunicação serial
    ser = configurar_porta_serial()

    if ser is None:
        return

    # Ler dados da porta serial
    while True:
        try:
            data = ser.readline().decode('utf-8').strip()
            temperatura, ph = data.split(',')
            temperatura = float(temperatura)
            ph = float(ph)
            if temperatura == '' or ph == '':
                continue
            elif temperatura < min_temp or temperatura > max_temp or ph < min_ph or ph > max_ph:
                print("AVISO! OS DADOS ESTÃO FORA DO LIMITE ESPERADO.")
            adicionar_dados(float(temperatura), float(ph))
        except ValueError:
            print("Erro ao ler dados da porta serial.")
            break
        if msvcrt.kbhit():
            user_input = msvcrt.getch().decode('utf-8')
            if user_input == 'q' or user_input == 'Q':  # Digite 'q' para sair
                break

    # Fechar comunicação serial
    ser.close()

# Função para suavizar linhas
def suavizar_linha(x, y, num_points=1000):
    x_new = np.linspace(min(x), max(x), num_points)
    spl = make_interp_spline(x, y, k=2)  # Quadratic spline for less curvature
    y_smooth = spl(x_new)
    return x_new, y_smooth

# Função para mostrar os dados e gráficos
def mostrar_dados():
    if len(temperaturas) == 0 or len(ph_values) == 0:
        print("Nenhum dado disponível.")
        return

    # Criar DataFrame
    dados = pd.DataFrame({
        'Temperatura': temperaturas,
        'pH': ph_values
    })

    print("Dados coletados:")
    print(dados)

    # Plotar gráficos
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle('Análise de Dados do Mar', fontsize=16, weight='bold')  # Título da janela
    fig.patch.set_facecolor('#f0f0f0')  # Cor de fundo da janela

    # Suavizar dados
    x = np.arange(len(dados))
    x_smooth, temp_smooth = suavizar_linha(x, dados['Temperatura'])
    _, ph_smooth = suavizar_linha(x, dados['pH'])

    # Gráfico de Temperaturas
    axs[0].plot(x_smooth, temp_smooth, color='b', lw=2)
    axs[0].scatter(x, dados['Temperatura'], color='b', s=10, zorder=5)
    axs[0].set_title('Temperaturas do Mar', fontsize=14, weight='bold')
    axs[0].set_ylabel('Temperatura (°C)', fontsize=12)
    axs[0].grid(True, linestyle='--', alpha=0.7)
    axs[0].set_facecolor('#eafff5')  # Cor de fundo do gráfico de temperaturas

    # Gráfico de pH
    axs[1].plot(x_smooth, ph_smooth, color='g', lw=2)
    axs[1].scatter(x, dados['pH'], color='g', s=10, zorder=5)
    axs[1].set_title('pH do Mar', fontsize=14, weight='bold')
    axs[1].set_xlabel('Medição', fontsize=12)
    axs[1].set_ylabel('pH', fontsize=12)
    axs[1].grid(True, linestyle='--', alpha=0.7)
    axs[1].set_facecolor('#fff4e6')  # Cor de fundo do gráfico de pH

    plt.tight_layout(pad=2.0)
    plt.subplots_adjust(top=0.9)  # Ajuste para não sobrepor o título

    # Integrar com tkinter
    root = tk.Tk()
    root.wm_title("Gráficos de Análise do Mar")
    
    root.configure(bg='#f0f0f0')  # Cor de fundo da janela tkinter

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Função callback para quando a janela for fechada
    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def configurar_min_max():
    global min_temp, max_temp, min_ph, max_ph
    try:
        min_temp = float(input("Digite o valor mínimo de temperatura (°C): "))
        max_temp = float(input("Digite o valor máximo de temperatura (°C): "))
        min_ph = float(input("Digite o valor mínimo de pH: "))
        max_ph = float(input("Digite o valor máximo de pH: "))
        print("Valores mínimos e máximos configurados com sucesso.")
    except ValueError:
        print("Digite um valor numérico válido.")

def configurar_porta_serial():
    porta = input("Digite o nome da porta serial (ex.: COM4): ")
    baud_rate = input("Digite a taxa de transmissão (baud rate): ")
    if(not baud_rate.isdigit() or int(baud_rate) <= 0):
        print("Digite um valor válido para a taxa de transmissão.")
        return None
    baud_rate = int(baud_rate)
    return serial.Serial(porta, baud_rate, timeout=1)

# Exemplo de uso
if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Adicionar dados")
        print("2. Mostrar dados e gráficos")
        print("3. Configurar valores mínimos e máximos de temperatura e pH")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            coletar_dados()
        elif opcao == "2":
            mostrar_dados()
        elif opcao == "3":
            configurar_min_max()
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
