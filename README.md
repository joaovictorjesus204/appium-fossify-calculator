# Appium + Python | Fossify Calculator (Android)

[![Testes mobile](https://github.com/joaovictorjesus204/appium-fossify-calculator/actions/workflows/appium.yml/badge.svg)](https://github.com/joaovictorjesus204/appium-fossify-calculator/actions/workflows/appium.yml)

**📊 Relatório da última execução, com vídeo de cada teste:** https://joaovictorjesus204.github.io/appium-fossify-calculator/

Testes mobile em **Python** com **Appium (UiAutomator2)** e **pytest** no **[Fossify Calculator](https://github.com/FossifyOrg/Calculator)**, calculadora Android de código aberto com conversor de unidades, distribuída no Google Play e no F-Droid. O celular roda em **português do Brasil**, com vírgula decimal e ponto no milhar.

Autor: João Victor de Jesus

---

## Números

| | |
|---|---|
| Testes | 27 (17 da calculadora e 10 do conversor de unidades) |
| Tipos | Operações, regras de exibição, erros, histórico e conversões orientadas a dados |
| Dispositivo | Emulador Android 14 (API 34), em português do Brasil |
| Evidências | Print da tela em cada falha e vídeo de cada teste no CI |
| Execução automática | A cada push e diariamente, nos dias úteis, pelo GitHub Actions, com emulador próprio |
| Relatório | HTML (pytest-html) publicado no GitHub Pages |

---

## Cobertura

| ID | Cenário | Tag |
|---|---|---|
| CALC-01 | 7 + 8 = 15 | `smoke` |
| CALC-02 | Multiplicação, divisão com decimal, resultado negativo, potência, raiz quadrada, 15% de 200 e 200 + 15% (7 casos) | |
| CALC-03 | 0,1 + 0,2 = 0,3, sem o erro de arredondamento de ponto flutuante | |
| CALC-04 | Resultado com ponto no milhar: 1.234.000 | |
| CALC-05 | A fórmula exibe a conta feita | |
| CALC-06 | Divisão por zero mostra "Erro: divisão por zero" | |
| CALC-07 | Apagar remove só o último dígito | |
| CALC-08 | Segurar o botão C zera resultado e fórmula | |
| CALC-09 | O resultado continua na próxima conta (15 × 2 = 30) | |
| CALC-10 | Histórico guarda as contas da mais recente para a mais antiga | `smoke` |
| CALC-11 | Histórico vazio avisa o usuário | |
| CONV-01 | O conversor lista Comprimento, Massa e Temperatura | |
| CONV-02 | Temperatura abre em Celsius → Kelvin: 100 °C = 373,15 K | `smoke` |
| CONV-03 | Celsius → Fahrenheit: 0, 100, 37 e −40 °C (4 casos) | |
| CONV-04 | Inverter troca as unidades de lugar | |
| CONV-05 | Unidades padrão: km → m e libra → kg (3 casos) | |

---

## Como rodar no computador (Windows)

O passo a passo de instalação está em [Instalação leve](#instalação-leve-sem-android-studio). Com tudo instalado:

```bash
# Terminal 1: abrir o celular virtual
emulator -avd Pixel_API_34 -memory 2048 -no-snapshot-save

# Terminal 2: iniciar o Appium
appium

# Terminal 3: rodar os testes (o app é baixado sozinho na primeira vez)
pip install -r requirements.txt
pytest -v
```

Relatório: `reports\report.html`.

| Comando | O que faz |
|---|---|
| `pytest -v` | Roda todos os testes. Você vê o app sendo usado no emulador |
| `pytest -v -m smoke` | Só os cenários críticos |
| `pytest -v -m conversor` | Só o conversor de unidades |
| `pytest -v --gravar-video` | Grava o vídeo de cada teste em `reports\videos` |

### Instalação leve (sem Android Studio)

Em vez do Android Studio completo (15 GB), o projeto usa só as ferramentas de linha de comando do Android e um emulador sem Play Store (cerca de 5 GB).

1. Ative **Plataforma do Hipervisor do Windows** em "Ativar ou desativar recursos do Windows".
2. Baixe as **Command line tools only** em https://developer.android.com/studio e extraia em `C:\android\cmdline-tools\latest`.
3. Crie a variável `ANDROID_HOME=C:\android` e adicione ao PATH: `C:\android\platform-tools`, `C:\android\emulator` e `C:\android\cmdline-tools\latest\bin`.
4. Instale o emulador e a imagem do Android 14:
   ```bash
   sdkmanager "platform-tools" "emulator" "system-images;android-34;default;x86_64"
   avdmanager create avd -n Pixel_API_34 -k "system-images;android-34;default;x86_64" -d pixel_5
   ```
5. Instale o Appium: `npm install -g appium` e `appium driver install uiautomator2`.

---

## Estrutura

```
pages/                   Page Objects: calculadora, histórico e conversor
tests/                   cenários da calculadora e do conversor
utils/numeros.py         converte "1.234,5" (formato brasileiro) em número
conftest.py              sessão Appium, download do app, app limpo por teste, print e vídeo
scripts/rodar-ci.sh      sobe o Appium e roda os testes dentro do emulador do CI
.github/workflows/       CI com emulador Android e relatório no GitHub Pages
```

---

## Decisões técnicas

| Decisão | Por quê |
|---|---|
| **App real e de código aberto** | O código-fonte público permitiu levantar os ids de cada botão e as regras de cálculo antes de automatizar, sem adivinhar seletores |
| **APK oficial baixado e conferido por hash** (SHA-256) | O repositório não guarda binário de terceiros. O teste baixa a versão 1.4.0 da página oficial de releases e confere que é exatamente esse arquivo |
| **Tela de abertura informada na configuração** (`appActivity`) | O app tem um atalho de abertura para cada cor de ícone que o usuário pode escolher. Na primeira execução, o Appium não conseguiu decidir qual abrir (`Intent matches multiple activities`). A configuração aponta o atalho padrão, o verde |
| **Zerar com toque longo** (`mobile: longClickGesture`) | O código do app tem um botão AC, mas ele fica escondido com o celular em pé. Para o usuário, zerar é segurar o botão C. O teste reproduz o gesto real em vez de procurar um botão que não aparece |
| **Porcentagem como o usuário usa** | Na calculadora, `%` aplica a porcentagem sobre a conta em andamento: 200 × 15% = 30 e 200 + 15% = 230. Os casos seguem esse uso, conferido na execução |
| **Celular em português do Brasil** (`language` e `locale`) | Os testes validam a formatação que o usuário brasileiro vê: vírgula decimal, ponto no milhar e mensagens traduzidas |
| **Comparação numérica, não de texto** (`para_decimal`) | "12,5" vira 12.5 antes de comparar. Os testes de regra não quebram por formatação; a formatação tem testes próprios (CALC-03 e CALC-04) |
| **App limpo antes de cada teste** (`mobile: clearApp`) | Histórico e unidades escolhidas ficam salvos no app. Limpar os dados deixa cada teste independente, sem reinstalar o app |
| **Uma sessão Appium para todos os testes** | Abrir sessão é o passo mais lento. Uma sessão só, com o app limpo a cada teste, deixa a suíte rápida sem perder isolamento |
| **Page Objects e seletores por id** | `org.fossify.math:id/btn_7` não muda com idioma nem com layout. Texto só é usado onde ele é o próprio requisito (nome da conversão e da unidade) |
| **Esperas explícitas** (`WebDriverWait`) | Nenhuma pausa fixa no código |
| **Leitura de toast** | Mensagens rápidas do Android ("Erro: divisão por zero", "O histórico está vazio") são verificadas pelo UiAutomator2 |
| **Testes orientados a dados** (`parametrize`) | Um cenário, vários casos, cada um com nome próprio no relatório |
| **Vídeo de cada teste no CI** | O GitHub Actions roda sem tela. O vídeo mostra o que aconteceu no celular, junto do print da falha |
| **Emulador com KVM no CI** | O emulador roda com aceleração de hardware no GitHub Actions, sem serviço pago de nuvem de dispositivos |

## Limitações

- Testes em emulador. Em um projeto real, a suíte rodaria também em aparelhos físicos ou em uma nuvem de dispositivos.
- Uma versão do Android (14). Uma matriz de versões no CI ampliaria a cobertura.

## Próximos passos

- Matriz de versões do Android no CI (API 29, 31 e 34).
- Testes do widget da calculadora na tela inicial.
- Testes de acessibilidade (tamanho de toque e descrição dos botões).
