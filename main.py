import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline

# Gerar dados predefinidos para teste
np.random.seed(0)
num_dados = 120
temperaturas = list(np.random.uniform(25, 30, num_dados) + np.sin(np.linspace(0, 20, num_dados)) * 5)
ph_values = list(np.random.uniform(7.0, 8.0, num_dados) - np.cos(np.linspace(0, 20, num_dados)) * 0.5)

# Função para adicionar dados
def adicionar_dados(temperatura, ph):
    temperaturas.append(temperatura)
    ph_values.append(ph)
    print(f"Dados adicionados: Temperatura = {temperatura}, pH = {ph}")

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

    # Gráfico de pH
    axs[1].plot(x_smooth, ph_smooth, color='g', lw=2)
    axs[1].scatter(x, dados['pH'], color='g', s=10, zorder=5)
    axs[1].set_title('pH do Mar', fontsize=14, weight='bold')
    axs[1].set_xlabel('Medição', fontsize=12)
    axs[1].set_ylabel('pH', fontsize=12)
    axs[1].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout(pad=2.0)
    plt.show()

# Exemplo de uso
if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Adicionar dados")
        print("2. Mostrar dados e gráficos")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                temperatura = float(input("Insira a temperatura do mar (°C): "))
                ph = float(input("Insira o pH do mar: "))
                adicionar_dados(temperatura, ph)
            except ValueError:
                print("Entrada inválida. Por favor, insira números válidos.")
        elif opcao == "2":
            mostrar_dados()
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
