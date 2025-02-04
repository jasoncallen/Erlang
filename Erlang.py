import math

class Erlang:
    """
    A comprehensive class for Erlang B, Erlang C, and various traffic and call center analytics.
    """

    @staticmethod
    def calculate_erlang(arrival_rate: float, mean_hold_time: float, average_call_time: float) -> float:
        """
        Calculates the traffic load (Erlangs) of a circuit.

        :param arrival_rate: The number of calls per hour.
        :param mean_hold_time: The average hold time per call (seconds).
        :param average_call_time: The average call duration (seconds).
        :return: The total traffic Erlangs.
        """
        if arrival_rate < 0 or mean_hold_time < 0 or average_call_time < 0:
            raise ValueError("All input values must be non-negative.")

        total_time = (mean_hold_time + average_call_time) / 60  # Convert minutes to hours
        erlangs = round((arrival_rate * total_time) / 60, 4)  # Convert to Erlangs

        return erlangs

    @staticmethod
    def calculate_erlang_b(erlangs: float, block_level_goal: float) -> int:
        """
        Calculates the required number of channels to support a given Erlang load and blocking probability.

        :param erlangs: The total traffic in Erlangs.
        :param block_level_goal: The target blocking probability (e.g., 0.01 for 1%).
        :return: The required number of channels.
        """
        if erlangs < 0 or block_level_goal <= 0 or block_level_goal >= 1:
            raise ValueError("Erlangs must be non-negative and block_level_goal must be between 0 and 1.")

        channel = 1
        previous_d = 1
        previous_e = 1

        while True:
            block_percentage = ((erlangs / channel) * previous_d) / (previous_e + ((erlangs / channel) * previous_d))
            previous_e += (erlangs / channel) * previous_d
            previous_d = (erlangs / channel) * previous_d

            if block_percentage < block_level_goal:
                break

            channel += 1

        return channel

    @staticmethod
    def calculate_blocking_probability(erlangs: float, channels: int) -> float:
        """
        Calculates the probability of call blocking given a certain number of channels.

        :param erlangs: The total traffic in Erlangs.
        :param channels: The number of available channels.
        :return: The blocking probability as a decimal (e.g., 0.05 for 5%).
        """
        if erlangs < 0 or channels < 1:
            raise ValueError("Erlangs must be non-negative and channels must be at least 1.")

        b = 1
        for k in range(1, channels + 1):
            b = 1 + (k * b) / erlangs

        return 1 / b

    @staticmethod
    def calculate_erlang_c(erlangs: float, channels: int) -> float:
        """
        Calculates the probability that a call will be delayed (Erlang C formula).

        :param erlangs: The total traffic in Erlangs.
        :param channels: The number of available channels.
        :return: The probability of delay.
        """
        if erlangs >= channels:
            return 1  # If traffic exceeds capacity, all calls are delayed

        try:
            numerator = (math.pow(erlangs, channels) / math.factorial(channels)) * (channels / (channels - erlangs))
            denominator = sum(math.pow(erlangs, k) / math.factorial(k) for k in range(channels + 1)) + numerator
        except OverflowError:
            return float('inf')

        return numerator / denominator

    @staticmethod
    def calculate_waiting_time(erlangs: float, channels: int, mean_service_time: float) -> float:
        """
        Computes the average waiting time in queue (minutes) using Erlang C.

        :param erlangs: The total traffic in Erlangs.
        :param channels: The number of available channels.
        :param mean_service_time: The average call duration (minutes).
        :return: The expected waiting time in queue (minutes).
        """
        pw = Erlang.calculate_erlang_c(erlangs, channels)
        return (pw / (channels - erlangs)) * mean_service_time if channels > erlangs else float('inf')

    @staticmethod
    def calculate_service_level(erlangs: float, channels: int, target_time: float) -> float:
        """
        Computes the service level (percentage of calls answered within target time).

        :param erlangs: The total traffic in Erlangs.
        :param channels: The number of available channels.
        :param target_time: The target answer time (minutes).
        :return: Service level as a percentage.
        """
        pw = Erlang.calculate_erlang_c(erlangs, channels)
        return (1 - pw * math.exp(-(channels - erlangs) * target_time)) * 100 if channels > erlangs else 0.0

    @staticmethod
    def calculate_offered_load(call_arrival_rate: float, mean_call_duration: float) -> float:
        """
        Computes the offered load in Erlangs.

        :param call_arrival_rate: Number of calls per second.
        :param mean_call_duration: Mean call duration in seconds.
        :return: Offered load in Erlangs.
        """
        return call_arrival_rate * mean_call_duration

    @staticmethod
    def calculate_utilization(erlangs: float, channels: int) -> float:
        """
        Computes the utilization factor.

        :param erlangs: The total traffic in Erlangs.
        :param channels: The number of available channels.
        :return: Utilization factor.
        """
        return erlangs / channels if channels > 0 else 0.0

    @staticmethod
    def calculate_busy_hour_traffic(daily_erlangs: float, busy_hour_fraction: float = 0.17) -> float:
        """
        Estimates busy hour traffic.

        :param daily_erlangs: The total daily traffic (Erlangs).
        :param busy_hour_fraction: The fraction of daily traffic occurring in the busy hour (default 17%).
        :return: Busy hour traffic in Erlangs.
        """
        return daily_erlangs * busy_hour_fraction

    @staticmethod
    def calculate_effective_traffic(offered_load: float, blocking_probability: float) -> float:
        """
        Calculates the effective carried traffic after blocking.
        
        Effective traffic represents the portion of offered traffic that is successfully carried
        by the system, excluding blocked calls.

        :param offered_load: The total offered traffic in Erlangs.
        :param blocking_probability: The probability of a call being blocked (decimal format, e.g., 0.02 for 2%).
        :return: The effective carried traffic in Erlangs.
        """
        return offered_load * (1 - blocking_probability)

    @staticmethod
    def calculate_overflow_traffic(offered_load: float, blocking_probability: float) -> float:
        """
        Calculates the overflow traffic (calls that were blocked due to congestion).
        
        Overflow traffic represents the portion of offered traffic that gets blocked
        and cannot be carried by the network.

        :param offered_load: The total offered traffic in Erlangs.
        :param blocking_probability: The probability of a call being blocked (decimal format, e.g., 0.02 for 2%).
        :return: The amount of blocked traffic in Erlangs.
        """
        return offered_load * blocking_probability

    @staticmethod
    def calculate_peak_hour_call_attempts(busy_hour_traffic: float, avg_call_duration: float) -> float:
        """
        Calculates the estimated number of call attempts during the peak hour.
        
        The peak hour call attempts (PHCA) is the estimated number of calls made during
        the busiest hour of the day, based on traffic load and call duration.

        :param busy_hour_traffic: The total traffic in Erlangs during the busiest hour.
        :param avg_call_duration: The average call duration in minutes.
        :return: The estimated number of call attempts during peak hour.
        """
        return busy_hour_traffic * (60 / avg_call_duration)

    @staticmethod
    def calculate_call_completion_rate(completed_calls: int, total_calls: int) -> float:
        """
        Calculates the Call Completion Rate (CCR).
        
        CCR represents the percentage of total calls that were successfully completed
        without disconnection or abandonment.

        :param completed_calls: The number of successfully completed calls.
        :param total_calls: The total number of call attempts made.
        :return: The call completion rate as a percentage (0-100%).
        """
        return (completed_calls / total_calls) * 100 if total_calls > 0 else 0

    @staticmethod
    def calculate_average_call_handling_time(total_talk_time: float, total_calls: int) -> float:
        """
        Calculates the Average Call Handling Time (AHT).
        
        AHT is the average time spent handling a call, including talk time
        and any necessary after-call work.

        :param total_talk_time: The total time spent on calls in minutes.
        :param total_calls: The total number of calls handled.
        :return: The average handling time per call in minutes.
        """
        return total_talk_time / total_calls if total_calls > 0 else 0

    @staticmethod
    def calculate_traffic_intensity(erlangs: float, channels: int) -> float:
        """
        Calculates the traffic intensity in percentage.
        
        Traffic intensity measures how busy the system is, based on the total traffic
        load and the available channels.

        :param erlangs: The total offered traffic in Erlangs.
        :param channels: The total number of available channels.
        :return: The traffic intensity as a percentage (0-100%).
        """
        return (erlangs / channels) * 100 if channels > 0 else 0

    @staticmethod
    def calculate_network_efficiency(successful_calls: int, total_calls: int) -> float:
        """
        Calculates the Network Efficiency (NE).
        
        NE measures how efficiently the network handles call traffic by comparing the number
        of successful calls to total call attempts.

        :param successful_calls: The number of successful (completed) calls.
        :param total_calls: The total number of call attempts.
        :return: The network efficiency as a percentage (0-100%).
        """
        return (successful_calls / total_calls) * 100 if total_calls > 0 else 0

    @staticmethod
    def calculate_agent_occupancy(offered_load: float, num_agents: int) -> float:
        """
        Calculates the Agent Occupancy Rate in a call center.
        
        This metric measures how busy agents are handling calls, based on the total traffic load
        and the number of available agents.

        :param offered_load: The total traffic in Erlangs.
        :param num_agents: The total number of agents handling calls.
        :return: The agent occupancy rate as a percentage (0-100%).
        """
        return (offered_load / num_agents) * 100 if num_agents > 0 else 0

    @staticmethod
    def calculate_call_load_per_channel(total_calls: int, channels: int) -> float:
        """
        Calculates the average call load per channel.
        
        This measures the number of calls processed per channel during a given period.

        :param total_calls: The total number of calls handled.
        :param channels: The total number of available channels.
        :return: The average number of calls per channel.
        """
        return total_calls / channels if channels > 0 else 0

    @staticmethod
    def calculate_average_speed_of_answer(total_answer_time: float, total_calls_answered: int) -> float:
        """
        Calculates the Average Speed of Answer (ASA).
        
        ASA measures the average wait time before a caller is connected to an agent.

        :param total_answer_time: The total time spent waiting for calls to be answered in minutes.
        :param total_calls_answered: The total number of calls that were answered.
        :return: The average speed of answer in minutes.
        """
        return total_answer_time / total_calls_answered if total_calls_answered > 0 else 0

    @staticmethod
    def calculate_call_abandonment_rate(abandoned_calls: int, total_calls: int) -> float:
        """
        Calculates the Call Abandonment Rate.
        
        This measures the percentage of callers who hung up before being connected to an agent.

        :param abandoned_calls: The number of calls abandoned before being answered.
        :param total_calls: The total number of call attempts.
        :return: The call abandonment rate as a percentage (0-100%).
        """
        return (abandoned_calls / total_calls) * 100 if total_calls > 0 else 0

    @staticmethod
    def calculate_service_accessibility(blocking_probability: float) -> float:
        """
        Calculates Service Accessibility.
        
        This metric represents the likelihood that a caller will successfully access a service without being blocked.

        :param blocking_probability: The probability of a call being blocked (decimal format, e.g., 0.02 for 2%).
        :return: The service accessibility as a percentage (0-100%).
        """
        return (1 - blocking_probability) * 100
