"""Conversor de unidades: regras de conversão, unidades padrão e troca de unidades."""
from decimal import Decimal

import pytest

from utils.numeros import para_decimal

pytestmark = pytest.mark.conversor


def test_conv01_lista_os_tipos_de_conversao(calculadora):
    tipos = calculadora.abrir_conversor().tipos()
    assert {"Comprimento", "Massa", "Temperatura"} <= set(tipos)


@pytest.mark.smoke
def test_conv02_temperatura_abre_em_celsius_para_kelvin(calculadora):
    conversor = calculadora.abrir_conversor().escolher("Temperatura")
    conversor.digitar("100")
    assert conversor.unidades() == ("Celsius", "Kelvin")
    assert para_decimal(conversor.valor_destino()) == Decimal("373.15")


@pytest.mark.parametrize(
    "celsius, fahrenheit",
    [
        pytest.param("0", Decimal("32"), id="congelamento-da-agua"),
        pytest.param("100", Decimal("212"), id="ebulicao-da-agua"),
        pytest.param("37", Decimal("98.6"), id="corpo-humano"),
        pytest.param("40±", Decimal("-40"), id="menos-40-e-igual-nas-duas-escalas"),
    ],
)
def test_conv03_celsius_para_fahrenheit(calculadora, celsius, fahrenheit):
    conversor = calculadora.abrir_conversor().escolher("Temperatura")
    conversor.escolher_unidade_destino("Fahrenheit")
    conversor.digitar(celsius)
    assert para_decimal(conversor.valor_destino()) == fahrenheit


def test_conv04_inverter_troca_as_unidades_de_lugar(calculadora):
    conversor = calculadora.abrir_conversor().escolher("Temperatura")
    origem, destino = conversor.unidades()
    conversor.inverter()
    assert conversor.unidades() == (destino, origem)


@pytest.mark.parametrize(
    "tipo, valor, unidades, esperado",
    [
        pytest.param("Comprimento", "1", ("Quilômetro", "Metro"), Decimal("1000"), id="1-km-em-metros"),
        pytest.param("Comprimento", "2,5", ("Quilômetro", "Metro"), Decimal("2500"), id="2,5-km-em-metros"),
        pytest.param("Massa", "1", ("Libra", "Quilograma"), Decimal("0.45359237"), id="1-libra-em-kg"),
    ],
)
def test_conv05_conversoes_com_unidades_padrao(calculadora, tipo, valor, unidades, esperado):
    conversor = calculadora.abrir_conversor().escolher(tipo)
    conversor.digitar(valor)
    assert conversor.unidades() == unidades
    assert para_decimal(conversor.valor_destino()) == esperado
