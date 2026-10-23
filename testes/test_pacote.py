import importlib
import re

import eletrica_br


def test_versao_segue_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", eletrica_br.__version__)


def test_nucleo_nao_depende_do_freecad():
    nucleo = importlib.import_module("eletrica_br.nucleo")
    assert "FreeCAD" not in vars(nucleo)
