import tkinter as tk
from PIL import Image, ImageTk
import os

def criar_janela_com_icone():
    root = tk.Tk()
    root.wm_title("Teste de Ícone do Tkinter")

    # Caminho absoluto para o arquivo de ícone
    icon_path = os.path.abspath('simple_icon.png')
    
    if os.path.isfile(icon_path):
        try:
            img = Image.open(icon_path)
            photo = ImageTk.PhotoImage(img)
            root.iconphoto(False, photo)
            print("Ícone definido com sucesso.")
        except Exception as e:
            print(f"Erro ao definir o ícone: {e}")
    else:
        print(f"Arquivo de ícone não encontrado: {icon_path}")
    
    root.geometry("200x100")
    root.mainloop()

if __name__ == "__main__":
    criar_janela_com_icone()
