#!/usr/bin/env python3
"""
Simple Kafka consumer that processes bid requests.
Shows basic consumption patterns and lag monitoring.
"""

import json
import time
from kafka import KafkaConsumer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'bid-requests'
GROUP_ID = 'bid-processor'

def process_bid(bid):
    """Simulate processing a bid request."""
    # In real life, this would:
    # - Extract features
    # - Look up user history
    # - Run FFM model
    # - Calculate bid price
    
    # Simulate some processing time (0.5-2ms)
    time.sleep(random.uniform(0.0005, 0.002))
    
    return {
        'request_id': bid['request_id'],
        'predicted_ctr': round(random.uniform(0.001, 0.05), 4),
        'bid_price': round(random.uniform(0.5, 3.0), 2)
    }

def main():
    # Create consumer
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        group_id=GROUP_ID,
        auto_offset_reset='earliest',  # Start from beginning if no offset
        enable_auto_commit=True,
        auto_commit_interval_ms=5000,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print(f"🎯 Starting bid request consumer")
    print(f"📍 Broker: {KAFKA_BROKER}")
    print(f"📝 Topic: {TOPIC}")
    print(f"👥 Group: {GROUP_ID}")
    print(f"\nPress Ctrl+C to stop\n")
    
    count = 0
    start_time = time.time()
    
    try:
        for message in consumer:
            bid = message.value
            
            # Process the bid
            result = process_bid(bid)
            
            count += 1
            
            # Print sample every 100 messages
            if count % 100 == 0:
                elapsed = time.time() - start_time
                rate = count / elapsed
                print(f"✅ Processed {count} bids | Rate: {rate:.1f} msg/sec")
                print(f"   Last bid: user={bid['user_id']}, "
                      f"publisher={bid['publisher']}, "
                      f"predicted_ctr={result['predicted_ctr']}")
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Stopped. Total processed: {count}")
        elapsed = time.time() - start_time
        print(f"⏱️  Total time: {elapsed:.1f}s")
        print(f"📊 Average rate: {count/elapsed:.1f} msg/sec")
    
    finally:
        consumer.close()

if __name__ == '__main__':
    import random  # Import here to avoid issues
    main()