# 10-Minute Kafka Lab Quickstart

Get your Kafka lab running in 10 minutes!

## Step 1: Setup (2 minutes)

```bash
# Create project
mkdir kafka-lab
cd kafka-lab

# Create data directories
mkdir -p data/kafka data/zookeeper

# Copy the docker-compose.yml file here
# Copy requirements.txt, bid_producer.py, bid_consumer.py here
```

## Step 2: Start Kafka (2 minutes)

```bash
# Start cluster
docker-compose up -d

# Wait 30 seconds for startup
sleep 30

# Verify it's running
docker-compose ps

# Should see both containers "Up"
```

## Step 3: Create Topics (1 minute)

```bash
# Create bid-requests topic
docker exec -it kafka-broker-1 kafka-topics \
  --create \
  --topic bid-requests \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# Verify
docker exec -it kafka-broker-1 kafka-topics \
  --list \
  --bootstrap-server localhost:9092
```

## Step 4: Install Python Dependencies (1 minute)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install kafka-python
pip install -r requirements.txt
```

## Step 5: Test It! (4 minutes)

### Terminal 1: Start Consumer
```bash
python bid_consumer.py
```

### Terminal 2: Start Producer
```bash
python bid_producer.py
```

### Terminal 3: Monitor Lag
```bash
# Watch consumer lag in real-time
watch -n 2 'docker exec kafka-broker-1 kafka-consumer-groups \
  --bootstrap-server localhost:9092 \
  --describe \
  --group bid-processor'
```

**You should see:**
- Producer: "📈 Sent X messages"
- Consumer: "✅ Processed X bids"
- Lag monitor: LAG column (should stay near 0)

## What to Try Next

### Experiment 1: Increase Load
Edit `bid_producer.py`:
```python
MESSAGES_PER_SECOND = 1000  # Increase from 100
```

Watch what happens to consumer lag!

### Experiment 2: Slow Consumer
Edit `bid_consumer.py`:
```python
time.sleep(random.uniform(0.01, 0.05))  # Increase sleep time
```

Consumer will fall behind → lag increases!

### Experiment 3: Multiple Consumers
Start 2 consumers in different terminals:
```bash
# Terminal 1
python bid_consumer.py

# Terminal 2
python bid_consumer.py
```

They'll share the load (Kafka auto-balances)!

## Quick Commands

```bash
# Stop everything
docker-compose down

# Start again
docker-compose up -d

# View Kafka logs
docker-compose logs -f kafka

# Delete topic and start fresh
docker exec -it kafka-broker-1 kafka-topics \
  --delete --topic bid-requests --bootstrap-server localhost:9092
```

## Troubleshooting

**Producer fails with "Connection refused":**
- Wait 30 seconds after `docker-compose up`
- Check: `docker-compose ps`

**Consumer doesn't receive messages:**
- Check producer is running
- Check topic exists: `kafka-topics --list`
- Check consumer group: `kafka-consumer-groups --list`

**Want to start fresh?**
```bash
docker-compose down
sudo rm -rf data/
docker-compose up -d
# Wait 30 seconds, recreate topics
```

## Success Checklist

- [ ] Kafka cluster running
- [ ] Created bid-requests topic
- [ ] Producer sending messages
- [ ] Consumer receiving messages
- [ ] Can monitor consumer lag

**If all checked: You're ready for Criteo! 🎉**

## Next Steps

1. Read the full README.md for detailed exercises
2. Try the failure scenarios
3. Add monitoring (Grafana)
4. Expand to 3-broker cluster

**Questions?** Check README.md or just experiment - you can't break anything!