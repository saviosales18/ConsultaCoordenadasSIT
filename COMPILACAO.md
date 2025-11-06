# Sistema de Consulta de Coordenadas - Executável Standalone

## 📦 Compilação do Executável

Este projeto pode ser compilado em um executável standalone que **não requer instalação do QGIS** no computador de destino.

### Pré-requisitos

1. **Python 3.9** instalado
2. **QGIS 3.12** instalado em: `C:\Program Files\QGIS 3.12`
3. **PyInstaller** instalado

### Instalação do PyInstaller

```cmd
pip install pyinstaller
```

### Passo a Passo para Compilar

#### 1. Prepare o Ambiente

Certifique-se de que todos os arquivos estão presentes:
- `consulta_interativa.py` - Script principal interativo
- `build_exe.py` - Script de compilação
- `LARGURAS FXD/` - Pasta com os shapefiles

#### 2. Execute a Compilação

```cmd
python build_exe.py
```

O script irá:
- Verificar se PyInstaller está instalado
- Localizar o QGIS instalado
- Configurar as dependências
- Compilar o executável único

#### 3. Arquivos Gerados

Após a compilação, você terá:

```
dist/
  └── ConsultaCoordenadas.exe  (executável standalone)
build/
  └── (arquivos temporários)
ConsultaCoordenadas.spec
  └── (especificação do PyInstaller)
```

### 📂 Distribuição

Para distribuir o sistema, crie um pacote com:

```
📦 ConsultaCoordenadasSIT/
  ├── ConsultaCoordenadas.exe    (executável compilado)
  └── LARGURAS FXD/               (shapefiles - OBRIGATÓRIO)
       ├── FXD23.shp
       ├── FXD24.shp
       ├── shape23.shp
       ├── shape24.shp
       ├── municipios23.shp
       ├── municipios24.shp
       └── (todos os arquivos .dbf, .shx, .prj, .cpg)
```

⚠️ **IMPORTANTE**: A pasta `LARGURAS FXD` deve estar no **mesmo diretório** do executável.

### 🚀 Uso do Executável

1. **Execute o programa**:
   - Dê duplo clique em `ConsultaCoordenadas.exe`
   - OU execute via prompt: `ConsultaCoordenadas.exe`

2. **Interface interativa**:
   ```
   ============================================================================
     CONSULTA DE COORDENADAS - SISTEMA RODOVIÁRIO
   ============================================================================

   Digite as coordenadas UTM (ou 'sair' para encerrar):

     Coordenada X (Este): 556853
     Coordenada Y (Norte): 8596068
     Zona UTM (23 ou 24): 24
   ```

3. **Resultado**:
   ```
   ============================================================================
   ⚠️  DENTRO DA FXD
   ============================================================================

   CÓDIGO SRE:        522EBA0025
   RODOVIA:           BA - 522
   TRECHO:            FIM DA TRAVESSIA URBANA DE CANDEIAS - ENTR BA 524
   MUNICÍPIO:         CANDEIAS
   KM CALCULADO:      33.41 km
   JURISDIÇÃO:        ESTADUAL
   AMPARO LEGAL:      Decreto nº 3.405 de 28/12/1989
   LARGURA FXD:       40
   PAVIMENTAÇÃO:      CBUQ
   DISTÂNCIA DO EIXO: 6.79 m

   Deseja fazer outra consulta? (S/N):
   ```

### 🔧 Solução de Problemas

#### Erro: "QGIS não encontrado"
- Verifique se o QGIS está instalado em `C:\Program Files\QGIS 3.12`
- Ajuste o caminho no arquivo `build_exe.py` se necessário

#### Erro: "PyInstaller não encontrado"
```cmd
pip install pyinstaller
```

#### Erro: "LARGURAS FXD não encontrado"
- Certifique-se de que a pasta está no mesmo diretório do .exe
- Verifique se todos os arquivos .shp, .dbf, .shx, .prj, .cpg estão presentes

#### Executável muito grande
- Normal! O executável incluirá todas as DLLs do QGIS (~500MB)
- Isso garante funcionamento em qualquer ambiente Windows

### 📋 Requisitos do Sistema de Destino

- **Windows 7/10/11** (64-bit)
- **Memória RAM**: Mínimo 4GB, recomendado 8GB
- **Espaço em disco**: ~1GB (executável + shapefiles)
- **Nenhuma dependência externa** (QGIS não precisa estar instalado)

### 🎯 Vantagens do Executável

✅ **Portável**: Funciona em qualquer Windows sem instalação  
✅ **Standalone**: Todas as dependências incluídas  
✅ **Simples**: Interface interativa via console  
✅ **Rápido**: Não precisa inicializar QGIS completo  
✅ **Distribuível**: Fácil de compartilhar com equipe  

### 📝 Notas Técnicas

- **Motor PyQGIS**: Incluído no executável
- **Bibliotecas Qt**: Empacotadas automaticamente
- **DLLs GDAL/GEOS**: Incluídas pelo PyInstaller
- **Shapefiles**: Devem estar na pasta `LARGURAS FXD`
- **Modo headless**: Qt rodando em modo offscreen (sem GUI)

### 🔄 Atualizações

Para atualizar o executável:

1. Modifique `consulta_interativa.py`
2. Execute novamente: `python build_exe.py`
3. Redistribua o novo `ConsultaCoordenadas.exe`

### 📞 Suporte

Em caso de dúvidas ou problemas:
- Verifique os logs de erro no console
- Confirme versões: Python 3.9, QGIS 3.12
- Teste primeiro com `python consulta_interativa.py`
