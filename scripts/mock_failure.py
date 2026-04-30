import asyncio
import httpx
import time

# Final URL and Headers verification
URL = "http://localhost:8000/ingest"
HEADERS = {"X-IMS-KEY": "sre-secret-key"}

# SRE Best Practice: Use a Semaphore to prevent socket exhaustion
# This limits concurrency to 50 signals at a time
SEMAPHORE = asyncio.Semaphore(50)

async def send_signal(client, i):
    async with SEMAPHORE:
        payload = {
            "component_id": "DB_CLUSTER_01",
            "error_message": f"Connection Timeout #{i}",
            "severity": "P0",
            "metadata": {"latency": "5000ms"}
        }
        try:
            # Set a 5-second timeout so one slow request doesn't kill the batch
            response = await client.post(URL, json=payload, headers=HEADERS, timeout=5.0)
            return response.status_code
        except Exception as e:
            return f"Error: {str(e)}"

async def run_load_test():
    # Use high-performance client limits
    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
    
    async with httpx.AsyncClient(limits=limits) as client:
        print(f"SRE Simulation: Firing 10,000 signals to {URL}...")
        start_time = time.time()
        
        # Create all 10,000 tasks
        tasks = [send_signal(client, i) for i in range(10000)]
        
        # Process them in batches of 1000 for better terminal feedback
        batch_size = 1000
        for i in range(0, 10000, batch_size):
            batch = tasks[i:i+batch_size]
            await asyncio.gather(*batch)
            print(f"Progress: Finished signal {i + batch_size}/10,000")
            
        end_time = time.time()
        print(f"\nSUCCESS: Fired 10,000 signals in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    try:
        asyncio.run(run_load_test())
    except KeyboardInterrupt:
        print("\nTest stopped by user.")