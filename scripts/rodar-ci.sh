#!/usr/bin/env bash
# Usado pelo GitHub Actions dentro do emulador: sobe o Appium, roda os testes e grava os vídeos.
set -u
mkdir -p reports
appium --log reports/appium.log --log-timestamp > /dev/null 2>&1 &
APPIUM_PID=$!

for i in $(seq 1 30); do
  curl -sf http://127.0.0.1:4723/status > /dev/null && break
  sleep 2
done

GRAVAR_VIDEO=1 python -m pytest -v
RESULTADO=$?

kill $APPIUM_PID 2>/dev/null || true
exit $RESULTADO
