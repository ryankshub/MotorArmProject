#!/usr/bin/env python3

# Project Import
from cadence_tracker import CadenceTracker

# Python import

# 3rd-party import

# Test file for CadenceTracker
# TODO: add this to unit test folder

CT_50 = CadenceTracker(freq_Hz = 500, time_window_ms=50)
CT_100 = CadenceTracker(freq_Hz = 500, time_window_ms=100)
CT_200 = CadenceTracker(freq_Hz = 500, time_window_ms=200)

CT_50.add_measurement(9.81)
print(f"CT_50 data: {CT_50._data}")
CT_200.add_datum([9.81, 0, 6])
print(f"CT_200 data: {CT_200._data}")
CT_200.clear_data()
print(f"CT_200 data: {CT_200._data}")
test = [1.1*i for i in range(30)]
CT_50.add_datum(test)
print(f"CT_50 data: {CT_50._data}")
print(f"CT_50 cadence: {CT_50.calculate_cadence()}")
print(f"CT_100 cadence: {CT_100.calculate_cadence()}")