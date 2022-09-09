#!/usr/bin/env bash

git clone git@github.com:Duckapple/Kat.git $HOME/.local/share/kat
ln -s $HOME/.local/share/kat/kattis.py $HOME/.local/bin/kat
ln -s $HOME/.local/share/kat/kattis.py $HOME/.local/bin/kattis

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
