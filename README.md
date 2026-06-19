# Rsync GUI

Interface gráfica para o **rsync** construída com Python e PyQt6.

## Requisitos

- Python 3.10+
- rsync instalado no sistema (`sudo apt install rsync`)

## Instalação

```bash
git clone <repo-url> rsync-gui
cd rsync-gui
chmod +x install.sh
sudo ./install.sh
```

O `install.sh` copia a aplicação para `/opt/rsync-gui/`, instala as dependências
de sistema (rsync, python3, pip), cria o ambiente virtual, e gera:

- Lançador em `/usr/local/bin/rsync-gui`
- Atalho no menu de aplicações (`.desktop`)
- Ícone SVG

Após a instalação, execute com:

```bash
rsync-gui
```

## Execução sem instalação (desenvolvimento)

```bash
chmod +x run.sh
./run.sh
```

O script `run.sh` cria automaticamente um ambiente virtual (`.venv`),
instala as dependências (PyQt6, PyYAML) e inicia a aplicação.

## Funcionalidades

- Seleção de diretório local (source)
- Input com histórico de destinos recentes (salvo em `~/.config/rsync-gui/config.yaml`)
- Opções personalizáveis:
  - Dry run (`--dry-run`)
  - Delete (`--delete`)
  - Compress (`-z`)
  - Keep partial (`--partial`)
  - Bandwidth limit (`--bwlimit`)
  - Opções extras em texto livre
- Barra de progresso (parse da saída `--progress` do rsync)
- Log completo da execução em tempo real
- Botão para cancelar a transferência
- Histórico dos últimos 5 jobs (timestamp, diretórios, dados trafegados, duração)
- Tratamento de erros (rsync não encontrado, código de saída, etc.)
- Dark theme

## Estrutura do projeto

```
rsync-gui/
├── install.sh             # Instalação no sistema (Linux)
├── run.sh                 # Execução local (desenvolvimento)
├── requirements.txt       # PyQt6, PyYAML
├── icons/
│   └── rsync-gui.svg      # Ícone SVG
└── src/
    ├── __init__.py
    ├── __main__.py        # Entry point
    ├── app.py             # Bootstrap da aplicação Qt
    ├── core/
    │   ├── config.py      # Modelo RsyncConfig (dataclass)
    │   ├── progress_parser.py  # Parse de porcentagem da saída do rsync
    │   ├── rsync_worker.py     # QThread para execução assíncrona do rsync
    │   ├── storage.py          # Persistência YAML (histórico, destinos)
    │   └── theme.py            # Dark theme (Fusion + QPalette + QSS)
    └── ui/
        ├── destination_selector.py  # QComboBox com histórico de destinos
        ├── directory_selector.py    # Seletor de diretório com Browse
        ├── history_panel.py         # Tabela dos últimos 5 jobs
        ├── options_panel.py         # Painel de opções do rsync
        ├── progress_panel.py        # Barra de progresso + log
        └── main_window.py           # Janela principal
```

## Princípios de design

- **SOLID**: single responsibility (cada classe tem um propósito único),
  open/closed, segregação de interface
- **Modular**: componentes desacoplados e reutilizáveis
- **Clean Code**: nomes expressivos, funções pequenas, sem comentários

## Opção padrão do rsync

- `-avh --progress` (arquivos, recursivo, verbose, human-readable, progresso)

## Personalização

Para adicionar opções fixas ao rsync, edite `DEFAULT_RSYNC_OPTIONS`
em `src/core/config.py`.

## Desinstalação

```bash
sudo rm -rf /opt/rsync-gui /usr/local/bin/rsync-gui /usr/local/share/applications/rsync-gui.desktop /usr/local/share/icons/hicolor/scalable/apps/rsync-gui.svg
```

---

> **Disclaimer:** Este projeto foi desenvolvido com assistência de inteligência artificial.
