from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Dados da tabela (pode ser qualquer lista de listas)
data = [['Nome', 'Idade', 'Cidade'],
        ['João', '30', 'São Paulo'],
        ['Maria', '25', 'Rio de Janeiro'],
        ['Pedro', '35', 'Salvador'],
        ['Ana', '28', 'Fortaleza']]

# Crie um arquivo PDF
pdf_filename = "tabela.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Crie a tabela e defina seu estilo
table = Table(data)
style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)])

table.setStyle(style)

# Construa a tabela e salve o PDF
elements = []
elements.append(table)
doc.build(elements)

print(f'O arquivo PDF "{pdf_filename}" foi criado com sucesso!')
