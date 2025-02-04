# Erlang Traffic & Call Center Analysis Library

## Overview
This Python module provides a comprehensive implementation of **Erlang B**, **Erlang C**, and various **traffic engineering & call center analytics** calculations. The library helps estimate call blocking probability, required channels, service levels, and more, making it useful for **telecommunications, call centers, and network planning.**

## Features
✅ **Erlang B Model** - Blocking probability and required channels
✅ **Erlang C Model** - Call queuing probability & waiting time
✅ **Service Level Analysis** - Compute response efficiency
✅ **Busy Hour Traffic Estimation** - Predict peak usage times
✅ **Call Center Metrics** - Abandonment rates, agent occupancy, ASA, CCR, and more
✅ **Traffic Utilization & Efficiency Metrics**
✅ **Peak Hour Call Attempts (PHCA) Calculation**
✅ **Call Completion & Handling Metrics**
✅ **Service Accessibility & Network Efficiency Analysis**

## Installation
No additional dependencies are required. Just include the `Erlang.py` file in your project.

## Usage
### Import the Erlang Class
```python
from Erlang import Erlang
```

### Calculate Erlang Traffic Load
```python
traffic_erlangs = Erlang.calculate_erlang(arrival_rate=120, mean_hold_time=5, average_call_time=3)
print(f"Traffic Load: {traffic_erlangs} Erlangs")
```

### Calculate Required Channels for a Given Blocking Probability
```python
channels_needed = Erlang.calculate_erlang_b(erlangs=traffic_erlangs, block_level_goal=0.01)
print(f"Required Channels: {channels_needed}")
```

### Calculate Blocking Probability
```python
blocking_prob = Erlang.calculate_blocking_probability(erlangs=traffic_erlangs, channels=channels_needed)
print(f"Blocking Probability: {blocking_prob:.2%}")
```

### Compute Queueing Probability (Erlang C)
```python
queue_prob = Erlang.calculate_erlang_c(erlangs=traffic_erlangs, channels=channels_needed)
print(f"Queueing Probability: {queue_prob:.2%}")
```

### Compute Average Waiting Time
```python
waiting_time = Erlang.calculate_waiting_time(erlangs=traffic_erlangs, channels=channels_needed, mean_service_time=3)
print(f"Expected Wait Time: {waiting_time:.2f} minutes")
```

### Compute Service Level
```python
service_level = Erlang.calculate_service_level(erlangs=traffic_erlangs, channels=channels_needed, target_time=1/3)
print(f"Service Level: {service_level:.2f}%")
```

### Compute Busy Hour Traffic
```python
busy_hour_traffic = Erlang.calculate_busy_hour_traffic(daily_erlangs=50)
print(f"Busy Hour Traffic: {busy_hour_traffic:.2f} Erlangs")
```

### Call Center Analytics
#### Call Abandonment Rate
```python
abandonment_rate = Erlang.calculate_call_abandonment_rate(abandoned_calls=50, total_calls=1000)
print(f"Call Abandonment Rate: {abandonment_rate:.2f}%")
```

#### Call Completion Rate
```python
completion_rate = Erlang.calculate_call_completion_rate(completed_calls=950, total_calls=1000)
print(f"Call Completion Rate: {completion_rate:.2f}%")
```

#### Agent Occupancy Rate
```python
occupancy = Erlang.calculate_agent_occupancy(offered_load=traffic_erlangs, num_agents=channels_needed)
print(f"Agent Occupancy: {occupancy:.2f}%")
```

#### Network Efficiency
```python
network_efficiency = Erlang.calculate_network_efficiency(successful_calls=900, total_calls=1000)
print(f"Network Efficiency: {network_efficiency:.2f}%")
```

#### Peak Hour Call Attempts
```python
phca = Erlang.calculate_peak_hour_call_attempts(busy_hour_traffic=50, avg_call_duration=3)
print(f"Peak Hour Call Attempts: {phca:.0f}")
```

## Contributions
Contributions are welcome! If you have suggestions or optimizations, feel free to submit a **pull request** or open an **issue**.

## License
This project is licensed under the **GNU General Public License v2.0**.

## Author
**Jason Callen** www.jasoncallen.com

