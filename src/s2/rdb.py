from src.s2.connection import supabase

def verificar_dado_medico(crm):
    try:
        response = supabase.table("medico").select("crm").eq("crm", crm).execute()
        if response.data:
            mensagem = "Existe no sistema"
            print(mensagem)
            return True, mensagem
        else:
            mensagem = "Não existe no sistema"
            print(mensagem)
            return False, mensagem
    except Exception as e:
        print(f"Erro ao verificar dado no banco de dados: {str(e)}")
        return False, mensagem

def inserir_dado_medico(dados):
    try:
        response = supabase.table("medico").insert(dados).execute()
        if response.data:
            mensagem = "Médico cadastrado com sucesso"
            print(mensagem)
            return True, mensagem
        else:
            mensagem = f"Erro ao inserir: {response.error}"
            print(mensagem)
            return False, mensagem
    except Exception as e:
        mensagem = f"Erro ao inserir dado no banco de dados: {str(e)}"
        print(mensagem)
        return False, mensagem

def remover_dado_medico(crm):
    try:
        delete_response = supabase.table("medico").delete().eq("crm", crm).execute()
        if delete_response.data:
            mensagem = "Médico deletado com sucesso"
            print(mensagem)
            return True, mensagem
        else:
            mensagem = f"Erro ao deletar: {delete_response.error}"
            print(mensagem)
            return False, mensagem
    
    except Exception as e:
        mensagem = f"Erro ao deletar dado no banco de dados: {str(e)}"
        print(mensagem)
        return False, mensagem
    
#def editar_dado_medico(crm):

def consultar_dado_medico(crm):
    try:
        consulta_response = supabase.table("medico").select("*").eq("crm", crm).execute()
        if consulta_response.data:
            linha = consulta_response.data[0]
            crm = linha['crm']
            nome = linha['nome']
            especialidade = linha['especializacao']
            mensagem = (f"Nome: {nome} \nCRM: {crm} \nEspecialização: {especialidade}")
            print(mensagem)
            return True, mensagem
        else:
            mensagem = f"Erro ao consultar: {consulta_response.error}"
            print(mensagem)
            return False, mensagem
    
    except Exception as e:
        mensagem = f"Erro ao consultar dado no banco de dados: {str(e)}"
        print(mensagem)
        return False, mensagem
    
def listar_dado_medico():
    try:
        consulta_response = supabase.table("medico").select("*").execute()
        mensagens = []
        if consulta_response.data:
            for linha in consulta_response.data:
                crm = linha['crm']
                nome = linha['nome']
                especialidade = linha['especializacao']
                mensagem = (f"---------------\nNome: {nome} \nCRM: {crm} \nEspecialização: {especialidade}\n---------------\n")
                mensagens.append(mensagem)  # Adiciona cada mensagem à lista
            return True, "\n".join(mensagens)  # Retorna todas as mensagens de uma vez
        else:
            mensagem = f"Erro ao listar: {consulta_response.error}"
            print(mensagem)
            return False, mensagem
        
    except Exception as e:
        mensagem = f"Erro ao listar dado no banco de dados: {str(e)}"
        print(mensagem)
        return False, mensagem
        