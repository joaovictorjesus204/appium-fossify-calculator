"""Configuração da sessão Appium, do app e das evidências (print e vídeo)."""
import base64
import hashlib
import os
import pathlib
import re
import urllib.request

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

from pages.base import PACOTE
from pages.calculadora_page import CalculadoraPage

RAIZ = pathlib.Path(__file__).parent
PASTA_RELATORIO = RAIZ / "reports"

# App testado: Fossify Calculator 1.4.0, baixado da página oficial de releases do projeto.
# O hash garante que o arquivo é exatamente a versão publicada.
APK_URL = "https://github.com/FossifyOrg/Calculator/releases/download/1.4.0/calculator-10-foss-release.apk"
APK_SHA256 = "7c5443c22d6d62c67dfe80df33ea9161ff0fa440f92590bcb45d7008b57613ed"
APK = RAIZ / "apps" / "fossify-calculator-1.4.0.apk"


def _sha256(caminho: pathlib.Path) -> str:
    return hashlib.sha256(caminho.read_bytes()).hexdigest()


def baixar_apk() -> pathlib.Path:
    if APK.exists() and _sha256(APK) == APK_SHA256:
        return APK
    APK.parent.mkdir(exist_ok=True)
    print(f"Baixando o app de {APK_URL}")
    urllib.request.urlretrieve(APK_URL, APK)
    if _sha256(APK) != APK_SHA256:
        APK.unlink()
        raise RuntimeError("O APK baixado não confere com o hash esperado.")
    return APK


def pytest_addoption(parser):
    parser.addoption("--appium-url", default=os.getenv("APPIUM_URL", "http://127.0.0.1:4723"))
    parser.addoption(
        "--gravar-video",
        action="store_true",
        default=os.getenv("GRAVAR_VIDEO") == "1",
        help="Grava um vídeo da tela do celular em cada teste (reports/videos)",
    )


@pytest.fixture(scope="session")
def driver(request):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.app = str(baixar_apk())
    # O app tem um atalho de abertura para cada cor de ícone (activity-alias); o padrão é o verde.
    # Sem informar qual abrir, o Android não sabe qual atalho usar.
    options.set_capability("appium:appPackage", PACOTE)
    options.set_capability("appium:appActivity", "org.fossify.math.activities.SplashActivity.Green")
    options.set_capability("appium:appWaitActivity", "*")
    # Celular em português do Brasil: vírgula decimal e ponto no milhar.
    options.set_capability("appium:language", "pt")
    options.set_capability("appium:locale", "BR")
    options.set_capability("appium:newCommandTimeout", 180)
    options.set_capability("appium:disableWindowAnimation", True)
    options.set_capability("appium:uiautomator2ServerInstallTimeout", 120000)
    options.set_capability("appium:adbExecTimeout", 60000)

    sessao = webdriver.Remote(request.config.getoption("--appium-url"), options=options)
    # Não esperar o app "ficar ocioso" antes de cada comando: no emulador do CI, sem placa de vídeo,
    # essa espera estourava o tempo e o UiAutomator2 não conseguia ler a tela.
    sessao.update_settings({"waitForIdleTimeout": 0})
    yield sessao
    sessao.quit()


@pytest.fixture(autouse=True)
def app_limpo(driver, request):
    """Cada teste começa com o app recém-instalado: sem histórico e sem unidades salvas."""
    driver.execute_script("mobile: clearApp", {"appId": PACOTE})
    driver.activate_app(PACOTE)

    gravar = request.config.getoption("--gravar-video")
    if gravar:
        driver.start_recording_screen(timeLimit="180", videoSize="720x1280")
    yield
    if gravar:
        video = driver.stop_recording_screen()
        pasta = PASTA_RELATORIO / "videos"
        pasta.mkdir(parents=True, exist_ok=True)
        nome = re.sub(r"[^\w-]+", "_", request.node.name)[:80] + ".mp4"
        (pasta / nome).write_bytes(base64.b64decode(video))
        request.node.video = f"videos/{nome}"


@pytest.fixture
def calculadora(driver) -> CalculadoraPage:
    return CalculadoraPage(driver).carregar()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Anexa ao relatório HTML o print da tela (na falha) e o vídeo do teste (se gravado)."""
    resultado = yield
    relatorio = resultado.get_result()
    plugin = item.config.pluginmanager.getplugin("html")
    if plugin is None:
        return
    extras = getattr(relatorio, "extras", [])
    sessao = item.funcargs.get("driver")
    if relatorio.when == "call" and relatorio.failed and sessao is not None:
        extras.append(plugin.extras.png(sessao.get_screenshot_as_base64(), "Tela no momento da falha"))
    if relatorio.when == "teardown" and getattr(item, "video", None):
        extras.append(plugin.extras.url(item.video, name="Vídeo do teste"))
    relatorio.extras = extras
