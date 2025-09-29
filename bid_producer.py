#!/usr/bin/env python3
"""
Simple Kafka producer that simulates ad bid requests.
Mimics real Criteo traffic patterns.
"""

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'bid-requests'
MESSAGES_PER_SECOND = 100  # Start slow, can increase

# Mock data
PUBLISHERS = ['cnn.com', 'bbc.com', 'nytimes.com', 'lemonde.fr', 'theguardian.com']
CATEGORIES = ['news', 'sports', 'tech', 'fashion', 'travel', 'food']
DEVICES = ['mobile', 'desktop', 'tablet']
COUNTRIES = ['US', 'FR', 'UK', 'DE', 'ES']

def generate_bid_request():
    """Generate a realistic bid request."""
    return {
        'request_id': f'req_{random.randint(1000000, 9999999)}',
        'timestamp': datetime.now(datetime.timezone.utc).isoformat(),
        'user_id': f'user_{random.randint(1, 100000)}',
        'publisher': random.choice(PUBLISHERS),
        'category': random.choice(CATEGORIES),
        'device': random.choice(DEVICES),
        'country': random.choice(COUNTRIES),
        'bid_floor': round(random.uniform(0.1, 2.0), 2)
    }

def main():
    # Create producer
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        acks=1,  # Wait for leader acknowledgment
        compression_type='lz4'  # Same as production
    )
    
    print(f"🚀 Starting bid request producer")
    print(f"📊 Target: {MESSAGES_PER_SECOND} messages/sec")
    print(f"📍 Broker: {KAFKA_BROKER}")
    print(f"📝 Topic: {TOPIC}")
    print(f"\nPress Ctrl+C to stop\n")
    
    count = 0
    start_time = time.time()
    
    try:
        while True:
            # Generate and send bid request
            bid = generate_bid_request()
            producer.send(TOPIC, value=bid)
            
            count += 1
            
            # Print stats every 100 messages
            if count % 100 == 0:
                elapsed = time.time() - start_time
                rate = count / elapsed
                print(f"📈 Sent {count} messages | Rate: {rate:.1f} msg/sec")
            
            # Control rate
            time.sleep(1.0 / MESSAGES_PER_SECOND)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Stopped. Total messages sent: {count}")
        elapsed = time.time() - start_time
        print(f"⏱️  Total time: {elapsed:.1f}s")
        print(f"📊 Average rate: {count/elapsed:.1f} msg/sec")
    
    finally:
        producer.close()

if __name__ == '__main__':
    main()