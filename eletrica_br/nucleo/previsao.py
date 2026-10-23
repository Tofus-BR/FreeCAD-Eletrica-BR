"""Previsão mínima de iluminação e de tomadas de uso geral (TUG) por cômodo de habitação.

Fonte: ABNT NBR 5410:2004, 9.5.2 (iluminação em 9.5.2.1, tomadas em 9.5.2.2), conferida com
H. Creder, Instalações Elétricas, 16ª ed., seções 3.3.2 e 3.3.3.
A norma admite reduzir a potência das TUG quando o conjunto de áreas molhadas passa de seis
pontos; aqui essa redução não é aplicada, o que fica sempre do lado da segurança.
"""

from dataclasses import dataclass
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal
from enum import Enum

FONTE_ILUMINACAO = "NBR 5410:2004 9.5.2.1"
FONTE_QTD_TUG = "NBR 5410:2004 9.5.2.2.1"
FONTE_POTENCIA_TUG = "NBR 5410:2004 9.5.2.2.2"

ILUMINACAO_BASE_VA = 100
ILUMINACAO_AREA_BASE_M2 = Decimal(6)
ILUMINACAO_ACRESCIMO_VA = 60
ILUMINACAO_PASSO_M2 = Decimal(4)

PERIMETRO_POR_TUG_AREA_MOLHADA_M = Decimal("3.5")
PERIMETRO_POR_TUG_M = Decimal(5)
AREA_MAX_OUTRO_COM_UMA_TUG_M2 = Decimal(6)

TUG_AREA_MOLHADA_VA = 600
TUG_AREA_MOLHADA_QTD_MAX = 3
TUG_VA = 100


class TipoComodo(Enum):
    BANHEIRO = "banheiro"
    COZINHA_SERVICO = "cozinha, copa, área de serviço ou lavanderia"
    VARANDA = "varanda"
    SALA_DORMITORIO = "sala ou dormitório"
    OUTRO = "demais cômodos"


AREAS_MOLHADAS = frozenset({TipoComodo.BANHEIRO, TipoComodo.COZINHA_SERVICO})


@dataclass(frozen=True)
class Passo:
    descricao: str
    fonte: str


@dataclass(frozen=True)
class Resultado:
    valor: int
    unidade: str
    passos: tuple[Passo, ...]


@dataclass(frozen=True)
class Comodo:
    nome: str
    tipo: TipoComodo
    area_m2: float
    perimetro_m: float

    def __post_init__(self) -> None:
        _positivo(self.area_m2, "área (m²)")
        _positivo(self.perimetro_m, "perímetro (m)")


def _positivo(valor: float, campo: str) -> Decimal:
    numero = Decimal(str(valor))
    if not numero > 0:
        raise ValueError(f"{campo} deve ser maior que zero; recebido: {valor}")
    return numero


def _por_fracao(perimetro: Decimal, passo_m: Decimal) -> int:
    return int((perimetro / passo_m).to_integral_value(ROUND_CEILING))


def iluminacao_minima_va(area_m2: float) -> Resultado:
    """Carga mínima de iluminação do cômodo, em VA, pela área."""
    area = _positivo(area_m2, "área (m²)")
    if area <= ILUMINACAO_AREA_BASE_M2:
        passo = f"área {area} m² ≤ 6 m²: {ILUMINACAO_BASE_VA} VA"
        return Resultado(ILUMINACAO_BASE_VA, "VA", (Passo(passo, FONTE_ILUMINACAO),))
    inteiros = int(((area - ILUMINACAO_AREA_BASE_M2) / ILUMINACAO_PASSO_M2).to_integral_value(ROUND_FLOOR))
    total = ILUMINACAO_BASE_VA + inteiros * ILUMINACAO_ACRESCIMO_VA
    passo = (
        f"área {area} m² = 6 m² + {inteiros} × 4 m² inteiros + resto: "
        f"{ILUMINACAO_BASE_VA} + {inteiros} × {ILUMINACAO_ACRESCIMO_VA} = {total} VA"
    )
    return Resultado(total, "VA", (Passo(passo, FONTE_ILUMINACAO),))


def tomadas_minimas(comodo: Comodo) -> Resultado:
    """Quantidade mínima de pontos de TUG do cômodo."""
    perimetro = Decimal(str(comodo.perimetro_m))
    area = Decimal(str(comodo.area_m2))
    tipo = comodo.tipo
    if tipo in {TipoComodo.BANHEIRO, TipoComodo.VARANDA}:
        qtd, regra = 1, f"{tipo.value}: pelo menos 1 ponto"
    elif tipo is TipoComodo.COZINHA_SERVICO:
        qtd = _por_fracao(perimetro, PERIMETRO_POR_TUG_AREA_MOLHADA_M)
        regra = f"1 ponto a cada 3,5 m ou fração de perímetro: {perimetro} m → {qtd}"
    elif tipo is TipoComodo.OUTRO and area <= AREA_MAX_OUTRO_COM_UMA_TUG_M2:
        qtd, regra = 1, f"área {area} m² ≤ 6 m²: pelo menos 1 ponto"
    else:
        qtd = _por_fracao(perimetro, PERIMETRO_POR_TUG_M)
        regra = f"1 ponto a cada 5 m ou fração de perímetro: {perimetro} m → {qtd}"
    return Resultado(qtd, "pontos", (Passo(f"{comodo.nome}: {regra}", FONTE_QTD_TUG),))


def potencia_tug_va(tipo: TipoComodo, quantidade: int) -> Resultado:
    """Potência mínima do conjunto de TUG de um cômodo, em VA."""
    if quantidade < 0:
        raise ValueError(f"quantidade de tomadas não pode ser negativa; recebido: {quantidade}")
    if tipo in AREAS_MOLHADAS:
        cheias = min(quantidade, TUG_AREA_MOLHADA_QTD_MAX)
        demais = quantidade - cheias
        total = cheias * TUG_AREA_MOLHADA_VA + demais * TUG_VA
        regra = f"{cheias} × {TUG_AREA_MOLHADA_VA} VA + {demais} × {TUG_VA} VA = {total} VA"
    else:
        total = quantidade * TUG_VA
        regra = f"{quantidade} × {TUG_VA} VA = {total} VA"
    return Resultado(total, "VA", (Passo(f"{tipo.value}: {regra}", FONTE_POTENCIA_TUG),))
