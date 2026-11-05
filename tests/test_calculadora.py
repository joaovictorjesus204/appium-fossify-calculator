"""Calculadora: operações, regras de exibição em português do Brasil, erros e histórico."""
from decimal import Decimal

import pytest

from utils.numeros import para_decimal

pytestmark = pytest.mark.calculadora


@pytest.mark.smoke
def test_calc01_soma_simples(calculadora):
    assert calculadora.calcular("7+8") == "15"


@pytest.mark.parametrize(
    "expressao, esperado",
    [
        pytest.param("9×6", Decimal("54"), id="multiplicacao"),
        pytest.param("100÷8", Decimal("12.5"), id="divisao-com-decimal"),
        pytest.param("25-40", Decimal("-15"), id="subtracao-negativa"),
        pytest.param("2^10", Decimal("1024"), id="potencia"),
        pytest.param("√144", Decimal("12"), id="raiz-quadrada"),
        pytest.param("200×15%", Decimal("30"), id="porcentagem-de-um-valor"),
        pytest.param("200+15%", Decimal("230"), id="acrescimo-percentual"),
    ],
)
def test_calc02_operacoes(calculadora, expressao, esperado):
    assert para_decimal(calculadora.calcular(expressao)) == esperado


def test_calc03_soma_de_decimais_sem_erro_de_arredondamento(calculadora):
    # Em ponto flutuante, 0.1 + 0.2 = 0.30000000000000004. O app usa BigDecimal e deve mostrar 0,3.
    assert calculadora.calcular("0,1+0,2") == "0,3"


def test_calc04_resultado_com_separador_de_milhar_brasileiro(calculadora):
    assert calculadora.calcular("1234×1000") == "1.234.000"


def test_calc05_formula_mostra_a_conta_feita(calculadora):
    calculadora.calcular("9×6")
    assert calculadora.formula() == "9×6"


def test_calc06_divisao_por_zero_avisa_o_usuario(calculadora):
    calculadora.digitar("10÷0=")
    assert "divisão por zero" in calculadora.ler_toast().lower()


def test_calc07_apagar_remove_so_o_ultimo_digito(calculadora):
    calculadora.digitar("123").apagar_ultimo()
    assert calculadora.resultado() == "12"


def test_calc08_segurar_c_zera_resultado_e_formula(calculadora):
    calculadora.calcular("7+8")
    calculadora.zerar()
    assert calculadora.resultado() == "0"
    assert calculadora.formula() == ""


def test_calc09_resultado_continua_na_proxima_conta(calculadora):
    calculadora.calcular("7+8")
    assert calculadora.calcular("×2") == "30"


@pytest.mark.smoke
def test_calc10_historico_guarda_as_contas_da_mais_recente_para_a_mais_antiga(calculadora):
    calculadora.calcular("7+8")
    calculadora.zerar()
    calculadora.calcular("9×6")
    historico = calculadora.abrir_historico().itens()
    assert historico[:2] == [("9×6", "54"), ("7+8", "15")]


def test_calc11_historico_vazio_avisa_o_usuario(calculadora):
    # Cada teste começa com os dados do app limpos: o histórico não pode "vazar" de um teste para outro.
    calculadora.tocar(calculadora.HISTORICO)
    assert calculadora.ler_toast() == "O histórico está vazio"
