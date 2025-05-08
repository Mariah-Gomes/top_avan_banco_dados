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
        mensagem = f"Erro ao inserir dado no banco de dados: {str(e)}"
        print(mensagem)
        return False, mensagem
    
#def editar_dado_medico(crm):

def consultar_dado_medico(crm):
    try:
        consulta_response = supabase.table("medico").select("*").eq("crm", crm).execute()
        print(consulta_response)
        if consulta_response.data and len(consulta_response.data) > 0:
            linha = consulta_response.data[0]
            crm = linha['crm']
            nome = linha['nome']
            especialidade = linha['especializacao']
            mensagem = (f"Nome: {nome} \nCRM: {crm} \nEspecialização: {especialidade}")
            print(mensagem)
            return True, mensagem
        else:
            mensagem = f"Erro ao deletar: {consulta_response.error}"
            print(mensagem)
            return False, mensagem
    
    except Exception as e:
        mensagem = f"Erro ao inserir dado no banco de dados: {str(e)}"
        print(mensagem)
        return False, mensagem