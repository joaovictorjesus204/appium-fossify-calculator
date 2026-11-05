from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PACOTE = "org.fossify.math"


def por_id(nome: str):
    return (AppiumBy.ID, f"{PACOTE}:id/{nome}")


class BasePage:
    TEMPO_ESPERA = 15

    def __init__(self, driver):
        self.driver = driver

    def esperar(self, localizador, tempo=None):
        return WebDriverWait(self.driver, tempo or self.TEMPO_ESPERA).until(
            EC.presence_of_element_located(localizador)
        )

    def tocar(self, localizador):
        WebDriverWait(self.driver, self.TEMPO_ESPERA).until(
            EC.element_to_be_clickable(localizador)
        ).click()

    def texto(self, localizador) -> str:
        return self.esperar(localizador).text

    def ler_toast(self, tempo=5) -> str:
        """Lê a mensagem rápida (toast) que o Android mostra na parte de baixo da tela."""
        toast = WebDriverWait(self.driver, tempo, poll_frequency=0.2).until(
            EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.Toast"))
        )
        return toast.get_attribute("text") or toast.get_attribute("name") or ""
