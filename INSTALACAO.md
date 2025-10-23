# 📦 Guia de Instalação - Sistema de Consulta de Coordenadas SIT# 🚀 Guia de Instalação Rápida



Instruções completas para instalar e executar o sistema em qualquer computador Windows.## Passo 1: Instalar Dependências



---Abra o terminal (cmd) no diretório do projeto e execute:



## 📋 Requisitos do Sistema```bash

pip install -r requirements.txt

### Hardware Mínimo```

- **Processador**: Intel Core i3 ou equivalente

- **RAM**: 4 GB (recomendado 8 GB)### Instalação Mínima (apenas para interface nova)

- **Disco**: 2 GB de espaço livre

- **SO**: Windows 7/8/10/11 (64-bit)Se quiser instalar apenas o necessário para a nova interface:



---```bash

pip install geopandas shapely pandas

## 🔧 Passo 1: Instalar QGIS 3.12```



### Download### Problemas com GeoPandas?

1. Acesse: https://qgis.org/downloads/

2. Procure por **QGIS 3.12** (versão LTR antiga)Se tiver problemas instalando geopandas no Windows, use:

3. Baixe o instalador para Windows 64-bit

```bash

### Instalaçãoconda install -c conda-forge geopandas

1. Execute o instalador `QGIS-OSGeo4W-3.12.X-X-Setup-x86_64.exe````

2. **IMPORTANTE**: Instale no caminho padrão:

   ```Ou baixe wheels pré-compilados de:

   C:\Program Files\QGIS 3.12https://www.lfd.uci.edu/~gohlke/pythonlibs/

   ```

3. Durante a instalação:## Passo 2: Executar a Interface

   - ✅ Instalar todos os componentes

   - ✅ Incluir Python 3```bash

   - ✅ Incluir bibliotecas GDALpython interface_consulta_qgis.py

   - ✅ Criar atalhos na área de trabalho```



4. Aguarde a instalação completa (~15 minutos)## Passo 3: Testar



### Verificar InstalaçãoUse estas coordenadas de exemplo:

1. Abra o Prompt de Comando (CMD)- **Zona**: 24

2. Execute:- **X (Leste)**: 507023

   ```cmd- **Y (Norte)**: 8646346

   "C:\Program Files\QGIS 3.12\bin\python-qgis.bat" --version

   ```## 🔧 Solução de Problemas

3. Deve mostrar algo como: `Python 3.7.0`

### Erro: ModuleNotFoundError: No module named 'geopandas'

---```bash

pip install geopandas

## 📥 Passo 2: Baixar o Projeto```



### Opção A: Clonar do GitHub (Recomendado)### Erro: No module named 'tkinter'

O tkinter vem com Python. Se não estiver disponível:

```cmd- Windows: Reinstale Python marcando "tcl/tk and IDLE"

cd C:\Users\SEU_USUARIO\Documents- Linux: `sudo apt-get install python3-tk`

git clone https://github.com/saviosales18/ConsultaCoordenadasSIT.git

cd ConsultaCoordenadasSIT### Erro ao carregar shapefile

```Verifique se os arquivos estão em:

```

### Opção B: Download DiretoLARGURAS FXD/FXD23.shp

LARGURAS FXD/FXD24.shp

1. Acesse: https://github.com/saviosales18/ConsultaCoordenadasSIT```

2. Clique em **Code** → **Download ZIP**

3. Extraia para: `C:\Users\SEU_USUARIO\Documents\ConsultaCoordenadasSIT`## 📁 Estrutura Necessária



---```

ConsultaCoordenadasSIT/

## 📂 Passo 3: Preparar os Shapefiles├── interface_consulta_qgis.py  ← Execute este

├── LARGURAS FXD/

### Estrutura de Pastas Necessária│   ├── FXD23.shp              ← Necessário

│   ├── FXD23.dbf              ← Necessário

```│   ├── FXD23.shx              ← Necessário

ConsultaCoordenadasSIT/│   ├── FXD23.prj              ← Necessário

└── LARGURAS FXD/│   ├── FXD24.shp              ← Necessário

    ├── FXD23.shp                  ← Faixa de Domínio Zona 23│   ├── FXD24.dbf              ← Necessário

    ├── FXD23.dbf│   ├── FXD24.shx              ← Necessário

    ├── FXD23.shx│   └── FXD24.prj              ← Necessário

    ├── FXD23.prj```

    ├── FXD24.shp                  ← Faixa de Domínio Zona 24

    ├── FXD24.dbf## ✅ Verificação da Instalação

    ├── FXD24.shx

    ├── FXD24.prjExecute para testar:

    ├── municipios23.shp           ← Municípios Zona 23

    ├── municipios23.dbf```bash

    ├── municipios23.shxpython teste_consulta.py

    ├── municipios23.prj```

    ├── municipios24.shp           ← Municípios Zona 24

    ├── municipios24.dbfSe funcionar, está tudo OK! 🎉

    ├── municipios24.shx

    ├── municipios24.prj## 📞 Versões Testadas

    ├── shape23.shp                ← Eixos Rodoviários Zona 23

    ├── shape23.dbf- Python 3.8+

    ├── shape23.shx- GeoPandas 0.14+

    ├── shape23.prj- Shapely 2.0+

    ├── shape24.shp                ← Eixos Rodoviários Zona 24- Windows 10/11

    ├── shape24.dbf

    ├── shape24.shx---

    └── shape24.prj

```**Dica**: Use ambientes virtuais para evitar conflitos:



### ⚠️ IMPORTANTE:```bash

- Cada shapefile precisa de **4 arquivos**: `.shp`, `.dbf`, `.shx`, `.prj`python -m venv venv

- Os nomes devem ser **exatamente** como mostrado acimavenv\Scripts\activate

- Sistema de Coordenadas deve ser **SIRGAS 2000 / UTM**pip install -r requirements.txt

  - Zona 23: EPSG:31983```

  - Zona 24: EPSG:31984

---

## ✅ Passo 4: Verificar Instalação

### Executar Teste

1. Abra o Prompt de Comando (CMD)
2. Navegue até a pasta do projeto:
   ```cmd
   cd C:\Users\SEU_USUARIO\Documents\ConsultaCoordenadasSIT
   ```

3. Execute o teste com coordenada conhecida:
   ```cmd
   executar_standalone.bat 496787 8640850 24
   ```

### Resultado Esperado

```
============================================================
⚠️  DENTRO DA FXD
============================================================
RODOVIA:           052
TRECHO:            ENTR BR 116 - ENTR BA 499 (P/ BONFIM DE FEIRA)
JURISDIÇÃO:        ESTADUAL
LARGURA FXD:       60
AMPARO LEGAL:      Decreto nº 8.244 de 06/05/2002
CÓDIGO SRE:        052EBA0005
MUNICÍPIO:         Feira de Santana
PAVIMENTAÇÃO:      CBUQ
DISTÂNCIA DO EIXO: 1.53 m
KM CALCULADO:      0.04 km
============================================================
```

---

## 🚀 Como Usar

### Sintaxe Básica

```cmd
executar_standalone.bat <X> <Y> <ZONA>
```

### Parâmetros

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| **X** | Coordenada Este (UTM) em metros | 496787 |
| **Y** | Coordenada Norte (UTM) em metros | 8640850 |
| **ZONA** | Zona UTM (23 ou 24) | 24 |

### Exemplos de Uso

**Zona 24 (Leste da Bahia):**
```cmd
executar_standalone.bat 496787 8640850 24
```

**Zona 23 (Oeste da Bahia):**
```cmd
executar_standalone.bat 450000 8500000 23
```

---

## 🔍 Como Obter Coordenadas UTM

### No Google Earth Pro

1. Abra o Google Earth Pro
2. Vá em: **Ferramentas** → **Opções** → **Vista 3D**
3. Em "Mostrar Lat/Long", selecione: **UTM**
4. Clique em qualquer ponto no mapa
5. As coordenadas aparecerão no canto inferior

### No QGIS

1. Abra seu projeto no QGIS
2. Configure o SRC do projeto para:
   - Zona 23: **EPSG:31983**
   - Zona 24: **EPSG:31984**
3. Clique com botão direito no ponto
4. Copie as coordenadas X e Y

### Online

Acesse: https://www.latlong.net/lat-long-utm.html
1. Cole as coordenadas lat/long
2. Selecione o datum: **SIRGAS 2000**
3. Obtenha as coordenadas UTM

---

## 🛠️ Solução de Problemas

### Erro: "QGIS não encontrado"

**Problema:**
```
❌ ERRO: QGIS não encontrado em: C:\Program Files\QGIS 3.12
```

**Solução:**
1. Verifique se QGIS foi instalado no caminho correto
2. Se instalou em outro local, edite `consulta_standalone.py`:
   ```python
   QGIS_PATH = r"C:\Program Files\QGIS 3.12"  # Ajuste aqui
   ```

---

### Erro: "Nenhum shapefile encontrado"

**Problema:**
```
❌ AVISO: Nenhum shapefile encontrado em LARGURAS FXD
```

**Solução:**
1. Verifique se a pasta `LARGURAS FXD` existe
2. Confirme que os shapefiles estão dentro desta pasta
3. Verifique os nomes dos arquivos (shape23.shp, shape24.shp, etc.)

---

### Erro: "Coordenada fora do range esperado"

**Problema:**
```
❌ ERRO: Coordenada X 1234 fora do range esperado para zona 24 (200000-850000)
```

**Solução:**
1. Verifique se as coordenadas estão em UTM (não em graus)
2. Confirme a zona correta (23 ou 24)
3. Verifique o sistema de referência: deve ser SIRGAS 2000

**Limites válidos:**
- **Zona 23**: X entre 160.000 e 850.000
- **Zona 24**: X entre 200.000 e 850.000
- **Ambas zonas**: Y entre 8.000.000 e 9.200.000

---

### Erro: "Nenhuma rodovia encontrada"

**Problema:**
```
❌ Nenhuma feição encontrada dentro do limite de 200m.
ℹ️  Rodovia mais próxima está a 15234.56m de distância.
```

**Solução:**
1. Coordenada está muito longe das rodovias cadastradas
2. Verifique se a zona está correta (troque 23 ↔ 24)
3. Confirme que as coordenadas são SIRGAS 2000 (não WGS84 ou outro datum)
4. Use ferramentas online para converter coordenadas

---

## 📊 Informações Retornadas

O sistema retorna as seguintes informações:

| Campo | Descrição |
|-------|-----------|
| **STATUS FXD** | ⚠️ DENTRO DA FXD ou ✅ FORA DA FXD |
| **RODOVIA** | Número da rodovia estadual (ex: 052 = BA-052) |
| **TRECHO** | Início e fim do trecho |
| **JURISDIÇÃO** | Estadual, Federal ou Municipal |
| **LARGURA FXD** | Largura da faixa de domínio em metros |
| **AMPARO LEGAL** | Decreto ou lei que define a FXD |
| **CÓDIGO SRE** | Código do segmento no SRE |
| **MUNICÍPIO** | Município onde está localizado |
| **PAVIMENTAÇÃO** | Tipo de pavimento (CBUQ, TSD, etc.) |
| **DISTÂNCIA DO EIXO** | Distância perpendicular ao eixo em metros |
| **KM CALCULADO** | Quilometragem exata no eixo rodoviário |

---

## 📁 Estrutura do Projeto

```
ConsultaCoordenadasSIT/
├── consulta_standalone.py      # Script principal (Python + PyQGIS)
├── executar_standalone.bat     # Executor em lote (Windows)
├── README.md                    # Documentação geral
├── INSTALACAO.md               # Este arquivo
├── requirements.txt             # Dependências Python (informativo)
├── .gitignore                   # Arquivos ignorados pelo Git
└── LARGURAS FXD/               # Shapefiles das rodovias
    ├── FXD23.shp               # Faixa de domínio zona 23
    ├── FXD24.shp               # Faixa de domínio zona 24
    ├── municipios23.shp        # Municípios zona 23
    ├── municipios24.shp        # Municípios zona 24
    ├── shape23.shp             # Eixos rodoviários zona 23
    └── shape24.shp             # Eixos rodoviários zona 24
```

---

## 🔐 Requisitos de Sistema de Coordenadas

### Shapefiles Devem Ter:

1. **Sistema de Referência**: SIRGAS 2000
2. **Projeção**: UTM (Universal Transversa de Mercator)
3. **Zona**: 23S ou 24S (sul do equador)
4. **EPSG**:
   - Zona 23: **31983**
   - Zona 24: **31984**

### Como Verificar no QGIS:

1. Abra o shapefile no QGIS
2. Clique com botão direito na camada
3. Propriedades → Informação
4. Verifique o campo "SRC": deve mostrar `EPSG:31983` ou `EPSG:31984`

---

## 📞 Suporte

### Em caso de dúvidas:

1. **GitHub Issues**: https://github.com/saviosales18/ConsultaCoordenadasSIT/issues
2. **Email**: savio.silva@exemplo.com
3. **Documentação**: Leia o `README.md` no repositório

---

## 📝 Notas Importantes

### ⚠️ Atenção:

1. **NÃO** mova ou renomeie a pasta `LARGURAS FXD`
2. **NÃO** altere os nomes dos shapefiles
3. **NÃO** modifique o caminho de instalação do QGIS após configurar
4. Mantenha todos os 4 arquivos de cada shapefile (.shp, .dbf, .shx, .prj)

### ✅ Boas Práticas:

1. Faça backup dos shapefiles antes de qualquer alteração
2. Mantenha o projeto em uma pasta de fácil acesso
3. Crie atalho do `executar_standalone.bat` na área de trabalho
4. Use coordenadas com precisão de metro (sem casas decimais excessivas)

---

## 🔄 Atualização do Sistema

### Atualizar via Git:

```cmd
cd C:\Users\SEU_USUARIO\Documents\ConsultaCoordenadasSIT
git pull origin main
```

### Atualizar manualmente:

1. Faça backup da pasta `LARGURAS FXD`
2. Baixe a versão mais recente do GitHub
3. Substitua todos os arquivos, **EXCETO** `LARGURAS FXD`
4. Teste com uma coordenada conhecida

---

## 📄 Licença

Sistema desenvolvido para o Sistema de Informações de Transportes (SIT) da Bahia.

---

**Desenvolvido com PyQGIS** | **Última atualização: Outubro 2025**

---

## ✅ Checklist de Instalação

Use esta checklist para garantir que tudo está correto:

- [ ] QGIS 3.12 instalado em `C:\Program Files\QGIS 3.12`
- [ ] Projeto baixado/clonado
- [ ] Pasta `LARGURAS FXD` existe
- [ ] Shapefiles zona 23 presentes (FXD23, municipios23, shape23)
- [ ] Shapefiles zona 24 presentes (FXD24, municipios24, shape24)
- [ ] Cada shapefile tem 4 arquivos (.shp, .dbf, .shx, .prj)
- [ ] Teste executado com sucesso
- [ ] Resultado correto exibido

**Se todos os itens estão marcados, o sistema está pronto para uso!** 🎉
