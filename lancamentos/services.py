import calendar, datetime

from .models import Conta, Journal, Lancamento


def atualizar_journals(usuario, mes, ano):
    # localiza todos os journals do usuario que sejam de tempo indeterminado
    # para cada journal, atualizar até o mes/ano indicado e salvar
    atualizar_ate = datetime.date(ano, mes, calendar.monthrange(ano, mes)[-1])
    
    journals_para_atualizar = Journal.objects.proprietario(usuario).filter(tempo_indeterminado=True).filter(ultima_atualizacao__lt=atualizar_ate)
    
    for journal in journals_para_atualizar:
        journal.atualizar(atualizar_ate)


def excluir_journal(journal):
    if not journal.lancamento_set:
        pass