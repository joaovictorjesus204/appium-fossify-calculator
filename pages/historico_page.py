from pages.base import BasePage, por_id


class HistoricoPage(BasePage):
    LISTA = por_id("history_list")
    FORMULAS = por_id("item_formula")
    RESULTADOS = por_id("item_result")

    def carregar(self):
        self.esperar(self.LISTA)
        return self

    def itens(self) -> list[tuple[str, str]]:
        """Lista de (fórmula, resultado), do mais recente para o mais antigo."""
        formulas = [e.text for e in self.driver.find_elements(*self.FORMULAS)]
        resultados = [e.text for e in self.driver.find_elements(*self.RESULTADOS)]
        return list(zip(formulas, resultados))
