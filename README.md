# 🛣️ Sistema de Consulta de Coordenadas - SIT Bahia# 🗺️ Consulta de Coordenadas SIT - DERBA/BA



Sistema para consulta precisa de coordenadas UTM em rodovias estaduais da Bahia, calculando a quilometragem exata e distância do eixo rodoviário.Sistema de consulta de informações de rodovias estaduais da Bahia através de coordenadas SIRGAS 2000 UTM.



## 📋 Requisitos![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)

![QGIS](https://img.shields.io/badge/QGIS-3.12+-green.svg)

- **QGIS 3.12** instalado em: `C:\Program Files\QGIS 3.12`![PyQGIS](https://img.shields.io/badge/PyQGIS-Integrated-orange.svg)

- **Python** (incluído no QGIS)![License](https://img.shields.io/badge/License-MIT-yellow.svg)

- **Shapefiles** das rodovias em: `LARGURAS FXD/`

---

## 🚀 Uso Rápido

## ⚠️ **AVISO IMPORTANTE - LEIA PRIMEIRO!**

```cmd

executar_standalone.bat <X> <Y> <ZONA>### Está vendo este erro?

``````

ModuleNotFoundError: No module named '_tkinter'

### Exemplos```



```cmd### ✅ **SOLUÇÃO RÁPIDA (2 minutos):**

# Consulta na BA-052 (Feira de Santana)

executar_standalone.bat 496787 8640850 241. **Abra QGIS 3.12 Desktop**

2. **Console Python:** `Plugins` → `Python Console` (ou `Ctrl+Alt+P`)

# Outra consulta na zona 233. **Cole este comando:**

executar_standalone.bat 510807 8649627 23   ```python

```   exec(open(r'C:\Users\savio.silva\Documents\repositories\ConsultaCoordenadasSIT\app_qgis_console.py').read()); consultar_coordenadas()

   ```

## 📊 Saída4. **Preencha:** Zona, X, Y

5. **Funciona!** 🎉

O sistema retorna:

📄 **Guia detalhado:** [`ERRO_E_SOLUCAO.md`](ERRO_E_SOLUCAO.md)  

- ✅ **Rodovia** identificada (ex: BA-052)📋 **Comandos prontos:** [`COPIE_E_COLE.md`](COPIE_E_COLE.md)

- ✅ **KM Calculado** - Quilometragem exata do ponto

- ✅ **Distância do Eixo** - Distância perpendicular até o eixo (metros)---

- ✅ **Município** - Localização administrativa

- ✅ **Código SRE** - Código do segmento rodoviário## 📋 Sobre o Projeto

- ✅ **Tipo de Revestimento** - CBUQ, TSD, etc.

Este projeto permite consultar informações detalhadas sobre rodovias estaduais da Bahia a partir de coordenadas geográficas UTM, incluindo:

### Exemplo de Saída

- ✅ Nome da rodovia

```- ✅ Trecho (início e fim)

============================================================- ✅ Jurisdição (estadual/federal)

📊 RESULTADO DA CONSULTA- ✅ Largura da Faixa de Domínio (FXD)

============================================================- ✅ Amparo legal

- ✅ Município onde se localiza

🛣️  RODOVIA:- ✅ Verificação se está dentro da FXD

   Shapefile: shape24

   Rodovia: 052## 🖥️ Interface



📏 QUILOMETRAGEM:A nova interface gráfica oferece:

   KM Inicial: 0.000 km

   KM Final: 12.509 km```

   ➡️  KM CALCULADO: 0.044 km┌─────────────────────────────────────────────┐

│  Consulta de Coordenadas SIRGAS 2000 UTM   │

📐 DISTÂNCIA DO EIXO:├─────────────────────────────────────────────┤

   1.53 metros│  Zona UTM:          [23 ▼]                 │

│  Coordenada X:      [         ]            │

📋 OUTROS DADOS:│  Coordenada Y:      [         ]            │

   TIPO_DE_RE: CBUQ│                                             │

============================================================│           [ Consultar ]                     │

```├─────────────────────────────────────────────┤

│  Informações da Rodovia:                   │

## 🔧 Funcionalidades Técnicas│  ┌───────────────────────────────────────┐ │

│  │ • Rodovia: BA-099                     │ │

### 1. Cálculo Inteligente de KM│  │ • Trecho: Local A - Local B           │ │

│  │ • Jurisdição: Estadual                │ │

O sistema usa **detecção por percentil** para identificar automaticamente se a geometria foi desenhada na direção correta ou invertida:│  │ • Largura FXD: 80m                    │ │

│  │ • Amparo Legal: Lei XXXX              │ │

```python│  │ • Município: Salvador                 │ │

# Lógica de detecção│  └───────────────────────────────────────┘ │

- Percentual > 80%  → Geometria INVERTIDA (usa km_final - proporção)└─────────────────────────────────────────────┘

- Percentual < 20%  → Geometria NORMAL (usa km_inicial + proporção)```

- Entre 20-80%      → Valida qual opção está no range válido

```## 🚀 Instalação Rápida



**Por que isso é necessário?**```bash

# Clone o repositório

Alguns shapefiles têm geometrias desenhadas do km_final → km_inicial, causando erros de cálculo. O sistema detecta isso automaticamente e corrige.git clone https://github.com/saviosales18/ConsultaCoordenadasSIT.git

cd ConsultaCoordenadasSIT

### 2. Validação de Resultados

# Instale as dependências

- Filtra feições por distância máxima (100m)pip install -r requirements.txt

- Valida se KM calculado está dentro do range válido

- Escolhe a feição mais próxima do eixo# Execute a interface

python interface_consulta_qgis.py

### 3. Suporte Multi-Zona UTM```



- **Zona 23 (EPSG:31983)** - Oeste da Bahia📖 Ver [INSTALACAO.md](INSTALACAO.md) para instruções detalhadas

- **Zona 24 (EPSG:31984)** - Leste da Bahia

## 💻 Uso

## 📁 Estrutura do Projeto

### Interface Gráfica

```

ConsultaCoordenadasSIT/```bash

├── consulta_standalone.py      # Script principalpython interface_consulta_qgis.py

├── executar_standalone.bat     # Executor em lote```

├── README.md                    # Esta documentação

├── requirements.txt             # Dependências Python1. Selecione a zona UTM (23 ou 24)

└── LARGURAS FXD/               # Shapefiles das rodovias2. Digite a coordenada X (Leste)

    ├── FXD23.shp               # Faixa de domínio zona 233. Digite a coordenada Y (Norte)

    ├── FXD24.shp               # Faixa de domínio zona 244. Clique em "Consultar"

    ├── FNE23.shp               # Faixa não edificante zona 23

    ├── FNE24.shp               # Faixa não edificante zona 24### Linha de Comando

    ├── shape23.shp             # Cadastro geral zona 23

    └── shape24.shp             # Cadastro geral zona 24```bash

```python teste_consulta.py

```

## 🔍 Como Funciona

### Exemplo de Código

### Fluxo de Processamento

```python

```from shapely.geometry import Point

1. Recebe coordenadas UTM (X, Y, Zona)import geopandas as gpd

   ↓

2. Valida entrada (range válido para Bahia)# Criar ponto

   ↓ponto = Point(507023, 8646346)

3. Busca em todos os shapefiles disponíveis

   ↓# Carregar shapefile

4. Para cada feição próxima:gdf = gpd.read_file('LARGURAS FXD/FXD24.shp')

   - Calcula distância perpendicular ao eixo

   - Calcula posição ao longo da linha (lineLocatePoint)# Verificar intersecção

   - Determina percentual percorridofor idx, feature in gdf.iterrows():

   - Aplica lógica de detecção de inversão    if feature.geometry.contains(ponto):

   ↓        print(f"Rodovia: {feature['RODOVIA']}")

5. Filtra resultados válidos (KM dentro do range)        print(f"Jurisdição: {feature['JURISDI_C']}")

   ↓        break

6. Retorna feição mais próxima do eixo```

```

## 📁 Estrutura do Projeto

### Algoritmo de Cálculo de KM

```

```pythonConsultaCoordenadasSIT/

# 1. Localizar ponto na linha├── 📄 interface_consulta_qgis.py    # ⭐ Interface principal (USE ESTE!)

distancia_ao_longo = geometria.lineLocatePoint(ponto)├── 📄 app.py                         # Interface antiga (Selenium)

percentual = (distancia_ao_longo / comprimento_total) * 100├── 📄 muni.py                        # Script consulta município

├── 📄 teste_consulta.py              # Testes via linha de comando

# 2. Calcular ambas opções│

km_normal = km_inicial + (proporcao * (km_final - km_inicial))├── 📂 LARGURAS FXD/                  # Shapefiles das rodovias

km_invertida = km_final - (proporcao * (km_final - km_inicial))│   ├── FXD23.shp                     # Faixa Domínio Zona 23S

│   ├── FXD24.shp                     # Faixa Domínio Zona 24S

# 3. Decidir baseado no percentil│   ├── municipios23.shp              # Municípios Zona 23S

if percentual > 80:│   └── municipios24.shp              # Municípios Zona 24S

    km_correto = km_invertida  # Geometria invertida│

elif percentual < 20:├── 📂 prompts/                       # Códigos exemplo QGIS

    km_correto = km_normal     # Geometria normal│   ├── Retorna Info das feições.txt

else:│   └── fxd sim-não pythonGis.txt

    km_correto = validar_range(km_normal, km_invertida)│

```├── 📂 PROJETOS/                      # Arquivos CAD

├── 📂 CONVERSORES/                   # Planilhas conversoras

## 🎯 Casos de Uso│

├── 📖 README.md                      # Este arquivo

### 1. Consulta de Licenciamento├── 📖 README_INTERFACE.md            # Documentação da interface

├── 📖 ANALISE_PROJETO.md             # Análise completa do projeto

Determine exatamente em qual KM uma construção está localizada para fins de licenciamento ambiental.├── 📖 INSTALACAO.md                  # Guia de instalação

└── 📄 requirements.txt               # Dependências Python

### 2. Fiscalização```



Identifique rapidamente se uma edificação está dentro da faixa de domínio ou faixa não edificante.## 🛠️ Tecnologias



### 3. Planejamento- **Python 3.8+**

- **GeoPandas** - Processamento de dados geoespaciais

Localize precisamente pontos de interesse ao longo das rodovias estaduais.- **Shapely** - Operações geométricas

- **Tkinter** - Interface gráfica

### 4. Manutenção- **Pandas** - Manipulação de dados



Registre localização exata de danos, buracos ou necessidade de manutenção.## 🗺️ Sistemas de Coordenadas



## ⚙️ Parâmetros Técnicos### SIRGAS 2000 UTM



| Parâmetro | Descrição | Valores |**Zona 23S (EPSG:31983)**

|-----------|-----------|---------|- Meridiano Central: -45°

| **X** | Coordenada Este (UTM) | 200.000 - 800.000 m |- Área: Oeste da Bahia

| **Y** | Coordenada Norte (UTM) | 8.000.000 - 9.000.000 m |

| **ZONA** | Zona UTM | 23 ou 24 |**Zona 24S (EPSG:31984)**

| **Distância Máxima** | Raio de busca | 100 metros |- Meridiano Central: -39°

| **Precisão KM** | Casas decimais | 3 (0.001 km = 1 metro) |- Área: Leste da Bahia



## 🐛 Troubleshooting## 📊 Dados



### Erro: "QGIS não encontrado"Os shapefiles contêm informações de:



```- **Faixas de Domínio (FXD)** - Área de propriedade da rodovia

❌ ERRO: QGIS não encontrado em: C:\Program Files\QGIS 3.12- **Faixas Não Edificáveis (FNE)** - Áreas com restrições

```- **Municípios** - Divisão territorial

- **Rodovias Estaduais** - Malha viária

**Solução**: Instale QGIS 3.12 ou ajuste o caminho em `consulta_standalone.py`:

**Fonte:** DERBA - Departamento de Infraestrutura de Transportes da Bahia

```python

QGIS_PATH = r"C:\Program Files\QGIS 3.12"  # Ajuste aqui## 📝 Exemplos de Coordenadas

```

### Teste 1 - Rodovia BA-099

### Erro: "Nenhum shapefile encontrado"```

Zona: 24

```X: 507023

❌ AVISO: Nenhum shapefile encontrado em LARGURAS FXDY: 8646346

``````



**Solução**: Verifique se o diretório `LARGURAS FXD/` existe e contém arquivos `.shp`### Teste 2 - Zona 23

```

### Erro: "Nenhuma rodovia encontrada"Zona: 23

X: [sua coordenada]

```Y: [sua coordenada]

❌ Nenhuma rodovia encontrada nesta coordenada.```

```

## 🔍 Funcionalidades

**Possíveis causas**:

1. Coordenada fora da área coberta pelos shapefiles### ✅ Implementadas

2. Zona UTM incorreta (troque 23 ↔ 24)

3. Ponto muito distante do eixo (>100m)- [x] Interface gráfica moderna

- [x] Consulta em shapefiles QGIS

## 📝 Clean Code Aplicado- [x] Validação de entrada

- [x] Detecção de FXD

Este projeto segue princípios de clean code:- [x] Informações completas da rodovia

- [x] Consulta de município

✅ **Funções Pequenas**: Cada função tem uma responsabilidade única  - [x] Suporte zonas 23S e 24S

✅ **Nomes Descritivos**: Variáveis e funções com nomes claros  - [x] Tratamento de erros

✅ **Comentários Úteis**: Documentação em docstrings  

✅ **DRY**: Sem repetição de código  ### 🚧 Futuras

✅ **Type Hints**: Tipos explícitos para parâmetros e retornos  

✅ **Tratamento de Erros**: Validações e exceções adequadas  - [ ] Processamento em lote

✅ **Separação de Responsabilidades**: Lógica dividida em módulos  - [ ] Exportação para CSV/PDF

- [ ] Visualização em mapa

## 📄 Licença- [ ] Histórico de consultas

- [ ] Busca por rodovia

Sistema desenvolvido para o Sistema de Informações de Transportes (SIT) da Bahia.- [ ] Cálculo de distância ao eixo

- [ ] API REST

---

## 📚 Documentação

**Desenvolvido com PyQGIS** | **Última atualização: Outubro 2025**

- [📖 README_INTERFACE.md](README_INTERFACE.md) - Detalhes da interface
- [📖 ANALISE_PROJETO.md](ANALISE_PROJETO.md) - Análise completa
- [📖 INSTALACAO.md](INSTALACAO.md) - Guia de instalação

## 🐛 Solução de Problemas

### Coordenada fora da FXD

- Verifique se a zona está correta (23 ou 24)
- Confirme o sistema de coordenadas (SIRGAS 2000 UTM)
- A rodovia pode ser federal (não cadastrada)

### Erro ao carregar shapefile

```bash
# Verifique se os arquivos existem
dir "LARGURAS FXD\FXD*.shp"

# Certifique-se de ter todos os arquivos:
# .shp, .shx, .dbf, .prj
```

### Erro de importação

```bash
pip install --upgrade geopandas shapely
```

## 👨‍💻 Desenvolvimento

### Estrutura do Código

```python
# Fluxo principal
1. Entrada de dados (zona, x, y)
2. Validação
3. Criar geometria Point
4. Carregar shapefile correspondente
5. Verificar intersecção/contenção
6. Extrair atributos
7. Buscar município (opcional)
8. Formatar e exibir resultado
```

### Testes

```bash
# Teste unitário
python teste_consulta.py

# Teste da interface
python interface_consulta_qgis.py
```

## 📄 Licença

Este projeto é de uso interno para consultas técnicas.

## 👥 Contribuição

Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📞 Contato

**Projeto:** ConsultaCoordenadasSIT  
**Órgão:** DERBA - Bahia  
**Sistema:** SIT (Sistema de Informações Territoriais)

---

## 🎯 Quick Start

```bash
# 1. Instalar
pip install geopandas shapely

# 2. Executar
python interface_consulta_qgis.py

# 3. Testar com coordenadas de exemplo
Zona: 24
X: 507023
Y: 8646346

# 4. Clique em Consultar

# 5. Veja o resultado! 🎉
```

---

**Desenvolvido para consultas de rodovias estaduais da Bahia** 🗺️  
**Versão:** 2.0  
**Última atualização:** Outubro/2025
