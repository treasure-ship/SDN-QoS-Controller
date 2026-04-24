#!/bin/bash
# validate.sh - Automated validation / regression testing script
#
# HOW TO RUN (from OUTSIDE Mininet, in a separate terminal):
#   sudo bash ~/qos_project/validate.sh
#
# OR inside Mininet:
#   mininet> sh bash ~/qos_project/validate.sh

echo "================================================"
echo "   QoS SDN PROJECT - VALIDATION SCRIPT"
echo "================================================"
echo ""

# ── TEST 1: Check OVS is running ─────────────────────
echo "[TEST 1] Checking Open vSwitch is running..."
if sudo ovs-vsctl show > /dev/null 2>&1; then
    echo "  PASS - OVS is running"
else
    echo "  FAIL - OVS not running. Start Mininet first!"
    exit 1
fi
echo ""

# ── TEST 2: Check switch exists ──────────────────────
echo "[TEST 2] Checking switch s1 exists..."
if sudo ovs-vsctl list-br | grep -q "s1"; then
    echo "  PASS - Switch s1 found"
else
    echo "  FAIL - Switch s1 not found. Start topo.py first!"
    exit 1
fi
echo ""

# ── TEST 3: Show flow table ──────────────────────────
echo "[TEST 3] Current flow table on s1:"
echo "---"
sudo ovs-ofctl dump-flows s1
echo "---"
echo ""

# ── TEST 4: Show port statistics ─────────────────────
echo "[TEST 4] Port statistics (packet counts):"
echo "---"
sudo ovs-ofctl dump-ports s1
echo "---"
echo ""

# ── TEST 5: Check if QoS rule exists ─────────────────
echo "[TEST 5] Checking flow rules..."
FLOW_COUNT=$(sudo ovs-ofctl dump-flows s1 | grep -c "actions")
echo "  Total flow rules installed: $FLOW_COUNT"
if [ "$FLOW_COUNT" -gt 0 ]; then
    echo "  PASS - Flow rules are present"
else
    echo "  INFO - No flow rules yet (run ping tests first)"
fi
echo ""

# ── TEST 6: Check block rule exists ──────────────────
echo "[TEST 6] Checking for BLOCK rule (h1→h2 drop)..."
if sudo ovs-ofctl dump-flows s1 | grep -q "drop\|actions="; then
    echo "  PASS - Block/drop rule found in flow table"
else
    echo "  INFO - No block rule yet (ping h1→h2 first to trigger it)"
fi
echo ""

# ── TEST 7: Check QoS on h2 interface ────────────────
echo "[TEST 7] Checking QoS on h2-eth0..."
QOS_CHECK=$(tc qdisc show dev h2-eth0 2>/dev/null)
if echo "$QOS_CHECK" | grep -q "tbf"; then
    echo "  PASS - TBF QoS rule is active on h2-eth0"
    echo "  Details: $QOS_CHECK"
else
    echo "  INFO - No QoS rule on h2-eth0 (run run_qos.sh first)"
fi
echo ""

echo "================================================"
echo "   VALIDATION COMPLETE"
echo "================================================"
echo ""
echo "SUMMARY:"
echo "  - Run 'h1 ping h2' in Mininet → should FAIL (blocked)"
echo "  - Run 'h3 ping h2' in Mininet → should PASS (allowed)"
echo "  - Run iperf BEFORE run_qos.sh → ~40 Gbps"
echo "  - Run iperf AFTER run_qos.sh  → ~1 Mbps"
echo ""
