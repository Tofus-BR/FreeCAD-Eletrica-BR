"""Previsão de cargas (NBR 5410:2004 9.5.2).

Casos de referência:
- [UFV] GESEP/UFV, Aula 6 "Previsão de cargas", slide 27:
  https://gesep.ufv.br/wp-content/uploads/2021/07/Aula-6-previsaodecargas.pdf
- [VOLTIMUM] "Instalações elétricas em edifícios — NBR 5410", exemplos de iluminação e tomadas:
  https://content.voltimum.com/br/3054/02_ie11_instalaes_eltricas_edifcios_nbr-5410_0.pdf
"""

import pytest

from eletrica_br.nucleo.previsao import (
    Comodo,
    TipoComodo,
    iluminacao_minima_va,
    potencia_tug_va,
    tomadas_minimas,
)


def comodo(tipo, area=10.0, perimetro=13.0):
    return Comodo("teste", tipo, area, perimetro)


# Casos de referência publicados


def test_iluminacao_12m2_voltimum():
    assert iluminacao_minima_va(12).valor == 160


def test_sala_perimetro_16m_ufv():
    qtd = tomadas_minimas(comodo(TipoComodo.SALA_DORMITORIO, area=16, perimetro=16)).valor
    assert qtd == 4
    assert potencia_tug_va(TipoComodo.SALA_DORMITORIO, qtd).valor == 400


def test_cozinha_perimetro_14_5m_ufv():
    qtd = tomadas_minimas(comodo(TipoComodo.COZINHA_SERVICO, area=13, perimetro=14.5)).valor
    assert qtd == 5
    assert potencia_tug_va(TipoComodo.COZINHA_SERVICO, qtd).valor == 2000


def test_cozinha_5_pontos_voltimum():
    assert potencia_tug_va(TipoComodo.COZINHA_SERVICO, 5).valor == 2000


def test_quarto_5_pontos_voltimum():
    assert potencia_tug_va(TipoComodo.SALA_DORMITORIO, 5).valor == 500


# Bordas


@pytest.mark.parametrize(
    ("area", "va"),
    [(0.5, 100), (6, 100), (6.01, 100), (9.99, 100), (10, 160), (14, 220), (13.99, 160)],
)
def test_iluminacao_nas_bordas(area, va):
    assert iluminacao_minima_va(area).valor == va


@pytest.mark.parametrize(("perimetro", "qtd"), [(3.5, 1), (3.51, 2), (7.0, 2), (10.5, 3), (10.51, 4)])
def test_cozinha_por_fracao_de_3_5m(perimetro, qtd):
    assert tomadas_minimas(comodo(TipoComodo.COZINHA_SERVICO, perimetro=perimetro)).valor == qtd


@pytest.mark.parametrize(("perimetro", "qtd"), [(5, 1), (5.01, 2), (15, 3), (15.01, 4)])
def test_sala_por_fracao_de_5m(perimetro, qtd):
    assert tomadas_minimas(comodo(TipoComodo.SALA_DORMITORIO, perimetro=perimetro)).valor == qtd


@pytest.mark.parametrize(
    ("area", "perimetro", "qtd"), [(2.0, 5.7, 1), (6, 10, 1), (6.01, 10, 2), (12, 14, 3)]
)
def test_demais_comodos(area, perimetro, qtd):
    assert tomadas_minimas(comodo(TipoComodo.OUTRO, area=area, perimetro=perimetro)).valor == qtd


@pytest.mark.parametrize("tipo", [TipoComodo.BANHEIRO, TipoComodo.VARANDA])
def test_banheiro_e_varanda_um_ponto_mesmo_grandes(tipo):
    assert tomadas_minimas(comodo(tipo, area=30, perimetro=22)).valor == 1


def test_banheiro_um_ponto_de_600va():
    assert potencia_tug_va(TipoComodo.BANHEIRO, 1).valor == 600


@pytest.mark.parametrize(("qtd", "va"), [(0, 0), (1, 600), (3, 1800), (4, 1900), (7, 2200)])
def test_area_molhada_600va_ate_tres_pontos(qtd, va):
    assert potencia_tug_va(TipoComodo.COZINHA_SERVICO, qtd).valor == va


# Invariantes


def test_iluminacao_nunca_diminui_com_a_area():
    valores = [iluminacao_minima_va(a / 10).valor for a in range(1, 400)]
    assert valores == sorted(valores)


@pytest.mark.parametrize("tipo", list(TipoComodo))
def test_tomadas_nunca_diminuem_com_o_perimetro(tipo):
    valores = [tomadas_minimas(comodo(tipo, area=20, perimetro=p / 10)).valor for p in range(10, 400)]
    assert valores == sorted(valores)
    assert min(valores) >= 1


def test_resultado_explica_o_calculo_com_a_fonte():
    passo = iluminacao_minima_va(12).passos[0]
    assert "160 VA" in passo.descricao
    assert passo.fonte.startswith("NBR 5410")


# Entradas inválidas


@pytest.mark.parametrize("area", [0, -1])
def test_area_invalida(area):
    with pytest.raises(ValueError, match="área"):
        iluminacao_minima_va(area)


@pytest.mark.parametrize(("area", "perimetro"), [(0, 10), (10, 0), (-2, 10)])
def test_comodo_invalido(area, perimetro):
    with pytest.raises(ValueError):
        Comodo("x", TipoComodo.SALA_DORMITORIO, area, perimetro)


def test_quantidade_negativa():
    with pytest.raises(ValueError, match="negativa"):
        potencia_tug_va(TipoComodo.SALA_DORMITORIO, -1)
