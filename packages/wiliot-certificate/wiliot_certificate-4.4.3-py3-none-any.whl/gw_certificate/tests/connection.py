import datetime
import json
import time
import pkg_resources
import pandas as pd
from packaging import version

from gw_certificate.tests.static.connection_defines import *
from gw_certificate.common.debug import debug_print
from gw_certificate.api_if.gw_capabilities import GWCapabilities
from gw_certificate.tests.generic import INCONCLUSIVE_MINIMUM, PassCriteria, MINIMUM_SCORE, PERFECT_SCORE, GenericStage, GenericTest, INFORMATIVE
from gw_certificate.api_if.api_validation import validate_message, MESSAGE_TYPES
from gw_certificate.interface.mqtt import MqttClient, Serialization
from gw_certificate.interface.ble_sniffer import BLESniffer, BLESnifferContext
from gw_certificate.tests.static.references import GW_MQTT_DOC

STATUS_MSG_TIMEOUT = 5

class ConnectionStage(GenericStage):
    def __init__(self, mqttc:MqttClient, **kwargs):
        self.mqttc = mqttc
        self.stage_tooltip = "Awaits the gateway to establish MQTT connection and upload it's configurations via the 'status' topic as it's first message"
        self.__dict__.update(kwargs)
        super().__init__(stage_name=type(self).__name__, **self.__dict__)

    def run(self):
        super().run()
        self.stage_pass = MINIMUM_SCORE
        input('The GW is expected to publish a configuration JSON/Protobuf message through the status topic upon connecting to mqtt:\n'
                'Please unplug GW from power. Press enter when unplugged')
        self.mqttc.flush_messages()
        input('Please plug GW back to power. Press enter when plugged')
        debug_print(f'Waiting for GW to connect... (Timeout {STATUS_MSG_TIMEOUT} minutes)')
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=STATUS_MSG_TIMEOUT)
        self.status_message = None

        while datetime.datetime.now() < timeout and self.status_message is None:
            time.sleep(2)
            self.status_message = self.mqttc.get_status_message()

        if self.status_message is not None:
            ser = self.mqttc.get_serialization()
            debug_print(self.status_message)
            if ser == Serialization.JSON:
                self.validation = validate_message(MESSAGE_TYPES.STATUS, self.status_message)
                self.stage_pass = PERFECT_SCORE if self.validation[0] else MINIMUM_SCORE
            else:
                self.stage_pass = PERFECT_SCORE
            # set GW Capabilities:
            for key, value in self.status_message.items():
                if key in GWCapabilities.get_capabilities() and type(value) is bool:
                    self.gw_capabilities.set_capability(key, value)
            self.cfg_data.status_msg_set(self.status_message, self.mqttc.get_serialization())

    def generate_stage_report(self):
        self.add_report_header()

        if self.status_message is not None:
            ser = self.mqttc.get_serialization()
            debug_print(f'{ser.value} serialization detected')
            self.add_to_stage_report(f'{ser.value} serialization detected')
            self.add_to_stage_report('GW Status packet received:')
            self.add_to_stage_report(f'{json.dumps(self.status_message)}\n')

            for key, value in self.status_message.items():
                if key in GWCapabilities.get_capabilities() and type(value) is bool:
                    self.add_to_stage_report(f'Capability set: {key} - {value}')
            # Add reason test failed to report if neccessary
            if self.stage_pass == MINIMUM_SCORE:
                self.error_summary = "API (JSON structure) is invalid. "
                self.add_to_stage_report(f'\n{len(self.validation[1])} validation errors:')
                for error in self.validation[1]:
                    self.add_to_stage_report(error.message)
                self.add_to_stage_report(f"Please look into the Status section in:\n{GW_MQTT_DOC}")

            self.add_report_topic_validation('status')
        else:
            self.error_summary = f"No message recieved from GW in status topic after {STATUS_MSG_TIMEOUT} mins."
            self.add_to_stage_report(self.error_summary)

        self.report_html = self.template_engine.render_template('stage.html', stage=self,
                                                                stage_report=self.report.split('\n'))
        debug_print(self.report)
        return super().generate_stage_report()
    

class InterferenceAnalysisStage(GenericStage):
    def __init__(self, sniffer:BLESniffer, **kwargs):
        self.sniffer = sniffer
        self.conversion_table_df = None
        self.stage_tooltip = "Analyze BLE interference level (Bad CRC %)"
        self.__dict__.update(kwargs)

        # Stage shows warning if CER is >=50%
        self.result_indication = INFORMATIVE
        self.pass_min = 51

        super().__init__(stage_name=type(self).__name__, **self.__dict__)

    def get_data_from_quantization_csv(self):
        relative_path = CSV_NAME
        csv_path = pkg_resources.resource_filename(__name__, relative_path)
        conversion_table_df = pd.read_csv(csv_path)
        self.conversion_table_df = conversion_table_df

    def interference_analysis(self):
        """Analyze the interference level (PER) before the test begins"""
        self.report_buffer = []
        
        def handle_wrap_around(a):
            "handle a wrap around of the counter"
            if a < 0:
                a = a + MAX_UNSIGNED_32_BIT
            return a
        
        for channel in CHANNELS_TO_ANALYZE:
            # Send the sniffer a command to retrive the counters and convert them to dict
            start_cntrs = self.sniffer.get_pkts_cntrs(channel[0])
            debug_print(f'Analyzing channel {channel[0]}... (30 seconds)')
            time.sleep(CNTRS_LISTEN_TIME_SEC)
            end_cntrs = self.sniffer.get_pkts_cntrs(channel[0])

            if start_cntrs == None or end_cntrs == None:
                debug_print(f'Channel {channel[0]} ({channel[1]} MHz) interference analysis was skipped beacause at least one counter is missing.')
                self.report_buffer.append(f'Channel {channel[0]} ({channel[1]} MHz) Ambient Interference was not calculated, missing at least one counter.')
                self.stage_pass = INCONCLUSIVE_MINIMUM
                continue

            # Calculate the bad CRC percentage
            diff_dict = dict()
            for key in CNTRS_KEYS:
                diff_dict[key] = handle_wrap_around(end_cntrs[key] - start_cntrs[key])
            if (diff_dict[WLT_RX] + diff_dict[NON_WLT_RX]) > 0:
                bad_crc_percentage = round((diff_dict[BAD_CRC] / (diff_dict[WLT_RX] + diff_dict[NON_WLT_RX])) * 100)
            else:
                bad_crc_percentage = 0
            self.report_buffer.append(f'Channel {channel[0]} ({channel[1]} MHz) Ambient Interference (bad CRC percentage) is: {bad_crc_percentage}%.')
            self.report_buffer.append(f'Good CRC packets = {diff_dict[NON_WLT_RX] + diff_dict[WLT_RX] - diff_dict[BAD_CRC]}, bad CRC packets: {diff_dict[BAD_CRC]}')

            good_crc_percentage = 100 - bad_crc_percentage
            if (self.stage_pass == MINIMUM_SCORE) or (good_crc_percentage < self.stage_pass):
                self.stage_pass = good_crc_percentage
                if self.stage_pass < self.pass_min:
                    self.error_summary = "High bad CRC rate within the current environment."
        
            # Uncomment if you want to see PER of the site (will require print adjustments). Below, we use the truth table from the csv to match PER the bad CRC percentage. Require an update of the CSV to the bridge-GW case
            # closest_index = (self.conversion_table_df['bad_crc_percent'] - bad_crc_percentage).abs().idxmin()
            # per_percent = self.conversion_table_df.iloc[closest_index]['per_percent']
            # self.add_to_stage_report(f'Channel {channel} PER is: {per_percent}%')

    def run(self):
        super().run()
        # Run interference analysis
        # Note: there is an infrastructure for converting bad_CRC % to PER, currently unused and commented since the quantization_csv does not match the bridge to GW case.
        debug_print(f"Starting interference analysis for channels {[ch[0] for ch in CHANNELS_TO_ANALYZE]}. This will take {30 * len(CHANNELS_TO_ANALYZE)} seconds (total)")
        # self.get_data_from_quantization_csv()
        self.interference_analysis()
    
    def generate_stage_report(self):
        self.add_report_header()
        for line in self.report_buffer:
            self.add_to_stage_report(line)

        self.report_html = self.template_engine.render_template('stage.html', stage=self,
                                                                stage_report=self.report.split('\n'))
        debug_print(self.report)
        return super().generate_stage_report()

STAGES = [ConnectionStage]

class ConnectionTest(GenericTest):
    def __init__(self, **kwargs):
        self.test_tooltip = "Stages related to cloud connectivity and environment"
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        stages = STAGES
        current_version = self.uart.get_version()
        if current_version != None and version.parse(current_version) >= version.parse(INTERFERENCE_ANALYSIS_FW_VER):
            stages.append(InterferenceAnalysisStage)
        self.stages = [stage(**self.__dict__) for stage in stages]
        
    def run(self):
        super().run()
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            self.test_pass = PassCriteria.calc_for_test(self, stage)
