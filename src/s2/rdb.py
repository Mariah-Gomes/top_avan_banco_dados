from src.s2.connection import supabase

def inserir_dado_medico(dados):
    try:
        response = supabase.table("medico").insert(dados).execute()
        if response.data:
            print("Inserção realizada com sucesso")
            return True
        else:
            print("Erro ao inserir:", response.error)
            return False

    except Exception as e:
        print(f"Erro ao inserir dado no banco de dados: {str(e)}")
        return False
