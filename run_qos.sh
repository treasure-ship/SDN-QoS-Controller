#!/bin/bash
# run_qos.sh - Apply QoS bandwidth limiting using tc (Traffic Control)
#
# HOW tc TBF WORKS:
#   TBF = Token Bucket Filter
#   Imagine a bucket that fills with tokens at a fixed rate (1 Mbit/s).
#   Each packet needs tokens to be sent.
#   If bucket is empty → packet is delayed (queued).
#   This limits the outgoing bandwidth to exactly 1 Mbit/s.
#
# RUN THIS INSIDE MININET:
#   mininet> h2 bash ~/qos_project/run_qos.sh

INTERFACE="h2-eth0"     # Network interface of h2
RATE="1mbit"            # Speed limit (change to 5mbit, 10mbit etc)
BURST="32kbit"          # Burst buffer size (small = stricter limit)
LATENCY="400ms"         # Max time a packet can wait in queue

echo "================================================"
echo "Applying QoS on interface: $INTERFACE"
echo "Rate limit: $RATE"
echo "================================================"

# Step 1: Remove any existing QoS rules (clean start)
echo "Step 1: Removing old rules..."
tc qdisc del dev $INTERFACE root 2>/dev/null
echo "  Old rules removed (or none existed)"

# Step 2: Apply Token Bucket Filter (TBF)
echo "Step 2: Applying TBF rate limit..."
tc qdisc add dev $INTERFACE root tbf \
    rate $RATE \
    burst $BURST \
    latency $LATENCY

# Check if it worked
if [ $? -eq 0 ]; then
    echo "  SUCCESS! QoS applied."
else
    echo "  ERROR: Failed to apply QoS"
    exit 1
fi

# Step 3: Show the result
echo ""
echo "Step 3: Verifying - current QoS rules:"
tc qdisc show dev $INTERFACE

echo ""
echo "================================================"
echo "QoS ACTIVE: $INTERFACE limited to $RATE"
echo "Now run iperf again to see the difference!"
echo "================================================"
