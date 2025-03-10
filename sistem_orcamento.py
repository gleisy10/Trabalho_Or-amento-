import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_planilha_e_pdf():
    # 1. Criando os dados da planilha
    dados = {
        "Item": [
            "Modem", 
            "Firewall", 
            "Roteador", 
            "Switch 24 portas", 
            "Patch Panel 24 portas", 
            "Access Point (Wi-Fi)",
            "Patch Cords (1 metro)", 
            "Canaletas (2 metros)", 
            "Tomadas com conectores fêmea"
        ],
        "Quantidade": [1, 1, 1, 1, 1, 2, 20, 10, 10],
        "Preço Unitário (R$)": [250, 600, 300, 500, 250, 350, 15, 20, 25],
    }

    # 2. Calculando o custo total
    custo_total = []
    for qtd, preco in zip(dados["Quantidade"], dados["Preço Unitário (R$)"]):
        custo_total.append(qtd * preco)

    dados["Custo Total (R$)"] = custo_total

    # 3. Criando o DataFrame
    df = pd.DataFrame(dados)

    # 4. Adicionando uma linha de TOTAL GERAL
    total_geral = df["Custo Total (R$)"].sum()
    # Aqui adicionamos uma nova linha com o total geral
    df.loc[len(df)] = ["TOTAL GERAL", "", "", total_geral]

    # 5. Exportando para Excel (opcional, se quiser ter um arquivo XLSX também)
    nome_arquivo_excel = "orcamento_rede.xlsx"
    df.to_excel(nome_arquivo_excel, index=False)

    print(f"Arquivo Excel '{nome_arquivo_excel}' gerado com sucesso!")

    # 6. Gerando o PDF
    nome_arquivo_pdf = "orcamento_rede.pdf"
    c = canvas.Canvas(nome_arquivo_pdf, pagesize=A4)
    largura, altura = A4

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, altura - 50, "Relatório de Orçamento - Equipamentos de Rede")

    # Cabeçalhos
    c.setFont("Helvetica-Bold", 10)
    y = altura - 100
    c.drawString(50, y, "Item")
    c.drawString(230, y, "Quantidade")
    c.drawString(330, y, "Preço Unitário (R$)")
    c.drawString(460, y, "Custo Total (R$)")

    # Conteúdo
    c.setFont("Helvetica", 10)
    y -= 20
    for i in range(len(df)):
        item = str(df.loc[i, "Item"])
        quantidade = str(df.loc[i, "Quantidade"])
        preco_unitario = df.loc[i, "Preço Unitário (R$)"]
        custo_total_item = df.loc[i, "Custo Total (R$)"]

        # Se for uma string vazia (como no TOTAL GERAL), a formatação fica diferente
        if quantidade == "":
            quantidade = "-"
            preco_unitario = "-"
        
        c.drawString(50, y, item)
        c.drawString(230, y, quantidade)
        
        # Se preco_unitario não for string vazia
        if preco_unitario != "-":
            c.drawString(330, y, f"R$ {preco_unitario:.2f}")
        else:
            c.drawString(330, y, "-")

        # Custo total
        if custo_total_item != "":
            c.drawString(460, y, f"R$ {float(custo_total_item):.2f}")
        else:
            c.drawString(460, y, "-")

        y -= 20

    # Espaço para a fonte
    y -= 40
    c.setFont("Helvetica", 9)
    c.drawString(50, y, "Fonte: Dados estimados com base em pesquisas de mercado (Março/2025)")

    # Salvando o PDF
    c.save()
    print(f"Arquivo PDF '{nome_arquivo_pdf}' gerado com sucesso!")

if __name__ == "__main__":
    gerar_planilha_e_pdf()
