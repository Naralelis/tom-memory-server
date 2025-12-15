import json
import os
import unittest
from unittest.mock import patch

import codex_engine
from call_llm import call_llm
from codex_engine import LeadInput


class EngineLLMIntegrationTests(unittest.TestCase):
    def test_local_steps_do_not_call_llm_without_generation(self):
        lead_input = LeadInput(texto_usuario="Quanto custa?", usuario_clicou_em_fazer_analise=True)

        with patch("codex_engine.call_llm") as mock_llm:
            context = codex_engine.normalizarEntrada(lead_input)
            intencao = codex_engine.detectarIntencao(context)
            perfil = codex_engine.detectarPerfil(context)
            modelo = codex_engine.selecionarModelo(intencao)
            codex_engine.construirPreenchimentos(modelo, context.mensagem_cliente)

            mock_llm.assert_not_called()
            self.assertEqual(intencao, "preco")
            self.assertIn(perfil, {"direto", "informal", "cauteloso", "tecnico"})

    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_does_not_break_local_steps(self):
        lead_input = LeadInput(texto_usuario="Quero detalhes do serviço", usuario_clicou_em_fazer_analise=True)

        context = codex_engine.normalizarEntrada(lead_input)
        intencao = codex_engine.detectarIntencao(context)
        perfil = codex_engine.detectarPerfil(context)
        modelo = codex_engine.selecionarModelo(intencao)
        prompt = codex_engine.montarPromptFinal(modelo, context.mensagem_cliente, codex_engine.CONTRATO_COGNITIVO)

        self.assertTrue(prompt)
        self.assertEqual(intencao, "detalhes")
        self.assertIn(perfil, {"direto", "informal", "cauteloso", "tecnico"})

    @patch.dict(os.environ, {}, clear=True)
    def test_call_llm_raises_without_api_key(self):
        with self.assertRaisesRegex(RuntimeError, "OPENAI_API_KEY environment variable is not set"):
            call_llm("prompt", "gpt-4.1-mini")

    def test_call_llm_called_once_per_analysis_with_api_key(self):
        lead_input = LeadInput(texto_usuario="Quanto custa esse serviço?", usuario_clicou_em_fazer_analise=True)

        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch("codex_engine.call_llm") as mock_llm:
                mock_llm.return_value = json.dumps(
                    {"curta": "Os valores começam em faixa X.\nEm seguida, posso explicar como aplicamos isso.",
                     "completa": "Os valores começam em faixa X e variam.\nEm seguida, posso explicar como aplicamos isso."}
                )

                resultado = codex_engine.executarAnalise(lead_input)

                mock_llm.assert_called_once()
                self.assertEqual(resultado.intencao, "preco")
                self.assertTrue(resultado.resposta_curta)
                self.assertTrue(resultado.resposta_completa)


if __name__ == "__main__":
    unittest.main()
