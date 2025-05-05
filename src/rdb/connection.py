import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente:
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Cria a conexão com o Supabase:
supabase: Client = create_client(supabase_url, supabase_key)