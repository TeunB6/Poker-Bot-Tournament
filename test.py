from src.judge import Judge
from src.poker_agent import CallAgent
import time

start = time.perf_counter()
judge = Judge(*[CallAgent() for  _ in range(10)])
h = judge.run_hand_n_times(num_rounds=100, display=False, verbose=True)
print(time.perf_counter()-start)