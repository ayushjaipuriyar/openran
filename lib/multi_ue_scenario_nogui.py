#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: srsRAN_multi_UE (No GUI)
# GNU Radio version: 3.10.12.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio import zeromq
import sys
import signal
from argparse import ArgumentParser
import time


class multi_ue_scenario_nogui(gr.top_block):

    def __init__(self, ue1_path_loss_db=0, ue2_path_loss_db=10, ue3_path_loss_db=20, slow_down_ratio=1):
        gr.top_block.__init__(self, "srsRAN_multi_UE_NoGUI", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.zmq_timeout = zmq_timeout = 100
        self.zmq_hwm = zmq_hwm = -1
        self.ue3_path_loss_db = ue3_path_loss_db
        self.ue2_path_loss_db = ue2_path_loss_db
        self.ue1_path_loss_db = ue1_path_loss_db
        self.slow_down_ratio = slow_down_ratio
        self.samp_rate = samp_rate = 11520000

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_req_source_1_0 = zeromq.req_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2201', zmq_timeout, False, zmq_hwm, False)
        self.zeromq_req_source_1 = zeromq.req_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2101', zmq_timeout, False, zmq_hwm, False)
        self.zeromq_req_source_0_0 = zeromq.req_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2301', zmq_timeout, False, zmq_hwm, False)
        self.zeromq_req_source_0 = zeromq.req_source(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2000', zmq_timeout, False, zmq_hwm, False)
        self.zeromq_rep_sink_0_2 = zeromq.rep_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2300', 100, False, zmq_hwm, True)
        self.zeromq_rep_sink_0_1 = zeromq.rep_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2001', zmq_timeout, False, zmq_hwm, True)
        self.zeromq_rep_sink_0_0 = zeromq.rep_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2200', zmq_timeout, False, zmq_hwm, True)
        self.zeromq_rep_sink_0 = zeromq.rep_sink(gr.sizeof_gr_complex, 1, 'tcp://127.0.0.1:2100', zmq_timeout, False, zmq_hwm, True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, (1.0*samp_rate/(1.0*slow_down_ratio)),True)
        self.blocks_multiply_const_vxx_0_1_1 = blocks.multiply_const_cc(10**(-1.0*ue2_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_cc(10**(-1.0*ue3_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_cc(10**(-1.0*ue1_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_cc(10**(-1.0*ue3_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_cc(10**(-1.0*ue2_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(10**(-1.0*ue1_path_loss_db/20.0))
        self.blocks_add_xx_0 = blocks.add_vcc(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.zeromq_rep_sink_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.zeromq_rep_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.zeromq_rep_sink_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_1, 0), (self.zeromq_rep_sink_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0_1_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_0_1_1, 0))
        self.connect((self.zeromq_req_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.zeromq_req_source_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.zeromq_req_source_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.zeromq_req_source_1_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))


    def get_zmq_timeout(self):
        return self.zmq_timeout

    def set_zmq_timeout(self, zmq_timeout):
        self.zmq_timeout = zmq_timeout

    def get_zmq_hwm(self):
        return self.zmq_hwm

    def set_zmq_hwm(self, zmq_hwm):
        self.zmq_hwm = zmq_hwm

    def get_ue3_path_loss_db(self):
        return self.ue3_path_loss_db

    def set_ue3_path_loss_db(self, ue3_path_loss_db):
        self.ue3_path_loss_db = ue3_path_loss_db
        self.blocks_multiply_const_vxx_0_0_0.set_k(10**(-1.0*self.ue3_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0_1_0.set_k(10**(-1.0*self.ue3_path_loss_db/20.0))

    def get_ue2_path_loss_db(self):
        return self.ue2_path_loss_db

    def set_ue2_path_loss_db(self, ue2_path_loss_db):
        self.ue2_path_loss_db = ue2_path_loss_db
        self.blocks_multiply_const_vxx_0_0.set_k(10**(-1.0*self.ue2_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0_1_1.set_k(10**(-1.0*self.ue2_path_loss_db/20.0))

    def get_ue1_path_loss_db(self):
        return self.ue1_path_loss_db

    def set_ue1_path_loss_db(self, ue1_path_loss_db):
        self.ue1_path_loss_db = ue1_path_loss_db
        self.blocks_multiply_const_vxx_0.set_k(10**(-1.0*self.ue1_path_loss_db/20.0))
        self.blocks_multiply_const_vxx_0_1.set_k(10**(-1.0*self.ue1_path_loss_db/20.0))

    def get_slow_down_ratio(self):
        return self.slow_down_ratio

    def set_slow_down_ratio(self, slow_down_ratio):
        self.slow_down_ratio = slow_down_ratio
        self.blocks_throttle_0.set_sample_rate((1.0*self.samp_rate/(1.0*self.slow_down_ratio)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate((1.0*self.samp_rate/(1.0*self.slow_down_ratio)))


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--ue1-path-loss", dest="ue1_path_loss_db", type=float, default=0.0,
        help="Set UE1 Path Loss [dB] [default=%(default)r]")
    parser.add_argument(
        "--ue2-path-loss", dest="ue2_path_loss_db", type=float, default=10.0,
        help="Set UE2 Path Loss [dB] [default=%(default)r]")
    parser.add_argument(
        "--ue3-path-loss", dest="ue3_path_loss_db", type=float, default=20.0,
        help="Set UE3 Path Loss [dB] [default=%(default)r]")
    parser.add_argument(
        "--slow-down-ratio", dest="slow_down_ratio", type=float, default=1.0,
        help="Set Time Slow Down Ratio [default=%(default)r]")
    # Legacy arguments for compatibility with old run_scenario.sh
    parser.add_argument("--snr-db", type=float, help="SNR (ignored, for compatibility)")
    parser.add_argument("--delay-ms", type=float, help="Delay (ignored, for compatibility)")
    parser.add_argument("--path-loss-db", type=float, help="Path loss (ignored, for compatibility)")
    parser.add_argument("--doppler-hz", type=float, help="Doppler (ignored, for compatibility)")
    return parser


def main(top_block_cls=multi_ue_scenario_nogui, options=None):
    if options is None:
        options = argument_parser().parse_args()

    tb = top_block_cls(
        ue1_path_loss_db=options.ue1_path_loss_db,
        ue2_path_loss_db=options.ue2_path_loss_db,
        ue3_path_loss_db=options.ue3_path_loss_db,
        slow_down_ratio=options.slow_down_ratio
    )

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    print(f"GNU Radio flowgraph started (No GUI)")
    print(f"  UE1 Path Loss: {options.ue1_path_loss_db} dB")
    print(f"  UE2 Path Loss: {options.ue2_path_loss_db} dB")
    print(f"  UE3 Path Loss: {options.ue3_path_loss_db} dB")
    print(f"  Slow Down Ratio: {options.slow_down_ratio}")
    print("Press Ctrl+C to stop")

    try:
        tb.wait()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
