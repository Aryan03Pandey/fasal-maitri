# Neon Database Setup Guide

## Step 1: Get Your Neon Database Connection String

1. Log into your Neon dashboard at https://console.neon.tech
2. Select your project
3. Go to the "Connection Details" section
4. Copy the connection string that looks like this:
   ```
   postgresql://username:password@ep-something.region.aws.neon.tech/database_name?sslmode=require
   ```

## Step 2: Create Environment File

Create a `.env` file in the `backend/` directory with the following content:

```env
# Neon Database Configuration
# Replace with your actual Neon database URL from the console
NEON_DB_URL=postgresql://username:password@ep-something.region.aws.neon.tech/database_name?sslmode=require

# Database Pool Configuration
NEON_DB_POOL_SIZE=10
NEON_DB_MAX_OVERFLOW=20

# Other API Keys (replace with your actual keys)
HUGGINGFACE_TOKEN=your_huggingface_token_here
GEMINI_API_KEY=your_gemini_api_key_here
REDIS_URL=redis://localhost:6379

# Session Configuration
SESSION_TTL=3600
```

## Step 3: Update Connection String for Async Support

Since your project uses SQLAlchemy with async support, you need to modify the connection string. Replace `postgresql://` with `postgresql+asyncpg://` in your NEON_DB_URL:

```env
NEON_DB_URL=postgresql+asyncpg://username:password@ep-something.region.aws.neon.tech/database_name?sslmode=require
```

## Step 4: Test the Connection

Run your application to test the database connection:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

## Step 5: Create Database Tables

Your application will automatically create tables when it starts, but you can also run:

```python
from app.database import create_tables
import asyncio

asyncio.run(create_tables())
```

## Troubleshooting

1. **SSL Mode**: Make sure `sslmode=require` is included in your connection string
2. **Pool Size**: Adjust `NEON_DB_POOL_SIZE` and `NEON_DB_MAX_OVERFLOW` based on your needs
3. **Connection Issues**: Check that your IP is not blocked by Neon's firewall settings 