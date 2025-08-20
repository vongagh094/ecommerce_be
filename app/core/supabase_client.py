from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        )

supabase_client = SupabaseClient().client