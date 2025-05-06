from src.s2.connection import supabase

def inserir_dado_medico(dados):
    try:
        response = supabase.table('medicos').insert(dados).execute()
        if response.status_code == 201:  # Se a inserção for bem-sucedida
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao inserir dado no banco de dados: {e}")
        return False
