import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO

class AppLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Atalhos Faceis")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Configurar o estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        
        # Criar o frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Selecione um aplicativo para abrir no navegador",
            font=('Arial', 12, 'bold')
        )
        self.title_label.pack(pady=(0, 20))
        
        # Frame para os ícones
        self.icons_frame = ttk.Frame(self.main_frame)
        self.icons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de aplicativos
        self.apps = [
            {"name": "Google", "url": "https://www.google.com", "icon_url": "https://www.google.com/favicon.ico"},
            {"name": "YouTube", "url": "https://www.youtube.com", "icon_url": "https://www.youtube.com/favicon.ico"},
            {"name": "WhatsApp", "url": "https://web.whatsapp.com", "icon_url": "https://web.whatsapp.com/favicon.ico"},
            {"name": "Facebook", "url": "https://www.facebook.com", "icon_url": "https://www.facebook.com/favicon.ico"},
            {"name": "Twitter", "url": "https://twitter.com", "icon_url": "https://twitter.com/favicon.ico"},
            {"name": "Gmail", "url": "https://mail.google.com", "icon_url": "https://mail.google.com/favicon.ico"}
        ]
        
        # Carregar e exibir os ícones
        self.load_icons()
        
    def load_icons(self):
        """Carrega e exibe os ícones dos aplicativos"""
        for i, app in enumerate(self.apps):
            try:
                # Baixar a imagem do ícone
                response = requests.get(app["icon_url"], timeout=5)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((64, 64), Image.Resampling.LANCZOS)
                
                # Converter para formato Tkinter
                tk_img = ImageTk.PhotoImage(img)
                
                # Criar um frame para cada ícone
                icon_frame = ttk.Frame(self.icons_frame)
                icon_frame.grid(row=i//3, column=i%3, padx=20, pady=20)
                
                # Criar o botão com a imagem
                btn = tk.Button(
                    icon_frame, 
                    image=tk_img, 
                    command=lambda url=app["url"]: webbrowser.open(url),
                    borderwidth=0,
                    relief=tk.FLAT
                )
                btn.image = tk_img  # Manter referência para evitar garbage collection
                btn.pack()
                
                # Adicionar label com o nome do app
                label = ttk.Label(icon_frame, text=app["name"])
                label.pack()
                
            except Exception as e:
                print(f"Erro ao carregar ícone para {app['name']}: {e}")
                # Usar um placeholder se o ícone não carregar
                self.create_text_icon(app["name"], app["url"], i)
    
    def create_text_icon(self, name, url, index):
        """Cria um botão de texto quando o ícone não está disponível"""
        icon_frame = ttk.Frame(self.icons_frame)
        icon_frame.grid(row=index//3, column=index%3, padx=20, pady=20)
        
        btn = tk.Button(
            icon_frame, 
            text=name,
            command=lambda: webbrowser.open(url),
            width=10,
            height=3,
            bg='#e0e0e0',
            fg='black',
            relief=tk.RAISED
        )
        btn.pack()
        
        label = ttk.Label(icon_frame, text=name)
        label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLauncher(root)
    root.mainloop()