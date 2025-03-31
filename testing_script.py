import asyncio
import httpx
import os
from pathlib import Path
import random
from collections import defaultdict
import statistics

async def test_classification(client, file_path, url="http://localhost:8000/classify_file"):
    """Send a file to the classification API."""
    try:
        start_time = asyncio.get_event_loop().time()
        
        # Open and read file
        with open(file_path, 'rb') as f:
            file_data = f.read()
            
        # Try with 'file' instead of 'upload_file' as the field name
        files = {'file': (os.path.basename(file_path), file_data, 'application/octet-stream')}
        
        response = await client.post(url, files=files)
        result = response.json()
        
        latency = asyncio.get_event_loop().time() - start_time
        return {
            'file': os.path.basename(file_path),
            'status': response.status_code,
            'result': result,
            'latency': latency,
            'size': len(file_data)
        }
    except Exception as e:
        return {
            'file': os.path.basename(file_path),
            'status': 'error',
            'result': str(e),
            'latency': asyncio.get_event_loop().time() - start_time,
            'size': 0
        }

async def run_tests(test_files_dir, num_requests=50):
    """Run multiple classification requests."""
    test_files = list(Path(test_files_dir).glob('*'))
    if not test_files:
        print(f"No files found in {test_files_dir}")
        return
    
    print(f"Found {len(test_files)} files for testing")
    
    # Statistics
    start_time = asyncio.get_event_loop().time()
    latencies = []
    classifier_stats = defaultdict(list)
    file_type_stats = defaultdict(list)
    
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(num_requests):
            file_path = random.choice(test_files)
            task = asyncio.create_task(test_classification(client, file_path))
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
    
    # Calculate statistics
    total_time = asyncio.get_event_loop().time() - start_time
    successful = sum(1 for r in results if r['status'] == 200)
    
    # Collect latency statistics
    for result in results:
        if result['status'] == 200:
            latencies.append(result['latency'])
            classifier_name = result['result']['classifier_name']
            doc_type = result['result']['document_type']
            classifier_stats[classifier_name].append(result['latency'])
            file_type_stats[doc_type].append(result['latency'])
    
    print("\nPerformance Statistics:")
    print(f"Total requests: {num_requests}")
    print(f"Successful requests: {successful}")
    print(f"Failed requests: {num_requests - successful}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Throughput: {num_requests/total_time:.2f} requests/second")
    
    if latencies:
        print("\nLatency Statistics (seconds):")
        print(f"Minimum: {min(latencies):.3f}")
        print(f"Maximum: {max(latencies):.3f}")
        print(f"Mean: {statistics.mean(latencies):.3f}")
        print(f"Median: {statistics.median(latencies):.3f}")
        print(f"95th percentile: {sorted(latencies)[int(len(latencies)*0.95)]:.3f}")
        print(f"99th percentile: {sorted(latencies)[int(len(latencies)*0.99)]:.3f}")
    
    print("\nClassifier Performance:")
    for classifier, times in classifier_stats.items():
        print(f"\n{classifier}:")
        print(f"  Count: {len(times)}")
        print(f"  Average latency: {statistics.mean(times):.3f}s")
        print(f"  95th percentile: {sorted(times)[int(len(times)*0.95)]:.3f}s")
    
    print("\nDocument Type Performance:")
    for doc_type, times in file_type_stats.items():
        print(f"\n{doc_type}:")
        print(f"  Count: {len(times)}")
        print(f"  Average latency: {statistics.mean(times):.3f}s")
        print(f"  95th percentile: {sorted(times)[int(len(times)*0.95)]:.3f}s")
    
    # Print some sample results
    print("\nSample Results:")
    for result in results:
        if result['status'] != 200:
            print(f"File: {result['file']}")
            print(f"Status: {result['status']}")
            print(f"Result: {result['result']}")
            print(f"Latency: {result['latency']:.3f}s")
            print(f"Size: {result['size']/1024:.1f}KB")
            print("---")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python test_api.py /path/to/test/files")
        sys.exit(1)
    
    test_files_dir = sys.argv[1]
    print(f"Starting API tests with files from: {test_files_dir}")
    asyncio.run(run_tests(test_files_dir))
