# 🚀 SDN QoS Priority Controller

## 📌 Project Description

This project implements a Software Defined Networking (SDN) based Quality of Service (QoS) controller using **Mininet** and **POX**. It demonstrates traffic control by blocking specific hosts and limiting bandwidth.

---

## 🧠 Key Concepts

* SDN (Software Defined Networking)
* OpenFlow Protocol
* Traffic Control (tc)
* Network Virtualization (Mininet)

---

## 🌐 Topology

3 Hosts (h1, h2, h3) connected to 1 Switch (s1)

```
h1     h2     h3
  \    |    /
        s1
        |
   Controller (POX)
```

---

## ⚙️ Features

* ❌ Block communication (h1 → h2)
* ✔ Allow selective traffic
* 🚦 Apply QoS using bandwidth control
* 📊 Measure performance using iperf

---

## 🧪 How to Run

### 1️⃣ Start Controller

```bash
cd ~/pox
python3 pox.py log.level --DEBUG openflow.of_01 block
```

### 2️⃣ Start Network

```bash
sudo python3 topo.py
```

### 3️⃣ Test Network

```bash
pingall
h1 ping h2
h3 iperf -c 10.0.0.2
```

---

## 📊 Results

| Stage      | Bandwidth  |
| ---------- | ---------- |
| Before QoS | ~18.6 Mbps |
| After QoS  | ~2.18 Mbps |

👉 Shows successful QoS implementation

---

## 🛠️ Tools Used

* Mininet
* POX Controller
* Open vSwitch
* Python
* iperf
* tc

---

## 📄 Author

**Nikitha V**
