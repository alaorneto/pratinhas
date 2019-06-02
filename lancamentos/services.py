from .models import Conta, Journal, Lancamento


def criar_lancamentos(usuario, mes, ano):
    # localiza todos os journals do usuario que sejam de tempo indeterminado
    # para cada journal, atualizar até o mes/ano indicado e salvar
    pass


def atualizar_journals(data_limite):
    pass


def excluir_journal(journal):
    if not journal.lancamento_set:
        pass