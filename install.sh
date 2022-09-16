#!/usr/bin/env bash

echo "Fetching code..."
mkdir $HOME/.local/share/
git clone https://github.com/Duckapple/Kat.git $HOME/.local/share/kat

echo "Ensuring binaries are in path..."
mkdir $HOME/.local/bin/
ln -s $HOME/.local/share/kat/kattis.py $HOME/.local/bin/kat
ln -s $HOME/.local/share/kat/kattis.py $HOME/.local/bin/kattis

if [[ "$PATH" != *"$HOME/.local/bin"* ]]; then
  if [ -f "$HOME/.zshrc" ]; then
    echo "export PATH=$PATH:$HOME/.local/bin" >> $HOME/.zshrc
  elif [ -f "$HOME/.bashrc"]; then
    echo "export PATH=$PATH:$HOME/.local/bin" >> $HOME/.bashrc
  else
    echo "Could not detect shell config file."
    echo "Add 'export PATH=$PATH:$HOME/.local/bin' to your shell config"
  fi
fi

echo "Installing dependencies..."

/usr/bin/env python3 -m pip install --user -r $HOME/.local/share/kat/requirements.txt

echo "======================================="
echo "Initial install complete!"
echo "Installed Kat to $HOME/.local/share/kat, invoke as 'kat' or 'kattis'"
echo "Navigate to https://open.kattis.com/download/kattisrc and save"
echo "  the 'kattisrc' to $HOME/ as '.kattisrc' to complete setup"

if [ "$(uname)" == "Darwin" ]; then
  open https://open.kattis.com/download/kattisrc
else
  xdg-open https://open.kattis.com/download/kattisrc
fi
