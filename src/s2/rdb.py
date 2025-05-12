from src.s2.connection import supabase

def verificar_dado_medico(crm):
    try:
        response = supabase.table("medico").select("crm", "nome").eq("crm", crm).execute()
        if response.data:
            nome_medico = response.data[0]['nome']
            auditoria = f"Medico: {nome_medico} (CRM: {crm}) existe no sistema"
            retorno = "CRM cadastrado no sistema"
            return True, retorno, auditoria
        else:
            retorno = f"Não existe no sistema com o CRM: {crm}"
            #print(mensagem)
            auditoria = retorno
            return False, retorno, auditoria
    except Exception as e:
        print(f"Erro ao verificar dado no banco de dados: {str(e)}")
        return False, str(e)

def inserir_dado_medico(dados):
    try:
        response = supabase.table("medico").insert(dados).execute()
        if response.data:
            retorno = f"Médico {dados['nome']} cadastrado com sucesso"
            #print(mensagem)
            auditoria = retorno
            return True, retorno, auditoria
        else:
            retorno = f"Erro ao inserir: {response.error}"
            #print(mensagem)
            auditoria = retorno
            return False, retorno, auditoria
    except Exception as e:
        retorno = f"Erro ao inserir dado no banco de dados: {str(e)}"
        #print(mensagem)
        auditoria = retorno
        return False, retorno, auditoria

def remover_dado_medico(crm):
    try:
        consulta_response = supabase.table("medico").select("nome").eq("crm", crm).execute()
        delete_response = supabase.table("medico").delete().eq("crm", crm).execute()
        if delete_response.data and consulta_response:
            retorno = f"Médico {consulta_response} deletado com sucesso"
            auditoria = retorno
            #print(mensagem)
            return True, retorno, auditoria
        else:
            retorno = f"Erro ao deletar: {delete_response.error}"
            auditoria = retorno
            #print(mensagem)
            return False, retorno, auditoria
    except Exception as e:
        retorno = f"Erro ao deletar dado no banco de dados: {str(e)}"
        auditoria = retorno
        #print(mensagem)
        return False, retorno, auditoria

def consultar_dado_medico(crm):
    try:
        consulta_response = supabase.table("medico").select("*").eq("crm", crm).execute()
        if consulta_response.data:
            linha = consulta_response.data[0]
            crm = linha['crm']
            nome = linha['nome']
            especialidade = linha['especializacao']
            retorno = (f"Nome: {nome} \nCRM: {crm} \nEspecialização: {especialidade}")
            auditoria = f"Médico {nome} consultado com sucesso"
            #print(mensagem)
            return True, retorno, auditoria
        else:
            retorno = f"Erro ao consultar: {consulta_response.error}"
            auditoria = retorno
            return False, retorno, auditoria
    except Exception as e:
        retorno = f"Erro ao consultar dado no banco de dados: {str(e)}"
        auditoria = retorno
        return False, retorno, auditoria

def listar_dado_medico():
    try:
        consulta_response = supabase.table("medico").select("*").execute()
        retornos = []
        if consulta_response.data:
            for linha in consulta_response.data:
                crm = linha['crm']
                nome = linha['nome']
                especialidade = linha['especializacao']
                retorno = (f"---------------\nNome: {nome} \nCRM: {crm} \nEspecialização: {especialidade}\n---------------\n")
                retornos.append(retorno)  # Adiciona cada mensagem à lista
            auditoria = "Foi possível ver uma lista com todos os médicos cadastrados"
            return True, "\n".join(retornos), auditoria  # Retorna todas as mensagens de uma vez
        else:
            retorno = f"Erro ao listar: {consulta_response.error}"
            auditoria = retorno
            #print(mensagem)
            return False, retorno, auditoria
    except Exception as e:
        retorno = f"Erro ao listar dado no banco de dados: {str(e)}"
        #print(mensagem)
        auditoria = retorno
        return False, retorno, auditoria