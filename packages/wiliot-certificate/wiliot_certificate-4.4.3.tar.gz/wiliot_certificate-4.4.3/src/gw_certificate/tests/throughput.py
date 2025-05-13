import datetime
import os
import time
import pandas as pd
import plotly.express as px
import tabulate

from gw_certificate.ag.ut_defines import PAYLOAD
from gw_certificate.common.debug import debug_print
from gw_certificate.api_if.gw_capabilities import GWCapabilities
from gw_certificate.interface.ble_simulator import BLESimulator
from gw_certificate.tests.static.uplink_defines import *
from gw_certificate.tests.uplink import TimestampsHelper
from gw_certificate.interface.mqtt import MqttClient
from gw_certificate.tests.static.generated_packet_table import StressRunData
from gw_certificate.tests.generic import PassCriteria, PERFECT_SCORE, GenericTest, GenericStage, INFORMATIVE

# HELPER DEFINES
ONE_SECOND_MS = 1000
STRESS_DEFAULT_DELAYS = [50, 25, 16.66, 12.5, 10, 8.33, 7.14, 6.25, 5.55, 5, 4.5, 4, 3.5, 3]
STRESS_DEFAULT_PPS = [int(1000 / delay) for delay in STRESS_DEFAULT_DELAYS]
TIME_PER_DELAY = 30
TIME_PER_DELAY_FIRST = 50

# HELPER FUNCTIONS

def process_payload(packet:dict):
    payload = packet[PAYLOAD]
    payload = payload.upper()
    if len(payload) == 62 and payload[2:4] == '16':
        payload = payload [4:]
    # big2little endian
    if payload[:4] == 'FCC6':
        payload = 'C6FC' + payload[4:]
    packet[PAYLOAD] = payload
    return packet


# TEST STAGES
class GenericStressStage(GenericStage):
    def __init__(self, mqttc:MqttClient, ble_sim:BLESimulator, gw_capabilities:GWCapabilities, stage_name,
                **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(stage_name=stage_name, **self.__dict__)
        
        self.result_indication = INFORMATIVE        
        
        # Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim

        # Packets list
        self.local_pkts = []
        self.mqtt_pkts = []
        self.full_test_pkts = pd.DataFrame()
        
        # GW Capabilities
        self.gw_capabilities = gw_capabilities

        #Run Data
        self.run_stress_data = StressRunData()
        
        # Data extracted from the test csv
        self.all_test_payloads = None
    
    def prepare_stage(self, reset_ble_sim=True):
        super().prepare_stage()
        self.mqttc.flush_messages()
        if reset_ble_sim:
            self.ble_sim.set_sim_mode(True) 
        
    def fetch_mqtt_from_stage(self):
        mqtt_pkts = self.mqttc.get_all_tags_pkts()
        self.mqtt_pkts = list(map(lambda p: process_payload(p), mqtt_pkts))
    
    def compare_local_mqtt(self):
        self.fetch_mqtt_from_stage()
        local_pkts_df = pd.DataFrame(self.local_pkts, columns=[PAYLOAD])
        mqtt_pkts_df = pd.DataFrame(self.mqtt_pkts)
        comparison = local_pkts_df

        if PAYLOAD not in mqtt_pkts_df.columns:
            mqtt_pkts_df[PAYLOAD] = ''
        received_pkts_df = pd.merge(local_pkts_df[PAYLOAD], mqtt_pkts_df[PAYLOAD], how='inner')
        
        received_pkts = set(received_pkts_df[PAYLOAD])

        self.pkts_received_count = pd.Series.count(received_pkts_df)
        unique_received_count = len(received_pkts)
        self.pkts_filtered_out_count = self.pkts_received_count - unique_received_count

        comparison[RECEIVED] = comparison[PAYLOAD].isin(received_pkts)
        self.comparison = comparison

class StressTestStage(GenericStressStage):
    
    def __init__(self, mqttc, ble_sim, gw_capabilities, **kwargs):
        super().__init__(mqttc, ble_sim, gw_capabilities, stage_name=type(self).__name__, **kwargs)
        self.duplicates = 1
        self.report_data = {}
        self.stage_tooltip = "Attempts different PPS (packets per second) rates to examine the gateway limit (actual PPS may vary per OS)"
        desired_pps = kwargs.get('stress_pps', None)

        def pps_to_delay(pps):
            delay = 1000 / pps
            trunctuated = int(delay * 100) / 100
            return trunctuated

        self.delays = STRESS_DEFAULT_DELAYS if desired_pps == None else [pps_to_delay(desired_pps)]
        self.ts_records_arr = [TimestampsHelper() for delay in self.delays]
        debug_print(f"StressTest delays configured: {self.delays}")
        
    def run(self):
        super().run()
        for idx, delay in enumerate(self.delays):
            self.stress_delay = delay
            debug_print(f"---Running Stress Test with delay of {delay}")
            self.run_full_stress_test(idx, delay)

    def run_full_stress_test(self, delay_idx, delay):
        self.prepare_stage()
        self.run_stress_test_with_delay(delay_idx, delay)
        if self.aggregation_time > 0:
            debug_print(f"Waiting {self.aggregation_time} seconds for packets to be uploaded before processing results..")
            time.sleep(self.aggregation_time)
        self.generate_stage_report(delay_idx)
        self.teardown_stage()

    def prepare_stage(self):
        super().prepare_stage()
        self.local_pkts = []

    def run_stress_test_with_delay(self, delay_idx, delay):
        run_data = self.run_stress_data.data
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=TIME_PER_DELAY_FIRST if delay == STRESS_DEFAULT_DELAYS[0] else TIME_PER_DELAY)
        last_sent_time = time.perf_counter_ns()
        debug_print('Advertising packets...')
        for index, row in run_data.iterrows():
            if datetime.datetime.now() > end_time:
                debug_print(f"Timeout for PPS rate {int(ONE_SECOND_MS / delay)} reached")
                break
            data = row[ADVA_PAYLOAD]
            self.local_pkts.append(row[PAYLOAD])
            while True:
                if time.perf_counter_ns() - last_sent_time >= delay * 10**6:
                    self.ble_sim.send_packet(data, duplicates=self.duplicates, delay=0, print_for_debug=False)
                    last_sent_time = time.perf_counter_ns()
                    break
            self.ts_records_arr[delay_idx].set_adv_timestamp_current(data)
        # Since stress entries in packet_table.csv are reused with different delays, we set it here. 
        # For each iteration a different ts_records instance that holds a different copy of the original dataframe.
        self.ts_records_arr[delay_idx].table.loc[pd.DataFrame.notna(self.ts_records_arr[delay_idx].table[ADV_TIMESTAMP]), 'time_delay'] = delay
        time.sleep(15)

    def teardown_stage(self):
        self.ble_sim.set_sim_mode(False)
        self.mqttc.flush_messages()

    def generate_stage_report(self, delay_idx):
        def save_to_csv(df, csv_path):
            """
            Save a DataFrame to a CSV file without overwriting existing content.
            
            :param df: The DataFrame to be saved.
            :param csv_path: The path to the CSV file.
            """
            if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
                df.to_csv(csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_path, mode='w', header=True, index=False)
                
        self.compare_local_mqtt()
        report = []
        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        self.stage_pass = PERFECT_SCORE    
        self.comparison['duplications'] = self.duplicates
        self.comparison['time_delay'] = self.stress_delay
        self.full_test_pkts = pd.concat([self.full_test_pkts, self.comparison], ignore_index=True)
        save_to_csv(self.comparison, self.csv_path)
        
        if str(self.stress_delay) not in self.report_data:
                self.report_data[str(self.stress_delay)] = {}
        self.report_data[str(self.stress_delay)]['pkts_sent'] = num_pkts_sent
        self.report_data[str(self.stress_delay)]['pkts_recieved'] = num_pkts_received
        self.report_data[str(self.stress_delay)]['pkts_per_sec_desired'] = int(1000 / (self.stress_delay * self.duplicates))
        self.report_data[str(self.stress_delay)]['pkts_per_sec_actual'] = (num_pkts_sent / (TIME_PER_DELAY_FIRST if self.stress_delay == STRESS_DEFAULT_DELAYS[0] else TIME_PER_DELAY))
        self.report_data[str(self.stress_delay)]['percent_of_false_recieved'] = 100 - (num_pkts_received * 100 / num_pkts_sent)

        self.ts_records_arr[delay_idx].validate_timestamps(self.mqtt_pkts)
        
        if self.stress_delay == self.delays[-1]:
            for delay in self.delays:
                delay = str(delay)
                report.append((f'Test - {self.report_data[delay]["pkts_per_sec_desired"]} packets per second. Actual packet per second - ', self.report_data[delay]["pkts_per_sec_actual"]))
                report.append(((f'Number of packets sent'), self.report_data[delay]['pkts_sent']))
                report.append(((f'Number of packets received'), self.report_data[delay]['pkts_recieved']))
            self.add_report_header()
            self.add_to_stage_report(tabulate.tabulate(pd.DataFrame(report), showindex=False))   
            for idx, delay in enumerate(self.delays):
                if self.ts_records_arr[idx].is_ts_error():
                    self.add_to_stage_report(f"Timestamps errors during PPS {self.report_data[str(delay)]['pkts_per_sec_desired']}:")
                    self.ts_records_arr[idx].add_ts_errs_to_report(self, newline=False)
                    self.add_report_line_separator()
            self.add_to_stage_report(f'Stage data saved - {self.csv_path}')

            fig_data = pd.DataFrame.from_dict(self.report_data, orient='index')
            fig_data.reset_index(inplace=True)
            fig_data.rename(columns={'index': 'time_delay'}, inplace=True)
            fig = px.line(fig_data, x='pkts_per_sec_actual', y='percent_of_false_recieved', title='Percentage of packets not recieved by packets per second sent',
              labels={'pkts_per_sec_actual': 'Packets Sent Per Second', 'false_percentage': 'Percentage of packets not recieved'})
            graph_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
            
            # Generate HTML
            table_html = self.template_engine.render_template('table.html', dataframe=self.comparison.to_html(table_id=self.stage_name), table_id=self.stage_name)
            self.report_html = self.template_engine.render_template('stage.html', stage=self, 
                                                                    stage_report=self.report.split('\n'), graph=graph_div)
            
            return self.report
        
        
STAGES = [StressTestStage] 

class StressTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.all_messages_in_test = []
        self.stages = [stage(**self.__dict__) for stage in STAGES]
        self.result_indication = INFORMATIVE
        self.test_tooltip = "Stages attempting to stress test a maximum throughput"

    def run(self):
        super().run()
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.test_pass = PassCriteria.calc_for_test(self, stage)
            self.all_messages_in_test.extend(self.mqttc.get_all_messages_from_topic('data'))
    
