# Configuration settings\nimport os\n\nclass Settings:\n    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./test.db')\n\nsettings = Settings() 
