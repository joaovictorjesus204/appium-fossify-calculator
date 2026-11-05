"""Conversão dos números exibidos pelo app (formato brasileiro) para Decimal."""
from decimal import Decimal


def para_decimal(texto: str) -> Decimal:
    """'1.234,5' -> Decimal('1234.5'); '−15' -> Decimal('-15')."""
    limpo = (
        texto.strip()
        .replace("−", "-")   # sinal de menos tipográfico
        .replace(" ", "")    # espaço não separável
        .replace(".", "")         # separador de milhar
        .replace(",", ".")        # vírgula decimal
    )
    return Decimal(limpo)
