import os

class Settings:
    database_url: str = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://admin:NtxZCgSHUHwBAik5r5Ob@silo-dev-db.c0wteib2ljjz.ap-south-1.rds.amazonaws.com:3306/ecommerce'
    )

settings = Settings()
