import asyncio
import asyncpg

regions = [
    "ap-southeast-1", # Singapore
    "us-east-1",      # N. Virginia
    "eu-central-1",   # Frankfurt
    "ap-southeast-2", # Sydney
    "ap-northeast-1", # Tokyo
    "ap-northeast-2", # Seoul
    "ap-south-1",     # Mumbai
    "us-west-1",      # N. California
    "us-west-2",      # Oregon
    "eu-west-1",      # Ireland
    "eu-west-2",      # London
    "eu-west-3",      # Paris
    "sa-east-1",      # Sao Paulo
    "ca-central-1"    # Canada
]

password = "myRev1000_PBKK"
project_ref = "erecxqltmvgeaesswdka"

async def test_region(region):
    # Try AWS IPv4 pooler
    host = f"aws-0-{region}.pooler.supabase.com"
    user = f"postgres.{project_ref}"
    dsn = f"postgresql://{user}:{password}@{host}:6543/postgres"
    try:
        conn = await asyncio.wait_for(asyncpg.connect(dsn), timeout=3.0)
        await conn.close()
        return dsn
    except Exception as e:
        return None

async def main():
    for r in regions:
        print(f"Testing {r}...")
        res = await test_region(r)
        if res:
            print(f"FOUND: {res}")
            return
    print("NOT FOUND")

if __name__ == "__main__":
    asyncio.run(main())
