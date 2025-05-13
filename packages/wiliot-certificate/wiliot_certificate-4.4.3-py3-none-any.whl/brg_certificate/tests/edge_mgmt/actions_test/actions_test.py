from brg_certificate.cert_prints import *
from brg_certificate.cert_defines import *
from brg_certificate.wlt_types import *
import brg_certificate.cert_common as cert_common
import brg_certificate.cert_config as cert_config
import random

BATTERY_SENSOR_SUPPORTING_BOARD_TYPES = [ag.BOARD_TYPE_MINEW_DUAL_BAND_V0, ag.BOARD_TYPE_ERM_V0,
                                         ag.BOARD_TYPE_ERM_V1, ag.BOARD_TYPE_KOAMTAC_V0]
POF_NOT_SUPPORTING_BOARD_TYPES = [ag.BOARD_TYPE_FANSTEL_WIFI_V0, ag.BOARD_TYPE_FANSTEL_LAN_V0]

# Non Default defines
BRG_NON_DEFAULT_DUTY_CYCLE = 15
BRG_NON_DEFAULT_OP_2_4 = 6
BRG_NON_DEFAULT_EP_2_4 = 1
BRG_NON_DEFAULT_SIGNAL_INDICATOR_CYCLE_2_4 = 100
BRG_NON_DEFAULT_SIGNAL_INDICATOR_REP_2_4 = 3
BRG_NON_DEFAULT_SIGNAL_INDICATOR_CYCLE_SUB1G = 100
BRG_NON_DEFAULT_SIGNAL_INDICATOR_REP_SUB1G = 3
BRG_NON_DEFAULT_OUTPUT_POWER_SUB1G = 26
BRG_NON_DEFAULT_PWR_MGMT_KEEP_ALIVE_SCAN = 0
BRG_NON_DEFAULT_TX_REPETITION = 2
BRG_NON_DEFAULT_PACER_INTERVAL = 20
BRG_NON_DEFAULT_RSSI_THRESHOLD = -80
BRG_NON_DEFAULT_CALIB_OUTPUT_POWER = 8
BRG_NON_DEFAULT_PKT_FILTER = 17
BRG_NON_DEFAULT_CALIB_PATTERN = 2
BRG_NON_DEFAULT_CALIB_INTERVAL = 15

LIS2DW12_NON_DEFAULT_STATE_THRESHOLD = 620
LIS2DW12_NON_DEFAULT_WAKE_UP_DURATION = 120
LIS2DW12_NON_DEFAULT_SLEEP_DURATION = 35


def get_brg_non_default_module_pkt(test, module):
    if 'Energy2400' in module.__name__:
        return cert_config.get_default_brg_pkt(test, pkt_type=test.active_brg.energy2400,
                                               duty_cycle=BRG_NON_DEFAULT_DUTY_CYCLE,
                                               output_power=BRG_NON_DEFAULT_OP_2_4, pattern=BRG_NON_DEFAULT_EP_2_4,
                                               signal_indicator_cycle=BRG_NON_DEFAULT_SIGNAL_INDICATOR_CYCLE_2_4,
                                               signal_indicator_rep=BRG_NON_DEFAULT_SIGNAL_INDICATOR_REP_2_4)
    elif 'EnergySub1G' in module.__name__:
        return cert_config.get_default_brg_pkt(test, pkt_type=test.active_brg.energy_sub1g,
                                               duty_cycle=BRG_NON_DEFAULT_DUTY_CYCLE,
                                               signal_indicator_cycle=BRG_NON_DEFAULT_SIGNAL_INDICATOR_CYCLE_SUB1G,
                                               signal_indicator_rep=BRG_NON_DEFAULT_SIGNAL_INDICATOR_REP_SUB1G)
    elif 'PwrMgmt' in module.__name__:
        return cert_config.get_default_brg_pkt(test, pkt_type=test.active_brg.pwr_mgmt,
                                               dynamic_keep_alive_scan=BRG_NON_DEFAULT_PWR_MGMT_KEEP_ALIVE_SCAN)
    elif 'Custom' in module.__name__:
        return cert_config.get_default_brg_pkt(test, pkt_type=test.active_brg.custom,
                                               motion_sensitivity_threshold=LIS2DW12_NON_DEFAULT_STATE_THRESHOLD,
                                               s2d_transition_time=LIS2DW12_NON_DEFAULT_WAKE_UP_DURATION,
                                               d2s_transition_time=LIS2DW12_NON_DEFAULT_SLEEP_DURATION)
    elif 'Datapath' in module.__name__:
        return cert_config.get_default_brg_pkt(test, pkt_type=test.active_brg.datapath,
                                               tx_repetition=BRG_NON_DEFAULT_TX_REPETITION,
                                               pkt_filter=BRG_NON_DEFAULT_PKT_FILTER,
                                               output_power=BRG_NON_DEFAULT_OP_2_4,
                                               pattern=ag.DATAPATH_PATTERN_EU_PATTERN,
                                               pacer_interval=BRG_NON_DEFAULT_PACER_INTERVAL,
                                               rssi_threshold=BRG_NON_DEFAULT_RSSI_THRESHOLD)
    elif 'Calibration' in module.__name__:
        return cert_config.get_default_brg_pkt(test, pkt_type=test.active_brg.calibration,
                                               output_power=BRG_NON_DEFAULT_CALIB_OUTPUT_POWER,
                                               interval=BRG_NON_DEFAULT_CALIB_INTERVAL,
                                               pattern=BRG_NON_DEFAULT_CALIB_PATTERN)
    elif 'ExtSensors' in module.__name__:
        return cert_config.get_default_brg_pkt(test, pkt_type=test.active_brg.sensors,
                                               sensor0=ag.EXTERNAL_SENSORS_MINEWS1,
                                               sensor1=ag.EXTERNAL_SENSORS_VOLTAIC_BATT_LEVEL_DONGLE,
                                               rssi_threshold=BRG_NON_DEFAULT_RSSI_THRESHOLD,
                                               sub1g_rssi_threshold=BRG_NON_DEFAULT_RSSI_THRESHOLD)
    return None


def brg_non_default_modules_cfg(test):
    for module in test.active_brg.modules:
        cfg_pkt = get_brg_non_default_module_pkt(test, module)
        if cfg_pkt:
            utPrint(f"Configuring {module.__name__} non-default cfg", "BLUE")
            test = cert_config.brg_configure(test=test, cfg_pkt=cfg_pkt)[0]
        if test.rc == TEST_FAILED and test.exit_on_param_failure:
            test.add_reason(f"{module.__name__} non-default cfg pkt was not found after {DEFAULT_BRG_FIELD_UPDATE_TIMEOUT} sec!")
            return test
    return test


def search_action_ack(test, action_id, **kwargs):
    test, mgmt_pkts = cert_common.scan_for_mgmt_pkts(test,
                                                     mgmt_type=[eval_pkt(f'{ag.ACTIONS_DICT[action_id]}{test.active_brg.api_version}')])
    if test.rc == TEST_FAILED:
        return test
    print("\nReceived ACK pkts:")
    for p in mgmt_pkts:
        print(p[MGMT_PKT].pkt)
        pkt = cert_config.get_default_brg_pkt(test,
                                              pkt_type=eval_pkt(f'{ag.ACTIONS_DICT[action_id]}{test.active_brg.api_version}'),
                                              **kwargs).pkt
        if p[MGMT_PKT].pkt == pkt:
            utPrint("Received ACK for action", "GREEN")
            return test
    test.rc = TEST_FAILED
    test.add_reason(f"Didn't find action ACK for action id {action_id} {ag.ACTIONS_DICT[action_id]}")
    return test


# modules should receive a list of module names to look for - identical to their actual classes' names!
def scan_for_modules(test, modules=[]):
    modules = test.active_brg.modules if not modules else modules
    found = {module.__name__: False for module in modules}
    start_time = datetime.datetime.now()

    # Search for packets
    while not all(found.values()):
        for module in found:
            pkts = cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=[eval_pkt(module)])
            if pkts and not found[module]:
                found[module] = True
                print("\nGot {} packet after {} sec!".format(module, (datetime.datetime.now() - start_time).seconds))
                print(pkts[-1][MGMT_PKT].pkt)
        print_update_wait()
        if (datetime.datetime.now() - start_time).seconds > DEFAULT_BRG_FIELD_UPDATE_TIMEOUT:
            test.rc = TEST_FAILED
            err_print = ','.join([module for module, value in found.items() if not value])
            test.add_reason("Didn't receive {} after {} seconds!".format(err_print, DEFAULT_BRG_FIELD_UPDATE_TIMEOUT))
            break
    return test

########################################################
# ACTIONS
########################################################


def test_action_gw_hb(test):
    # Create randomized 13 bytes hex to send as the gw
    randomized_gw = ''.join(f'{b:02X}' for b in bytes([random.randint(0, 255) for _ in range(13)]))
    randomized_gw = hex_str2int(randomized_gw)
    # send action
    cert_config.send_brg_action(test, ag.ACTION_GW_HB, gw_id=randomized_gw)
    # analysis
    gw_hb_pkt = eval_pkt(f'ActionGwHbV{test.active_brg.api_version}')
    test, mgmt_pkts = cert_common.scan_for_mgmt_pkts(test, [gw_hb_pkt])
    if not mgmt_pkts:
        test.add_reason("Didn't find ACTION GW HB ACK pkts")
        test.rc = TEST_FAILED
    else:
        for p in mgmt_pkts:
            if p[MGMT_PKT].pkt.rssi == 0 or randomized_gw != p[MGMT_PKT].pkt.gw_id:
                print(f'''ERROR: PKT RSSI: {p[MGMT_PKT].pkt.rssi}\nGW_ID:{p[MGMT_PKT].pkt.gw_id}\n
                    randomized_gw: {randomized_gw}''')
                test.add_reason("GW ID not found OR RSSI is zero on the ACTION GW HB ACK pkt")
                test.rc = TEST_FAILED
    return test


def test_action_blink(test):
    # send action
    cert_config.send_brg_action(test, ag.ACTION_BLINK)
    # analysis
    test = search_action_ack(test, ag.ACTION_BLINK)
    return test


def test_action_send_hb(test):

    # send action
    cert_config.send_brg_action(test, ag.ACTION_SEND_HB)
    # analysis
    test, mgmt_pkts = cert_common.scan_for_mgmt_pkts(test, [eval_pkt(f'Brg2GwHbV{test.active_brg.api_version}')])
    if not mgmt_pkts:
        test.add_reason("Didn't find ACTION HB pkt")
        test.rc = TEST_FAILED
    return test


def test_action_get_battery_sensor(test):
    if test.active_brg.board_type not in BATTERY_SENSOR_SUPPORTING_BOARD_TYPES:
        test.rc = TEST_SKIPPED
        return test
    # prolog
    functionality_run_print('ACTION_GET_BATTERY_SENSOR')
    # send action
    cert_config.send_brg_action(test, ag.ACTION_GET_BATTERY_SENSOR)
    # analysis
    test = search_action_ack(test, ag.ACTION_GET_BATTERY_SENSOR)
    if test.rc == TEST_FAILED:
        return test

    start_time = datetime.datetime.now()
    # This timeout is due to queueing si pkt with needed info at the back of the queue
    scan_time = ACTION_SI_PKT_TIMEOUT
    found_packet = False
    while ((datetime.datetime.now() - start_time).seconds <= scan_time):
        custom_pkts = cert_mqtt.get_all_custom_pkts(test)
        for p in custom_pkts:
            if p[SENSOR_UUID] == f"{ag.SENSOR_SERVICE_ID_BATTERY_SENSOR:06X}":
                print_pkt(p)
                found_packet = True
                break
        if found_packet is True:
            break
        print_update_wait()
    if found_packet is False:
        test.rc = TEST_FAILED
        test.add_reason(f"Didn't find battery sensor data packet within {scan_time} seconds")
    return test


def test_action_get_pof_data(test):
    if test.active_brg.board_type in POF_NOT_SUPPORTING_BOARD_TYPES:
        test.rc = TEST_SKIPPED
        return test
    # send action
    cert_config.send_brg_action(test, ag.ACTION_GET_POF_DATA)
    # analysis
    test = search_action_ack(test, ag.ACTION_GET_POF_DATA)
    if test.rc == TEST_FAILED:
        return test

    start_time = datetime.datetime.now()
    # This timeout is due to queueing si pkt with needed info at the back of the queue
    scan_time = ACTION_SI_PKT_TIMEOUT
    found_packet = False
    while ((datetime.datetime.now() - start_time).seconds <= scan_time):
        custom_pkts = cert_mqtt.get_all_custom_pkts(test)
        for p in custom_pkts:
            if p[SENSOR_UUID] == f"{ag.SENSOR_SERVICE_ID_POF_DATA:06X}":
                print_pkt(p)
                found_packet = True
                break
        if found_packet is True:
            break
        print_update_wait()
    if found_packet is False:
        test.rc = TEST_FAILED
        test.add_reason(f"Didn't find pof data packet within {scan_time} seconds")
    return test


def test_action_pl_status(test):
    # send action - Set status to 0 only, if pl is set to 1 BRG works differently
    cert_config.send_brg_action(test, ag.ACTION_PL_STATUS, status=0)
    # analysis
    test = search_action_ack(test, ag.ACTION_PL_STATUS, status=0)
    return test


def test_action_get_module(test):
    # CHECK ONLY FOR ONE MODULE (ModuleDatapath) #
    # send action
    print("\nCHECK ONLY FOR ModuleDatapath\n")
    cert_config.send_brg_action(test, ag.ACTION_GET_MODULE, datapath=1)
    # analysis
    test = search_action_ack(test, ag.ACTION_GET_MODULE, datapath=1)
    test = scan_for_modules(test, [test.active_brg.datapath])
    if test.rc == TEST_FAILED:
        return test

    # CHECK FOR ALL MODULES AT ONCE #
    # send action
    print("\nCHECK FOR ALL MODULES AT ONCE\n")
    cert_config.send_brg_action(test, ag.ACTION_GET_MODULE, interface=1, datapath=1, energy2400=1,
                                energy_sub1g=1, calibration=1, pwr_mgmt=1, ext_sensors=1, custom=1)
    # analysis
    test = search_action_ack(test, ag.ACTION_GET_MODULE, interface=1, datapath=1, energy2400=1,
                             energy_sub1g=1, calibration=1, pwr_mgmt=1, ext_sensors=1, custom=1)
    test = scan_for_modules(test)
    return test


def test_action_reboot(test):
    # non-default cfg
    test = brg_non_default_modules_cfg(test)
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True)
    # sample non-default cfg_hash
    test, non_default_hash = cert_common.get_cfg_hash(test)
    if test.active_brg.cfg_hash == non_default_hash:
        test.rc = TEST_FAILED
        test.add_reason(f"Config failed default_hash==non_default==0x{non_default_hash:08X}")
    if test.rc == TEST_FAILED:
        return test
    print(f"\nnon_default_hash: 0x{non_default_hash:08X}\n")
    # send action
    cert_config.send_brg_action(test, ag.ACTION_REBOOT)
    # analysis
    test = cert_common.reboot_config_analysis(test, expected_hash=non_default_hash, timeout=40)
    # epilog
    test = cert_config.config_brg_defaults(test)[0]
    return test


def test_action_restore_defaults(test):
    # non-default cfg
    test = brg_non_default_modules_cfg(test)
    if test.rc == TEST_FAILED and test.exit_on_param_failure:
        return cert_common.test_epilog(test, revert_brgs=True)
    # sample non-default cfg_hash
    test, non_default_hash = cert_common.get_cfg_hash(test)
    if test.rc == TEST_FAILED:
        # revert to defaults without restore_defaults action if action failed
        test = cert_config.config_brg_defaults(test)[0]
        return test
    # send action
    cert_config.send_brg_action(test, ag.ACTION_RESTORE_DEFAULTS)
    # analysis
    expected_hash = test.active_brg.cfg_hash
    utPrint("Analyzing Restore Defaults", "BLUE")
    # First 30 for wlt app start + 10 sec extra for brg to settle to recieve its get module action
    cert_common.wait_time_n_print(40)

    start_time = datetime.datetime.now()
    seq_ids = []
    cfg_once = True
    test.mqttc.flush_pkts()

    utPrint(f"Get Interface Module from BRG {test.active_brg.id_str}")
    cert_config.send_brg_action(test, ag.ACTION_GET_MODULE, interface=1)
    test = search_action_ack(test, ag.ACTION_GET_MODULE, interface=1)
    if test.rc == TEST_FAILED:
        return test

    while True:
        # scan for ModuleIf pkt of all api versions to support api version change on update
        pkts = cert_mqtt.get_brg2gw_mgmt_pkts(test.mqttc, test, mgmt_types=[eval_pkt(f'ModuleIfV{test.active_brg.api_version}')])
        for p in pkts:
            if (not seq_ids or p[SEQUENCE_ID] not in seq_ids):
                seq_ids.append(p[SEQUENCE_ID])
                interface = p[MGMT_PKT].pkt
                if interface:
                    test.active_brg.api_version = interface.api_version
                    print(f"\nGot pkt after {(datetime.datetime.now() - start_time).seconds} sec!")
                    print(interface)
                    received_hash = interface.cfg_hash
                    print(f"\nexpected cfg_hash: 0x{expected_hash:08X}\n"
                          f"received cfg_hash: 0x{received_hash:08X}\n"
                          f"non_default_hash: 0x{non_default_hash:08X}")
                    if received_hash == non_default_hash:
                        # test.rc = TEST_FAILED
                        test.add_reason("received_hash is equal to non_default_hash, ACTION_RESTORE_DEFAULTS was not received by the brg!")
                        # return test
                    elif received_hash == expected_hash:
                        return test
                    else:
                        # Default SUB1G EP in the BRG is 0 and in the UT is 9
                        # in order to allign BRG cfg to the one after ut.py start script
                        # we should configure sub1g ep individually once after reboot in case cfg hash dont match
                        if ag.MODULE_ENERGY_SUB1G in test.active_brg.sup_caps and cfg_once:
                            cfg_once = False
                            cfg_pkt = cert_config.get_default_brg_pkt(test,
                                                                      test.active_brg.energy_sub1g,
                                                                      **{BRG_PATTERN: ag.SUB1G_ENERGY_PATTERN_ISRAEL})
                            test = cert_config.brg_configure(test, cfg_pkt=cfg_pkt)[0]
                            if test.rc == TEST_FAILED:
                                return test
                            cert_config.send_brg_action(test, ag.ACTION_GET_MODULE, interface=1)
        print_update_wait()

        if (datetime.datetime.now() - start_time).seconds > DEFAULT_BRG_FIELD_UPDATE_TIMEOUT:
            test.rc = TEST_FAILED
            test.add_reason(f"Didn't receive expected ModuleIfV{test.active_brg.api_version} pkt "
                            f"after {DEFAULT_BRG_FIELD_UPDATE_TIMEOUT} seconds!")
            # revert to defaults without restore_defaults action if action failed
            test = cert_config.config_brg_defaults(test)[0]
            break
    return test


ACTIONS_TEST_MAP = {ag.ACTION_GW_HB: test_action_gw_hb, ag.ACTION_BLINK: test_action_blink,
                    ag.ACTION_SEND_HB: test_action_send_hb, ag.ACTION_GET_BATTERY_SENSOR: test_action_get_battery_sensor,
                    ag.ACTION_GET_POF_DATA: test_action_get_pof_data, ag.ACTION_PL_STATUS: test_action_pl_status,
                    ag.ACTION_GET_MODULE: test_action_get_module, ag.ACTION_REBOOT: test_action_reboot,
                    ag.ACTION_RESTORE_DEFAULTS: test_action_restore_defaults}


def run(test):
    test = cert_common.test_prolog(test)
    if test.rc == TEST_FAILED:
        return cert_common.test_epilog(test)

    for param in test.params:
        # Run action
        functionality_run_print(param.name)
        test = ACTIONS_TEST_MAP[param.value](test)
        # action Epilog
        generate_log_file(test, param.name)
        field_functionality_pass_fail_print(test, param.name)
        test.set_phase_rc(param.name, test.rc)
        test.add_phase_reason(param.name, test.reason)
        if test.rc == TEST_FAILED:
            if test.exit_on_param_failure:
                break  # break the whole for loop and keep the test as failed
        test.reset_result()  # reset result and continue to next param

    return cert_common.test_epilog(test)
