"""Testes dentro do FreeCAD, sem interface.

Uso: freecadcmd testes/freecad/rodar.py
Sai com código 1 se algum teste falhar (o relatório sai no terminal).
"""

import os
import sys
import unittest
from pathlib import Path

import FreeCAD

# O freecadcmd não põe a raiz do projeto no caminho de importação.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import eletrica_br


class TestPacoteNoFreeCAD(unittest.TestCase):
    def test_importa_dentro_do_freecad(self):
        self.assertTrue(eletrica_br.__version__)
        self.assertGreaterEqual(int(FreeCAD.Version()[0]), 1)


resultado = unittest.TextTestRunner(verbosity=2).run(
    unittest.defaultTestLoader.loadTestsFromTestCase(TestPacoteNoFreeCAD)
)
os._exit(0 if resultado.wasSuccessful() else 1)
