from src.s2.connection import supabase

def inserir_dado_medico(dados):
    resultado = supabase.table("medico").insert(dados).execute()
    return resultado
