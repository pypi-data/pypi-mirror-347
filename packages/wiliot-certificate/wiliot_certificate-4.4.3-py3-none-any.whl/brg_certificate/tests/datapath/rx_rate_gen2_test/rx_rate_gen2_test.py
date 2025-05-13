
from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import brg_certificate.cert_data_sim as cert_data_sim
import time


def cal_scan_time(test, delay, pacer_interval):
    # Calculate the scan time to ensure at least 5 packets are captured in data scan
    # define the num of packet that you want to get
    num_of_sending_pkt = 2  # actually it will be 3 because the first one always send
    delay = delay / 1000
    if delay < pacer_interval:
        scan_time = (pacer_interval * num_of_sending_pkt) + 10
    elif pacer_interval <= delay:
        scan_time = (delay * num_of_sending_pkt) + 10
    # verify scan time value
    if scan_time < (2 * pacer_interval):
        print("scan time is too low in related to pacer interval")
        test.rc == TEST_FAILED
        test.add_reason("scan time is too low in related to pacer interval value")
    return test, scan_time


def scan_and_compare(test, pacer_interval, delay, expected_address_value):

    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=1, duplicates=3, delay=delay, pkt_types=[0], pixels_type=GEN3)
    pixel_sim_thread.start()
    test, scan_time = cal_scan_time(test, delay, pacer_interval)
    df = cert_common.data_scan(test, scan_time=scan_time, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    pixel_sim_thread.stop()
    cert_mqtt.dump_pkts(test, log="rx_rate")
    cert_common.display_data(df, tbc=True, nfpkt=True, rssi=True, dir=test.dir)
    # check if the dataframe is empty or not
    if len(df) <= 1:
        print("Df is empty")
        test.rc = TEST_FAILED
        test.add_reason("Df is empty")
        return test
    else:
        # Divided the dataframe by tag_id and continue with df's tag that has the highest number of rows.
        tag_counts = df[TAG_ID].value_counts()
        print(f"Tag counts:\n{tag_counts.to_string(header=False)}")
        most_common_tag = tag_counts.idxmax()
        print(f"Most common tag: {most_common_tag}")
        df = df[df[TAG_ID] == most_common_tag]
        df = df[[TAG_ID, TBC, PACKET_TYPE, DATETIME]]
        length = len(df)
        mid_index = int(length // 2)
        if mid_index == 0:
            mid_index = 1
        print(f"Length of df: {length}, mid index: {mid_index}")
        print(f"df:\n {df}")

        tag = df.iloc[0][TAG_ID]
        # iloc [1:] to skip the first value of tbc_values which could be 0 sometimes.
        actual_address_value = round(df.iloc[mid_index:][TBC].mean(), 2)  # extract the tbc value from df
        print(f"\nactual address value: {actual_address_value}\nexpected address value: {expected_address_value}")
        THRESHOLD_ADDRESS_VALUE = 5
        # check if the actual address value is in the range of -+5 of the expected address value
        if (actual_address_value < (expected_address_value - THRESHOLD_ADDRESS_VALUE) or
                actual_address_value > (expected_address_value + THRESHOLD_ADDRESS_VALUE)):
            print(f"\nAddress value for tag {tag} is {actual_address_value}, expected value: {expected_address_value}!\n")
            test.rc = TEST_FAILED
            test.add_reason(f"Address value for tag {tag} is {actual_address_value} expected: {expected_address_value}!\n")
        if test.params == [mid_values] and delay == 1000:
            # checking 0 value in the first packet.
            first_row = df.iloc[0][TBC]
            second_row = df.iloc[1][TBC]
            if first_row != 0 and second_row != 0:
                test.rc = TEST_FAILED
                test.add_reason("first tbc value is not 0 as supposed to be while sanity checking")
    return test


def mid_values(test, datapath_module):
    # mid values - Sanity check: Generate packets with delays of 1, 5, and 0.5 seconds.
    # Check address values 192, 243, and 128. Verify that the address value is 0 for the first packet.
    SANITY_DELAY_ADDRESS_VALUES = {1000: 192, 5000: 243, 500: 128}
    for delay, expected_address_value in SANITY_DELAY_ADDRESS_VALUES.items():
        pacer_interval = 1
        test = scan_and_compare(test, pacer_interval=pacer_interval, delay=delay, expected_address_value=expected_address_value)
    time.sleep(2)
    return test


def diff_pacer(test, datapath_module):
    # diff pacer - Generate packets with a 1-second delay and pacer intervals of 30 and 60. Ensure the address value remains 192.
    SANITY_ADDRESS_VALUE = 192
    PACER_INTERVAL_LIST = [30, 60]
    delay = 1000  # 1 sec
    for pacer_interval in PACER_INTERVAL_LIST:
        test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
        if test.rc == TEST_FAILED:
            test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
            return test
        test = scan_and_compare(test, pacer_interval=pacer_interval, delay=delay, expected_address_value=SANITY_ADDRESS_VALUE)
    time.sleep(2)
    return test


def min_value(test, datapath_module):
    # min_value -  Minimum value: Generate packets with a 0.1-second delay. Verify that the address value is 1.
    MIN_ADDRESS_VALUE = 1
    pacer_interval = 1
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
        return test
    delay = 100
    test = scan_and_compare(test, pacer_interval=pacer_interval, delay=delay, expected_address_value=MIN_ADDRESS_VALUE)
    time.sleep(2)
    return test


def max_value(test, datapath_module):
    # max value - Maximum value: Generate packets with a 70-second delay and a pacer interval of 80. Verify that the address value is 255.
    MAX_ADDRESS_VALUE = 255
    pacer_interval = 80
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
        return test
    delay = 70000
    test = scan_and_compare(test, pacer_interval=pacer_interval, delay=delay, expected_address_value=MAX_ADDRESS_VALUE)
    time.sleep(2)
    return test


def diff_rate(test, datapath_module):
    # diff rate - a filter: Generate packets with delay 1 and change to 5, according the delay change test the tolerance address value
    pacer_interval = 1
    delay_duration = [[500, 5], [3000, 3]]
    first_delay = delay_duration[0][0]
    first_duration = delay_duration[0][1]
    second_delay = delay_duration[1][0]
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
        return test
    pixel_sim_thread = cert_data_sim.DataSimThread(test=test, num_of_pixels=1, duplicates=2,
                                                   delay=first_delay, pkt_types=[0], pixels_type=GEN2)
    pixel_sim_thread.start()
    time_sleep = first_duration - ((first_delay / 1000) / 2)
    print(f"sleep for {time_sleep} sec\n")
    time.sleep(time_sleep)
    pixel_sim_thread.delay = second_delay
    scan_time = sum(duration for _, duration in delay_duration) + 20
    df = cert_common.data_scan(test, scan_time=scan_time, brg_data=(not test.internal_brg), gw_data=test.internal_brg)
    pixel_sim_thread.stop()
    df = df[[TAG_ID, TBC]]
    lenght = len(df)

    if len(df) <= 1:
        test.add_reason("Df is empty")
        test.rc = TEST_FAILED
        return test
    else:
        print(f"Df:\n {df}")
    # NOTE: all next rows are specific for the values: delay 0.5 and 3, and in relation address values 128 and 235
    # check if the last tbc value is as we expected  for delay 3 sec we need to get 235 according to LUT  table
    # we define tolerance of +-10 units for address value

    # Most important check, verify it converges to the correct value
    if df.iloc[-1][TBC] not in range(232, 237):
        test.rc = TEST_FAILED
        test.add_reason(f"TBC value: {df.iloc[-1][TBC]}, expected value [232,236]")
        print(f"TBC value: {df.iloc[-1][TBC]}, expected value [232,236] according to delay:{second_delay / 1000} sec")
        return test
    # for loop that skip the first row and check if somewhere there is the expected gap 130 to 200
    result = False
    for i in range(0, lenght - 1):
        prev = df.iloc[i][TBC]
        current = df.iloc[i + 1][TBC]
        if prev in range(120, 140) and current in range(190, 210):
            print(f"Found the gap between {prev} and {current}")
            print(f"row {i}: {df.iloc[i][TBC]}")
            print(f"row {i + 1}: {df.iloc[i + 1][TBC]}")
            result = True
    if not result:
        test.rc = TEST_FAILED
        test.add_reason("Didn't find the correct gap according to alpha filter calculation")
    return test


def run(test):

    # "Test prolog"
    datapath_module = test.active_brg.datapath

    test = cert_common.test_prolog(test)
    pacer_interval = 1
    test = cert_config.brg_configure(test, fields=[BRG_PACER_INTERVAL], values=[pacer_interval], module=datapath_module)[0]
    if test.rc == TEST_FAILED:
        test.add_reason(f"Didn't succeed to config pacer interval {pacer_interval}")
    name = test.phases[0].name
    test.set_phase_rc(name, test.rc)
    test.add_phase_reason(name, test.reason)

    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    RX_RATE_TEST_MAP = {"mid_values": mid_values, "diff_pacer": diff_pacer, "min_value": min_value,
                        "max_value": max_value, "diff_rate": diff_rate}
    for param in test.params:
        functionality_run_print(param.name)
        test = RX_RATE_TEST_MAP[param.value](test, datapath_module)
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED:
            if test.exit_on_param_failure:
                break  # break the whole for loop and keep the test as failed
        test.reset_result()  # reset result and continue to next param

    return cert_common.test_epilog(test)
