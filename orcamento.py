import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class SistemaOrcamento:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Orçamento")
        
        self.dados = []
        
        # Criando a interface
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(self.frame, text="Descrição:").grid(row=0, column=0, sticky=tk.W)
        self.descricao = ttk.Entry(self.frame, width=30)
        self.descricao.grid(row=0, column=1)
        
        ttk.Label(self.frame, text="Quantidade:").grid(row=1, column=0, sticky=tk.W)
        self.quantidade = ttk.Entry(self.frame, width=10)
        self.quantidade.grid(row=1, column=1)
        
        ttk.Label(self.frame, text="Preço Unitário:").grid(row=2, column=0, sticky=tk.W)
        self.preco = ttk.Entry(self.frame, width=10)
        self.preco.grid(row=2, column=1)
        
        ttk.Button(self.frame, text="Adicionar", command=self.adicionar_item).grid(row=3, column=0, columnspan=2)
        
        self.tree = ttk.Treeview(self.frame, columns=("#1", "#2", "#3"), show="headings")
        self.tree.heading("#1", text="Descrição")
        self.tree.heading("#2", text="Quantidade")
        self.tree.heading("#3", text="Preço Unitário")
        self.tree.grid(row=4, column=0, columnspan=2)
        
        ttk.Button(self.frame, text="Gerar PDF", command=self.gerar_pdf).grid(row=5, column=0)
        ttk.Button(self.frame, text="Exportar Excel", command=self.exportar_excel).grid(row=5, column=1)
        
    def adicionar_item(self):
        descricao = self.descricao.get()
        quantidade = self.quantidade.get()
        preco = self.preco.get()
        
        if descricao and quantidade and preco:
            self.dados.append((descricao, quantidade, preco))
            self.tree.insert("", tk.END, values=(descricao, quantidade, preco))
            self.descricao.delete(0, tk.END)
            self.quantidade.delete(0, tk.END)
            self.preco.delete(0, tk.END)
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
        
    def gerar_pdf(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not arquivo:
            return
        
        c = canvas.Canvas(arquivo, pagesize=A4)
        width, height = A4
        c.drawString(100, height - 50, "Relatório de Orçamento")
        
        y = height - 100
        for item in self.dados:
            c.drawString(100, y, f"{item[0]} - {item[1]} x R${item[2]}")
            y -= 20
        
        c.save()
        messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
        
    def exportar_excel(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not arquivo:
            return
        
        df = pd.DataFrame(self.dados, columns=["Descrição", "Quantidade", "Preço Unitário"])
        df.to_excel(arquivo, index=False)
        messagebox.showinfo("Sucesso", "Arquivo Excel gerado com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaOrcamento(root)
    root.mainloop()
