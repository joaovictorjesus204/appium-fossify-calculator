from appium.webdriver.common.appiumby import AppiumBy

from pages.base import PACOTE, BasePage, por_id


class SeletorDeConversorPage(BasePage):
    """Tela que lista os tipos de conversão (Temperatura, Comprimento, Massa...)."""

    def carregar(self):
        self.esperar(por_id("unit_label"))
        return self

    def tipos(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(*por_id("unit_label"))]

    def escolher(self, tipo: str) -> "ConversorPage":
        self.tocar((AppiumBy.XPATH, f"//*[@resource-id='{PACOTE}:id/unit_label' and @text='{tipo}']"))
        return ConversorPage(self.driver).carregar()


class ConversorPage(BasePage):
    VALOR_ORIGEM = por_id("top_unit_text")
    VALOR_DESTINO = por_id("bottom_unit_text")
    UNIDADE_ORIGEM = por_id("top_unit_name")
    UNIDADE_DESTINO = por_id("bottom_unit_name")
    INVERTER = por_id("swap_button")

    BOTOES = {
        **{str(n): f"btn_{n}" for n in range(10)},
        ",": "btn_decimal",
        "±": "btn_plus_minus",
    }

    def carregar(self):
        self.esperar(self.VALOR_ORIGEM)
        return self

    def digitar(self, valor: str):
        """Digita o valor no teclado do conversor. Use '±' no fim para tornar negativo."""
        for simbolo in valor:
            self.tocar(por_id(self.BOTOES[simbolo]))
        return self

    def escolher_unidade_destino(self, nome: str):
        self.tocar(self.UNIDADE_DESTINO)
        self.tocar((AppiumBy.XPATH, f"//android.widget.RadioButton[starts-with(@text, '{nome}')]"))
        return self

    def inverter(self):
        self.tocar(self.INVERTER)
        return self

    def valor_origem(self) -> str:
        return self.texto(self.VALOR_ORIGEM)

    def valor_destino(self) -> str:
        return self.texto(self.VALOR_DESTINO)

    def unidades(self) -> tuple[str, str]:
        return self.texto(self.UNIDADE_ORIGEM), self.texto(self.UNIDADE_DESTINO)
