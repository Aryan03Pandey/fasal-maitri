import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from app.models import Base, User, AgriculturalData

# Load environment variables
load_dotenv("../.env")  # Fix path to point to root directory

async def insert_test_data(session: AsyncSession):
    """Insert test data into the database"""
    try:
        print("📝 Inserting test data...")
        
        # Create test users
        user1 = User(
            phone_number="+919876543244",
            name="Rahul Kumar",
            language="hi",
            location="Punjab, India"
        )
        
        user2 = User(
            phone_number="+919876543223",
            name="Priya Sharma",
            language="en",
            location="Karnataka, India"
        )
        
        session.add_all([user1, user2])
        await session.flush()  # Flush to get IDs
        
        # Create test agricultural data
        agri_data1 = AgriculturalData(
            user_id=user1.id,
            crop_type="Wheat"
        )
        
        agri_data2 = AgriculturalData(
            user_id=user2.id,
            crop_type="Tomatoes"
        )
        
        session.add_all([agri_data1, agri_data2])
        
        await session.commit()
        print("✅ Test data inserted successfully!")
        
        # Query and display the inserted data using SQLAlchemy ORM
        print("\n📊 Displaying inserted data:")
        
        # Query users using ORM
        users_result = await session.execute(select(User.id, User.name, User.phone_number, User.language))
        users = users_result.fetchall()
        print("\n👥 Users:")
        for user in users:
            print(f"  - {user.name} ({user.phone_number}) - Language: {user.language}")
        
        # Query agricultural data using ORM
        agri_data_result = await session.execute(
            select(AgriculturalData.id, AgriculturalData.user_id, AgriculturalData.crop_type)
        )
        agri_data = agri_data_result.fetchall()
        print("\n🌾 Agricultural Data:")
        for data in agri_data:
            print(f"  - User {data.user_id}: {data.crop_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error inserting test data: {e}")
        await session.rollback()
        return False

async def test_connection():
    """Test the database connection and insert test data"""
    try:
        # Get the database URL from environment
        db_url = os.getenv("NEON_DB_URL")
        if not db_url:
            print("❌ NEON_DB_URL not found in environment variables")
            print("Please create a .env file with your Neon database URL")
            return False
        
        # Create engine
        print("🔌 Creating database engine...")
        engine = create_async_engine(db_url, echo=True)
        
        # Test connection
        print("🔍 Testing database connection...")
        async with engine.begin() as conn:
            print("✅ Database connection successful!")
        
        # Test table creation
        print("📋 Testing table creation...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created successfully!")
        
        # Create session factory
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )
        
        # Insert test data
        async with async_session() as session:
            await insert_test_data(session)
        
        await engine.dispose()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def main():
    """Main function"""
    print("🚀 Testing Neon Database Connection and Data Insertion")
    print("=" * 55)
    
    success = await test_connection()
    
    if success:
        print("\n🎉 All tests passed! Your Neon database is ready to use.")
        print("You can now run your FastAPI application:")
        print("python -m uvicorn app.main:app --reload")
    else:
        print("\n💡 Troubleshooting tips:")
        print("1. Check your .env file exists and has the correct NEON_DB_URL")
        print("2. Make sure your connection string includes 'sslmode=require'")
        print("3. Verify your Neon database is running and accessible")
        print("4. Check if your IP is allowed in Neon's firewall settings")

if __name__ == "__main__":
    asyncio.run(main())