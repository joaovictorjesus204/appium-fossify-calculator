from appium.webdriver.common.appiumby import AppiumBy

from pages.base import BasePage, por_id
from pages.conversor_page import SeletorDeConversorPage
from pages.historico_page import HistoricoPage


class CalculadoraPage(BasePage):
    RESULTADO = por_id("result")
    FORMULA = por_id("formula")
    HISTORICO = por_id("history")
    CONVERSOR = por_id("unit_converter")

    # Cada símbolo da expressão corresponde a um botão do teclado do app.
    BOTOES = {
        **{str(n): f"btn_{n}" for n in range(10)},
        ",": "btn_decimal",
        "+": "btn_plus",
        "-": "btn_minus",
        "×": "btn_multiply",
        "÷": "btn_divide",
        "%": "btn_percent",
        "^": "btn_power",
        "√": "btn_root",
        "=": "btn_equals",
        "C": "btn_clear",
    }

    def carregar(self):
        self.esperar(self.RESULTADO, tempo=30)
        return self

    def digitar(self, sequencia: str):
        for simbolo in sequencia:
            self.tocar(por_id(self.BOTOES[simbolo]))
        return self

    def calcular(self, expressao: str) -> str:
        self.digitar(expressao + "=")
        return self.resultado()

    def apagar_ultimo(self):
        self.tocar(por_id("btn_clear"))
        return self

    def zerar(self):
        """Na tela em pé, o botão AC fica escondido: zerar é segurar o botão C."""
        botao = self.esperar(por_id("btn_clear"))
        self.driver.execute_script("mobile: longClickGesture", {"elementId": botao.id, "duration": 1000})
        return self

    def resultado(self) -> str:
        return self.texto(self.RESULTADO)

    def formula(self) -> str:
        return self.texto(self.FORMULA)

    def abrir_historico(self) -> HistoricoPage:
        self.tocar(self.HISTORICO)
        return HistoricoPage(self.driver).carregar()

    def abrir_conversor(self) -> SeletorDeConversorPage:
        self.tocar(self.CONVERSOR)
        return SeletorDeConversorPage(self.driver).carregar()
