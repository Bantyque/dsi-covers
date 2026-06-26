#!/usr/bin/env bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=== Установка dsi-covers ===${NC}"

echo -e "\n${BLUE}[1/3] Установка Python-библиотек...${NC}"
pip install --user requests pillow tqdm

echo -e "\n${BLUE}[2/3] Копирование в ~/.local/bin/...${NC}"
mkdir -p "$HOME/.local/bin"

cp dsi-covers.py "$HOME/.local/bin/dsi-covers"
chmod +x "$HOME/.local/bin/dsi-covers"

echo -e "\n${BLUE}[3/3] Создание .desktop ...${NC}"
mkdir -p "$HOME/.local/share/applications"

cat << EOF > "$HOME/.local/share/applications/dsi-covers.desktop"
[Desktop Entry]
Type=Application
Name=DSi Covers Fetcher
Comment=Скачивание и ресайз обложек для TWiLightMenu
Exec=bash -c "dsi-covers; echo -e '\nНажмите Enter для выхода...'; read"
Icon=applications-games
Terminal=true
Categories=Game;Utility;
EOF

echo -e "\n${GREEN}=== Установка успешно завершена! ===${NC}"
