#!/usr/bin/env python
"""
Test script to verify OpenAI and Pinecone API access.
"""
import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

async def test_openai():
    """Test OpenAI API access."""
    print("Testing OpenAI API...")
    
    api_key = os.getenv("TESTINDEX_EMBEDDING__OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found in environment variables")
        return False
    
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="Hello, world!"
        )
        embedding = response.data[0].embedding
        print(f"✅ OpenAI API is working! Embedding dimension: {len(embedding)}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

async def test_pinecone():
    """Test Pinecone API access."""
    print("\nTesting Pinecone API...")
    
    api_key = os.getenv("TESTINDEX_PINECONE__API_KEY")
    environment = os.getenv("TESTINDEX_PINECONE__ENVIRONMENT")
    index_name = os.getenv("TESTINDEX_PINECONE__INDEX_NAME")
    
    if not api_key or not environment:
        print("❌ Pinecone credentials not found in environment variables")
        return False
    
    try:
        # Initialize Pinecone
        pc = Pinecone(api_key=api_key)
        
        # Check if index exists
        indexes = pc.list_indexes()
        
        if index_name in [idx["name"] for idx in indexes]:
            print(f"✅ Pinecone index '{index_name}' exists")
        else:
            print(f"⚠️ Pinecone index '{index_name}' does not exist yet")
            print("   Creating index...")
            
            # Create the index if it doesn't exist
            pc.create_index(
                name=index_name,
                dimension=1536,  # OpenAI embedding dimension
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-west-2")
            )
            print(f"✅ Created Pinecone index '{index_name}'")
        
        # Connect to the index
        index = pc.Index(index_name)
        
        # Check if we can query the index
        stats = index.describe_index_stats()
        print(f"✅ Pinecone connection successful! Current index size: {stats['total_vector_count']} vectors")
        return True
        
    except Exception as e:
        print(f"❌ Pinecone API error: {e}")
        return False

async def main():
    """Run all tests."""
    openai_success = await test_openai()
    pinecone_success = await test_pinecone()
    
    print("\n=== Summary ===")
    print(f"OpenAI API: {'✅ Working' if openai_success else '❌ Not working'}")
    print(f"Pinecone API: {'✅ Working' if pinecone_success else '❌ Not working'}")
    
    if openai_success and pinecone_success:
        print("\n🎉 All services are configured correctly and working!")
    else:
        print("\n⚠️ Some services are not configured correctly. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())
