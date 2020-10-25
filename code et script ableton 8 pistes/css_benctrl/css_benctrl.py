from __future__ import division
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import *
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement
import time
from itertools import imap, chain
from _Framework.Util import find_if
import collections
try:
	from user import *
except ImportError:
	from user import *

class css_benctrl(ControlSurface):
	def __init__(self, c_instance):
		super(css_benctrl, self).__init__(c_instance)
		with self.component_guard():
			global _map_modes
			_map_modes = Live.MidiMap.MapMode
			self.current_track_offset = 0
			self.current_scene_offset = 0
			# mixer
			global mixer
			num_tracks = 128
			num_returns = 24
			self._settings()
			self._inputs()
			self.turn_inputs_off()
			self.mixer = MixerComponent(num_tracks, num_returns)
			global active_mode
			self.debug_on = False
			self.device_parameter_banks()
			self.mode_list()
			self.set_active_mode(self.modes[0])
			self.listening_to_tracks()
			self.song().add_tracks_listener(self.listening_to_tracks)

	def _settings(self):
		self.global_feedback = "default"
		self.global_feedback_active = True
		self.global_LED_on = 127
		self.global_LED_off = 0
		self.controller_LED_on = 127
		self.controller_LED_off = 0
		self.led_on = self.controller_LED_on
		self.led_off = self.controller_LED_off

	def mode_list(self):
		global modes
		self.modes = {}
		self.modes[0] = "1"
		self.modes[1] = "169"

	def _inputs(self):
		self.input_map = [
			"midi_cc_ch_0_val_7",
			"midi_cc_ch_1_val_7",
			"midi_cc_ch_2_val_7",
			"midi_cc_ch_3_val_7",
			"midi_cc_ch_4_val_7",
			"midi_cc_ch_5_val_7",
			"midi_cc_ch_6_val_7",
			"midi_cc_ch_7_val_7",
			"midi_cc_ch_0_val_94",
			"midi_cc_ch_1_val_94",
			"midi_cc_ch_2_val_94",
			"midi_cc_ch_3_val_94",
			"midi_cc_ch_4_val_94",
			"midi_cc_ch_5_val_94",
			"midi_cc_ch_6_val_94",
			"midi_cc_ch_7_val_94",
			"midi_cc_ch_15_val_120",
			"midi_cc_ch_8_val_94",
			"midi_cc_ch_9_val_94",
			"midi_cc_ch_15_val_85",
			"midi_cc_ch_15_val_86",
			"midi_cc_ch_15_val_87",
			"midi_cc_ch_15_val_88",
			"midi_cc_ch_15_val_89",
			"midi_cc_ch_15_val_90",
			"midi_cc_ch_15_val_91",
			"midi_cc_ch_15_val_92",
			"midi_cc_ch_15_val_24",
			"midi_cc_ch_15_val_25",
			"midi_cc_ch_15_val_26",
			"midi_cc_ch_15_val_27",
			"midi_cc_ch_15_val_28",
			"midi_cc_ch_15_val_29",
			"midi_cc_ch_15_val_31",
			"midi_cc_ch_15_val_119",
			"midi_cc_ch_0_val_81",
			"midi_cc_ch_1_val_81",
			"midi_cc_ch_2_val_81",
			"midi_cc_ch_3_val_81",
			"midi_cc_ch_4_val_81",
			"midi_cc_ch_5_val_81",
			"midi_cc_ch_6_val_81",
			"midi_cc_ch_7_val_81",
			"midi_cc_ch_0_val_10",
			"midi_cc_ch_1_val_10",
			"midi_cc_ch_2_val_10",
			"midi_cc_ch_3_val_10",
			"midi_cc_ch_4_val_10",
			"midi_cc_ch_5_val_10",
			"midi_cc_ch_6_val_10",
			"midi_cc_ch_7_val_10",
			"midi_cc_ch_0_val_70",
			"midi_cc_ch_1_val_70",
			"midi_cc_ch_2_val_70",
			"midi_cc_ch_3_val_70",
			"midi_cc_ch_4_val_70",
			"midi_cc_ch_5_val_70",
			"midi_cc_ch_6_val_70",
			"midi_cc_ch_7_val_70",
			"midi_cc_ch_0_val_71",
			"midi_cc_ch_1_val_71",
			"midi_cc_ch_2_val_71",
			"midi_cc_ch_3_val_71",
			"midi_cc_ch_4_val_71",
			"midi_cc_ch_5_val_71",
			"midi_cc_ch_6_val_71",
			"midi_cc_ch_7_val_71",
			"midi_cc_ch_0_val_83",
			"midi_cc_ch_1_val_83",
			"midi_cc_ch_2_val_83",
			"midi_cc_ch_3_val_83",
			"midi_cc_ch_4_val_83",
			"midi_cc_ch_5_val_83",
			"midi_cc_ch_6_val_83",
			"midi_cc_ch_7_val_83",
			"midi_cc_ch_0_val_82",
			"midi_cc_ch_1_val_82",
			"midi_cc_ch_2_val_82",
			"midi_cc_ch_3_val_82",
			"midi_cc_ch_4_val_82",
			"midi_cc_ch_5_val_82",
			"midi_cc_ch_6_val_82",
			"midi_cc_ch_7_val_82",
			"midi_cc_ch_8_val_81",
			"midi_cc_ch_8_val_10",
			"midi_cc_ch_8_val_70",
			"midi_cc_ch_8_val_71",
			"midi_cc_ch_8_val_83",
			"midi_cc_ch_8_val_82",
			"midi_cc_ch_9_val_82",
			"midi_cc_ch_9_val_83",
			"midi_cc_ch_9_val_71",
			"midi_cc_ch_9_val_70",
			"midi_cc_ch_9_val_10",
			"midi_cc_ch_9_val_81",
			"midi_cc_ch_10_val_81",
			"midi_cc_ch_11_val_81",
			"midi_cc_ch_10_val_10",
			"midi_cc_ch_11_val_10",
			"midi_cc_ch_10_val_70",
			"midi_cc_ch_11_val_70",
			"midi_cc_ch_10_val_71",
			"midi_cc_ch_11_val_71",
			"midi_cc_ch_10_val_83",
			"midi_cc_ch_11_val_83",
			"midi_cc_ch_10_val_82",
			"midi_cc_ch_11_val_82",
			"midi_cc_ch_10_val_94",
			"midi_cc_ch_11_val_94",
			"midi_cc_ch_12_val_94",
			"midi_cc_ch_13_val_94",
			"midi_cc_ch_14_val_94",
			"midi_cc_ch_15_val_94",
			"midi_cc_ch_12_val_82",
			"midi_cc_ch_13_val_82",
			"midi_cc_ch_14_val_82",
			"midi_cc_ch_15_val_82",
			"midi_cc_ch_12_val_83",
			"midi_cc_ch_13_val_83",
			"midi_cc_ch_14_val_83",
			"midi_cc_ch_15_val_83",
			"midi_cc_ch_12_val_71",
			"midi_cc_ch_13_val_71",
			"midi_cc_ch_14_val_71",
			"midi_cc_ch_15_val_71",
			"midi_cc_ch_12_val_70",
			"midi_cc_ch_13_val_70",
			"midi_cc_ch_14_val_70",
			"midi_cc_ch_15_val_70",
			"midi_cc_ch_12_val_10",
			"midi_cc_ch_13_val_10",
			"midi_cc_ch_14_val_10",
			"midi_cc_ch_15_val_10",
			"midi_cc_ch_12_val_81",
			"midi_cc_ch_13_val_81",
			"midi_cc_ch_14_val_81",
			"midi_cc_ch_15_val_81",
			"midi_cc_ch_15_val_121",
			"midi_cc_ch_8_val_7",
			"midi_cc_ch_9_val_7",
			"midi_cc_ch_10_val_7",
			"midi_cc_ch_11_val_7",
			"midi_cc_ch_12_val_7",
			"midi_cc_ch_13_val_7",
			"midi_cc_ch_14_val_7",
			"midi_cc_ch_15_val_7"]
		self.midi_cc_ch_0_val_7 = EncoderElement(MIDI_CC_TYPE, 0, 7, _map_modes.absolute)
		self.midi_cc_ch_0_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_7 = EncoderElement(MIDI_CC_TYPE, 1, 7, _map_modes.absolute)
		self.midi_cc_ch_1_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_7 = EncoderElement(MIDI_CC_TYPE, 2, 7, _map_modes.absolute)
		self.midi_cc_ch_2_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_7 = EncoderElement(MIDI_CC_TYPE, 3, 7, _map_modes.absolute)
		self.midi_cc_ch_3_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_7 = EncoderElement(MIDI_CC_TYPE, 4, 7, _map_modes.absolute)
		self.midi_cc_ch_4_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_7 = EncoderElement(MIDI_CC_TYPE, 5, 7, _map_modes.absolute)
		self.midi_cc_ch_5_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_7 = EncoderElement(MIDI_CC_TYPE, 6, 7, _map_modes.absolute)
		self.midi_cc_ch_6_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_7 = EncoderElement(MIDI_CC_TYPE, 7, 7, _map_modes.absolute)
		self.midi_cc_ch_7_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 94)
		self.midi_cc_ch_0_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 1, 94)
		self.midi_cc_ch_1_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_1_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 2, 94)
		self.midi_cc_ch_2_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_2_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 3, 94)
		self.midi_cc_ch_3_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_3_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 4, 94)
		self.midi_cc_ch_4_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_4_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 5, 94)
		self.midi_cc_ch_5_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_5_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 6, 94)
		self.midi_cc_ch_6_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_6_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 7, 94)
		self.midi_cc_ch_7_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_7_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_120 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 15, 120)
		self.midi_cc_ch_15_val_120.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_15_val_120.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 8, 94)
		self.midi_cc_ch_8_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_8_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 9, 94)
		self.midi_cc_ch_9_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_9_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_85 = EncoderElement(MIDI_CC_TYPE, 15, 85, _map_modes.absolute)
		self.midi_cc_ch_15_val_85.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_86 = EncoderElement(MIDI_CC_TYPE, 15, 86, _map_modes.absolute)
		self.midi_cc_ch_15_val_86.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_87 = EncoderElement(MIDI_CC_TYPE, 15, 87, _map_modes.absolute)
		self.midi_cc_ch_15_val_87.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_88 = EncoderElement(MIDI_CC_TYPE, 15, 88, _map_modes.absolute)
		self.midi_cc_ch_15_val_88.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_89 = EncoderElement(MIDI_CC_TYPE, 15, 89, _map_modes.absolute)
		self.midi_cc_ch_15_val_89.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_90 = EncoderElement(MIDI_CC_TYPE, 15, 90, _map_modes.absolute)
		self.midi_cc_ch_15_val_90.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_91 = EncoderElement(MIDI_CC_TYPE, 15, 91, _map_modes.absolute)
		self.midi_cc_ch_15_val_91.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_92 = EncoderElement(MIDI_CC_TYPE, 15, 92, _map_modes.absolute)
		self.midi_cc_ch_15_val_92.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_24 = EncoderElement(MIDI_CC_TYPE, 15, 24, _map_modes.absolute)
		self.midi_cc_ch_15_val_24.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_25 = EncoderElement(MIDI_CC_TYPE, 15, 25, _map_modes.absolute)
		self.midi_cc_ch_15_val_25.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_26 = EncoderElement(MIDI_CC_TYPE, 15, 26, _map_modes.absolute)
		self.midi_cc_ch_15_val_26.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_27 = EncoderElement(MIDI_CC_TYPE, 15, 27, _map_modes.absolute)
		self.midi_cc_ch_15_val_27.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_28 = EncoderElement(MIDI_CC_TYPE, 15, 28, _map_modes.absolute)
		self.midi_cc_ch_15_val_28.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_29 = EncoderElement(MIDI_CC_TYPE, 15, 29, _map_modes.absolute)
		self.midi_cc_ch_15_val_29.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_31 = EncoderElement(MIDI_CC_TYPE, 15, 31, _map_modes.absolute)
		self.midi_cc_ch_15_val_31.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_119 = EncoderElement(MIDI_CC_TYPE, 15, 119, _map_modes.absolute)
		self.midi_cc_ch_15_val_119.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_81 = EncoderElement(MIDI_CC_TYPE, 0, 81, _map_modes.absolute)
		self.midi_cc_ch_0_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_81 = EncoderElement(MIDI_CC_TYPE, 1, 81, _map_modes.absolute)
		self.midi_cc_ch_1_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_81 = EncoderElement(MIDI_CC_TYPE, 2, 81, _map_modes.absolute)
		self.midi_cc_ch_2_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_81 = EncoderElement(MIDI_CC_TYPE, 3, 81, _map_modes.absolute)
		self.midi_cc_ch_3_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_81 = EncoderElement(MIDI_CC_TYPE, 4, 81, _map_modes.absolute)
		self.midi_cc_ch_4_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_81 = EncoderElement(MIDI_CC_TYPE, 5, 81, _map_modes.absolute)
		self.midi_cc_ch_5_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_81 = EncoderElement(MIDI_CC_TYPE, 6, 81, _map_modes.absolute)
		self.midi_cc_ch_6_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_81 = EncoderElement(MIDI_CC_TYPE, 7, 81, _map_modes.absolute)
		self.midi_cc_ch_7_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_10 = EncoderElement(MIDI_CC_TYPE, 0, 10, _map_modes.absolute)
		self.midi_cc_ch_0_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_10 = EncoderElement(MIDI_CC_TYPE, 1, 10, _map_modes.absolute)
		self.midi_cc_ch_1_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_10 = EncoderElement(MIDI_CC_TYPE, 2, 10, _map_modes.absolute)
		self.midi_cc_ch_2_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_10 = EncoderElement(MIDI_CC_TYPE, 3, 10, _map_modes.absolute)
		self.midi_cc_ch_3_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_10 = EncoderElement(MIDI_CC_TYPE, 4, 10, _map_modes.absolute)
		self.midi_cc_ch_4_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_10 = EncoderElement(MIDI_CC_TYPE, 5, 10, _map_modes.absolute)
		self.midi_cc_ch_5_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_10 = EncoderElement(MIDI_CC_TYPE, 6, 10, _map_modes.absolute)
		self.midi_cc_ch_6_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_10 = EncoderElement(MIDI_CC_TYPE, 7, 10, _map_modes.absolute)
		self.midi_cc_ch_7_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_70 = EncoderElement(MIDI_CC_TYPE, 0, 70, _map_modes.absolute)
		self.midi_cc_ch_0_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_70 = EncoderElement(MIDI_CC_TYPE, 1, 70, _map_modes.absolute)
		self.midi_cc_ch_1_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_70 = EncoderElement(MIDI_CC_TYPE, 2, 70, _map_modes.absolute)
		self.midi_cc_ch_2_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_70 = EncoderElement(MIDI_CC_TYPE, 3, 70, _map_modes.absolute)
		self.midi_cc_ch_3_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_70 = EncoderElement(MIDI_CC_TYPE, 4, 70, _map_modes.absolute)
		self.midi_cc_ch_4_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_70 = EncoderElement(MIDI_CC_TYPE, 5, 70, _map_modes.absolute)
		self.midi_cc_ch_5_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_70 = EncoderElement(MIDI_CC_TYPE, 6, 70, _map_modes.absolute)
		self.midi_cc_ch_6_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_70 = EncoderElement(MIDI_CC_TYPE, 7, 70, _map_modes.absolute)
		self.midi_cc_ch_7_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_71 = EncoderElement(MIDI_CC_TYPE, 0, 71, _map_modes.absolute)
		self.midi_cc_ch_0_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_71 = EncoderElement(MIDI_CC_TYPE, 1, 71, _map_modes.absolute)
		self.midi_cc_ch_1_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_71 = EncoderElement(MIDI_CC_TYPE, 2, 71, _map_modes.absolute)
		self.midi_cc_ch_2_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_71 = EncoderElement(MIDI_CC_TYPE, 3, 71, _map_modes.absolute)
		self.midi_cc_ch_3_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_71 = EncoderElement(MIDI_CC_TYPE, 4, 71, _map_modes.absolute)
		self.midi_cc_ch_4_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_71 = EncoderElement(MIDI_CC_TYPE, 5, 71, _map_modes.absolute)
		self.midi_cc_ch_5_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_71 = EncoderElement(MIDI_CC_TYPE, 6, 71, _map_modes.absolute)
		self.midi_cc_ch_6_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_71 = EncoderElement(MIDI_CC_TYPE, 7, 71, _map_modes.absolute)
		self.midi_cc_ch_7_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_83 = EncoderElement(MIDI_CC_TYPE, 0, 83, _map_modes.absolute)
		self.midi_cc_ch_0_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_83 = EncoderElement(MIDI_CC_TYPE, 1, 83, _map_modes.absolute)
		self.midi_cc_ch_1_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_83 = EncoderElement(MIDI_CC_TYPE, 2, 83, _map_modes.absolute)
		self.midi_cc_ch_2_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_83 = EncoderElement(MIDI_CC_TYPE, 3, 83, _map_modes.absolute)
		self.midi_cc_ch_3_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_83 = EncoderElement(MIDI_CC_TYPE, 4, 83, _map_modes.absolute)
		self.midi_cc_ch_4_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_83 = EncoderElement(MIDI_CC_TYPE, 5, 83, _map_modes.absolute)
		self.midi_cc_ch_5_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_83 = EncoderElement(MIDI_CC_TYPE, 6, 83, _map_modes.absolute)
		self.midi_cc_ch_6_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_83 = EncoderElement(MIDI_CC_TYPE, 7, 83, _map_modes.absolute)
		self.midi_cc_ch_7_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_82 = EncoderElement(MIDI_CC_TYPE, 0, 82, _map_modes.absolute)
		self.midi_cc_ch_0_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_82 = EncoderElement(MIDI_CC_TYPE, 1, 82, _map_modes.absolute)
		self.midi_cc_ch_1_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_82 = EncoderElement(MIDI_CC_TYPE, 2, 82, _map_modes.absolute)
		self.midi_cc_ch_2_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_82 = EncoderElement(MIDI_CC_TYPE, 3, 82, _map_modes.absolute)
		self.midi_cc_ch_3_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_82 = EncoderElement(MIDI_CC_TYPE, 4, 82, _map_modes.absolute)
		self.midi_cc_ch_4_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_82 = EncoderElement(MIDI_CC_TYPE, 5, 82, _map_modes.absolute)
		self.midi_cc_ch_5_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_82 = EncoderElement(MIDI_CC_TYPE, 6, 82, _map_modes.absolute)
		self.midi_cc_ch_6_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_7_val_82 = EncoderElement(MIDI_CC_TYPE, 7, 82, _map_modes.absolute)
		self.midi_cc_ch_7_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_81 = EncoderElement(MIDI_CC_TYPE, 8, 81, _map_modes.absolute)
		self.midi_cc_ch_8_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_10 = EncoderElement(MIDI_CC_TYPE, 8, 10, _map_modes.absolute)
		self.midi_cc_ch_8_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_70 = EncoderElement(MIDI_CC_TYPE, 8, 70, _map_modes.absolute)
		self.midi_cc_ch_8_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_71 = EncoderElement(MIDI_CC_TYPE, 8, 71, _map_modes.absolute)
		self.midi_cc_ch_8_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_83 = EncoderElement(MIDI_CC_TYPE, 8, 83, _map_modes.absolute)
		self.midi_cc_ch_8_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_82 = EncoderElement(MIDI_CC_TYPE, 8, 82, _map_modes.absolute)
		self.midi_cc_ch_8_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_82 = EncoderElement(MIDI_CC_TYPE, 9, 82, _map_modes.absolute)
		self.midi_cc_ch_9_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_83 = EncoderElement(MIDI_CC_TYPE, 9, 83, _map_modes.absolute)
		self.midi_cc_ch_9_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_71 = EncoderElement(MIDI_CC_TYPE, 9, 71, _map_modes.absolute)
		self.midi_cc_ch_9_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_70 = EncoderElement(MIDI_CC_TYPE, 9, 70, _map_modes.absolute)
		self.midi_cc_ch_9_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_10 = EncoderElement(MIDI_CC_TYPE, 9, 10, _map_modes.absolute)
		self.midi_cc_ch_9_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_81 = EncoderElement(MIDI_CC_TYPE, 9, 81, _map_modes.absolute)
		self.midi_cc_ch_9_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_81 = EncoderElement(MIDI_CC_TYPE, 10, 81, _map_modes.absolute)
		self.midi_cc_ch_10_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_81 = EncoderElement(MIDI_CC_TYPE, 11, 81, _map_modes.absolute)
		self.midi_cc_ch_11_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_10 = EncoderElement(MIDI_CC_TYPE, 10, 10, _map_modes.absolute)
		self.midi_cc_ch_10_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_10 = EncoderElement(MIDI_CC_TYPE, 11, 10, _map_modes.absolute)
		self.midi_cc_ch_11_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_70 = EncoderElement(MIDI_CC_TYPE, 10, 70, _map_modes.absolute)
		self.midi_cc_ch_10_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_70 = EncoderElement(MIDI_CC_TYPE, 11, 70, _map_modes.absolute)
		self.midi_cc_ch_11_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_71 = EncoderElement(MIDI_CC_TYPE, 10, 71, _map_modes.absolute)
		self.midi_cc_ch_10_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_71 = EncoderElement(MIDI_CC_TYPE, 11, 71, _map_modes.absolute)
		self.midi_cc_ch_11_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_83 = EncoderElement(MIDI_CC_TYPE, 10, 83, _map_modes.absolute)
		self.midi_cc_ch_10_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_83 = EncoderElement(MIDI_CC_TYPE, 11, 83, _map_modes.absolute)
		self.midi_cc_ch_11_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_82 = EncoderElement(MIDI_CC_TYPE, 10, 82, _map_modes.absolute)
		self.midi_cc_ch_10_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_82 = EncoderElement(MIDI_CC_TYPE, 11, 82, _map_modes.absolute)
		self.midi_cc_ch_11_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 10, 94)
		self.midi_cc_ch_10_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_10_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 11, 94)
		self.midi_cc_ch_11_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_11_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 12, 94)
		self.midi_cc_ch_12_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_12_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 13, 94)
		self.midi_cc_ch_13_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_13_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 14, 94)
		self.midi_cc_ch_14_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_14_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_94 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 15, 94)
		self.midi_cc_ch_15_val_94.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_15_val_94.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_82 = EncoderElement(MIDI_CC_TYPE, 12, 82, _map_modes.absolute)
		self.midi_cc_ch_12_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_82 = EncoderElement(MIDI_CC_TYPE, 13, 82, _map_modes.absolute)
		self.midi_cc_ch_13_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_82 = EncoderElement(MIDI_CC_TYPE, 14, 82, _map_modes.absolute)
		self.midi_cc_ch_14_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_82 = EncoderElement(MIDI_CC_TYPE, 15, 82, _map_modes.absolute)
		self.midi_cc_ch_15_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_83 = EncoderElement(MIDI_CC_TYPE, 12, 83, _map_modes.absolute)
		self.midi_cc_ch_12_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_83 = EncoderElement(MIDI_CC_TYPE, 13, 83, _map_modes.absolute)
		self.midi_cc_ch_13_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_83 = EncoderElement(MIDI_CC_TYPE, 14, 83, _map_modes.absolute)
		self.midi_cc_ch_14_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_83 = EncoderElement(MIDI_CC_TYPE, 15, 83, _map_modes.absolute)
		self.midi_cc_ch_15_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_71 = EncoderElement(MIDI_CC_TYPE, 12, 71, _map_modes.absolute)
		self.midi_cc_ch_12_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_71 = EncoderElement(MIDI_CC_TYPE, 13, 71, _map_modes.absolute)
		self.midi_cc_ch_13_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_71 = EncoderElement(MIDI_CC_TYPE, 14, 71, _map_modes.absolute)
		self.midi_cc_ch_14_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_71 = EncoderElement(MIDI_CC_TYPE, 15, 71, _map_modes.absolute)
		self.midi_cc_ch_15_val_71.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_70 = EncoderElement(MIDI_CC_TYPE, 12, 70, _map_modes.absolute)
		self.midi_cc_ch_12_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_70 = EncoderElement(MIDI_CC_TYPE, 13, 70, _map_modes.absolute)
		self.midi_cc_ch_13_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_70 = EncoderElement(MIDI_CC_TYPE, 14, 70, _map_modes.absolute)
		self.midi_cc_ch_14_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_70 = EncoderElement(MIDI_CC_TYPE, 15, 70, _map_modes.absolute)
		self.midi_cc_ch_15_val_70.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_10 = EncoderElement(MIDI_CC_TYPE, 12, 10, _map_modes.absolute)
		self.midi_cc_ch_12_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_10 = EncoderElement(MIDI_CC_TYPE, 13, 10, _map_modes.absolute)
		self.midi_cc_ch_13_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_10 = EncoderElement(MIDI_CC_TYPE, 14, 10, _map_modes.absolute)
		self.midi_cc_ch_14_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_10 = EncoderElement(MIDI_CC_TYPE, 15, 10, _map_modes.absolute)
		self.midi_cc_ch_15_val_10.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_81 = EncoderElement(MIDI_CC_TYPE, 12, 81, _map_modes.absolute)
		self.midi_cc_ch_12_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_81 = EncoderElement(MIDI_CC_TYPE, 13, 81, _map_modes.absolute)
		self.midi_cc_ch_13_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_81 = EncoderElement(MIDI_CC_TYPE, 14, 81, _map_modes.absolute)
		self.midi_cc_ch_14_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_81 = EncoderElement(MIDI_CC_TYPE, 15, 81, _map_modes.absolute)
		self.midi_cc_ch_15_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_121 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 15, 121)
		self.midi_cc_ch_15_val_121.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_15_val_121.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_8_val_7 = EncoderElement(MIDI_CC_TYPE, 8, 7, _map_modes.absolute)
		self.midi_cc_ch_8_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_9_val_7 = EncoderElement(MIDI_CC_TYPE, 9, 7, _map_modes.absolute)
		self.midi_cc_ch_9_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_10_val_7 = EncoderElement(MIDI_CC_TYPE, 10, 7, _map_modes.absolute)
		self.midi_cc_ch_10_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_11_val_7 = EncoderElement(MIDI_CC_TYPE, 11, 7, _map_modes.absolute)
		self.midi_cc_ch_11_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_12_val_7 = EncoderElement(MIDI_CC_TYPE, 12, 7, _map_modes.absolute)
		self.midi_cc_ch_12_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_13_val_7 = EncoderElement(MIDI_CC_TYPE, 13, 7, _map_modes.absolute)
		self.midi_cc_ch_13_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_14_val_7 = EncoderElement(MIDI_CC_TYPE, 14, 7, _map_modes.absolute)
		self.midi_cc_ch_14_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_7 = EncoderElement(MIDI_CC_TYPE, 15, 7, _map_modes.absolute)
		self.midi_cc_ch_15_val_7.add_value_listener(self.placehold_listener,identify_sender= False)

	def _mode1(self):
		self.show_message("Mode 1 is active")
		# Session Box
		num_tracks = 8
		num_scenes = 2
		track_offset = 0
		scene_offset = self.current_scene_offset
		combination_mode = "on"
		feedbackArr = {}
		feedbackArr["ClipRecording"] = None
		feedbackArr["ClipStarted"] = None
		feedbackArr["ClipStopped"] = None
		feedbackArr["ClipTriggeredPlay"] = None
		feedbackArr["ClipTriggeredRecord"] = None
		feedbackArr["NoScene"] = None
		feedbackArr["RecordButton"] = None
		feedbackArr["Scene"] = None
		feedbackArr["SceneTriggered"] = None
		feedbackArr["StopAllOff"] = None
		feedbackArr["StopAllOn"] = None
		feedbackArr["StopClip"] = None
		feedbackArr["StopClipTriggered"] = None
		feedbackArr["StopTrackPlaying"] = None
		feedbackArr["StopTrackStopped"] = None
		clips = []
		stop_all = []
		stop_tracks = []
		scene_launch = []
		self.session_box(num_tracks, num_scenes, track_offset, scene_offset, clips, stop_all, stop_tracks, scene_launch, feedbackArr, combination_mode)
		# /Session Box end
		self.midi_cc_ch_0_val_7.add_value_listener(self.midi_cc_ch_0_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_82.add_value_listener(self.midi_cc_ch_0_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_94.add_value_listener(self.midi_cc_ch_0_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_83.add_value_listener(self.midi_cc_ch_0_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_71.add_value_listener(self.midi_cc_ch_0_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_70.add_value_listener(self.midi_cc_ch_0_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_10.add_value_listener(self.midi_cc_ch_0_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_83.add_value_listener(self.midi_cc_ch_1_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_71.add_value_listener(self.midi_cc_ch_1_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_70.add_value_listener(self.midi_cc_ch_1_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_10.add_value_listener(self.midi_cc_ch_1_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_7.add_value_listener(self.midi_cc_ch_1_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_82.add_value_listener(self.midi_cc_ch_1_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_94.add_value_listener(self.midi_cc_ch_1_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_83.add_value_listener(self.midi_cc_ch_2_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_71.add_value_listener(self.midi_cc_ch_2_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_70.add_value_listener(self.midi_cc_ch_2_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_10.add_value_listener(self.midi_cc_ch_2_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_7.add_value_listener(self.midi_cc_ch_2_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_82.add_value_listener(self.midi_cc_ch_2_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_94.add_value_listener(self.midi_cc_ch_2_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_83.add_value_listener(self.midi_cc_ch_3_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_71.add_value_listener(self.midi_cc_ch_3_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_70.add_value_listener(self.midi_cc_ch_3_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_10.add_value_listener(self.midi_cc_ch_3_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_7.add_value_listener(self.midi_cc_ch_3_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_82.add_value_listener(self.midi_cc_ch_3_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_94.add_value_listener(self.midi_cc_ch_3_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_83.add_value_listener(self.midi_cc_ch_4_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_71.add_value_listener(self.midi_cc_ch_4_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_70.add_value_listener(self.midi_cc_ch_4_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_10.add_value_listener(self.midi_cc_ch_4_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_7.add_value_listener(self.midi_cc_ch_4_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_82.add_value_listener(self.midi_cc_ch_4_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_94.add_value_listener(self.midi_cc_ch_4_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_83.add_value_listener(self.midi_cc_ch_5_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_71.add_value_listener(self.midi_cc_ch_5_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_70.add_value_listener(self.midi_cc_ch_5_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_10.add_value_listener(self.midi_cc_ch_5_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_7.add_value_listener(self.midi_cc_ch_5_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_82.add_value_listener(self.midi_cc_ch_5_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_94.add_value_listener(self.midi_cc_ch_5_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_83.add_value_listener(self.midi_cc_ch_6_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_71.add_value_listener(self.midi_cc_ch_6_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_70.add_value_listener(self.midi_cc_ch_6_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_10.add_value_listener(self.midi_cc_ch_6_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_7.add_value_listener(self.midi_cc_ch_6_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_82.add_value_listener(self.midi_cc_ch_6_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_94.add_value_listener(self.midi_cc_ch_6_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_7_val_83.add_value_listener(self.midi_cc_ch_7_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_7_val_71.add_value_listener(self.midi_cc_ch_7_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_7_val_70.add_value_listener(self.midi_cc_ch_7_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_7_val_10.add_value_listener(self.midi_cc_ch_7_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_7_val_7.add_value_listener(self.midi_cc_ch_7_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_7_val_82.add_value_listener(self.midi_cc_ch_7_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_7_val_94.add_value_listener(self.midi_cc_ch_7_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_85.add_value_listener(self.midi_cc_ch_15_val_85_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_86.add_value_listener(self.midi_cc_ch_15_val_86_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_87.add_value_listener(self.midi_cc_ch_15_val_87_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_88.add_value_listener(self.midi_cc_ch_15_val_88_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_89.add_value_listener(self.midi_cc_ch_15_val_89_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_90.add_value_listener(self.midi_cc_ch_15_val_90_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_91.add_value_listener(self.midi_cc_ch_15_val_91_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_92.add_value_listener(self.midi_cc_ch_15_val_92_mode1_listener,identify_sender= False)
		self.midi_cc_ch_8_val_83.add_value_listener(self.midi_cc_ch_8_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_8_val_71.add_value_listener(self.midi_cc_ch_8_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_8_val_70.add_value_listener(self.midi_cc_ch_8_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_8_val_10.add_value_listener(self.midi_cc_ch_8_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_8_val_7.add_value_listener(self.midi_cc_ch_8_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_8_val_82.add_value_listener(self.midi_cc_ch_8_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_8_val_94.add_value_listener(self.midi_cc_ch_8_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_9_val_83.add_value_listener(self.midi_cc_ch_9_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_9_val_71.add_value_listener(self.midi_cc_ch_9_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_9_val_70.add_value_listener(self.midi_cc_ch_9_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_9_val_10.add_value_listener(self.midi_cc_ch_9_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_9_val_7.add_value_listener(self.midi_cc_ch_9_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_9_val_82.add_value_listener(self.midi_cc_ch_9_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_9_val_94.add_value_listener(self.midi_cc_ch_9_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_10_val_83.add_value_listener(self.midi_cc_ch_10_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_10_val_71.add_value_listener(self.midi_cc_ch_10_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_10_val_70.add_value_listener(self.midi_cc_ch_10_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_10_val_10.add_value_listener(self.midi_cc_ch_10_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_10_val_7.add_value_listener(self.midi_cc_ch_10_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_10_val_82.add_value_listener(self.midi_cc_ch_10_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_10_val_94.add_value_listener(self.midi_cc_ch_10_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_11_val_83.add_value_listener(self.midi_cc_ch_11_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_11_val_71.add_value_listener(self.midi_cc_ch_11_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_11_val_70.add_value_listener(self.midi_cc_ch_11_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_11_val_10.add_value_listener(self.midi_cc_ch_11_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_11_val_7.add_value_listener(self.midi_cc_ch_11_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_11_val_82.add_value_listener(self.midi_cc_ch_11_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_11_val_94.add_value_listener(self.midi_cc_ch_11_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_12_val_83.add_value_listener(self.midi_cc_ch_12_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_12_val_71.add_value_listener(self.midi_cc_ch_12_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_12_val_70.add_value_listener(self.midi_cc_ch_12_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_12_val_10.add_value_listener(self.midi_cc_ch_12_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_12_val_7.add_value_listener(self.midi_cc_ch_12_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_12_val_82.add_value_listener(self.midi_cc_ch_12_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_12_val_94.add_value_listener(self.midi_cc_ch_12_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_13_val_83.add_value_listener(self.midi_cc_ch_13_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_13_val_71.add_value_listener(self.midi_cc_ch_13_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_13_val_70.add_value_listener(self.midi_cc_ch_13_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_13_val_10.add_value_listener(self.midi_cc_ch_13_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_13_val_7.add_value_listener(self.midi_cc_ch_13_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_13_val_82.add_value_listener(self.midi_cc_ch_13_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_13_val_94.add_value_listener(self.midi_cc_ch_13_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_14_val_83.add_value_listener(self.midi_cc_ch_14_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_14_val_71.add_value_listener(self.midi_cc_ch_14_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_14_val_70.add_value_listener(self.midi_cc_ch_14_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_14_val_10.add_value_listener(self.midi_cc_ch_14_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_14_val_7.add_value_listener(self.midi_cc_ch_14_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_14_val_82.add_value_listener(self.midi_cc_ch_14_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_14_val_94.add_value_listener(self.midi_cc_ch_14_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_83.add_value_listener(self.midi_cc_ch_15_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_71.add_value_listener(self.midi_cc_ch_15_val_71_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_70.add_value_listener(self.midi_cc_ch_15_val_70_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_10.add_value_listener(self.midi_cc_ch_15_val_10_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_7.add_value_listener(self.midi_cc_ch_15_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_82.add_value_listener(self.midi_cc_ch_15_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_94.add_value_listener(self.midi_cc_ch_15_val_94_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_120.add_value_listener(self.midi_cc_ch_15_val_120_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_121.add_value_listener(self.midi_cc_ch_15_val_121_mode1_listener,identify_sender= False)
		self._mode1_configs()
		self._mode1_led_listeners()

	def _mode169(self):
		self.show_message("Mode 2 is active")
		self.midi_cc_ch_0_val_7.add_value_listener(self.midi_cc_ch_0_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_0_val_82.add_value_listener(self.midi_cc_ch_0_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_1_val_7.add_value_listener(self.midi_cc_ch_1_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_1_val_82.add_value_listener(self.midi_cc_ch_1_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_2_val_7.add_value_listener(self.midi_cc_ch_2_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_2_val_82.add_value_listener(self.midi_cc_ch_2_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_3_val_7.add_value_listener(self.midi_cc_ch_3_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_3_val_82.add_value_listener(self.midi_cc_ch_3_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_4_val_7.add_value_listener(self.midi_cc_ch_4_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_4_val_82.add_value_listener(self.midi_cc_ch_4_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_5_val_7.add_value_listener(self.midi_cc_ch_5_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_5_val_82.add_value_listener(self.midi_cc_ch_5_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_6_val_7.add_value_listener(self.midi_cc_ch_6_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_6_val_82.add_value_listener(self.midi_cc_ch_6_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_7_val_7.add_value_listener(self.midi_cc_ch_7_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_7_val_82.add_value_listener(self.midi_cc_ch_7_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_85.add_value_listener(self.midi_cc_ch_15_val_85_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_86.add_value_listener(self.midi_cc_ch_15_val_86_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_87.add_value_listener(self.midi_cc_ch_15_val_87_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_88.add_value_listener(self.midi_cc_ch_15_val_88_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_89.add_value_listener(self.midi_cc_ch_15_val_89_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_90.add_value_listener(self.midi_cc_ch_15_val_90_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_91.add_value_listener(self.midi_cc_ch_15_val_91_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_92.add_value_listener(self.midi_cc_ch_15_val_92_mode169_listener,identify_sender= False)
		self.midi_cc_ch_8_val_7.add_value_listener(self.midi_cc_ch_8_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_8_val_82.add_value_listener(self.midi_cc_ch_8_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_9_val_7.add_value_listener(self.midi_cc_ch_9_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_9_val_82.add_value_listener(self.midi_cc_ch_9_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_10_val_7.add_value_listener(self.midi_cc_ch_10_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_10_val_82.add_value_listener(self.midi_cc_ch_10_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_11_val_7.add_value_listener(self.midi_cc_ch_11_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_11_val_82.add_value_listener(self.midi_cc_ch_11_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_12_val_7.add_value_listener(self.midi_cc_ch_12_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_12_val_82.add_value_listener(self.midi_cc_ch_12_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_13_val_7.add_value_listener(self.midi_cc_ch_13_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_13_val_82.add_value_listener(self.midi_cc_ch_13_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_14_val_7.add_value_listener(self.midi_cc_ch_14_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_14_val_82.add_value_listener(self.midi_cc_ch_14_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_7.add_value_listener(self.midi_cc_ch_15_val_7_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_82.add_value_listener(self.midi_cc_ch_15_val_82_mode169_listener,identify_sender= False)
		self.midi_cc_ch_0_val_94.add_value_listener(self.midi_cc_ch_0_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_1_val_94.add_value_listener(self.midi_cc_ch_1_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_2_val_94.add_value_listener(self.midi_cc_ch_2_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_3_val_94.add_value_listener(self.midi_cc_ch_3_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_4_val_94.add_value_listener(self.midi_cc_ch_4_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_5_val_94.add_value_listener(self.midi_cc_ch_5_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_6_val_94.add_value_listener(self.midi_cc_ch_6_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_7_val_94.add_value_listener(self.midi_cc_ch_7_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_8_val_94.add_value_listener(self.midi_cc_ch_8_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_9_val_94.add_value_listener(self.midi_cc_ch_9_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_10_val_94.add_value_listener(self.midi_cc_ch_10_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_11_val_94.add_value_listener(self.midi_cc_ch_11_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_12_val_94.add_value_listener(self.midi_cc_ch_12_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_13_val_94.add_value_listener(self.midi_cc_ch_13_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_14_val_94.add_value_listener(self.midi_cc_ch_14_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_94.add_value_listener(self.midi_cc_ch_15_val_94_mode169_listener,identify_sender= False)
		self.midi_cc_ch_15_val_120.add_value_listener(self.midi_cc_ch_15_val_120_mode169_listener,identify_sender= False)
		self._mode169_configs()
		self._mode169_led_listeners()

	def _remove_mode1(self):
		combination_mode = "on"
		self.remove_session_box(combination_mode)
		self.midi_cc_ch_0_val_7.remove_value_listener(self.midi_cc_ch_0_val_7_mode1_listener)
		self.midi_cc_ch_0_val_82.remove_value_listener(self.midi_cc_ch_0_val_82_mode1_listener)
		self.midi_cc_ch_0_val_94.remove_value_listener(self.midi_cc_ch_0_val_94_mode1_listener)
		self.midi_cc_ch_0_val_83.remove_value_listener(self.midi_cc_ch_0_val_83_mode1_listener)
		self.midi_cc_ch_0_val_71.remove_value_listener(self.midi_cc_ch_0_val_71_mode1_listener)
		self.midi_cc_ch_0_val_70.remove_value_listener(self.midi_cc_ch_0_val_70_mode1_listener)
		self.midi_cc_ch_0_val_10.remove_value_listener(self.midi_cc_ch_0_val_10_mode1_listener)
		self.midi_cc_ch_1_val_83.remove_value_listener(self.midi_cc_ch_1_val_83_mode1_listener)
		self.midi_cc_ch_1_val_71.remove_value_listener(self.midi_cc_ch_1_val_71_mode1_listener)
		self.midi_cc_ch_1_val_70.remove_value_listener(self.midi_cc_ch_1_val_70_mode1_listener)
		self.midi_cc_ch_1_val_10.remove_value_listener(self.midi_cc_ch_1_val_10_mode1_listener)
		self.midi_cc_ch_1_val_7.remove_value_listener(self.midi_cc_ch_1_val_7_mode1_listener)
		self.midi_cc_ch_1_val_82.remove_value_listener(self.midi_cc_ch_1_val_82_mode1_listener)
		self.midi_cc_ch_1_val_94.remove_value_listener(self.midi_cc_ch_1_val_94_mode1_listener)
		self.midi_cc_ch_2_val_83.remove_value_listener(self.midi_cc_ch_2_val_83_mode1_listener)
		self.midi_cc_ch_2_val_71.remove_value_listener(self.midi_cc_ch_2_val_71_mode1_listener)
		self.midi_cc_ch_2_val_70.remove_value_listener(self.midi_cc_ch_2_val_70_mode1_listener)
		self.midi_cc_ch_2_val_10.remove_value_listener(self.midi_cc_ch_2_val_10_mode1_listener)
		self.midi_cc_ch_2_val_7.remove_value_listener(self.midi_cc_ch_2_val_7_mode1_listener)
		self.midi_cc_ch_2_val_82.remove_value_listener(self.midi_cc_ch_2_val_82_mode1_listener)
		self.midi_cc_ch_2_val_94.remove_value_listener(self.midi_cc_ch_2_val_94_mode1_listener)
		self.midi_cc_ch_3_val_83.remove_value_listener(self.midi_cc_ch_3_val_83_mode1_listener)
		self.midi_cc_ch_3_val_71.remove_value_listener(self.midi_cc_ch_3_val_71_mode1_listener)
		self.midi_cc_ch_3_val_70.remove_value_listener(self.midi_cc_ch_3_val_70_mode1_listener)
		self.midi_cc_ch_3_val_10.remove_value_listener(self.midi_cc_ch_3_val_10_mode1_listener)
		self.midi_cc_ch_3_val_7.remove_value_listener(self.midi_cc_ch_3_val_7_mode1_listener)
		self.midi_cc_ch_3_val_82.remove_value_listener(self.midi_cc_ch_3_val_82_mode1_listener)
		self.midi_cc_ch_3_val_94.remove_value_listener(self.midi_cc_ch_3_val_94_mode1_listener)
		self.midi_cc_ch_4_val_83.remove_value_listener(self.midi_cc_ch_4_val_83_mode1_listener)
		self.midi_cc_ch_4_val_71.remove_value_listener(self.midi_cc_ch_4_val_71_mode1_listener)
		self.midi_cc_ch_4_val_70.remove_value_listener(self.midi_cc_ch_4_val_70_mode1_listener)
		self.midi_cc_ch_4_val_10.remove_value_listener(self.midi_cc_ch_4_val_10_mode1_listener)
		self.midi_cc_ch_4_val_7.remove_value_listener(self.midi_cc_ch_4_val_7_mode1_listener)
		self.midi_cc_ch_4_val_82.remove_value_listener(self.midi_cc_ch_4_val_82_mode1_listener)
		self.midi_cc_ch_4_val_94.remove_value_listener(self.midi_cc_ch_4_val_94_mode1_listener)
		self.midi_cc_ch_5_val_83.remove_value_listener(self.midi_cc_ch_5_val_83_mode1_listener)
		self.midi_cc_ch_5_val_71.remove_value_listener(self.midi_cc_ch_5_val_71_mode1_listener)
		self.midi_cc_ch_5_val_70.remove_value_listener(self.midi_cc_ch_5_val_70_mode1_listener)
		self.midi_cc_ch_5_val_10.remove_value_listener(self.midi_cc_ch_5_val_10_mode1_listener)
		self.midi_cc_ch_5_val_7.remove_value_listener(self.midi_cc_ch_5_val_7_mode1_listener)
		self.midi_cc_ch_5_val_82.remove_value_listener(self.midi_cc_ch_5_val_82_mode1_listener)
		self.midi_cc_ch_5_val_94.remove_value_listener(self.midi_cc_ch_5_val_94_mode1_listener)
		self.midi_cc_ch_6_val_83.remove_value_listener(self.midi_cc_ch_6_val_83_mode1_listener)
		self.midi_cc_ch_6_val_71.remove_value_listener(self.midi_cc_ch_6_val_71_mode1_listener)
		self.midi_cc_ch_6_val_70.remove_value_listener(self.midi_cc_ch_6_val_70_mode1_listener)
		self.midi_cc_ch_6_val_10.remove_value_listener(self.midi_cc_ch_6_val_10_mode1_listener)
		self.midi_cc_ch_6_val_7.remove_value_listener(self.midi_cc_ch_6_val_7_mode1_listener)
		self.midi_cc_ch_6_val_82.remove_value_listener(self.midi_cc_ch_6_val_82_mode1_listener)
		self.midi_cc_ch_6_val_94.remove_value_listener(self.midi_cc_ch_6_val_94_mode1_listener)
		self.midi_cc_ch_7_val_83.remove_value_listener(self.midi_cc_ch_7_val_83_mode1_listener)
		self.midi_cc_ch_7_val_71.remove_value_listener(self.midi_cc_ch_7_val_71_mode1_listener)
		self.midi_cc_ch_7_val_70.remove_value_listener(self.midi_cc_ch_7_val_70_mode1_listener)
		self.midi_cc_ch_7_val_10.remove_value_listener(self.midi_cc_ch_7_val_10_mode1_listener)
		self.midi_cc_ch_7_val_7.remove_value_listener(self.midi_cc_ch_7_val_7_mode1_listener)
		self.midi_cc_ch_7_val_82.remove_value_listener(self.midi_cc_ch_7_val_82_mode1_listener)
		self.midi_cc_ch_7_val_94.remove_value_listener(self.midi_cc_ch_7_val_94_mode1_listener)
		self.midi_cc_ch_15_val_85.remove_value_listener(self.midi_cc_ch_15_val_85_mode1_listener)
		self.midi_cc_ch_15_val_86.remove_value_listener(self.midi_cc_ch_15_val_86_mode1_listener)
		self.midi_cc_ch_15_val_87.remove_value_listener(self.midi_cc_ch_15_val_87_mode1_listener)
		self.midi_cc_ch_15_val_88.remove_value_listener(self.midi_cc_ch_15_val_88_mode1_listener)
		self.midi_cc_ch_15_val_89.remove_value_listener(self.midi_cc_ch_15_val_89_mode1_listener)
		self.midi_cc_ch_15_val_90.remove_value_listener(self.midi_cc_ch_15_val_90_mode1_listener)
		self.midi_cc_ch_15_val_91.remove_value_listener(self.midi_cc_ch_15_val_91_mode1_listener)
		self.midi_cc_ch_15_val_92.remove_value_listener(self.midi_cc_ch_15_val_92_mode1_listener)
		self.midi_cc_ch_8_val_83.remove_value_listener(self.midi_cc_ch_8_val_83_mode1_listener)
		self.midi_cc_ch_8_val_71.remove_value_listener(self.midi_cc_ch_8_val_71_mode1_listener)
		self.midi_cc_ch_8_val_70.remove_value_listener(self.midi_cc_ch_8_val_70_mode1_listener)
		self.midi_cc_ch_8_val_10.remove_value_listener(self.midi_cc_ch_8_val_10_mode1_listener)
		self.midi_cc_ch_8_val_7.remove_value_listener(self.midi_cc_ch_8_val_7_mode1_listener)
		self.midi_cc_ch_8_val_82.remove_value_listener(self.midi_cc_ch_8_val_82_mode1_listener)
		self.midi_cc_ch_8_val_94.remove_value_listener(self.midi_cc_ch_8_val_94_mode1_listener)
		self.midi_cc_ch_9_val_83.remove_value_listener(self.midi_cc_ch_9_val_83_mode1_listener)
		self.midi_cc_ch_9_val_71.remove_value_listener(self.midi_cc_ch_9_val_71_mode1_listener)
		self.midi_cc_ch_9_val_70.remove_value_listener(self.midi_cc_ch_9_val_70_mode1_listener)
		self.midi_cc_ch_9_val_10.remove_value_listener(self.midi_cc_ch_9_val_10_mode1_listener)
		self.midi_cc_ch_9_val_7.remove_value_listener(self.midi_cc_ch_9_val_7_mode1_listener)
		self.midi_cc_ch_9_val_82.remove_value_listener(self.midi_cc_ch_9_val_82_mode1_listener)
		self.midi_cc_ch_9_val_94.remove_value_listener(self.midi_cc_ch_9_val_94_mode1_listener)
		self.midi_cc_ch_10_val_83.remove_value_listener(self.midi_cc_ch_10_val_83_mode1_listener)
		self.midi_cc_ch_10_val_71.remove_value_listener(self.midi_cc_ch_10_val_71_mode1_listener)
		self.midi_cc_ch_10_val_70.remove_value_listener(self.midi_cc_ch_10_val_70_mode1_listener)
		self.midi_cc_ch_10_val_10.remove_value_listener(self.midi_cc_ch_10_val_10_mode1_listener)
		self.midi_cc_ch_10_val_7.remove_value_listener(self.midi_cc_ch_10_val_7_mode1_listener)
		self.midi_cc_ch_10_val_82.remove_value_listener(self.midi_cc_ch_10_val_82_mode1_listener)
		self.midi_cc_ch_10_val_94.remove_value_listener(self.midi_cc_ch_10_val_94_mode1_listener)
		self.midi_cc_ch_11_val_83.remove_value_listener(self.midi_cc_ch_11_val_83_mode1_listener)
		self.midi_cc_ch_11_val_71.remove_value_listener(self.midi_cc_ch_11_val_71_mode1_listener)
		self.midi_cc_ch_11_val_70.remove_value_listener(self.midi_cc_ch_11_val_70_mode1_listener)
		self.midi_cc_ch_11_val_10.remove_value_listener(self.midi_cc_ch_11_val_10_mode1_listener)
		self.midi_cc_ch_11_val_7.remove_value_listener(self.midi_cc_ch_11_val_7_mode1_listener)
		self.midi_cc_ch_11_val_82.remove_value_listener(self.midi_cc_ch_11_val_82_mode1_listener)
		self.midi_cc_ch_11_val_94.remove_value_listener(self.midi_cc_ch_11_val_94_mode1_listener)
		self.midi_cc_ch_12_val_83.remove_value_listener(self.midi_cc_ch_12_val_83_mode1_listener)
		self.midi_cc_ch_12_val_71.remove_value_listener(self.midi_cc_ch_12_val_71_mode1_listener)
		self.midi_cc_ch_12_val_70.remove_value_listener(self.midi_cc_ch_12_val_70_mode1_listener)
		self.midi_cc_ch_12_val_10.remove_value_listener(self.midi_cc_ch_12_val_10_mode1_listener)
		self.midi_cc_ch_12_val_7.remove_value_listener(self.midi_cc_ch_12_val_7_mode1_listener)
		self.midi_cc_ch_12_val_82.remove_value_listener(self.midi_cc_ch_12_val_82_mode1_listener)
		self.midi_cc_ch_12_val_94.remove_value_listener(self.midi_cc_ch_12_val_94_mode1_listener)
		self.midi_cc_ch_13_val_83.remove_value_listener(self.midi_cc_ch_13_val_83_mode1_listener)
		self.midi_cc_ch_13_val_71.remove_value_listener(self.midi_cc_ch_13_val_71_mode1_listener)
		self.midi_cc_ch_13_val_70.remove_value_listener(self.midi_cc_ch_13_val_70_mode1_listener)
		self.midi_cc_ch_13_val_10.remove_value_listener(self.midi_cc_ch_13_val_10_mode1_listener)
		self.midi_cc_ch_13_val_7.remove_value_listener(self.midi_cc_ch_13_val_7_mode1_listener)
		self.midi_cc_ch_13_val_82.remove_value_listener(self.midi_cc_ch_13_val_82_mode1_listener)
		self.midi_cc_ch_13_val_94.remove_value_listener(self.midi_cc_ch_13_val_94_mode1_listener)
		self.midi_cc_ch_14_val_83.remove_value_listener(self.midi_cc_ch_14_val_83_mode1_listener)
		self.midi_cc_ch_14_val_71.remove_value_listener(self.midi_cc_ch_14_val_71_mode1_listener)
		self.midi_cc_ch_14_val_70.remove_value_listener(self.midi_cc_ch_14_val_70_mode1_listener)
		self.midi_cc_ch_14_val_10.remove_value_listener(self.midi_cc_ch_14_val_10_mode1_listener)
		self.midi_cc_ch_14_val_7.remove_value_listener(self.midi_cc_ch_14_val_7_mode1_listener)
		self.midi_cc_ch_14_val_82.remove_value_listener(self.midi_cc_ch_14_val_82_mode1_listener)
		self.midi_cc_ch_14_val_94.remove_value_listener(self.midi_cc_ch_14_val_94_mode1_listener)
		self.midi_cc_ch_15_val_83.remove_value_listener(self.midi_cc_ch_15_val_83_mode1_listener)
		self.midi_cc_ch_15_val_71.remove_value_listener(self.midi_cc_ch_15_val_71_mode1_listener)
		self.midi_cc_ch_15_val_70.remove_value_listener(self.midi_cc_ch_15_val_70_mode1_listener)
		self.midi_cc_ch_15_val_10.remove_value_listener(self.midi_cc_ch_15_val_10_mode1_listener)
		self.midi_cc_ch_15_val_7.remove_value_listener(self.midi_cc_ch_15_val_7_mode1_listener)
		self.midi_cc_ch_15_val_82.remove_value_listener(self.midi_cc_ch_15_val_82_mode1_listener)
		self.midi_cc_ch_15_val_94.remove_value_listener(self.midi_cc_ch_15_val_94_mode1_listener)
		self.midi_cc_ch_15_val_120.remove_value_listener(self.midi_cc_ch_15_val_120_mode1_listener)
		self.midi_cc_ch_15_val_121.remove_value_listener(self.midi_cc_ch_15_val_121_mode1_listener)
		self._remove_mode1_led_listeners()

	def _remove_mode169(self):
		self.midi_cc_ch_0_val_7.remove_value_listener(self.midi_cc_ch_0_val_7_mode169_listener)
		self.midi_cc_ch_0_val_82.remove_value_listener(self.midi_cc_ch_0_val_82_mode169_listener)
		self.midi_cc_ch_1_val_7.remove_value_listener(self.midi_cc_ch_1_val_7_mode169_listener)
		self.midi_cc_ch_1_val_82.remove_value_listener(self.midi_cc_ch_1_val_82_mode169_listener)
		self.midi_cc_ch_2_val_7.remove_value_listener(self.midi_cc_ch_2_val_7_mode169_listener)
		self.midi_cc_ch_2_val_82.remove_value_listener(self.midi_cc_ch_2_val_82_mode169_listener)
		self.midi_cc_ch_3_val_7.remove_value_listener(self.midi_cc_ch_3_val_7_mode169_listener)
		self.midi_cc_ch_3_val_82.remove_value_listener(self.midi_cc_ch_3_val_82_mode169_listener)
		self.midi_cc_ch_4_val_7.remove_value_listener(self.midi_cc_ch_4_val_7_mode169_listener)
		self.midi_cc_ch_4_val_82.remove_value_listener(self.midi_cc_ch_4_val_82_mode169_listener)
		self.midi_cc_ch_5_val_7.remove_value_listener(self.midi_cc_ch_5_val_7_mode169_listener)
		self.midi_cc_ch_5_val_82.remove_value_listener(self.midi_cc_ch_5_val_82_mode169_listener)
		self.midi_cc_ch_6_val_7.remove_value_listener(self.midi_cc_ch_6_val_7_mode169_listener)
		self.midi_cc_ch_6_val_82.remove_value_listener(self.midi_cc_ch_6_val_82_mode169_listener)
		self.midi_cc_ch_7_val_7.remove_value_listener(self.midi_cc_ch_7_val_7_mode169_listener)
		self.midi_cc_ch_7_val_82.remove_value_listener(self.midi_cc_ch_7_val_82_mode169_listener)
		self.midi_cc_ch_15_val_85.remove_value_listener(self.midi_cc_ch_15_val_85_mode169_listener)
		self.midi_cc_ch_15_val_86.remove_value_listener(self.midi_cc_ch_15_val_86_mode169_listener)
		self.midi_cc_ch_15_val_87.remove_value_listener(self.midi_cc_ch_15_val_87_mode169_listener)
		self.midi_cc_ch_15_val_88.remove_value_listener(self.midi_cc_ch_15_val_88_mode169_listener)
		self.midi_cc_ch_15_val_89.remove_value_listener(self.midi_cc_ch_15_val_89_mode169_listener)
		self.midi_cc_ch_15_val_90.remove_value_listener(self.midi_cc_ch_15_val_90_mode169_listener)
		self.midi_cc_ch_15_val_91.remove_value_listener(self.midi_cc_ch_15_val_91_mode169_listener)
		self.midi_cc_ch_15_val_92.remove_value_listener(self.midi_cc_ch_15_val_92_mode169_listener)
		self.midi_cc_ch_8_val_7.remove_value_listener(self.midi_cc_ch_8_val_7_mode169_listener)
		self.midi_cc_ch_8_val_82.remove_value_listener(self.midi_cc_ch_8_val_82_mode169_listener)
		self.midi_cc_ch_9_val_7.remove_value_listener(self.midi_cc_ch_9_val_7_mode169_listener)
		self.midi_cc_ch_9_val_82.remove_value_listener(self.midi_cc_ch_9_val_82_mode169_listener)
		self.midi_cc_ch_10_val_7.remove_value_listener(self.midi_cc_ch_10_val_7_mode169_listener)
		self.midi_cc_ch_10_val_82.remove_value_listener(self.midi_cc_ch_10_val_82_mode169_listener)
		self.midi_cc_ch_11_val_7.remove_value_listener(self.midi_cc_ch_11_val_7_mode169_listener)
		self.midi_cc_ch_11_val_82.remove_value_listener(self.midi_cc_ch_11_val_82_mode169_listener)
		self.midi_cc_ch_12_val_7.remove_value_listener(self.midi_cc_ch_12_val_7_mode169_listener)
		self.midi_cc_ch_12_val_82.remove_value_listener(self.midi_cc_ch_12_val_82_mode169_listener)
		self.midi_cc_ch_13_val_7.remove_value_listener(self.midi_cc_ch_13_val_7_mode169_listener)
		self.midi_cc_ch_13_val_82.remove_value_listener(self.midi_cc_ch_13_val_82_mode169_listener)
		self.midi_cc_ch_14_val_7.remove_value_listener(self.midi_cc_ch_14_val_7_mode169_listener)
		self.midi_cc_ch_14_val_82.remove_value_listener(self.midi_cc_ch_14_val_82_mode169_listener)
		self.midi_cc_ch_15_val_7.remove_value_listener(self.midi_cc_ch_15_val_7_mode169_listener)
		self.midi_cc_ch_15_val_82.remove_value_listener(self.midi_cc_ch_15_val_82_mode169_listener)
		self.midi_cc_ch_0_val_94.remove_value_listener(self.midi_cc_ch_0_val_94_mode169_listener)
		self.midi_cc_ch_1_val_94.remove_value_listener(self.midi_cc_ch_1_val_94_mode169_listener)
		self.midi_cc_ch_2_val_94.remove_value_listener(self.midi_cc_ch_2_val_94_mode169_listener)
		self.midi_cc_ch_3_val_94.remove_value_listener(self.midi_cc_ch_3_val_94_mode169_listener)
		self.midi_cc_ch_4_val_94.remove_value_listener(self.midi_cc_ch_4_val_94_mode169_listener)
		self.midi_cc_ch_5_val_94.remove_value_listener(self.midi_cc_ch_5_val_94_mode169_listener)
		self.midi_cc_ch_6_val_94.remove_value_listener(self.midi_cc_ch_6_val_94_mode169_listener)
		self.midi_cc_ch_7_val_94.remove_value_listener(self.midi_cc_ch_7_val_94_mode169_listener)
		self.midi_cc_ch_8_val_94.remove_value_listener(self.midi_cc_ch_8_val_94_mode169_listener)
		self.midi_cc_ch_9_val_94.remove_value_listener(self.midi_cc_ch_9_val_94_mode169_listener)
		self.midi_cc_ch_10_val_94.remove_value_listener(self.midi_cc_ch_10_val_94_mode169_listener)
		self.midi_cc_ch_11_val_94.remove_value_listener(self.midi_cc_ch_11_val_94_mode169_listener)
		self.midi_cc_ch_12_val_94.remove_value_listener(self.midi_cc_ch_12_val_94_mode169_listener)
		self.midi_cc_ch_13_val_94.remove_value_listener(self.midi_cc_ch_13_val_94_mode169_listener)
		self.midi_cc_ch_14_val_94.remove_value_listener(self.midi_cc_ch_14_val_94_mode169_listener)
		self.midi_cc_ch_15_val_94.remove_value_listener(self.midi_cc_ch_15_val_94_mode169_listener)
		self.midi_cc_ch_15_val_120.remove_value_listener(self.midi_cc_ch_15_val_120_mode169_listener)
		self._remove_mode169_led_listeners()

	def device_parameter_banks(self):
		self.device_id_86_banks = ["parameter_bank_1_id_87"]
		self.device_id_243_banks = ["parameter_bank_1_id_242"]
		self.device_id_86_bank_names = ["Parameter Bank 1"]
		self.device_id_86_active_bank = 0
		self.device_id_243_bank_names = ["Parameter Bank 1"]
		self.device_id_243_active_bank = 0
		self.device_id_86_bank_parameters_0 = [
			"parameter_1_id_88",
			"parameter_2_id_89",
			"parameter_3_id_90",
			"parameter_4_id_91",
			"parameter_5_id_92",
			"parameter_6_id_93",
			"parameter_7_id_94",
			"parameter_8_id_95"]
		self.device_id_243_bank_parameters_0 = [
			"parameter_1_id_234",
			"parameter_2_id_235",
			"parameter_3_id_236",
			"parameter_4_id_237",
			"parameter_5_id_238",
			"parameter_6_id_239",
			"parameter_7_id_240",
			"parameter_8_id_241"]

	def midi_cc_ch_0_val_7_mode1_listener(self, value):
		self.midi_cc_ch_0_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_7, "pre_val"):
			self.midi_cc_ch_0_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_7, "prev_press_time"):
			self.midi_cc_ch_0_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_1_id_3)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_7.pre_val = value
		self.midi_cc_ch_0_val_7.prev_press_time = time.time()

	def midi_cc_ch_0_val_82_mode1_listener(self, value):
		self.midi_cc_ch_0_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_82, "pre_val"):
			self.midi_cc_ch_0_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_82, "prev_press_time"):
			self.midi_cc_ch_0_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_1_id_4)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_82.pre_val = value
		self.midi_cc_ch_0_val_82.prev_press_time = time.time()

	def midi_cc_ch_0_val_94_mode1_listener(self, value):
		self.midi_cc_ch_0_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_94, "pre_val"):
			self.midi_cc_ch_0_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_94, "prev_press_time"):
			self.midi_cc_ch_0_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_1_id_5)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_94.pre_val = value
		self.midi_cc_ch_0_val_94.prev_press_time = time.time()

	def midi_cc_ch_0_val_83_mode1_listener(self, value):
		self.midi_cc_ch_0_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_83, "pre_val"):
			self.midi_cc_ch_0_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_83, "prev_press_time"):
			self.midi_cc_ch_0_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_8)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_83.pre_val = value
		self.midi_cc_ch_0_val_83.prev_press_time = time.time()

	def midi_cc_ch_0_val_71_mode1_listener(self, value):
		self.midi_cc_ch_0_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_71, "pre_val"):
			self.midi_cc_ch_0_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_71, "prev_press_time"):
			self.midi_cc_ch_0_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_9)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_71.pre_val = value
		self.midi_cc_ch_0_val_71.prev_press_time = time.time()

	def midi_cc_ch_0_val_70_mode1_listener(self, value):
		self.midi_cc_ch_0_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_70, "pre_val"):
			self.midi_cc_ch_0_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_70, "prev_press_time"):
			self.midi_cc_ch_0_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_10)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_70.pre_val = value
		self.midi_cc_ch_0_val_70.prev_press_time = time.time()

	def midi_cc_ch_0_val_10_mode1_listener(self, value):
		self.midi_cc_ch_0_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_10, "pre_val"):
			self.midi_cc_ch_0_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_10, "prev_press_time"):
			self.midi_cc_ch_0_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_11)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_10.pre_val = value
		self.midi_cc_ch_0_val_10.prev_press_time = time.time()

	def midi_cc_ch_1_val_83_mode1_listener(self, value):
		self.midi_cc_ch_1_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_83, "pre_val"):
			self.midi_cc_ch_1_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_83, "prev_press_time"):
			self.midi_cc_ch_1_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_13)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_83.pre_val = value
		self.midi_cc_ch_1_val_83.prev_press_time = time.time()

	def midi_cc_ch_1_val_71_mode1_listener(self, value):
		self.midi_cc_ch_1_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_71, "pre_val"):
			self.midi_cc_ch_1_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_71, "prev_press_time"):
			self.midi_cc_ch_1_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_14)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_71.pre_val = value
		self.midi_cc_ch_1_val_71.prev_press_time = time.time()

	def midi_cc_ch_1_val_70_mode1_listener(self, value):
		self.midi_cc_ch_1_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_70, "pre_val"):
			self.midi_cc_ch_1_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_70, "prev_press_time"):
			self.midi_cc_ch_1_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_15)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_70.pre_val = value
		self.midi_cc_ch_1_val_70.prev_press_time = time.time()

	def midi_cc_ch_1_val_10_mode1_listener(self, value):
		self.midi_cc_ch_1_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_10, "pre_val"):
			self.midi_cc_ch_1_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_10, "prev_press_time"):
			self.midi_cc_ch_1_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_16)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_10.pre_val = value
		self.midi_cc_ch_1_val_10.prev_press_time = time.time()

	def midi_cc_ch_1_val_7_mode1_listener(self, value):
		self.midi_cc_ch_1_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_7, "pre_val"):
			self.midi_cc_ch_1_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_7, "prev_press_time"):
			self.midi_cc_ch_1_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_2_id_17)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_7.pre_val = value
		self.midi_cc_ch_1_val_7.prev_press_time = time.time()

	def midi_cc_ch_1_val_82_mode1_listener(self, value):
		self.midi_cc_ch_1_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_82, "pre_val"):
			self.midi_cc_ch_1_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_82, "prev_press_time"):
			self.midi_cc_ch_1_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_2_id_18)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_82.pre_val = value
		self.midi_cc_ch_1_val_82.prev_press_time = time.time()

	def midi_cc_ch_1_val_94_mode1_listener(self, value):
		self.midi_cc_ch_1_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_94, "pre_val"):
			self.midi_cc_ch_1_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_94, "prev_press_time"):
			self.midi_cc_ch_1_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_2_id_19)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_94.pre_val = value
		self.midi_cc_ch_1_val_94.prev_press_time = time.time()

	def midi_cc_ch_2_val_83_mode1_listener(self, value):
		self.midi_cc_ch_2_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_83, "pre_val"):
			self.midi_cc_ch_2_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_83, "prev_press_time"):
			self.midi_cc_ch_2_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_23)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_83.pre_val = value
		self.midi_cc_ch_2_val_83.prev_press_time = time.time()

	def midi_cc_ch_2_val_71_mode1_listener(self, value):
		self.midi_cc_ch_2_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_71, "pre_val"):
			self.midi_cc_ch_2_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_71, "prev_press_time"):
			self.midi_cc_ch_2_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_24)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_71.pre_val = value
		self.midi_cc_ch_2_val_71.prev_press_time = time.time()

	def midi_cc_ch_2_val_70_mode1_listener(self, value):
		self.midi_cc_ch_2_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_70, "pre_val"):
			self.midi_cc_ch_2_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_70, "prev_press_time"):
			self.midi_cc_ch_2_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_25)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_70.pre_val = value
		self.midi_cc_ch_2_val_70.prev_press_time = time.time()

	def midi_cc_ch_2_val_10_mode1_listener(self, value):
		self.midi_cc_ch_2_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_10, "pre_val"):
			self.midi_cc_ch_2_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_10, "prev_press_time"):
			self.midi_cc_ch_2_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_26)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_10.pre_val = value
		self.midi_cc_ch_2_val_10.prev_press_time = time.time()

	def midi_cc_ch_2_val_7_mode1_listener(self, value):
		self.midi_cc_ch_2_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_7, "pre_val"):
			self.midi_cc_ch_2_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_7, "prev_press_time"):
			self.midi_cc_ch_2_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_3_id_27)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_7.pre_val = value
		self.midi_cc_ch_2_val_7.prev_press_time = time.time()

	def midi_cc_ch_2_val_82_mode1_listener(self, value):
		self.midi_cc_ch_2_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_82, "pre_val"):
			self.midi_cc_ch_2_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_82, "prev_press_time"):
			self.midi_cc_ch_2_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_3_id_28)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_82.pre_val = value
		self.midi_cc_ch_2_val_82.prev_press_time = time.time()

	def midi_cc_ch_2_val_94_mode1_listener(self, value):
		self.midi_cc_ch_2_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_94, "pre_val"):
			self.midi_cc_ch_2_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_94, "prev_press_time"):
			self.midi_cc_ch_2_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_3_id_29)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_94.pre_val = value
		self.midi_cc_ch_2_val_94.prev_press_time = time.time()

	def midi_cc_ch_3_val_83_mode1_listener(self, value):
		self.midi_cc_ch_3_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_83, "pre_val"):
			self.midi_cc_ch_3_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_83, "prev_press_time"):
			self.midi_cc_ch_3_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_33)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_83.pre_val = value
		self.midi_cc_ch_3_val_83.prev_press_time = time.time()

	def midi_cc_ch_3_val_71_mode1_listener(self, value):
		self.midi_cc_ch_3_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_71, "pre_val"):
			self.midi_cc_ch_3_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_71, "prev_press_time"):
			self.midi_cc_ch_3_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_34)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_71.pre_val = value
		self.midi_cc_ch_3_val_71.prev_press_time = time.time()

	def midi_cc_ch_3_val_70_mode1_listener(self, value):
		self.midi_cc_ch_3_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_70, "pre_val"):
			self.midi_cc_ch_3_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_70, "prev_press_time"):
			self.midi_cc_ch_3_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_35)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_70.pre_val = value
		self.midi_cc_ch_3_val_70.prev_press_time = time.time()

	def midi_cc_ch_3_val_10_mode1_listener(self, value):
		self.midi_cc_ch_3_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_10, "pre_val"):
			self.midi_cc_ch_3_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_10, "prev_press_time"):
			self.midi_cc_ch_3_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_36)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_10.pre_val = value
		self.midi_cc_ch_3_val_10.prev_press_time = time.time()

	def midi_cc_ch_3_val_7_mode1_listener(self, value):
		self.midi_cc_ch_3_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_7, "pre_val"):
			self.midi_cc_ch_3_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_7, "prev_press_time"):
			self.midi_cc_ch_3_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_4_id_37)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_7.pre_val = value
		self.midi_cc_ch_3_val_7.prev_press_time = time.time()

	def midi_cc_ch_3_val_82_mode1_listener(self, value):
		self.midi_cc_ch_3_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_82, "pre_val"):
			self.midi_cc_ch_3_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_82, "prev_press_time"):
			self.midi_cc_ch_3_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_4_id_38)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_82.pre_val = value
		self.midi_cc_ch_3_val_82.prev_press_time = time.time()

	def midi_cc_ch_3_val_94_mode1_listener(self, value):
		self.midi_cc_ch_3_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_94, "pre_val"):
			self.midi_cc_ch_3_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_94, "prev_press_time"):
			self.midi_cc_ch_3_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_4_id_39)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_94.pre_val = value
		self.midi_cc_ch_3_val_94.prev_press_time = time.time()

	def midi_cc_ch_4_val_83_mode1_listener(self, value):
		self.midi_cc_ch_4_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_83, "pre_val"):
			self.midi_cc_ch_4_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_83, "prev_press_time"):
			self.midi_cc_ch_4_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_43)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_83.pre_val = value
		self.midi_cc_ch_4_val_83.prev_press_time = time.time()

	def midi_cc_ch_4_val_71_mode1_listener(self, value):
		self.midi_cc_ch_4_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_71, "pre_val"):
			self.midi_cc_ch_4_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_71, "prev_press_time"):
			self.midi_cc_ch_4_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_44)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_71.pre_val = value
		self.midi_cc_ch_4_val_71.prev_press_time = time.time()

	def midi_cc_ch_4_val_70_mode1_listener(self, value):
		self.midi_cc_ch_4_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_70, "pre_val"):
			self.midi_cc_ch_4_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_70, "prev_press_time"):
			self.midi_cc_ch_4_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_45)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_70.pre_val = value
		self.midi_cc_ch_4_val_70.prev_press_time = time.time()

	def midi_cc_ch_4_val_10_mode1_listener(self, value):
		self.midi_cc_ch_4_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_10, "pre_val"):
			self.midi_cc_ch_4_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_10, "prev_press_time"):
			self.midi_cc_ch_4_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_46)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_10.pre_val = value
		self.midi_cc_ch_4_val_10.prev_press_time = time.time()

	def midi_cc_ch_4_val_7_mode1_listener(self, value):
		self.midi_cc_ch_4_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_7, "pre_val"):
			self.midi_cc_ch_4_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_7, "prev_press_time"):
			self.midi_cc_ch_4_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_5_id_47)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_7.pre_val = value
		self.midi_cc_ch_4_val_7.prev_press_time = time.time()

	def midi_cc_ch_4_val_82_mode1_listener(self, value):
		self.midi_cc_ch_4_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_82, "pre_val"):
			self.midi_cc_ch_4_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_82, "prev_press_time"):
			self.midi_cc_ch_4_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_5_id_48)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_82.pre_val = value
		self.midi_cc_ch_4_val_82.prev_press_time = time.time()

	def midi_cc_ch_4_val_94_mode1_listener(self, value):
		self.midi_cc_ch_4_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_94, "pre_val"):
			self.midi_cc_ch_4_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_94, "prev_press_time"):
			self.midi_cc_ch_4_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_5_id_49)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_94.pre_val = value
		self.midi_cc_ch_4_val_94.prev_press_time = time.time()

	def midi_cc_ch_5_val_83_mode1_listener(self, value):
		self.midi_cc_ch_5_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_83, "pre_val"):
			self.midi_cc_ch_5_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_83, "prev_press_time"):
			self.midi_cc_ch_5_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_53)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_83.pre_val = value
		self.midi_cc_ch_5_val_83.prev_press_time = time.time()

	def midi_cc_ch_5_val_71_mode1_listener(self, value):
		self.midi_cc_ch_5_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_71, "pre_val"):
			self.midi_cc_ch_5_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_71, "prev_press_time"):
			self.midi_cc_ch_5_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_54)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_71.pre_val = value
		self.midi_cc_ch_5_val_71.prev_press_time = time.time()

	def midi_cc_ch_5_val_70_mode1_listener(self, value):
		self.midi_cc_ch_5_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_70, "pre_val"):
			self.midi_cc_ch_5_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_70, "prev_press_time"):
			self.midi_cc_ch_5_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_55)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_70.pre_val = value
		self.midi_cc_ch_5_val_70.prev_press_time = time.time()

	def midi_cc_ch_5_val_10_mode1_listener(self, value):
		self.midi_cc_ch_5_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_10, "pre_val"):
			self.midi_cc_ch_5_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_10, "prev_press_time"):
			self.midi_cc_ch_5_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_56)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_10.pre_val = value
		self.midi_cc_ch_5_val_10.prev_press_time = time.time()

	def midi_cc_ch_5_val_7_mode1_listener(self, value):
		self.midi_cc_ch_5_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_7, "pre_val"):
			self.midi_cc_ch_5_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_7, "prev_press_time"):
			self.midi_cc_ch_5_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_6_id_57)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_7.pre_val = value
		self.midi_cc_ch_5_val_7.prev_press_time = time.time()

	def midi_cc_ch_5_val_82_mode1_listener(self, value):
		self.midi_cc_ch_5_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_82, "pre_val"):
			self.midi_cc_ch_5_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_82, "prev_press_time"):
			self.midi_cc_ch_5_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_6_id_58)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_82.pre_val = value
		self.midi_cc_ch_5_val_82.prev_press_time = time.time()

	def midi_cc_ch_5_val_94_mode1_listener(self, value):
		self.midi_cc_ch_5_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_94, "pre_val"):
			self.midi_cc_ch_5_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_94, "prev_press_time"):
			self.midi_cc_ch_5_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_6_id_59)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_94.pre_val = value
		self.midi_cc_ch_5_val_94.prev_press_time = time.time()

	def midi_cc_ch_6_val_83_mode1_listener(self, value):
		self.midi_cc_ch_6_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_83, "pre_val"):
			self.midi_cc_ch_6_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_83, "prev_press_time"):
			self.midi_cc_ch_6_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_63)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_83.pre_val = value
		self.midi_cc_ch_6_val_83.prev_press_time = time.time()

	def midi_cc_ch_6_val_71_mode1_listener(self, value):
		self.midi_cc_ch_6_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_71, "pre_val"):
			self.midi_cc_ch_6_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_71, "prev_press_time"):
			self.midi_cc_ch_6_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_64)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_71.pre_val = value
		self.midi_cc_ch_6_val_71.prev_press_time = time.time()

	def midi_cc_ch_6_val_70_mode1_listener(self, value):
		self.midi_cc_ch_6_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_70, "pre_val"):
			self.midi_cc_ch_6_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_70, "prev_press_time"):
			self.midi_cc_ch_6_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_65)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_70.pre_val = value
		self.midi_cc_ch_6_val_70.prev_press_time = time.time()

	def midi_cc_ch_6_val_10_mode1_listener(self, value):
		self.midi_cc_ch_6_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_10, "pre_val"):
			self.midi_cc_ch_6_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_10, "prev_press_time"):
			self.midi_cc_ch_6_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_66)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_10.pre_val = value
		self.midi_cc_ch_6_val_10.prev_press_time = time.time()

	def midi_cc_ch_6_val_7_mode1_listener(self, value):
		self.midi_cc_ch_6_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_7, "pre_val"):
			self.midi_cc_ch_6_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_7, "prev_press_time"):
			self.midi_cc_ch_6_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_7_id_67)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_7.pre_val = value
		self.midi_cc_ch_6_val_7.prev_press_time = time.time()

	def midi_cc_ch_6_val_82_mode1_listener(self, value):
		self.midi_cc_ch_6_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_82, "pre_val"):
			self.midi_cc_ch_6_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_82, "prev_press_time"):
			self.midi_cc_ch_6_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_7_id_68)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_82.pre_val = value
		self.midi_cc_ch_6_val_82.prev_press_time = time.time()

	def midi_cc_ch_6_val_94_mode1_listener(self, value):
		self.midi_cc_ch_6_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_94, "pre_val"):
			self.midi_cc_ch_6_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_94, "prev_press_time"):
			self.midi_cc_ch_6_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_7_id_69)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_94.pre_val = value
		self.midi_cc_ch_6_val_94.prev_press_time = time.time()

	def midi_cc_ch_7_val_83_mode1_listener(self, value):
		self.midi_cc_ch_7_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_83, "pre_val"):
			self.midi_cc_ch_7_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_83, "prev_press_time"):
			self.midi_cc_ch_7_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_73)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_83.pre_val = value
		self.midi_cc_ch_7_val_83.prev_press_time = time.time()

	def midi_cc_ch_7_val_71_mode1_listener(self, value):
		self.midi_cc_ch_7_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_71, "pre_val"):
			self.midi_cc_ch_7_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_71, "prev_press_time"):
			self.midi_cc_ch_7_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_74)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_71.pre_val = value
		self.midi_cc_ch_7_val_71.prev_press_time = time.time()

	def midi_cc_ch_7_val_70_mode1_listener(self, value):
		self.midi_cc_ch_7_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_70, "pre_val"):
			self.midi_cc_ch_7_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_70, "prev_press_time"):
			self.midi_cc_ch_7_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_75)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_70.pre_val = value
		self.midi_cc_ch_7_val_70.prev_press_time = time.time()

	def midi_cc_ch_7_val_10_mode1_listener(self, value):
		self.midi_cc_ch_7_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_10, "pre_val"):
			self.midi_cc_ch_7_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_10, "prev_press_time"):
			self.midi_cc_ch_7_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_76)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_10.pre_val = value
		self.midi_cc_ch_7_val_10.prev_press_time = time.time()

	def midi_cc_ch_7_val_7_mode1_listener(self, value):
		self.midi_cc_ch_7_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_7, "pre_val"):
			self.midi_cc_ch_7_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_7, "prev_press_time"):
			self.midi_cc_ch_7_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_8_id_77)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_7.pre_val = value
		self.midi_cc_ch_7_val_7.prev_press_time = time.time()

	def midi_cc_ch_7_val_82_mode1_listener(self, value):
		self.midi_cc_ch_7_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_82, "pre_val"):
			self.midi_cc_ch_7_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_82, "prev_press_time"):
			self.midi_cc_ch_7_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_8_id_78)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_82.pre_val = value
		self.midi_cc_ch_7_val_82.prev_press_time = time.time()

	def midi_cc_ch_7_val_94_mode1_listener(self, value):
		self.midi_cc_ch_7_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_94, "pre_val"):
			self.midi_cc_ch_7_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_94, "prev_press_time"):
			self.midi_cc_ch_7_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_8_id_79)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_94.pre_val = value
		self.midi_cc_ch_7_val_94.prev_press_time = time.time()

	def midi_cc_ch_15_val_85_mode1_listener(self, value):
		self.midi_cc_ch_15_val_85.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_85, "pre_val"):
			self.midi_cc_ch_15_val_85.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_85, "prev_press_time"):
			self.midi_cc_ch_15_val_85.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_1_id_88)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_85.pre_val = value
		self.midi_cc_ch_15_val_85.prev_press_time = time.time()

	def midi_cc_ch_15_val_86_mode1_listener(self, value):
		self.midi_cc_ch_15_val_86.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_86, "pre_val"):
			self.midi_cc_ch_15_val_86.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_86, "prev_press_time"):
			self.midi_cc_ch_15_val_86.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_2_id_89)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_86.pre_val = value
		self.midi_cc_ch_15_val_86.prev_press_time = time.time()

	def midi_cc_ch_15_val_87_mode1_listener(self, value):
		self.midi_cc_ch_15_val_87.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_87, "pre_val"):
			self.midi_cc_ch_15_val_87.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_87, "prev_press_time"):
			self.midi_cc_ch_15_val_87.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_3_id_90)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_87.pre_val = value
		self.midi_cc_ch_15_val_87.prev_press_time = time.time()

	def midi_cc_ch_15_val_88_mode1_listener(self, value):
		self.midi_cc_ch_15_val_88.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_88, "pre_val"):
			self.midi_cc_ch_15_val_88.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_88, "prev_press_time"):
			self.midi_cc_ch_15_val_88.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_4_id_91)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_88.pre_val = value
		self.midi_cc_ch_15_val_88.prev_press_time = time.time()

	def midi_cc_ch_15_val_89_mode1_listener(self, value):
		self.midi_cc_ch_15_val_89.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_89, "pre_val"):
			self.midi_cc_ch_15_val_89.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_89, "prev_press_time"):
			self.midi_cc_ch_15_val_89.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_5_id_92)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_89.pre_val = value
		self.midi_cc_ch_15_val_89.prev_press_time = time.time()

	def midi_cc_ch_15_val_90_mode1_listener(self, value):
		self.midi_cc_ch_15_val_90.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_90, "pre_val"):
			self.midi_cc_ch_15_val_90.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_90, "prev_press_time"):
			self.midi_cc_ch_15_val_90.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_6_id_93)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_90.pre_val = value
		self.midi_cc_ch_15_val_90.prev_press_time = time.time()

	def midi_cc_ch_15_val_91_mode1_listener(self, value):
		self.midi_cc_ch_15_val_91.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_91, "pre_val"):
			self.midi_cc_ch_15_val_91.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_91, "prev_press_time"):
			self.midi_cc_ch_15_val_91.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_7_id_94)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_91.pre_val = value
		self.midi_cc_ch_15_val_91.prev_press_time = time.time()

	def midi_cc_ch_15_val_92_mode1_listener(self, value):
		self.midi_cc_ch_15_val_92.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_92, "pre_val"):
			self.midi_cc_ch_15_val_92.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_92, "prev_press_time"):
			self.midi_cc_ch_15_val_92.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_86_active_bank == 0):
			self.pick_brain(self.parameter_8_id_95)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_92.pre_val = value
		self.midi_cc_ch_15_val_92.prev_press_time = time.time()

	def midi_cc_ch_8_val_83_mode1_listener(self, value):
		self.midi_cc_ch_8_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_83, "pre_val"):
			self.midi_cc_ch_8_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_83, "prev_press_time"):
			self.midi_cc_ch_8_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_97)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_83.pre_val = value
		self.midi_cc_ch_8_val_83.prev_press_time = time.time()

	def midi_cc_ch_8_val_71_mode1_listener(self, value):
		self.midi_cc_ch_8_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_71, "pre_val"):
			self.midi_cc_ch_8_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_71, "prev_press_time"):
			self.midi_cc_ch_8_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_98)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_71.pre_val = value
		self.midi_cc_ch_8_val_71.prev_press_time = time.time()

	def midi_cc_ch_8_val_70_mode1_listener(self, value):
		self.midi_cc_ch_8_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_70, "pre_val"):
			self.midi_cc_ch_8_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_70, "prev_press_time"):
			self.midi_cc_ch_8_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_99)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_70.pre_val = value
		self.midi_cc_ch_8_val_70.prev_press_time = time.time()

	def midi_cc_ch_8_val_10_mode1_listener(self, value):
		self.midi_cc_ch_8_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_10, "pre_val"):
			self.midi_cc_ch_8_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_10, "prev_press_time"):
			self.midi_cc_ch_8_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_100)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_10.pre_val = value
		self.midi_cc_ch_8_val_10.prev_press_time = time.time()

	def midi_cc_ch_8_val_7_mode1_listener(self, value):
		self.midi_cc_ch_8_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_7, "pre_val"):
			self.midi_cc_ch_8_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_7, "prev_press_time"):
			self.midi_cc_ch_8_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_9_id_101)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_7.pre_val = value
		self.midi_cc_ch_8_val_7.prev_press_time = time.time()

	def midi_cc_ch_8_val_82_mode1_listener(self, value):
		self.midi_cc_ch_8_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_82, "pre_val"):
			self.midi_cc_ch_8_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_82, "prev_press_time"):
			self.midi_cc_ch_8_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_9_id_102)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_82.pre_val = value
		self.midi_cc_ch_8_val_82.prev_press_time = time.time()

	def midi_cc_ch_8_val_94_mode1_listener(self, value):
		self.midi_cc_ch_8_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_94, "pre_val"):
			self.midi_cc_ch_8_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_94, "prev_press_time"):
			self.midi_cc_ch_8_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_9_id_103)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_94.pre_val = value
		self.midi_cc_ch_8_val_94.prev_press_time = time.time()

	def midi_cc_ch_9_val_83_mode1_listener(self, value):
		self.midi_cc_ch_9_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_83, "pre_val"):
			self.midi_cc_ch_9_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_83, "prev_press_time"):
			self.midi_cc_ch_9_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_106)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_83.pre_val = value
		self.midi_cc_ch_9_val_83.prev_press_time = time.time()

	def midi_cc_ch_9_val_71_mode1_listener(self, value):
		self.midi_cc_ch_9_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_71, "pre_val"):
			self.midi_cc_ch_9_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_71, "prev_press_time"):
			self.midi_cc_ch_9_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_107)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_71.pre_val = value
		self.midi_cc_ch_9_val_71.prev_press_time = time.time()

	def midi_cc_ch_9_val_70_mode1_listener(self, value):
		self.midi_cc_ch_9_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_70, "pre_val"):
			self.midi_cc_ch_9_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_70, "prev_press_time"):
			self.midi_cc_ch_9_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_108)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_70.pre_val = value
		self.midi_cc_ch_9_val_70.prev_press_time = time.time()

	def midi_cc_ch_9_val_10_mode1_listener(self, value):
		self.midi_cc_ch_9_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_10, "pre_val"):
			self.midi_cc_ch_9_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_10, "prev_press_time"):
			self.midi_cc_ch_9_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_109)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_10.pre_val = value
		self.midi_cc_ch_9_val_10.prev_press_time = time.time()

	def midi_cc_ch_9_val_7_mode1_listener(self, value):
		self.midi_cc_ch_9_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_7, "pre_val"):
			self.midi_cc_ch_9_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_7, "prev_press_time"):
			self.midi_cc_ch_9_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_10_id_110)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_7.pre_val = value
		self.midi_cc_ch_9_val_7.prev_press_time = time.time()

	def midi_cc_ch_9_val_82_mode1_listener(self, value):
		self.midi_cc_ch_9_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_82, "pre_val"):
			self.midi_cc_ch_9_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_82, "prev_press_time"):
			self.midi_cc_ch_9_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_10_id_111)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_82.pre_val = value
		self.midi_cc_ch_9_val_82.prev_press_time = time.time()

	def midi_cc_ch_9_val_94_mode1_listener(self, value):
		self.midi_cc_ch_9_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_94, "pre_val"):
			self.midi_cc_ch_9_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_94, "prev_press_time"):
			self.midi_cc_ch_9_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_10_id_112)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_94.pre_val = value
		self.midi_cc_ch_9_val_94.prev_press_time = time.time()

	def midi_cc_ch_10_val_83_mode1_listener(self, value):
		self.midi_cc_ch_10_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_83, "pre_val"):
			self.midi_cc_ch_10_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_83, "prev_press_time"):
			self.midi_cc_ch_10_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_115)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_83.pre_val = value
		self.midi_cc_ch_10_val_83.prev_press_time = time.time()

	def midi_cc_ch_10_val_71_mode1_listener(self, value):
		self.midi_cc_ch_10_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_71, "pre_val"):
			self.midi_cc_ch_10_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_71, "prev_press_time"):
			self.midi_cc_ch_10_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_116)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_71.pre_val = value
		self.midi_cc_ch_10_val_71.prev_press_time = time.time()

	def midi_cc_ch_10_val_70_mode1_listener(self, value):
		self.midi_cc_ch_10_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_70, "pre_val"):
			self.midi_cc_ch_10_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_70, "prev_press_time"):
			self.midi_cc_ch_10_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_117)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_70.pre_val = value
		self.midi_cc_ch_10_val_70.prev_press_time = time.time()

	def midi_cc_ch_10_val_10_mode1_listener(self, value):
		self.midi_cc_ch_10_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_10, "pre_val"):
			self.midi_cc_ch_10_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_10, "prev_press_time"):
			self.midi_cc_ch_10_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_118)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_10.pre_val = value
		self.midi_cc_ch_10_val_10.prev_press_time = time.time()

	def midi_cc_ch_10_val_7_mode1_listener(self, value):
		self.midi_cc_ch_10_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_7, "pre_val"):
			self.midi_cc_ch_10_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_7, "prev_press_time"):
			self.midi_cc_ch_10_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_11_id_119)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_7.pre_val = value
		self.midi_cc_ch_10_val_7.prev_press_time = time.time()

	def midi_cc_ch_10_val_82_mode1_listener(self, value):
		self.midi_cc_ch_10_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_82, "pre_val"):
			self.midi_cc_ch_10_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_82, "prev_press_time"):
			self.midi_cc_ch_10_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_11_id_120)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_82.pre_val = value
		self.midi_cc_ch_10_val_82.prev_press_time = time.time()

	def midi_cc_ch_10_val_94_mode1_listener(self, value):
		self.midi_cc_ch_10_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_94, "pre_val"):
			self.midi_cc_ch_10_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_94, "prev_press_time"):
			self.midi_cc_ch_10_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_11_id_121)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_94.pre_val = value
		self.midi_cc_ch_10_val_94.prev_press_time = time.time()

	def midi_cc_ch_11_val_83_mode1_listener(self, value):
		self.midi_cc_ch_11_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_83, "pre_val"):
			self.midi_cc_ch_11_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_83, "prev_press_time"):
			self.midi_cc_ch_11_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_124)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_83.pre_val = value
		self.midi_cc_ch_11_val_83.prev_press_time = time.time()

	def midi_cc_ch_11_val_71_mode1_listener(self, value):
		self.midi_cc_ch_11_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_71, "pre_val"):
			self.midi_cc_ch_11_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_71, "prev_press_time"):
			self.midi_cc_ch_11_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_125)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_71.pre_val = value
		self.midi_cc_ch_11_val_71.prev_press_time = time.time()

	def midi_cc_ch_11_val_70_mode1_listener(self, value):
		self.midi_cc_ch_11_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_70, "pre_val"):
			self.midi_cc_ch_11_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_70, "prev_press_time"):
			self.midi_cc_ch_11_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_126)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_70.pre_val = value
		self.midi_cc_ch_11_val_70.prev_press_time = time.time()

	def midi_cc_ch_11_val_10_mode1_listener(self, value):
		self.midi_cc_ch_11_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_10, "pre_val"):
			self.midi_cc_ch_11_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_10, "prev_press_time"):
			self.midi_cc_ch_11_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_127)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_10.pre_val = value
		self.midi_cc_ch_11_val_10.prev_press_time = time.time()

	def midi_cc_ch_11_val_7_mode1_listener(self, value):
		self.midi_cc_ch_11_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_7, "pre_val"):
			self.midi_cc_ch_11_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_7, "prev_press_time"):
			self.midi_cc_ch_11_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_12_id_128)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_7.pre_val = value
		self.midi_cc_ch_11_val_7.prev_press_time = time.time()

	def midi_cc_ch_11_val_82_mode1_listener(self, value):
		self.midi_cc_ch_11_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_82, "pre_val"):
			self.midi_cc_ch_11_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_82, "prev_press_time"):
			self.midi_cc_ch_11_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_12_id_129)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_82.pre_val = value
		self.midi_cc_ch_11_val_82.prev_press_time = time.time()

	def midi_cc_ch_11_val_94_mode1_listener(self, value):
		self.midi_cc_ch_11_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_94, "pre_val"):
			self.midi_cc_ch_11_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_94, "prev_press_time"):
			self.midi_cc_ch_11_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_12_id_130)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_94.pre_val = value
		self.midi_cc_ch_11_val_94.prev_press_time = time.time()

	def midi_cc_ch_12_val_83_mode1_listener(self, value):
		self.midi_cc_ch_12_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_83, "pre_val"):
			self.midi_cc_ch_12_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_83, "prev_press_time"):
			self.midi_cc_ch_12_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_133)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_83.pre_val = value
		self.midi_cc_ch_12_val_83.prev_press_time = time.time()

	def midi_cc_ch_12_val_71_mode1_listener(self, value):
		self.midi_cc_ch_12_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_71, "pre_val"):
			self.midi_cc_ch_12_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_71, "prev_press_time"):
			self.midi_cc_ch_12_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_134)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_71.pre_val = value
		self.midi_cc_ch_12_val_71.prev_press_time = time.time()

	def midi_cc_ch_12_val_70_mode1_listener(self, value):
		self.midi_cc_ch_12_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_70, "pre_val"):
			self.midi_cc_ch_12_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_70, "prev_press_time"):
			self.midi_cc_ch_12_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_135)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_70.pre_val = value
		self.midi_cc_ch_12_val_70.prev_press_time = time.time()

	def midi_cc_ch_12_val_10_mode1_listener(self, value):
		self.midi_cc_ch_12_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_10, "pre_val"):
			self.midi_cc_ch_12_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_10, "prev_press_time"):
			self.midi_cc_ch_12_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_136)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_10.pre_val = value
		self.midi_cc_ch_12_val_10.prev_press_time = time.time()

	def midi_cc_ch_12_val_7_mode1_listener(self, value):
		self.midi_cc_ch_12_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_7, "pre_val"):
			self.midi_cc_ch_12_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_7, "prev_press_time"):
			self.midi_cc_ch_12_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_13_id_137)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_7.pre_val = value
		self.midi_cc_ch_12_val_7.prev_press_time = time.time()

	def midi_cc_ch_12_val_82_mode1_listener(self, value):
		self.midi_cc_ch_12_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_82, "pre_val"):
			self.midi_cc_ch_12_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_82, "prev_press_time"):
			self.midi_cc_ch_12_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_13_id_138)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_82.pre_val = value
		self.midi_cc_ch_12_val_82.prev_press_time = time.time()

	def midi_cc_ch_12_val_94_mode1_listener(self, value):
		self.midi_cc_ch_12_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_94, "pre_val"):
			self.midi_cc_ch_12_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_94, "prev_press_time"):
			self.midi_cc_ch_12_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_13_id_139)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_94.pre_val = value
		self.midi_cc_ch_12_val_94.prev_press_time = time.time()

	def midi_cc_ch_13_val_83_mode1_listener(self, value):
		self.midi_cc_ch_13_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_83, "pre_val"):
			self.midi_cc_ch_13_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_83, "prev_press_time"):
			self.midi_cc_ch_13_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_142)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_83.pre_val = value
		self.midi_cc_ch_13_val_83.prev_press_time = time.time()

	def midi_cc_ch_13_val_71_mode1_listener(self, value):
		self.midi_cc_ch_13_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_71, "pre_val"):
			self.midi_cc_ch_13_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_71, "prev_press_time"):
			self.midi_cc_ch_13_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_143)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_71.pre_val = value
		self.midi_cc_ch_13_val_71.prev_press_time = time.time()

	def midi_cc_ch_13_val_70_mode1_listener(self, value):
		self.midi_cc_ch_13_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_70, "pre_val"):
			self.midi_cc_ch_13_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_70, "prev_press_time"):
			self.midi_cc_ch_13_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_144)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_70.pre_val = value
		self.midi_cc_ch_13_val_70.prev_press_time = time.time()

	def midi_cc_ch_13_val_10_mode1_listener(self, value):
		self.midi_cc_ch_13_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_10, "pre_val"):
			self.midi_cc_ch_13_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_10, "prev_press_time"):
			self.midi_cc_ch_13_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_145)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_10.pre_val = value
		self.midi_cc_ch_13_val_10.prev_press_time = time.time()

	def midi_cc_ch_13_val_7_mode1_listener(self, value):
		self.midi_cc_ch_13_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_7, "pre_val"):
			self.midi_cc_ch_13_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_7, "prev_press_time"):
			self.midi_cc_ch_13_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_14_id_146)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_7.pre_val = value
		self.midi_cc_ch_13_val_7.prev_press_time = time.time()

	def midi_cc_ch_13_val_82_mode1_listener(self, value):
		self.midi_cc_ch_13_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_82, "pre_val"):
			self.midi_cc_ch_13_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_82, "prev_press_time"):
			self.midi_cc_ch_13_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_14_id_147)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_82.pre_val = value
		self.midi_cc_ch_13_val_82.prev_press_time = time.time()

	def midi_cc_ch_13_val_94_mode1_listener(self, value):
		self.midi_cc_ch_13_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_94, "pre_val"):
			self.midi_cc_ch_13_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_94, "prev_press_time"):
			self.midi_cc_ch_13_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_14_id_148)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_94.pre_val = value
		self.midi_cc_ch_13_val_94.prev_press_time = time.time()

	def midi_cc_ch_14_val_83_mode1_listener(self, value):
		self.midi_cc_ch_14_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_83, "pre_val"):
			self.midi_cc_ch_14_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_83, "prev_press_time"):
			self.midi_cc_ch_14_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_151)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_83.pre_val = value
		self.midi_cc_ch_14_val_83.prev_press_time = time.time()

	def midi_cc_ch_14_val_71_mode1_listener(self, value):
		self.midi_cc_ch_14_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_71, "pre_val"):
			self.midi_cc_ch_14_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_71, "prev_press_time"):
			self.midi_cc_ch_14_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_152)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_71.pre_val = value
		self.midi_cc_ch_14_val_71.prev_press_time = time.time()

	def midi_cc_ch_14_val_70_mode1_listener(self, value):
		self.midi_cc_ch_14_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_70, "pre_val"):
			self.midi_cc_ch_14_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_70, "prev_press_time"):
			self.midi_cc_ch_14_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_153)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_70.pre_val = value
		self.midi_cc_ch_14_val_70.prev_press_time = time.time()

	def midi_cc_ch_14_val_10_mode1_listener(self, value):
		self.midi_cc_ch_14_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_10, "pre_val"):
			self.midi_cc_ch_14_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_10, "prev_press_time"):
			self.midi_cc_ch_14_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_154)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_10.pre_val = value
		self.midi_cc_ch_14_val_10.prev_press_time = time.time()

	def midi_cc_ch_14_val_7_mode1_listener(self, value):
		self.midi_cc_ch_14_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_7, "pre_val"):
			self.midi_cc_ch_14_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_7, "prev_press_time"):
			self.midi_cc_ch_14_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_15_id_155)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_7.pre_val = value
		self.midi_cc_ch_14_val_7.prev_press_time = time.time()

	def midi_cc_ch_14_val_82_mode1_listener(self, value):
		self.midi_cc_ch_14_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_82, "pre_val"):
			self.midi_cc_ch_14_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_82, "prev_press_time"):
			self.midi_cc_ch_14_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_15_id_156)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_82.pre_val = value
		self.midi_cc_ch_14_val_82.prev_press_time = time.time()

	def midi_cc_ch_14_val_94_mode1_listener(self, value):
		self.midi_cc_ch_14_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_94, "pre_val"):
			self.midi_cc_ch_14_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_94, "prev_press_time"):
			self.midi_cc_ch_14_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_15_id_157)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_94.pre_val = value
		self.midi_cc_ch_14_val_94.prev_press_time = time.time()

	def midi_cc_ch_15_val_83_mode1_listener(self, value):
		self.midi_cc_ch_15_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_83, "pre_val"):
			self.midi_cc_ch_15_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_83, "prev_press_time"):
			self.midi_cc_ch_15_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_1_id_160)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_83.pre_val = value
		self.midi_cc_ch_15_val_83.prev_press_time = time.time()

	def midi_cc_ch_15_val_71_mode1_listener(self, value):
		self.midi_cc_ch_15_val_71.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_71, "pre_val"):
			self.midi_cc_ch_15_val_71.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_71, "prev_press_time"):
			self.midi_cc_ch_15_val_71.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_2_id_161)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_71.pre_val = value
		self.midi_cc_ch_15_val_71.prev_press_time = time.time()

	def midi_cc_ch_15_val_70_mode1_listener(self, value):
		self.midi_cc_ch_15_val_70.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_70, "pre_val"):
			self.midi_cc_ch_15_val_70.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_70, "prev_press_time"):
			self.midi_cc_ch_15_val_70.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_3_id_162)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_70.pre_val = value
		self.midi_cc_ch_15_val_70.prev_press_time = time.time()

	def midi_cc_ch_15_val_10_mode1_listener(self, value):
		self.midi_cc_ch_15_val_10.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_10, "pre_val"):
			self.midi_cc_ch_15_val_10.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_10, "prev_press_time"):
			self.midi_cc_ch_15_val_10.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.send_4_id_163)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_10.pre_val = value
		self.midi_cc_ch_15_val_10.prev_press_time = time.time()

	def midi_cc_ch_15_val_7_mode1_listener(self, value):
		self.midi_cc_ch_15_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_7, "pre_val"):
			self.midi_cc_ch_15_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_7, "prev_press_time"):
			self.midi_cc_ch_15_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_16_id_164)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_7.pre_val = value
		self.midi_cc_ch_15_val_7.prev_press_time = time.time()

	def midi_cc_ch_15_val_82_mode1_listener(self, value):
		self.midi_cc_ch_15_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_82, "pre_val"):
			self.midi_cc_ch_15_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_82, "prev_press_time"):
			self.midi_cc_ch_15_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_16_id_165)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_82.pre_val = value
		self.midi_cc_ch_15_val_82.prev_press_time = time.time()

	def midi_cc_ch_15_val_94_mode1_listener(self, value):
		self.midi_cc_ch_15_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_94, "pre_val"):
			self.midi_cc_ch_15_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_94, "prev_press_time"):
			self.midi_cc_ch_15_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mute_16_id_166)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_94.pre_val = value
		self.midi_cc_ch_15_val_94.prev_press_time = time.time()

	def midi_cc_ch_15_val_120_mode1_listener(self, value):
		self.midi_cc_ch_15_val_120.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_120, "pre_val"):
			self.midi_cc_ch_15_val_120.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_120, "prev_press_time"):
			self.midi_cc_ch_15_val_120.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mode_selector_1_id_168)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_120.pre_val = value
		self.midi_cc_ch_15_val_120.prev_press_time = time.time()

	def midi_cc_ch_0_val_7_mode169_listener(self, value):
		self.midi_cc_ch_0_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_7, "pre_val"):
			self.midi_cc_ch_0_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_7, "prev_press_time"):
			self.midi_cc_ch_0_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_1_id_174)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_7.pre_val = value
		self.midi_cc_ch_0_val_7.prev_press_time = time.time()

	def midi_cc_ch_0_val_82_mode169_listener(self, value):
		self.midi_cc_ch_0_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_82, "pre_val"):
			self.midi_cc_ch_0_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_82, "prev_press_time"):
			self.midi_cc_ch_0_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_1_id_175)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_82.pre_val = value
		self.midi_cc_ch_0_val_82.prev_press_time = time.time()

	def midi_cc_ch_1_val_7_mode169_listener(self, value):
		self.midi_cc_ch_1_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_7, "pre_val"):
			self.midi_cc_ch_1_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_7, "prev_press_time"):
			self.midi_cc_ch_1_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_2_id_182)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_7.pre_val = value
		self.midi_cc_ch_1_val_7.prev_press_time = time.time()

	def midi_cc_ch_1_val_82_mode169_listener(self, value):
		self.midi_cc_ch_1_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_82, "pre_val"):
			self.midi_cc_ch_1_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_82, "prev_press_time"):
			self.midi_cc_ch_1_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_2_id_183)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_82.pre_val = value
		self.midi_cc_ch_1_val_82.prev_press_time = time.time()

	def midi_cc_ch_2_val_7_mode169_listener(self, value):
		self.midi_cc_ch_2_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_7, "pre_val"):
			self.midi_cc_ch_2_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_7, "prev_press_time"):
			self.midi_cc_ch_2_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_3_id_190)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_7.pre_val = value
		self.midi_cc_ch_2_val_7.prev_press_time = time.time()

	def midi_cc_ch_2_val_82_mode169_listener(self, value):
		self.midi_cc_ch_2_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_82, "pre_val"):
			self.midi_cc_ch_2_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_82, "prev_press_time"):
			self.midi_cc_ch_2_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_3_id_191)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_82.pre_val = value
		self.midi_cc_ch_2_val_82.prev_press_time = time.time()

	def midi_cc_ch_3_val_7_mode169_listener(self, value):
		self.midi_cc_ch_3_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_7, "pre_val"):
			self.midi_cc_ch_3_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_7, "prev_press_time"):
			self.midi_cc_ch_3_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_4_id_198)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_7.pre_val = value
		self.midi_cc_ch_3_val_7.prev_press_time = time.time()

	def midi_cc_ch_3_val_82_mode169_listener(self, value):
		self.midi_cc_ch_3_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_82, "pre_val"):
			self.midi_cc_ch_3_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_82, "prev_press_time"):
			self.midi_cc_ch_3_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_4_id_199)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_82.pre_val = value
		self.midi_cc_ch_3_val_82.prev_press_time = time.time()

	def midi_cc_ch_4_val_7_mode169_listener(self, value):
		self.midi_cc_ch_4_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_7, "pre_val"):
			self.midi_cc_ch_4_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_7, "prev_press_time"):
			self.midi_cc_ch_4_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_5_id_206)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_7.pre_val = value
		self.midi_cc_ch_4_val_7.prev_press_time = time.time()

	def midi_cc_ch_4_val_82_mode169_listener(self, value):
		self.midi_cc_ch_4_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_82, "pre_val"):
			self.midi_cc_ch_4_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_82, "prev_press_time"):
			self.midi_cc_ch_4_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_5_id_207)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_82.pre_val = value
		self.midi_cc_ch_4_val_82.prev_press_time = time.time()

	def midi_cc_ch_5_val_7_mode169_listener(self, value):
		self.midi_cc_ch_5_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_7, "pre_val"):
			self.midi_cc_ch_5_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_7, "prev_press_time"):
			self.midi_cc_ch_5_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_6_id_214)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_7.pre_val = value
		self.midi_cc_ch_5_val_7.prev_press_time = time.time()

	def midi_cc_ch_5_val_82_mode169_listener(self, value):
		self.midi_cc_ch_5_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_82, "pre_val"):
			self.midi_cc_ch_5_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_82, "prev_press_time"):
			self.midi_cc_ch_5_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_6_id_215)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_82.pre_val = value
		self.midi_cc_ch_5_val_82.prev_press_time = time.time()

	def midi_cc_ch_6_val_7_mode169_listener(self, value):
		self.midi_cc_ch_6_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_7, "pre_val"):
			self.midi_cc_ch_6_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_7, "prev_press_time"):
			self.midi_cc_ch_6_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_7_id_222)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_7.pre_val = value
		self.midi_cc_ch_6_val_7.prev_press_time = time.time()

	def midi_cc_ch_6_val_82_mode169_listener(self, value):
		self.midi_cc_ch_6_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_82, "pre_val"):
			self.midi_cc_ch_6_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_82, "prev_press_time"):
			self.midi_cc_ch_6_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_7_id_223)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_82.pre_val = value
		self.midi_cc_ch_6_val_82.prev_press_time = time.time()

	def midi_cc_ch_7_val_7_mode169_listener(self, value):
		self.midi_cc_ch_7_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_7, "pre_val"):
			self.midi_cc_ch_7_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_7, "prev_press_time"):
			self.midi_cc_ch_7_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_8_id_230)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_7.pre_val = value
		self.midi_cc_ch_7_val_7.prev_press_time = time.time()

	def midi_cc_ch_7_val_82_mode169_listener(self, value):
		self.midi_cc_ch_7_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_82, "pre_val"):
			self.midi_cc_ch_7_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_82, "prev_press_time"):
			self.midi_cc_ch_7_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_8_id_231)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_82.pre_val = value
		self.midi_cc_ch_7_val_82.prev_press_time = time.time()

	def midi_cc_ch_15_val_85_mode169_listener(self, value):
		self.midi_cc_ch_15_val_85.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_85, "pre_val"):
			self.midi_cc_ch_15_val_85.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_85, "prev_press_time"):
			self.midi_cc_ch_15_val_85.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_1_id_234)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_85.pre_val = value
		self.midi_cc_ch_15_val_85.prev_press_time = time.time()

	def midi_cc_ch_15_val_86_mode169_listener(self, value):
		self.midi_cc_ch_15_val_86.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_86, "pre_val"):
			self.midi_cc_ch_15_val_86.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_86, "prev_press_time"):
			self.midi_cc_ch_15_val_86.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_2_id_235)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_86.pre_val = value
		self.midi_cc_ch_15_val_86.prev_press_time = time.time()

	def midi_cc_ch_15_val_87_mode169_listener(self, value):
		self.midi_cc_ch_15_val_87.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_87, "pre_val"):
			self.midi_cc_ch_15_val_87.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_87, "prev_press_time"):
			self.midi_cc_ch_15_val_87.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_3_id_236)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_87.pre_val = value
		self.midi_cc_ch_15_val_87.prev_press_time = time.time()

	def midi_cc_ch_15_val_88_mode169_listener(self, value):
		self.midi_cc_ch_15_val_88.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_88, "pre_val"):
			self.midi_cc_ch_15_val_88.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_88, "prev_press_time"):
			self.midi_cc_ch_15_val_88.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_4_id_237)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_88.pre_val = value
		self.midi_cc_ch_15_val_88.prev_press_time = time.time()

	def midi_cc_ch_15_val_89_mode169_listener(self, value):
		self.midi_cc_ch_15_val_89.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_89, "pre_val"):
			self.midi_cc_ch_15_val_89.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_89, "prev_press_time"):
			self.midi_cc_ch_15_val_89.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_5_id_238)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_89.pre_val = value
		self.midi_cc_ch_15_val_89.prev_press_time = time.time()

	def midi_cc_ch_15_val_90_mode169_listener(self, value):
		self.midi_cc_ch_15_val_90.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_90, "pre_val"):
			self.midi_cc_ch_15_val_90.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_90, "prev_press_time"):
			self.midi_cc_ch_15_val_90.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_6_id_239)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_90.pre_val = value
		self.midi_cc_ch_15_val_90.prev_press_time = time.time()

	def midi_cc_ch_15_val_91_mode169_listener(self, value):
		self.midi_cc_ch_15_val_91.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_91, "pre_val"):
			self.midi_cc_ch_15_val_91.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_91, "prev_press_time"):
			self.midi_cc_ch_15_val_91.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_7_id_240)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_91.pre_val = value
		self.midi_cc_ch_15_val_91.prev_press_time = time.time()

	def midi_cc_ch_15_val_92_mode169_listener(self, value):
		self.midi_cc_ch_15_val_92.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_92, "pre_val"):
			self.midi_cc_ch_15_val_92.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_92, "prev_press_time"):
			self.midi_cc_ch_15_val_92.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_243_active_bank == 0):
			self.pick_brain(self.parameter_8_id_241)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_92.pre_val = value
		self.midi_cc_ch_15_val_92.prev_press_time = time.time()

	def midi_cc_ch_8_val_7_mode169_listener(self, value):
		self.midi_cc_ch_8_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_7, "pre_val"):
			self.midi_cc_ch_8_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_7, "prev_press_time"):
			self.midi_cc_ch_8_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_9_id_248)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_7.pre_val = value
		self.midi_cc_ch_8_val_7.prev_press_time = time.time()

	def midi_cc_ch_8_val_82_mode169_listener(self, value):
		self.midi_cc_ch_8_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_82, "pre_val"):
			self.midi_cc_ch_8_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_82, "prev_press_time"):
			self.midi_cc_ch_8_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_9_id_249)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_82.pre_val = value
		self.midi_cc_ch_8_val_82.prev_press_time = time.time()

	def midi_cc_ch_9_val_7_mode169_listener(self, value):
		self.midi_cc_ch_9_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_7, "pre_val"):
			self.midi_cc_ch_9_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_7, "prev_press_time"):
			self.midi_cc_ch_9_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_10_id_256)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_7.pre_val = value
		self.midi_cc_ch_9_val_7.prev_press_time = time.time()

	def midi_cc_ch_9_val_82_mode169_listener(self, value):
		self.midi_cc_ch_9_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_82, "pre_val"):
			self.midi_cc_ch_9_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_82, "prev_press_time"):
			self.midi_cc_ch_9_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_10_id_257)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_82.pre_val = value
		self.midi_cc_ch_9_val_82.prev_press_time = time.time()

	def midi_cc_ch_10_val_7_mode169_listener(self, value):
		self.midi_cc_ch_10_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_7, "pre_val"):
			self.midi_cc_ch_10_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_7, "prev_press_time"):
			self.midi_cc_ch_10_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_11_id_264)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_7.pre_val = value
		self.midi_cc_ch_10_val_7.prev_press_time = time.time()

	def midi_cc_ch_10_val_82_mode169_listener(self, value):
		self.midi_cc_ch_10_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_82, "pre_val"):
			self.midi_cc_ch_10_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_82, "prev_press_time"):
			self.midi_cc_ch_10_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_11_id_265)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_82.pre_val = value
		self.midi_cc_ch_10_val_82.prev_press_time = time.time()

	def midi_cc_ch_11_val_7_mode169_listener(self, value):
		self.midi_cc_ch_11_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_7, "pre_val"):
			self.midi_cc_ch_11_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_7, "prev_press_time"):
			self.midi_cc_ch_11_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_12_id_272)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_7.pre_val = value
		self.midi_cc_ch_11_val_7.prev_press_time = time.time()

	def midi_cc_ch_11_val_82_mode169_listener(self, value):
		self.midi_cc_ch_11_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_82, "pre_val"):
			self.midi_cc_ch_11_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_82, "prev_press_time"):
			self.midi_cc_ch_11_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_12_id_273)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_82.pre_val = value
		self.midi_cc_ch_11_val_82.prev_press_time = time.time()

	def midi_cc_ch_12_val_7_mode169_listener(self, value):
		self.midi_cc_ch_12_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_7, "pre_val"):
			self.midi_cc_ch_12_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_7, "prev_press_time"):
			self.midi_cc_ch_12_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_13_id_280)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_7.pre_val = value
		self.midi_cc_ch_12_val_7.prev_press_time = time.time()

	def midi_cc_ch_12_val_82_mode169_listener(self, value):
		self.midi_cc_ch_12_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_82, "pre_val"):
			self.midi_cc_ch_12_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_82, "prev_press_time"):
			self.midi_cc_ch_12_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_13_id_281)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_82.pre_val = value
		self.midi_cc_ch_12_val_82.prev_press_time = time.time()

	def midi_cc_ch_13_val_7_mode169_listener(self, value):
		self.midi_cc_ch_13_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_7, "pre_val"):
			self.midi_cc_ch_13_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_7, "prev_press_time"):
			self.midi_cc_ch_13_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_14_id_288)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_7.pre_val = value
		self.midi_cc_ch_13_val_7.prev_press_time = time.time()

	def midi_cc_ch_13_val_82_mode169_listener(self, value):
		self.midi_cc_ch_13_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_82, "pre_val"):
			self.midi_cc_ch_13_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_82, "prev_press_time"):
			self.midi_cc_ch_13_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_14_id_289)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_82.pre_val = value
		self.midi_cc_ch_13_val_82.prev_press_time = time.time()

	def midi_cc_ch_14_val_7_mode169_listener(self, value):
		self.midi_cc_ch_14_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_7, "pre_val"):
			self.midi_cc_ch_14_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_7, "prev_press_time"):
			self.midi_cc_ch_14_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_15_id_296)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_7.pre_val = value
		self.midi_cc_ch_14_val_7.prev_press_time = time.time()

	def midi_cc_ch_14_val_82_mode169_listener(self, value):
		self.midi_cc_ch_14_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_82, "pre_val"):
			self.midi_cc_ch_14_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_82, "prev_press_time"):
			self.midi_cc_ch_14_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_15_id_297)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_82.pre_val = value
		self.midi_cc_ch_14_val_82.prev_press_time = time.time()

	def midi_cc_ch_15_val_7_mode169_listener(self, value):
		self.midi_cc_ch_15_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_7, "pre_val"):
			self.midi_cc_ch_15_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_7, "prev_press_time"):
			self.midi_cc_ch_15_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_16_id_304)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_7.pre_val = value
		self.midi_cc_ch_15_val_7.prev_press_time = time.time()

	def midi_cc_ch_15_val_82_mode169_listener(self, value):
		self.midi_cc_ch_15_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_82, "pre_val"):
			self.midi_cc_ch_15_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_82, "prev_press_time"):
			self.midi_cc_ch_15_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.pan_16_id_305)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_82.pre_val = value
		self.midi_cc_ch_15_val_82.prev_press_time = time.time()

	def midi_cc_ch_0_val_94_mode169_listener(self, value):
		self.midi_cc_ch_0_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_94, "pre_val"):
			self.midi_cc_ch_0_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_94, "prev_press_time"):
			self.midi_cc_ch_0_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_1_id_328)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_94.pre_val = value
		self.midi_cc_ch_0_val_94.prev_press_time = time.time()

	def midi_cc_ch_1_val_94_mode169_listener(self, value):
		self.midi_cc_ch_1_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_94, "pre_val"):
			self.midi_cc_ch_1_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_94, "prev_press_time"):
			self.midi_cc_ch_1_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_2_id_329)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_94.pre_val = value
		self.midi_cc_ch_1_val_94.prev_press_time = time.time()

	def midi_cc_ch_2_val_94_mode169_listener(self, value):
		self.midi_cc_ch_2_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_94, "pre_val"):
			self.midi_cc_ch_2_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_94, "prev_press_time"):
			self.midi_cc_ch_2_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_3_id_330)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_94.pre_val = value
		self.midi_cc_ch_2_val_94.prev_press_time = time.time()

	def midi_cc_ch_3_val_94_mode169_listener(self, value):
		self.midi_cc_ch_3_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_94, "pre_val"):
			self.midi_cc_ch_3_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_94, "prev_press_time"):
			self.midi_cc_ch_3_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_4_id_331)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_94.pre_val = value
		self.midi_cc_ch_3_val_94.prev_press_time = time.time()

	def midi_cc_ch_4_val_94_mode169_listener(self, value):
		self.midi_cc_ch_4_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_94, "pre_val"):
			self.midi_cc_ch_4_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_94, "prev_press_time"):
			self.midi_cc_ch_4_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_5_id_332)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_94.pre_val = value
		self.midi_cc_ch_4_val_94.prev_press_time = time.time()

	def midi_cc_ch_5_val_94_mode169_listener(self, value):
		self.midi_cc_ch_5_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_94, "pre_val"):
			self.midi_cc_ch_5_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_94, "prev_press_time"):
			self.midi_cc_ch_5_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_6_id_333)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_94.pre_val = value
		self.midi_cc_ch_5_val_94.prev_press_time = time.time()

	def midi_cc_ch_6_val_94_mode169_listener(self, value):
		self.midi_cc_ch_6_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_94, "pre_val"):
			self.midi_cc_ch_6_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_94, "prev_press_time"):
			self.midi_cc_ch_6_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_7_id_334)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_94.pre_val = value
		self.midi_cc_ch_6_val_94.prev_press_time = time.time()

	def midi_cc_ch_7_val_94_mode169_listener(self, value):
		self.midi_cc_ch_7_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_7_val_94, "pre_val"):
			self.midi_cc_ch_7_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_7_val_94, "prev_press_time"):
			self.midi_cc_ch_7_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_8_id_335)
		######################################
		### After running everything #####
		self.midi_cc_ch_7_val_94.pre_val = value
		self.midi_cc_ch_7_val_94.prev_press_time = time.time()

	def midi_cc_ch_8_val_94_mode169_listener(self, value):
		self.midi_cc_ch_8_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_8_val_94, "pre_val"):
			self.midi_cc_ch_8_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_8_val_94, "prev_press_time"):
			self.midi_cc_ch_8_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_9_id_336)
		######################################
		### After running everything #####
		self.midi_cc_ch_8_val_94.pre_val = value
		self.midi_cc_ch_8_val_94.prev_press_time = time.time()

	def midi_cc_ch_9_val_94_mode169_listener(self, value):
		self.midi_cc_ch_9_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_9_val_94, "pre_val"):
			self.midi_cc_ch_9_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_9_val_94, "prev_press_time"):
			self.midi_cc_ch_9_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_10_id_337)
		######################################
		### After running everything #####
		self.midi_cc_ch_9_val_94.pre_val = value
		self.midi_cc_ch_9_val_94.prev_press_time = time.time()

	def midi_cc_ch_10_val_94_mode169_listener(self, value):
		self.midi_cc_ch_10_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_10_val_94, "pre_val"):
			self.midi_cc_ch_10_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_10_val_94, "prev_press_time"):
			self.midi_cc_ch_10_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_11_id_338)
		######################################
		### After running everything #####
		self.midi_cc_ch_10_val_94.pre_val = value
		self.midi_cc_ch_10_val_94.prev_press_time = time.time()

	def midi_cc_ch_11_val_94_mode169_listener(self, value):
		self.midi_cc_ch_11_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_11_val_94, "pre_val"):
			self.midi_cc_ch_11_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_11_val_94, "prev_press_time"):
			self.midi_cc_ch_11_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_12_id_339)
		######################################
		### After running everything #####
		self.midi_cc_ch_11_val_94.pre_val = value
		self.midi_cc_ch_11_val_94.prev_press_time = time.time()

	def midi_cc_ch_12_val_94_mode169_listener(self, value):
		self.midi_cc_ch_12_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_12_val_94, "pre_val"):
			self.midi_cc_ch_12_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_12_val_94, "prev_press_time"):
			self.midi_cc_ch_12_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_13_id_340)
		######################################
		### After running everything #####
		self.midi_cc_ch_12_val_94.pre_val = value
		self.midi_cc_ch_12_val_94.prev_press_time = time.time()

	def midi_cc_ch_13_val_94_mode169_listener(self, value):
		self.midi_cc_ch_13_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_13_val_94, "pre_val"):
			self.midi_cc_ch_13_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_13_val_94, "prev_press_time"):
			self.midi_cc_ch_13_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_14_id_341)
		######################################
		### After running everything #####
		self.midi_cc_ch_13_val_94.pre_val = value
		self.midi_cc_ch_13_val_94.prev_press_time = time.time()

	def midi_cc_ch_14_val_94_mode169_listener(self, value):
		self.midi_cc_ch_14_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_14_val_94, "pre_val"):
			self.midi_cc_ch_14_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_14_val_94, "prev_press_time"):
			self.midi_cc_ch_14_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_15_id_342)
		######################################
		### After running everything #####
		self.midi_cc_ch_14_val_94.pre_val = value
		self.midi_cc_ch_14_val_94.prev_press_time = time.time()

	def midi_cc_ch_15_val_94_mode169_listener(self, value):
		self.midi_cc_ch_15_val_94.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_94, "pre_val"):
			self.midi_cc_ch_15_val_94.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_94, "prev_press_time"):
			self.midi_cc_ch_15_val_94.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.solo_16_id_343)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_94.pre_val = value
		self.midi_cc_ch_15_val_94.prev_press_time = time.time()

	def midi_cc_ch_15_val_120_mode169_listener(self, value):
		self.midi_cc_ch_15_val_120.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_120, "pre_val"):
			self.midi_cc_ch_15_val_120.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_120, "prev_press_time"):
			self.midi_cc_ch_15_val_120.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.mode_selector_1_copy_id_346)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_120.pre_val = value
		self.midi_cc_ch_15_val_120.prev_press_time = time.time()

	def midi_cc_ch_15_val_121_mode1_listener(self, value):
		self.midi_cc_ch_15_val_121.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_121, "pre_val"):
			self.midi_cc_ch_15_val_121.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_121, "prev_press_time"):
			self.midi_cc_ch_15_val_121.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.session_box_navigation_1_copy_id_347)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_121.pre_val = value
		self.midi_cc_ch_15_val_121.prev_press_time = time.time()

	def _mode1_configs(self):
		self.mode_1_configs_map = [
			"track_1_id_2",
			"volume_1_id_3",
			"pan_1_id_4",
			"mute_1_id_5",
			"send_1_id_8",
			"send_2_id_9",
			"send_3_id_10",
			"send_4_id_11",
			"track_2_id_12",
			"send_1_id_13",
			"send_2_id_14",
			"send_3_id_15",
			"send_4_id_16",
			"volume_2_id_17",
			"pan_2_id_18",
			"mute_2_id_19",
			"track_3_id_22",
			"send_1_id_23",
			"send_2_id_24",
			"send_3_id_25",
			"send_4_id_26",
			"volume_3_id_27",
			"pan_3_id_28",
			"mute_3_id_29",
			"track_4_id_32",
			"send_1_id_33",
			"send_2_id_34",
			"send_3_id_35",
			"send_4_id_36",
			"volume_4_id_37",
			"pan_4_id_38",
			"mute_4_id_39",
			"track_5_id_42",
			"send_1_id_43",
			"send_2_id_44",
			"send_3_id_45",
			"send_4_id_46",
			"volume_5_id_47",
			"pan_5_id_48",
			"mute_5_id_49",
			"track_6_id_52",
			"send_1_id_53",
			"send_2_id_54",
			"send_3_id_55",
			"send_4_id_56",
			"volume_6_id_57",
			"pan_6_id_58",
			"mute_6_id_59",
			"track_7_id_62",
			"send_1_id_63",
			"send_2_id_64",
			"send_3_id_65",
			"send_4_id_66",
			"volume_7_id_67",
			"pan_7_id_68",
			"mute_7_id_69",
			"track_8_id_72",
			"send_1_id_73",
			"send_2_id_74",
			"send_3_id_75",
			"send_4_id_76",
			"volume_8_id_77",
			"pan_8_id_78",
			"mute_8_id_79",
			"track_select_id_85",
			"device_1_id_86",
			"parameter_bank_1_id_87",
			"parameter_1_id_88",
			"parameter_2_id_89",
			"parameter_3_id_90",
			"parameter_4_id_91",
			"parameter_5_id_92",
			"parameter_6_id_93",
			"parameter_7_id_94",
			"parameter_8_id_95",
			"track_9_id_96",
			"send_1_id_97",
			"send_2_id_98",
			"send_3_id_99",
			"send_4_id_100",
			"volume_9_id_101",
			"pan_9_id_102",
			"mute_9_id_103",
			"track_10_id_105",
			"send_1_id_106",
			"send_2_id_107",
			"send_3_id_108",
			"send_4_id_109",
			"volume_10_id_110",
			"pan_10_id_111",
			"mute_10_id_112",
			"track_11_id_114",
			"send_1_id_115",
			"send_2_id_116",
			"send_3_id_117",
			"send_4_id_118",
			"volume_11_id_119",
			"pan_11_id_120",
			"mute_11_id_121",
			"track_12_id_123",
			"send_1_id_124",
			"send_2_id_125",
			"send_3_id_126",
			"send_4_id_127",
			"volume_12_id_128",
			"pan_12_id_129",
			"mute_12_id_130",
			"track_13_id_132",
			"send_1_id_133",
			"send_2_id_134",
			"send_3_id_135",
			"send_4_id_136",
			"volume_13_id_137",
			"pan_13_id_138",
			"mute_13_id_139",
			"track_14_id_141",
			"send_1_id_142",
			"send_2_id_143",
			"send_3_id_144",
			"send_4_id_145",
			"volume_14_id_146",
			"pan_14_id_147",
			"mute_14_id_148",
			"track_15_id_150",
			"send_1_id_151",
			"send_2_id_152",
			"send_3_id_153",
			"send_4_id_154",
			"volume_15_id_155",
			"pan_15_id_156",
			"mute_15_id_157",
			"track_16_id_159",
			"send_1_id_160",
			"send_2_id_161",
			"send_3_id_162",
			"send_4_id_163",
			"volume_16_id_164",
			"pan_16_id_165",
			"mute_16_id_166",
			"mode_selector_1_id_168",
			"session_box_navigation_1_copy_id_347"]
		self.track_1_id_2 = {}
		self.track_1_id_2["track"] = self.track_num(2)
		self.track_1_id_2["module"] = "self.song().tracks[self.track_num(0)]"
		self.track_1_id_2["LED_mapping_type_needs_feedback"] = ""
		self.track_1_id_2["LED_feedback"] = "custom"
		self.track_1_id_2["LED_feedback_active"] = ""
		self.track_1_id_2["LED_on"] = "127"
		self.track_1_id_2["LED_off"] = "0"
		self.track_1_id_2["LED_send_feedback_to_selected"] = []
		self.track_1_id_2["json_id"] = 2
		self.track_1_id_2["mapping_name"] = "Track 1"
		self.track_1_id_2["mapping_type"] = "Track"
		self.track_1_id_2["parent_json_id"] = 1
		self.track_1_id_2["parent_name"] = "mode_1_id_1"
		self.volume_1_id_3 = {}
		self.volume_1_id_3["attached_to"] = "midi_cc_ch_0_val_7"
		self.volume_1_id_3["track"] = self.track_num(2)
		self.volume_1_id_3["module"] = "self.song().tracks[self.track_num(0)].mixer_device.volume"
		self.volume_1_id_3["element"] = "value"
		self.volume_1_id_3["output_type"] = "val"
		self.volume_1_id_3["minimum"] = round(0,2)
		self.volume_1_id_3["maximum"] = round(85,2)
		self.volume_1_id_3["decimal_places"] = 2
		self.volume_1_id_3["ui_listener"] = "value"
		self.volume_1_id_3["feedback_brain"] = "feedback_range"
		self.volume_1_id_3["ctrl_type"] = "absolute"
		self.volume_1_id_3["takeover_mode"] = "None"
		self.volume_1_id_3["enc_first"] = 0
		self.volume_1_id_3["enc_second"] = 127
		self.volume_1_id_3["reverse_mode"] = False
		self.volume_1_id_3["LED_mapping_type_needs_feedback"] = "1"
		self.volume_1_id_3["LED_feedback"] = "default"
		self.volume_1_id_3["LED_feedback_active"] = "1"
		self.volume_1_id_3["LED_on"] = "127"
		self.volume_1_id_3["LED_off"] = "0"
		self.volume_1_id_3["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_7"]
		self.volume_1_id_3["snap_to"] = True
		self.volume_1_id_3["json_id"] = 3
		self.volume_1_id_3["mapping_name"] = "Volume 1"
		self.volume_1_id_3["mapping_type"] = "Volume"
		self.volume_1_id_3["parent_json_id"] = 2
		self.volume_1_id_3["parent_name"] = "track_1_id_2"
		self.pan_1_id_4 = {}
		self.pan_1_id_4["attached_to"] = "midi_cc_ch_0_val_82"
		self.pan_1_id_4["track"] = self.track_num(2)
		self.pan_1_id_4["module"] = "self.song().tracks[self.track_num(0)].mixer_device.panning"
		self.pan_1_id_4["element"] = "value"
		self.pan_1_id_4["output_type"] = "val"
		self.pan_1_id_4["minimum"] = round(0,2)
		self.pan_1_id_4["maximum"] = round(100,2)
		self.pan_1_id_4["decimal_places"] = 2
		self.pan_1_id_4["ui_listener"] = "value"
		self.pan_1_id_4["feedback_brain"] = "feedback_range"
		self.pan_1_id_4["ctrl_type"] = "absolute"
		self.pan_1_id_4["takeover_mode"] = "Value scaling"
		self.pan_1_id_4["enc_first"] = 0
		self.pan_1_id_4["enc_second"] = 127
		self.pan_1_id_4["reverse_mode"] = False
		self.pan_1_id_4["LED_mapping_type_needs_feedback"] = "1"
		self.pan_1_id_4["LED_feedback"] = "default"
		self.pan_1_id_4["LED_feedback_active"] = "1"
		self.pan_1_id_4["LED_on"] = "127"
		self.pan_1_id_4["LED_off"] = "0"
		self.pan_1_id_4["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_82"]
		self.pan_1_id_4["snap_to"] = True
		self.pan_1_id_4["json_id"] = 4
		self.pan_1_id_4["mapping_name"] = "Pan 1"
		self.pan_1_id_4["mapping_type"] = "Pan"
		self.pan_1_id_4["parent_json_id"] = 2
		self.pan_1_id_4["parent_name"] = "track_1_id_2"
		self.mute_1_id_5 = {}
		self.mute_1_id_5["attached_to"] = "midi_cc_ch_0_val_94"
		self.mute_1_id_5["track"] = self.track_num(2)
		self.mute_1_id_5["module"] = "self.song().tracks[self.track_num(0)]"
		self.mute_1_id_5["element"] = "mute"
		self.mute_1_id_5["output_type"] = "bool"
		self.mute_1_id_5["ui_listener"] = "mute"
		self.mute_1_id_5["feedback_brain"] = "feedback_bool"
		self.mute_1_id_5["enc_first"] = 127
		self.mute_1_id_5["enc_second"] = 0
		self.mute_1_id_5["switch_type"] = "toggle"
		self.mute_1_id_5["ctrl_type"] = "on/off"
		self.mute_1_id_5["LED_mapping_type_needs_feedback"] = "1"
		self.mute_1_id_5["LED_feedback"] = "default"
		self.mute_1_id_5["LED_feedback_active"] = "1"
		self.mute_1_id_5["LED_on"] = "127"
		self.mute_1_id_5["LED_off"] = "0"
		self.mute_1_id_5["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_94"]
		self.mute_1_id_5["json_id"] = 5
		self.mute_1_id_5["mapping_name"] = "Mute 1"
		self.mute_1_id_5["mapping_type"] = "Mute"
		self.mute_1_id_5["parent_json_id"] = 2
		self.mute_1_id_5["parent_name"] = "track_1_id_2"
		self.send_1_id_8 = {}
		self.send_1_id_8["attached_to"] = "midi_cc_ch_0_val_83"
		self.send_1_id_8["track"] = self.track_num(2)
		self.send_1_id_8["module"] = "self.song().tracks[self.track_num(0)].mixer_device.sends[0]"
		self.send_1_id_8["element"] = "value"
		self.send_1_id_8["output_type"] = "val"
		self.send_1_id_8["minimum"] = round(0,3)
		self.send_1_id_8["maximum"] = round(100,3)
		self.send_1_id_8["decimal_places"] = 3
		self.send_1_id_8["ui_listener"] = "value"
		self.send_1_id_8["feedback_brain"] = "feedback_range"
		self.send_1_id_8["ctrl_type"] = "absolute"
		self.send_1_id_8["takeover_mode"] = "Value scaling"
		self.send_1_id_8["enc_first"] = 0
		self.send_1_id_8["enc_second"] = 127
		self.send_1_id_8["reverse_mode"] = False
		self.send_1_id_8["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_8["LED_feedback"] = "default"
		self.send_1_id_8["LED_feedback_active"] = "1"
		self.send_1_id_8["LED_on"] = "127"
		self.send_1_id_8["LED_off"] = "0"
		self.send_1_id_8["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_83"]
		self.send_1_id_8["snap_to"] = True
		self.send_1_id_8["json_id"] = 8
		self.send_1_id_8["mapping_name"] = "Send 1"
		self.send_1_id_8["mapping_type"] = "Send"
		self.send_1_id_8["parent_json_id"] = 7
		self.send_1_id_8["parent_name"] = "sends_1_id_7"
		self.send_2_id_9 = {}
		self.send_2_id_9["attached_to"] = "midi_cc_ch_0_val_71"
		self.send_2_id_9["track"] = self.track_num(2)
		self.send_2_id_9["module"] = "self.song().tracks[self.track_num(0)].mixer_device.sends[1]"
		self.send_2_id_9["element"] = "value"
		self.send_2_id_9["output_type"] = "val"
		self.send_2_id_9["minimum"] = round(0,3)
		self.send_2_id_9["maximum"] = round(100,3)
		self.send_2_id_9["decimal_places"] = 3
		self.send_2_id_9["ui_listener"] = "value"
		self.send_2_id_9["feedback_brain"] = "feedback_range"
		self.send_2_id_9["ctrl_type"] = "absolute"
		self.send_2_id_9["takeover_mode"] = "Value scaling"
		self.send_2_id_9["enc_first"] = 0
		self.send_2_id_9["enc_second"] = 127
		self.send_2_id_9["reverse_mode"] = False
		self.send_2_id_9["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_9["LED_feedback"] = "default"
		self.send_2_id_9["LED_feedback_active"] = "1"
		self.send_2_id_9["LED_on"] = "127"
		self.send_2_id_9["LED_off"] = "0"
		self.send_2_id_9["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_71"]
		self.send_2_id_9["snap_to"] = True
		self.send_2_id_9["json_id"] = 9
		self.send_2_id_9["mapping_name"] = "Send 2"
		self.send_2_id_9["mapping_type"] = "Send"
		self.send_2_id_9["parent_json_id"] = 7
		self.send_2_id_9["parent_name"] = "sends_1_id_7"
		self.send_3_id_10 = {}
		self.send_3_id_10["attached_to"] = "midi_cc_ch_0_val_70"
		self.send_3_id_10["track"] = self.track_num(2)
		self.send_3_id_10["module"] = "self.song().tracks[self.track_num(0)].mixer_device.sends[2]"
		self.send_3_id_10["element"] = "value"
		self.send_3_id_10["output_type"] = "val"
		self.send_3_id_10["minimum"] = round(0,3)
		self.send_3_id_10["maximum"] = round(100,3)
		self.send_3_id_10["decimal_places"] = 3
		self.send_3_id_10["ui_listener"] = "value"
		self.send_3_id_10["feedback_brain"] = "feedback_range"
		self.send_3_id_10["ctrl_type"] = "absolute"
		self.send_3_id_10["takeover_mode"] = "Value scaling"
		self.send_3_id_10["enc_first"] = 0
		self.send_3_id_10["enc_second"] = 127
		self.send_3_id_10["reverse_mode"] = False
		self.send_3_id_10["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_10["LED_feedback"] = "default"
		self.send_3_id_10["LED_feedback_active"] = "1"
		self.send_3_id_10["LED_on"] = "127"
		self.send_3_id_10["LED_off"] = "0"
		self.send_3_id_10["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_70"]
		self.send_3_id_10["snap_to"] = True
		self.send_3_id_10["json_id"] = 10
		self.send_3_id_10["mapping_name"] = "Send 3"
		self.send_3_id_10["mapping_type"] = "Send"
		self.send_3_id_10["parent_json_id"] = 7
		self.send_3_id_10["parent_name"] = "sends_1_id_7"
		self.send_4_id_11 = {}
		self.send_4_id_11["attached_to"] = "midi_cc_ch_0_val_10"
		self.send_4_id_11["track"] = self.track_num(2)
		self.send_4_id_11["module"] = "self.song().tracks[self.track_num(0)].mixer_device.sends[3]"
		self.send_4_id_11["element"] = "value"
		self.send_4_id_11["output_type"] = "val"
		self.send_4_id_11["minimum"] = round(0,3)
		self.send_4_id_11["maximum"] = round(100,3)
		self.send_4_id_11["decimal_places"] = 3
		self.send_4_id_11["ui_listener"] = "value"
		self.send_4_id_11["feedback_brain"] = "feedback_range"
		self.send_4_id_11["ctrl_type"] = "absolute"
		self.send_4_id_11["takeover_mode"] = "Value scaling"
		self.send_4_id_11["enc_first"] = 0
		self.send_4_id_11["enc_second"] = 127
		self.send_4_id_11["reverse_mode"] = False
		self.send_4_id_11["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_11["LED_feedback"] = "default"
		self.send_4_id_11["LED_feedback_active"] = "1"
		self.send_4_id_11["LED_on"] = "127"
		self.send_4_id_11["LED_off"] = "0"
		self.send_4_id_11["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_10"]
		self.send_4_id_11["snap_to"] = True
		self.send_4_id_11["json_id"] = 11
		self.send_4_id_11["mapping_name"] = "Send 4"
		self.send_4_id_11["mapping_type"] = "Send"
		self.send_4_id_11["parent_json_id"] = 7
		self.send_4_id_11["parent_name"] = "sends_1_id_7"
		self.track_2_id_12 = {}
		self.track_2_id_12["track"] = self.track_num(2)
		self.track_2_id_12["module"] = "self.song().tracks[self.track_num(1)]"
		self.track_2_id_12["LED_mapping_type_needs_feedback"] = ""
		self.track_2_id_12["LED_feedback"] = "custom"
		self.track_2_id_12["LED_feedback_active"] = ""
		self.track_2_id_12["LED_on"] = "127"
		self.track_2_id_12["LED_off"] = "0"
		self.track_2_id_12["LED_send_feedback_to_selected"] = []
		self.track_2_id_12["json_id"] = 12
		self.track_2_id_12["mapping_name"] = "Track 2"
		self.track_2_id_12["mapping_type"] = "Track"
		self.track_2_id_12["parent_json_id"] = 1
		self.track_2_id_12["parent_name"] = "mode_1_id_1"
		self.send_1_id_13 = {}
		self.send_1_id_13["attached_to"] = "midi_cc_ch_1_val_83"
		self.send_1_id_13["track"] = self.track_num(2)
		self.send_1_id_13["module"] = "self.song().tracks[self.track_num(1)].mixer_device.sends[0]"
		self.send_1_id_13["element"] = "value"
		self.send_1_id_13["output_type"] = "val"
		self.send_1_id_13["minimum"] = round(0,3)
		self.send_1_id_13["maximum"] = round(100,3)
		self.send_1_id_13["decimal_places"] = 3
		self.send_1_id_13["ui_listener"] = "value"
		self.send_1_id_13["feedback_brain"] = "feedback_range"
		self.send_1_id_13["ctrl_type"] = "absolute"
		self.send_1_id_13["takeover_mode"] = "Value scaling"
		self.send_1_id_13["enc_first"] = 0
		self.send_1_id_13["enc_second"] = 127
		self.send_1_id_13["reverse_mode"] = False
		self.send_1_id_13["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_13["LED_feedback"] = "default"
		self.send_1_id_13["LED_feedback_active"] = "1"
		self.send_1_id_13["LED_on"] = "127"
		self.send_1_id_13["LED_off"] = "0"
		self.send_1_id_13["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_83"]
		self.send_1_id_13["snap_to"] = True
		self.send_1_id_13["json_id"] = 13
		self.send_1_id_13["mapping_name"] = "Send 1"
		self.send_1_id_13["mapping_type"] = "Send"
		self.send_1_id_13["parent_json_id"] = 21
		self.send_1_id_13["parent_name"] = "sends_2_id_21"
		self.send_2_id_14 = {}
		self.send_2_id_14["attached_to"] = "midi_cc_ch_1_val_71"
		self.send_2_id_14["track"] = self.track_num(2)
		self.send_2_id_14["module"] = "self.song().tracks[self.track_num(1)].mixer_device.sends[1]"
		self.send_2_id_14["element"] = "value"
		self.send_2_id_14["output_type"] = "val"
		self.send_2_id_14["minimum"] = round(0,3)
		self.send_2_id_14["maximum"] = round(100,3)
		self.send_2_id_14["decimal_places"] = 3
		self.send_2_id_14["ui_listener"] = "value"
		self.send_2_id_14["feedback_brain"] = "feedback_range"
		self.send_2_id_14["ctrl_type"] = "absolute"
		self.send_2_id_14["takeover_mode"] = "Value scaling"
		self.send_2_id_14["enc_first"] = 0
		self.send_2_id_14["enc_second"] = 127
		self.send_2_id_14["reverse_mode"] = False
		self.send_2_id_14["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_14["LED_feedback"] = "default"
		self.send_2_id_14["LED_feedback_active"] = "1"
		self.send_2_id_14["LED_on"] = "127"
		self.send_2_id_14["LED_off"] = "0"
		self.send_2_id_14["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_71"]
		self.send_2_id_14["snap_to"] = True
		self.send_2_id_14["json_id"] = 14
		self.send_2_id_14["mapping_name"] = "Send 2"
		self.send_2_id_14["mapping_type"] = "Send"
		self.send_2_id_14["parent_json_id"] = 21
		self.send_2_id_14["parent_name"] = "sends_2_id_21"
		self.send_3_id_15 = {}
		self.send_3_id_15["attached_to"] = "midi_cc_ch_1_val_70"
		self.send_3_id_15["track"] = self.track_num(2)
		self.send_3_id_15["module"] = "self.song().tracks[self.track_num(1)].mixer_device.sends[2]"
		self.send_3_id_15["element"] = "value"
		self.send_3_id_15["output_type"] = "val"
		self.send_3_id_15["minimum"] = round(0,3)
		self.send_3_id_15["maximum"] = round(100,3)
		self.send_3_id_15["decimal_places"] = 3
		self.send_3_id_15["ui_listener"] = "value"
		self.send_3_id_15["feedback_brain"] = "feedback_range"
		self.send_3_id_15["ctrl_type"] = "absolute"
		self.send_3_id_15["takeover_mode"] = "Value scaling"
		self.send_3_id_15["enc_first"] = 0
		self.send_3_id_15["enc_second"] = 127
		self.send_3_id_15["reverse_mode"] = False
		self.send_3_id_15["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_15["LED_feedback"] = "default"
		self.send_3_id_15["LED_feedback_active"] = "1"
		self.send_3_id_15["LED_on"] = "127"
		self.send_3_id_15["LED_off"] = "0"
		self.send_3_id_15["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_70"]
		self.send_3_id_15["snap_to"] = True
		self.send_3_id_15["json_id"] = 15
		self.send_3_id_15["mapping_name"] = "Send 3"
		self.send_3_id_15["mapping_type"] = "Send"
		self.send_3_id_15["parent_json_id"] = 21
		self.send_3_id_15["parent_name"] = "sends_2_id_21"
		self.send_4_id_16 = {}
		self.send_4_id_16["attached_to"] = "midi_cc_ch_1_val_10"
		self.send_4_id_16["track"] = self.track_num(2)
		self.send_4_id_16["module"] = "self.song().tracks[self.track_num(1)].mixer_device.sends[3]"
		self.send_4_id_16["element"] = "value"
		self.send_4_id_16["output_type"] = "val"
		self.send_4_id_16["minimum"] = round(0,3)
		self.send_4_id_16["maximum"] = round(100,3)
		self.send_4_id_16["decimal_places"] = 3
		self.send_4_id_16["ui_listener"] = "value"
		self.send_4_id_16["feedback_brain"] = "feedback_range"
		self.send_4_id_16["ctrl_type"] = "absolute"
		self.send_4_id_16["takeover_mode"] = "Value scaling"
		self.send_4_id_16["enc_first"] = 0
		self.send_4_id_16["enc_second"] = 127
		self.send_4_id_16["reverse_mode"] = False
		self.send_4_id_16["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_16["LED_feedback"] = "default"
		self.send_4_id_16["LED_feedback_active"] = "1"
		self.send_4_id_16["LED_on"] = "127"
		self.send_4_id_16["LED_off"] = "0"
		self.send_4_id_16["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_10"]
		self.send_4_id_16["snap_to"] = True
		self.send_4_id_16["json_id"] = 16
		self.send_4_id_16["mapping_name"] = "Send 4"
		self.send_4_id_16["mapping_type"] = "Send"
		self.send_4_id_16["parent_json_id"] = 21
		self.send_4_id_16["parent_name"] = "sends_2_id_21"
		self.volume_2_id_17 = {}
		self.volume_2_id_17["attached_to"] = "midi_cc_ch_1_val_7"
		self.volume_2_id_17["track"] = self.track_num(2)
		self.volume_2_id_17["module"] = "self.song().tracks[self.track_num(1)].mixer_device.volume"
		self.volume_2_id_17["element"] = "value"
		self.volume_2_id_17["output_type"] = "val"
		self.volume_2_id_17["minimum"] = round(0,2)
		self.volume_2_id_17["maximum"] = round(85,2)
		self.volume_2_id_17["decimal_places"] = 2
		self.volume_2_id_17["ui_listener"] = "value"
		self.volume_2_id_17["feedback_brain"] = "feedback_range"
		self.volume_2_id_17["ctrl_type"] = "absolute"
		self.volume_2_id_17["takeover_mode"] = "None"
		self.volume_2_id_17["enc_first"] = 0
		self.volume_2_id_17["enc_second"] = 127
		self.volume_2_id_17["reverse_mode"] = False
		self.volume_2_id_17["LED_mapping_type_needs_feedback"] = "1"
		self.volume_2_id_17["LED_feedback"] = "default"
		self.volume_2_id_17["LED_feedback_active"] = "1"
		self.volume_2_id_17["LED_on"] = "127"
		self.volume_2_id_17["LED_off"] = "0"
		self.volume_2_id_17["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_7"]
		self.volume_2_id_17["snap_to"] = True
		self.volume_2_id_17["json_id"] = 17
		self.volume_2_id_17["mapping_name"] = "Volume 2"
		self.volume_2_id_17["mapping_type"] = "Volume"
		self.volume_2_id_17["parent_json_id"] = 12
		self.volume_2_id_17["parent_name"] = "track_2_id_12"
		self.pan_2_id_18 = {}
		self.pan_2_id_18["attached_to"] = "midi_cc_ch_1_val_82"
		self.pan_2_id_18["track"] = self.track_num(2)
		self.pan_2_id_18["module"] = "self.song().tracks[self.track_num(1)].mixer_device.panning"
		self.pan_2_id_18["element"] = "value"
		self.pan_2_id_18["output_type"] = "val"
		self.pan_2_id_18["minimum"] = round(0,2)
		self.pan_2_id_18["maximum"] = round(100,2)
		self.pan_2_id_18["decimal_places"] = 2
		self.pan_2_id_18["ui_listener"] = "value"
		self.pan_2_id_18["feedback_brain"] = "feedback_range"
		self.pan_2_id_18["ctrl_type"] = "absolute"
		self.pan_2_id_18["takeover_mode"] = "Value scaling"
		self.pan_2_id_18["enc_first"] = 0
		self.pan_2_id_18["enc_second"] = 127
		self.pan_2_id_18["reverse_mode"] = False
		self.pan_2_id_18["LED_mapping_type_needs_feedback"] = "1"
		self.pan_2_id_18["LED_feedback"] = "default"
		self.pan_2_id_18["LED_feedback_active"] = "1"
		self.pan_2_id_18["LED_on"] = "127"
		self.pan_2_id_18["LED_off"] = "0"
		self.pan_2_id_18["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_82"]
		self.pan_2_id_18["snap_to"] = True
		self.pan_2_id_18["json_id"] = 18
		self.pan_2_id_18["mapping_name"] = "Pan 2"
		self.pan_2_id_18["mapping_type"] = "Pan"
		self.pan_2_id_18["parent_json_id"] = 12
		self.pan_2_id_18["parent_name"] = "track_2_id_12"
		self.mute_2_id_19 = {}
		self.mute_2_id_19["attached_to"] = "midi_cc_ch_1_val_94"
		self.mute_2_id_19["track"] = self.track_num(2)
		self.mute_2_id_19["module"] = "self.song().tracks[self.track_num(1)]"
		self.mute_2_id_19["element"] = "mute"
		self.mute_2_id_19["output_type"] = "bool"
		self.mute_2_id_19["ui_listener"] = "mute"
		self.mute_2_id_19["feedback_brain"] = "feedback_bool"
		self.mute_2_id_19["enc_first"] = 127
		self.mute_2_id_19["enc_second"] = 0
		self.mute_2_id_19["switch_type"] = "toggle"
		self.mute_2_id_19["ctrl_type"] = "on/off"
		self.mute_2_id_19["LED_mapping_type_needs_feedback"] = "1"
		self.mute_2_id_19["LED_feedback"] = "default"
		self.mute_2_id_19["LED_feedback_active"] = "1"
		self.mute_2_id_19["LED_on"] = "127"
		self.mute_2_id_19["LED_off"] = "0"
		self.mute_2_id_19["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_94"]
		self.mute_2_id_19["json_id"] = 19
		self.mute_2_id_19["mapping_name"] = "Mute 2"
		self.mute_2_id_19["mapping_type"] = "Mute"
		self.mute_2_id_19["parent_json_id"] = 12
		self.mute_2_id_19["parent_name"] = "track_2_id_12"
		self.track_3_id_22 = {}
		self.track_3_id_22["track"] = self.track_num(2)
		self.track_3_id_22["module"] = "self.song().tracks[self.track_num(2)]"
		self.track_3_id_22["LED_mapping_type_needs_feedback"] = ""
		self.track_3_id_22["LED_feedback"] = "custom"
		self.track_3_id_22["LED_feedback_active"] = ""
		self.track_3_id_22["LED_on"] = "127"
		self.track_3_id_22["LED_off"] = "0"
		self.track_3_id_22["LED_send_feedback_to_selected"] = []
		self.track_3_id_22["json_id"] = 22
		self.track_3_id_22["mapping_name"] = "Track 3"
		self.track_3_id_22["mapping_type"] = "Track"
		self.track_3_id_22["parent_json_id"] = 1
		self.track_3_id_22["parent_name"] = "mode_1_id_1"
		self.send_1_id_23 = {}
		self.send_1_id_23["attached_to"] = "midi_cc_ch_2_val_83"
		self.send_1_id_23["track"] = self.track_num(2)
		self.send_1_id_23["module"] = "self.song().tracks[self.track_num(2)].mixer_device.sends[0]"
		self.send_1_id_23["element"] = "value"
		self.send_1_id_23["output_type"] = "val"
		self.send_1_id_23["minimum"] = round(0,3)
		self.send_1_id_23["maximum"] = round(100,3)
		self.send_1_id_23["decimal_places"] = 3
		self.send_1_id_23["ui_listener"] = "value"
		self.send_1_id_23["feedback_brain"] = "feedback_range"
		self.send_1_id_23["ctrl_type"] = "absolute"
		self.send_1_id_23["takeover_mode"] = "Value scaling"
		self.send_1_id_23["enc_first"] = 0
		self.send_1_id_23["enc_second"] = 127
		self.send_1_id_23["reverse_mode"] = False
		self.send_1_id_23["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_23["LED_feedback"] = "default"
		self.send_1_id_23["LED_feedback_active"] = "1"
		self.send_1_id_23["LED_on"] = "127"
		self.send_1_id_23["LED_off"] = "0"
		self.send_1_id_23["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_83"]
		self.send_1_id_23["snap_to"] = True
		self.send_1_id_23["json_id"] = 23
		self.send_1_id_23["mapping_name"] = "Send 1"
		self.send_1_id_23["mapping_type"] = "Send"
		self.send_1_id_23["parent_json_id"] = 31
		self.send_1_id_23["parent_name"] = "sends_3_id_31"
		self.send_2_id_24 = {}
		self.send_2_id_24["attached_to"] = "midi_cc_ch_2_val_71"
		self.send_2_id_24["track"] = self.track_num(2)
		self.send_2_id_24["module"] = "self.song().tracks[self.track_num(2)].mixer_device.sends[1]"
		self.send_2_id_24["element"] = "value"
		self.send_2_id_24["output_type"] = "val"
		self.send_2_id_24["minimum"] = round(0,3)
		self.send_2_id_24["maximum"] = round(100,3)
		self.send_2_id_24["decimal_places"] = 3
		self.send_2_id_24["ui_listener"] = "value"
		self.send_2_id_24["feedback_brain"] = "feedback_range"
		self.send_2_id_24["ctrl_type"] = "absolute"
		self.send_2_id_24["takeover_mode"] = "Value scaling"
		self.send_2_id_24["enc_first"] = 0
		self.send_2_id_24["enc_second"] = 127
		self.send_2_id_24["reverse_mode"] = False
		self.send_2_id_24["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_24["LED_feedback"] = "default"
		self.send_2_id_24["LED_feedback_active"] = "1"
		self.send_2_id_24["LED_on"] = "127"
		self.send_2_id_24["LED_off"] = "0"
		self.send_2_id_24["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_71"]
		self.send_2_id_24["snap_to"] = True
		self.send_2_id_24["json_id"] = 24
		self.send_2_id_24["mapping_name"] = "Send 2"
		self.send_2_id_24["mapping_type"] = "Send"
		self.send_2_id_24["parent_json_id"] = 31
		self.send_2_id_24["parent_name"] = "sends_3_id_31"
		self.send_3_id_25 = {}
		self.send_3_id_25["attached_to"] = "midi_cc_ch_2_val_70"
		self.send_3_id_25["track"] = self.track_num(2)
		self.send_3_id_25["module"] = "self.song().tracks[self.track_num(2)].mixer_device.sends[2]"
		self.send_3_id_25["element"] = "value"
		self.send_3_id_25["output_type"] = "val"
		self.send_3_id_25["minimum"] = round(0,3)
		self.send_3_id_25["maximum"] = round(100,3)
		self.send_3_id_25["decimal_places"] = 3
		self.send_3_id_25["ui_listener"] = "value"
		self.send_3_id_25["feedback_brain"] = "feedback_range"
		self.send_3_id_25["ctrl_type"] = "absolute"
		self.send_3_id_25["takeover_mode"] = "Value scaling"
		self.send_3_id_25["enc_first"] = 0
		self.send_3_id_25["enc_second"] = 127
		self.send_3_id_25["reverse_mode"] = False
		self.send_3_id_25["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_25["LED_feedback"] = "default"
		self.send_3_id_25["LED_feedback_active"] = "1"
		self.send_3_id_25["LED_on"] = "127"
		self.send_3_id_25["LED_off"] = "0"
		self.send_3_id_25["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_70"]
		self.send_3_id_25["snap_to"] = True
		self.send_3_id_25["json_id"] = 25
		self.send_3_id_25["mapping_name"] = "Send 3"
		self.send_3_id_25["mapping_type"] = "Send"
		self.send_3_id_25["parent_json_id"] = 31
		self.send_3_id_25["parent_name"] = "sends_3_id_31"
		self.send_4_id_26 = {}
		self.send_4_id_26["attached_to"] = "midi_cc_ch_2_val_10"
		self.send_4_id_26["track"] = self.track_num(2)
		self.send_4_id_26["module"] = "self.song().tracks[self.track_num(2)].mixer_device.sends[3]"
		self.send_4_id_26["element"] = "value"
		self.send_4_id_26["output_type"] = "val"
		self.send_4_id_26["minimum"] = round(0,3)
		self.send_4_id_26["maximum"] = round(100,3)
		self.send_4_id_26["decimal_places"] = 3
		self.send_4_id_26["ui_listener"] = "value"
		self.send_4_id_26["feedback_brain"] = "feedback_range"
		self.send_4_id_26["ctrl_type"] = "absolute"
		self.send_4_id_26["takeover_mode"] = "Value scaling"
		self.send_4_id_26["enc_first"] = 0
		self.send_4_id_26["enc_second"] = 127
		self.send_4_id_26["reverse_mode"] = False
		self.send_4_id_26["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_26["LED_feedback"] = "default"
		self.send_4_id_26["LED_feedback_active"] = "1"
		self.send_4_id_26["LED_on"] = "127"
		self.send_4_id_26["LED_off"] = "0"
		self.send_4_id_26["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_10"]
		self.send_4_id_26["snap_to"] = True
		self.send_4_id_26["json_id"] = 26
		self.send_4_id_26["mapping_name"] = "Send 4"
		self.send_4_id_26["mapping_type"] = "Send"
		self.send_4_id_26["parent_json_id"] = 31
		self.send_4_id_26["parent_name"] = "sends_3_id_31"
		self.volume_3_id_27 = {}
		self.volume_3_id_27["attached_to"] = "midi_cc_ch_2_val_7"
		self.volume_3_id_27["track"] = self.track_num(2)
		self.volume_3_id_27["module"] = "self.song().tracks[self.track_num(2)].mixer_device.volume"
		self.volume_3_id_27["element"] = "value"
		self.volume_3_id_27["output_type"] = "val"
		self.volume_3_id_27["minimum"] = round(0,2)
		self.volume_3_id_27["maximum"] = round(85,2)
		self.volume_3_id_27["decimal_places"] = 2
		self.volume_3_id_27["ui_listener"] = "value"
		self.volume_3_id_27["feedback_brain"] = "feedback_range"
		self.volume_3_id_27["ctrl_type"] = "absolute"
		self.volume_3_id_27["takeover_mode"] = "None"
		self.volume_3_id_27["enc_first"] = 0
		self.volume_3_id_27["enc_second"] = 127
		self.volume_3_id_27["reverse_mode"] = False
		self.volume_3_id_27["LED_mapping_type_needs_feedback"] = "1"
		self.volume_3_id_27["LED_feedback"] = "default"
		self.volume_3_id_27["LED_feedback_active"] = "1"
		self.volume_3_id_27["LED_on"] = "127"
		self.volume_3_id_27["LED_off"] = "0"
		self.volume_3_id_27["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_7"]
		self.volume_3_id_27["snap_to"] = True
		self.volume_3_id_27["json_id"] = 27
		self.volume_3_id_27["mapping_name"] = "Volume 3"
		self.volume_3_id_27["mapping_type"] = "Volume"
		self.volume_3_id_27["parent_json_id"] = 22
		self.volume_3_id_27["parent_name"] = "track_3_id_22"
		self.pan_3_id_28 = {}
		self.pan_3_id_28["attached_to"] = "midi_cc_ch_2_val_82"
		self.pan_3_id_28["track"] = self.track_num(2)
		self.pan_3_id_28["module"] = "self.song().tracks[self.track_num(2)].mixer_device.panning"
		self.pan_3_id_28["element"] = "value"
		self.pan_3_id_28["output_type"] = "val"
		self.pan_3_id_28["minimum"] = round(0,2)
		self.pan_3_id_28["maximum"] = round(100,2)
		self.pan_3_id_28["decimal_places"] = 2
		self.pan_3_id_28["ui_listener"] = "value"
		self.pan_3_id_28["feedback_brain"] = "feedback_range"
		self.pan_3_id_28["ctrl_type"] = "absolute"
		self.pan_3_id_28["takeover_mode"] = "Value scaling"
		self.pan_3_id_28["enc_first"] = 0
		self.pan_3_id_28["enc_second"] = 127
		self.pan_3_id_28["reverse_mode"] = False
		self.pan_3_id_28["LED_mapping_type_needs_feedback"] = "1"
		self.pan_3_id_28["LED_feedback"] = "default"
		self.pan_3_id_28["LED_feedback_active"] = "1"
		self.pan_3_id_28["LED_on"] = "127"
		self.pan_3_id_28["LED_off"] = "0"
		self.pan_3_id_28["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_82"]
		self.pan_3_id_28["snap_to"] = True
		self.pan_3_id_28["json_id"] = 28
		self.pan_3_id_28["mapping_name"] = "Pan 3"
		self.pan_3_id_28["mapping_type"] = "Pan"
		self.pan_3_id_28["parent_json_id"] = 22
		self.pan_3_id_28["parent_name"] = "track_3_id_22"
		self.mute_3_id_29 = {}
		self.mute_3_id_29["attached_to"] = "midi_cc_ch_2_val_94"
		self.mute_3_id_29["track"] = self.track_num(2)
		self.mute_3_id_29["module"] = "self.song().tracks[self.track_num(2)]"
		self.mute_3_id_29["element"] = "mute"
		self.mute_3_id_29["output_type"] = "bool"
		self.mute_3_id_29["ui_listener"] = "mute"
		self.mute_3_id_29["feedback_brain"] = "feedback_bool"
		self.mute_3_id_29["enc_first"] = 127
		self.mute_3_id_29["enc_second"] = 0
		self.mute_3_id_29["switch_type"] = "toggle"
		self.mute_3_id_29["ctrl_type"] = "on/off"
		self.mute_3_id_29["LED_mapping_type_needs_feedback"] = "1"
		self.mute_3_id_29["LED_feedback"] = "default"
		self.mute_3_id_29["LED_feedback_active"] = "1"
		self.mute_3_id_29["LED_on"] = "127"
		self.mute_3_id_29["LED_off"] = "0"
		self.mute_3_id_29["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_94"]
		self.mute_3_id_29["json_id"] = 29
		self.mute_3_id_29["mapping_name"] = "Mute 3"
		self.mute_3_id_29["mapping_type"] = "Mute"
		self.mute_3_id_29["parent_json_id"] = 22
		self.mute_3_id_29["parent_name"] = "track_3_id_22"
		self.track_4_id_32 = {}
		self.track_4_id_32["track"] = self.track_num(2)
		self.track_4_id_32["module"] = "self.song().tracks[self.track_num(3)]"
		self.track_4_id_32["LED_mapping_type_needs_feedback"] = ""
		self.track_4_id_32["LED_feedback"] = "custom"
		self.track_4_id_32["LED_feedback_active"] = ""
		self.track_4_id_32["LED_on"] = "127"
		self.track_4_id_32["LED_off"] = "0"
		self.track_4_id_32["LED_send_feedback_to_selected"] = []
		self.track_4_id_32["json_id"] = 32
		self.track_4_id_32["mapping_name"] = "Track 4"
		self.track_4_id_32["mapping_type"] = "Track"
		self.track_4_id_32["parent_json_id"] = 1
		self.track_4_id_32["parent_name"] = "mode_1_id_1"
		self.send_1_id_33 = {}
		self.send_1_id_33["attached_to"] = "midi_cc_ch_3_val_83"
		self.send_1_id_33["track"] = self.track_num(2)
		self.send_1_id_33["module"] = "self.song().tracks[self.track_num(3)].mixer_device.sends[0]"
		self.send_1_id_33["element"] = "value"
		self.send_1_id_33["output_type"] = "val"
		self.send_1_id_33["minimum"] = round(0,3)
		self.send_1_id_33["maximum"] = round(100,3)
		self.send_1_id_33["decimal_places"] = 3
		self.send_1_id_33["ui_listener"] = "value"
		self.send_1_id_33["feedback_brain"] = "feedback_range"
		self.send_1_id_33["ctrl_type"] = "absolute"
		self.send_1_id_33["takeover_mode"] = "Value scaling"
		self.send_1_id_33["enc_first"] = 0
		self.send_1_id_33["enc_second"] = 127
		self.send_1_id_33["reverse_mode"] = False
		self.send_1_id_33["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_33["LED_feedback"] = "default"
		self.send_1_id_33["LED_feedback_active"] = "1"
		self.send_1_id_33["LED_on"] = "127"
		self.send_1_id_33["LED_off"] = "0"
		self.send_1_id_33["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_83"]
		self.send_1_id_33["snap_to"] = True
		self.send_1_id_33["json_id"] = 33
		self.send_1_id_33["mapping_name"] = "Send 1"
		self.send_1_id_33["mapping_type"] = "Send"
		self.send_1_id_33["parent_json_id"] = 41
		self.send_1_id_33["parent_name"] = "sends_4_id_41"
		self.send_2_id_34 = {}
		self.send_2_id_34["attached_to"] = "midi_cc_ch_3_val_71"
		self.send_2_id_34["track"] = self.track_num(2)
		self.send_2_id_34["module"] = "self.song().tracks[self.track_num(3)].mixer_device.sends[1]"
		self.send_2_id_34["element"] = "value"
		self.send_2_id_34["output_type"] = "val"
		self.send_2_id_34["minimum"] = round(0,3)
		self.send_2_id_34["maximum"] = round(100,3)
		self.send_2_id_34["decimal_places"] = 3
		self.send_2_id_34["ui_listener"] = "value"
		self.send_2_id_34["feedback_brain"] = "feedback_range"
		self.send_2_id_34["ctrl_type"] = "absolute"
		self.send_2_id_34["takeover_mode"] = "Value scaling"
		self.send_2_id_34["enc_first"] = 0
		self.send_2_id_34["enc_second"] = 127
		self.send_2_id_34["reverse_mode"] = False
		self.send_2_id_34["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_34["LED_feedback"] = "default"
		self.send_2_id_34["LED_feedback_active"] = "1"
		self.send_2_id_34["LED_on"] = "127"
		self.send_2_id_34["LED_off"] = "0"
		self.send_2_id_34["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_71"]
		self.send_2_id_34["snap_to"] = True
		self.send_2_id_34["json_id"] = 34
		self.send_2_id_34["mapping_name"] = "Send 2"
		self.send_2_id_34["mapping_type"] = "Send"
		self.send_2_id_34["parent_json_id"] = 41
		self.send_2_id_34["parent_name"] = "sends_4_id_41"
		self.send_3_id_35 = {}
		self.send_3_id_35["attached_to"] = "midi_cc_ch_3_val_70"
		self.send_3_id_35["track"] = self.track_num(2)
		self.send_3_id_35["module"] = "self.song().tracks[self.track_num(3)].mixer_device.sends[2]"
		self.send_3_id_35["element"] = "value"
		self.send_3_id_35["output_type"] = "val"
		self.send_3_id_35["minimum"] = round(0,3)
		self.send_3_id_35["maximum"] = round(100,3)
		self.send_3_id_35["decimal_places"] = 3
		self.send_3_id_35["ui_listener"] = "value"
		self.send_3_id_35["feedback_brain"] = "feedback_range"
		self.send_3_id_35["ctrl_type"] = "absolute"
		self.send_3_id_35["takeover_mode"] = "Value scaling"
		self.send_3_id_35["enc_first"] = 0
		self.send_3_id_35["enc_second"] = 127
		self.send_3_id_35["reverse_mode"] = False
		self.send_3_id_35["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_35["LED_feedback"] = "default"
		self.send_3_id_35["LED_feedback_active"] = "1"
		self.send_3_id_35["LED_on"] = "127"
		self.send_3_id_35["LED_off"] = "0"
		self.send_3_id_35["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_70"]
		self.send_3_id_35["snap_to"] = True
		self.send_3_id_35["json_id"] = 35
		self.send_3_id_35["mapping_name"] = "Send 3"
		self.send_3_id_35["mapping_type"] = "Send"
		self.send_3_id_35["parent_json_id"] = 41
		self.send_3_id_35["parent_name"] = "sends_4_id_41"
		self.send_4_id_36 = {}
		self.send_4_id_36["attached_to"] = "midi_cc_ch_3_val_10"
		self.send_4_id_36["track"] = self.track_num(2)
		self.send_4_id_36["module"] = "self.song().tracks[self.track_num(3)].mixer_device.sends[3]"
		self.send_4_id_36["element"] = "value"
		self.send_4_id_36["output_type"] = "val"
		self.send_4_id_36["minimum"] = round(0,3)
		self.send_4_id_36["maximum"] = round(100,3)
		self.send_4_id_36["decimal_places"] = 3
		self.send_4_id_36["ui_listener"] = "value"
		self.send_4_id_36["feedback_brain"] = "feedback_range"
		self.send_4_id_36["ctrl_type"] = "absolute"
		self.send_4_id_36["takeover_mode"] = "Value scaling"
		self.send_4_id_36["enc_first"] = 0
		self.send_4_id_36["enc_second"] = 127
		self.send_4_id_36["reverse_mode"] = False
		self.send_4_id_36["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_36["LED_feedback"] = "default"
		self.send_4_id_36["LED_feedback_active"] = "1"
		self.send_4_id_36["LED_on"] = "127"
		self.send_4_id_36["LED_off"] = "0"
		self.send_4_id_36["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_10"]
		self.send_4_id_36["snap_to"] = True
		self.send_4_id_36["json_id"] = 36
		self.send_4_id_36["mapping_name"] = "Send 4"
		self.send_4_id_36["mapping_type"] = "Send"
		self.send_4_id_36["parent_json_id"] = 41
		self.send_4_id_36["parent_name"] = "sends_4_id_41"
		self.volume_4_id_37 = {}
		self.volume_4_id_37["attached_to"] = "midi_cc_ch_3_val_7"
		self.volume_4_id_37["track"] = self.track_num(2)
		self.volume_4_id_37["module"] = "self.song().tracks[self.track_num(3)].mixer_device.volume"
		self.volume_4_id_37["element"] = "value"
		self.volume_4_id_37["output_type"] = "val"
		self.volume_4_id_37["minimum"] = round(0,2)
		self.volume_4_id_37["maximum"] = round(85,2)
		self.volume_4_id_37["decimal_places"] = 2
		self.volume_4_id_37["ui_listener"] = "value"
		self.volume_4_id_37["feedback_brain"] = "feedback_range"
		self.volume_4_id_37["ctrl_type"] = "absolute"
		self.volume_4_id_37["takeover_mode"] = "None"
		self.volume_4_id_37["enc_first"] = 0
		self.volume_4_id_37["enc_second"] = 127
		self.volume_4_id_37["reverse_mode"] = False
		self.volume_4_id_37["LED_mapping_type_needs_feedback"] = "1"
		self.volume_4_id_37["LED_feedback"] = "default"
		self.volume_4_id_37["LED_feedback_active"] = "1"
		self.volume_4_id_37["LED_on"] = "127"
		self.volume_4_id_37["LED_off"] = "0"
		self.volume_4_id_37["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_7"]
		self.volume_4_id_37["snap_to"] = True
		self.volume_4_id_37["json_id"] = 37
		self.volume_4_id_37["mapping_name"] = "Volume 4"
		self.volume_4_id_37["mapping_type"] = "Volume"
		self.volume_4_id_37["parent_json_id"] = 32
		self.volume_4_id_37["parent_name"] = "track_4_id_32"
		self.pan_4_id_38 = {}
		self.pan_4_id_38["attached_to"] = "midi_cc_ch_3_val_82"
		self.pan_4_id_38["track"] = self.track_num(2)
		self.pan_4_id_38["module"] = "self.song().tracks[self.track_num(3)].mixer_device.panning"
		self.pan_4_id_38["element"] = "value"
		self.pan_4_id_38["output_type"] = "val"
		self.pan_4_id_38["minimum"] = round(0,2)
		self.pan_4_id_38["maximum"] = round(100,2)
		self.pan_4_id_38["decimal_places"] = 2
		self.pan_4_id_38["ui_listener"] = "value"
		self.pan_4_id_38["feedback_brain"] = "feedback_range"
		self.pan_4_id_38["ctrl_type"] = "absolute"
		self.pan_4_id_38["takeover_mode"] = "Value scaling"
		self.pan_4_id_38["enc_first"] = 0
		self.pan_4_id_38["enc_second"] = 127
		self.pan_4_id_38["reverse_mode"] = False
		self.pan_4_id_38["LED_mapping_type_needs_feedback"] = "1"
		self.pan_4_id_38["LED_feedback"] = "default"
		self.pan_4_id_38["LED_feedback_active"] = "1"
		self.pan_4_id_38["LED_on"] = "127"
		self.pan_4_id_38["LED_off"] = "0"
		self.pan_4_id_38["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_82"]
		self.pan_4_id_38["snap_to"] = True
		self.pan_4_id_38["json_id"] = 38
		self.pan_4_id_38["mapping_name"] = "Pan 4"
		self.pan_4_id_38["mapping_type"] = "Pan"
		self.pan_4_id_38["parent_json_id"] = 32
		self.pan_4_id_38["parent_name"] = "track_4_id_32"
		self.mute_4_id_39 = {}
		self.mute_4_id_39["attached_to"] = "midi_cc_ch_3_val_94"
		self.mute_4_id_39["track"] = self.track_num(2)
		self.mute_4_id_39["module"] = "self.song().tracks[self.track_num(3)]"
		self.mute_4_id_39["element"] = "mute"
		self.mute_4_id_39["output_type"] = "bool"
		self.mute_4_id_39["ui_listener"] = "mute"
		self.mute_4_id_39["feedback_brain"] = "feedback_bool"
		self.mute_4_id_39["enc_first"] = 127
		self.mute_4_id_39["enc_second"] = 0
		self.mute_4_id_39["switch_type"] = "toggle"
		self.mute_4_id_39["ctrl_type"] = "on/off"
		self.mute_4_id_39["LED_mapping_type_needs_feedback"] = "1"
		self.mute_4_id_39["LED_feedback"] = "default"
		self.mute_4_id_39["LED_feedback_active"] = "1"
		self.mute_4_id_39["LED_on"] = "127"
		self.mute_4_id_39["LED_off"] = "0"
		self.mute_4_id_39["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_94"]
		self.mute_4_id_39["json_id"] = 39
		self.mute_4_id_39["mapping_name"] = "Mute 4"
		self.mute_4_id_39["mapping_type"] = "Mute"
		self.mute_4_id_39["parent_json_id"] = 32
		self.mute_4_id_39["parent_name"] = "track_4_id_32"
		self.track_5_id_42 = {}
		self.track_5_id_42["track"] = self.track_num(2)
		self.track_5_id_42["module"] = "self.song().tracks[self.track_num(4)]"
		self.track_5_id_42["LED_mapping_type_needs_feedback"] = ""
		self.track_5_id_42["LED_feedback"] = "custom"
		self.track_5_id_42["LED_feedback_active"] = ""
		self.track_5_id_42["LED_on"] = "127"
		self.track_5_id_42["LED_off"] = "0"
		self.track_5_id_42["LED_send_feedback_to_selected"] = []
		self.track_5_id_42["json_id"] = 42
		self.track_5_id_42["mapping_name"] = "Track 5"
		self.track_5_id_42["mapping_type"] = "Track"
		self.track_5_id_42["parent_json_id"] = 1
		self.track_5_id_42["parent_name"] = "mode_1_id_1"
		self.send_1_id_43 = {}
		self.send_1_id_43["attached_to"] = "midi_cc_ch_4_val_83"
		self.send_1_id_43["track"] = self.track_num(2)
		self.send_1_id_43["module"] = "self.song().tracks[self.track_num(4)].mixer_device.sends[0]"
		self.send_1_id_43["element"] = "value"
		self.send_1_id_43["output_type"] = "val"
		self.send_1_id_43["minimum"] = round(0,3)
		self.send_1_id_43["maximum"] = round(100,3)
		self.send_1_id_43["decimal_places"] = 3
		self.send_1_id_43["ui_listener"] = "value"
		self.send_1_id_43["feedback_brain"] = "feedback_range"
		self.send_1_id_43["ctrl_type"] = "absolute"
		self.send_1_id_43["takeover_mode"] = "Value scaling"
		self.send_1_id_43["enc_first"] = 0
		self.send_1_id_43["enc_second"] = 127
		self.send_1_id_43["reverse_mode"] = False
		self.send_1_id_43["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_43["LED_feedback"] = "default"
		self.send_1_id_43["LED_feedback_active"] = "1"
		self.send_1_id_43["LED_on"] = "127"
		self.send_1_id_43["LED_off"] = "0"
		self.send_1_id_43["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_83"]
		self.send_1_id_43["snap_to"] = True
		self.send_1_id_43["json_id"] = 43
		self.send_1_id_43["mapping_name"] = "Send 1"
		self.send_1_id_43["mapping_type"] = "Send"
		self.send_1_id_43["parent_json_id"] = 51
		self.send_1_id_43["parent_name"] = "sends_5_id_51"
		self.send_2_id_44 = {}
		self.send_2_id_44["attached_to"] = "midi_cc_ch_4_val_71"
		self.send_2_id_44["track"] = self.track_num(2)
		self.send_2_id_44["module"] = "self.song().tracks[self.track_num(4)].mixer_device.sends[1]"
		self.send_2_id_44["element"] = "value"
		self.send_2_id_44["output_type"] = "val"
		self.send_2_id_44["minimum"] = round(0,3)
		self.send_2_id_44["maximum"] = round(100,3)
		self.send_2_id_44["decimal_places"] = 3
		self.send_2_id_44["ui_listener"] = "value"
		self.send_2_id_44["feedback_brain"] = "feedback_range"
		self.send_2_id_44["ctrl_type"] = "absolute"
		self.send_2_id_44["takeover_mode"] = "Value scaling"
		self.send_2_id_44["enc_first"] = 0
		self.send_2_id_44["enc_second"] = 127
		self.send_2_id_44["reverse_mode"] = False
		self.send_2_id_44["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_44["LED_feedback"] = "default"
		self.send_2_id_44["LED_feedback_active"] = "1"
		self.send_2_id_44["LED_on"] = "127"
		self.send_2_id_44["LED_off"] = "0"
		self.send_2_id_44["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_71"]
		self.send_2_id_44["snap_to"] = True
		self.send_2_id_44["json_id"] = 44
		self.send_2_id_44["mapping_name"] = "Send 2"
		self.send_2_id_44["mapping_type"] = "Send"
		self.send_2_id_44["parent_json_id"] = 51
		self.send_2_id_44["parent_name"] = "sends_5_id_51"
		self.send_3_id_45 = {}
		self.send_3_id_45["attached_to"] = "midi_cc_ch_4_val_70"
		self.send_3_id_45["track"] = self.track_num(2)
		self.send_3_id_45["module"] = "self.song().tracks[self.track_num(4)].mixer_device.sends[2]"
		self.send_3_id_45["element"] = "value"
		self.send_3_id_45["output_type"] = "val"
		self.send_3_id_45["minimum"] = round(0,3)
		self.send_3_id_45["maximum"] = round(100,3)
		self.send_3_id_45["decimal_places"] = 3
		self.send_3_id_45["ui_listener"] = "value"
		self.send_3_id_45["feedback_brain"] = "feedback_range"
		self.send_3_id_45["ctrl_type"] = "absolute"
		self.send_3_id_45["takeover_mode"] = "Value scaling"
		self.send_3_id_45["enc_first"] = 0
		self.send_3_id_45["enc_second"] = 127
		self.send_3_id_45["reverse_mode"] = False
		self.send_3_id_45["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_45["LED_feedback"] = "default"
		self.send_3_id_45["LED_feedback_active"] = "1"
		self.send_3_id_45["LED_on"] = "127"
		self.send_3_id_45["LED_off"] = "0"
		self.send_3_id_45["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_70"]
		self.send_3_id_45["snap_to"] = True
		self.send_3_id_45["json_id"] = 45
		self.send_3_id_45["mapping_name"] = "Send 3"
		self.send_3_id_45["mapping_type"] = "Send"
		self.send_3_id_45["parent_json_id"] = 51
		self.send_3_id_45["parent_name"] = "sends_5_id_51"
		self.send_4_id_46 = {}
		self.send_4_id_46["attached_to"] = "midi_cc_ch_4_val_10"
		self.send_4_id_46["track"] = self.track_num(2)
		self.send_4_id_46["module"] = "self.song().tracks[self.track_num(4)].mixer_device.sends[3]"
		self.send_4_id_46["element"] = "value"
		self.send_4_id_46["output_type"] = "val"
		self.send_4_id_46["minimum"] = round(0,3)
		self.send_4_id_46["maximum"] = round(100,3)
		self.send_4_id_46["decimal_places"] = 3
		self.send_4_id_46["ui_listener"] = "value"
		self.send_4_id_46["feedback_brain"] = "feedback_range"
		self.send_4_id_46["ctrl_type"] = "absolute"
		self.send_4_id_46["takeover_mode"] = "Value scaling"
		self.send_4_id_46["enc_first"] = 0
		self.send_4_id_46["enc_second"] = 127
		self.send_4_id_46["reverse_mode"] = False
		self.send_4_id_46["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_46["LED_feedback"] = "default"
		self.send_4_id_46["LED_feedback_active"] = "1"
		self.send_4_id_46["LED_on"] = "127"
		self.send_4_id_46["LED_off"] = "0"
		self.send_4_id_46["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_10"]
		self.send_4_id_46["snap_to"] = True
		self.send_4_id_46["json_id"] = 46
		self.send_4_id_46["mapping_name"] = "Send 4"
		self.send_4_id_46["mapping_type"] = "Send"
		self.send_4_id_46["parent_json_id"] = 51
		self.send_4_id_46["parent_name"] = "sends_5_id_51"
		self.volume_5_id_47 = {}
		self.volume_5_id_47["attached_to"] = "midi_cc_ch_4_val_7"
		self.volume_5_id_47["track"] = self.track_num(2)
		self.volume_5_id_47["module"] = "self.song().tracks[self.track_num(4)].mixer_device.volume"
		self.volume_5_id_47["element"] = "value"
		self.volume_5_id_47["output_type"] = "val"
		self.volume_5_id_47["minimum"] = round(0,2)
		self.volume_5_id_47["maximum"] = round(85,2)
		self.volume_5_id_47["decimal_places"] = 2
		self.volume_5_id_47["ui_listener"] = "value"
		self.volume_5_id_47["feedback_brain"] = "feedback_range"
		self.volume_5_id_47["ctrl_type"] = "absolute"
		self.volume_5_id_47["takeover_mode"] = "None"
		self.volume_5_id_47["enc_first"] = 0
		self.volume_5_id_47["enc_second"] = 127
		self.volume_5_id_47["reverse_mode"] = False
		self.volume_5_id_47["LED_mapping_type_needs_feedback"] = "1"
		self.volume_5_id_47["LED_feedback"] = "default"
		self.volume_5_id_47["LED_feedback_active"] = "1"
		self.volume_5_id_47["LED_on"] = "127"
		self.volume_5_id_47["LED_off"] = "0"
		self.volume_5_id_47["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_7"]
		self.volume_5_id_47["snap_to"] = True
		self.volume_5_id_47["json_id"] = 47
		self.volume_5_id_47["mapping_name"] = "Volume 5"
		self.volume_5_id_47["mapping_type"] = "Volume"
		self.volume_5_id_47["parent_json_id"] = 42
		self.volume_5_id_47["parent_name"] = "track_5_id_42"
		self.pan_5_id_48 = {}
		self.pan_5_id_48["attached_to"] = "midi_cc_ch_4_val_82"
		self.pan_5_id_48["track"] = self.track_num(2)
		self.pan_5_id_48["module"] = "self.song().tracks[self.track_num(4)].mixer_device.panning"
		self.pan_5_id_48["element"] = "value"
		self.pan_5_id_48["output_type"] = "val"
		self.pan_5_id_48["minimum"] = round(0,2)
		self.pan_5_id_48["maximum"] = round(100,2)
		self.pan_5_id_48["decimal_places"] = 2
		self.pan_5_id_48["ui_listener"] = "value"
		self.pan_5_id_48["feedback_brain"] = "feedback_range"
		self.pan_5_id_48["ctrl_type"] = "absolute"
		self.pan_5_id_48["takeover_mode"] = "Value scaling"
		self.pan_5_id_48["enc_first"] = 0
		self.pan_5_id_48["enc_second"] = 127
		self.pan_5_id_48["reverse_mode"] = False
		self.pan_5_id_48["LED_mapping_type_needs_feedback"] = "1"
		self.pan_5_id_48["LED_feedback"] = "default"
		self.pan_5_id_48["LED_feedback_active"] = "1"
		self.pan_5_id_48["LED_on"] = "127"
		self.pan_5_id_48["LED_off"] = "0"
		self.pan_5_id_48["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_82"]
		self.pan_5_id_48["snap_to"] = True
		self.pan_5_id_48["json_id"] = 48
		self.pan_5_id_48["mapping_name"] = "Pan 5"
		self.pan_5_id_48["mapping_type"] = "Pan"
		self.pan_5_id_48["parent_json_id"] = 42
		self.pan_5_id_48["parent_name"] = "track_5_id_42"
		self.mute_5_id_49 = {}
		self.mute_5_id_49["attached_to"] = "midi_cc_ch_4_val_94"
		self.mute_5_id_49["track"] = self.track_num(2)
		self.mute_5_id_49["module"] = "self.song().tracks[self.track_num(4)]"
		self.mute_5_id_49["element"] = "mute"
		self.mute_5_id_49["output_type"] = "bool"
		self.mute_5_id_49["ui_listener"] = "mute"
		self.mute_5_id_49["feedback_brain"] = "feedback_bool"
		self.mute_5_id_49["enc_first"] = 127
		self.mute_5_id_49["enc_second"] = 0
		self.mute_5_id_49["switch_type"] = "toggle"
		self.mute_5_id_49["ctrl_type"] = "on/off"
		self.mute_5_id_49["LED_mapping_type_needs_feedback"] = "1"
		self.mute_5_id_49["LED_feedback"] = "default"
		self.mute_5_id_49["LED_feedback_active"] = "1"
		self.mute_5_id_49["LED_on"] = "127"
		self.mute_5_id_49["LED_off"] = "0"
		self.mute_5_id_49["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_94"]
		self.mute_5_id_49["json_id"] = 49
		self.mute_5_id_49["mapping_name"] = "Mute 5"
		self.mute_5_id_49["mapping_type"] = "Mute"
		self.mute_5_id_49["parent_json_id"] = 42
		self.mute_5_id_49["parent_name"] = "track_5_id_42"
		self.track_6_id_52 = {}
		self.track_6_id_52["track"] = self.track_num(2)
		self.track_6_id_52["module"] = "self.song().tracks[self.track_num(5)]"
		self.track_6_id_52["LED_mapping_type_needs_feedback"] = ""
		self.track_6_id_52["LED_feedback"] = "custom"
		self.track_6_id_52["LED_feedback_active"] = ""
		self.track_6_id_52["LED_on"] = "127"
		self.track_6_id_52["LED_off"] = "0"
		self.track_6_id_52["LED_send_feedback_to_selected"] = []
		self.track_6_id_52["json_id"] = 52
		self.track_6_id_52["mapping_name"] = "Track 6"
		self.track_6_id_52["mapping_type"] = "Track"
		self.track_6_id_52["parent_json_id"] = 1
		self.track_6_id_52["parent_name"] = "mode_1_id_1"
		self.send_1_id_53 = {}
		self.send_1_id_53["attached_to"] = "midi_cc_ch_5_val_83"
		self.send_1_id_53["track"] = self.track_num(2)
		self.send_1_id_53["module"] = "self.song().tracks[self.track_num(5)].mixer_device.sends[0]"
		self.send_1_id_53["element"] = "value"
		self.send_1_id_53["output_type"] = "val"
		self.send_1_id_53["minimum"] = round(0,3)
		self.send_1_id_53["maximum"] = round(100,3)
		self.send_1_id_53["decimal_places"] = 3
		self.send_1_id_53["ui_listener"] = "value"
		self.send_1_id_53["feedback_brain"] = "feedback_range"
		self.send_1_id_53["ctrl_type"] = "absolute"
		self.send_1_id_53["takeover_mode"] = "Value scaling"
		self.send_1_id_53["enc_first"] = 0
		self.send_1_id_53["enc_second"] = 127
		self.send_1_id_53["reverse_mode"] = False
		self.send_1_id_53["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_53["LED_feedback"] = "default"
		self.send_1_id_53["LED_feedback_active"] = "1"
		self.send_1_id_53["LED_on"] = "127"
		self.send_1_id_53["LED_off"] = "0"
		self.send_1_id_53["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_83"]
		self.send_1_id_53["snap_to"] = True
		self.send_1_id_53["json_id"] = 53
		self.send_1_id_53["mapping_name"] = "Send 1"
		self.send_1_id_53["mapping_type"] = "Send"
		self.send_1_id_53["parent_json_id"] = 61
		self.send_1_id_53["parent_name"] = "sends_6_id_61"
		self.send_2_id_54 = {}
		self.send_2_id_54["attached_to"] = "midi_cc_ch_5_val_71"
		self.send_2_id_54["track"] = self.track_num(2)
		self.send_2_id_54["module"] = "self.song().tracks[self.track_num(5)].mixer_device.sends[1]"
		self.send_2_id_54["element"] = "value"
		self.send_2_id_54["output_type"] = "val"
		self.send_2_id_54["minimum"] = round(0,3)
		self.send_2_id_54["maximum"] = round(100,3)
		self.send_2_id_54["decimal_places"] = 3
		self.send_2_id_54["ui_listener"] = "value"
		self.send_2_id_54["feedback_brain"] = "feedback_range"
		self.send_2_id_54["ctrl_type"] = "absolute"
		self.send_2_id_54["takeover_mode"] = "Value scaling"
		self.send_2_id_54["enc_first"] = 0
		self.send_2_id_54["enc_second"] = 127
		self.send_2_id_54["reverse_mode"] = False
		self.send_2_id_54["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_54["LED_feedback"] = "default"
		self.send_2_id_54["LED_feedback_active"] = "1"
		self.send_2_id_54["LED_on"] = "127"
		self.send_2_id_54["LED_off"] = "0"
		self.send_2_id_54["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_71"]
		self.send_2_id_54["snap_to"] = True
		self.send_2_id_54["json_id"] = 54
		self.send_2_id_54["mapping_name"] = "Send 2"
		self.send_2_id_54["mapping_type"] = "Send"
		self.send_2_id_54["parent_json_id"] = 61
		self.send_2_id_54["parent_name"] = "sends_6_id_61"
		self.send_3_id_55 = {}
		self.send_3_id_55["attached_to"] = "midi_cc_ch_5_val_70"
		self.send_3_id_55["track"] = self.track_num(2)
		self.send_3_id_55["module"] = "self.song().tracks[self.track_num(5)].mixer_device.sends[2]"
		self.send_3_id_55["element"] = "value"
		self.send_3_id_55["output_type"] = "val"
		self.send_3_id_55["minimum"] = round(0,3)
		self.send_3_id_55["maximum"] = round(100,3)
		self.send_3_id_55["decimal_places"] = 3
		self.send_3_id_55["ui_listener"] = "value"
		self.send_3_id_55["feedback_brain"] = "feedback_range"
		self.send_3_id_55["ctrl_type"] = "absolute"
		self.send_3_id_55["takeover_mode"] = "Value scaling"
		self.send_3_id_55["enc_first"] = 0
		self.send_3_id_55["enc_second"] = 127
		self.send_3_id_55["reverse_mode"] = False
		self.send_3_id_55["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_55["LED_feedback"] = "default"
		self.send_3_id_55["LED_feedback_active"] = "1"
		self.send_3_id_55["LED_on"] = "127"
		self.send_3_id_55["LED_off"] = "0"
		self.send_3_id_55["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_70"]
		self.send_3_id_55["snap_to"] = True
		self.send_3_id_55["json_id"] = 55
		self.send_3_id_55["mapping_name"] = "Send 3"
		self.send_3_id_55["mapping_type"] = "Send"
		self.send_3_id_55["parent_json_id"] = 61
		self.send_3_id_55["parent_name"] = "sends_6_id_61"
		self.send_4_id_56 = {}
		self.send_4_id_56["attached_to"] = "midi_cc_ch_5_val_10"
		self.send_4_id_56["track"] = self.track_num(2)
		self.send_4_id_56["module"] = "self.song().tracks[self.track_num(5)].mixer_device.sends[3]"
		self.send_4_id_56["element"] = "value"
		self.send_4_id_56["output_type"] = "val"
		self.send_4_id_56["minimum"] = round(0,3)
		self.send_4_id_56["maximum"] = round(100,3)
		self.send_4_id_56["decimal_places"] = 3
		self.send_4_id_56["ui_listener"] = "value"
		self.send_4_id_56["feedback_brain"] = "feedback_range"
		self.send_4_id_56["ctrl_type"] = "absolute"
		self.send_4_id_56["takeover_mode"] = "Value scaling"
		self.send_4_id_56["enc_first"] = 0
		self.send_4_id_56["enc_second"] = 127
		self.send_4_id_56["reverse_mode"] = False
		self.send_4_id_56["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_56["LED_feedback"] = "default"
		self.send_4_id_56["LED_feedback_active"] = "1"
		self.send_4_id_56["LED_on"] = "127"
		self.send_4_id_56["LED_off"] = "0"
		self.send_4_id_56["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_10"]
		self.send_4_id_56["snap_to"] = True
		self.send_4_id_56["json_id"] = 56
		self.send_4_id_56["mapping_name"] = "Send 4"
		self.send_4_id_56["mapping_type"] = "Send"
		self.send_4_id_56["parent_json_id"] = 61
		self.send_4_id_56["parent_name"] = "sends_6_id_61"
		self.volume_6_id_57 = {}
		self.volume_6_id_57["attached_to"] = "midi_cc_ch_5_val_7"
		self.volume_6_id_57["track"] = self.track_num(2)
		self.volume_6_id_57["module"] = "self.song().tracks[self.track_num(5)].mixer_device.volume"
		self.volume_6_id_57["element"] = "value"
		self.volume_6_id_57["output_type"] = "val"
		self.volume_6_id_57["minimum"] = round(0,2)
		self.volume_6_id_57["maximum"] = round(85,2)
		self.volume_6_id_57["decimal_places"] = 2
		self.volume_6_id_57["ui_listener"] = "value"
		self.volume_6_id_57["feedback_brain"] = "feedback_range"
		self.volume_6_id_57["ctrl_type"] = "absolute"
		self.volume_6_id_57["takeover_mode"] = "None"
		self.volume_6_id_57["enc_first"] = 0
		self.volume_6_id_57["enc_second"] = 127
		self.volume_6_id_57["reverse_mode"] = False
		self.volume_6_id_57["LED_mapping_type_needs_feedback"] = "1"
		self.volume_6_id_57["LED_feedback"] = "default"
		self.volume_6_id_57["LED_feedback_active"] = "1"
		self.volume_6_id_57["LED_on"] = "127"
		self.volume_6_id_57["LED_off"] = "0"
		self.volume_6_id_57["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_7"]
		self.volume_6_id_57["snap_to"] = True
		self.volume_6_id_57["json_id"] = 57
		self.volume_6_id_57["mapping_name"] = "Volume 6"
		self.volume_6_id_57["mapping_type"] = "Volume"
		self.volume_6_id_57["parent_json_id"] = 52
		self.volume_6_id_57["parent_name"] = "track_6_id_52"
		self.pan_6_id_58 = {}
		self.pan_6_id_58["attached_to"] = "midi_cc_ch_5_val_82"
		self.pan_6_id_58["track"] = self.track_num(2)
		self.pan_6_id_58["module"] = "self.song().tracks[self.track_num(5)].mixer_device.panning"
		self.pan_6_id_58["element"] = "value"
		self.pan_6_id_58["output_type"] = "val"
		self.pan_6_id_58["minimum"] = round(0,2)
		self.pan_6_id_58["maximum"] = round(100,2)
		self.pan_6_id_58["decimal_places"] = 2
		self.pan_6_id_58["ui_listener"] = "value"
		self.pan_6_id_58["feedback_brain"] = "feedback_range"
		self.pan_6_id_58["ctrl_type"] = "absolute"
		self.pan_6_id_58["takeover_mode"] = "Value scaling"
		self.pan_6_id_58["enc_first"] = 0
		self.pan_6_id_58["enc_second"] = 127
		self.pan_6_id_58["reverse_mode"] = False
		self.pan_6_id_58["LED_mapping_type_needs_feedback"] = "1"
		self.pan_6_id_58["LED_feedback"] = "default"
		self.pan_6_id_58["LED_feedback_active"] = "1"
		self.pan_6_id_58["LED_on"] = "127"
		self.pan_6_id_58["LED_off"] = "0"
		self.pan_6_id_58["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_82"]
		self.pan_6_id_58["snap_to"] = True
		self.pan_6_id_58["json_id"] = 58
		self.pan_6_id_58["mapping_name"] = "Pan 6"
		self.pan_6_id_58["mapping_type"] = "Pan"
		self.pan_6_id_58["parent_json_id"] = 52
		self.pan_6_id_58["parent_name"] = "track_6_id_52"
		self.mute_6_id_59 = {}
		self.mute_6_id_59["attached_to"] = "midi_cc_ch_5_val_94"
		self.mute_6_id_59["track"] = self.track_num(2)
		self.mute_6_id_59["module"] = "self.song().tracks[self.track_num(5)]"
		self.mute_6_id_59["element"] = "mute"
		self.mute_6_id_59["output_type"] = "bool"
		self.mute_6_id_59["ui_listener"] = "mute"
		self.mute_6_id_59["feedback_brain"] = "feedback_bool"
		self.mute_6_id_59["enc_first"] = 127
		self.mute_6_id_59["enc_second"] = 0
		self.mute_6_id_59["switch_type"] = "toggle"
		self.mute_6_id_59["ctrl_type"] = "on/off"
		self.mute_6_id_59["LED_mapping_type_needs_feedback"] = "1"
		self.mute_6_id_59["LED_feedback"] = "default"
		self.mute_6_id_59["LED_feedback_active"] = "1"
		self.mute_6_id_59["LED_on"] = "127"
		self.mute_6_id_59["LED_off"] = "0"
		self.mute_6_id_59["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_94"]
		self.mute_6_id_59["json_id"] = 59
		self.mute_6_id_59["mapping_name"] = "Mute 6"
		self.mute_6_id_59["mapping_type"] = "Mute"
		self.mute_6_id_59["parent_json_id"] = 52
		self.mute_6_id_59["parent_name"] = "track_6_id_52"
		self.track_7_id_62 = {}
		self.track_7_id_62["track"] = self.track_num(2)
		self.track_7_id_62["module"] = "self.song().tracks[self.track_num(6)]"
		self.track_7_id_62["LED_mapping_type_needs_feedback"] = ""
		self.track_7_id_62["LED_feedback"] = "custom"
		self.track_7_id_62["LED_feedback_active"] = ""
		self.track_7_id_62["LED_on"] = "127"
		self.track_7_id_62["LED_off"] = "0"
		self.track_7_id_62["LED_send_feedback_to_selected"] = []
		self.track_7_id_62["json_id"] = 62
		self.track_7_id_62["mapping_name"] = "Track 7"
		self.track_7_id_62["mapping_type"] = "Track"
		self.track_7_id_62["parent_json_id"] = 1
		self.track_7_id_62["parent_name"] = "mode_1_id_1"
		self.send_1_id_63 = {}
		self.send_1_id_63["attached_to"] = "midi_cc_ch_6_val_83"
		self.send_1_id_63["track"] = self.track_num(2)
		self.send_1_id_63["module"] = "self.song().tracks[self.track_num(6)].mixer_device.sends[0]"
		self.send_1_id_63["element"] = "value"
		self.send_1_id_63["output_type"] = "val"
		self.send_1_id_63["minimum"] = round(0,3)
		self.send_1_id_63["maximum"] = round(100,3)
		self.send_1_id_63["decimal_places"] = 3
		self.send_1_id_63["ui_listener"] = "value"
		self.send_1_id_63["feedback_brain"] = "feedback_range"
		self.send_1_id_63["ctrl_type"] = "absolute"
		self.send_1_id_63["takeover_mode"] = "Value scaling"
		self.send_1_id_63["enc_first"] = 0
		self.send_1_id_63["enc_second"] = 127
		self.send_1_id_63["reverse_mode"] = False
		self.send_1_id_63["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_63["LED_feedback"] = "default"
		self.send_1_id_63["LED_feedback_active"] = "1"
		self.send_1_id_63["LED_on"] = "127"
		self.send_1_id_63["LED_off"] = "0"
		self.send_1_id_63["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_83"]
		self.send_1_id_63["snap_to"] = True
		self.send_1_id_63["json_id"] = 63
		self.send_1_id_63["mapping_name"] = "Send 1"
		self.send_1_id_63["mapping_type"] = "Send"
		self.send_1_id_63["parent_json_id"] = 71
		self.send_1_id_63["parent_name"] = "sends_7_id_71"
		self.send_2_id_64 = {}
		self.send_2_id_64["attached_to"] = "midi_cc_ch_6_val_71"
		self.send_2_id_64["track"] = self.track_num(2)
		self.send_2_id_64["module"] = "self.song().tracks[self.track_num(6)].mixer_device.sends[1]"
		self.send_2_id_64["element"] = "value"
		self.send_2_id_64["output_type"] = "val"
		self.send_2_id_64["minimum"] = round(0,3)
		self.send_2_id_64["maximum"] = round(100,3)
		self.send_2_id_64["decimal_places"] = 3
		self.send_2_id_64["ui_listener"] = "value"
		self.send_2_id_64["feedback_brain"] = "feedback_range"
		self.send_2_id_64["ctrl_type"] = "absolute"
		self.send_2_id_64["takeover_mode"] = "Value scaling"
		self.send_2_id_64["enc_first"] = 0
		self.send_2_id_64["enc_second"] = 127
		self.send_2_id_64["reverse_mode"] = False
		self.send_2_id_64["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_64["LED_feedback"] = "default"
		self.send_2_id_64["LED_feedback_active"] = "1"
		self.send_2_id_64["LED_on"] = "127"
		self.send_2_id_64["LED_off"] = "0"
		self.send_2_id_64["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_71"]
		self.send_2_id_64["snap_to"] = True
		self.send_2_id_64["json_id"] = 64
		self.send_2_id_64["mapping_name"] = "Send 2"
		self.send_2_id_64["mapping_type"] = "Send"
		self.send_2_id_64["parent_json_id"] = 71
		self.send_2_id_64["parent_name"] = "sends_7_id_71"
		self.send_3_id_65 = {}
		self.send_3_id_65["attached_to"] = "midi_cc_ch_6_val_70"
		self.send_3_id_65["track"] = self.track_num(2)
		self.send_3_id_65["module"] = "self.song().tracks[self.track_num(6)].mixer_device.sends[2]"
		self.send_3_id_65["element"] = "value"
		self.send_3_id_65["output_type"] = "val"
		self.send_3_id_65["minimum"] = round(0,3)
		self.send_3_id_65["maximum"] = round(100,3)
		self.send_3_id_65["decimal_places"] = 3
		self.send_3_id_65["ui_listener"] = "value"
		self.send_3_id_65["feedback_brain"] = "feedback_range"
		self.send_3_id_65["ctrl_type"] = "absolute"
		self.send_3_id_65["takeover_mode"] = "Value scaling"
		self.send_3_id_65["enc_first"] = 0
		self.send_3_id_65["enc_second"] = 127
		self.send_3_id_65["reverse_mode"] = False
		self.send_3_id_65["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_65["LED_feedback"] = "default"
		self.send_3_id_65["LED_feedback_active"] = "1"
		self.send_3_id_65["LED_on"] = "127"
		self.send_3_id_65["LED_off"] = "0"
		self.send_3_id_65["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_70"]
		self.send_3_id_65["snap_to"] = True
		self.send_3_id_65["json_id"] = 65
		self.send_3_id_65["mapping_name"] = "Send 3"
		self.send_3_id_65["mapping_type"] = "Send"
		self.send_3_id_65["parent_json_id"] = 71
		self.send_3_id_65["parent_name"] = "sends_7_id_71"
		self.send_4_id_66 = {}
		self.send_4_id_66["attached_to"] = "midi_cc_ch_6_val_10"
		self.send_4_id_66["track"] = self.track_num(2)
		self.send_4_id_66["module"] = "self.song().tracks[self.track_num(6)].mixer_device.sends[3]"
		self.send_4_id_66["element"] = "value"
		self.send_4_id_66["output_type"] = "val"
		self.send_4_id_66["minimum"] = round(0,3)
		self.send_4_id_66["maximum"] = round(100,3)
		self.send_4_id_66["decimal_places"] = 3
		self.send_4_id_66["ui_listener"] = "value"
		self.send_4_id_66["feedback_brain"] = "feedback_range"
		self.send_4_id_66["ctrl_type"] = "absolute"
		self.send_4_id_66["takeover_mode"] = "Value scaling"
		self.send_4_id_66["enc_first"] = 0
		self.send_4_id_66["enc_second"] = 127
		self.send_4_id_66["reverse_mode"] = False
		self.send_4_id_66["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_66["LED_feedback"] = "default"
		self.send_4_id_66["LED_feedback_active"] = "1"
		self.send_4_id_66["LED_on"] = "127"
		self.send_4_id_66["LED_off"] = "0"
		self.send_4_id_66["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_10"]
		self.send_4_id_66["snap_to"] = True
		self.send_4_id_66["json_id"] = 66
		self.send_4_id_66["mapping_name"] = "Send 4"
		self.send_4_id_66["mapping_type"] = "Send"
		self.send_4_id_66["parent_json_id"] = 71
		self.send_4_id_66["parent_name"] = "sends_7_id_71"
		self.volume_7_id_67 = {}
		self.volume_7_id_67["attached_to"] = "midi_cc_ch_6_val_7"
		self.volume_7_id_67["track"] = self.track_num(2)
		self.volume_7_id_67["module"] = "self.song().tracks[self.track_num(6)].mixer_device.volume"
		self.volume_7_id_67["element"] = "value"
		self.volume_7_id_67["output_type"] = "val"
		self.volume_7_id_67["minimum"] = round(0,2)
		self.volume_7_id_67["maximum"] = round(85,2)
		self.volume_7_id_67["decimal_places"] = 2
		self.volume_7_id_67["ui_listener"] = "value"
		self.volume_7_id_67["feedback_brain"] = "feedback_range"
		self.volume_7_id_67["ctrl_type"] = "absolute"
		self.volume_7_id_67["takeover_mode"] = "None"
		self.volume_7_id_67["enc_first"] = 0
		self.volume_7_id_67["enc_second"] = 127
		self.volume_7_id_67["reverse_mode"] = False
		self.volume_7_id_67["LED_mapping_type_needs_feedback"] = "1"
		self.volume_7_id_67["LED_feedback"] = "default"
		self.volume_7_id_67["LED_feedback_active"] = "1"
		self.volume_7_id_67["LED_on"] = "127"
		self.volume_7_id_67["LED_off"] = "0"
		self.volume_7_id_67["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_7"]
		self.volume_7_id_67["snap_to"] = True
		self.volume_7_id_67["json_id"] = 67
		self.volume_7_id_67["mapping_name"] = "Volume 7"
		self.volume_7_id_67["mapping_type"] = "Volume"
		self.volume_7_id_67["parent_json_id"] = 62
		self.volume_7_id_67["parent_name"] = "track_7_id_62"
		self.pan_7_id_68 = {}
		self.pan_7_id_68["attached_to"] = "midi_cc_ch_6_val_82"
		self.pan_7_id_68["track"] = self.track_num(2)
		self.pan_7_id_68["module"] = "self.song().tracks[self.track_num(6)].mixer_device.panning"
		self.pan_7_id_68["element"] = "value"
		self.pan_7_id_68["output_type"] = "val"
		self.pan_7_id_68["minimum"] = round(0,2)
		self.pan_7_id_68["maximum"] = round(100,2)
		self.pan_7_id_68["decimal_places"] = 2
		self.pan_7_id_68["ui_listener"] = "value"
		self.pan_7_id_68["feedback_brain"] = "feedback_range"
		self.pan_7_id_68["ctrl_type"] = "absolute"
		self.pan_7_id_68["takeover_mode"] = "Value scaling"
		self.pan_7_id_68["enc_first"] = 0
		self.pan_7_id_68["enc_second"] = 127
		self.pan_7_id_68["reverse_mode"] = False
		self.pan_7_id_68["LED_mapping_type_needs_feedback"] = "1"
		self.pan_7_id_68["LED_feedback"] = "default"
		self.pan_7_id_68["LED_feedback_active"] = "1"
		self.pan_7_id_68["LED_on"] = "127"
		self.pan_7_id_68["LED_off"] = "0"
		self.pan_7_id_68["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_82"]
		self.pan_7_id_68["snap_to"] = True
		self.pan_7_id_68["json_id"] = 68
		self.pan_7_id_68["mapping_name"] = "Pan 7"
		self.pan_7_id_68["mapping_type"] = "Pan"
		self.pan_7_id_68["parent_json_id"] = 62
		self.pan_7_id_68["parent_name"] = "track_7_id_62"
		self.mute_7_id_69 = {}
		self.mute_7_id_69["attached_to"] = "midi_cc_ch_6_val_94"
		self.mute_7_id_69["track"] = self.track_num(2)
		self.mute_7_id_69["module"] = "self.song().tracks[self.track_num(6)]"
		self.mute_7_id_69["element"] = "mute"
		self.mute_7_id_69["output_type"] = "bool"
		self.mute_7_id_69["ui_listener"] = "mute"
		self.mute_7_id_69["feedback_brain"] = "feedback_bool"
		self.mute_7_id_69["enc_first"] = 127
		self.mute_7_id_69["enc_second"] = 0
		self.mute_7_id_69["switch_type"] = "toggle"
		self.mute_7_id_69["ctrl_type"] = "on/off"
		self.mute_7_id_69["LED_mapping_type_needs_feedback"] = "1"
		self.mute_7_id_69["LED_feedback"] = "default"
		self.mute_7_id_69["LED_feedback_active"] = "1"
		self.mute_7_id_69["LED_on"] = "127"
		self.mute_7_id_69["LED_off"] = "0"
		self.mute_7_id_69["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_94"]
		self.mute_7_id_69["json_id"] = 69
		self.mute_7_id_69["mapping_name"] = "Mute 7"
		self.mute_7_id_69["mapping_type"] = "Mute"
		self.mute_7_id_69["parent_json_id"] = 62
		self.mute_7_id_69["parent_name"] = "track_7_id_62"
		self.track_8_id_72 = {}
		self.track_8_id_72["track"] = self.track_num(2)
		self.track_8_id_72["module"] = "self.song().tracks[self.track_num(7)]"
		self.track_8_id_72["LED_mapping_type_needs_feedback"] = ""
		self.track_8_id_72["LED_feedback"] = "custom"
		self.track_8_id_72["LED_feedback_active"] = ""
		self.track_8_id_72["LED_on"] = "127"
		self.track_8_id_72["LED_off"] = "0"
		self.track_8_id_72["LED_send_feedback_to_selected"] = []
		self.track_8_id_72["json_id"] = 72
		self.track_8_id_72["mapping_name"] = "Track 8"
		self.track_8_id_72["mapping_type"] = "Track"
		self.track_8_id_72["parent_json_id"] = 1
		self.track_8_id_72["parent_name"] = "mode_1_id_1"
		self.send_1_id_73 = {}
		self.send_1_id_73["attached_to"] = "midi_cc_ch_7_val_83"
		self.send_1_id_73["track"] = self.track_num(2)
		self.send_1_id_73["module"] = "self.song().tracks[self.track_num(7)].mixer_device.sends[0]"
		self.send_1_id_73["element"] = "value"
		self.send_1_id_73["output_type"] = "val"
		self.send_1_id_73["minimum"] = round(0,3)
		self.send_1_id_73["maximum"] = round(100,3)
		self.send_1_id_73["decimal_places"] = 3
		self.send_1_id_73["ui_listener"] = "value"
		self.send_1_id_73["feedback_brain"] = "feedback_range"
		self.send_1_id_73["ctrl_type"] = "absolute"
		self.send_1_id_73["takeover_mode"] = "Value scaling"
		self.send_1_id_73["enc_first"] = 0
		self.send_1_id_73["enc_second"] = 127
		self.send_1_id_73["reverse_mode"] = False
		self.send_1_id_73["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_73["LED_feedback"] = "default"
		self.send_1_id_73["LED_feedback_active"] = "1"
		self.send_1_id_73["LED_on"] = "127"
		self.send_1_id_73["LED_off"] = "0"
		self.send_1_id_73["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_83"]
		self.send_1_id_73["snap_to"] = True
		self.send_1_id_73["json_id"] = 73
		self.send_1_id_73["mapping_name"] = "Send 1"
		self.send_1_id_73["mapping_type"] = "Send"
		self.send_1_id_73["parent_json_id"] = 81
		self.send_1_id_73["parent_name"] = "sends_7_id_81"
		self.send_2_id_74 = {}
		self.send_2_id_74["attached_to"] = "midi_cc_ch_7_val_71"
		self.send_2_id_74["track"] = self.track_num(2)
		self.send_2_id_74["module"] = "self.song().tracks[self.track_num(7)].mixer_device.sends[1]"
		self.send_2_id_74["element"] = "value"
		self.send_2_id_74["output_type"] = "val"
		self.send_2_id_74["minimum"] = round(0,3)
		self.send_2_id_74["maximum"] = round(100,3)
		self.send_2_id_74["decimal_places"] = 3
		self.send_2_id_74["ui_listener"] = "value"
		self.send_2_id_74["feedback_brain"] = "feedback_range"
		self.send_2_id_74["ctrl_type"] = "absolute"
		self.send_2_id_74["takeover_mode"] = "Value scaling"
		self.send_2_id_74["enc_first"] = 0
		self.send_2_id_74["enc_second"] = 127
		self.send_2_id_74["reverse_mode"] = False
		self.send_2_id_74["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_74["LED_feedback"] = "default"
		self.send_2_id_74["LED_feedback_active"] = "1"
		self.send_2_id_74["LED_on"] = "127"
		self.send_2_id_74["LED_off"] = "0"
		self.send_2_id_74["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_71"]
		self.send_2_id_74["snap_to"] = True
		self.send_2_id_74["json_id"] = 74
		self.send_2_id_74["mapping_name"] = "Send 2"
		self.send_2_id_74["mapping_type"] = "Send"
		self.send_2_id_74["parent_json_id"] = 81
		self.send_2_id_74["parent_name"] = "sends_7_id_81"
		self.send_3_id_75 = {}
		self.send_3_id_75["attached_to"] = "midi_cc_ch_7_val_70"
		self.send_3_id_75["track"] = self.track_num(2)
		self.send_3_id_75["module"] = "self.song().tracks[self.track_num(7)].mixer_device.sends[2]"
		self.send_3_id_75["element"] = "value"
		self.send_3_id_75["output_type"] = "val"
		self.send_3_id_75["minimum"] = round(0,3)
		self.send_3_id_75["maximum"] = round(100,3)
		self.send_3_id_75["decimal_places"] = 3
		self.send_3_id_75["ui_listener"] = "value"
		self.send_3_id_75["feedback_brain"] = "feedback_range"
		self.send_3_id_75["ctrl_type"] = "absolute"
		self.send_3_id_75["takeover_mode"] = "Value scaling"
		self.send_3_id_75["enc_first"] = 0
		self.send_3_id_75["enc_second"] = 127
		self.send_3_id_75["reverse_mode"] = False
		self.send_3_id_75["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_75["LED_feedback"] = "default"
		self.send_3_id_75["LED_feedback_active"] = "1"
		self.send_3_id_75["LED_on"] = "127"
		self.send_3_id_75["LED_off"] = "0"
		self.send_3_id_75["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_70"]
		self.send_3_id_75["snap_to"] = True
		self.send_3_id_75["json_id"] = 75
		self.send_3_id_75["mapping_name"] = "Send 3"
		self.send_3_id_75["mapping_type"] = "Send"
		self.send_3_id_75["parent_json_id"] = 81
		self.send_3_id_75["parent_name"] = "sends_7_id_81"
		self.send_4_id_76 = {}
		self.send_4_id_76["attached_to"] = "midi_cc_ch_7_val_10"
		self.send_4_id_76["track"] = self.track_num(2)
		self.send_4_id_76["module"] = "self.song().tracks[self.track_num(7)].mixer_device.sends[3]"
		self.send_4_id_76["element"] = "value"
		self.send_4_id_76["output_type"] = "val"
		self.send_4_id_76["minimum"] = round(0,3)
		self.send_4_id_76["maximum"] = round(100,3)
		self.send_4_id_76["decimal_places"] = 3
		self.send_4_id_76["ui_listener"] = "value"
		self.send_4_id_76["feedback_brain"] = "feedback_range"
		self.send_4_id_76["ctrl_type"] = "absolute"
		self.send_4_id_76["takeover_mode"] = "Value scaling"
		self.send_4_id_76["enc_first"] = 0
		self.send_4_id_76["enc_second"] = 127
		self.send_4_id_76["reverse_mode"] = False
		self.send_4_id_76["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_76["LED_feedback"] = "default"
		self.send_4_id_76["LED_feedback_active"] = "1"
		self.send_4_id_76["LED_on"] = "127"
		self.send_4_id_76["LED_off"] = "0"
		self.send_4_id_76["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_10"]
		self.send_4_id_76["snap_to"] = True
		self.send_4_id_76["json_id"] = 76
		self.send_4_id_76["mapping_name"] = "Send 4"
		self.send_4_id_76["mapping_type"] = "Send"
		self.send_4_id_76["parent_json_id"] = 81
		self.send_4_id_76["parent_name"] = "sends_7_id_81"
		self.volume_8_id_77 = {}
		self.volume_8_id_77["attached_to"] = "midi_cc_ch_7_val_7"
		self.volume_8_id_77["track"] = self.track_num(2)
		self.volume_8_id_77["module"] = "self.song().tracks[self.track_num(7)].mixer_device.volume"
		self.volume_8_id_77["element"] = "value"
		self.volume_8_id_77["output_type"] = "val"
		self.volume_8_id_77["minimum"] = round(0,2)
		self.volume_8_id_77["maximum"] = round(85,2)
		self.volume_8_id_77["decimal_places"] = 2
		self.volume_8_id_77["ui_listener"] = "value"
		self.volume_8_id_77["feedback_brain"] = "feedback_range"
		self.volume_8_id_77["ctrl_type"] = "absolute"
		self.volume_8_id_77["takeover_mode"] = "None"
		self.volume_8_id_77["enc_first"] = 0
		self.volume_8_id_77["enc_second"] = 127
		self.volume_8_id_77["reverse_mode"] = False
		self.volume_8_id_77["LED_mapping_type_needs_feedback"] = "1"
		self.volume_8_id_77["LED_feedback"] = "default"
		self.volume_8_id_77["LED_feedback_active"] = "1"
		self.volume_8_id_77["LED_on"] = "127"
		self.volume_8_id_77["LED_off"] = "0"
		self.volume_8_id_77["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_7"]
		self.volume_8_id_77["snap_to"] = True
		self.volume_8_id_77["json_id"] = 77
		self.volume_8_id_77["mapping_name"] = "Volume 8"
		self.volume_8_id_77["mapping_type"] = "Volume"
		self.volume_8_id_77["parent_json_id"] = 72
		self.volume_8_id_77["parent_name"] = "track_8_id_72"
		self.pan_8_id_78 = {}
		self.pan_8_id_78["attached_to"] = "midi_cc_ch_7_val_82"
		self.pan_8_id_78["track"] = self.track_num(2)
		self.pan_8_id_78["module"] = "self.song().tracks[self.track_num(7)].mixer_device.panning"
		self.pan_8_id_78["element"] = "value"
		self.pan_8_id_78["output_type"] = "val"
		self.pan_8_id_78["minimum"] = round(0,2)
		self.pan_8_id_78["maximum"] = round(100,2)
		self.pan_8_id_78["decimal_places"] = 2
		self.pan_8_id_78["ui_listener"] = "value"
		self.pan_8_id_78["feedback_brain"] = "feedback_range"
		self.pan_8_id_78["ctrl_type"] = "absolute"
		self.pan_8_id_78["takeover_mode"] = "Value scaling"
		self.pan_8_id_78["enc_first"] = 0
		self.pan_8_id_78["enc_second"] = 127
		self.pan_8_id_78["reverse_mode"] = False
		self.pan_8_id_78["LED_mapping_type_needs_feedback"] = "1"
		self.pan_8_id_78["LED_feedback"] = "default"
		self.pan_8_id_78["LED_feedback_active"] = "1"
		self.pan_8_id_78["LED_on"] = "127"
		self.pan_8_id_78["LED_off"] = "0"
		self.pan_8_id_78["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_82"]
		self.pan_8_id_78["snap_to"] = True
		self.pan_8_id_78["json_id"] = 78
		self.pan_8_id_78["mapping_name"] = "Pan 8"
		self.pan_8_id_78["mapping_type"] = "Pan"
		self.pan_8_id_78["parent_json_id"] = 72
		self.pan_8_id_78["parent_name"] = "track_8_id_72"
		self.mute_8_id_79 = {}
		self.mute_8_id_79["attached_to"] = "midi_cc_ch_7_val_94"
		self.mute_8_id_79["track"] = self.track_num(2)
		self.mute_8_id_79["module"] = "self.song().tracks[self.track_num(7)]"
		self.mute_8_id_79["element"] = "mute"
		self.mute_8_id_79["output_type"] = "bool"
		self.mute_8_id_79["ui_listener"] = "mute"
		self.mute_8_id_79["feedback_brain"] = "feedback_bool"
		self.mute_8_id_79["enc_first"] = 127
		self.mute_8_id_79["enc_second"] = 0
		self.mute_8_id_79["switch_type"] = "toggle"
		self.mute_8_id_79["ctrl_type"] = "on/off"
		self.mute_8_id_79["LED_mapping_type_needs_feedback"] = "1"
		self.mute_8_id_79["LED_feedback"] = "default"
		self.mute_8_id_79["LED_feedback_active"] = "1"
		self.mute_8_id_79["LED_on"] = "127"
		self.mute_8_id_79["LED_off"] = "0"
		self.mute_8_id_79["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_94"]
		self.mute_8_id_79["json_id"] = 79
		self.mute_8_id_79["mapping_name"] = "Mute 8"
		self.mute_8_id_79["mapping_type"] = "Mute"
		self.mute_8_id_79["parent_json_id"] = 72
		self.mute_8_id_79["parent_name"] = "track_8_id_72"
		self.track_select_id_85 = {}
		self.track_select_id_85["track"] = self.track_num(2)
		self.track_select_id_85["module"] = "self.song().view.selected_track"
		self.track_select_id_85["LED_mapping_type_needs_feedback"] = ""
		self.track_select_id_85["LED_feedback"] = "custom"
		self.track_select_id_85["LED_feedback_active"] = ""
		self.track_select_id_85["LED_on"] = "127"
		self.track_select_id_85["LED_off"] = "0"
		self.track_select_id_85["LED_send_feedback_to_selected"] = []
		self.track_select_id_85["json_id"] = 85
		self.track_select_id_85["mapping_name"] = "track select"
		self.track_select_id_85["mapping_type"] = "Track"
		self.track_select_id_85["parent_json_id"] = 1
		self.track_select_id_85["parent_name"] = "mode_1_id_1"
		self.device_1_id_86 = {}
		self.device_1_id_86["track"] = self.track_num(2)
		self.device_1_id_86["module"] = "self.song().view.selected_track.devices[0]"
		self.device_1_id_86["LED_mapping_type_needs_feedback"] = ""
		self.device_1_id_86["LED_feedback"] = "custom"
		self.device_1_id_86["LED_feedback_active"] = ""
		self.device_1_id_86["LED_on"] = "127"
		self.device_1_id_86["LED_off"] = "0"
		self.device_1_id_86["LED_send_feedback_to_selected"] = []
		self.device_1_id_86["json_id"] = 86
		self.device_1_id_86["mapping_name"] = "Device 1"
		self.device_1_id_86["mapping_type"] = "Device"
		self.device_1_id_86["parent_json_id"] = 85
		self.device_1_id_86["parent_name"] = "track_select_id_85"
		self.parameter_bank_1_id_87 = {}
		self.parameter_bank_1_id_87["LED_mapping_type_needs_feedback"] = ""
		self.parameter_bank_1_id_87["LED_feedback"] = "custom"
		self.parameter_bank_1_id_87["LED_feedback_active"] = ""
		self.parameter_bank_1_id_87["LED_on"] = "127"
		self.parameter_bank_1_id_87["LED_off"] = "0"
		self.parameter_bank_1_id_87["LED_send_feedback_to_selected"] = []
		self.parameter_bank_1_id_87["json_id"] = 87
		self.parameter_bank_1_id_87["mapping_name"] = "Parameter Bank 1"
		self.parameter_bank_1_id_87["mapping_type"] = "Parameter Bank"
		self.parameter_bank_1_id_87["parent_json_id"] = 86
		self.parameter_bank_1_id_87["parent_name"] = "device_1_id_86"
		self.parameter_1_id_88 = {}
		self.parameter_1_id_88["attached_to"] = "midi_cc_ch_15_val_85"
		self.parameter_1_id_88["track"] = self.track_num(2)
		self.parameter_1_id_88["module"] = "self.song().view.selected_track.devices[0].parameters[1]"
		self.parameter_1_id_88["element"] = "value"
		self.parameter_1_id_88["output_type"] = "val"
		self.parameter_1_id_88["minimum"] = round(0,2)
		self.parameter_1_id_88["maximum"] = round(100,2)
		self.parameter_1_id_88["decimal_places"] = 2
		self.parameter_1_id_88["ui_listener"] = "value"
		self.parameter_1_id_88["feedback_brain"] = "feedback_range"
		self.parameter_1_id_88["ctrl_type"] = "absolute"
		self.parameter_1_id_88["takeover_mode"] = "Value scaling"
		self.parameter_1_id_88["enc_first"] = 0
		self.parameter_1_id_88["enc_second"] = 127
		self.parameter_1_id_88["reverse_mode"] = False
		self.parameter_1_id_88["steps"] = 20
		self.parameter_1_id_88["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_1_id_88["LED_feedback"] = "default"
		self.parameter_1_id_88["LED_feedback_active"] = "1"
		self.parameter_1_id_88["LED_on"] = "127"
		self.parameter_1_id_88["LED_off"] = "0"
		self.parameter_1_id_88["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_85"]
		self.parameter_1_id_88["snap_to"] = True
		self.parameter_1_id_88["json_id"] = 88
		self.parameter_1_id_88["mapping_name"] = "Parameter 1"
		self.parameter_1_id_88["mapping_type"] = "Parameter"
		self.parameter_1_id_88["parent_json_id"] = 87
		self.parameter_1_id_88["parent_name"] = "parameter_bank_1_id_87"
		self.parameter_2_id_89 = {}
		self.parameter_2_id_89["attached_to"] = "midi_cc_ch_15_val_86"
		self.parameter_2_id_89["track"] = self.track_num(2)
		self.parameter_2_id_89["module"] = "self.song().view.selected_track.devices[0].parameters[2]"
		self.parameter_2_id_89["element"] = "value"
		self.parameter_2_id_89["output_type"] = "val"
		self.parameter_2_id_89["minimum"] = round(0,2)
		self.parameter_2_id_89["maximum"] = round(100,2)
		self.parameter_2_id_89["decimal_places"] = 2
		self.parameter_2_id_89["ui_listener"] = "value"
		self.parameter_2_id_89["feedback_brain"] = "feedback_range"
		self.parameter_2_id_89["ctrl_type"] = "absolute"
		self.parameter_2_id_89["takeover_mode"] = "Value scaling"
		self.parameter_2_id_89["enc_first"] = 0
		self.parameter_2_id_89["enc_second"] = 127
		self.parameter_2_id_89["reverse_mode"] = False
		self.parameter_2_id_89["steps"] = 20
		self.parameter_2_id_89["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_2_id_89["LED_feedback"] = "default"
		self.parameter_2_id_89["LED_feedback_active"] = "1"
		self.parameter_2_id_89["LED_on"] = "127"
		self.parameter_2_id_89["LED_off"] = "0"
		self.parameter_2_id_89["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_86"]
		self.parameter_2_id_89["snap_to"] = True
		self.parameter_2_id_89["json_id"] = 89
		self.parameter_2_id_89["mapping_name"] = "Parameter 2"
		self.parameter_2_id_89["mapping_type"] = "Parameter"
		self.parameter_2_id_89["parent_json_id"] = 87
		self.parameter_2_id_89["parent_name"] = "parameter_bank_1_id_87"
		self.parameter_3_id_90 = {}
		self.parameter_3_id_90["attached_to"] = "midi_cc_ch_15_val_87"
		self.parameter_3_id_90["track"] = self.track_num(2)
		self.parameter_3_id_90["module"] = "self.song().view.selected_track.devices[0].parameters[3]"
		self.parameter_3_id_90["element"] = "value"
		self.parameter_3_id_90["output_type"] = "val"
		self.parameter_3_id_90["minimum"] = round(0,2)
		self.parameter_3_id_90["maximum"] = round(100,2)
		self.parameter_3_id_90["decimal_places"] = 2
		self.parameter_3_id_90["ui_listener"] = "value"
		self.parameter_3_id_90["feedback_brain"] = "feedback_range"
		self.parameter_3_id_90["ctrl_type"] = "absolute"
		self.parameter_3_id_90["takeover_mode"] = "Value scaling"
		self.parameter_3_id_90["enc_first"] = 0
		self.parameter_3_id_90["enc_second"] = 127
		self.parameter_3_id_90["reverse_mode"] = False
		self.parameter_3_id_90["steps"] = 20
		self.parameter_3_id_90["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_3_id_90["LED_feedback"] = "default"
		self.parameter_3_id_90["LED_feedback_active"] = "1"
		self.parameter_3_id_90["LED_on"] = "127"
		self.parameter_3_id_90["LED_off"] = "0"
		self.parameter_3_id_90["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_87"]
		self.parameter_3_id_90["snap_to"] = True
		self.parameter_3_id_90["json_id"] = 90
		self.parameter_3_id_90["mapping_name"] = "Parameter 3"
		self.parameter_3_id_90["mapping_type"] = "Parameter"
		self.parameter_3_id_90["parent_json_id"] = 87
		self.parameter_3_id_90["parent_name"] = "parameter_bank_1_id_87"
		self.parameter_4_id_91 = {}
		self.parameter_4_id_91["attached_to"] = "midi_cc_ch_15_val_88"
		self.parameter_4_id_91["track"] = self.track_num(2)
		self.parameter_4_id_91["module"] = "self.song().view.selected_track.devices[0].parameters[4]"
		self.parameter_4_id_91["element"] = "value"
		self.parameter_4_id_91["output_type"] = "val"
		self.parameter_4_id_91["minimum"] = round(0,2)
		self.parameter_4_id_91["maximum"] = round(100,2)
		self.parameter_4_id_91["decimal_places"] = 2
		self.parameter_4_id_91["ui_listener"] = "value"
		self.parameter_4_id_91["feedback_brain"] = "feedback_range"
		self.parameter_4_id_91["ctrl_type"] = "absolute"
		self.parameter_4_id_91["takeover_mode"] = "Value scaling"
		self.parameter_4_id_91["enc_first"] = 0
		self.parameter_4_id_91["enc_second"] = 127
		self.parameter_4_id_91["reverse_mode"] = False
		self.parameter_4_id_91["steps"] = 20
		self.parameter_4_id_91["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_4_id_91["LED_feedback"] = "default"
		self.parameter_4_id_91["LED_feedback_active"] = "1"
		self.parameter_4_id_91["LED_on"] = "127"
		self.parameter_4_id_91["LED_off"] = "0"
		self.parameter_4_id_91["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_88"]
		self.parameter_4_id_91["snap_to"] = True
		self.parameter_4_id_91["json_id"] = 91
		self.parameter_4_id_91["mapping_name"] = "Parameter 4"
		self.parameter_4_id_91["mapping_type"] = "Parameter"
		self.parameter_4_id_91["parent_json_id"] = 87
		self.parameter_4_id_91["parent_name"] = "parameter_bank_1_id_87"
		self.parameter_5_id_92 = {}
		self.parameter_5_id_92["attached_to"] = "midi_cc_ch_15_val_89"
		self.parameter_5_id_92["track"] = self.track_num(2)
		self.parameter_5_id_92["module"] = "self.song().view.selected_track.devices[0].parameters[5]"
		self.parameter_5_id_92["element"] = "value"
		self.parameter_5_id_92["output_type"] = "val"
		self.parameter_5_id_92["minimum"] = round(0,2)
		self.parameter_5_id_92["maximum"] = round(100,2)
		self.parameter_5_id_92["decimal_places"] = 2
		self.parameter_5_id_92["ui_listener"] = "value"
		self.parameter_5_id_92["feedback_brain"] = "feedback_range"
		self.parameter_5_id_92["ctrl_type"] = "absolute"
		self.parameter_5_id_92["takeover_mode"] = "Value scaling"
		self.parameter_5_id_92["enc_first"] = 0
		self.parameter_5_id_92["enc_second"] = 127
		self.parameter_5_id_92["reverse_mode"] = False
		self.parameter_5_id_92["steps"] = 20
		self.parameter_5_id_92["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_5_id_92["LED_feedback"] = "default"
		self.parameter_5_id_92["LED_feedback_active"] = "1"
		self.parameter_5_id_92["LED_on"] = "127"
		self.parameter_5_id_92["LED_off"] = "0"
		self.parameter_5_id_92["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_89"]
		self.parameter_5_id_92["snap_to"] = True
		self.parameter_5_id_92["json_id"] = 92
		self.parameter_5_id_92["mapping_name"] = "Parameter 5"
		self.parameter_5_id_92["mapping_type"] = "Parameter"
		self.parameter_5_id_92["parent_json_id"] = 87
		self.parameter_5_id_92["parent_name"] = "parameter_bank_1_id_87"
		self.parameter_6_id_93 = {}
		self.parameter_6_id_93["attached_to"] = "midi_cc_ch_15_val_90"
		self.parameter_6_id_93["track"] = self.track_num(2)
		self.parameter_6_id_93["module"] = "self.song().view.selected_track.devices[0].parameters[6]"
		self.parameter_6_id_93["element"] = "value"
		self.parameter_6_id_93["output_type"] = "val"
		self.parameter_6_id_93["minimum"] = round(0,2)
		self.parameter_6_id_93["maximum"] = round(100,2)
		self.parameter_6_id_93["decimal_places"] = 2
		self.parameter_6_id_93["ui_listener"] = "value"
		self.parameter_6_id_93["feedback_brain"] = "feedback_range"
		self.parameter_6_id_93["ctrl_type"] = "absolute"
		self.parameter_6_id_93["takeover_mode"] = "Value scaling"
		self.parameter_6_id_93["enc_first"] = 0
		self.parameter_6_id_93["enc_second"] = 127
		self.parameter_6_id_93["reverse_mode"] = False
		self.parameter_6_id_93["steps"] = 20
		self.parameter_6_id_93["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_6_id_93["LED_feedback"] = "default"
		self.parameter_6_id_93["LED_feedback_active"] = "1"
		self.parameter_6_id_93["LED_on"] = "127"
		self.parameter_6_id_93["LED_off"] = "0"
		self.parameter_6_id_93["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_90"]
		self.parameter_6_id_93["snap_to"] = True
		self.parameter_6_id_93["json_id"] = 93
		self.parameter_6_id_93["mapping_name"] = "Parameter 6"
		self.parameter_6_id_93["mapping_type"] = "Parameter"
		self.parameter_6_id_93["parent_json_id"] = 87
		self.parameter_6_id_93["parent_name"] = "parameter_bank_1_id_87"
		self.parameter_7_id_94 = {}
		self.parameter_7_id_94["attached_to"] = "midi_cc_ch_15_val_91"
		self.parameter_7_id_94["track"] = self.track_num(2)
		self.parameter_7_id_94["module"] = "self.song().view.selected_track.devices[0].parameters[7]"
		self.parameter_7_id_94["element"] = "value"
		self.parameter_7_id_94["output_type"] = "val"
		self.parameter_7_id_94["minimum"] = round(0,2)
		self.parameter_7_id_94["maximum"] = round(100,2)
		self.parameter_7_id_94["decimal_places"] = 2
		self.parameter_7_id_94["ui_listener"] = "value"
		self.parameter_7_id_94["feedback_brain"] = "feedback_range"
		self.parameter_7_id_94["ctrl_type"] = "absolute"
		self.parameter_7_id_94["takeover_mode"] = "Value scaling"
		self.parameter_7_id_94["enc_first"] = 0
		self.parameter_7_id_94["enc_second"] = 127
		self.parameter_7_id_94["reverse_mode"] = False
		self.parameter_7_id_94["steps"] = 20
		self.parameter_7_id_94["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_7_id_94["LED_feedback"] = "default"
		self.parameter_7_id_94["LED_feedback_active"] = "1"
		self.parameter_7_id_94["LED_on"] = "127"
		self.parameter_7_id_94["LED_off"] = "0"
		self.parameter_7_id_94["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_91"]
		self.parameter_7_id_94["snap_to"] = True
		self.parameter_7_id_94["json_id"] = 94
		self.parameter_7_id_94["mapping_name"] = "Parameter 7"
		self.parameter_7_id_94["mapping_type"] = "Parameter"
		self.parameter_7_id_94["parent_json_id"] = 87
		self.parameter_7_id_94["parent_name"] = "parameter_bank_1_id_87"
		self.parameter_8_id_95 = {}
		self.parameter_8_id_95["attached_to"] = "midi_cc_ch_15_val_92"
		self.parameter_8_id_95["track"] = self.track_num(2)
		self.parameter_8_id_95["module"] = "self.song().view.selected_track.devices[0].parameters[8]"
		self.parameter_8_id_95["element"] = "value"
		self.parameter_8_id_95["output_type"] = "val"
		self.parameter_8_id_95["minimum"] = round(0,2)
		self.parameter_8_id_95["maximum"] = round(100,2)
		self.parameter_8_id_95["decimal_places"] = 2
		self.parameter_8_id_95["ui_listener"] = "value"
		self.parameter_8_id_95["feedback_brain"] = "feedback_range"
		self.parameter_8_id_95["ctrl_type"] = "absolute"
		self.parameter_8_id_95["takeover_mode"] = "Value scaling"
		self.parameter_8_id_95["enc_first"] = 0
		self.parameter_8_id_95["enc_second"] = 127
		self.parameter_8_id_95["reverse_mode"] = False
		self.parameter_8_id_95["steps"] = 20
		self.parameter_8_id_95["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_8_id_95["LED_feedback"] = "default"
		self.parameter_8_id_95["LED_feedback_active"] = "1"
		self.parameter_8_id_95["LED_on"] = "127"
		self.parameter_8_id_95["LED_off"] = "0"
		self.parameter_8_id_95["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_92"]
		self.parameter_8_id_95["snap_to"] = True
		self.parameter_8_id_95["json_id"] = 95
		self.parameter_8_id_95["mapping_name"] = "Parameter 8"
		self.parameter_8_id_95["mapping_type"] = "Parameter"
		self.parameter_8_id_95["parent_json_id"] = 87
		self.parameter_8_id_95["parent_name"] = "parameter_bank_1_id_87"
		self.track_9_id_96 = {}
		self.track_9_id_96["track"] = self.track_num(2)
		self.track_9_id_96["module"] = "self.song().tracks[self.track_num(8)]"
		self.track_9_id_96["LED_mapping_type_needs_feedback"] = ""
		self.track_9_id_96["LED_feedback"] = "custom"
		self.track_9_id_96["LED_feedback_active"] = ""
		self.track_9_id_96["LED_on"] = "127"
		self.track_9_id_96["LED_off"] = "0"
		self.track_9_id_96["LED_send_feedback_to_selected"] = []
		self.track_9_id_96["json_id"] = 96
		self.track_9_id_96["mapping_name"] = "Track 9"
		self.track_9_id_96["mapping_type"] = "Track"
		self.track_9_id_96["parent_json_id"] = 1
		self.track_9_id_96["parent_name"] = "mode_1_id_1"
		self.send_1_id_97 = {}
		self.send_1_id_97["attached_to"] = "midi_cc_ch_8_val_83"
		self.send_1_id_97["track"] = self.track_num(2)
		self.send_1_id_97["module"] = "self.song().tracks[self.track_num(8)].mixer_device.sends[0]"
		self.send_1_id_97["element"] = "value"
		self.send_1_id_97["output_type"] = "val"
		self.send_1_id_97["minimum"] = round(0,3)
		self.send_1_id_97["maximum"] = round(100,3)
		self.send_1_id_97["decimal_places"] = 3
		self.send_1_id_97["ui_listener"] = "value"
		self.send_1_id_97["feedback_brain"] = "feedback_range"
		self.send_1_id_97["ctrl_type"] = "absolute"
		self.send_1_id_97["takeover_mode"] = "None"
		self.send_1_id_97["enc_first"] = 0
		self.send_1_id_97["enc_second"] = 127
		self.send_1_id_97["reverse_mode"] = False
		self.send_1_id_97["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_97["LED_feedback"] = "default"
		self.send_1_id_97["LED_feedback_active"] = "1"
		self.send_1_id_97["LED_on"] = "127"
		self.send_1_id_97["LED_off"] = "0"
		self.send_1_id_97["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_83"]
		self.send_1_id_97["snap_to"] = True
		self.send_1_id_97["json_id"] = 97
		self.send_1_id_97["mapping_name"] = "Send 1"
		self.send_1_id_97["mapping_type"] = "Send"
		self.send_1_id_97["parent_json_id"] = 104
		self.send_1_id_97["parent_name"] = "sends_9_id_104"
		self.send_2_id_98 = {}
		self.send_2_id_98["attached_to"] = "midi_cc_ch_8_val_71"
		self.send_2_id_98["track"] = self.track_num(2)
		self.send_2_id_98["module"] = "self.song().tracks[self.track_num(8)].mixer_device.sends[1]"
		self.send_2_id_98["element"] = "value"
		self.send_2_id_98["output_type"] = "val"
		self.send_2_id_98["minimum"] = round(0,3)
		self.send_2_id_98["maximum"] = round(100,3)
		self.send_2_id_98["decimal_places"] = 3
		self.send_2_id_98["ui_listener"] = "value"
		self.send_2_id_98["feedback_brain"] = "feedback_range"
		self.send_2_id_98["ctrl_type"] = "absolute"
		self.send_2_id_98["takeover_mode"] = "None"
		self.send_2_id_98["enc_first"] = 0
		self.send_2_id_98["enc_second"] = 127
		self.send_2_id_98["reverse_mode"] = False
		self.send_2_id_98["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_98["LED_feedback"] = "default"
		self.send_2_id_98["LED_feedback_active"] = "1"
		self.send_2_id_98["LED_on"] = "127"
		self.send_2_id_98["LED_off"] = "0"
		self.send_2_id_98["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_71"]
		self.send_2_id_98["snap_to"] = True
		self.send_2_id_98["json_id"] = 98
		self.send_2_id_98["mapping_name"] = "Send 2"
		self.send_2_id_98["mapping_type"] = "Send"
		self.send_2_id_98["parent_json_id"] = 104
		self.send_2_id_98["parent_name"] = "sends_9_id_104"
		self.send_3_id_99 = {}
		self.send_3_id_99["attached_to"] = "midi_cc_ch_8_val_70"
		self.send_3_id_99["track"] = self.track_num(2)
		self.send_3_id_99["module"] = "self.song().tracks[self.track_num(8)].mixer_device.sends[2]"
		self.send_3_id_99["element"] = "value"
		self.send_3_id_99["output_type"] = "val"
		self.send_3_id_99["minimum"] = round(0,3)
		self.send_3_id_99["maximum"] = round(100,3)
		self.send_3_id_99["decimal_places"] = 3
		self.send_3_id_99["ui_listener"] = "value"
		self.send_3_id_99["feedback_brain"] = "feedback_range"
		self.send_3_id_99["ctrl_type"] = "absolute"
		self.send_3_id_99["takeover_mode"] = "None"
		self.send_3_id_99["enc_first"] = 0
		self.send_3_id_99["enc_second"] = 127
		self.send_3_id_99["reverse_mode"] = False
		self.send_3_id_99["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_99["LED_feedback"] = "default"
		self.send_3_id_99["LED_feedback_active"] = "1"
		self.send_3_id_99["LED_on"] = "127"
		self.send_3_id_99["LED_off"] = "0"
		self.send_3_id_99["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_70"]
		self.send_3_id_99["snap_to"] = True
		self.send_3_id_99["json_id"] = 99
		self.send_3_id_99["mapping_name"] = "Send 3"
		self.send_3_id_99["mapping_type"] = "Send"
		self.send_3_id_99["parent_json_id"] = 104
		self.send_3_id_99["parent_name"] = "sends_9_id_104"
		self.send_4_id_100 = {}
		self.send_4_id_100["attached_to"] = "midi_cc_ch_8_val_10"
		self.send_4_id_100["track"] = self.track_num(2)
		self.send_4_id_100["module"] = "self.song().tracks[self.track_num(8)].mixer_device.sends[3]"
		self.send_4_id_100["element"] = "value"
		self.send_4_id_100["output_type"] = "val"
		self.send_4_id_100["minimum"] = round(0,3)
		self.send_4_id_100["maximum"] = round(100,3)
		self.send_4_id_100["decimal_places"] = 3
		self.send_4_id_100["ui_listener"] = "value"
		self.send_4_id_100["feedback_brain"] = "feedback_range"
		self.send_4_id_100["ctrl_type"] = "absolute"
		self.send_4_id_100["takeover_mode"] = "None"
		self.send_4_id_100["enc_first"] = 0
		self.send_4_id_100["enc_second"] = 127
		self.send_4_id_100["reverse_mode"] = False
		self.send_4_id_100["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_100["LED_feedback"] = "default"
		self.send_4_id_100["LED_feedback_active"] = "1"
		self.send_4_id_100["LED_on"] = "127"
		self.send_4_id_100["LED_off"] = "0"
		self.send_4_id_100["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_10"]
		self.send_4_id_100["snap_to"] = True
		self.send_4_id_100["json_id"] = 100
		self.send_4_id_100["mapping_name"] = "Send 4"
		self.send_4_id_100["mapping_type"] = "Send"
		self.send_4_id_100["parent_json_id"] = 104
		self.send_4_id_100["parent_name"] = "sends_9_id_104"
		self.volume_9_id_101 = {}
		self.volume_9_id_101["attached_to"] = "midi_cc_ch_8_val_7"
		self.volume_9_id_101["track"] = self.track_num(2)
		self.volume_9_id_101["module"] = "self.song().tracks[self.track_num(8)].mixer_device.volume"
		self.volume_9_id_101["element"] = "value"
		self.volume_9_id_101["output_type"] = "val"
		self.volume_9_id_101["minimum"] = round(0,2)
		self.volume_9_id_101["maximum"] = round(85,2)
		self.volume_9_id_101["decimal_places"] = 2
		self.volume_9_id_101["ui_listener"] = "value"
		self.volume_9_id_101["feedback_brain"] = "feedback_range"
		self.volume_9_id_101["ctrl_type"] = "absolute"
		self.volume_9_id_101["takeover_mode"] = "None"
		self.volume_9_id_101["enc_first"] = 0
		self.volume_9_id_101["enc_second"] = 127
		self.volume_9_id_101["reverse_mode"] = False
		self.volume_9_id_101["LED_mapping_type_needs_feedback"] = "1"
		self.volume_9_id_101["LED_feedback"] = "default"
		self.volume_9_id_101["LED_feedback_active"] = "1"
		self.volume_9_id_101["LED_on"] = "127"
		self.volume_9_id_101["LED_off"] = "0"
		self.volume_9_id_101["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_7"]
		self.volume_9_id_101["snap_to"] = True
		self.volume_9_id_101["json_id"] = 101
		self.volume_9_id_101["mapping_name"] = "Volume 9"
		self.volume_9_id_101["mapping_type"] = "Volume"
		self.volume_9_id_101["parent_json_id"] = 96
		self.volume_9_id_101["parent_name"] = "track_9_id_96"
		self.pan_9_id_102 = {}
		self.pan_9_id_102["attached_to"] = "midi_cc_ch_8_val_82"
		self.pan_9_id_102["track"] = self.track_num(2)
		self.pan_9_id_102["module"] = "self.song().tracks[self.track_num(8)].mixer_device.panning"
		self.pan_9_id_102["element"] = "value"
		self.pan_9_id_102["output_type"] = "val"
		self.pan_9_id_102["minimum"] = round(0,2)
		self.pan_9_id_102["maximum"] = round(100,2)
		self.pan_9_id_102["decimal_places"] = 2
		self.pan_9_id_102["ui_listener"] = "value"
		self.pan_9_id_102["feedback_brain"] = "feedback_range"
		self.pan_9_id_102["ctrl_type"] = "absolute"
		self.pan_9_id_102["takeover_mode"] = "None"
		self.pan_9_id_102["enc_first"] = 0
		self.pan_9_id_102["enc_second"] = 127
		self.pan_9_id_102["reverse_mode"] = False
		self.pan_9_id_102["LED_mapping_type_needs_feedback"] = "1"
		self.pan_9_id_102["LED_feedback"] = "default"
		self.pan_9_id_102["LED_feedback_active"] = "1"
		self.pan_9_id_102["LED_on"] = "127"
		self.pan_9_id_102["LED_off"] = "0"
		self.pan_9_id_102["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_82"]
		self.pan_9_id_102["snap_to"] = True
		self.pan_9_id_102["json_id"] = 102
		self.pan_9_id_102["mapping_name"] = "Pan 9"
		self.pan_9_id_102["mapping_type"] = "Pan"
		self.pan_9_id_102["parent_json_id"] = 96
		self.pan_9_id_102["parent_name"] = "track_9_id_96"
		self.mute_9_id_103 = {}
		self.mute_9_id_103["attached_to"] = "midi_cc_ch_8_val_94"
		self.mute_9_id_103["track"] = self.track_num(2)
		self.mute_9_id_103["module"] = "self.song().tracks[self.track_num(8)]"
		self.mute_9_id_103["element"] = "mute"
		self.mute_9_id_103["output_type"] = "bool"
		self.mute_9_id_103["ui_listener"] = "mute"
		self.mute_9_id_103["feedback_brain"] = "feedback_bool"
		self.mute_9_id_103["enc_first"] = 127
		self.mute_9_id_103["enc_second"] = 0
		self.mute_9_id_103["switch_type"] = "toggle"
		self.mute_9_id_103["ctrl_type"] = "on/off"
		self.mute_9_id_103["LED_mapping_type_needs_feedback"] = "1"
		self.mute_9_id_103["LED_feedback"] = "default"
		self.mute_9_id_103["LED_feedback_active"] = "1"
		self.mute_9_id_103["LED_on"] = "127"
		self.mute_9_id_103["LED_off"] = "0"
		self.mute_9_id_103["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_94"]
		self.mute_9_id_103["json_id"] = 103
		self.mute_9_id_103["mapping_name"] = "Mute 9"
		self.mute_9_id_103["mapping_type"] = "Mute"
		self.mute_9_id_103["parent_json_id"] = 96
		self.mute_9_id_103["parent_name"] = "track_9_id_96"
		self.track_10_id_105 = {}
		self.track_10_id_105["track"] = self.track_num(2)
		self.track_10_id_105["module"] = "self.song().tracks[self.track_num(9)]"
		self.track_10_id_105["LED_mapping_type_needs_feedback"] = ""
		self.track_10_id_105["LED_feedback"] = "custom"
		self.track_10_id_105["LED_feedback_active"] = ""
		self.track_10_id_105["LED_on"] = "127"
		self.track_10_id_105["LED_off"] = "0"
		self.track_10_id_105["LED_send_feedback_to_selected"] = []
		self.track_10_id_105["json_id"] = 105
		self.track_10_id_105["mapping_name"] = "Track 10"
		self.track_10_id_105["mapping_type"] = "Track"
		self.track_10_id_105["parent_json_id"] = 1
		self.track_10_id_105["parent_name"] = "mode_1_id_1"
		self.send_1_id_106 = {}
		self.send_1_id_106["attached_to"] = "midi_cc_ch_9_val_83"
		self.send_1_id_106["track"] = self.track_num(2)
		self.send_1_id_106["module"] = "self.song().tracks[self.track_num(9)].mixer_device.sends[0]"
		self.send_1_id_106["element"] = "value"
		self.send_1_id_106["output_type"] = "val"
		self.send_1_id_106["minimum"] = round(0,3)
		self.send_1_id_106["maximum"] = round(100,3)
		self.send_1_id_106["decimal_places"] = 3
		self.send_1_id_106["ui_listener"] = "value"
		self.send_1_id_106["feedback_brain"] = "feedback_range"
		self.send_1_id_106["ctrl_type"] = "absolute"
		self.send_1_id_106["takeover_mode"] = "None"
		self.send_1_id_106["enc_first"] = 0
		self.send_1_id_106["enc_second"] = 127
		self.send_1_id_106["reverse_mode"] = False
		self.send_1_id_106["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_106["LED_feedback"] = "default"
		self.send_1_id_106["LED_feedback_active"] = "1"
		self.send_1_id_106["LED_on"] = "127"
		self.send_1_id_106["LED_off"] = "0"
		self.send_1_id_106["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_83"]
		self.send_1_id_106["snap_to"] = True
		self.send_1_id_106["json_id"] = 106
		self.send_1_id_106["mapping_name"] = "Send 1"
		self.send_1_id_106["mapping_type"] = "Send"
		self.send_1_id_106["parent_json_id"] = 113
		self.send_1_id_106["parent_name"] = "sends_10_id_113"
		self.send_2_id_107 = {}
		self.send_2_id_107["attached_to"] = "midi_cc_ch_9_val_71"
		self.send_2_id_107["track"] = self.track_num(2)
		self.send_2_id_107["module"] = "self.song().tracks[self.track_num(9)].mixer_device.sends[1]"
		self.send_2_id_107["element"] = "value"
		self.send_2_id_107["output_type"] = "val"
		self.send_2_id_107["minimum"] = round(0,3)
		self.send_2_id_107["maximum"] = round(100,3)
		self.send_2_id_107["decimal_places"] = 3
		self.send_2_id_107["ui_listener"] = "value"
		self.send_2_id_107["feedback_brain"] = "feedback_range"
		self.send_2_id_107["ctrl_type"] = "absolute"
		self.send_2_id_107["takeover_mode"] = "None"
		self.send_2_id_107["enc_first"] = 0
		self.send_2_id_107["enc_second"] = 127
		self.send_2_id_107["reverse_mode"] = False
		self.send_2_id_107["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_107["LED_feedback"] = "default"
		self.send_2_id_107["LED_feedback_active"] = "1"
		self.send_2_id_107["LED_on"] = "127"
		self.send_2_id_107["LED_off"] = "0"
		self.send_2_id_107["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_71"]
		self.send_2_id_107["snap_to"] = True
		self.send_2_id_107["json_id"] = 107
		self.send_2_id_107["mapping_name"] = "Send 2"
		self.send_2_id_107["mapping_type"] = "Send"
		self.send_2_id_107["parent_json_id"] = 113
		self.send_2_id_107["parent_name"] = "sends_10_id_113"
		self.send_3_id_108 = {}
		self.send_3_id_108["attached_to"] = "midi_cc_ch_9_val_70"
		self.send_3_id_108["track"] = self.track_num(2)
		self.send_3_id_108["module"] = "self.song().tracks[self.track_num(9)].mixer_device.sends[2]"
		self.send_3_id_108["element"] = "value"
		self.send_3_id_108["output_type"] = "val"
		self.send_3_id_108["minimum"] = round(0,3)
		self.send_3_id_108["maximum"] = round(100,3)
		self.send_3_id_108["decimal_places"] = 3
		self.send_3_id_108["ui_listener"] = "value"
		self.send_3_id_108["feedback_brain"] = "feedback_range"
		self.send_3_id_108["ctrl_type"] = "absolute"
		self.send_3_id_108["takeover_mode"] = "None"
		self.send_3_id_108["enc_first"] = 0
		self.send_3_id_108["enc_second"] = 127
		self.send_3_id_108["reverse_mode"] = False
		self.send_3_id_108["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_108["LED_feedback"] = "default"
		self.send_3_id_108["LED_feedback_active"] = "1"
		self.send_3_id_108["LED_on"] = "127"
		self.send_3_id_108["LED_off"] = "0"
		self.send_3_id_108["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_70"]
		self.send_3_id_108["snap_to"] = True
		self.send_3_id_108["json_id"] = 108
		self.send_3_id_108["mapping_name"] = "Send 3"
		self.send_3_id_108["mapping_type"] = "Send"
		self.send_3_id_108["parent_json_id"] = 113
		self.send_3_id_108["parent_name"] = "sends_10_id_113"
		self.send_4_id_109 = {}
		self.send_4_id_109["attached_to"] = "midi_cc_ch_9_val_10"
		self.send_4_id_109["track"] = self.track_num(2)
		self.send_4_id_109["module"] = "self.song().tracks[self.track_num(9)].mixer_device.sends[3]"
		self.send_4_id_109["element"] = "value"
		self.send_4_id_109["output_type"] = "val"
		self.send_4_id_109["minimum"] = round(0,3)
		self.send_4_id_109["maximum"] = round(100,3)
		self.send_4_id_109["decimal_places"] = 3
		self.send_4_id_109["ui_listener"] = "value"
		self.send_4_id_109["feedback_brain"] = "feedback_range"
		self.send_4_id_109["ctrl_type"] = "absolute"
		self.send_4_id_109["takeover_mode"] = "None"
		self.send_4_id_109["enc_first"] = 0
		self.send_4_id_109["enc_second"] = 127
		self.send_4_id_109["reverse_mode"] = False
		self.send_4_id_109["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_109["LED_feedback"] = "default"
		self.send_4_id_109["LED_feedback_active"] = "1"
		self.send_4_id_109["LED_on"] = "127"
		self.send_4_id_109["LED_off"] = "0"
		self.send_4_id_109["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_10"]
		self.send_4_id_109["snap_to"] = True
		self.send_4_id_109["json_id"] = 109
		self.send_4_id_109["mapping_name"] = "Send 4"
		self.send_4_id_109["mapping_type"] = "Send"
		self.send_4_id_109["parent_json_id"] = 113
		self.send_4_id_109["parent_name"] = "sends_10_id_113"
		self.volume_10_id_110 = {}
		self.volume_10_id_110["attached_to"] = "midi_cc_ch_9_val_7"
		self.volume_10_id_110["track"] = self.track_num(2)
		self.volume_10_id_110["module"] = "self.song().tracks[self.track_num(9)].mixer_device.volume"
		self.volume_10_id_110["element"] = "value"
		self.volume_10_id_110["output_type"] = "val"
		self.volume_10_id_110["minimum"] = round(0,2)
		self.volume_10_id_110["maximum"] = round(85,2)
		self.volume_10_id_110["decimal_places"] = 2
		self.volume_10_id_110["ui_listener"] = "value"
		self.volume_10_id_110["feedback_brain"] = "feedback_range"
		self.volume_10_id_110["ctrl_type"] = "absolute"
		self.volume_10_id_110["takeover_mode"] = "None"
		self.volume_10_id_110["enc_first"] = 0
		self.volume_10_id_110["enc_second"] = 127
		self.volume_10_id_110["reverse_mode"] = False
		self.volume_10_id_110["LED_mapping_type_needs_feedback"] = "1"
		self.volume_10_id_110["LED_feedback"] = "default"
		self.volume_10_id_110["LED_feedback_active"] = "1"
		self.volume_10_id_110["LED_on"] = "127"
		self.volume_10_id_110["LED_off"] = "0"
		self.volume_10_id_110["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_7"]
		self.volume_10_id_110["snap_to"] = True
		self.volume_10_id_110["json_id"] = 110
		self.volume_10_id_110["mapping_name"] = "Volume 10"
		self.volume_10_id_110["mapping_type"] = "Volume"
		self.volume_10_id_110["parent_json_id"] = 105
		self.volume_10_id_110["parent_name"] = "track_10_id_105"
		self.pan_10_id_111 = {}
		self.pan_10_id_111["attached_to"] = "midi_cc_ch_9_val_82"
		self.pan_10_id_111["track"] = self.track_num(2)
		self.pan_10_id_111["module"] = "self.song().tracks[self.track_num(9)].mixer_device.panning"
		self.pan_10_id_111["element"] = "value"
		self.pan_10_id_111["output_type"] = "val"
		self.pan_10_id_111["minimum"] = round(0,2)
		self.pan_10_id_111["maximum"] = round(100,2)
		self.pan_10_id_111["decimal_places"] = 2
		self.pan_10_id_111["ui_listener"] = "value"
		self.pan_10_id_111["feedback_brain"] = "feedback_range"
		self.pan_10_id_111["ctrl_type"] = "absolute"
		self.pan_10_id_111["takeover_mode"] = "None"
		self.pan_10_id_111["enc_first"] = 0
		self.pan_10_id_111["enc_second"] = 127
		self.pan_10_id_111["reverse_mode"] = False
		self.pan_10_id_111["LED_mapping_type_needs_feedback"] = "1"
		self.pan_10_id_111["LED_feedback"] = "default"
		self.pan_10_id_111["LED_feedback_active"] = "1"
		self.pan_10_id_111["LED_on"] = "127"
		self.pan_10_id_111["LED_off"] = "0"
		self.pan_10_id_111["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_82"]
		self.pan_10_id_111["snap_to"] = True
		self.pan_10_id_111["json_id"] = 111
		self.pan_10_id_111["mapping_name"] = "Pan 10"
		self.pan_10_id_111["mapping_type"] = "Pan"
		self.pan_10_id_111["parent_json_id"] = 105
		self.pan_10_id_111["parent_name"] = "track_10_id_105"
		self.mute_10_id_112 = {}
		self.mute_10_id_112["attached_to"] = "midi_cc_ch_9_val_94"
		self.mute_10_id_112["track"] = self.track_num(2)
		self.mute_10_id_112["module"] = "self.song().tracks[self.track_num(9)]"
		self.mute_10_id_112["element"] = "mute"
		self.mute_10_id_112["output_type"] = "bool"
		self.mute_10_id_112["ui_listener"] = "mute"
		self.mute_10_id_112["feedback_brain"] = "feedback_bool"
		self.mute_10_id_112["enc_first"] = 127
		self.mute_10_id_112["enc_second"] = 0
		self.mute_10_id_112["switch_type"] = "toggle"
		self.mute_10_id_112["ctrl_type"] = "on/off"
		self.mute_10_id_112["LED_mapping_type_needs_feedback"] = "1"
		self.mute_10_id_112["LED_feedback"] = "default"
		self.mute_10_id_112["LED_feedback_active"] = "1"
		self.mute_10_id_112["LED_on"] = "127"
		self.mute_10_id_112["LED_off"] = "0"
		self.mute_10_id_112["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_94"]
		self.mute_10_id_112["json_id"] = 112
		self.mute_10_id_112["mapping_name"] = "Mute 10"
		self.mute_10_id_112["mapping_type"] = "Mute"
		self.mute_10_id_112["parent_json_id"] = 105
		self.mute_10_id_112["parent_name"] = "track_10_id_105"
		self.track_11_id_114 = {}
		self.track_11_id_114["track"] = self.track_num(2)
		self.track_11_id_114["module"] = "self.song().tracks[self.track_num(10)]"
		self.track_11_id_114["LED_mapping_type_needs_feedback"] = ""
		self.track_11_id_114["LED_feedback"] = "custom"
		self.track_11_id_114["LED_feedback_active"] = ""
		self.track_11_id_114["LED_on"] = "127"
		self.track_11_id_114["LED_off"] = "0"
		self.track_11_id_114["LED_send_feedback_to_selected"] = []
		self.track_11_id_114["json_id"] = 114
		self.track_11_id_114["mapping_name"] = "Track 11"
		self.track_11_id_114["mapping_type"] = "Track"
		self.track_11_id_114["parent_json_id"] = 1
		self.track_11_id_114["parent_name"] = "mode_1_id_1"
		self.send_1_id_115 = {}
		self.send_1_id_115["attached_to"] = "midi_cc_ch_10_val_83"
		self.send_1_id_115["track"] = self.track_num(2)
		self.send_1_id_115["module"] = "self.song().tracks[self.track_num(10)].mixer_device.sends[0]"
		self.send_1_id_115["element"] = "value"
		self.send_1_id_115["output_type"] = "val"
		self.send_1_id_115["minimum"] = round(0,3)
		self.send_1_id_115["maximum"] = round(100,3)
		self.send_1_id_115["decimal_places"] = 3
		self.send_1_id_115["ui_listener"] = "value"
		self.send_1_id_115["feedback_brain"] = "feedback_range"
		self.send_1_id_115["ctrl_type"] = "absolute"
		self.send_1_id_115["takeover_mode"] = "None"
		self.send_1_id_115["enc_first"] = 0
		self.send_1_id_115["enc_second"] = 127
		self.send_1_id_115["reverse_mode"] = False
		self.send_1_id_115["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_115["LED_feedback"] = "default"
		self.send_1_id_115["LED_feedback_active"] = "1"
		self.send_1_id_115["LED_on"] = "127"
		self.send_1_id_115["LED_off"] = "0"
		self.send_1_id_115["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_83"]
		self.send_1_id_115["snap_to"] = True
		self.send_1_id_115["json_id"] = 115
		self.send_1_id_115["mapping_name"] = "Send 1"
		self.send_1_id_115["mapping_type"] = "Send"
		self.send_1_id_115["parent_json_id"] = 122
		self.send_1_id_115["parent_name"] = "sends_11_id_122"
		self.send_2_id_116 = {}
		self.send_2_id_116["attached_to"] = "midi_cc_ch_10_val_71"
		self.send_2_id_116["track"] = self.track_num(2)
		self.send_2_id_116["module"] = "self.song().tracks[self.track_num(10)].mixer_device.sends[1]"
		self.send_2_id_116["element"] = "value"
		self.send_2_id_116["output_type"] = "val"
		self.send_2_id_116["minimum"] = round(0,3)
		self.send_2_id_116["maximum"] = round(100,3)
		self.send_2_id_116["decimal_places"] = 3
		self.send_2_id_116["ui_listener"] = "value"
		self.send_2_id_116["feedback_brain"] = "feedback_range"
		self.send_2_id_116["ctrl_type"] = "absolute"
		self.send_2_id_116["takeover_mode"] = "None"
		self.send_2_id_116["enc_first"] = 0
		self.send_2_id_116["enc_second"] = 127
		self.send_2_id_116["reverse_mode"] = False
		self.send_2_id_116["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_116["LED_feedback"] = "default"
		self.send_2_id_116["LED_feedback_active"] = "1"
		self.send_2_id_116["LED_on"] = "127"
		self.send_2_id_116["LED_off"] = "0"
		self.send_2_id_116["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_71"]
		self.send_2_id_116["snap_to"] = True
		self.send_2_id_116["json_id"] = 116
		self.send_2_id_116["mapping_name"] = "Send 2"
		self.send_2_id_116["mapping_type"] = "Send"
		self.send_2_id_116["parent_json_id"] = 122
		self.send_2_id_116["parent_name"] = "sends_11_id_122"
		self.send_3_id_117 = {}
		self.send_3_id_117["attached_to"] = "midi_cc_ch_10_val_70"
		self.send_3_id_117["track"] = self.track_num(2)
		self.send_3_id_117["module"] = "self.song().tracks[self.track_num(10)].mixer_device.sends[2]"
		self.send_3_id_117["element"] = "value"
		self.send_3_id_117["output_type"] = "val"
		self.send_3_id_117["minimum"] = round(0,3)
		self.send_3_id_117["maximum"] = round(100,3)
		self.send_3_id_117["decimal_places"] = 3
		self.send_3_id_117["ui_listener"] = "value"
		self.send_3_id_117["feedback_brain"] = "feedback_range"
		self.send_3_id_117["ctrl_type"] = "absolute"
		self.send_3_id_117["takeover_mode"] = "None"
		self.send_3_id_117["enc_first"] = 0
		self.send_3_id_117["enc_second"] = 127
		self.send_3_id_117["reverse_mode"] = False
		self.send_3_id_117["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_117["LED_feedback"] = "default"
		self.send_3_id_117["LED_feedback_active"] = "1"
		self.send_3_id_117["LED_on"] = "127"
		self.send_3_id_117["LED_off"] = "0"
		self.send_3_id_117["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_70"]
		self.send_3_id_117["snap_to"] = True
		self.send_3_id_117["json_id"] = 117
		self.send_3_id_117["mapping_name"] = "Send 3"
		self.send_3_id_117["mapping_type"] = "Send"
		self.send_3_id_117["parent_json_id"] = 122
		self.send_3_id_117["parent_name"] = "sends_11_id_122"
		self.send_4_id_118 = {}
		self.send_4_id_118["attached_to"] = "midi_cc_ch_10_val_10"
		self.send_4_id_118["track"] = self.track_num(2)
		self.send_4_id_118["module"] = "self.song().tracks[self.track_num(10)].mixer_device.sends[3]"
		self.send_4_id_118["element"] = "value"
		self.send_4_id_118["output_type"] = "val"
		self.send_4_id_118["minimum"] = round(0,3)
		self.send_4_id_118["maximum"] = round(100,3)
		self.send_4_id_118["decimal_places"] = 3
		self.send_4_id_118["ui_listener"] = "value"
		self.send_4_id_118["feedback_brain"] = "feedback_range"
		self.send_4_id_118["ctrl_type"] = "absolute"
		self.send_4_id_118["takeover_mode"] = "None"
		self.send_4_id_118["enc_first"] = 0
		self.send_4_id_118["enc_second"] = 127
		self.send_4_id_118["reverse_mode"] = False
		self.send_4_id_118["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_118["LED_feedback"] = "default"
		self.send_4_id_118["LED_feedback_active"] = "1"
		self.send_4_id_118["LED_on"] = "127"
		self.send_4_id_118["LED_off"] = "0"
		self.send_4_id_118["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_10"]
		self.send_4_id_118["snap_to"] = True
		self.send_4_id_118["json_id"] = 118
		self.send_4_id_118["mapping_name"] = "Send 4"
		self.send_4_id_118["mapping_type"] = "Send"
		self.send_4_id_118["parent_json_id"] = 122
		self.send_4_id_118["parent_name"] = "sends_11_id_122"
		self.volume_11_id_119 = {}
		self.volume_11_id_119["attached_to"] = "midi_cc_ch_10_val_7"
		self.volume_11_id_119["track"] = self.track_num(2)
		self.volume_11_id_119["module"] = "self.song().tracks[self.track_num(10)].mixer_device.volume"
		self.volume_11_id_119["element"] = "value"
		self.volume_11_id_119["output_type"] = "val"
		self.volume_11_id_119["minimum"] = round(0,2)
		self.volume_11_id_119["maximum"] = round(85,2)
		self.volume_11_id_119["decimal_places"] = 2
		self.volume_11_id_119["ui_listener"] = "value"
		self.volume_11_id_119["feedback_brain"] = "feedback_range"
		self.volume_11_id_119["ctrl_type"] = "absolute"
		self.volume_11_id_119["takeover_mode"] = "None"
		self.volume_11_id_119["enc_first"] = 0
		self.volume_11_id_119["enc_second"] = 127
		self.volume_11_id_119["reverse_mode"] = False
		self.volume_11_id_119["LED_mapping_type_needs_feedback"] = "1"
		self.volume_11_id_119["LED_feedback"] = "default"
		self.volume_11_id_119["LED_feedback_active"] = "1"
		self.volume_11_id_119["LED_on"] = "127"
		self.volume_11_id_119["LED_off"] = "0"
		self.volume_11_id_119["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_7"]
		self.volume_11_id_119["snap_to"] = True
		self.volume_11_id_119["json_id"] = 119
		self.volume_11_id_119["mapping_name"] = "Volume 11"
		self.volume_11_id_119["mapping_type"] = "Volume"
		self.volume_11_id_119["parent_json_id"] = 114
		self.volume_11_id_119["parent_name"] = "track_11_id_114"
		self.pan_11_id_120 = {}
		self.pan_11_id_120["attached_to"] = "midi_cc_ch_10_val_82"
		self.pan_11_id_120["track"] = self.track_num(2)
		self.pan_11_id_120["module"] = "self.song().tracks[self.track_num(10)].mixer_device.panning"
		self.pan_11_id_120["element"] = "value"
		self.pan_11_id_120["output_type"] = "val"
		self.pan_11_id_120["minimum"] = round(0,2)
		self.pan_11_id_120["maximum"] = round(100,2)
		self.pan_11_id_120["decimal_places"] = 2
		self.pan_11_id_120["ui_listener"] = "value"
		self.pan_11_id_120["feedback_brain"] = "feedback_range"
		self.pan_11_id_120["ctrl_type"] = "absolute"
		self.pan_11_id_120["takeover_mode"] = "None"
		self.pan_11_id_120["enc_first"] = 0
		self.pan_11_id_120["enc_second"] = 127
		self.pan_11_id_120["reverse_mode"] = False
		self.pan_11_id_120["LED_mapping_type_needs_feedback"] = "1"
		self.pan_11_id_120["LED_feedback"] = "default"
		self.pan_11_id_120["LED_feedback_active"] = "1"
		self.pan_11_id_120["LED_on"] = "127"
		self.pan_11_id_120["LED_off"] = "0"
		self.pan_11_id_120["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_82"]
		self.pan_11_id_120["snap_to"] = True
		self.pan_11_id_120["json_id"] = 120
		self.pan_11_id_120["mapping_name"] = "Pan 11"
		self.pan_11_id_120["mapping_type"] = "Pan"
		self.pan_11_id_120["parent_json_id"] = 114
		self.pan_11_id_120["parent_name"] = "track_11_id_114"
		self.mute_11_id_121 = {}
		self.mute_11_id_121["attached_to"] = "midi_cc_ch_10_val_94"
		self.mute_11_id_121["track"] = self.track_num(2)
		self.mute_11_id_121["module"] = "self.song().tracks[self.track_num(10)]"
		self.mute_11_id_121["element"] = "mute"
		self.mute_11_id_121["output_type"] = "bool"
		self.mute_11_id_121["ui_listener"] = "mute"
		self.mute_11_id_121["feedback_brain"] = "feedback_bool"
		self.mute_11_id_121["enc_first"] = 127
		self.mute_11_id_121["enc_second"] = 0
		self.mute_11_id_121["switch_type"] = "toggle"
		self.mute_11_id_121["ctrl_type"] = "on/off"
		self.mute_11_id_121["LED_mapping_type_needs_feedback"] = "1"
		self.mute_11_id_121["LED_feedback"] = "default"
		self.mute_11_id_121["LED_feedback_active"] = "1"
		self.mute_11_id_121["LED_on"] = "127"
		self.mute_11_id_121["LED_off"] = "0"
		self.mute_11_id_121["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_94"]
		self.mute_11_id_121["json_id"] = 121
		self.mute_11_id_121["mapping_name"] = "Mute 11"
		self.mute_11_id_121["mapping_type"] = "Mute"
		self.mute_11_id_121["parent_json_id"] = 114
		self.mute_11_id_121["parent_name"] = "track_11_id_114"
		self.track_12_id_123 = {}
		self.track_12_id_123["track"] = self.track_num(2)
		self.track_12_id_123["module"] = "self.song().tracks[self.track_num(11)]"
		self.track_12_id_123["LED_mapping_type_needs_feedback"] = ""
		self.track_12_id_123["LED_feedback"] = "custom"
		self.track_12_id_123["LED_feedback_active"] = ""
		self.track_12_id_123["LED_on"] = "127"
		self.track_12_id_123["LED_off"] = "0"
		self.track_12_id_123["LED_send_feedback_to_selected"] = []
		self.track_12_id_123["json_id"] = 123
		self.track_12_id_123["mapping_name"] = "Track 12"
		self.track_12_id_123["mapping_type"] = "Track"
		self.track_12_id_123["parent_json_id"] = 1
		self.track_12_id_123["parent_name"] = "mode_1_id_1"
		self.send_1_id_124 = {}
		self.send_1_id_124["attached_to"] = "midi_cc_ch_11_val_83"
		self.send_1_id_124["track"] = self.track_num(2)
		self.send_1_id_124["module"] = "self.song().tracks[self.track_num(11)].mixer_device.sends[0]"
		self.send_1_id_124["element"] = "value"
		self.send_1_id_124["output_type"] = "val"
		self.send_1_id_124["minimum"] = round(0,3)
		self.send_1_id_124["maximum"] = round(100,3)
		self.send_1_id_124["decimal_places"] = 3
		self.send_1_id_124["ui_listener"] = "value"
		self.send_1_id_124["feedback_brain"] = "feedback_range"
		self.send_1_id_124["ctrl_type"] = "absolute"
		self.send_1_id_124["takeover_mode"] = "None"
		self.send_1_id_124["enc_first"] = 0
		self.send_1_id_124["enc_second"] = 127
		self.send_1_id_124["reverse_mode"] = False
		self.send_1_id_124["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_124["LED_feedback"] = "default"
		self.send_1_id_124["LED_feedback_active"] = "1"
		self.send_1_id_124["LED_on"] = "127"
		self.send_1_id_124["LED_off"] = "0"
		self.send_1_id_124["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_83"]
		self.send_1_id_124["snap_to"] = True
		self.send_1_id_124["json_id"] = 124
		self.send_1_id_124["mapping_name"] = "Send 1"
		self.send_1_id_124["mapping_type"] = "Send"
		self.send_1_id_124["parent_json_id"] = 131
		self.send_1_id_124["parent_name"] = "sends_12_id_131"
		self.send_2_id_125 = {}
		self.send_2_id_125["attached_to"] = "midi_cc_ch_11_val_71"
		self.send_2_id_125["track"] = self.track_num(2)
		self.send_2_id_125["module"] = "self.song().tracks[self.track_num(11)].mixer_device.sends[1]"
		self.send_2_id_125["element"] = "value"
		self.send_2_id_125["output_type"] = "val"
		self.send_2_id_125["minimum"] = round(0,3)
		self.send_2_id_125["maximum"] = round(100,3)
		self.send_2_id_125["decimal_places"] = 3
		self.send_2_id_125["ui_listener"] = "value"
		self.send_2_id_125["feedback_brain"] = "feedback_range"
		self.send_2_id_125["ctrl_type"] = "absolute"
		self.send_2_id_125["takeover_mode"] = "None"
		self.send_2_id_125["enc_first"] = 0
		self.send_2_id_125["enc_second"] = 127
		self.send_2_id_125["reverse_mode"] = False
		self.send_2_id_125["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_125["LED_feedback"] = "default"
		self.send_2_id_125["LED_feedback_active"] = "1"
		self.send_2_id_125["LED_on"] = "127"
		self.send_2_id_125["LED_off"] = "0"
		self.send_2_id_125["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_71"]
		self.send_2_id_125["snap_to"] = True
		self.send_2_id_125["json_id"] = 125
		self.send_2_id_125["mapping_name"] = "Send 2"
		self.send_2_id_125["mapping_type"] = "Send"
		self.send_2_id_125["parent_json_id"] = 131
		self.send_2_id_125["parent_name"] = "sends_12_id_131"
		self.send_3_id_126 = {}
		self.send_3_id_126["attached_to"] = "midi_cc_ch_11_val_70"
		self.send_3_id_126["track"] = self.track_num(2)
		self.send_3_id_126["module"] = "self.song().tracks[self.track_num(11)].mixer_device.sends[2]"
		self.send_3_id_126["element"] = "value"
		self.send_3_id_126["output_type"] = "val"
		self.send_3_id_126["minimum"] = round(0,3)
		self.send_3_id_126["maximum"] = round(100,3)
		self.send_3_id_126["decimal_places"] = 3
		self.send_3_id_126["ui_listener"] = "value"
		self.send_3_id_126["feedback_brain"] = "feedback_range"
		self.send_3_id_126["ctrl_type"] = "absolute"
		self.send_3_id_126["takeover_mode"] = "None"
		self.send_3_id_126["enc_first"] = 0
		self.send_3_id_126["enc_second"] = 127
		self.send_3_id_126["reverse_mode"] = False
		self.send_3_id_126["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_126["LED_feedback"] = "default"
		self.send_3_id_126["LED_feedback_active"] = "1"
		self.send_3_id_126["LED_on"] = "127"
		self.send_3_id_126["LED_off"] = "0"
		self.send_3_id_126["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_70"]
		self.send_3_id_126["snap_to"] = True
		self.send_3_id_126["json_id"] = 126
		self.send_3_id_126["mapping_name"] = "Send 3"
		self.send_3_id_126["mapping_type"] = "Send"
		self.send_3_id_126["parent_json_id"] = 131
		self.send_3_id_126["parent_name"] = "sends_12_id_131"
		self.send_4_id_127 = {}
		self.send_4_id_127["attached_to"] = "midi_cc_ch_11_val_10"
		self.send_4_id_127["track"] = self.track_num(2)
		self.send_4_id_127["module"] = "self.song().tracks[self.track_num(11)].mixer_device.sends[3]"
		self.send_4_id_127["element"] = "value"
		self.send_4_id_127["output_type"] = "val"
		self.send_4_id_127["minimum"] = round(0,3)
		self.send_4_id_127["maximum"] = round(100,3)
		self.send_4_id_127["decimal_places"] = 3
		self.send_4_id_127["ui_listener"] = "value"
		self.send_4_id_127["feedback_brain"] = "feedback_range"
		self.send_4_id_127["ctrl_type"] = "absolute"
		self.send_4_id_127["takeover_mode"] = "None"
		self.send_4_id_127["enc_first"] = 0
		self.send_4_id_127["enc_second"] = 127
		self.send_4_id_127["reverse_mode"] = False
		self.send_4_id_127["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_127["LED_feedback"] = "default"
		self.send_4_id_127["LED_feedback_active"] = "1"
		self.send_4_id_127["LED_on"] = "127"
		self.send_4_id_127["LED_off"] = "0"
		self.send_4_id_127["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_10"]
		self.send_4_id_127["snap_to"] = True
		self.send_4_id_127["json_id"] = 127
		self.send_4_id_127["mapping_name"] = "Send 4"
		self.send_4_id_127["mapping_type"] = "Send"
		self.send_4_id_127["parent_json_id"] = 131
		self.send_4_id_127["parent_name"] = "sends_12_id_131"
		self.volume_12_id_128 = {}
		self.volume_12_id_128["attached_to"] = "midi_cc_ch_11_val_7"
		self.volume_12_id_128["track"] = self.track_num(2)
		self.volume_12_id_128["module"] = "self.song().tracks[self.track_num(11)].mixer_device.volume"
		self.volume_12_id_128["element"] = "value"
		self.volume_12_id_128["output_type"] = "val"
		self.volume_12_id_128["minimum"] = round(0,2)
		self.volume_12_id_128["maximum"] = round(85,2)
		self.volume_12_id_128["decimal_places"] = 2
		self.volume_12_id_128["ui_listener"] = "value"
		self.volume_12_id_128["feedback_brain"] = "feedback_range"
		self.volume_12_id_128["ctrl_type"] = "absolute"
		self.volume_12_id_128["takeover_mode"] = "None"
		self.volume_12_id_128["enc_first"] = 0
		self.volume_12_id_128["enc_second"] = 127
		self.volume_12_id_128["reverse_mode"] = False
		self.volume_12_id_128["LED_mapping_type_needs_feedback"] = "1"
		self.volume_12_id_128["LED_feedback"] = "default"
		self.volume_12_id_128["LED_feedback_active"] = "1"
		self.volume_12_id_128["LED_on"] = "127"
		self.volume_12_id_128["LED_off"] = "0"
		self.volume_12_id_128["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_7"]
		self.volume_12_id_128["snap_to"] = True
		self.volume_12_id_128["json_id"] = 128
		self.volume_12_id_128["mapping_name"] = "Volume 12"
		self.volume_12_id_128["mapping_type"] = "Volume"
		self.volume_12_id_128["parent_json_id"] = 123
		self.volume_12_id_128["parent_name"] = "track_12_id_123"
		self.pan_12_id_129 = {}
		self.pan_12_id_129["attached_to"] = "midi_cc_ch_11_val_82"
		self.pan_12_id_129["track"] = self.track_num(2)
		self.pan_12_id_129["module"] = "self.song().tracks[self.track_num(11)].mixer_device.panning"
		self.pan_12_id_129["element"] = "value"
		self.pan_12_id_129["output_type"] = "val"
		self.pan_12_id_129["minimum"] = round(0,2)
		self.pan_12_id_129["maximum"] = round(100,2)
		self.pan_12_id_129["decimal_places"] = 2
		self.pan_12_id_129["ui_listener"] = "value"
		self.pan_12_id_129["feedback_brain"] = "feedback_range"
		self.pan_12_id_129["ctrl_type"] = "absolute"
		self.pan_12_id_129["takeover_mode"] = "None"
		self.pan_12_id_129["enc_first"] = 0
		self.pan_12_id_129["enc_second"] = 127
		self.pan_12_id_129["reverse_mode"] = False
		self.pan_12_id_129["LED_mapping_type_needs_feedback"] = "1"
		self.pan_12_id_129["LED_feedback"] = "default"
		self.pan_12_id_129["LED_feedback_active"] = "1"
		self.pan_12_id_129["LED_on"] = "127"
		self.pan_12_id_129["LED_off"] = "0"
		self.pan_12_id_129["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_82"]
		self.pan_12_id_129["snap_to"] = True
		self.pan_12_id_129["json_id"] = 129
		self.pan_12_id_129["mapping_name"] = "Pan 12"
		self.pan_12_id_129["mapping_type"] = "Pan"
		self.pan_12_id_129["parent_json_id"] = 123
		self.pan_12_id_129["parent_name"] = "track_12_id_123"
		self.mute_12_id_130 = {}
		self.mute_12_id_130["attached_to"] = "midi_cc_ch_11_val_94"
		self.mute_12_id_130["track"] = self.track_num(2)
		self.mute_12_id_130["module"] = "self.song().tracks[self.track_num(11)]"
		self.mute_12_id_130["element"] = "mute"
		self.mute_12_id_130["output_type"] = "bool"
		self.mute_12_id_130["ui_listener"] = "mute"
		self.mute_12_id_130["feedback_brain"] = "feedback_bool"
		self.mute_12_id_130["enc_first"] = 127
		self.mute_12_id_130["enc_second"] = 0
		self.mute_12_id_130["switch_type"] = "toggle"
		self.mute_12_id_130["ctrl_type"] = "on/off"
		self.mute_12_id_130["LED_mapping_type_needs_feedback"] = "1"
		self.mute_12_id_130["LED_feedback"] = "default"
		self.mute_12_id_130["LED_feedback_active"] = "1"
		self.mute_12_id_130["LED_on"] = "127"
		self.mute_12_id_130["LED_off"] = "0"
		self.mute_12_id_130["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_94"]
		self.mute_12_id_130["json_id"] = 130
		self.mute_12_id_130["mapping_name"] = "Mute 12"
		self.mute_12_id_130["mapping_type"] = "Mute"
		self.mute_12_id_130["parent_json_id"] = 123
		self.mute_12_id_130["parent_name"] = "track_12_id_123"
		self.track_13_id_132 = {}
		self.track_13_id_132["track"] = self.track_num(2)
		self.track_13_id_132["module"] = "self.song().tracks[self.track_num(12)]"
		self.track_13_id_132["LED_mapping_type_needs_feedback"] = ""
		self.track_13_id_132["LED_feedback"] = "custom"
		self.track_13_id_132["LED_feedback_active"] = ""
		self.track_13_id_132["LED_on"] = "127"
		self.track_13_id_132["LED_off"] = "0"
		self.track_13_id_132["LED_send_feedback_to_selected"] = []
		self.track_13_id_132["json_id"] = 132
		self.track_13_id_132["mapping_name"] = "Track 13"
		self.track_13_id_132["mapping_type"] = "Track"
		self.track_13_id_132["parent_json_id"] = 1
		self.track_13_id_132["parent_name"] = "mode_1_id_1"
		self.send_1_id_133 = {}
		self.send_1_id_133["attached_to"] = "midi_cc_ch_12_val_83"
		self.send_1_id_133["track"] = self.track_num(2)
		self.send_1_id_133["module"] = "self.song().tracks[self.track_num(12)].mixer_device.sends[0]"
		self.send_1_id_133["element"] = "value"
		self.send_1_id_133["output_type"] = "val"
		self.send_1_id_133["minimum"] = round(0,3)
		self.send_1_id_133["maximum"] = round(100,3)
		self.send_1_id_133["decimal_places"] = 3
		self.send_1_id_133["ui_listener"] = "value"
		self.send_1_id_133["feedback_brain"] = "feedback_range"
		self.send_1_id_133["ctrl_type"] = "absolute"
		self.send_1_id_133["takeover_mode"] = "None"
		self.send_1_id_133["enc_first"] = 0
		self.send_1_id_133["enc_second"] = 127
		self.send_1_id_133["reverse_mode"] = False
		self.send_1_id_133["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_133["LED_feedback"] = "default"
		self.send_1_id_133["LED_feedback_active"] = "1"
		self.send_1_id_133["LED_on"] = "127"
		self.send_1_id_133["LED_off"] = "0"
		self.send_1_id_133["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_83"]
		self.send_1_id_133["snap_to"] = True
		self.send_1_id_133["json_id"] = 133
		self.send_1_id_133["mapping_name"] = "Send 1"
		self.send_1_id_133["mapping_type"] = "Send"
		self.send_1_id_133["parent_json_id"] = 140
		self.send_1_id_133["parent_name"] = "sends_13_id_140"
		self.send_2_id_134 = {}
		self.send_2_id_134["attached_to"] = "midi_cc_ch_12_val_71"
		self.send_2_id_134["track"] = self.track_num(2)
		self.send_2_id_134["module"] = "self.song().tracks[self.track_num(12)].mixer_device.sends[1]"
		self.send_2_id_134["element"] = "value"
		self.send_2_id_134["output_type"] = "val"
		self.send_2_id_134["minimum"] = round(0,3)
		self.send_2_id_134["maximum"] = round(100,3)
		self.send_2_id_134["decimal_places"] = 3
		self.send_2_id_134["ui_listener"] = "value"
		self.send_2_id_134["feedback_brain"] = "feedback_range"
		self.send_2_id_134["ctrl_type"] = "absolute"
		self.send_2_id_134["takeover_mode"] = "None"
		self.send_2_id_134["enc_first"] = 0
		self.send_2_id_134["enc_second"] = 127
		self.send_2_id_134["reverse_mode"] = False
		self.send_2_id_134["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_134["LED_feedback"] = "default"
		self.send_2_id_134["LED_feedback_active"] = "1"
		self.send_2_id_134["LED_on"] = "127"
		self.send_2_id_134["LED_off"] = "0"
		self.send_2_id_134["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_71"]
		self.send_2_id_134["snap_to"] = True
		self.send_2_id_134["json_id"] = 134
		self.send_2_id_134["mapping_name"] = "Send 2"
		self.send_2_id_134["mapping_type"] = "Send"
		self.send_2_id_134["parent_json_id"] = 140
		self.send_2_id_134["parent_name"] = "sends_13_id_140"
		self.send_3_id_135 = {}
		self.send_3_id_135["attached_to"] = "midi_cc_ch_12_val_70"
		self.send_3_id_135["track"] = self.track_num(2)
		self.send_3_id_135["module"] = "self.song().tracks[self.track_num(12)].mixer_device.sends[2]"
		self.send_3_id_135["element"] = "value"
		self.send_3_id_135["output_type"] = "val"
		self.send_3_id_135["minimum"] = round(0,3)
		self.send_3_id_135["maximum"] = round(100,3)
		self.send_3_id_135["decimal_places"] = 3
		self.send_3_id_135["ui_listener"] = "value"
		self.send_3_id_135["feedback_brain"] = "feedback_range"
		self.send_3_id_135["ctrl_type"] = "absolute"
		self.send_3_id_135["takeover_mode"] = "None"
		self.send_3_id_135["enc_first"] = 0
		self.send_3_id_135["enc_second"] = 127
		self.send_3_id_135["reverse_mode"] = False
		self.send_3_id_135["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_135["LED_feedback"] = "default"
		self.send_3_id_135["LED_feedback_active"] = "1"
		self.send_3_id_135["LED_on"] = "127"
		self.send_3_id_135["LED_off"] = "0"
		self.send_3_id_135["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_70"]
		self.send_3_id_135["snap_to"] = True
		self.send_3_id_135["json_id"] = 135
		self.send_3_id_135["mapping_name"] = "Send 3"
		self.send_3_id_135["mapping_type"] = "Send"
		self.send_3_id_135["parent_json_id"] = 140
		self.send_3_id_135["parent_name"] = "sends_13_id_140"
		self.send_4_id_136 = {}
		self.send_4_id_136["attached_to"] = "midi_cc_ch_12_val_10"
		self.send_4_id_136["track"] = self.track_num(2)
		self.send_4_id_136["module"] = "self.song().tracks[self.track_num(12)].mixer_device.sends[3]"
		self.send_4_id_136["element"] = "value"
		self.send_4_id_136["output_type"] = "val"
		self.send_4_id_136["minimum"] = round(0,3)
		self.send_4_id_136["maximum"] = round(100,3)
		self.send_4_id_136["decimal_places"] = 3
		self.send_4_id_136["ui_listener"] = "value"
		self.send_4_id_136["feedback_brain"] = "feedback_range"
		self.send_4_id_136["ctrl_type"] = "absolute"
		self.send_4_id_136["takeover_mode"] = "None"
		self.send_4_id_136["enc_first"] = 0
		self.send_4_id_136["enc_second"] = 127
		self.send_4_id_136["reverse_mode"] = False
		self.send_4_id_136["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_136["LED_feedback"] = "default"
		self.send_4_id_136["LED_feedback_active"] = "1"
		self.send_4_id_136["LED_on"] = "127"
		self.send_4_id_136["LED_off"] = "0"
		self.send_4_id_136["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_10"]
		self.send_4_id_136["snap_to"] = True
		self.send_4_id_136["json_id"] = 136
		self.send_4_id_136["mapping_name"] = "Send 4"
		self.send_4_id_136["mapping_type"] = "Send"
		self.send_4_id_136["parent_json_id"] = 140
		self.send_4_id_136["parent_name"] = "sends_13_id_140"
		self.volume_13_id_137 = {}
		self.volume_13_id_137["attached_to"] = "midi_cc_ch_12_val_7"
		self.volume_13_id_137["track"] = self.track_num(2)
		self.volume_13_id_137["module"] = "self.song().tracks[self.track_num(12)].mixer_device.volume"
		self.volume_13_id_137["element"] = "value"
		self.volume_13_id_137["output_type"] = "val"
		self.volume_13_id_137["minimum"] = round(0,2)
		self.volume_13_id_137["maximum"] = round(85,2)
		self.volume_13_id_137["decimal_places"] = 2
		self.volume_13_id_137["ui_listener"] = "value"
		self.volume_13_id_137["feedback_brain"] = "feedback_range"
		self.volume_13_id_137["ctrl_type"] = "absolute"
		self.volume_13_id_137["takeover_mode"] = "None"
		self.volume_13_id_137["enc_first"] = 0
		self.volume_13_id_137["enc_second"] = 127
		self.volume_13_id_137["reverse_mode"] = False
		self.volume_13_id_137["LED_mapping_type_needs_feedback"] = "1"
		self.volume_13_id_137["LED_feedback"] = "default"
		self.volume_13_id_137["LED_feedback_active"] = "1"
		self.volume_13_id_137["LED_on"] = "127"
		self.volume_13_id_137["LED_off"] = "0"
		self.volume_13_id_137["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_7"]
		self.volume_13_id_137["snap_to"] = True
		self.volume_13_id_137["json_id"] = 137
		self.volume_13_id_137["mapping_name"] = "Volume 13"
		self.volume_13_id_137["mapping_type"] = "Volume"
		self.volume_13_id_137["parent_json_id"] = 132
		self.volume_13_id_137["parent_name"] = "track_13_id_132"
		self.pan_13_id_138 = {}
		self.pan_13_id_138["attached_to"] = "midi_cc_ch_12_val_82"
		self.pan_13_id_138["track"] = self.track_num(2)
		self.pan_13_id_138["module"] = "self.song().tracks[self.track_num(12)].mixer_device.panning"
		self.pan_13_id_138["element"] = "value"
		self.pan_13_id_138["output_type"] = "val"
		self.pan_13_id_138["minimum"] = round(0,2)
		self.pan_13_id_138["maximum"] = round(100,2)
		self.pan_13_id_138["decimal_places"] = 2
		self.pan_13_id_138["ui_listener"] = "value"
		self.pan_13_id_138["feedback_brain"] = "feedback_range"
		self.pan_13_id_138["ctrl_type"] = "absolute"
		self.pan_13_id_138["takeover_mode"] = "None"
		self.pan_13_id_138["enc_first"] = 0
		self.pan_13_id_138["enc_second"] = 127
		self.pan_13_id_138["reverse_mode"] = False
		self.pan_13_id_138["LED_mapping_type_needs_feedback"] = "1"
		self.pan_13_id_138["LED_feedback"] = "default"
		self.pan_13_id_138["LED_feedback_active"] = "1"
		self.pan_13_id_138["LED_on"] = "127"
		self.pan_13_id_138["LED_off"] = "0"
		self.pan_13_id_138["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_82"]
		self.pan_13_id_138["snap_to"] = True
		self.pan_13_id_138["json_id"] = 138
		self.pan_13_id_138["mapping_name"] = "Pan 13"
		self.pan_13_id_138["mapping_type"] = "Pan"
		self.pan_13_id_138["parent_json_id"] = 132
		self.pan_13_id_138["parent_name"] = "track_13_id_132"
		self.mute_13_id_139 = {}
		self.mute_13_id_139["attached_to"] = "midi_cc_ch_12_val_94"
		self.mute_13_id_139["track"] = self.track_num(2)
		self.mute_13_id_139["module"] = "self.song().tracks[self.track_num(12)]"
		self.mute_13_id_139["element"] = "mute"
		self.mute_13_id_139["output_type"] = "bool"
		self.mute_13_id_139["ui_listener"] = "mute"
		self.mute_13_id_139["feedback_brain"] = "feedback_bool"
		self.mute_13_id_139["enc_first"] = 127
		self.mute_13_id_139["enc_second"] = 0
		self.mute_13_id_139["switch_type"] = "toggle"
		self.mute_13_id_139["ctrl_type"] = "on/off"
		self.mute_13_id_139["LED_mapping_type_needs_feedback"] = "1"
		self.mute_13_id_139["LED_feedback"] = "default"
		self.mute_13_id_139["LED_feedback_active"] = "1"
		self.mute_13_id_139["LED_on"] = "127"
		self.mute_13_id_139["LED_off"] = "0"
		self.mute_13_id_139["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_94"]
		self.mute_13_id_139["json_id"] = 139
		self.mute_13_id_139["mapping_name"] = "Mute 13"
		self.mute_13_id_139["mapping_type"] = "Mute"
		self.mute_13_id_139["parent_json_id"] = 132
		self.mute_13_id_139["parent_name"] = "track_13_id_132"
		self.track_14_id_141 = {}
		self.track_14_id_141["track"] = self.track_num(2)
		self.track_14_id_141["module"] = "self.song().tracks[self.track_num(13)]"
		self.track_14_id_141["LED_mapping_type_needs_feedback"] = ""
		self.track_14_id_141["LED_feedback"] = "custom"
		self.track_14_id_141["LED_feedback_active"] = ""
		self.track_14_id_141["LED_on"] = "127"
		self.track_14_id_141["LED_off"] = "0"
		self.track_14_id_141["LED_send_feedback_to_selected"] = []
		self.track_14_id_141["json_id"] = 141
		self.track_14_id_141["mapping_name"] = "Track 14"
		self.track_14_id_141["mapping_type"] = "Track"
		self.track_14_id_141["parent_json_id"] = 1
		self.track_14_id_141["parent_name"] = "mode_1_id_1"
		self.send_1_id_142 = {}
		self.send_1_id_142["attached_to"] = "midi_cc_ch_13_val_83"
		self.send_1_id_142["track"] = self.track_num(2)
		self.send_1_id_142["module"] = "self.song().tracks[self.track_num(13)].mixer_device.sends[0]"
		self.send_1_id_142["element"] = "value"
		self.send_1_id_142["output_type"] = "val"
		self.send_1_id_142["minimum"] = round(0,3)
		self.send_1_id_142["maximum"] = round(100,3)
		self.send_1_id_142["decimal_places"] = 3
		self.send_1_id_142["ui_listener"] = "value"
		self.send_1_id_142["feedback_brain"] = "feedback_range"
		self.send_1_id_142["ctrl_type"] = "absolute"
		self.send_1_id_142["takeover_mode"] = "None"
		self.send_1_id_142["enc_first"] = 0
		self.send_1_id_142["enc_second"] = 127
		self.send_1_id_142["reverse_mode"] = False
		self.send_1_id_142["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_142["LED_feedback"] = "default"
		self.send_1_id_142["LED_feedback_active"] = "1"
		self.send_1_id_142["LED_on"] = "127"
		self.send_1_id_142["LED_off"] = "0"
		self.send_1_id_142["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_83"]
		self.send_1_id_142["snap_to"] = True
		self.send_1_id_142["json_id"] = 142
		self.send_1_id_142["mapping_name"] = "Send 1"
		self.send_1_id_142["mapping_type"] = "Send"
		self.send_1_id_142["parent_json_id"] = 149
		self.send_1_id_142["parent_name"] = "sends_14_id_149"
		self.send_2_id_143 = {}
		self.send_2_id_143["attached_to"] = "midi_cc_ch_13_val_71"
		self.send_2_id_143["track"] = self.track_num(2)
		self.send_2_id_143["module"] = "self.song().tracks[self.track_num(13)].mixer_device.sends[1]"
		self.send_2_id_143["element"] = "value"
		self.send_2_id_143["output_type"] = "val"
		self.send_2_id_143["minimum"] = round(0,3)
		self.send_2_id_143["maximum"] = round(100,3)
		self.send_2_id_143["decimal_places"] = 3
		self.send_2_id_143["ui_listener"] = "value"
		self.send_2_id_143["feedback_brain"] = "feedback_range"
		self.send_2_id_143["ctrl_type"] = "absolute"
		self.send_2_id_143["takeover_mode"] = "None"
		self.send_2_id_143["enc_first"] = 0
		self.send_2_id_143["enc_second"] = 127
		self.send_2_id_143["reverse_mode"] = False
		self.send_2_id_143["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_143["LED_feedback"] = "default"
		self.send_2_id_143["LED_feedback_active"] = "1"
		self.send_2_id_143["LED_on"] = "127"
		self.send_2_id_143["LED_off"] = "0"
		self.send_2_id_143["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_71"]
		self.send_2_id_143["snap_to"] = True
		self.send_2_id_143["json_id"] = 143
		self.send_2_id_143["mapping_name"] = "Send 2"
		self.send_2_id_143["mapping_type"] = "Send"
		self.send_2_id_143["parent_json_id"] = 149
		self.send_2_id_143["parent_name"] = "sends_14_id_149"
		self.send_3_id_144 = {}
		self.send_3_id_144["attached_to"] = "midi_cc_ch_13_val_70"
		self.send_3_id_144["track"] = self.track_num(2)
		self.send_3_id_144["module"] = "self.song().tracks[self.track_num(13)].mixer_device.sends[2]"
		self.send_3_id_144["element"] = "value"
		self.send_3_id_144["output_type"] = "val"
		self.send_3_id_144["minimum"] = round(0,3)
		self.send_3_id_144["maximum"] = round(100,3)
		self.send_3_id_144["decimal_places"] = 3
		self.send_3_id_144["ui_listener"] = "value"
		self.send_3_id_144["feedback_brain"] = "feedback_range"
		self.send_3_id_144["ctrl_type"] = "absolute"
		self.send_3_id_144["takeover_mode"] = "None"
		self.send_3_id_144["enc_first"] = 0
		self.send_3_id_144["enc_second"] = 127
		self.send_3_id_144["reverse_mode"] = False
		self.send_3_id_144["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_144["LED_feedback"] = "default"
		self.send_3_id_144["LED_feedback_active"] = "1"
		self.send_3_id_144["LED_on"] = "127"
		self.send_3_id_144["LED_off"] = "0"
		self.send_3_id_144["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_70"]
		self.send_3_id_144["snap_to"] = True
		self.send_3_id_144["json_id"] = 144
		self.send_3_id_144["mapping_name"] = "Send 3"
		self.send_3_id_144["mapping_type"] = "Send"
		self.send_3_id_144["parent_json_id"] = 149
		self.send_3_id_144["parent_name"] = "sends_14_id_149"
		self.send_4_id_145 = {}
		self.send_4_id_145["attached_to"] = "midi_cc_ch_13_val_10"
		self.send_4_id_145["track"] = self.track_num(2)
		self.send_4_id_145["module"] = "self.song().tracks[self.track_num(13)].mixer_device.sends[3]"
		self.send_4_id_145["element"] = "value"
		self.send_4_id_145["output_type"] = "val"
		self.send_4_id_145["minimum"] = round(0,3)
		self.send_4_id_145["maximum"] = round(100,3)
		self.send_4_id_145["decimal_places"] = 3
		self.send_4_id_145["ui_listener"] = "value"
		self.send_4_id_145["feedback_brain"] = "feedback_range"
		self.send_4_id_145["ctrl_type"] = "absolute"
		self.send_4_id_145["takeover_mode"] = "None"
		self.send_4_id_145["enc_first"] = 0
		self.send_4_id_145["enc_second"] = 127
		self.send_4_id_145["reverse_mode"] = False
		self.send_4_id_145["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_145["LED_feedback"] = "default"
		self.send_4_id_145["LED_feedback_active"] = "1"
		self.send_4_id_145["LED_on"] = "127"
		self.send_4_id_145["LED_off"] = "0"
		self.send_4_id_145["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_10"]
		self.send_4_id_145["snap_to"] = True
		self.send_4_id_145["json_id"] = 145
		self.send_4_id_145["mapping_name"] = "Send 4"
		self.send_4_id_145["mapping_type"] = "Send"
		self.send_4_id_145["parent_json_id"] = 149
		self.send_4_id_145["parent_name"] = "sends_14_id_149"
		self.volume_14_id_146 = {}
		self.volume_14_id_146["attached_to"] = "midi_cc_ch_13_val_7"
		self.volume_14_id_146["track"] = self.track_num(2)
		self.volume_14_id_146["module"] = "self.song().tracks[self.track_num(13)].mixer_device.volume"
		self.volume_14_id_146["element"] = "value"
		self.volume_14_id_146["output_type"] = "val"
		self.volume_14_id_146["minimum"] = round(0,2)
		self.volume_14_id_146["maximum"] = round(85,2)
		self.volume_14_id_146["decimal_places"] = 2
		self.volume_14_id_146["ui_listener"] = "value"
		self.volume_14_id_146["feedback_brain"] = "feedback_range"
		self.volume_14_id_146["ctrl_type"] = "absolute"
		self.volume_14_id_146["takeover_mode"] = "None"
		self.volume_14_id_146["enc_first"] = 0
		self.volume_14_id_146["enc_second"] = 127
		self.volume_14_id_146["reverse_mode"] = False
		self.volume_14_id_146["LED_mapping_type_needs_feedback"] = "1"
		self.volume_14_id_146["LED_feedback"] = "default"
		self.volume_14_id_146["LED_feedback_active"] = "1"
		self.volume_14_id_146["LED_on"] = "127"
		self.volume_14_id_146["LED_off"] = "0"
		self.volume_14_id_146["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_7"]
		self.volume_14_id_146["snap_to"] = True
		self.volume_14_id_146["json_id"] = 146
		self.volume_14_id_146["mapping_name"] = "Volume 14"
		self.volume_14_id_146["mapping_type"] = "Volume"
		self.volume_14_id_146["parent_json_id"] = 141
		self.volume_14_id_146["parent_name"] = "track_14_id_141"
		self.pan_14_id_147 = {}
		self.pan_14_id_147["attached_to"] = "midi_cc_ch_13_val_82"
		self.pan_14_id_147["track"] = self.track_num(2)
		self.pan_14_id_147["module"] = "self.song().tracks[self.track_num(13)].mixer_device.panning"
		self.pan_14_id_147["element"] = "value"
		self.pan_14_id_147["output_type"] = "val"
		self.pan_14_id_147["minimum"] = round(0,2)
		self.pan_14_id_147["maximum"] = round(100,2)
		self.pan_14_id_147["decimal_places"] = 2
		self.pan_14_id_147["ui_listener"] = "value"
		self.pan_14_id_147["feedback_brain"] = "feedback_range"
		self.pan_14_id_147["ctrl_type"] = "absolute"
		self.pan_14_id_147["takeover_mode"] = "None"
		self.pan_14_id_147["enc_first"] = 0
		self.pan_14_id_147["enc_second"] = 127
		self.pan_14_id_147["reverse_mode"] = False
		self.pan_14_id_147["LED_mapping_type_needs_feedback"] = "1"
		self.pan_14_id_147["LED_feedback"] = "default"
		self.pan_14_id_147["LED_feedback_active"] = "1"
		self.pan_14_id_147["LED_on"] = "127"
		self.pan_14_id_147["LED_off"] = "0"
		self.pan_14_id_147["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_82"]
		self.pan_14_id_147["snap_to"] = True
		self.pan_14_id_147["json_id"] = 147
		self.pan_14_id_147["mapping_name"] = "Pan 14"
		self.pan_14_id_147["mapping_type"] = "Pan"
		self.pan_14_id_147["parent_json_id"] = 141
		self.pan_14_id_147["parent_name"] = "track_14_id_141"
		self.mute_14_id_148 = {}
		self.mute_14_id_148["attached_to"] = "midi_cc_ch_13_val_94"
		self.mute_14_id_148["track"] = self.track_num(2)
		self.mute_14_id_148["module"] = "self.song().tracks[self.track_num(13)]"
		self.mute_14_id_148["element"] = "mute"
		self.mute_14_id_148["output_type"] = "bool"
		self.mute_14_id_148["ui_listener"] = "mute"
		self.mute_14_id_148["feedback_brain"] = "feedback_bool"
		self.mute_14_id_148["enc_first"] = 127
		self.mute_14_id_148["enc_second"] = 0
		self.mute_14_id_148["switch_type"] = "toggle"
		self.mute_14_id_148["ctrl_type"] = "on/off"
		self.mute_14_id_148["LED_mapping_type_needs_feedback"] = "1"
		self.mute_14_id_148["LED_feedback"] = "default"
		self.mute_14_id_148["LED_feedback_active"] = "1"
		self.mute_14_id_148["LED_on"] = "127"
		self.mute_14_id_148["LED_off"] = "0"
		self.mute_14_id_148["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_94"]
		self.mute_14_id_148["json_id"] = 148
		self.mute_14_id_148["mapping_name"] = "Mute 14"
		self.mute_14_id_148["mapping_type"] = "Mute"
		self.mute_14_id_148["parent_json_id"] = 141
		self.mute_14_id_148["parent_name"] = "track_14_id_141"
		self.track_15_id_150 = {}
		self.track_15_id_150["track"] = self.track_num(2)
		self.track_15_id_150["module"] = "self.song().tracks[self.track_num(14)]"
		self.track_15_id_150["LED_mapping_type_needs_feedback"] = ""
		self.track_15_id_150["LED_feedback"] = "custom"
		self.track_15_id_150["LED_feedback_active"] = ""
		self.track_15_id_150["LED_on"] = "127"
		self.track_15_id_150["LED_off"] = "0"
		self.track_15_id_150["LED_send_feedback_to_selected"] = []
		self.track_15_id_150["json_id"] = 150
		self.track_15_id_150["mapping_name"] = "Track 15"
		self.track_15_id_150["mapping_type"] = "Track"
		self.track_15_id_150["parent_json_id"] = 1
		self.track_15_id_150["parent_name"] = "mode_1_id_1"
		self.send_1_id_151 = {}
		self.send_1_id_151["attached_to"] = "midi_cc_ch_14_val_83"
		self.send_1_id_151["track"] = self.track_num(2)
		self.send_1_id_151["module"] = "self.song().tracks[self.track_num(14)].mixer_device.sends[0]"
		self.send_1_id_151["element"] = "value"
		self.send_1_id_151["output_type"] = "val"
		self.send_1_id_151["minimum"] = round(0,3)
		self.send_1_id_151["maximum"] = round(100,3)
		self.send_1_id_151["decimal_places"] = 3
		self.send_1_id_151["ui_listener"] = "value"
		self.send_1_id_151["feedback_brain"] = "feedback_range"
		self.send_1_id_151["ctrl_type"] = "absolute"
		self.send_1_id_151["takeover_mode"] = "None"
		self.send_1_id_151["enc_first"] = 0
		self.send_1_id_151["enc_second"] = 127
		self.send_1_id_151["reverse_mode"] = False
		self.send_1_id_151["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_151["LED_feedback"] = "default"
		self.send_1_id_151["LED_feedback_active"] = "1"
		self.send_1_id_151["LED_on"] = "127"
		self.send_1_id_151["LED_off"] = "0"
		self.send_1_id_151["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_83"]
		self.send_1_id_151["snap_to"] = True
		self.send_1_id_151["json_id"] = 151
		self.send_1_id_151["mapping_name"] = "Send 1"
		self.send_1_id_151["mapping_type"] = "Send"
		self.send_1_id_151["parent_json_id"] = 158
		self.send_1_id_151["parent_name"] = "sends_15_id_158"
		self.send_2_id_152 = {}
		self.send_2_id_152["attached_to"] = "midi_cc_ch_14_val_71"
		self.send_2_id_152["track"] = self.track_num(2)
		self.send_2_id_152["module"] = "self.song().tracks[self.track_num(14)].mixer_device.sends[1]"
		self.send_2_id_152["element"] = "value"
		self.send_2_id_152["output_type"] = "val"
		self.send_2_id_152["minimum"] = round(0,3)
		self.send_2_id_152["maximum"] = round(100,3)
		self.send_2_id_152["decimal_places"] = 3
		self.send_2_id_152["ui_listener"] = "value"
		self.send_2_id_152["feedback_brain"] = "feedback_range"
		self.send_2_id_152["ctrl_type"] = "absolute"
		self.send_2_id_152["takeover_mode"] = "None"
		self.send_2_id_152["enc_first"] = 0
		self.send_2_id_152["enc_second"] = 127
		self.send_2_id_152["reverse_mode"] = False
		self.send_2_id_152["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_152["LED_feedback"] = "default"
		self.send_2_id_152["LED_feedback_active"] = "1"
		self.send_2_id_152["LED_on"] = "127"
		self.send_2_id_152["LED_off"] = "0"
		self.send_2_id_152["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_71"]
		self.send_2_id_152["snap_to"] = True
		self.send_2_id_152["json_id"] = 152
		self.send_2_id_152["mapping_name"] = "Send 2"
		self.send_2_id_152["mapping_type"] = "Send"
		self.send_2_id_152["parent_json_id"] = 158
		self.send_2_id_152["parent_name"] = "sends_15_id_158"
		self.send_3_id_153 = {}
		self.send_3_id_153["attached_to"] = "midi_cc_ch_14_val_70"
		self.send_3_id_153["track"] = self.track_num(2)
		self.send_3_id_153["module"] = "self.song().tracks[self.track_num(14)].mixer_device.sends[2]"
		self.send_3_id_153["element"] = "value"
		self.send_3_id_153["output_type"] = "val"
		self.send_3_id_153["minimum"] = round(0,3)
		self.send_3_id_153["maximum"] = round(100,3)
		self.send_3_id_153["decimal_places"] = 3
		self.send_3_id_153["ui_listener"] = "value"
		self.send_3_id_153["feedback_brain"] = "feedback_range"
		self.send_3_id_153["ctrl_type"] = "absolute"
		self.send_3_id_153["takeover_mode"] = "None"
		self.send_3_id_153["enc_first"] = 0
		self.send_3_id_153["enc_second"] = 127
		self.send_3_id_153["reverse_mode"] = False
		self.send_3_id_153["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_153["LED_feedback"] = "default"
		self.send_3_id_153["LED_feedback_active"] = "1"
		self.send_3_id_153["LED_on"] = "127"
		self.send_3_id_153["LED_off"] = "0"
		self.send_3_id_153["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_70"]
		self.send_3_id_153["snap_to"] = True
		self.send_3_id_153["json_id"] = 153
		self.send_3_id_153["mapping_name"] = "Send 3"
		self.send_3_id_153["mapping_type"] = "Send"
		self.send_3_id_153["parent_json_id"] = 158
		self.send_3_id_153["parent_name"] = "sends_15_id_158"
		self.send_4_id_154 = {}
		self.send_4_id_154["attached_to"] = "midi_cc_ch_14_val_10"
		self.send_4_id_154["track"] = self.track_num(2)
		self.send_4_id_154["module"] = "self.song().tracks[self.track_num(14)].mixer_device.sends[3]"
		self.send_4_id_154["element"] = "value"
		self.send_4_id_154["output_type"] = "val"
		self.send_4_id_154["minimum"] = round(0,3)
		self.send_4_id_154["maximum"] = round(100,3)
		self.send_4_id_154["decimal_places"] = 3
		self.send_4_id_154["ui_listener"] = "value"
		self.send_4_id_154["feedback_brain"] = "feedback_range"
		self.send_4_id_154["ctrl_type"] = "absolute"
		self.send_4_id_154["takeover_mode"] = "None"
		self.send_4_id_154["enc_first"] = 0
		self.send_4_id_154["enc_second"] = 127
		self.send_4_id_154["reverse_mode"] = False
		self.send_4_id_154["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_154["LED_feedback"] = "default"
		self.send_4_id_154["LED_feedback_active"] = "1"
		self.send_4_id_154["LED_on"] = "127"
		self.send_4_id_154["LED_off"] = "0"
		self.send_4_id_154["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_10"]
		self.send_4_id_154["snap_to"] = True
		self.send_4_id_154["json_id"] = 154
		self.send_4_id_154["mapping_name"] = "Send 4"
		self.send_4_id_154["mapping_type"] = "Send"
		self.send_4_id_154["parent_json_id"] = 158
		self.send_4_id_154["parent_name"] = "sends_15_id_158"
		self.volume_15_id_155 = {}
		self.volume_15_id_155["attached_to"] = "midi_cc_ch_14_val_7"
		self.volume_15_id_155["track"] = self.track_num(2)
		self.volume_15_id_155["module"] = "self.song().tracks[self.track_num(14)].mixer_device.volume"
		self.volume_15_id_155["element"] = "value"
		self.volume_15_id_155["output_type"] = "val"
		self.volume_15_id_155["minimum"] = round(0,2)
		self.volume_15_id_155["maximum"] = round(85,2)
		self.volume_15_id_155["decimal_places"] = 2
		self.volume_15_id_155["ui_listener"] = "value"
		self.volume_15_id_155["feedback_brain"] = "feedback_range"
		self.volume_15_id_155["ctrl_type"] = "absolute"
		self.volume_15_id_155["takeover_mode"] = "None"
		self.volume_15_id_155["enc_first"] = 0
		self.volume_15_id_155["enc_second"] = 127
		self.volume_15_id_155["reverse_mode"] = False
		self.volume_15_id_155["LED_mapping_type_needs_feedback"] = "1"
		self.volume_15_id_155["LED_feedback"] = "default"
		self.volume_15_id_155["LED_feedback_active"] = "1"
		self.volume_15_id_155["LED_on"] = "127"
		self.volume_15_id_155["LED_off"] = "0"
		self.volume_15_id_155["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_7"]
		self.volume_15_id_155["snap_to"] = True
		self.volume_15_id_155["json_id"] = 155
		self.volume_15_id_155["mapping_name"] = "Volume 15"
		self.volume_15_id_155["mapping_type"] = "Volume"
		self.volume_15_id_155["parent_json_id"] = 150
		self.volume_15_id_155["parent_name"] = "track_15_id_150"
		self.pan_15_id_156 = {}
		self.pan_15_id_156["attached_to"] = "midi_cc_ch_14_val_82"
		self.pan_15_id_156["track"] = self.track_num(2)
		self.pan_15_id_156["module"] = "self.song().tracks[self.track_num(14)].mixer_device.panning"
		self.pan_15_id_156["element"] = "value"
		self.pan_15_id_156["output_type"] = "val"
		self.pan_15_id_156["minimum"] = round(0,2)
		self.pan_15_id_156["maximum"] = round(100,2)
		self.pan_15_id_156["decimal_places"] = 2
		self.pan_15_id_156["ui_listener"] = "value"
		self.pan_15_id_156["feedback_brain"] = "feedback_range"
		self.pan_15_id_156["ctrl_type"] = "absolute"
		self.pan_15_id_156["takeover_mode"] = "None"
		self.pan_15_id_156["enc_first"] = 0
		self.pan_15_id_156["enc_second"] = 127
		self.pan_15_id_156["reverse_mode"] = False
		self.pan_15_id_156["LED_mapping_type_needs_feedback"] = "1"
		self.pan_15_id_156["LED_feedback"] = "default"
		self.pan_15_id_156["LED_feedback_active"] = "1"
		self.pan_15_id_156["LED_on"] = "127"
		self.pan_15_id_156["LED_off"] = "0"
		self.pan_15_id_156["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_82"]
		self.pan_15_id_156["snap_to"] = True
		self.pan_15_id_156["json_id"] = 156
		self.pan_15_id_156["mapping_name"] = "Pan 15"
		self.pan_15_id_156["mapping_type"] = "Pan"
		self.pan_15_id_156["parent_json_id"] = 150
		self.pan_15_id_156["parent_name"] = "track_15_id_150"
		self.mute_15_id_157 = {}
		self.mute_15_id_157["attached_to"] = "midi_cc_ch_14_val_94"
		self.mute_15_id_157["track"] = self.track_num(2)
		self.mute_15_id_157["module"] = "self.song().tracks[self.track_num(14)]"
		self.mute_15_id_157["element"] = "mute"
		self.mute_15_id_157["output_type"] = "bool"
		self.mute_15_id_157["ui_listener"] = "mute"
		self.mute_15_id_157["feedback_brain"] = "feedback_bool"
		self.mute_15_id_157["enc_first"] = 127
		self.mute_15_id_157["enc_second"] = 0
		self.mute_15_id_157["switch_type"] = "toggle"
		self.mute_15_id_157["ctrl_type"] = "on/off"
		self.mute_15_id_157["LED_mapping_type_needs_feedback"] = "1"
		self.mute_15_id_157["LED_feedback"] = "default"
		self.mute_15_id_157["LED_feedback_active"] = "1"
		self.mute_15_id_157["LED_on"] = "127"
		self.mute_15_id_157["LED_off"] = "0"
		self.mute_15_id_157["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_94"]
		self.mute_15_id_157["json_id"] = 157
		self.mute_15_id_157["mapping_name"] = "Mute 15"
		self.mute_15_id_157["mapping_type"] = "Mute"
		self.mute_15_id_157["parent_json_id"] = 150
		self.mute_15_id_157["parent_name"] = "track_15_id_150"
		self.track_16_id_159 = {}
		self.track_16_id_159["track"] = self.track_num(2)
		self.track_16_id_159["module"] = "self.song().tracks[self.track_num(15)]"
		self.track_16_id_159["LED_mapping_type_needs_feedback"] = ""
		self.track_16_id_159["LED_feedback"] = "custom"
		self.track_16_id_159["LED_feedback_active"] = ""
		self.track_16_id_159["LED_on"] = "127"
		self.track_16_id_159["LED_off"] = "0"
		self.track_16_id_159["LED_send_feedback_to_selected"] = []
		self.track_16_id_159["json_id"] = 159
		self.track_16_id_159["mapping_name"] = "Track 16"
		self.track_16_id_159["mapping_type"] = "Track"
		self.track_16_id_159["parent_json_id"] = 1
		self.track_16_id_159["parent_name"] = "mode_1_id_1"
		self.send_1_id_160 = {}
		self.send_1_id_160["attached_to"] = "midi_cc_ch_15_val_83"
		self.send_1_id_160["track"] = self.track_num(2)
		self.send_1_id_160["module"] = "self.song().tracks[self.track_num(15)].mixer_device.sends[0]"
		self.send_1_id_160["element"] = "value"
		self.send_1_id_160["output_type"] = "val"
		self.send_1_id_160["minimum"] = round(0,3)
		self.send_1_id_160["maximum"] = round(100,3)
		self.send_1_id_160["decimal_places"] = 3
		self.send_1_id_160["ui_listener"] = "value"
		self.send_1_id_160["feedback_brain"] = "feedback_range"
		self.send_1_id_160["ctrl_type"] = "absolute"
		self.send_1_id_160["takeover_mode"] = "None"
		self.send_1_id_160["enc_first"] = 0
		self.send_1_id_160["enc_second"] = 127
		self.send_1_id_160["reverse_mode"] = False
		self.send_1_id_160["LED_mapping_type_needs_feedback"] = "1"
		self.send_1_id_160["LED_feedback"] = "default"
		self.send_1_id_160["LED_feedback_active"] = "1"
		self.send_1_id_160["LED_on"] = "127"
		self.send_1_id_160["LED_off"] = "0"
		self.send_1_id_160["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_83"]
		self.send_1_id_160["snap_to"] = True
		self.send_1_id_160["json_id"] = 160
		self.send_1_id_160["mapping_name"] = "Send 1"
		self.send_1_id_160["mapping_type"] = "Send"
		self.send_1_id_160["parent_json_id"] = 167
		self.send_1_id_160["parent_name"] = "sends_16_id_167"
		self.send_2_id_161 = {}
		self.send_2_id_161["attached_to"] = "midi_cc_ch_15_val_71"
		self.send_2_id_161["track"] = self.track_num(2)
		self.send_2_id_161["module"] = "self.song().tracks[self.track_num(15)].mixer_device.sends[1]"
		self.send_2_id_161["element"] = "value"
		self.send_2_id_161["output_type"] = "val"
		self.send_2_id_161["minimum"] = round(0,3)
		self.send_2_id_161["maximum"] = round(100,3)
		self.send_2_id_161["decimal_places"] = 3
		self.send_2_id_161["ui_listener"] = "value"
		self.send_2_id_161["feedback_brain"] = "feedback_range"
		self.send_2_id_161["ctrl_type"] = "absolute"
		self.send_2_id_161["takeover_mode"] = "None"
		self.send_2_id_161["enc_first"] = 0
		self.send_2_id_161["enc_second"] = 127
		self.send_2_id_161["reverse_mode"] = False
		self.send_2_id_161["LED_mapping_type_needs_feedback"] = "1"
		self.send_2_id_161["LED_feedback"] = "default"
		self.send_2_id_161["LED_feedback_active"] = "1"
		self.send_2_id_161["LED_on"] = "127"
		self.send_2_id_161["LED_off"] = "0"
		self.send_2_id_161["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_71"]
		self.send_2_id_161["snap_to"] = True
		self.send_2_id_161["json_id"] = 161
		self.send_2_id_161["mapping_name"] = "Send 2"
		self.send_2_id_161["mapping_type"] = "Send"
		self.send_2_id_161["parent_json_id"] = 167
		self.send_2_id_161["parent_name"] = "sends_16_id_167"
		self.send_3_id_162 = {}
		self.send_3_id_162["attached_to"] = "midi_cc_ch_15_val_70"
		self.send_3_id_162["track"] = self.track_num(2)
		self.send_3_id_162["module"] = "self.song().tracks[self.track_num(15)].mixer_device.sends[2]"
		self.send_3_id_162["element"] = "value"
		self.send_3_id_162["output_type"] = "val"
		self.send_3_id_162["minimum"] = round(0,3)
		self.send_3_id_162["maximum"] = round(100,3)
		self.send_3_id_162["decimal_places"] = 3
		self.send_3_id_162["ui_listener"] = "value"
		self.send_3_id_162["feedback_brain"] = "feedback_range"
		self.send_3_id_162["ctrl_type"] = "absolute"
		self.send_3_id_162["takeover_mode"] = "None"
		self.send_3_id_162["enc_first"] = 0
		self.send_3_id_162["enc_second"] = 127
		self.send_3_id_162["reverse_mode"] = False
		self.send_3_id_162["LED_mapping_type_needs_feedback"] = "1"
		self.send_3_id_162["LED_feedback"] = "default"
		self.send_3_id_162["LED_feedback_active"] = "1"
		self.send_3_id_162["LED_on"] = "127"
		self.send_3_id_162["LED_off"] = "0"
		self.send_3_id_162["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_70"]
		self.send_3_id_162["snap_to"] = True
		self.send_3_id_162["json_id"] = 162
		self.send_3_id_162["mapping_name"] = "Send 3"
		self.send_3_id_162["mapping_type"] = "Send"
		self.send_3_id_162["parent_json_id"] = 167
		self.send_3_id_162["parent_name"] = "sends_16_id_167"
		self.send_4_id_163 = {}
		self.send_4_id_163["attached_to"] = "midi_cc_ch_15_val_10"
		self.send_4_id_163["track"] = self.track_num(2)
		self.send_4_id_163["module"] = "self.song().tracks[self.track_num(15)].mixer_device.sends[3]"
		self.send_4_id_163["element"] = "value"
		self.send_4_id_163["output_type"] = "val"
		self.send_4_id_163["minimum"] = round(0,3)
		self.send_4_id_163["maximum"] = round(100,3)
		self.send_4_id_163["decimal_places"] = 3
		self.send_4_id_163["ui_listener"] = "value"
		self.send_4_id_163["feedback_brain"] = "feedback_range"
		self.send_4_id_163["ctrl_type"] = "absolute"
		self.send_4_id_163["takeover_mode"] = "None"
		self.send_4_id_163["enc_first"] = 0
		self.send_4_id_163["enc_second"] = 127
		self.send_4_id_163["reverse_mode"] = False
		self.send_4_id_163["LED_mapping_type_needs_feedback"] = "1"
		self.send_4_id_163["LED_feedback"] = "default"
		self.send_4_id_163["LED_feedback_active"] = "1"
		self.send_4_id_163["LED_on"] = "127"
		self.send_4_id_163["LED_off"] = "0"
		self.send_4_id_163["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_10"]
		self.send_4_id_163["snap_to"] = True
		self.send_4_id_163["json_id"] = 163
		self.send_4_id_163["mapping_name"] = "Send 4"
		self.send_4_id_163["mapping_type"] = "Send"
		self.send_4_id_163["parent_json_id"] = 167
		self.send_4_id_163["parent_name"] = "sends_16_id_167"
		self.volume_16_id_164 = {}
		self.volume_16_id_164["attached_to"] = "midi_cc_ch_15_val_7"
		self.volume_16_id_164["track"] = self.track_num(2)
		self.volume_16_id_164["module"] = "self.song().tracks[self.track_num(15)].mixer_device.volume"
		self.volume_16_id_164["element"] = "value"
		self.volume_16_id_164["output_type"] = "val"
		self.volume_16_id_164["minimum"] = round(0,2)
		self.volume_16_id_164["maximum"] = round(85,2)
		self.volume_16_id_164["decimal_places"] = 2
		self.volume_16_id_164["ui_listener"] = "value"
		self.volume_16_id_164["feedback_brain"] = "feedback_range"
		self.volume_16_id_164["ctrl_type"] = "absolute"
		self.volume_16_id_164["takeover_mode"] = "None"
		self.volume_16_id_164["enc_first"] = 0
		self.volume_16_id_164["enc_second"] = 127
		self.volume_16_id_164["reverse_mode"] = False
		self.volume_16_id_164["LED_mapping_type_needs_feedback"] = "1"
		self.volume_16_id_164["LED_feedback"] = "default"
		self.volume_16_id_164["LED_feedback_active"] = "1"
		self.volume_16_id_164["LED_on"] = "127"
		self.volume_16_id_164["LED_off"] = "0"
		self.volume_16_id_164["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_7"]
		self.volume_16_id_164["snap_to"] = True
		self.volume_16_id_164["json_id"] = 164
		self.volume_16_id_164["mapping_name"] = "Volume 16"
		self.volume_16_id_164["mapping_type"] = "Volume"
		self.volume_16_id_164["parent_json_id"] = 159
		self.volume_16_id_164["parent_name"] = "track_16_id_159"
		self.pan_16_id_165 = {}
		self.pan_16_id_165["attached_to"] = "midi_cc_ch_15_val_82"
		self.pan_16_id_165["track"] = self.track_num(2)
		self.pan_16_id_165["module"] = "self.song().tracks[self.track_num(15)].mixer_device.panning"
		self.pan_16_id_165["element"] = "value"
		self.pan_16_id_165["output_type"] = "val"
		self.pan_16_id_165["minimum"] = round(0,2)
		self.pan_16_id_165["maximum"] = round(100,2)
		self.pan_16_id_165["decimal_places"] = 2
		self.pan_16_id_165["ui_listener"] = "value"
		self.pan_16_id_165["feedback_brain"] = "feedback_range"
		self.pan_16_id_165["ctrl_type"] = "absolute"
		self.pan_16_id_165["takeover_mode"] = "None"
		self.pan_16_id_165["enc_first"] = 0
		self.pan_16_id_165["enc_second"] = 127
		self.pan_16_id_165["reverse_mode"] = False
		self.pan_16_id_165["LED_mapping_type_needs_feedback"] = "1"
		self.pan_16_id_165["LED_feedback"] = "default"
		self.pan_16_id_165["LED_feedback_active"] = "1"
		self.pan_16_id_165["LED_on"] = "127"
		self.pan_16_id_165["LED_off"] = "0"
		self.pan_16_id_165["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_82"]
		self.pan_16_id_165["snap_to"] = True
		self.pan_16_id_165["json_id"] = 165
		self.pan_16_id_165["mapping_name"] = "Pan 16"
		self.pan_16_id_165["mapping_type"] = "Pan"
		self.pan_16_id_165["parent_json_id"] = 159
		self.pan_16_id_165["parent_name"] = "track_16_id_159"
		self.mute_16_id_166 = {}
		self.mute_16_id_166["attached_to"] = "midi_cc_ch_15_val_94"
		self.mute_16_id_166["track"] = self.track_num(2)
		self.mute_16_id_166["module"] = "self.song().tracks[self.track_num(15)]"
		self.mute_16_id_166["element"] = "mute"
		self.mute_16_id_166["output_type"] = "bool"
		self.mute_16_id_166["ui_listener"] = "mute"
		self.mute_16_id_166["feedback_brain"] = "feedback_bool"
		self.mute_16_id_166["enc_first"] = 127
		self.mute_16_id_166["enc_second"] = 0
		self.mute_16_id_166["switch_type"] = "toggle"
		self.mute_16_id_166["ctrl_type"] = "on/off"
		self.mute_16_id_166["LED_mapping_type_needs_feedback"] = "1"
		self.mute_16_id_166["LED_feedback"] = "default"
		self.mute_16_id_166["LED_feedback_active"] = "1"
		self.mute_16_id_166["LED_on"] = "127"
		self.mute_16_id_166["LED_off"] = "0"
		self.mute_16_id_166["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_94"]
		self.mute_16_id_166["json_id"] = 166
		self.mute_16_id_166["mapping_name"] = "Mute 16"
		self.mute_16_id_166["mapping_type"] = "Mute"
		self.mute_16_id_166["parent_json_id"] = 159
		self.mute_16_id_166["parent_name"] = "track_16_id_159"
		self.mode_selector_1_id_168 = {}
		self.mode_selector_1_id_168["attached_to"] = "midi_cc_ch_15_val_120"
		self.mode_selector_1_id_168["module"] = "self"
		self.mode_selector_1_id_168["element"] = "scroll_modes"
		self.mode_selector_1_id_168["output_type"] = "func"
		self.mode_selector_1_id_168["func_arg"] = "cnfg"
		self.mode_selector_1_id_168["ui_listener"] = "value"
		self.mode_selector_1_id_168["feedback_brain"] = "feedback_scroll_mode_selector"
		self.mode_selector_1_id_168["ctrl_type"] = "absolute"
		self.mode_selector_1_id_168["takeover_mode"] = "Value scaling"
		self.mode_selector_1_id_168["enc_first"] = 0
		self.mode_selector_1_id_168["enc_second"] = 127
		self.mode_selector_1_id_168["reverse_mode"] = False
		self.mode_selector_1_id_168["steps"] = 1
		self.mode_selector_1_id_168["LED_mapping_type_needs_feedback"] = "1"
		self.mode_selector_1_id_168["LED_feedback"] = "default"
		self.mode_selector_1_id_168["LED_feedback_active"] = "1"
		self.mode_selector_1_id_168["LED_on"] = "127"
		self.mode_selector_1_id_168["LED_off"] = "0"
		self.mode_selector_1_id_168["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_120"]
		self.mode_selector_1_id_168["json_id"] = 168
		self.mode_selector_1_id_168["mapping_name"] = "Mode Selector 1"
		self.mode_selector_1_id_168["mapping_type"] = "Mode Selector"
		self.mode_selector_1_id_168["parent_json_id"] = 1
		self.mode_selector_1_id_168["parent_name"] = "mode_1_id_1"
		self.session_box_navigation_1_copy_id_347 = {}
		self.session_box_navigation_1_copy_id_347["attached_to"] = "midi_cc_ch_15_val_121"
		self.session_box_navigation_1_copy_id_347["module"] = "self"
		self.session_box_navigation_1_copy_id_347["element"] = "scroll_sess_offset"
		self.session_box_navigation_1_copy_id_347["output_type"] = "func"
		self.session_box_navigation_1_copy_id_347["func_arg"] = "cnfg"
		self.session_box_navigation_1_copy_id_347["tracks_scenes"] = "tracks"
		self.session_box_navigation_1_copy_id_347["ui_listener"] = "offset"
		self.session_box_navigation_1_copy_id_347["feedback_brain"] = "feedback_sessbox_nav"
		self.session_box_navigation_1_copy_id_347["ctrl_type"] = "relative"
		self.session_box_navigation_1_copy_id_347["enc_first"] = 0
		self.session_box_navigation_1_copy_id_347["enc_second"] = 127
		self.session_box_navigation_1_copy_id_347["steps"] = 8
		self.session_box_navigation_1_copy_id_347["LED_mapping_type_needs_feedback"] = "1"
		self.session_box_navigation_1_copy_id_347["LED_feedback"] = "default"
		self.session_box_navigation_1_copy_id_347["LED_feedback_active"] = "1"
		self.session_box_navigation_1_copy_id_347["LED_on"] = "127"
		self.session_box_navigation_1_copy_id_347["LED_off"] = "0"
		self.session_box_navigation_1_copy_id_347["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_121"]
		self.session_box_navigation_1_copy_id_347["json_id"] = 347
		self.session_box_navigation_1_copy_id_347["mapping_name"] = "Session Box Navigation 1 copy"
		self.session_box_navigation_1_copy_id_347["mapping_type"] = "Session Box Navigation"
		self.session_box_navigation_1_copy_id_347["parent_json_id"] = 1
		self.session_box_navigation_1_copy_id_347["parent_name"] = "mode_1_id_1"

	def _mode169_configs(self):
		self.mode_169_configs_map = [
			"volume_1_id_174",
			"pan_1_id_175",
			"volume_2_id_182",
			"pan_2_id_183",
			"volume_3_id_190",
			"pan_3_id_191",
			"volume_4_id_198",
			"pan_4_id_199",
			"volume_5_id_206",
			"pan_5_id_207",
			"volume_6_id_214",
			"pan_6_id_215",
			"volume_7_id_222",
			"pan_7_id_223",
			"volume_8_id_230",
			"pan_8_id_231",
			"parameter_1_id_234",
			"parameter_2_id_235",
			"parameter_3_id_236",
			"parameter_4_id_237",
			"parameter_5_id_238",
			"parameter_6_id_239",
			"parameter_7_id_240",
			"parameter_8_id_241",
			"parameter_bank_1_id_242",
			"device_1_id_243",
			"volume_9_id_248",
			"pan_9_id_249",
			"volume_10_id_256",
			"pan_10_id_257",
			"volume_11_id_264",
			"pan_11_id_265",
			"volume_12_id_272",
			"pan_12_id_273",
			"volume_13_id_280",
			"pan_13_id_281",
			"volume_14_id_288",
			"pan_14_id_289",
			"volume_15_id_296",
			"pan_15_id_297",
			"volume_16_id_304",
			"pan_16_id_305",
			"track_1_id_308",
			"track_2_id_309",
			"track_3_id_310",
			"track_4_id_311",
			"track_5_id_312",
			"track_6_id_313",
			"track_7_id_314",
			"track_8_id_315",
			"track_select_id_318",
			"track_9_id_319",
			"track_10_id_320",
			"track_11_id_321",
			"track_12_id_322",
			"track_13_id_323",
			"track_14_id_324",
			"track_15_id_325",
			"track_16_id_326",
			"solo_1_id_328",
			"solo_2_id_329",
			"solo_3_id_330",
			"solo_4_id_331",
			"solo_5_id_332",
			"solo_6_id_333",
			"solo_7_id_334",
			"solo_8_id_335",
			"solo_9_id_336",
			"solo_10_id_337",
			"solo_11_id_338",
			"solo_12_id_339",
			"solo_13_id_340",
			"solo_14_id_341",
			"solo_15_id_342",
			"solo_16_id_343",
			"mode_selector_1_copy_id_346"]
		self.volume_1_id_174 = {}
		self.volume_1_id_174["attached_to"] = "midi_cc_ch_0_val_7"
		self.volume_1_id_174["track"] = self.track_num(2)
		self.volume_1_id_174["module"] = "self.song().tracks[self.track_num(0)].mixer_device.volume"
		self.volume_1_id_174["element"] = "value"
		self.volume_1_id_174["output_type"] = "val"
		self.volume_1_id_174["minimum"] = round(0,2)
		self.volume_1_id_174["maximum"] = round(85,2)
		self.volume_1_id_174["decimal_places"] = 2
		self.volume_1_id_174["ui_listener"] = "value"
		self.volume_1_id_174["feedback_brain"] = "feedback_range"
		self.volume_1_id_174["ctrl_type"] = "absolute"
		self.volume_1_id_174["takeover_mode"] = "None"
		self.volume_1_id_174["enc_first"] = 0
		self.volume_1_id_174["enc_second"] = 127
		self.volume_1_id_174["reverse_mode"] = False
		self.volume_1_id_174["LED_mapping_type_needs_feedback"] = "1"
		self.volume_1_id_174["LED_feedback"] = "default"
		self.volume_1_id_174["LED_feedback_active"] = "1"
		self.volume_1_id_174["LED_on"] = "127"
		self.volume_1_id_174["LED_off"] = "0"
		self.volume_1_id_174["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_7"]
		self.volume_1_id_174["snap_to"] = True
		self.volume_1_id_174["json_id"] = 174
		self.volume_1_id_174["mapping_name"] = "Volume 1"
		self.volume_1_id_174["mapping_type"] = "Volume"
		self.volume_1_id_174["parent_json_id"] = 308
		self.volume_1_id_174["parent_name"] = "track_1_id_308"
		self.pan_1_id_175 = {}
		self.pan_1_id_175["attached_to"] = "midi_cc_ch_0_val_82"
		self.pan_1_id_175["track"] = self.track_num(2)
		self.pan_1_id_175["module"] = "self.song().tracks[self.track_num(0)].mixer_device.panning"
		self.pan_1_id_175["element"] = "value"
		self.pan_1_id_175["output_type"] = "val"
		self.pan_1_id_175["minimum"] = round(0,2)
		self.pan_1_id_175["maximum"] = round(100,2)
		self.pan_1_id_175["decimal_places"] = 2
		self.pan_1_id_175["ui_listener"] = "value"
		self.pan_1_id_175["feedback_brain"] = "feedback_range"
		self.pan_1_id_175["ctrl_type"] = "absolute"
		self.pan_1_id_175["takeover_mode"] = "Value scaling"
		self.pan_1_id_175["enc_first"] = 0
		self.pan_1_id_175["enc_second"] = 127
		self.pan_1_id_175["reverse_mode"] = False
		self.pan_1_id_175["LED_mapping_type_needs_feedback"] = "1"
		self.pan_1_id_175["LED_feedback"] = "default"
		self.pan_1_id_175["LED_feedback_active"] = "1"
		self.pan_1_id_175["LED_on"] = "127"
		self.pan_1_id_175["LED_off"] = "0"
		self.pan_1_id_175["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_82"]
		self.pan_1_id_175["snap_to"] = True
		self.pan_1_id_175["json_id"] = 175
		self.pan_1_id_175["mapping_name"] = "Pan 1"
		self.pan_1_id_175["mapping_type"] = "Pan"
		self.pan_1_id_175["parent_json_id"] = 308
		self.pan_1_id_175["parent_name"] = "track_1_id_308"
		self.volume_2_id_182 = {}
		self.volume_2_id_182["attached_to"] = "midi_cc_ch_1_val_7"
		self.volume_2_id_182["track"] = self.track_num(2)
		self.volume_2_id_182["module"] = "self.song().tracks[self.track_num(1)].mixer_device.volume"
		self.volume_2_id_182["element"] = "value"
		self.volume_2_id_182["output_type"] = "val"
		self.volume_2_id_182["minimum"] = round(0,2)
		self.volume_2_id_182["maximum"] = round(85,2)
		self.volume_2_id_182["decimal_places"] = 2
		self.volume_2_id_182["ui_listener"] = "value"
		self.volume_2_id_182["feedback_brain"] = "feedback_range"
		self.volume_2_id_182["ctrl_type"] = "absolute"
		self.volume_2_id_182["takeover_mode"] = "None"
		self.volume_2_id_182["enc_first"] = 0
		self.volume_2_id_182["enc_second"] = 127
		self.volume_2_id_182["reverse_mode"] = False
		self.volume_2_id_182["LED_mapping_type_needs_feedback"] = "1"
		self.volume_2_id_182["LED_feedback"] = "default"
		self.volume_2_id_182["LED_feedback_active"] = "1"
		self.volume_2_id_182["LED_on"] = "127"
		self.volume_2_id_182["LED_off"] = "0"
		self.volume_2_id_182["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_7"]
		self.volume_2_id_182["snap_to"] = True
		self.volume_2_id_182["json_id"] = 182
		self.volume_2_id_182["mapping_name"] = "Volume 2"
		self.volume_2_id_182["mapping_type"] = "Volume"
		self.volume_2_id_182["parent_json_id"] = 309
		self.volume_2_id_182["parent_name"] = "track_2_id_309"
		self.pan_2_id_183 = {}
		self.pan_2_id_183["attached_to"] = "midi_cc_ch_1_val_82"
		self.pan_2_id_183["track"] = self.track_num(2)
		self.pan_2_id_183["module"] = "self.song().tracks[self.track_num(1)].mixer_device.panning"
		self.pan_2_id_183["element"] = "value"
		self.pan_2_id_183["output_type"] = "val"
		self.pan_2_id_183["minimum"] = round(0,2)
		self.pan_2_id_183["maximum"] = round(100,2)
		self.pan_2_id_183["decimal_places"] = 2
		self.pan_2_id_183["ui_listener"] = "value"
		self.pan_2_id_183["feedback_brain"] = "feedback_range"
		self.pan_2_id_183["ctrl_type"] = "absolute"
		self.pan_2_id_183["takeover_mode"] = "Value scaling"
		self.pan_2_id_183["enc_first"] = 0
		self.pan_2_id_183["enc_second"] = 127
		self.pan_2_id_183["reverse_mode"] = False
		self.pan_2_id_183["LED_mapping_type_needs_feedback"] = "1"
		self.pan_2_id_183["LED_feedback"] = "default"
		self.pan_2_id_183["LED_feedback_active"] = "1"
		self.pan_2_id_183["LED_on"] = "127"
		self.pan_2_id_183["LED_off"] = "0"
		self.pan_2_id_183["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_82"]
		self.pan_2_id_183["snap_to"] = True
		self.pan_2_id_183["json_id"] = 183
		self.pan_2_id_183["mapping_name"] = "Pan 2"
		self.pan_2_id_183["mapping_type"] = "Pan"
		self.pan_2_id_183["parent_json_id"] = 309
		self.pan_2_id_183["parent_name"] = "track_2_id_309"
		self.volume_3_id_190 = {}
		self.volume_3_id_190["attached_to"] = "midi_cc_ch_2_val_7"
		self.volume_3_id_190["track"] = self.track_num(2)
		self.volume_3_id_190["module"] = "self.song().tracks[self.track_num(2)].mixer_device.volume"
		self.volume_3_id_190["element"] = "value"
		self.volume_3_id_190["output_type"] = "val"
		self.volume_3_id_190["minimum"] = round(0,2)
		self.volume_3_id_190["maximum"] = round(85,2)
		self.volume_3_id_190["decimal_places"] = 2
		self.volume_3_id_190["ui_listener"] = "value"
		self.volume_3_id_190["feedback_brain"] = "feedback_range"
		self.volume_3_id_190["ctrl_type"] = "absolute"
		self.volume_3_id_190["takeover_mode"] = "None"
		self.volume_3_id_190["enc_first"] = 0
		self.volume_3_id_190["enc_second"] = 127
		self.volume_3_id_190["reverse_mode"] = False
		self.volume_3_id_190["LED_mapping_type_needs_feedback"] = "1"
		self.volume_3_id_190["LED_feedback"] = "default"
		self.volume_3_id_190["LED_feedback_active"] = "1"
		self.volume_3_id_190["LED_on"] = "127"
		self.volume_3_id_190["LED_off"] = "0"
		self.volume_3_id_190["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_7"]
		self.volume_3_id_190["snap_to"] = True
		self.volume_3_id_190["json_id"] = 190
		self.volume_3_id_190["mapping_name"] = "Volume 3"
		self.volume_3_id_190["mapping_type"] = "Volume"
		self.volume_3_id_190["parent_json_id"] = 310
		self.volume_3_id_190["parent_name"] = "track_3_id_310"
		self.pan_3_id_191 = {}
		self.pan_3_id_191["attached_to"] = "midi_cc_ch_2_val_82"
		self.pan_3_id_191["track"] = self.track_num(2)
		self.pan_3_id_191["module"] = "self.song().tracks[self.track_num(2)].mixer_device.panning"
		self.pan_3_id_191["element"] = "value"
		self.pan_3_id_191["output_type"] = "val"
		self.pan_3_id_191["minimum"] = round(0,2)
		self.pan_3_id_191["maximum"] = round(100,2)
		self.pan_3_id_191["decimal_places"] = 2
		self.pan_3_id_191["ui_listener"] = "value"
		self.pan_3_id_191["feedback_brain"] = "feedback_range"
		self.pan_3_id_191["ctrl_type"] = "absolute"
		self.pan_3_id_191["takeover_mode"] = "Value scaling"
		self.pan_3_id_191["enc_first"] = 0
		self.pan_3_id_191["enc_second"] = 127
		self.pan_3_id_191["reverse_mode"] = False
		self.pan_3_id_191["LED_mapping_type_needs_feedback"] = "1"
		self.pan_3_id_191["LED_feedback"] = "default"
		self.pan_3_id_191["LED_feedback_active"] = "1"
		self.pan_3_id_191["LED_on"] = "127"
		self.pan_3_id_191["LED_off"] = "0"
		self.pan_3_id_191["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_82"]
		self.pan_3_id_191["snap_to"] = True
		self.pan_3_id_191["json_id"] = 191
		self.pan_3_id_191["mapping_name"] = "Pan 3"
		self.pan_3_id_191["mapping_type"] = "Pan"
		self.pan_3_id_191["parent_json_id"] = 310
		self.pan_3_id_191["parent_name"] = "track_3_id_310"
		self.volume_4_id_198 = {}
		self.volume_4_id_198["attached_to"] = "midi_cc_ch_3_val_7"
		self.volume_4_id_198["track"] = self.track_num(2)
		self.volume_4_id_198["module"] = "self.song().tracks[self.track_num(3)].mixer_device.volume"
		self.volume_4_id_198["element"] = "value"
		self.volume_4_id_198["output_type"] = "val"
		self.volume_4_id_198["minimum"] = round(0,2)
		self.volume_4_id_198["maximum"] = round(85,2)
		self.volume_4_id_198["decimal_places"] = 2
		self.volume_4_id_198["ui_listener"] = "value"
		self.volume_4_id_198["feedback_brain"] = "feedback_range"
		self.volume_4_id_198["ctrl_type"] = "absolute"
		self.volume_4_id_198["takeover_mode"] = "None"
		self.volume_4_id_198["enc_first"] = 0
		self.volume_4_id_198["enc_second"] = 127
		self.volume_4_id_198["reverse_mode"] = False
		self.volume_4_id_198["LED_mapping_type_needs_feedback"] = "1"
		self.volume_4_id_198["LED_feedback"] = "default"
		self.volume_4_id_198["LED_feedback_active"] = "1"
		self.volume_4_id_198["LED_on"] = "127"
		self.volume_4_id_198["LED_off"] = "0"
		self.volume_4_id_198["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_7"]
		self.volume_4_id_198["snap_to"] = True
		self.volume_4_id_198["json_id"] = 198
		self.volume_4_id_198["mapping_name"] = "Volume 4"
		self.volume_4_id_198["mapping_type"] = "Volume"
		self.volume_4_id_198["parent_json_id"] = 311
		self.volume_4_id_198["parent_name"] = "track_4_id_311"
		self.pan_4_id_199 = {}
		self.pan_4_id_199["attached_to"] = "midi_cc_ch_3_val_82"
		self.pan_4_id_199["track"] = self.track_num(2)
		self.pan_4_id_199["module"] = "self.song().tracks[self.track_num(3)].mixer_device.panning"
		self.pan_4_id_199["element"] = "value"
		self.pan_4_id_199["output_type"] = "val"
		self.pan_4_id_199["minimum"] = round(0,2)
		self.pan_4_id_199["maximum"] = round(100,2)
		self.pan_4_id_199["decimal_places"] = 2
		self.pan_4_id_199["ui_listener"] = "value"
		self.pan_4_id_199["feedback_brain"] = "feedback_range"
		self.pan_4_id_199["ctrl_type"] = "absolute"
		self.pan_4_id_199["takeover_mode"] = "Value scaling"
		self.pan_4_id_199["enc_first"] = 0
		self.pan_4_id_199["enc_second"] = 127
		self.pan_4_id_199["reverse_mode"] = False
		self.pan_4_id_199["LED_mapping_type_needs_feedback"] = "1"
		self.pan_4_id_199["LED_feedback"] = "default"
		self.pan_4_id_199["LED_feedback_active"] = "1"
		self.pan_4_id_199["LED_on"] = "127"
		self.pan_4_id_199["LED_off"] = "0"
		self.pan_4_id_199["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_82"]
		self.pan_4_id_199["snap_to"] = True
		self.pan_4_id_199["json_id"] = 199
		self.pan_4_id_199["mapping_name"] = "Pan 4"
		self.pan_4_id_199["mapping_type"] = "Pan"
		self.pan_4_id_199["parent_json_id"] = 311
		self.pan_4_id_199["parent_name"] = "track_4_id_311"
		self.volume_5_id_206 = {}
		self.volume_5_id_206["attached_to"] = "midi_cc_ch_4_val_7"
		self.volume_5_id_206["track"] = self.track_num(2)
		self.volume_5_id_206["module"] = "self.song().tracks[self.track_num(4)].mixer_device.volume"
		self.volume_5_id_206["element"] = "value"
		self.volume_5_id_206["output_type"] = "val"
		self.volume_5_id_206["minimum"] = round(0,2)
		self.volume_5_id_206["maximum"] = round(85,2)
		self.volume_5_id_206["decimal_places"] = 2
		self.volume_5_id_206["ui_listener"] = "value"
		self.volume_5_id_206["feedback_brain"] = "feedback_range"
		self.volume_5_id_206["ctrl_type"] = "absolute"
		self.volume_5_id_206["takeover_mode"] = "None"
		self.volume_5_id_206["enc_first"] = 0
		self.volume_5_id_206["enc_second"] = 127
		self.volume_5_id_206["reverse_mode"] = False
		self.volume_5_id_206["LED_mapping_type_needs_feedback"] = "1"
		self.volume_5_id_206["LED_feedback"] = "default"
		self.volume_5_id_206["LED_feedback_active"] = "1"
		self.volume_5_id_206["LED_on"] = "127"
		self.volume_5_id_206["LED_off"] = "0"
		self.volume_5_id_206["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_7"]
		self.volume_5_id_206["snap_to"] = True
		self.volume_5_id_206["json_id"] = 206
		self.volume_5_id_206["mapping_name"] = "Volume 5"
		self.volume_5_id_206["mapping_type"] = "Volume"
		self.volume_5_id_206["parent_json_id"] = 312
		self.volume_5_id_206["parent_name"] = "track_5_id_312"
		self.pan_5_id_207 = {}
		self.pan_5_id_207["attached_to"] = "midi_cc_ch_4_val_82"
		self.pan_5_id_207["track"] = self.track_num(2)
		self.pan_5_id_207["module"] = "self.song().tracks[self.track_num(4)].mixer_device.panning"
		self.pan_5_id_207["element"] = "value"
		self.pan_5_id_207["output_type"] = "val"
		self.pan_5_id_207["minimum"] = round(0,2)
		self.pan_5_id_207["maximum"] = round(100,2)
		self.pan_5_id_207["decimal_places"] = 2
		self.pan_5_id_207["ui_listener"] = "value"
		self.pan_5_id_207["feedback_brain"] = "feedback_range"
		self.pan_5_id_207["ctrl_type"] = "absolute"
		self.pan_5_id_207["takeover_mode"] = "Value scaling"
		self.pan_5_id_207["enc_first"] = 0
		self.pan_5_id_207["enc_second"] = 127
		self.pan_5_id_207["reverse_mode"] = False
		self.pan_5_id_207["LED_mapping_type_needs_feedback"] = "1"
		self.pan_5_id_207["LED_feedback"] = "default"
		self.pan_5_id_207["LED_feedback_active"] = "1"
		self.pan_5_id_207["LED_on"] = "127"
		self.pan_5_id_207["LED_off"] = "0"
		self.pan_5_id_207["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_82"]
		self.pan_5_id_207["snap_to"] = True
		self.pan_5_id_207["json_id"] = 207
		self.pan_5_id_207["mapping_name"] = "Pan 5"
		self.pan_5_id_207["mapping_type"] = "Pan"
		self.pan_5_id_207["parent_json_id"] = 312
		self.pan_5_id_207["parent_name"] = "track_5_id_312"
		self.volume_6_id_214 = {}
		self.volume_6_id_214["attached_to"] = "midi_cc_ch_5_val_7"
		self.volume_6_id_214["track"] = self.track_num(2)
		self.volume_6_id_214["module"] = "self.song().tracks[self.track_num(5)].mixer_device.volume"
		self.volume_6_id_214["element"] = "value"
		self.volume_6_id_214["output_type"] = "val"
		self.volume_6_id_214["minimum"] = round(0,2)
		self.volume_6_id_214["maximum"] = round(85,2)
		self.volume_6_id_214["decimal_places"] = 2
		self.volume_6_id_214["ui_listener"] = "value"
		self.volume_6_id_214["feedback_brain"] = "feedback_range"
		self.volume_6_id_214["ctrl_type"] = "absolute"
		self.volume_6_id_214["takeover_mode"] = "None"
		self.volume_6_id_214["enc_first"] = 0
		self.volume_6_id_214["enc_second"] = 127
		self.volume_6_id_214["reverse_mode"] = False
		self.volume_6_id_214["LED_mapping_type_needs_feedback"] = "1"
		self.volume_6_id_214["LED_feedback"] = "default"
		self.volume_6_id_214["LED_feedback_active"] = "1"
		self.volume_6_id_214["LED_on"] = "127"
		self.volume_6_id_214["LED_off"] = "0"
		self.volume_6_id_214["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_7"]
		self.volume_6_id_214["snap_to"] = True
		self.volume_6_id_214["json_id"] = 214
		self.volume_6_id_214["mapping_name"] = "Volume 6"
		self.volume_6_id_214["mapping_type"] = "Volume"
		self.volume_6_id_214["parent_json_id"] = 313
		self.volume_6_id_214["parent_name"] = "track_6_id_313"
		self.pan_6_id_215 = {}
		self.pan_6_id_215["attached_to"] = "midi_cc_ch_5_val_82"
		self.pan_6_id_215["track"] = self.track_num(2)
		self.pan_6_id_215["module"] = "self.song().tracks[self.track_num(5)].mixer_device.panning"
		self.pan_6_id_215["element"] = "value"
		self.pan_6_id_215["output_type"] = "val"
		self.pan_6_id_215["minimum"] = round(0,2)
		self.pan_6_id_215["maximum"] = round(100,2)
		self.pan_6_id_215["decimal_places"] = 2
		self.pan_6_id_215["ui_listener"] = "value"
		self.pan_6_id_215["feedback_brain"] = "feedback_range"
		self.pan_6_id_215["ctrl_type"] = "absolute"
		self.pan_6_id_215["takeover_mode"] = "Value scaling"
		self.pan_6_id_215["enc_first"] = 0
		self.pan_6_id_215["enc_second"] = 127
		self.pan_6_id_215["reverse_mode"] = False
		self.pan_6_id_215["LED_mapping_type_needs_feedback"] = "1"
		self.pan_6_id_215["LED_feedback"] = "default"
		self.pan_6_id_215["LED_feedback_active"] = "1"
		self.pan_6_id_215["LED_on"] = "127"
		self.pan_6_id_215["LED_off"] = "0"
		self.pan_6_id_215["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_82"]
		self.pan_6_id_215["snap_to"] = True
		self.pan_6_id_215["json_id"] = 215
		self.pan_6_id_215["mapping_name"] = "Pan 6"
		self.pan_6_id_215["mapping_type"] = "Pan"
		self.pan_6_id_215["parent_json_id"] = 313
		self.pan_6_id_215["parent_name"] = "track_6_id_313"
		self.volume_7_id_222 = {}
		self.volume_7_id_222["attached_to"] = "midi_cc_ch_6_val_7"
		self.volume_7_id_222["track"] = self.track_num(2)
		self.volume_7_id_222["module"] = "self.song().tracks[self.track_num(6)].mixer_device.volume"
		self.volume_7_id_222["element"] = "value"
		self.volume_7_id_222["output_type"] = "val"
		self.volume_7_id_222["minimum"] = round(0,2)
		self.volume_7_id_222["maximum"] = round(85,2)
		self.volume_7_id_222["decimal_places"] = 2
		self.volume_7_id_222["ui_listener"] = "value"
		self.volume_7_id_222["feedback_brain"] = "feedback_range"
		self.volume_7_id_222["ctrl_type"] = "absolute"
		self.volume_7_id_222["takeover_mode"] = "None"
		self.volume_7_id_222["enc_first"] = 0
		self.volume_7_id_222["enc_second"] = 127
		self.volume_7_id_222["reverse_mode"] = False
		self.volume_7_id_222["LED_mapping_type_needs_feedback"] = "1"
		self.volume_7_id_222["LED_feedback"] = "default"
		self.volume_7_id_222["LED_feedback_active"] = "1"
		self.volume_7_id_222["LED_on"] = "127"
		self.volume_7_id_222["LED_off"] = "0"
		self.volume_7_id_222["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_7"]
		self.volume_7_id_222["snap_to"] = True
		self.volume_7_id_222["json_id"] = 222
		self.volume_7_id_222["mapping_name"] = "Volume 7"
		self.volume_7_id_222["mapping_type"] = "Volume"
		self.volume_7_id_222["parent_json_id"] = 314
		self.volume_7_id_222["parent_name"] = "track_7_id_314"
		self.pan_7_id_223 = {}
		self.pan_7_id_223["attached_to"] = "midi_cc_ch_6_val_82"
		self.pan_7_id_223["track"] = self.track_num(2)
		self.pan_7_id_223["module"] = "self.song().tracks[self.track_num(6)].mixer_device.panning"
		self.pan_7_id_223["element"] = "value"
		self.pan_7_id_223["output_type"] = "val"
		self.pan_7_id_223["minimum"] = round(0,2)
		self.pan_7_id_223["maximum"] = round(100,2)
		self.pan_7_id_223["decimal_places"] = 2
		self.pan_7_id_223["ui_listener"] = "value"
		self.pan_7_id_223["feedback_brain"] = "feedback_range"
		self.pan_7_id_223["ctrl_type"] = "absolute"
		self.pan_7_id_223["takeover_mode"] = "Value scaling"
		self.pan_7_id_223["enc_first"] = 0
		self.pan_7_id_223["enc_second"] = 127
		self.pan_7_id_223["reverse_mode"] = False
		self.pan_7_id_223["LED_mapping_type_needs_feedback"] = "1"
		self.pan_7_id_223["LED_feedback"] = "default"
		self.pan_7_id_223["LED_feedback_active"] = "1"
		self.pan_7_id_223["LED_on"] = "127"
		self.pan_7_id_223["LED_off"] = "0"
		self.pan_7_id_223["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_82"]
		self.pan_7_id_223["snap_to"] = True
		self.pan_7_id_223["json_id"] = 223
		self.pan_7_id_223["mapping_name"] = "Pan 7"
		self.pan_7_id_223["mapping_type"] = "Pan"
		self.pan_7_id_223["parent_json_id"] = 314
		self.pan_7_id_223["parent_name"] = "track_7_id_314"
		self.volume_8_id_230 = {}
		self.volume_8_id_230["attached_to"] = "midi_cc_ch_7_val_7"
		self.volume_8_id_230["track"] = self.track_num(2)
		self.volume_8_id_230["module"] = "self.song().tracks[self.track_num(7)].mixer_device.volume"
		self.volume_8_id_230["element"] = "value"
		self.volume_8_id_230["output_type"] = "val"
		self.volume_8_id_230["minimum"] = round(0,2)
		self.volume_8_id_230["maximum"] = round(85,2)
		self.volume_8_id_230["decimal_places"] = 2
		self.volume_8_id_230["ui_listener"] = "value"
		self.volume_8_id_230["feedback_brain"] = "feedback_range"
		self.volume_8_id_230["ctrl_type"] = "absolute"
		self.volume_8_id_230["takeover_mode"] = "None"
		self.volume_8_id_230["enc_first"] = 0
		self.volume_8_id_230["enc_second"] = 127
		self.volume_8_id_230["reverse_mode"] = False
		self.volume_8_id_230["LED_mapping_type_needs_feedback"] = "1"
		self.volume_8_id_230["LED_feedback"] = "default"
		self.volume_8_id_230["LED_feedback_active"] = "1"
		self.volume_8_id_230["LED_on"] = "127"
		self.volume_8_id_230["LED_off"] = "0"
		self.volume_8_id_230["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_7"]
		self.volume_8_id_230["snap_to"] = True
		self.volume_8_id_230["json_id"] = 230
		self.volume_8_id_230["mapping_name"] = "Volume 8"
		self.volume_8_id_230["mapping_type"] = "Volume"
		self.volume_8_id_230["parent_json_id"] = 315
		self.volume_8_id_230["parent_name"] = "track_8_id_315"
		self.pan_8_id_231 = {}
		self.pan_8_id_231["attached_to"] = "midi_cc_ch_7_val_82"
		self.pan_8_id_231["track"] = self.track_num(2)
		self.pan_8_id_231["module"] = "self.song().tracks[self.track_num(7)].mixer_device.panning"
		self.pan_8_id_231["element"] = "value"
		self.pan_8_id_231["output_type"] = "val"
		self.pan_8_id_231["minimum"] = round(0,2)
		self.pan_8_id_231["maximum"] = round(100,2)
		self.pan_8_id_231["decimal_places"] = 2
		self.pan_8_id_231["ui_listener"] = "value"
		self.pan_8_id_231["feedback_brain"] = "feedback_range"
		self.pan_8_id_231["ctrl_type"] = "absolute"
		self.pan_8_id_231["takeover_mode"] = "Value scaling"
		self.pan_8_id_231["enc_first"] = 0
		self.pan_8_id_231["enc_second"] = 127
		self.pan_8_id_231["reverse_mode"] = False
		self.pan_8_id_231["LED_mapping_type_needs_feedback"] = "1"
		self.pan_8_id_231["LED_feedback"] = "default"
		self.pan_8_id_231["LED_feedback_active"] = "1"
		self.pan_8_id_231["LED_on"] = "127"
		self.pan_8_id_231["LED_off"] = "0"
		self.pan_8_id_231["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_82"]
		self.pan_8_id_231["snap_to"] = True
		self.pan_8_id_231["json_id"] = 231
		self.pan_8_id_231["mapping_name"] = "Pan 8"
		self.pan_8_id_231["mapping_type"] = "Pan"
		self.pan_8_id_231["parent_json_id"] = 315
		self.pan_8_id_231["parent_name"] = "track_8_id_315"
		self.parameter_1_id_234 = {}
		self.parameter_1_id_234["attached_to"] = "midi_cc_ch_15_val_85"
		self.parameter_1_id_234["track"] = self.track_num(2)
		self.parameter_1_id_234["module"] = "self.song().view.selected_track.devices[0].parameters[1]"
		self.parameter_1_id_234["element"] = "value"
		self.parameter_1_id_234["output_type"] = "val"
		self.parameter_1_id_234["minimum"] = round(0,2)
		self.parameter_1_id_234["maximum"] = round(100,2)
		self.parameter_1_id_234["decimal_places"] = 2
		self.parameter_1_id_234["ui_listener"] = "value"
		self.parameter_1_id_234["feedback_brain"] = "feedback_range"
		self.parameter_1_id_234["ctrl_type"] = "absolute"
		self.parameter_1_id_234["takeover_mode"] = "Value scaling"
		self.parameter_1_id_234["enc_first"] = 0
		self.parameter_1_id_234["enc_second"] = 127
		self.parameter_1_id_234["reverse_mode"] = False
		self.parameter_1_id_234["steps"] = 20
		self.parameter_1_id_234["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_1_id_234["LED_feedback"] = "default"
		self.parameter_1_id_234["LED_feedback_active"] = "1"
		self.parameter_1_id_234["LED_on"] = "127"
		self.parameter_1_id_234["LED_off"] = "0"
		self.parameter_1_id_234["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_85"]
		self.parameter_1_id_234["snap_to"] = True
		self.parameter_1_id_234["json_id"] = 234
		self.parameter_1_id_234["mapping_name"] = "Parameter 1"
		self.parameter_1_id_234["mapping_type"] = "Parameter"
		self.parameter_1_id_234["parent_json_id"] = 242
		self.parameter_1_id_234["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_2_id_235 = {}
		self.parameter_2_id_235["attached_to"] = "midi_cc_ch_15_val_86"
		self.parameter_2_id_235["track"] = self.track_num(2)
		self.parameter_2_id_235["module"] = "self.song().view.selected_track.devices[0].parameters[2]"
		self.parameter_2_id_235["element"] = "value"
		self.parameter_2_id_235["output_type"] = "val"
		self.parameter_2_id_235["minimum"] = round(0,2)
		self.parameter_2_id_235["maximum"] = round(100,2)
		self.parameter_2_id_235["decimal_places"] = 2
		self.parameter_2_id_235["ui_listener"] = "value"
		self.parameter_2_id_235["feedback_brain"] = "feedback_range"
		self.parameter_2_id_235["ctrl_type"] = "absolute"
		self.parameter_2_id_235["takeover_mode"] = "Value scaling"
		self.parameter_2_id_235["enc_first"] = 0
		self.parameter_2_id_235["enc_second"] = 127
		self.parameter_2_id_235["reverse_mode"] = False
		self.parameter_2_id_235["steps"] = 20
		self.parameter_2_id_235["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_2_id_235["LED_feedback"] = "default"
		self.parameter_2_id_235["LED_feedback_active"] = "1"
		self.parameter_2_id_235["LED_on"] = "127"
		self.parameter_2_id_235["LED_off"] = "0"
		self.parameter_2_id_235["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_86"]
		self.parameter_2_id_235["snap_to"] = True
		self.parameter_2_id_235["json_id"] = 235
		self.parameter_2_id_235["mapping_name"] = "Parameter 2"
		self.parameter_2_id_235["mapping_type"] = "Parameter"
		self.parameter_2_id_235["parent_json_id"] = 242
		self.parameter_2_id_235["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_3_id_236 = {}
		self.parameter_3_id_236["attached_to"] = "midi_cc_ch_15_val_87"
		self.parameter_3_id_236["track"] = self.track_num(2)
		self.parameter_3_id_236["module"] = "self.song().view.selected_track.devices[0].parameters[3]"
		self.parameter_3_id_236["element"] = "value"
		self.parameter_3_id_236["output_type"] = "val"
		self.parameter_3_id_236["minimum"] = round(0,2)
		self.parameter_3_id_236["maximum"] = round(100,2)
		self.parameter_3_id_236["decimal_places"] = 2
		self.parameter_3_id_236["ui_listener"] = "value"
		self.parameter_3_id_236["feedback_brain"] = "feedback_range"
		self.parameter_3_id_236["ctrl_type"] = "absolute"
		self.parameter_3_id_236["takeover_mode"] = "Value scaling"
		self.parameter_3_id_236["enc_first"] = 0
		self.parameter_3_id_236["enc_second"] = 127
		self.parameter_3_id_236["reverse_mode"] = False
		self.parameter_3_id_236["steps"] = 20
		self.parameter_3_id_236["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_3_id_236["LED_feedback"] = "default"
		self.parameter_3_id_236["LED_feedback_active"] = "1"
		self.parameter_3_id_236["LED_on"] = "127"
		self.parameter_3_id_236["LED_off"] = "0"
		self.parameter_3_id_236["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_87"]
		self.parameter_3_id_236["snap_to"] = True
		self.parameter_3_id_236["json_id"] = 236
		self.parameter_3_id_236["mapping_name"] = "Parameter 3"
		self.parameter_3_id_236["mapping_type"] = "Parameter"
		self.parameter_3_id_236["parent_json_id"] = 242
		self.parameter_3_id_236["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_4_id_237 = {}
		self.parameter_4_id_237["attached_to"] = "midi_cc_ch_15_val_88"
		self.parameter_4_id_237["track"] = self.track_num(2)
		self.parameter_4_id_237["module"] = "self.song().view.selected_track.devices[0].parameters[4]"
		self.parameter_4_id_237["element"] = "value"
		self.parameter_4_id_237["output_type"] = "val"
		self.parameter_4_id_237["minimum"] = round(0,2)
		self.parameter_4_id_237["maximum"] = round(100,2)
		self.parameter_4_id_237["decimal_places"] = 2
		self.parameter_4_id_237["ui_listener"] = "value"
		self.parameter_4_id_237["feedback_brain"] = "feedback_range"
		self.parameter_4_id_237["ctrl_type"] = "absolute"
		self.parameter_4_id_237["takeover_mode"] = "Value scaling"
		self.parameter_4_id_237["enc_first"] = 0
		self.parameter_4_id_237["enc_second"] = 127
		self.parameter_4_id_237["reverse_mode"] = False
		self.parameter_4_id_237["steps"] = 20
		self.parameter_4_id_237["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_4_id_237["LED_feedback"] = "default"
		self.parameter_4_id_237["LED_feedback_active"] = "1"
		self.parameter_4_id_237["LED_on"] = "127"
		self.parameter_4_id_237["LED_off"] = "0"
		self.parameter_4_id_237["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_88"]
		self.parameter_4_id_237["snap_to"] = True
		self.parameter_4_id_237["json_id"] = 237
		self.parameter_4_id_237["mapping_name"] = "Parameter 4"
		self.parameter_4_id_237["mapping_type"] = "Parameter"
		self.parameter_4_id_237["parent_json_id"] = 242
		self.parameter_4_id_237["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_5_id_238 = {}
		self.parameter_5_id_238["attached_to"] = "midi_cc_ch_15_val_89"
		self.parameter_5_id_238["track"] = self.track_num(2)
		self.parameter_5_id_238["module"] = "self.song().view.selected_track.devices[0].parameters[5]"
		self.parameter_5_id_238["element"] = "value"
		self.parameter_5_id_238["output_type"] = "val"
		self.parameter_5_id_238["minimum"] = round(0,2)
		self.parameter_5_id_238["maximum"] = round(100,2)
		self.parameter_5_id_238["decimal_places"] = 2
		self.parameter_5_id_238["ui_listener"] = "value"
		self.parameter_5_id_238["feedback_brain"] = "feedback_range"
		self.parameter_5_id_238["ctrl_type"] = "absolute"
		self.parameter_5_id_238["takeover_mode"] = "Value scaling"
		self.parameter_5_id_238["enc_first"] = 0
		self.parameter_5_id_238["enc_second"] = 127
		self.parameter_5_id_238["reverse_mode"] = False
		self.parameter_5_id_238["steps"] = 20
		self.parameter_5_id_238["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_5_id_238["LED_feedback"] = "default"
		self.parameter_5_id_238["LED_feedback_active"] = "1"
		self.parameter_5_id_238["LED_on"] = "127"
		self.parameter_5_id_238["LED_off"] = "0"
		self.parameter_5_id_238["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_89"]
		self.parameter_5_id_238["snap_to"] = True
		self.parameter_5_id_238["json_id"] = 238
		self.parameter_5_id_238["mapping_name"] = "Parameter 5"
		self.parameter_5_id_238["mapping_type"] = "Parameter"
		self.parameter_5_id_238["parent_json_id"] = 242
		self.parameter_5_id_238["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_6_id_239 = {}
		self.parameter_6_id_239["attached_to"] = "midi_cc_ch_15_val_90"
		self.parameter_6_id_239["track"] = self.track_num(2)
		self.parameter_6_id_239["module"] = "self.song().view.selected_track.devices[0].parameters[6]"
		self.parameter_6_id_239["element"] = "value"
		self.parameter_6_id_239["output_type"] = "val"
		self.parameter_6_id_239["minimum"] = round(0,2)
		self.parameter_6_id_239["maximum"] = round(100,2)
		self.parameter_6_id_239["decimal_places"] = 2
		self.parameter_6_id_239["ui_listener"] = "value"
		self.parameter_6_id_239["feedback_brain"] = "feedback_range"
		self.parameter_6_id_239["ctrl_type"] = "absolute"
		self.parameter_6_id_239["takeover_mode"] = "Value scaling"
		self.parameter_6_id_239["enc_first"] = 0
		self.parameter_6_id_239["enc_second"] = 127
		self.parameter_6_id_239["reverse_mode"] = False
		self.parameter_6_id_239["steps"] = 20
		self.parameter_6_id_239["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_6_id_239["LED_feedback"] = "default"
		self.parameter_6_id_239["LED_feedback_active"] = "1"
		self.parameter_6_id_239["LED_on"] = "127"
		self.parameter_6_id_239["LED_off"] = "0"
		self.parameter_6_id_239["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_90"]
		self.parameter_6_id_239["snap_to"] = True
		self.parameter_6_id_239["json_id"] = 239
		self.parameter_6_id_239["mapping_name"] = "Parameter 6"
		self.parameter_6_id_239["mapping_type"] = "Parameter"
		self.parameter_6_id_239["parent_json_id"] = 242
		self.parameter_6_id_239["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_7_id_240 = {}
		self.parameter_7_id_240["attached_to"] = "midi_cc_ch_15_val_91"
		self.parameter_7_id_240["track"] = self.track_num(2)
		self.parameter_7_id_240["module"] = "self.song().view.selected_track.devices[0].parameters[7]"
		self.parameter_7_id_240["element"] = "value"
		self.parameter_7_id_240["output_type"] = "val"
		self.parameter_7_id_240["minimum"] = round(0,2)
		self.parameter_7_id_240["maximum"] = round(100,2)
		self.parameter_7_id_240["decimal_places"] = 2
		self.parameter_7_id_240["ui_listener"] = "value"
		self.parameter_7_id_240["feedback_brain"] = "feedback_range"
		self.parameter_7_id_240["ctrl_type"] = "absolute"
		self.parameter_7_id_240["takeover_mode"] = "Value scaling"
		self.parameter_7_id_240["enc_first"] = 0
		self.parameter_7_id_240["enc_second"] = 127
		self.parameter_7_id_240["reverse_mode"] = False
		self.parameter_7_id_240["steps"] = 20
		self.parameter_7_id_240["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_7_id_240["LED_feedback"] = "default"
		self.parameter_7_id_240["LED_feedback_active"] = "1"
		self.parameter_7_id_240["LED_on"] = "127"
		self.parameter_7_id_240["LED_off"] = "0"
		self.parameter_7_id_240["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_91"]
		self.parameter_7_id_240["snap_to"] = True
		self.parameter_7_id_240["json_id"] = 240
		self.parameter_7_id_240["mapping_name"] = "Parameter 7"
		self.parameter_7_id_240["mapping_type"] = "Parameter"
		self.parameter_7_id_240["parent_json_id"] = 242
		self.parameter_7_id_240["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_8_id_241 = {}
		self.parameter_8_id_241["attached_to"] = "midi_cc_ch_15_val_92"
		self.parameter_8_id_241["track"] = self.track_num(2)
		self.parameter_8_id_241["module"] = "self.song().view.selected_track.devices[0].parameters[8]"
		self.parameter_8_id_241["element"] = "value"
		self.parameter_8_id_241["output_type"] = "val"
		self.parameter_8_id_241["minimum"] = round(0,2)
		self.parameter_8_id_241["maximum"] = round(100,2)
		self.parameter_8_id_241["decimal_places"] = 2
		self.parameter_8_id_241["ui_listener"] = "value"
		self.parameter_8_id_241["feedback_brain"] = "feedback_range"
		self.parameter_8_id_241["ctrl_type"] = "absolute"
		self.parameter_8_id_241["takeover_mode"] = "Value scaling"
		self.parameter_8_id_241["enc_first"] = 0
		self.parameter_8_id_241["enc_second"] = 127
		self.parameter_8_id_241["reverse_mode"] = False
		self.parameter_8_id_241["steps"] = 20
		self.parameter_8_id_241["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_8_id_241["LED_feedback"] = "default"
		self.parameter_8_id_241["LED_feedback_active"] = "1"
		self.parameter_8_id_241["LED_on"] = "127"
		self.parameter_8_id_241["LED_off"] = "0"
		self.parameter_8_id_241["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_92"]
		self.parameter_8_id_241["snap_to"] = True
		self.parameter_8_id_241["json_id"] = 241
		self.parameter_8_id_241["mapping_name"] = "Parameter 8"
		self.parameter_8_id_241["mapping_type"] = "Parameter"
		self.parameter_8_id_241["parent_json_id"] = 242
		self.parameter_8_id_241["parent_name"] = "parameter_bank_1_id_242"
		self.parameter_bank_1_id_242 = {}
		self.parameter_bank_1_id_242["LED_mapping_type_needs_feedback"] = ""
		self.parameter_bank_1_id_242["LED_feedback"] = "custom"
		self.parameter_bank_1_id_242["LED_feedback_active"] = ""
		self.parameter_bank_1_id_242["LED_on"] = "127"
		self.parameter_bank_1_id_242["LED_off"] = "0"
		self.parameter_bank_1_id_242["LED_send_feedback_to_selected"] = []
		self.parameter_bank_1_id_242["json_id"] = 242
		self.parameter_bank_1_id_242["mapping_name"] = "Parameter Bank 1"
		self.parameter_bank_1_id_242["mapping_type"] = "Parameter Bank"
		self.parameter_bank_1_id_242["parent_json_id"] = 243
		self.parameter_bank_1_id_242["parent_name"] = "device_1_id_243"
		self.device_1_id_243 = {}
		self.device_1_id_243["track"] = self.track_num(2)
		self.device_1_id_243["module"] = "self.song().view.selected_track.devices[0]"
		self.device_1_id_243["LED_mapping_type_needs_feedback"] = ""
		self.device_1_id_243["LED_feedback"] = "custom"
		self.device_1_id_243["LED_feedback_active"] = ""
		self.device_1_id_243["LED_on"] = "127"
		self.device_1_id_243["LED_off"] = "0"
		self.device_1_id_243["LED_send_feedback_to_selected"] = []
		self.device_1_id_243["json_id"] = 243
		self.device_1_id_243["mapping_name"] = "Device 1"
		self.device_1_id_243["mapping_type"] = "Device"
		self.device_1_id_243["parent_json_id"] = 318
		self.device_1_id_243["parent_name"] = "track_select_id_318"
		self.volume_9_id_248 = {}
		self.volume_9_id_248["attached_to"] = "midi_cc_ch_8_val_7"
		self.volume_9_id_248["track"] = self.track_num(2)
		self.volume_9_id_248["module"] = "self.song().tracks[self.track_num(8)].mixer_device.volume"
		self.volume_9_id_248["element"] = "value"
		self.volume_9_id_248["output_type"] = "val"
		self.volume_9_id_248["minimum"] = round(0,2)
		self.volume_9_id_248["maximum"] = round(85,2)
		self.volume_9_id_248["decimal_places"] = 2
		self.volume_9_id_248["ui_listener"] = "value"
		self.volume_9_id_248["feedback_brain"] = "feedback_range"
		self.volume_9_id_248["ctrl_type"] = "absolute"
		self.volume_9_id_248["takeover_mode"] = "None"
		self.volume_9_id_248["enc_first"] = 0
		self.volume_9_id_248["enc_second"] = 127
		self.volume_9_id_248["reverse_mode"] = False
		self.volume_9_id_248["LED_mapping_type_needs_feedback"] = "1"
		self.volume_9_id_248["LED_feedback"] = "default"
		self.volume_9_id_248["LED_feedback_active"] = "1"
		self.volume_9_id_248["LED_on"] = "127"
		self.volume_9_id_248["LED_off"] = "0"
		self.volume_9_id_248["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_7"]
		self.volume_9_id_248["snap_to"] = True
		self.volume_9_id_248["json_id"] = 248
		self.volume_9_id_248["mapping_name"] = "Volume 9"
		self.volume_9_id_248["mapping_type"] = "Volume"
		self.volume_9_id_248["parent_json_id"] = 319
		self.volume_9_id_248["parent_name"] = "track_9_id_319"
		self.pan_9_id_249 = {}
		self.pan_9_id_249["attached_to"] = "midi_cc_ch_8_val_82"
		self.pan_9_id_249["track"] = self.track_num(2)
		self.pan_9_id_249["module"] = "self.song().tracks[self.track_num(8)].mixer_device.panning"
		self.pan_9_id_249["element"] = "value"
		self.pan_9_id_249["output_type"] = "val"
		self.pan_9_id_249["minimum"] = round(0,2)
		self.pan_9_id_249["maximum"] = round(100,2)
		self.pan_9_id_249["decimal_places"] = 2
		self.pan_9_id_249["ui_listener"] = "value"
		self.pan_9_id_249["feedback_brain"] = "feedback_range"
		self.pan_9_id_249["ctrl_type"] = "absolute"
		self.pan_9_id_249["takeover_mode"] = "None"
		self.pan_9_id_249["enc_first"] = 0
		self.pan_9_id_249["enc_second"] = 127
		self.pan_9_id_249["reverse_mode"] = False
		self.pan_9_id_249["LED_mapping_type_needs_feedback"] = "1"
		self.pan_9_id_249["LED_feedback"] = "default"
		self.pan_9_id_249["LED_feedback_active"] = "1"
		self.pan_9_id_249["LED_on"] = "127"
		self.pan_9_id_249["LED_off"] = "0"
		self.pan_9_id_249["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_82"]
		self.pan_9_id_249["snap_to"] = True
		self.pan_9_id_249["json_id"] = 249
		self.pan_9_id_249["mapping_name"] = "Pan 9"
		self.pan_9_id_249["mapping_type"] = "Pan"
		self.pan_9_id_249["parent_json_id"] = 319
		self.pan_9_id_249["parent_name"] = "track_9_id_319"
		self.volume_10_id_256 = {}
		self.volume_10_id_256["attached_to"] = "midi_cc_ch_9_val_7"
		self.volume_10_id_256["track"] = self.track_num(2)
		self.volume_10_id_256["module"] = "self.song().tracks[self.track_num(9)].mixer_device.volume"
		self.volume_10_id_256["element"] = "value"
		self.volume_10_id_256["output_type"] = "val"
		self.volume_10_id_256["minimum"] = round(0,2)
		self.volume_10_id_256["maximum"] = round(85,2)
		self.volume_10_id_256["decimal_places"] = 2
		self.volume_10_id_256["ui_listener"] = "value"
		self.volume_10_id_256["feedback_brain"] = "feedback_range"
		self.volume_10_id_256["ctrl_type"] = "absolute"
		self.volume_10_id_256["takeover_mode"] = "None"
		self.volume_10_id_256["enc_first"] = 0
		self.volume_10_id_256["enc_second"] = 127
		self.volume_10_id_256["reverse_mode"] = False
		self.volume_10_id_256["LED_mapping_type_needs_feedback"] = "1"
		self.volume_10_id_256["LED_feedback"] = "default"
		self.volume_10_id_256["LED_feedback_active"] = "1"
		self.volume_10_id_256["LED_on"] = "127"
		self.volume_10_id_256["LED_off"] = "0"
		self.volume_10_id_256["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_7"]
		self.volume_10_id_256["snap_to"] = True
		self.volume_10_id_256["json_id"] = 256
		self.volume_10_id_256["mapping_name"] = "Volume 10"
		self.volume_10_id_256["mapping_type"] = "Volume"
		self.volume_10_id_256["parent_json_id"] = 320
		self.volume_10_id_256["parent_name"] = "track_10_id_320"
		self.pan_10_id_257 = {}
		self.pan_10_id_257["attached_to"] = "midi_cc_ch_9_val_82"
		self.pan_10_id_257["track"] = self.track_num(2)
		self.pan_10_id_257["module"] = "self.song().tracks[self.track_num(9)].mixer_device.panning"
		self.pan_10_id_257["element"] = "value"
		self.pan_10_id_257["output_type"] = "val"
		self.pan_10_id_257["minimum"] = round(0,2)
		self.pan_10_id_257["maximum"] = round(100,2)
		self.pan_10_id_257["decimal_places"] = 2
		self.pan_10_id_257["ui_listener"] = "value"
		self.pan_10_id_257["feedback_brain"] = "feedback_range"
		self.pan_10_id_257["ctrl_type"] = "absolute"
		self.pan_10_id_257["takeover_mode"] = "None"
		self.pan_10_id_257["enc_first"] = 0
		self.pan_10_id_257["enc_second"] = 127
		self.pan_10_id_257["reverse_mode"] = False
		self.pan_10_id_257["LED_mapping_type_needs_feedback"] = "1"
		self.pan_10_id_257["LED_feedback"] = "default"
		self.pan_10_id_257["LED_feedback_active"] = "1"
		self.pan_10_id_257["LED_on"] = "127"
		self.pan_10_id_257["LED_off"] = "0"
		self.pan_10_id_257["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_82"]
		self.pan_10_id_257["snap_to"] = True
		self.pan_10_id_257["json_id"] = 257
		self.pan_10_id_257["mapping_name"] = "Pan 10"
		self.pan_10_id_257["mapping_type"] = "Pan"
		self.pan_10_id_257["parent_json_id"] = 320
		self.pan_10_id_257["parent_name"] = "track_10_id_320"
		self.volume_11_id_264 = {}
		self.volume_11_id_264["attached_to"] = "midi_cc_ch_10_val_7"
		self.volume_11_id_264["track"] = self.track_num(2)
		self.volume_11_id_264["module"] = "self.song().tracks[self.track_num(10)].mixer_device.volume"
		self.volume_11_id_264["element"] = "value"
		self.volume_11_id_264["output_type"] = "val"
		self.volume_11_id_264["minimum"] = round(0,2)
		self.volume_11_id_264["maximum"] = round(85,2)
		self.volume_11_id_264["decimal_places"] = 2
		self.volume_11_id_264["ui_listener"] = "value"
		self.volume_11_id_264["feedback_brain"] = "feedback_range"
		self.volume_11_id_264["ctrl_type"] = "absolute"
		self.volume_11_id_264["takeover_mode"] = "None"
		self.volume_11_id_264["enc_first"] = 0
		self.volume_11_id_264["enc_second"] = 127
		self.volume_11_id_264["reverse_mode"] = False
		self.volume_11_id_264["LED_mapping_type_needs_feedback"] = "1"
		self.volume_11_id_264["LED_feedback"] = "default"
		self.volume_11_id_264["LED_feedback_active"] = "1"
		self.volume_11_id_264["LED_on"] = "127"
		self.volume_11_id_264["LED_off"] = "0"
		self.volume_11_id_264["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_7"]
		self.volume_11_id_264["snap_to"] = True
		self.volume_11_id_264["json_id"] = 264
		self.volume_11_id_264["mapping_name"] = "Volume 11"
		self.volume_11_id_264["mapping_type"] = "Volume"
		self.volume_11_id_264["parent_json_id"] = 321
		self.volume_11_id_264["parent_name"] = "track_11_id_321"
		self.pan_11_id_265 = {}
		self.pan_11_id_265["attached_to"] = "midi_cc_ch_10_val_82"
		self.pan_11_id_265["track"] = self.track_num(2)
		self.pan_11_id_265["module"] = "self.song().tracks[self.track_num(10)].mixer_device.panning"
		self.pan_11_id_265["element"] = "value"
		self.pan_11_id_265["output_type"] = "val"
		self.pan_11_id_265["minimum"] = round(0,2)
		self.pan_11_id_265["maximum"] = round(100,2)
		self.pan_11_id_265["decimal_places"] = 2
		self.pan_11_id_265["ui_listener"] = "value"
		self.pan_11_id_265["feedback_brain"] = "feedback_range"
		self.pan_11_id_265["ctrl_type"] = "absolute"
		self.pan_11_id_265["takeover_mode"] = "None"
		self.pan_11_id_265["enc_first"] = 0
		self.pan_11_id_265["enc_second"] = 127
		self.pan_11_id_265["reverse_mode"] = False
		self.pan_11_id_265["LED_mapping_type_needs_feedback"] = "1"
		self.pan_11_id_265["LED_feedback"] = "default"
		self.pan_11_id_265["LED_feedback_active"] = "1"
		self.pan_11_id_265["LED_on"] = "127"
		self.pan_11_id_265["LED_off"] = "0"
		self.pan_11_id_265["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_82"]
		self.pan_11_id_265["snap_to"] = True
		self.pan_11_id_265["json_id"] = 265
		self.pan_11_id_265["mapping_name"] = "Pan 11"
		self.pan_11_id_265["mapping_type"] = "Pan"
		self.pan_11_id_265["parent_json_id"] = 321
		self.pan_11_id_265["parent_name"] = "track_11_id_321"
		self.volume_12_id_272 = {}
		self.volume_12_id_272["attached_to"] = "midi_cc_ch_11_val_7"
		self.volume_12_id_272["track"] = self.track_num(2)
		self.volume_12_id_272["module"] = "self.song().tracks[self.track_num(11)].mixer_device.volume"
		self.volume_12_id_272["element"] = "value"
		self.volume_12_id_272["output_type"] = "val"
		self.volume_12_id_272["minimum"] = round(0,2)
		self.volume_12_id_272["maximum"] = round(85,2)
		self.volume_12_id_272["decimal_places"] = 2
		self.volume_12_id_272["ui_listener"] = "value"
		self.volume_12_id_272["feedback_brain"] = "feedback_range"
		self.volume_12_id_272["ctrl_type"] = "absolute"
		self.volume_12_id_272["takeover_mode"] = "None"
		self.volume_12_id_272["enc_first"] = 0
		self.volume_12_id_272["enc_second"] = 127
		self.volume_12_id_272["reverse_mode"] = False
		self.volume_12_id_272["LED_mapping_type_needs_feedback"] = "1"
		self.volume_12_id_272["LED_feedback"] = "default"
		self.volume_12_id_272["LED_feedback_active"] = "1"
		self.volume_12_id_272["LED_on"] = "127"
		self.volume_12_id_272["LED_off"] = "0"
		self.volume_12_id_272["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_7"]
		self.volume_12_id_272["snap_to"] = True
		self.volume_12_id_272["json_id"] = 272
		self.volume_12_id_272["mapping_name"] = "Volume 12"
		self.volume_12_id_272["mapping_type"] = "Volume"
		self.volume_12_id_272["parent_json_id"] = 322
		self.volume_12_id_272["parent_name"] = "track_12_id_322"
		self.pan_12_id_273 = {}
		self.pan_12_id_273["attached_to"] = "midi_cc_ch_11_val_82"
		self.pan_12_id_273["track"] = self.track_num(2)
		self.pan_12_id_273["module"] = "self.song().tracks[self.track_num(11)].mixer_device.panning"
		self.pan_12_id_273["element"] = "value"
		self.pan_12_id_273["output_type"] = "val"
		self.pan_12_id_273["minimum"] = round(0,2)
		self.pan_12_id_273["maximum"] = round(100,2)
		self.pan_12_id_273["decimal_places"] = 2
		self.pan_12_id_273["ui_listener"] = "value"
		self.pan_12_id_273["feedback_brain"] = "feedback_range"
		self.pan_12_id_273["ctrl_type"] = "absolute"
		self.pan_12_id_273["takeover_mode"] = "None"
		self.pan_12_id_273["enc_first"] = 0
		self.pan_12_id_273["enc_second"] = 127
		self.pan_12_id_273["reverse_mode"] = False
		self.pan_12_id_273["LED_mapping_type_needs_feedback"] = "1"
		self.pan_12_id_273["LED_feedback"] = "default"
		self.pan_12_id_273["LED_feedback_active"] = "1"
		self.pan_12_id_273["LED_on"] = "127"
		self.pan_12_id_273["LED_off"] = "0"
		self.pan_12_id_273["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_82"]
		self.pan_12_id_273["snap_to"] = True
		self.pan_12_id_273["json_id"] = 273
		self.pan_12_id_273["mapping_name"] = "Pan 12"
		self.pan_12_id_273["mapping_type"] = "Pan"
		self.pan_12_id_273["parent_json_id"] = 322
		self.pan_12_id_273["parent_name"] = "track_12_id_322"
		self.volume_13_id_280 = {}
		self.volume_13_id_280["attached_to"] = "midi_cc_ch_12_val_7"
		self.volume_13_id_280["track"] = self.track_num(2)
		self.volume_13_id_280["module"] = "self.song().tracks[self.track_num(12)].mixer_device.volume"
		self.volume_13_id_280["element"] = "value"
		self.volume_13_id_280["output_type"] = "val"
		self.volume_13_id_280["minimum"] = round(0,2)
		self.volume_13_id_280["maximum"] = round(85,2)
		self.volume_13_id_280["decimal_places"] = 2
		self.volume_13_id_280["ui_listener"] = "value"
		self.volume_13_id_280["feedback_brain"] = "feedback_range"
		self.volume_13_id_280["ctrl_type"] = "absolute"
		self.volume_13_id_280["takeover_mode"] = "None"
		self.volume_13_id_280["enc_first"] = 0
		self.volume_13_id_280["enc_second"] = 127
		self.volume_13_id_280["reverse_mode"] = False
		self.volume_13_id_280["LED_mapping_type_needs_feedback"] = "1"
		self.volume_13_id_280["LED_feedback"] = "default"
		self.volume_13_id_280["LED_feedback_active"] = "1"
		self.volume_13_id_280["LED_on"] = "127"
		self.volume_13_id_280["LED_off"] = "0"
		self.volume_13_id_280["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_7"]
		self.volume_13_id_280["snap_to"] = True
		self.volume_13_id_280["json_id"] = 280
		self.volume_13_id_280["mapping_name"] = "Volume 13"
		self.volume_13_id_280["mapping_type"] = "Volume"
		self.volume_13_id_280["parent_json_id"] = 323
		self.volume_13_id_280["parent_name"] = "track_13_id_323"
		self.pan_13_id_281 = {}
		self.pan_13_id_281["attached_to"] = "midi_cc_ch_12_val_82"
		self.pan_13_id_281["track"] = self.track_num(2)
		self.pan_13_id_281["module"] = "self.song().tracks[self.track_num(12)].mixer_device.panning"
		self.pan_13_id_281["element"] = "value"
		self.pan_13_id_281["output_type"] = "val"
		self.pan_13_id_281["minimum"] = round(0,2)
		self.pan_13_id_281["maximum"] = round(100,2)
		self.pan_13_id_281["decimal_places"] = 2
		self.pan_13_id_281["ui_listener"] = "value"
		self.pan_13_id_281["feedback_brain"] = "feedback_range"
		self.pan_13_id_281["ctrl_type"] = "absolute"
		self.pan_13_id_281["takeover_mode"] = "None"
		self.pan_13_id_281["enc_first"] = 0
		self.pan_13_id_281["enc_second"] = 127
		self.pan_13_id_281["reverse_mode"] = False
		self.pan_13_id_281["LED_mapping_type_needs_feedback"] = "1"
		self.pan_13_id_281["LED_feedback"] = "default"
		self.pan_13_id_281["LED_feedback_active"] = "1"
		self.pan_13_id_281["LED_on"] = "127"
		self.pan_13_id_281["LED_off"] = "0"
		self.pan_13_id_281["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_82"]
		self.pan_13_id_281["snap_to"] = True
		self.pan_13_id_281["json_id"] = 281
		self.pan_13_id_281["mapping_name"] = "Pan 13"
		self.pan_13_id_281["mapping_type"] = "Pan"
		self.pan_13_id_281["parent_json_id"] = 323
		self.pan_13_id_281["parent_name"] = "track_13_id_323"
		self.volume_14_id_288 = {}
		self.volume_14_id_288["attached_to"] = "midi_cc_ch_13_val_7"
		self.volume_14_id_288["track"] = self.track_num(2)
		self.volume_14_id_288["module"] = "self.song().tracks[self.track_num(13)].mixer_device.volume"
		self.volume_14_id_288["element"] = "value"
		self.volume_14_id_288["output_type"] = "val"
		self.volume_14_id_288["minimum"] = round(0,2)
		self.volume_14_id_288["maximum"] = round(85,2)
		self.volume_14_id_288["decimal_places"] = 2
		self.volume_14_id_288["ui_listener"] = "value"
		self.volume_14_id_288["feedback_brain"] = "feedback_range"
		self.volume_14_id_288["ctrl_type"] = "absolute"
		self.volume_14_id_288["takeover_mode"] = "None"
		self.volume_14_id_288["enc_first"] = 0
		self.volume_14_id_288["enc_second"] = 127
		self.volume_14_id_288["reverse_mode"] = False
		self.volume_14_id_288["LED_mapping_type_needs_feedback"] = "1"
		self.volume_14_id_288["LED_feedback"] = "default"
		self.volume_14_id_288["LED_feedback_active"] = "1"
		self.volume_14_id_288["LED_on"] = "127"
		self.volume_14_id_288["LED_off"] = "0"
		self.volume_14_id_288["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_7"]
		self.volume_14_id_288["snap_to"] = True
		self.volume_14_id_288["json_id"] = 288
		self.volume_14_id_288["mapping_name"] = "Volume 14"
		self.volume_14_id_288["mapping_type"] = "Volume"
		self.volume_14_id_288["parent_json_id"] = 324
		self.volume_14_id_288["parent_name"] = "track_14_id_324"
		self.pan_14_id_289 = {}
		self.pan_14_id_289["attached_to"] = "midi_cc_ch_13_val_82"
		self.pan_14_id_289["track"] = self.track_num(2)
		self.pan_14_id_289["module"] = "self.song().tracks[self.track_num(13)].mixer_device.panning"
		self.pan_14_id_289["element"] = "value"
		self.pan_14_id_289["output_type"] = "val"
		self.pan_14_id_289["minimum"] = round(0,2)
		self.pan_14_id_289["maximum"] = round(100,2)
		self.pan_14_id_289["decimal_places"] = 2
		self.pan_14_id_289["ui_listener"] = "value"
		self.pan_14_id_289["feedback_brain"] = "feedback_range"
		self.pan_14_id_289["ctrl_type"] = "absolute"
		self.pan_14_id_289["takeover_mode"] = "None"
		self.pan_14_id_289["enc_first"] = 0
		self.pan_14_id_289["enc_second"] = 127
		self.pan_14_id_289["reverse_mode"] = False
		self.pan_14_id_289["LED_mapping_type_needs_feedback"] = "1"
		self.pan_14_id_289["LED_feedback"] = "default"
		self.pan_14_id_289["LED_feedback_active"] = "1"
		self.pan_14_id_289["LED_on"] = "127"
		self.pan_14_id_289["LED_off"] = "0"
		self.pan_14_id_289["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_82"]
		self.pan_14_id_289["snap_to"] = True
		self.pan_14_id_289["json_id"] = 289
		self.pan_14_id_289["mapping_name"] = "Pan 14"
		self.pan_14_id_289["mapping_type"] = "Pan"
		self.pan_14_id_289["parent_json_id"] = 324
		self.pan_14_id_289["parent_name"] = "track_14_id_324"
		self.volume_15_id_296 = {}
		self.volume_15_id_296["attached_to"] = "midi_cc_ch_14_val_7"
		self.volume_15_id_296["track"] = self.track_num(2)
		self.volume_15_id_296["module"] = "self.song().tracks[self.track_num(14)].mixer_device.volume"
		self.volume_15_id_296["element"] = "value"
		self.volume_15_id_296["output_type"] = "val"
		self.volume_15_id_296["minimum"] = round(0,2)
		self.volume_15_id_296["maximum"] = round(85,2)
		self.volume_15_id_296["decimal_places"] = 2
		self.volume_15_id_296["ui_listener"] = "value"
		self.volume_15_id_296["feedback_brain"] = "feedback_range"
		self.volume_15_id_296["ctrl_type"] = "absolute"
		self.volume_15_id_296["takeover_mode"] = "None"
		self.volume_15_id_296["enc_first"] = 0
		self.volume_15_id_296["enc_second"] = 127
		self.volume_15_id_296["reverse_mode"] = False
		self.volume_15_id_296["LED_mapping_type_needs_feedback"] = "1"
		self.volume_15_id_296["LED_feedback"] = "default"
		self.volume_15_id_296["LED_feedback_active"] = "1"
		self.volume_15_id_296["LED_on"] = "127"
		self.volume_15_id_296["LED_off"] = "0"
		self.volume_15_id_296["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_7"]
		self.volume_15_id_296["snap_to"] = True
		self.volume_15_id_296["json_id"] = 296
		self.volume_15_id_296["mapping_name"] = "Volume 15"
		self.volume_15_id_296["mapping_type"] = "Volume"
		self.volume_15_id_296["parent_json_id"] = 325
		self.volume_15_id_296["parent_name"] = "track_15_id_325"
		self.pan_15_id_297 = {}
		self.pan_15_id_297["attached_to"] = "midi_cc_ch_14_val_82"
		self.pan_15_id_297["track"] = self.track_num(2)
		self.pan_15_id_297["module"] = "self.song().tracks[self.track_num(14)].mixer_device.panning"
		self.pan_15_id_297["element"] = "value"
		self.pan_15_id_297["output_type"] = "val"
		self.pan_15_id_297["minimum"] = round(0,2)
		self.pan_15_id_297["maximum"] = round(100,2)
		self.pan_15_id_297["decimal_places"] = 2
		self.pan_15_id_297["ui_listener"] = "value"
		self.pan_15_id_297["feedback_brain"] = "feedback_range"
		self.pan_15_id_297["ctrl_type"] = "absolute"
		self.pan_15_id_297["takeover_mode"] = "None"
		self.pan_15_id_297["enc_first"] = 0
		self.pan_15_id_297["enc_second"] = 127
		self.pan_15_id_297["reverse_mode"] = False
		self.pan_15_id_297["LED_mapping_type_needs_feedback"] = "1"
		self.pan_15_id_297["LED_feedback"] = "default"
		self.pan_15_id_297["LED_feedback_active"] = "1"
		self.pan_15_id_297["LED_on"] = "127"
		self.pan_15_id_297["LED_off"] = "0"
		self.pan_15_id_297["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_82"]
		self.pan_15_id_297["snap_to"] = True
		self.pan_15_id_297["json_id"] = 297
		self.pan_15_id_297["mapping_name"] = "Pan 15"
		self.pan_15_id_297["mapping_type"] = "Pan"
		self.pan_15_id_297["parent_json_id"] = 325
		self.pan_15_id_297["parent_name"] = "track_15_id_325"
		self.volume_16_id_304 = {}
		self.volume_16_id_304["attached_to"] = "midi_cc_ch_15_val_7"
		self.volume_16_id_304["track"] = self.track_num(2)
		self.volume_16_id_304["module"] = "self.song().tracks[self.track_num(15)].mixer_device.volume"
		self.volume_16_id_304["element"] = "value"
		self.volume_16_id_304["output_type"] = "val"
		self.volume_16_id_304["minimum"] = round(0,2)
		self.volume_16_id_304["maximum"] = round(85,2)
		self.volume_16_id_304["decimal_places"] = 2
		self.volume_16_id_304["ui_listener"] = "value"
		self.volume_16_id_304["feedback_brain"] = "feedback_range"
		self.volume_16_id_304["ctrl_type"] = "absolute"
		self.volume_16_id_304["takeover_mode"] = "None"
		self.volume_16_id_304["enc_first"] = 0
		self.volume_16_id_304["enc_second"] = 127
		self.volume_16_id_304["reverse_mode"] = False
		self.volume_16_id_304["LED_mapping_type_needs_feedback"] = "1"
		self.volume_16_id_304["LED_feedback"] = "default"
		self.volume_16_id_304["LED_feedback_active"] = "1"
		self.volume_16_id_304["LED_on"] = "127"
		self.volume_16_id_304["LED_off"] = "0"
		self.volume_16_id_304["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_7"]
		self.volume_16_id_304["snap_to"] = True
		self.volume_16_id_304["json_id"] = 304
		self.volume_16_id_304["mapping_name"] = "Volume 16"
		self.volume_16_id_304["mapping_type"] = "Volume"
		self.volume_16_id_304["parent_json_id"] = 326
		self.volume_16_id_304["parent_name"] = "track_16_id_326"
		self.pan_16_id_305 = {}
		self.pan_16_id_305["attached_to"] = "midi_cc_ch_15_val_82"
		self.pan_16_id_305["track"] = self.track_num(2)
		self.pan_16_id_305["module"] = "self.song().tracks[self.track_num(15)].mixer_device.panning"
		self.pan_16_id_305["element"] = "value"
		self.pan_16_id_305["output_type"] = "val"
		self.pan_16_id_305["minimum"] = round(0,2)
		self.pan_16_id_305["maximum"] = round(100,2)
		self.pan_16_id_305["decimal_places"] = 2
		self.pan_16_id_305["ui_listener"] = "value"
		self.pan_16_id_305["feedback_brain"] = "feedback_range"
		self.pan_16_id_305["ctrl_type"] = "absolute"
		self.pan_16_id_305["takeover_mode"] = "None"
		self.pan_16_id_305["enc_first"] = 0
		self.pan_16_id_305["enc_second"] = 127
		self.pan_16_id_305["reverse_mode"] = False
		self.pan_16_id_305["LED_mapping_type_needs_feedback"] = "1"
		self.pan_16_id_305["LED_feedback"] = "default"
		self.pan_16_id_305["LED_feedback_active"] = "1"
		self.pan_16_id_305["LED_on"] = "127"
		self.pan_16_id_305["LED_off"] = "0"
		self.pan_16_id_305["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_82"]
		self.pan_16_id_305["snap_to"] = True
		self.pan_16_id_305["json_id"] = 305
		self.pan_16_id_305["mapping_name"] = "Pan 16"
		self.pan_16_id_305["mapping_type"] = "Pan"
		self.pan_16_id_305["parent_json_id"] = 326
		self.pan_16_id_305["parent_name"] = "track_16_id_326"
		self.track_1_id_308 = {}
		self.track_1_id_308["track"] = self.track_num(2)
		self.track_1_id_308["module"] = "self.song().tracks[self.track_num(0)]"
		self.track_1_id_308["LED_mapping_type_needs_feedback"] = ""
		self.track_1_id_308["LED_feedback"] = "custom"
		self.track_1_id_308["LED_feedback_active"] = ""
		self.track_1_id_308["LED_on"] = "127"
		self.track_1_id_308["LED_off"] = "0"
		self.track_1_id_308["LED_send_feedback_to_selected"] = []
		self.track_1_id_308["json_id"] = 308
		self.track_1_id_308["mapping_name"] = "Track 1"
		self.track_1_id_308["mapping_type"] = "Track"
		self.track_1_id_308["parent_json_id"] = 169
		self.track_1_id_308["parent_name"] = "mode_2_id_169"
		self.track_2_id_309 = {}
		self.track_2_id_309["track"] = self.track_num(2)
		self.track_2_id_309["module"] = "self.song().tracks[self.track_num(1)]"
		self.track_2_id_309["LED_mapping_type_needs_feedback"] = ""
		self.track_2_id_309["LED_feedback"] = "custom"
		self.track_2_id_309["LED_feedback_active"] = ""
		self.track_2_id_309["LED_on"] = "127"
		self.track_2_id_309["LED_off"] = "0"
		self.track_2_id_309["LED_send_feedback_to_selected"] = []
		self.track_2_id_309["json_id"] = 309
		self.track_2_id_309["mapping_name"] = "Track 2"
		self.track_2_id_309["mapping_type"] = "Track"
		self.track_2_id_309["parent_json_id"] = 169
		self.track_2_id_309["parent_name"] = "mode_2_id_169"
		self.track_3_id_310 = {}
		self.track_3_id_310["track"] = self.track_num(2)
		self.track_3_id_310["module"] = "self.song().tracks[self.track_num(2)]"
		self.track_3_id_310["LED_mapping_type_needs_feedback"] = ""
		self.track_3_id_310["LED_feedback"] = "custom"
		self.track_3_id_310["LED_feedback_active"] = ""
		self.track_3_id_310["LED_on"] = "127"
		self.track_3_id_310["LED_off"] = "0"
		self.track_3_id_310["LED_send_feedback_to_selected"] = []
		self.track_3_id_310["json_id"] = 310
		self.track_3_id_310["mapping_name"] = "Track 3"
		self.track_3_id_310["mapping_type"] = "Track"
		self.track_3_id_310["parent_json_id"] = 169
		self.track_3_id_310["parent_name"] = "mode_2_id_169"
		self.track_4_id_311 = {}
		self.track_4_id_311["track"] = self.track_num(2)
		self.track_4_id_311["module"] = "self.song().tracks[self.track_num(3)]"
		self.track_4_id_311["LED_mapping_type_needs_feedback"] = ""
		self.track_4_id_311["LED_feedback"] = "custom"
		self.track_4_id_311["LED_feedback_active"] = ""
		self.track_4_id_311["LED_on"] = "127"
		self.track_4_id_311["LED_off"] = "0"
		self.track_4_id_311["LED_send_feedback_to_selected"] = []
		self.track_4_id_311["json_id"] = 311
		self.track_4_id_311["mapping_name"] = "Track 4"
		self.track_4_id_311["mapping_type"] = "Track"
		self.track_4_id_311["parent_json_id"] = 169
		self.track_4_id_311["parent_name"] = "mode_2_id_169"
		self.track_5_id_312 = {}
		self.track_5_id_312["track"] = self.track_num(2)
		self.track_5_id_312["module"] = "self.song().tracks[self.track_num(4)]"
		self.track_5_id_312["LED_mapping_type_needs_feedback"] = ""
		self.track_5_id_312["LED_feedback"] = "custom"
		self.track_5_id_312["LED_feedback_active"] = ""
		self.track_5_id_312["LED_on"] = "127"
		self.track_5_id_312["LED_off"] = "0"
		self.track_5_id_312["LED_send_feedback_to_selected"] = []
		self.track_5_id_312["json_id"] = 312
		self.track_5_id_312["mapping_name"] = "Track 5"
		self.track_5_id_312["mapping_type"] = "Track"
		self.track_5_id_312["parent_json_id"] = 169
		self.track_5_id_312["parent_name"] = "mode_2_id_169"
		self.track_6_id_313 = {}
		self.track_6_id_313["track"] = self.track_num(2)
		self.track_6_id_313["module"] = "self.song().tracks[self.track_num(5)]"
		self.track_6_id_313["LED_mapping_type_needs_feedback"] = ""
		self.track_6_id_313["LED_feedback"] = "custom"
		self.track_6_id_313["LED_feedback_active"] = ""
		self.track_6_id_313["LED_on"] = "127"
		self.track_6_id_313["LED_off"] = "0"
		self.track_6_id_313["LED_send_feedback_to_selected"] = []
		self.track_6_id_313["json_id"] = 313
		self.track_6_id_313["mapping_name"] = "Track 6"
		self.track_6_id_313["mapping_type"] = "Track"
		self.track_6_id_313["parent_json_id"] = 169
		self.track_6_id_313["parent_name"] = "mode_2_id_169"
		self.track_7_id_314 = {}
		self.track_7_id_314["track"] = self.track_num(2)
		self.track_7_id_314["module"] = "self.song().tracks[self.track_num(6)]"
		self.track_7_id_314["LED_mapping_type_needs_feedback"] = ""
		self.track_7_id_314["LED_feedback"] = "custom"
		self.track_7_id_314["LED_feedback_active"] = ""
		self.track_7_id_314["LED_on"] = "127"
		self.track_7_id_314["LED_off"] = "0"
		self.track_7_id_314["LED_send_feedback_to_selected"] = []
		self.track_7_id_314["json_id"] = 314
		self.track_7_id_314["mapping_name"] = "Track 7"
		self.track_7_id_314["mapping_type"] = "Track"
		self.track_7_id_314["parent_json_id"] = 169
		self.track_7_id_314["parent_name"] = "mode_2_id_169"
		self.track_8_id_315 = {}
		self.track_8_id_315["track"] = self.track_num(2)
		self.track_8_id_315["module"] = "self.song().tracks[self.track_num(7)]"
		self.track_8_id_315["LED_mapping_type_needs_feedback"] = ""
		self.track_8_id_315["LED_feedback"] = "custom"
		self.track_8_id_315["LED_feedback_active"] = ""
		self.track_8_id_315["LED_on"] = "127"
		self.track_8_id_315["LED_off"] = "0"
		self.track_8_id_315["LED_send_feedback_to_selected"] = []
		self.track_8_id_315["json_id"] = 315
		self.track_8_id_315["mapping_name"] = "Track 8"
		self.track_8_id_315["mapping_type"] = "Track"
		self.track_8_id_315["parent_json_id"] = 169
		self.track_8_id_315["parent_name"] = "mode_2_id_169"
		self.track_select_id_318 = {}
		self.track_select_id_318["track"] = self.track_num(2)
		self.track_select_id_318["module"] = "self.song().view.selected_track"
		self.track_select_id_318["LED_mapping_type_needs_feedback"] = ""
		self.track_select_id_318["LED_feedback"] = "custom"
		self.track_select_id_318["LED_feedback_active"] = ""
		self.track_select_id_318["LED_on"] = "127"
		self.track_select_id_318["LED_off"] = "0"
		self.track_select_id_318["LED_send_feedback_to_selected"] = []
		self.track_select_id_318["json_id"] = 318
		self.track_select_id_318["mapping_name"] = "track select"
		self.track_select_id_318["mapping_type"] = "Track"
		self.track_select_id_318["parent_json_id"] = 169
		self.track_select_id_318["parent_name"] = "mode_2_id_169"
		self.track_9_id_319 = {}
		self.track_9_id_319["track"] = self.track_num(2)
		self.track_9_id_319["module"] = "self.song().tracks[self.track_num(8)]"
		self.track_9_id_319["LED_mapping_type_needs_feedback"] = ""
		self.track_9_id_319["LED_feedback"] = "custom"
		self.track_9_id_319["LED_feedback_active"] = ""
		self.track_9_id_319["LED_on"] = "127"
		self.track_9_id_319["LED_off"] = "0"
		self.track_9_id_319["LED_send_feedback_to_selected"] = []
		self.track_9_id_319["json_id"] = 319
		self.track_9_id_319["mapping_name"] = "Track 9"
		self.track_9_id_319["mapping_type"] = "Track"
		self.track_9_id_319["parent_json_id"] = 169
		self.track_9_id_319["parent_name"] = "mode_2_id_169"
		self.track_10_id_320 = {}
		self.track_10_id_320["track"] = self.track_num(2)
		self.track_10_id_320["module"] = "self.song().tracks[self.track_num(9)]"
		self.track_10_id_320["LED_mapping_type_needs_feedback"] = ""
		self.track_10_id_320["LED_feedback"] = "custom"
		self.track_10_id_320["LED_feedback_active"] = ""
		self.track_10_id_320["LED_on"] = "127"
		self.track_10_id_320["LED_off"] = "0"
		self.track_10_id_320["LED_send_feedback_to_selected"] = []
		self.track_10_id_320["json_id"] = 320
		self.track_10_id_320["mapping_name"] = "Track 10"
		self.track_10_id_320["mapping_type"] = "Track"
		self.track_10_id_320["parent_json_id"] = 169
		self.track_10_id_320["parent_name"] = "mode_2_id_169"
		self.track_11_id_321 = {}
		self.track_11_id_321["track"] = self.track_num(2)
		self.track_11_id_321["module"] = "self.song().tracks[self.track_num(10)]"
		self.track_11_id_321["LED_mapping_type_needs_feedback"] = ""
		self.track_11_id_321["LED_feedback"] = "custom"
		self.track_11_id_321["LED_feedback_active"] = ""
		self.track_11_id_321["LED_on"] = "127"
		self.track_11_id_321["LED_off"] = "0"
		self.track_11_id_321["LED_send_feedback_to_selected"] = []
		self.track_11_id_321["json_id"] = 321
		self.track_11_id_321["mapping_name"] = "Track 11"
		self.track_11_id_321["mapping_type"] = "Track"
		self.track_11_id_321["parent_json_id"] = 169
		self.track_11_id_321["parent_name"] = "mode_2_id_169"
		self.track_12_id_322 = {}
		self.track_12_id_322["track"] = self.track_num(2)
		self.track_12_id_322["module"] = "self.song().tracks[self.track_num(11)]"
		self.track_12_id_322["LED_mapping_type_needs_feedback"] = ""
		self.track_12_id_322["LED_feedback"] = "custom"
		self.track_12_id_322["LED_feedback_active"] = ""
		self.track_12_id_322["LED_on"] = "127"
		self.track_12_id_322["LED_off"] = "0"
		self.track_12_id_322["LED_send_feedback_to_selected"] = []
		self.track_12_id_322["json_id"] = 322
		self.track_12_id_322["mapping_name"] = "Track 12"
		self.track_12_id_322["mapping_type"] = "Track"
		self.track_12_id_322["parent_json_id"] = 169
		self.track_12_id_322["parent_name"] = "mode_2_id_169"
		self.track_13_id_323 = {}
		self.track_13_id_323["track"] = self.track_num(2)
		self.track_13_id_323["module"] = "self.song().tracks[self.track_num(12)]"
		self.track_13_id_323["LED_mapping_type_needs_feedback"] = ""
		self.track_13_id_323["LED_feedback"] = "custom"
		self.track_13_id_323["LED_feedback_active"] = ""
		self.track_13_id_323["LED_on"] = "127"
		self.track_13_id_323["LED_off"] = "0"
		self.track_13_id_323["LED_send_feedback_to_selected"] = []
		self.track_13_id_323["json_id"] = 323
		self.track_13_id_323["mapping_name"] = "Track 13"
		self.track_13_id_323["mapping_type"] = "Track"
		self.track_13_id_323["parent_json_id"] = 169
		self.track_13_id_323["parent_name"] = "mode_2_id_169"
		self.track_14_id_324 = {}
		self.track_14_id_324["track"] = self.track_num(2)
		self.track_14_id_324["module"] = "self.song().tracks[self.track_num(13)]"
		self.track_14_id_324["LED_mapping_type_needs_feedback"] = ""
		self.track_14_id_324["LED_feedback"] = "custom"
		self.track_14_id_324["LED_feedback_active"] = ""
		self.track_14_id_324["LED_on"] = "127"
		self.track_14_id_324["LED_off"] = "0"
		self.track_14_id_324["LED_send_feedback_to_selected"] = []
		self.track_14_id_324["json_id"] = 324
		self.track_14_id_324["mapping_name"] = "Track 14"
		self.track_14_id_324["mapping_type"] = "Track"
		self.track_14_id_324["parent_json_id"] = 169
		self.track_14_id_324["parent_name"] = "mode_2_id_169"
		self.track_15_id_325 = {}
		self.track_15_id_325["track"] = self.track_num(2)
		self.track_15_id_325["module"] = "self.song().tracks[self.track_num(14)]"
		self.track_15_id_325["LED_mapping_type_needs_feedback"] = ""
		self.track_15_id_325["LED_feedback"] = "custom"
		self.track_15_id_325["LED_feedback_active"] = ""
		self.track_15_id_325["LED_on"] = "127"
		self.track_15_id_325["LED_off"] = "0"
		self.track_15_id_325["LED_send_feedback_to_selected"] = []
		self.track_15_id_325["json_id"] = 325
		self.track_15_id_325["mapping_name"] = "Track 15"
		self.track_15_id_325["mapping_type"] = "Track"
		self.track_15_id_325["parent_json_id"] = 169
		self.track_15_id_325["parent_name"] = "mode_2_id_169"
		self.track_16_id_326 = {}
		self.track_16_id_326["track"] = self.track_num(2)
		self.track_16_id_326["module"] = "self.song().tracks[self.track_num(15)]"
		self.track_16_id_326["LED_mapping_type_needs_feedback"] = ""
		self.track_16_id_326["LED_feedback"] = "custom"
		self.track_16_id_326["LED_feedback_active"] = ""
		self.track_16_id_326["LED_on"] = "127"
		self.track_16_id_326["LED_off"] = "0"
		self.track_16_id_326["LED_send_feedback_to_selected"] = []
		self.track_16_id_326["json_id"] = 326
		self.track_16_id_326["mapping_name"] = "Track 16"
		self.track_16_id_326["mapping_type"] = "Track"
		self.track_16_id_326["parent_json_id"] = 169
		self.track_16_id_326["parent_name"] = "mode_2_id_169"
		self.solo_1_id_328 = {}
		self.solo_1_id_328["attached_to"] = "midi_cc_ch_0_val_94"
		self.solo_1_id_328["track"] = self.track_num(2)
		self.solo_1_id_328["module"] = "self.song().tracks[self.track_num(0)]"
		self.solo_1_id_328["element"] = "solo"
		self.solo_1_id_328["output_type"] = "bool"
		self.solo_1_id_328["ui_listener"] = "solo"
		self.solo_1_id_328["feedback_brain"] = "feedback_bool"
		self.solo_1_id_328["enc_first"] = 127
		self.solo_1_id_328["enc_second"] = 0
		self.solo_1_id_328["switch_type"] = "toggle"
		self.solo_1_id_328["ctrl_type"] = "on/off"
		self.solo_1_id_328["LED_mapping_type_needs_feedback"] = "1"
		self.solo_1_id_328["LED_feedback"] = "default"
		self.solo_1_id_328["LED_feedback_active"] = "1"
		self.solo_1_id_328["LED_on"] = "127"
		self.solo_1_id_328["LED_off"] = "0"
		self.solo_1_id_328["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_94"]
		self.solo_1_id_328["json_id"] = 328
		self.solo_1_id_328["mapping_name"] = "Solo 1"
		self.solo_1_id_328["mapping_type"] = "Solo"
		self.solo_1_id_328["parent_json_id"] = 308
		self.solo_1_id_328["parent_name"] = "track_1_id_308"
		self.solo_2_id_329 = {}
		self.solo_2_id_329["attached_to"] = "midi_cc_ch_1_val_94"
		self.solo_2_id_329["track"] = self.track_num(2)
		self.solo_2_id_329["module"] = "self.song().tracks[self.track_num(1)]"
		self.solo_2_id_329["element"] = "solo"
		self.solo_2_id_329["output_type"] = "bool"
		self.solo_2_id_329["ui_listener"] = "solo"
		self.solo_2_id_329["feedback_brain"] = "feedback_bool"
		self.solo_2_id_329["enc_first"] = 127
		self.solo_2_id_329["enc_second"] = 0
		self.solo_2_id_329["switch_type"] = "toggle"
		self.solo_2_id_329["ctrl_type"] = "on/off"
		self.solo_2_id_329["LED_mapping_type_needs_feedback"] = "1"
		self.solo_2_id_329["LED_feedback"] = "default"
		self.solo_2_id_329["LED_feedback_active"] = "1"
		self.solo_2_id_329["LED_on"] = "127"
		self.solo_2_id_329["LED_off"] = "0"
		self.solo_2_id_329["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_94"]
		self.solo_2_id_329["json_id"] = 329
		self.solo_2_id_329["mapping_name"] = "Solo 2"
		self.solo_2_id_329["mapping_type"] = "Solo"
		self.solo_2_id_329["parent_json_id"] = 309
		self.solo_2_id_329["parent_name"] = "track_2_id_309"
		self.solo_3_id_330 = {}
		self.solo_3_id_330["attached_to"] = "midi_cc_ch_2_val_94"
		self.solo_3_id_330["track"] = self.track_num(2)
		self.solo_3_id_330["module"] = "self.song().tracks[self.track_num(2)]"
		self.solo_3_id_330["element"] = "solo"
		self.solo_3_id_330["output_type"] = "bool"
		self.solo_3_id_330["ui_listener"] = "solo"
		self.solo_3_id_330["feedback_brain"] = "feedback_bool"
		self.solo_3_id_330["enc_first"] = 127
		self.solo_3_id_330["enc_second"] = 0
		self.solo_3_id_330["switch_type"] = "toggle"
		self.solo_3_id_330["ctrl_type"] = "on/off"
		self.solo_3_id_330["LED_mapping_type_needs_feedback"] = "1"
		self.solo_3_id_330["LED_feedback"] = "default"
		self.solo_3_id_330["LED_feedback_active"] = "1"
		self.solo_3_id_330["LED_on"] = "127"
		self.solo_3_id_330["LED_off"] = "0"
		self.solo_3_id_330["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_94"]
		self.solo_3_id_330["json_id"] = 330
		self.solo_3_id_330["mapping_name"] = "Solo 3"
		self.solo_3_id_330["mapping_type"] = "Solo"
		self.solo_3_id_330["parent_json_id"] = 310
		self.solo_3_id_330["parent_name"] = "track_3_id_310"
		self.solo_4_id_331 = {}
		self.solo_4_id_331["attached_to"] = "midi_cc_ch_3_val_94"
		self.solo_4_id_331["track"] = self.track_num(2)
		self.solo_4_id_331["module"] = "self.song().tracks[self.track_num(3)]"
		self.solo_4_id_331["element"] = "solo"
		self.solo_4_id_331["output_type"] = "bool"
		self.solo_4_id_331["ui_listener"] = "solo"
		self.solo_4_id_331["feedback_brain"] = "feedback_bool"
		self.solo_4_id_331["enc_first"] = 127
		self.solo_4_id_331["enc_second"] = 0
		self.solo_4_id_331["switch_type"] = "toggle"
		self.solo_4_id_331["ctrl_type"] = "on/off"
		self.solo_4_id_331["LED_mapping_type_needs_feedback"] = "1"
		self.solo_4_id_331["LED_feedback"] = "default"
		self.solo_4_id_331["LED_feedback_active"] = "1"
		self.solo_4_id_331["LED_on"] = "127"
		self.solo_4_id_331["LED_off"] = "0"
		self.solo_4_id_331["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_94"]
		self.solo_4_id_331["json_id"] = 331
		self.solo_4_id_331["mapping_name"] = "Solo 4"
		self.solo_4_id_331["mapping_type"] = "Solo"
		self.solo_4_id_331["parent_json_id"] = 311
		self.solo_4_id_331["parent_name"] = "track_4_id_311"
		self.solo_5_id_332 = {}
		self.solo_5_id_332["attached_to"] = "midi_cc_ch_4_val_94"
		self.solo_5_id_332["track"] = self.track_num(2)
		self.solo_5_id_332["module"] = "self.song().tracks[self.track_num(4)]"
		self.solo_5_id_332["element"] = "solo"
		self.solo_5_id_332["output_type"] = "bool"
		self.solo_5_id_332["ui_listener"] = "solo"
		self.solo_5_id_332["feedback_brain"] = "feedback_bool"
		self.solo_5_id_332["enc_first"] = 127
		self.solo_5_id_332["enc_second"] = 0
		self.solo_5_id_332["switch_type"] = "toggle"
		self.solo_5_id_332["ctrl_type"] = "on/off"
		self.solo_5_id_332["LED_mapping_type_needs_feedback"] = "1"
		self.solo_5_id_332["LED_feedback"] = "default"
		self.solo_5_id_332["LED_feedback_active"] = "1"
		self.solo_5_id_332["LED_on"] = "127"
		self.solo_5_id_332["LED_off"] = "0"
		self.solo_5_id_332["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_94"]
		self.solo_5_id_332["json_id"] = 332
		self.solo_5_id_332["mapping_name"] = "Solo 5"
		self.solo_5_id_332["mapping_type"] = "Solo"
		self.solo_5_id_332["parent_json_id"] = 312
		self.solo_5_id_332["parent_name"] = "track_5_id_312"
		self.solo_6_id_333 = {}
		self.solo_6_id_333["attached_to"] = "midi_cc_ch_5_val_94"
		self.solo_6_id_333["track"] = self.track_num(2)
		self.solo_6_id_333["module"] = "self.song().tracks[self.track_num(5)]"
		self.solo_6_id_333["element"] = "solo"
		self.solo_6_id_333["output_type"] = "bool"
		self.solo_6_id_333["ui_listener"] = "solo"
		self.solo_6_id_333["feedback_brain"] = "feedback_bool"
		self.solo_6_id_333["enc_first"] = 127
		self.solo_6_id_333["enc_second"] = 0
		self.solo_6_id_333["switch_type"] = "toggle"
		self.solo_6_id_333["ctrl_type"] = "on/off"
		self.solo_6_id_333["LED_mapping_type_needs_feedback"] = "1"
		self.solo_6_id_333["LED_feedback"] = "default"
		self.solo_6_id_333["LED_feedback_active"] = "1"
		self.solo_6_id_333["LED_on"] = "127"
		self.solo_6_id_333["LED_off"] = "0"
		self.solo_6_id_333["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_94"]
		self.solo_6_id_333["json_id"] = 333
		self.solo_6_id_333["mapping_name"] = "Solo 6"
		self.solo_6_id_333["mapping_type"] = "Solo"
		self.solo_6_id_333["parent_json_id"] = 313
		self.solo_6_id_333["parent_name"] = "track_6_id_313"
		self.solo_7_id_334 = {}
		self.solo_7_id_334["attached_to"] = "midi_cc_ch_6_val_94"
		self.solo_7_id_334["track"] = self.track_num(2)
		self.solo_7_id_334["module"] = "self.song().tracks[self.track_num(6)]"
		self.solo_7_id_334["element"] = "solo"
		self.solo_7_id_334["output_type"] = "bool"
		self.solo_7_id_334["ui_listener"] = "solo"
		self.solo_7_id_334["feedback_brain"] = "feedback_bool"
		self.solo_7_id_334["enc_first"] = 127
		self.solo_7_id_334["enc_second"] = 0
		self.solo_7_id_334["switch_type"] = "toggle"
		self.solo_7_id_334["ctrl_type"] = "on/off"
		self.solo_7_id_334["LED_mapping_type_needs_feedback"] = "1"
		self.solo_7_id_334["LED_feedback"] = "default"
		self.solo_7_id_334["LED_feedback_active"] = "1"
		self.solo_7_id_334["LED_on"] = "127"
		self.solo_7_id_334["LED_off"] = "0"
		self.solo_7_id_334["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_94"]
		self.solo_7_id_334["json_id"] = 334
		self.solo_7_id_334["mapping_name"] = "Solo 7"
		self.solo_7_id_334["mapping_type"] = "Solo"
		self.solo_7_id_334["parent_json_id"] = 314
		self.solo_7_id_334["parent_name"] = "track_7_id_314"
		self.solo_8_id_335 = {}
		self.solo_8_id_335["attached_to"] = "midi_cc_ch_7_val_94"
		self.solo_8_id_335["track"] = self.track_num(2)
		self.solo_8_id_335["module"] = "self.song().tracks[self.track_num(7)]"
		self.solo_8_id_335["element"] = "solo"
		self.solo_8_id_335["output_type"] = "bool"
		self.solo_8_id_335["ui_listener"] = "solo"
		self.solo_8_id_335["feedback_brain"] = "feedback_bool"
		self.solo_8_id_335["enc_first"] = 127
		self.solo_8_id_335["enc_second"] = 0
		self.solo_8_id_335["switch_type"] = "toggle"
		self.solo_8_id_335["ctrl_type"] = "on/off"
		self.solo_8_id_335["LED_mapping_type_needs_feedback"] = "1"
		self.solo_8_id_335["LED_feedback"] = "default"
		self.solo_8_id_335["LED_feedback_active"] = "1"
		self.solo_8_id_335["LED_on"] = "127"
		self.solo_8_id_335["LED_off"] = "0"
		self.solo_8_id_335["LED_send_feedback_to_selected"] = ["midi_cc_ch_7_val_94"]
		self.solo_8_id_335["json_id"] = 335
		self.solo_8_id_335["mapping_name"] = "Solo 8"
		self.solo_8_id_335["mapping_type"] = "Solo"
		self.solo_8_id_335["parent_json_id"] = 315
		self.solo_8_id_335["parent_name"] = "track_8_id_315"
		self.solo_9_id_336 = {}
		self.solo_9_id_336["attached_to"] = "midi_cc_ch_8_val_94"
		self.solo_9_id_336["track"] = self.track_num(2)
		self.solo_9_id_336["module"] = "self.song().tracks[self.track_num(8)]"
		self.solo_9_id_336["element"] = "solo"
		self.solo_9_id_336["output_type"] = "bool"
		self.solo_9_id_336["ui_listener"] = "solo"
		self.solo_9_id_336["feedback_brain"] = "feedback_bool"
		self.solo_9_id_336["enc_first"] = 127
		self.solo_9_id_336["enc_second"] = 0
		self.solo_9_id_336["switch_type"] = "toggle"
		self.solo_9_id_336["ctrl_type"] = "on/off"
		self.solo_9_id_336["LED_mapping_type_needs_feedback"] = "1"
		self.solo_9_id_336["LED_feedback"] = "default"
		self.solo_9_id_336["LED_feedback_active"] = "1"
		self.solo_9_id_336["LED_on"] = "127"
		self.solo_9_id_336["LED_off"] = "0"
		self.solo_9_id_336["LED_send_feedback_to_selected"] = ["midi_cc_ch_8_val_94"]
		self.solo_9_id_336["json_id"] = 336
		self.solo_9_id_336["mapping_name"] = "Solo 9"
		self.solo_9_id_336["mapping_type"] = "Solo"
		self.solo_9_id_336["parent_json_id"] = 319
		self.solo_9_id_336["parent_name"] = "track_9_id_319"
		self.solo_10_id_337 = {}
		self.solo_10_id_337["attached_to"] = "midi_cc_ch_9_val_94"
		self.solo_10_id_337["track"] = self.track_num(2)
		self.solo_10_id_337["module"] = "self.song().tracks[self.track_num(9)]"
		self.solo_10_id_337["element"] = "solo"
		self.solo_10_id_337["output_type"] = "bool"
		self.solo_10_id_337["ui_listener"] = "solo"
		self.solo_10_id_337["feedback_brain"] = "feedback_bool"
		self.solo_10_id_337["enc_first"] = 127
		self.solo_10_id_337["enc_second"] = 0
		self.solo_10_id_337["switch_type"] = "toggle"
		self.solo_10_id_337["ctrl_type"] = "on/off"
		self.solo_10_id_337["LED_mapping_type_needs_feedback"] = "1"
		self.solo_10_id_337["LED_feedback"] = "default"
		self.solo_10_id_337["LED_feedback_active"] = "1"
		self.solo_10_id_337["LED_on"] = "127"
		self.solo_10_id_337["LED_off"] = "0"
		self.solo_10_id_337["LED_send_feedback_to_selected"] = ["midi_cc_ch_9_val_94"]
		self.solo_10_id_337["json_id"] = 337
		self.solo_10_id_337["mapping_name"] = "Solo 10"
		self.solo_10_id_337["mapping_type"] = "Solo"
		self.solo_10_id_337["parent_json_id"] = 320
		self.solo_10_id_337["parent_name"] = "track_10_id_320"
		self.solo_11_id_338 = {}
		self.solo_11_id_338["attached_to"] = "midi_cc_ch_10_val_94"
		self.solo_11_id_338["track"] = self.track_num(2)
		self.solo_11_id_338["module"] = "self.song().tracks[self.track_num(10)]"
		self.solo_11_id_338["element"] = "solo"
		self.solo_11_id_338["output_type"] = "bool"
		self.solo_11_id_338["ui_listener"] = "solo"
		self.solo_11_id_338["feedback_brain"] = "feedback_bool"
		self.solo_11_id_338["enc_first"] = 127
		self.solo_11_id_338["enc_second"] = 0
		self.solo_11_id_338["switch_type"] = "toggle"
		self.solo_11_id_338["ctrl_type"] = "on/off"
		self.solo_11_id_338["LED_mapping_type_needs_feedback"] = "1"
		self.solo_11_id_338["LED_feedback"] = "default"
		self.solo_11_id_338["LED_feedback_active"] = "1"
		self.solo_11_id_338["LED_on"] = "127"
		self.solo_11_id_338["LED_off"] = "0"
		self.solo_11_id_338["LED_send_feedback_to_selected"] = ["midi_cc_ch_10_val_94"]
		self.solo_11_id_338["json_id"] = 338
		self.solo_11_id_338["mapping_name"] = "Solo 11"
		self.solo_11_id_338["mapping_type"] = "Solo"
		self.solo_11_id_338["parent_json_id"] = 321
		self.solo_11_id_338["parent_name"] = "track_11_id_321"
		self.solo_12_id_339 = {}
		self.solo_12_id_339["attached_to"] = "midi_cc_ch_11_val_94"
		self.solo_12_id_339["track"] = self.track_num(2)
		self.solo_12_id_339["module"] = "self.song().tracks[self.track_num(11)]"
		self.solo_12_id_339["element"] = "solo"
		self.solo_12_id_339["output_type"] = "bool"
		self.solo_12_id_339["ui_listener"] = "solo"
		self.solo_12_id_339["feedback_brain"] = "feedback_bool"
		self.solo_12_id_339["enc_first"] = 127
		self.solo_12_id_339["enc_second"] = 0
		self.solo_12_id_339["switch_type"] = "toggle"
		self.solo_12_id_339["ctrl_type"] = "on/off"
		self.solo_12_id_339["LED_mapping_type_needs_feedback"] = "1"
		self.solo_12_id_339["LED_feedback"] = "default"
		self.solo_12_id_339["LED_feedback_active"] = "1"
		self.solo_12_id_339["LED_on"] = "127"
		self.solo_12_id_339["LED_off"] = "0"
		self.solo_12_id_339["LED_send_feedback_to_selected"] = ["midi_cc_ch_11_val_94"]
		self.solo_12_id_339["json_id"] = 339
		self.solo_12_id_339["mapping_name"] = "Solo 12"
		self.solo_12_id_339["mapping_type"] = "Solo"
		self.solo_12_id_339["parent_json_id"] = 322
		self.solo_12_id_339["parent_name"] = "track_12_id_322"
		self.solo_13_id_340 = {}
		self.solo_13_id_340["attached_to"] = "midi_cc_ch_12_val_94"
		self.solo_13_id_340["track"] = self.track_num(2)
		self.solo_13_id_340["module"] = "self.song().tracks[self.track_num(12)]"
		self.solo_13_id_340["element"] = "solo"
		self.solo_13_id_340["output_type"] = "bool"
		self.solo_13_id_340["ui_listener"] = "solo"
		self.solo_13_id_340["feedback_brain"] = "feedback_bool"
		self.solo_13_id_340["enc_first"] = 127
		self.solo_13_id_340["enc_second"] = 0
		self.solo_13_id_340["switch_type"] = "toggle"
		self.solo_13_id_340["ctrl_type"] = "on/off"
		self.solo_13_id_340["LED_mapping_type_needs_feedback"] = "1"
		self.solo_13_id_340["LED_feedback"] = "default"
		self.solo_13_id_340["LED_feedback_active"] = "1"
		self.solo_13_id_340["LED_on"] = "127"
		self.solo_13_id_340["LED_off"] = "0"
		self.solo_13_id_340["LED_send_feedback_to_selected"] = ["midi_cc_ch_12_val_94"]
		self.solo_13_id_340["json_id"] = 340
		self.solo_13_id_340["mapping_name"] = "Solo 13"
		self.solo_13_id_340["mapping_type"] = "Solo"
		self.solo_13_id_340["parent_json_id"] = 323
		self.solo_13_id_340["parent_name"] = "track_13_id_323"
		self.solo_14_id_341 = {}
		self.solo_14_id_341["attached_to"] = "midi_cc_ch_13_val_94"
		self.solo_14_id_341["track"] = self.track_num(2)
		self.solo_14_id_341["module"] = "self.song().tracks[self.track_num(13)]"
		self.solo_14_id_341["element"] = "solo"
		self.solo_14_id_341["output_type"] = "bool"
		self.solo_14_id_341["ui_listener"] = "solo"
		self.solo_14_id_341["feedback_brain"] = "feedback_bool"
		self.solo_14_id_341["enc_first"] = 127
		self.solo_14_id_341["enc_second"] = 0
		self.solo_14_id_341["switch_type"] = "toggle"
		self.solo_14_id_341["ctrl_type"] = "on/off"
		self.solo_14_id_341["LED_mapping_type_needs_feedback"] = "1"
		self.solo_14_id_341["LED_feedback"] = "default"
		self.solo_14_id_341["LED_feedback_active"] = "1"
		self.solo_14_id_341["LED_on"] = "127"
		self.solo_14_id_341["LED_off"] = "0"
		self.solo_14_id_341["LED_send_feedback_to_selected"] = ["midi_cc_ch_13_val_94"]
		self.solo_14_id_341["json_id"] = 341
		self.solo_14_id_341["mapping_name"] = "Solo 14"
		self.solo_14_id_341["mapping_type"] = "Solo"
		self.solo_14_id_341["parent_json_id"] = 324
		self.solo_14_id_341["parent_name"] = "track_14_id_324"
		self.solo_15_id_342 = {}
		self.solo_15_id_342["attached_to"] = "midi_cc_ch_14_val_94"
		self.solo_15_id_342["track"] = self.track_num(2)
		self.solo_15_id_342["module"] = "self.song().tracks[self.track_num(14)]"
		self.solo_15_id_342["element"] = "solo"
		self.solo_15_id_342["output_type"] = "bool"
		self.solo_15_id_342["ui_listener"] = "solo"
		self.solo_15_id_342["feedback_brain"] = "feedback_bool"
		self.solo_15_id_342["enc_first"] = 127
		self.solo_15_id_342["enc_second"] = 0
		self.solo_15_id_342["switch_type"] = "toggle"
		self.solo_15_id_342["ctrl_type"] = "on/off"
		self.solo_15_id_342["LED_mapping_type_needs_feedback"] = "1"
		self.solo_15_id_342["LED_feedback"] = "default"
		self.solo_15_id_342["LED_feedback_active"] = "1"
		self.solo_15_id_342["LED_on"] = "127"
		self.solo_15_id_342["LED_off"] = "0"
		self.solo_15_id_342["LED_send_feedback_to_selected"] = ["midi_cc_ch_14_val_94"]
		self.solo_15_id_342["json_id"] = 342
		self.solo_15_id_342["mapping_name"] = "Solo 15"
		self.solo_15_id_342["mapping_type"] = "Solo"
		self.solo_15_id_342["parent_json_id"] = 325
		self.solo_15_id_342["parent_name"] = "track_15_id_325"
		self.solo_16_id_343 = {}
		self.solo_16_id_343["attached_to"] = "midi_cc_ch_15_val_94"
		self.solo_16_id_343["track"] = self.track_num(2)
		self.solo_16_id_343["module"] = "self.song().tracks[self.track_num(15)]"
		self.solo_16_id_343["element"] = "solo"
		self.solo_16_id_343["output_type"] = "bool"
		self.solo_16_id_343["ui_listener"] = "solo"
		self.solo_16_id_343["feedback_brain"] = "feedback_bool"
		self.solo_16_id_343["enc_first"] = 127
		self.solo_16_id_343["enc_second"] = 0
		self.solo_16_id_343["switch_type"] = "toggle"
		self.solo_16_id_343["ctrl_type"] = "on/off"
		self.solo_16_id_343["LED_mapping_type_needs_feedback"] = "1"
		self.solo_16_id_343["LED_feedback"] = "default"
		self.solo_16_id_343["LED_feedback_active"] = "1"
		self.solo_16_id_343["LED_on"] = "127"
		self.solo_16_id_343["LED_off"] = "0"
		self.solo_16_id_343["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_94"]
		self.solo_16_id_343["json_id"] = 343
		self.solo_16_id_343["mapping_name"] = "Solo 16"
		self.solo_16_id_343["mapping_type"] = "Solo"
		self.solo_16_id_343["parent_json_id"] = 326
		self.solo_16_id_343["parent_name"] = "track_16_id_326"
		self.mode_selector_1_copy_id_346 = {}
		self.mode_selector_1_copy_id_346["attached_to"] = "midi_cc_ch_15_val_120"
		self.mode_selector_1_copy_id_346["module"] = "self"
		self.mode_selector_1_copy_id_346["element"] = "scroll_modes"
		self.mode_selector_1_copy_id_346["output_type"] = "func"
		self.mode_selector_1_copy_id_346["func_arg"] = "cnfg"
		self.mode_selector_1_copy_id_346["ui_listener"] = "value"
		self.mode_selector_1_copy_id_346["feedback_brain"] = "feedback_scroll_mode_selector"
		self.mode_selector_1_copy_id_346["ctrl_type"] = "absolute"
		self.mode_selector_1_copy_id_346["takeover_mode"] = "Value scaling"
		self.mode_selector_1_copy_id_346["enc_first"] = 0
		self.mode_selector_1_copy_id_346["enc_second"] = 127
		self.mode_selector_1_copy_id_346["reverse_mode"] = False
		self.mode_selector_1_copy_id_346["steps"] = 1
		self.mode_selector_1_copy_id_346["LED_mapping_type_needs_feedback"] = "1"
		self.mode_selector_1_copy_id_346["LED_feedback"] = "default"
		self.mode_selector_1_copy_id_346["LED_feedback_active"] = "1"
		self.mode_selector_1_copy_id_346["LED_on"] = "127"
		self.mode_selector_1_copy_id_346["LED_off"] = "0"
		self.mode_selector_1_copy_id_346["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_120"]
		self.mode_selector_1_copy_id_346["json_id"] = 346
		self.mode_selector_1_copy_id_346["mapping_name"] = "Mode Selector 1 copy"
		self.mode_selector_1_copy_id_346["mapping_type"] = "Mode Selector"
		self.mode_selector_1_copy_id_346["parent_json_id"] = 169
		self.mode_selector_1_copy_id_346["parent_name"] = "mode_2_id_169"

	def _mode1_led_listeners(self):
		try:
			self._mode1_fire_all_feedback()
		except:
			self.log("_mode1_led_listeners tried to call _mode1_fire_all_feedback but it does not exist")
		try:
			self.song().add_tracks_listener(self._all_tracks_listener)
		except:
			self.log("_mode1_led_listeners tried to call add_tracks_listener but it does not exist")
		try:
			self.all_track_device_listeners()
		except:
			self.log("_mode1_led_listeners tried to call all_track_device_listeners but it does not exist")
		try:
			self._mode1_ui_listeners()
		except:
			self.log("_mode1_led_listeners tried to call _mode1_ui_listeners but it does not exist")
		self.track_feedback(1)
		self.device_feedback(1)
		self.mode_device_bank_leds(1)

	def _mode169_led_listeners(self):
		try:
			self._mode169_fire_all_feedback()
		except:
			self.log("_mode169_led_listeners tried to call _mode169_fire_all_feedback but it does not exist")
		try:
			self.song().add_tracks_listener(self._all_tracks_listener)
		except:
			self.log("_mode169_led_listeners tried to call add_tracks_listener but it does not exist")
		try:
			self.all_track_device_listeners()
		except:
			self.log("_mode169_led_listeners tried to call all_track_device_listeners but it does not exist")
		try:
			self._mode169_ui_listeners()
		except:
			self.log("_mode169_led_listeners tried to call _mode169_ui_listeners but it does not exist")
		self.track_feedback(169)
		self.device_feedback(169)
		self.mode_device_bank_leds(169)

	def _remove_mode1_led_listeners(self):
		try:
			self.song().remove_tracks_listener(self._all_tracks_listener)
		except:
			self.log("_remove_mode1_led_listeners tried to call remove_tracks_listener but it does not exist")
		try:
			self._remove_all_track_device_listeners()
		except:
			self.log("_remove_mode1_led_listeners tried to call _remove_all_track_device_listeners but it does not exist")
		try:
			self._remove_mode1_ui_listeners()
		except:
			self.log("_remove_mode1_led_listeners tried to call _remove_mode1_ui_listeners but it does not exist")
		self.turn_inputs_off()

	def _remove_mode169_led_listeners(self):
		try:
			self.song().remove_tracks_listener(self._all_tracks_listener)
		except:
			self.log("_remove_mode169_led_listeners tried to call remove_tracks_listener but it does not exist")
		try:
			self._remove_all_track_device_listeners()
		except:
			self.log("_remove_mode169_led_listeners tried to call _remove_all_track_device_listeners but it does not exist")
		try:
			self._remove_mode169_ui_listeners()
		except:
			self.log("_remove_mode169_led_listeners tried to call _remove_mode169_ui_listeners but it does not exist")
		self.turn_inputs_off()

	def _mode1_ui_listeners(self):
		try:
			self.volume_1_id_3_led = eval(self.volume_1_id_3["module"])
			self.volume_1_id_3_led.add_value_listener(self.volume_1_id_3_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_1_id_3["element"]) + " does not exist")
		try:
			self.pan_1_id_4_led = eval(self.pan_1_id_4["module"])
			self.pan_1_id_4_led.add_value_listener(self.pan_1_id_4_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_1_id_4["element"]) + " does not exist")
		try:
			self.mute_1_id_5_led = eval(self.mute_1_id_5["module"])
			self.mute_1_id_5_led.add_mute_listener(self.mute_1_id_5_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_1_id_5["element"]) + " does not exist")
		try:
			self.send_1_id_8_led = eval(self.send_1_id_8["module"])
			self.send_1_id_8_led.add_value_listener(self.send_1_id_8_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_8["element"]) + " does not exist")
		try:
			self.send_2_id_9_led = eval(self.send_2_id_9["module"])
			self.send_2_id_9_led.add_value_listener(self.send_2_id_9_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_9["element"]) + " does not exist")
		try:
			self.send_3_id_10_led = eval(self.send_3_id_10["module"])
			self.send_3_id_10_led.add_value_listener(self.send_3_id_10_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_10["element"]) + " does not exist")
		try:
			self.send_4_id_11_led = eval(self.send_4_id_11["module"])
			self.send_4_id_11_led.add_value_listener(self.send_4_id_11_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_11["element"]) + " does not exist")
		try:
			self.send_1_id_13_led = eval(self.send_1_id_13["module"])
			self.send_1_id_13_led.add_value_listener(self.send_1_id_13_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_13["element"]) + " does not exist")
		try:
			self.send_2_id_14_led = eval(self.send_2_id_14["module"])
			self.send_2_id_14_led.add_value_listener(self.send_2_id_14_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_14["element"]) + " does not exist")
		try:
			self.send_3_id_15_led = eval(self.send_3_id_15["module"])
			self.send_3_id_15_led.add_value_listener(self.send_3_id_15_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_15["element"]) + " does not exist")
		try:
			self.send_4_id_16_led = eval(self.send_4_id_16["module"])
			self.send_4_id_16_led.add_value_listener(self.send_4_id_16_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_16["element"]) + " does not exist")
		try:
			self.volume_2_id_17_led = eval(self.volume_2_id_17["module"])
			self.volume_2_id_17_led.add_value_listener(self.volume_2_id_17_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_2_id_17["element"]) + " does not exist")
		try:
			self.pan_2_id_18_led = eval(self.pan_2_id_18["module"])
			self.pan_2_id_18_led.add_value_listener(self.pan_2_id_18_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_2_id_18["element"]) + " does not exist")
		try:
			self.mute_2_id_19_led = eval(self.mute_2_id_19["module"])
			self.mute_2_id_19_led.add_mute_listener(self.mute_2_id_19_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_2_id_19["element"]) + " does not exist")
		try:
			self.send_1_id_23_led = eval(self.send_1_id_23["module"])
			self.send_1_id_23_led.add_value_listener(self.send_1_id_23_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_23["element"]) + " does not exist")
		try:
			self.send_2_id_24_led = eval(self.send_2_id_24["module"])
			self.send_2_id_24_led.add_value_listener(self.send_2_id_24_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_24["element"]) + " does not exist")
		try:
			self.send_3_id_25_led = eval(self.send_3_id_25["module"])
			self.send_3_id_25_led.add_value_listener(self.send_3_id_25_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_25["element"]) + " does not exist")
		try:
			self.send_4_id_26_led = eval(self.send_4_id_26["module"])
			self.send_4_id_26_led.add_value_listener(self.send_4_id_26_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_26["element"]) + " does not exist")
		try:
			self.volume_3_id_27_led = eval(self.volume_3_id_27["module"])
			self.volume_3_id_27_led.add_value_listener(self.volume_3_id_27_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_3_id_27["element"]) + " does not exist")
		try:
			self.pan_3_id_28_led = eval(self.pan_3_id_28["module"])
			self.pan_3_id_28_led.add_value_listener(self.pan_3_id_28_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_3_id_28["element"]) + " does not exist")
		try:
			self.mute_3_id_29_led = eval(self.mute_3_id_29["module"])
			self.mute_3_id_29_led.add_mute_listener(self.mute_3_id_29_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_3_id_29["element"]) + " does not exist")
		try:
			self.send_1_id_33_led = eval(self.send_1_id_33["module"])
			self.send_1_id_33_led.add_value_listener(self.send_1_id_33_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_33["element"]) + " does not exist")
		try:
			self.send_2_id_34_led = eval(self.send_2_id_34["module"])
			self.send_2_id_34_led.add_value_listener(self.send_2_id_34_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_34["element"]) + " does not exist")
		try:
			self.send_3_id_35_led = eval(self.send_3_id_35["module"])
			self.send_3_id_35_led.add_value_listener(self.send_3_id_35_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_35["element"]) + " does not exist")
		try:
			self.send_4_id_36_led = eval(self.send_4_id_36["module"])
			self.send_4_id_36_led.add_value_listener(self.send_4_id_36_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_36["element"]) + " does not exist")
		try:
			self.volume_4_id_37_led = eval(self.volume_4_id_37["module"])
			self.volume_4_id_37_led.add_value_listener(self.volume_4_id_37_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_4_id_37["element"]) + " does not exist")
		try:
			self.pan_4_id_38_led = eval(self.pan_4_id_38["module"])
			self.pan_4_id_38_led.add_value_listener(self.pan_4_id_38_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_4_id_38["element"]) + " does not exist")
		try:
			self.mute_4_id_39_led = eval(self.mute_4_id_39["module"])
			self.mute_4_id_39_led.add_mute_listener(self.mute_4_id_39_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_4_id_39["element"]) + " does not exist")
		try:
			self.send_1_id_43_led = eval(self.send_1_id_43["module"])
			self.send_1_id_43_led.add_value_listener(self.send_1_id_43_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_43["element"]) + " does not exist")
		try:
			self.send_2_id_44_led = eval(self.send_2_id_44["module"])
			self.send_2_id_44_led.add_value_listener(self.send_2_id_44_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_44["element"]) + " does not exist")
		try:
			self.send_3_id_45_led = eval(self.send_3_id_45["module"])
			self.send_3_id_45_led.add_value_listener(self.send_3_id_45_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_45["element"]) + " does not exist")
		try:
			self.send_4_id_46_led = eval(self.send_4_id_46["module"])
			self.send_4_id_46_led.add_value_listener(self.send_4_id_46_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_46["element"]) + " does not exist")
		try:
			self.volume_5_id_47_led = eval(self.volume_5_id_47["module"])
			self.volume_5_id_47_led.add_value_listener(self.volume_5_id_47_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_5_id_47["element"]) + " does not exist")
		try:
			self.pan_5_id_48_led = eval(self.pan_5_id_48["module"])
			self.pan_5_id_48_led.add_value_listener(self.pan_5_id_48_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_5_id_48["element"]) + " does not exist")
		try:
			self.mute_5_id_49_led = eval(self.mute_5_id_49["module"])
			self.mute_5_id_49_led.add_mute_listener(self.mute_5_id_49_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_5_id_49["element"]) + " does not exist")
		try:
			self.send_1_id_53_led = eval(self.send_1_id_53["module"])
			self.send_1_id_53_led.add_value_listener(self.send_1_id_53_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_53["element"]) + " does not exist")
		try:
			self.send_2_id_54_led = eval(self.send_2_id_54["module"])
			self.send_2_id_54_led.add_value_listener(self.send_2_id_54_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_54["element"]) + " does not exist")
		try:
			self.send_3_id_55_led = eval(self.send_3_id_55["module"])
			self.send_3_id_55_led.add_value_listener(self.send_3_id_55_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_55["element"]) + " does not exist")
		try:
			self.send_4_id_56_led = eval(self.send_4_id_56["module"])
			self.send_4_id_56_led.add_value_listener(self.send_4_id_56_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_56["element"]) + " does not exist")
		try:
			self.volume_6_id_57_led = eval(self.volume_6_id_57["module"])
			self.volume_6_id_57_led.add_value_listener(self.volume_6_id_57_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_6_id_57["element"]) + " does not exist")
		try:
			self.pan_6_id_58_led = eval(self.pan_6_id_58["module"])
			self.pan_6_id_58_led.add_value_listener(self.pan_6_id_58_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_6_id_58["element"]) + " does not exist")
		try:
			self.mute_6_id_59_led = eval(self.mute_6_id_59["module"])
			self.mute_6_id_59_led.add_mute_listener(self.mute_6_id_59_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_6_id_59["element"]) + " does not exist")
		try:
			self.send_1_id_63_led = eval(self.send_1_id_63["module"])
			self.send_1_id_63_led.add_value_listener(self.send_1_id_63_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_63["element"]) + " does not exist")
		try:
			self.send_2_id_64_led = eval(self.send_2_id_64["module"])
			self.send_2_id_64_led.add_value_listener(self.send_2_id_64_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_64["element"]) + " does not exist")
		try:
			self.send_3_id_65_led = eval(self.send_3_id_65["module"])
			self.send_3_id_65_led.add_value_listener(self.send_3_id_65_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_65["element"]) + " does not exist")
		try:
			self.send_4_id_66_led = eval(self.send_4_id_66["module"])
			self.send_4_id_66_led.add_value_listener(self.send_4_id_66_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_66["element"]) + " does not exist")
		try:
			self.volume_7_id_67_led = eval(self.volume_7_id_67["module"])
			self.volume_7_id_67_led.add_value_listener(self.volume_7_id_67_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_7_id_67["element"]) + " does not exist")
		try:
			self.pan_7_id_68_led = eval(self.pan_7_id_68["module"])
			self.pan_7_id_68_led.add_value_listener(self.pan_7_id_68_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_7_id_68["element"]) + " does not exist")
		try:
			self.mute_7_id_69_led = eval(self.mute_7_id_69["module"])
			self.mute_7_id_69_led.add_mute_listener(self.mute_7_id_69_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_7_id_69["element"]) + " does not exist")
		try:
			self.send_1_id_73_led = eval(self.send_1_id_73["module"])
			self.send_1_id_73_led.add_value_listener(self.send_1_id_73_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_73["element"]) + " does not exist")
		try:
			self.send_2_id_74_led = eval(self.send_2_id_74["module"])
			self.send_2_id_74_led.add_value_listener(self.send_2_id_74_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_74["element"]) + " does not exist")
		try:
			self.send_3_id_75_led = eval(self.send_3_id_75["module"])
			self.send_3_id_75_led.add_value_listener(self.send_3_id_75_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_75["element"]) + " does not exist")
		try:
			self.send_4_id_76_led = eval(self.send_4_id_76["module"])
			self.send_4_id_76_led.add_value_listener(self.send_4_id_76_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_76["element"]) + " does not exist")
		try:
			self.volume_8_id_77_led = eval(self.volume_8_id_77["module"])
			self.volume_8_id_77_led.add_value_listener(self.volume_8_id_77_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_8_id_77["element"]) + " does not exist")
		try:
			self.pan_8_id_78_led = eval(self.pan_8_id_78["module"])
			self.pan_8_id_78_led.add_value_listener(self.pan_8_id_78_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_8_id_78["element"]) + " does not exist")
		try:
			self.mute_8_id_79_led = eval(self.mute_8_id_79["module"])
			self.mute_8_id_79_led.add_mute_listener(self.mute_8_id_79_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_8_id_79["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_1_id_88_led = eval(self.parameter_1_id_88["module"])
				self.parameter_1_id_88_led.add_value_listener(self.parameter_1_id_88_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_1_id_88["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_2_id_89_led = eval(self.parameter_2_id_89["module"])
				self.parameter_2_id_89_led.add_value_listener(self.parameter_2_id_89_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_2_id_89["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_3_id_90_led = eval(self.parameter_3_id_90["module"])
				self.parameter_3_id_90_led.add_value_listener(self.parameter_3_id_90_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_3_id_90["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_4_id_91_led = eval(self.parameter_4_id_91["module"])
				self.parameter_4_id_91_led.add_value_listener(self.parameter_4_id_91_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_4_id_91["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_5_id_92_led = eval(self.parameter_5_id_92["module"])
				self.parameter_5_id_92_led.add_value_listener(self.parameter_5_id_92_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_5_id_92["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_6_id_93_led = eval(self.parameter_6_id_93["module"])
				self.parameter_6_id_93_led.add_value_listener(self.parameter_6_id_93_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_6_id_93["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_7_id_94_led = eval(self.parameter_7_id_94["module"])
				self.parameter_7_id_94_led.add_value_listener(self.parameter_7_id_94_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_7_id_94["element"]) + " does not exist")
		if self.device_id_86_active_bank == 0:
			try:
				self.parameter_8_id_95_led = eval(self.parameter_8_id_95["module"])
				self.parameter_8_id_95_led.add_value_listener(self.parameter_8_id_95_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_8_id_95["element"]) + " does not exist")
		try:
			self.send_1_id_97_led = eval(self.send_1_id_97["module"])
			self.send_1_id_97_led.add_value_listener(self.send_1_id_97_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_97["element"]) + " does not exist")
		try:
			self.send_2_id_98_led = eval(self.send_2_id_98["module"])
			self.send_2_id_98_led.add_value_listener(self.send_2_id_98_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_98["element"]) + " does not exist")
		try:
			self.send_3_id_99_led = eval(self.send_3_id_99["module"])
			self.send_3_id_99_led.add_value_listener(self.send_3_id_99_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_99["element"]) + " does not exist")
		try:
			self.send_4_id_100_led = eval(self.send_4_id_100["module"])
			self.send_4_id_100_led.add_value_listener(self.send_4_id_100_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_100["element"]) + " does not exist")
		try:
			self.volume_9_id_101_led = eval(self.volume_9_id_101["module"])
			self.volume_9_id_101_led.add_value_listener(self.volume_9_id_101_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_9_id_101["element"]) + " does not exist")
		try:
			self.pan_9_id_102_led = eval(self.pan_9_id_102["module"])
			self.pan_9_id_102_led.add_value_listener(self.pan_9_id_102_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_9_id_102["element"]) + " does not exist")
		try:
			self.mute_9_id_103_led = eval(self.mute_9_id_103["module"])
			self.mute_9_id_103_led.add_mute_listener(self.mute_9_id_103_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_9_id_103["element"]) + " does not exist")
		try:
			self.send_1_id_106_led = eval(self.send_1_id_106["module"])
			self.send_1_id_106_led.add_value_listener(self.send_1_id_106_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_106["element"]) + " does not exist")
		try:
			self.send_2_id_107_led = eval(self.send_2_id_107["module"])
			self.send_2_id_107_led.add_value_listener(self.send_2_id_107_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_107["element"]) + " does not exist")
		try:
			self.send_3_id_108_led = eval(self.send_3_id_108["module"])
			self.send_3_id_108_led.add_value_listener(self.send_3_id_108_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_108["element"]) + " does not exist")
		try:
			self.send_4_id_109_led = eval(self.send_4_id_109["module"])
			self.send_4_id_109_led.add_value_listener(self.send_4_id_109_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_109["element"]) + " does not exist")
		try:
			self.volume_10_id_110_led = eval(self.volume_10_id_110["module"])
			self.volume_10_id_110_led.add_value_listener(self.volume_10_id_110_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_10_id_110["element"]) + " does not exist")
		try:
			self.pan_10_id_111_led = eval(self.pan_10_id_111["module"])
			self.pan_10_id_111_led.add_value_listener(self.pan_10_id_111_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_10_id_111["element"]) + " does not exist")
		try:
			self.mute_10_id_112_led = eval(self.mute_10_id_112["module"])
			self.mute_10_id_112_led.add_mute_listener(self.mute_10_id_112_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_10_id_112["element"]) + " does not exist")
		try:
			self.send_1_id_115_led = eval(self.send_1_id_115["module"])
			self.send_1_id_115_led.add_value_listener(self.send_1_id_115_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_115["element"]) + " does not exist")
		try:
			self.send_2_id_116_led = eval(self.send_2_id_116["module"])
			self.send_2_id_116_led.add_value_listener(self.send_2_id_116_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_116["element"]) + " does not exist")
		try:
			self.send_3_id_117_led = eval(self.send_3_id_117["module"])
			self.send_3_id_117_led.add_value_listener(self.send_3_id_117_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_117["element"]) + " does not exist")
		try:
			self.send_4_id_118_led = eval(self.send_4_id_118["module"])
			self.send_4_id_118_led.add_value_listener(self.send_4_id_118_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_118["element"]) + " does not exist")
		try:
			self.volume_11_id_119_led = eval(self.volume_11_id_119["module"])
			self.volume_11_id_119_led.add_value_listener(self.volume_11_id_119_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_11_id_119["element"]) + " does not exist")
		try:
			self.pan_11_id_120_led = eval(self.pan_11_id_120["module"])
			self.pan_11_id_120_led.add_value_listener(self.pan_11_id_120_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_11_id_120["element"]) + " does not exist")
		try:
			self.mute_11_id_121_led = eval(self.mute_11_id_121["module"])
			self.mute_11_id_121_led.add_mute_listener(self.mute_11_id_121_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_11_id_121["element"]) + " does not exist")
		try:
			self.send_1_id_124_led = eval(self.send_1_id_124["module"])
			self.send_1_id_124_led.add_value_listener(self.send_1_id_124_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_124["element"]) + " does not exist")
		try:
			self.send_2_id_125_led = eval(self.send_2_id_125["module"])
			self.send_2_id_125_led.add_value_listener(self.send_2_id_125_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_125["element"]) + " does not exist")
		try:
			self.send_3_id_126_led = eval(self.send_3_id_126["module"])
			self.send_3_id_126_led.add_value_listener(self.send_3_id_126_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_126["element"]) + " does not exist")
		try:
			self.send_4_id_127_led = eval(self.send_4_id_127["module"])
			self.send_4_id_127_led.add_value_listener(self.send_4_id_127_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_127["element"]) + " does not exist")
		try:
			self.volume_12_id_128_led = eval(self.volume_12_id_128["module"])
			self.volume_12_id_128_led.add_value_listener(self.volume_12_id_128_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_12_id_128["element"]) + " does not exist")
		try:
			self.pan_12_id_129_led = eval(self.pan_12_id_129["module"])
			self.pan_12_id_129_led.add_value_listener(self.pan_12_id_129_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_12_id_129["element"]) + " does not exist")
		try:
			self.mute_12_id_130_led = eval(self.mute_12_id_130["module"])
			self.mute_12_id_130_led.add_mute_listener(self.mute_12_id_130_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_12_id_130["element"]) + " does not exist")
		try:
			self.send_1_id_133_led = eval(self.send_1_id_133["module"])
			self.send_1_id_133_led.add_value_listener(self.send_1_id_133_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_133["element"]) + " does not exist")
		try:
			self.send_2_id_134_led = eval(self.send_2_id_134["module"])
			self.send_2_id_134_led.add_value_listener(self.send_2_id_134_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_134["element"]) + " does not exist")
		try:
			self.send_3_id_135_led = eval(self.send_3_id_135["module"])
			self.send_3_id_135_led.add_value_listener(self.send_3_id_135_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_135["element"]) + " does not exist")
		try:
			self.send_4_id_136_led = eval(self.send_4_id_136["module"])
			self.send_4_id_136_led.add_value_listener(self.send_4_id_136_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_136["element"]) + " does not exist")
		try:
			self.volume_13_id_137_led = eval(self.volume_13_id_137["module"])
			self.volume_13_id_137_led.add_value_listener(self.volume_13_id_137_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_13_id_137["element"]) + " does not exist")
		try:
			self.pan_13_id_138_led = eval(self.pan_13_id_138["module"])
			self.pan_13_id_138_led.add_value_listener(self.pan_13_id_138_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_13_id_138["element"]) + " does not exist")
		try:
			self.mute_13_id_139_led = eval(self.mute_13_id_139["module"])
			self.mute_13_id_139_led.add_mute_listener(self.mute_13_id_139_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_13_id_139["element"]) + " does not exist")
		try:
			self.send_1_id_142_led = eval(self.send_1_id_142["module"])
			self.send_1_id_142_led.add_value_listener(self.send_1_id_142_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_142["element"]) + " does not exist")
		try:
			self.send_2_id_143_led = eval(self.send_2_id_143["module"])
			self.send_2_id_143_led.add_value_listener(self.send_2_id_143_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_143["element"]) + " does not exist")
		try:
			self.send_3_id_144_led = eval(self.send_3_id_144["module"])
			self.send_3_id_144_led.add_value_listener(self.send_3_id_144_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_144["element"]) + " does not exist")
		try:
			self.send_4_id_145_led = eval(self.send_4_id_145["module"])
			self.send_4_id_145_led.add_value_listener(self.send_4_id_145_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_145["element"]) + " does not exist")
		try:
			self.volume_14_id_146_led = eval(self.volume_14_id_146["module"])
			self.volume_14_id_146_led.add_value_listener(self.volume_14_id_146_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_14_id_146["element"]) + " does not exist")
		try:
			self.pan_14_id_147_led = eval(self.pan_14_id_147["module"])
			self.pan_14_id_147_led.add_value_listener(self.pan_14_id_147_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_14_id_147["element"]) + " does not exist")
		try:
			self.mute_14_id_148_led = eval(self.mute_14_id_148["module"])
			self.mute_14_id_148_led.add_mute_listener(self.mute_14_id_148_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_14_id_148["element"]) + " does not exist")
		try:
			self.send_1_id_151_led = eval(self.send_1_id_151["module"])
			self.send_1_id_151_led.add_value_listener(self.send_1_id_151_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_151["element"]) + " does not exist")
		try:
			self.send_2_id_152_led = eval(self.send_2_id_152["module"])
			self.send_2_id_152_led.add_value_listener(self.send_2_id_152_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_152["element"]) + " does not exist")
		try:
			self.send_3_id_153_led = eval(self.send_3_id_153["module"])
			self.send_3_id_153_led.add_value_listener(self.send_3_id_153_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_153["element"]) + " does not exist")
		try:
			self.send_4_id_154_led = eval(self.send_4_id_154["module"])
			self.send_4_id_154_led.add_value_listener(self.send_4_id_154_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_154["element"]) + " does not exist")
		try:
			self.volume_15_id_155_led = eval(self.volume_15_id_155["module"])
			self.volume_15_id_155_led.add_value_listener(self.volume_15_id_155_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_15_id_155["element"]) + " does not exist")
		try:
			self.pan_15_id_156_led = eval(self.pan_15_id_156["module"])
			self.pan_15_id_156_led.add_value_listener(self.pan_15_id_156_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_15_id_156["element"]) + " does not exist")
		try:
			self.mute_15_id_157_led = eval(self.mute_15_id_157["module"])
			self.mute_15_id_157_led.add_mute_listener(self.mute_15_id_157_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_15_id_157["element"]) + " does not exist")
		try:
			self.send_1_id_160_led = eval(self.send_1_id_160["module"])
			self.send_1_id_160_led.add_value_listener(self.send_1_id_160_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_1_id_160["element"]) + " does not exist")
		try:
			self.send_2_id_161_led = eval(self.send_2_id_161["module"])
			self.send_2_id_161_led.add_value_listener(self.send_2_id_161_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_2_id_161["element"]) + " does not exist")
		try:
			self.send_3_id_162_led = eval(self.send_3_id_162["module"])
			self.send_3_id_162_led.add_value_listener(self.send_3_id_162_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_3_id_162["element"]) + " does not exist")
		try:
			self.send_4_id_163_led = eval(self.send_4_id_163["module"])
			self.send_4_id_163_led.add_value_listener(self.send_4_id_163_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.send_4_id_163["element"]) + " does not exist")
		try:
			self.volume_16_id_164_led = eval(self.volume_16_id_164["module"])
			self.volume_16_id_164_led.add_value_listener(self.volume_16_id_164_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_16_id_164["element"]) + " does not exist")
		try:
			self.pan_16_id_165_led = eval(self.pan_16_id_165["module"])
			self.pan_16_id_165_led.add_value_listener(self.pan_16_id_165_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.pan_16_id_165["element"]) + " does not exist")
		try:
			self.mute_16_id_166_led = eval(self.mute_16_id_166["module"])
			self.mute_16_id_166_led.add_mute_listener(self.mute_16_id_166_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.mute_16_id_166["element"]) + " does not exist")
		try:
			self._session.add_offset_listener(self.session_box_navigation_1_copy_id_347_led_listener)
		except:
			self.log("_mode1_ui_listeners: self._session does not exist")

	def _mode169_ui_listeners(self):
		try:
			self.volume_1_id_174_led = eval(self.volume_1_id_174["module"])
			self.volume_1_id_174_led.add_value_listener(self.volume_1_id_174_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_1_id_174["element"]) + " does not exist")
		try:
			self.pan_1_id_175_led = eval(self.pan_1_id_175["module"])
			self.pan_1_id_175_led.add_value_listener(self.pan_1_id_175_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_1_id_175["element"]) + " does not exist")
		try:
			self.volume_2_id_182_led = eval(self.volume_2_id_182["module"])
			self.volume_2_id_182_led.add_value_listener(self.volume_2_id_182_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_2_id_182["element"]) + " does not exist")
		try:
			self.pan_2_id_183_led = eval(self.pan_2_id_183["module"])
			self.pan_2_id_183_led.add_value_listener(self.pan_2_id_183_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_2_id_183["element"]) + " does not exist")
		try:
			self.volume_3_id_190_led = eval(self.volume_3_id_190["module"])
			self.volume_3_id_190_led.add_value_listener(self.volume_3_id_190_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_3_id_190["element"]) + " does not exist")
		try:
			self.pan_3_id_191_led = eval(self.pan_3_id_191["module"])
			self.pan_3_id_191_led.add_value_listener(self.pan_3_id_191_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_3_id_191["element"]) + " does not exist")
		try:
			self.volume_4_id_198_led = eval(self.volume_4_id_198["module"])
			self.volume_4_id_198_led.add_value_listener(self.volume_4_id_198_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_4_id_198["element"]) + " does not exist")
		try:
			self.pan_4_id_199_led = eval(self.pan_4_id_199["module"])
			self.pan_4_id_199_led.add_value_listener(self.pan_4_id_199_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_4_id_199["element"]) + " does not exist")
		try:
			self.volume_5_id_206_led = eval(self.volume_5_id_206["module"])
			self.volume_5_id_206_led.add_value_listener(self.volume_5_id_206_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_5_id_206["element"]) + " does not exist")
		try:
			self.pan_5_id_207_led = eval(self.pan_5_id_207["module"])
			self.pan_5_id_207_led.add_value_listener(self.pan_5_id_207_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_5_id_207["element"]) + " does not exist")
		try:
			self.volume_6_id_214_led = eval(self.volume_6_id_214["module"])
			self.volume_6_id_214_led.add_value_listener(self.volume_6_id_214_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_6_id_214["element"]) + " does not exist")
		try:
			self.pan_6_id_215_led = eval(self.pan_6_id_215["module"])
			self.pan_6_id_215_led.add_value_listener(self.pan_6_id_215_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_6_id_215["element"]) + " does not exist")
		try:
			self.volume_7_id_222_led = eval(self.volume_7_id_222["module"])
			self.volume_7_id_222_led.add_value_listener(self.volume_7_id_222_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_7_id_222["element"]) + " does not exist")
		try:
			self.pan_7_id_223_led = eval(self.pan_7_id_223["module"])
			self.pan_7_id_223_led.add_value_listener(self.pan_7_id_223_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_7_id_223["element"]) + " does not exist")
		try:
			self.volume_8_id_230_led = eval(self.volume_8_id_230["module"])
			self.volume_8_id_230_led.add_value_listener(self.volume_8_id_230_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_8_id_230["element"]) + " does not exist")
		try:
			self.pan_8_id_231_led = eval(self.pan_8_id_231["module"])
			self.pan_8_id_231_led.add_value_listener(self.pan_8_id_231_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_8_id_231["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_1_id_234_led = eval(self.parameter_1_id_234["module"])
				self.parameter_1_id_234_led.add_value_listener(self.parameter_1_id_234_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_1_id_234["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_2_id_235_led = eval(self.parameter_2_id_235["module"])
				self.parameter_2_id_235_led.add_value_listener(self.parameter_2_id_235_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_2_id_235["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_3_id_236_led = eval(self.parameter_3_id_236["module"])
				self.parameter_3_id_236_led.add_value_listener(self.parameter_3_id_236_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_3_id_236["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_4_id_237_led = eval(self.parameter_4_id_237["module"])
				self.parameter_4_id_237_led.add_value_listener(self.parameter_4_id_237_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_4_id_237["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_5_id_238_led = eval(self.parameter_5_id_238["module"])
				self.parameter_5_id_238_led.add_value_listener(self.parameter_5_id_238_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_5_id_238["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_6_id_239_led = eval(self.parameter_6_id_239["module"])
				self.parameter_6_id_239_led.add_value_listener(self.parameter_6_id_239_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_6_id_239["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_7_id_240_led = eval(self.parameter_7_id_240["module"])
				self.parameter_7_id_240_led.add_value_listener(self.parameter_7_id_240_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_7_id_240["element"]) + " does not exist")
		if self.device_id_243_active_bank == 0:
			try:
				self.parameter_8_id_241_led = eval(self.parameter_8_id_241["module"])
				self.parameter_8_id_241_led.add_value_listener(self.parameter_8_id_241_led_listener)
			except:
				self.log("_mode169_ui_listeners: " + str(self.parameter_8_id_241["element"]) + " does not exist")
		try:
			self.volume_9_id_248_led = eval(self.volume_9_id_248["module"])
			self.volume_9_id_248_led.add_value_listener(self.volume_9_id_248_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_9_id_248["element"]) + " does not exist")
		try:
			self.pan_9_id_249_led = eval(self.pan_9_id_249["module"])
			self.pan_9_id_249_led.add_value_listener(self.pan_9_id_249_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_9_id_249["element"]) + " does not exist")
		try:
			self.volume_10_id_256_led = eval(self.volume_10_id_256["module"])
			self.volume_10_id_256_led.add_value_listener(self.volume_10_id_256_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_10_id_256["element"]) + " does not exist")
		try:
			self.pan_10_id_257_led = eval(self.pan_10_id_257["module"])
			self.pan_10_id_257_led.add_value_listener(self.pan_10_id_257_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_10_id_257["element"]) + " does not exist")
		try:
			self.volume_11_id_264_led = eval(self.volume_11_id_264["module"])
			self.volume_11_id_264_led.add_value_listener(self.volume_11_id_264_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_11_id_264["element"]) + " does not exist")
		try:
			self.pan_11_id_265_led = eval(self.pan_11_id_265["module"])
			self.pan_11_id_265_led.add_value_listener(self.pan_11_id_265_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_11_id_265["element"]) + " does not exist")
		try:
			self.volume_12_id_272_led = eval(self.volume_12_id_272["module"])
			self.volume_12_id_272_led.add_value_listener(self.volume_12_id_272_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_12_id_272["element"]) + " does not exist")
		try:
			self.pan_12_id_273_led = eval(self.pan_12_id_273["module"])
			self.pan_12_id_273_led.add_value_listener(self.pan_12_id_273_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_12_id_273["element"]) + " does not exist")
		try:
			self.volume_13_id_280_led = eval(self.volume_13_id_280["module"])
			self.volume_13_id_280_led.add_value_listener(self.volume_13_id_280_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_13_id_280["element"]) + " does not exist")
		try:
			self.pan_13_id_281_led = eval(self.pan_13_id_281["module"])
			self.pan_13_id_281_led.add_value_listener(self.pan_13_id_281_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_13_id_281["element"]) + " does not exist")
		try:
			self.volume_14_id_288_led = eval(self.volume_14_id_288["module"])
			self.volume_14_id_288_led.add_value_listener(self.volume_14_id_288_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_14_id_288["element"]) + " does not exist")
		try:
			self.pan_14_id_289_led = eval(self.pan_14_id_289["module"])
			self.pan_14_id_289_led.add_value_listener(self.pan_14_id_289_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_14_id_289["element"]) + " does not exist")
		try:
			self.volume_15_id_296_led = eval(self.volume_15_id_296["module"])
			self.volume_15_id_296_led.add_value_listener(self.volume_15_id_296_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_15_id_296["element"]) + " does not exist")
		try:
			self.pan_15_id_297_led = eval(self.pan_15_id_297["module"])
			self.pan_15_id_297_led.add_value_listener(self.pan_15_id_297_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_15_id_297["element"]) + " does not exist")
		try:
			self.volume_16_id_304_led = eval(self.volume_16_id_304["module"])
			self.volume_16_id_304_led.add_value_listener(self.volume_16_id_304_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.volume_16_id_304["element"]) + " does not exist")
		try:
			self.pan_16_id_305_led = eval(self.pan_16_id_305["module"])
			self.pan_16_id_305_led.add_value_listener(self.pan_16_id_305_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.pan_16_id_305["element"]) + " does not exist")
		try:
			self.solo_1_id_328_led = eval(self.solo_1_id_328["module"])
			self.solo_1_id_328_led.add_solo_listener(self.solo_1_id_328_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_1_id_328["element"]) + " does not exist")
		try:
			self.solo_2_id_329_led = eval(self.solo_2_id_329["module"])
			self.solo_2_id_329_led.add_solo_listener(self.solo_2_id_329_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_2_id_329["element"]) + " does not exist")
		try:
			self.solo_3_id_330_led = eval(self.solo_3_id_330["module"])
			self.solo_3_id_330_led.add_solo_listener(self.solo_3_id_330_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_3_id_330["element"]) + " does not exist")
		try:
			self.solo_4_id_331_led = eval(self.solo_4_id_331["module"])
			self.solo_4_id_331_led.add_solo_listener(self.solo_4_id_331_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_4_id_331["element"]) + " does not exist")
		try:
			self.solo_5_id_332_led = eval(self.solo_5_id_332["module"])
			self.solo_5_id_332_led.add_solo_listener(self.solo_5_id_332_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_5_id_332["element"]) + " does not exist")
		try:
			self.solo_6_id_333_led = eval(self.solo_6_id_333["module"])
			self.solo_6_id_333_led.add_solo_listener(self.solo_6_id_333_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_6_id_333["element"]) + " does not exist")
		try:
			self.solo_7_id_334_led = eval(self.solo_7_id_334["module"])
			self.solo_7_id_334_led.add_solo_listener(self.solo_7_id_334_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_7_id_334["element"]) + " does not exist")
		try:
			self.solo_8_id_335_led = eval(self.solo_8_id_335["module"])
			self.solo_8_id_335_led.add_solo_listener(self.solo_8_id_335_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_8_id_335["element"]) + " does not exist")
		try:
			self.solo_9_id_336_led = eval(self.solo_9_id_336["module"])
			self.solo_9_id_336_led.add_solo_listener(self.solo_9_id_336_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_9_id_336["element"]) + " does not exist")
		try:
			self.solo_10_id_337_led = eval(self.solo_10_id_337["module"])
			self.solo_10_id_337_led.add_solo_listener(self.solo_10_id_337_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_10_id_337["element"]) + " does not exist")
		try:
			self.solo_11_id_338_led = eval(self.solo_11_id_338["module"])
			self.solo_11_id_338_led.add_solo_listener(self.solo_11_id_338_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_11_id_338["element"]) + " does not exist")
		try:
			self.solo_12_id_339_led = eval(self.solo_12_id_339["module"])
			self.solo_12_id_339_led.add_solo_listener(self.solo_12_id_339_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_12_id_339["element"]) + " does not exist")
		try:
			self.solo_13_id_340_led = eval(self.solo_13_id_340["module"])
			self.solo_13_id_340_led.add_solo_listener(self.solo_13_id_340_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_13_id_340["element"]) + " does not exist")
		try:
			self.solo_14_id_341_led = eval(self.solo_14_id_341["module"])
			self.solo_14_id_341_led.add_solo_listener(self.solo_14_id_341_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_14_id_341["element"]) + " does not exist")
		try:
			self.solo_15_id_342_led = eval(self.solo_15_id_342["module"])
			self.solo_15_id_342_led.add_solo_listener(self.solo_15_id_342_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_15_id_342["element"]) + " does not exist")
		try:
			self.solo_16_id_343_led = eval(self.solo_16_id_343["module"])
			self.solo_16_id_343_led.add_solo_listener(self.solo_16_id_343_led_listener)
		except:
			self.log("_mode169_ui_listeners: " + str(self.solo_16_id_343["element"]) + " does not exist")

	def _remove_mode1_ui_listeners(self):
		try:
			self.volume_1_id_3_led.remove_value_listener(self.volume_1_id_3_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_1_id_3["element"]) + " does not exist")
		try:
			self.pan_1_id_4_led.remove_value_listener(self.pan_1_id_4_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_1_id_4["element"]) + " does not exist")
		try:
			self.mute_1_id_5_led.remove_mute_listener(self.mute_1_id_5_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_1_id_5["element"]) + " does not exist")
		try:
			self.send_1_id_8_led.remove_value_listener(self.send_1_id_8_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_8["element"]) + " does not exist")
		try:
			self.send_2_id_9_led.remove_value_listener(self.send_2_id_9_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_9["element"]) + " does not exist")
		try:
			self.send_3_id_10_led.remove_value_listener(self.send_3_id_10_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_10["element"]) + " does not exist")
		try:
			self.send_4_id_11_led.remove_value_listener(self.send_4_id_11_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_11["element"]) + " does not exist")
		try:
			self.send_1_id_13_led.remove_value_listener(self.send_1_id_13_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_13["element"]) + " does not exist")
		try:
			self.send_2_id_14_led.remove_value_listener(self.send_2_id_14_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_14["element"]) + " does not exist")
		try:
			self.send_3_id_15_led.remove_value_listener(self.send_3_id_15_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_15["element"]) + " does not exist")
		try:
			self.send_4_id_16_led.remove_value_listener(self.send_4_id_16_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_16["element"]) + " does not exist")
		try:
			self.volume_2_id_17_led.remove_value_listener(self.volume_2_id_17_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_2_id_17["element"]) + " does not exist")
		try:
			self.pan_2_id_18_led.remove_value_listener(self.pan_2_id_18_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_2_id_18["element"]) + " does not exist")
		try:
			self.mute_2_id_19_led.remove_mute_listener(self.mute_2_id_19_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_2_id_19["element"]) + " does not exist")
		try:
			self.send_1_id_23_led.remove_value_listener(self.send_1_id_23_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_23["element"]) + " does not exist")
		try:
			self.send_2_id_24_led.remove_value_listener(self.send_2_id_24_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_24["element"]) + " does not exist")
		try:
			self.send_3_id_25_led.remove_value_listener(self.send_3_id_25_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_25["element"]) + " does not exist")
		try:
			self.send_4_id_26_led.remove_value_listener(self.send_4_id_26_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_26["element"]) + " does not exist")
		try:
			self.volume_3_id_27_led.remove_value_listener(self.volume_3_id_27_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_3_id_27["element"]) + " does not exist")
		try:
			self.pan_3_id_28_led.remove_value_listener(self.pan_3_id_28_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_3_id_28["element"]) + " does not exist")
		try:
			self.mute_3_id_29_led.remove_mute_listener(self.mute_3_id_29_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_3_id_29["element"]) + " does not exist")
		try:
			self.send_1_id_33_led.remove_value_listener(self.send_1_id_33_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_33["element"]) + " does not exist")
		try:
			self.send_2_id_34_led.remove_value_listener(self.send_2_id_34_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_34["element"]) + " does not exist")
		try:
			self.send_3_id_35_led.remove_value_listener(self.send_3_id_35_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_35["element"]) + " does not exist")
		try:
			self.send_4_id_36_led.remove_value_listener(self.send_4_id_36_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_36["element"]) + " does not exist")
		try:
			self.volume_4_id_37_led.remove_value_listener(self.volume_4_id_37_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_4_id_37["element"]) + " does not exist")
		try:
			self.pan_4_id_38_led.remove_value_listener(self.pan_4_id_38_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_4_id_38["element"]) + " does not exist")
		try:
			self.mute_4_id_39_led.remove_mute_listener(self.mute_4_id_39_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_4_id_39["element"]) + " does not exist")
		try:
			self.send_1_id_43_led.remove_value_listener(self.send_1_id_43_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_43["element"]) + " does not exist")
		try:
			self.send_2_id_44_led.remove_value_listener(self.send_2_id_44_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_44["element"]) + " does not exist")
		try:
			self.send_3_id_45_led.remove_value_listener(self.send_3_id_45_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_45["element"]) + " does not exist")
		try:
			self.send_4_id_46_led.remove_value_listener(self.send_4_id_46_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_46["element"]) + " does not exist")
		try:
			self.volume_5_id_47_led.remove_value_listener(self.volume_5_id_47_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_5_id_47["element"]) + " does not exist")
		try:
			self.pan_5_id_48_led.remove_value_listener(self.pan_5_id_48_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_5_id_48["element"]) + " does not exist")
		try:
			self.mute_5_id_49_led.remove_mute_listener(self.mute_5_id_49_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_5_id_49["element"]) + " does not exist")
		try:
			self.send_1_id_53_led.remove_value_listener(self.send_1_id_53_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_53["element"]) + " does not exist")
		try:
			self.send_2_id_54_led.remove_value_listener(self.send_2_id_54_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_54["element"]) + " does not exist")
		try:
			self.send_3_id_55_led.remove_value_listener(self.send_3_id_55_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_55["element"]) + " does not exist")
		try:
			self.send_4_id_56_led.remove_value_listener(self.send_4_id_56_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_56["element"]) + " does not exist")
		try:
			self.volume_6_id_57_led.remove_value_listener(self.volume_6_id_57_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_6_id_57["element"]) + " does not exist")
		try:
			self.pan_6_id_58_led.remove_value_listener(self.pan_6_id_58_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_6_id_58["element"]) + " does not exist")
		try:
			self.mute_6_id_59_led.remove_mute_listener(self.mute_6_id_59_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_6_id_59["element"]) + " does not exist")
		try:
			self.send_1_id_63_led.remove_value_listener(self.send_1_id_63_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_63["element"]) + " does not exist")
		try:
			self.send_2_id_64_led.remove_value_listener(self.send_2_id_64_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_64["element"]) + " does not exist")
		try:
			self.send_3_id_65_led.remove_value_listener(self.send_3_id_65_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_65["element"]) + " does not exist")
		try:
			self.send_4_id_66_led.remove_value_listener(self.send_4_id_66_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_66["element"]) + " does not exist")
		try:
			self.volume_7_id_67_led.remove_value_listener(self.volume_7_id_67_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_7_id_67["element"]) + " does not exist")
		try:
			self.pan_7_id_68_led.remove_value_listener(self.pan_7_id_68_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_7_id_68["element"]) + " does not exist")
		try:
			self.mute_7_id_69_led.remove_mute_listener(self.mute_7_id_69_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_7_id_69["element"]) + " does not exist")
		try:
			self.send_1_id_73_led.remove_value_listener(self.send_1_id_73_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_73["element"]) + " does not exist")
		try:
			self.send_2_id_74_led.remove_value_listener(self.send_2_id_74_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_74["element"]) + " does not exist")
		try:
			self.send_3_id_75_led.remove_value_listener(self.send_3_id_75_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_75["element"]) + " does not exist")
		try:
			self.send_4_id_76_led.remove_value_listener(self.send_4_id_76_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_76["element"]) + " does not exist")
		try:
			self.volume_8_id_77_led.remove_value_listener(self.volume_8_id_77_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_8_id_77["element"]) + " does not exist")
		try:
			self.pan_8_id_78_led.remove_value_listener(self.pan_8_id_78_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_8_id_78["element"]) + " does not exist")
		try:
			self.mute_8_id_79_led.remove_mute_listener(self.mute_8_id_79_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_8_id_79["element"]) + " does not exist")
		try:
			self.parameter_1_id_88_led.remove_value_listener(self.parameter_1_id_88_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_1_id_88["element"]) + " does not exist")
		try:
			self.parameter_2_id_89_led.remove_value_listener(self.parameter_2_id_89_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_2_id_89["element"]) + " does not exist")
		try:
			self.parameter_3_id_90_led.remove_value_listener(self.parameter_3_id_90_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_3_id_90["element"]) + " does not exist")
		try:
			self.parameter_4_id_91_led.remove_value_listener(self.parameter_4_id_91_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_4_id_91["element"]) + " does not exist")
		try:
			self.parameter_5_id_92_led.remove_value_listener(self.parameter_5_id_92_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_5_id_92["element"]) + " does not exist")
		try:
			self.parameter_6_id_93_led.remove_value_listener(self.parameter_6_id_93_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_6_id_93["element"]) + " does not exist")
		try:
			self.parameter_7_id_94_led.remove_value_listener(self.parameter_7_id_94_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_7_id_94["element"]) + " does not exist")
		try:
			self.parameter_8_id_95_led.remove_value_listener(self.parameter_8_id_95_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_8_id_95["element"]) + " does not exist")
		try:
			self.send_1_id_97_led.remove_value_listener(self.send_1_id_97_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_97["element"]) + " does not exist")
		try:
			self.send_2_id_98_led.remove_value_listener(self.send_2_id_98_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_98["element"]) + " does not exist")
		try:
			self.send_3_id_99_led.remove_value_listener(self.send_3_id_99_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_99["element"]) + " does not exist")
		try:
			self.send_4_id_100_led.remove_value_listener(self.send_4_id_100_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_100["element"]) + " does not exist")
		try:
			self.volume_9_id_101_led.remove_value_listener(self.volume_9_id_101_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_9_id_101["element"]) + " does not exist")
		try:
			self.pan_9_id_102_led.remove_value_listener(self.pan_9_id_102_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_9_id_102["element"]) + " does not exist")
		try:
			self.mute_9_id_103_led.remove_mute_listener(self.mute_9_id_103_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_9_id_103["element"]) + " does not exist")
		try:
			self.send_1_id_106_led.remove_value_listener(self.send_1_id_106_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_106["element"]) + " does not exist")
		try:
			self.send_2_id_107_led.remove_value_listener(self.send_2_id_107_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_107["element"]) + " does not exist")
		try:
			self.send_3_id_108_led.remove_value_listener(self.send_3_id_108_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_108["element"]) + " does not exist")
		try:
			self.send_4_id_109_led.remove_value_listener(self.send_4_id_109_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_109["element"]) + " does not exist")
		try:
			self.volume_10_id_110_led.remove_value_listener(self.volume_10_id_110_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_10_id_110["element"]) + " does not exist")
		try:
			self.pan_10_id_111_led.remove_value_listener(self.pan_10_id_111_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_10_id_111["element"]) + " does not exist")
		try:
			self.mute_10_id_112_led.remove_mute_listener(self.mute_10_id_112_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_10_id_112["element"]) + " does not exist")
		try:
			self.send_1_id_115_led.remove_value_listener(self.send_1_id_115_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_115["element"]) + " does not exist")
		try:
			self.send_2_id_116_led.remove_value_listener(self.send_2_id_116_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_116["element"]) + " does not exist")
		try:
			self.send_3_id_117_led.remove_value_listener(self.send_3_id_117_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_117["element"]) + " does not exist")
		try:
			self.send_4_id_118_led.remove_value_listener(self.send_4_id_118_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_118["element"]) + " does not exist")
		try:
			self.volume_11_id_119_led.remove_value_listener(self.volume_11_id_119_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_11_id_119["element"]) + " does not exist")
		try:
			self.pan_11_id_120_led.remove_value_listener(self.pan_11_id_120_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_11_id_120["element"]) + " does not exist")
		try:
			self.mute_11_id_121_led.remove_mute_listener(self.mute_11_id_121_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_11_id_121["element"]) + " does not exist")
		try:
			self.send_1_id_124_led.remove_value_listener(self.send_1_id_124_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_124["element"]) + " does not exist")
		try:
			self.send_2_id_125_led.remove_value_listener(self.send_2_id_125_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_125["element"]) + " does not exist")
		try:
			self.send_3_id_126_led.remove_value_listener(self.send_3_id_126_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_126["element"]) + " does not exist")
		try:
			self.send_4_id_127_led.remove_value_listener(self.send_4_id_127_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_127["element"]) + " does not exist")
		try:
			self.volume_12_id_128_led.remove_value_listener(self.volume_12_id_128_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_12_id_128["element"]) + " does not exist")
		try:
			self.pan_12_id_129_led.remove_value_listener(self.pan_12_id_129_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_12_id_129["element"]) + " does not exist")
		try:
			self.mute_12_id_130_led.remove_mute_listener(self.mute_12_id_130_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_12_id_130["element"]) + " does not exist")
		try:
			self.send_1_id_133_led.remove_value_listener(self.send_1_id_133_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_133["element"]) + " does not exist")
		try:
			self.send_2_id_134_led.remove_value_listener(self.send_2_id_134_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_134["element"]) + " does not exist")
		try:
			self.send_3_id_135_led.remove_value_listener(self.send_3_id_135_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_135["element"]) + " does not exist")
		try:
			self.send_4_id_136_led.remove_value_listener(self.send_4_id_136_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_136["element"]) + " does not exist")
		try:
			self.volume_13_id_137_led.remove_value_listener(self.volume_13_id_137_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_13_id_137["element"]) + " does not exist")
		try:
			self.pan_13_id_138_led.remove_value_listener(self.pan_13_id_138_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_13_id_138["element"]) + " does not exist")
		try:
			self.mute_13_id_139_led.remove_mute_listener(self.mute_13_id_139_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_13_id_139["element"]) + " does not exist")
		try:
			self.send_1_id_142_led.remove_value_listener(self.send_1_id_142_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_142["element"]) + " does not exist")
		try:
			self.send_2_id_143_led.remove_value_listener(self.send_2_id_143_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_143["element"]) + " does not exist")
		try:
			self.send_3_id_144_led.remove_value_listener(self.send_3_id_144_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_144["element"]) + " does not exist")
		try:
			self.send_4_id_145_led.remove_value_listener(self.send_4_id_145_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_145["element"]) + " does not exist")
		try:
			self.volume_14_id_146_led.remove_value_listener(self.volume_14_id_146_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_14_id_146["element"]) + " does not exist")
		try:
			self.pan_14_id_147_led.remove_value_listener(self.pan_14_id_147_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_14_id_147["element"]) + " does not exist")
		try:
			self.mute_14_id_148_led.remove_mute_listener(self.mute_14_id_148_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_14_id_148["element"]) + " does not exist")
		try:
			self.send_1_id_151_led.remove_value_listener(self.send_1_id_151_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_151["element"]) + " does not exist")
		try:
			self.send_2_id_152_led.remove_value_listener(self.send_2_id_152_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_152["element"]) + " does not exist")
		try:
			self.send_3_id_153_led.remove_value_listener(self.send_3_id_153_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_153["element"]) + " does not exist")
		try:
			self.send_4_id_154_led.remove_value_listener(self.send_4_id_154_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_154["element"]) + " does not exist")
		try:
			self.volume_15_id_155_led.remove_value_listener(self.volume_15_id_155_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_15_id_155["element"]) + " does not exist")
		try:
			self.pan_15_id_156_led.remove_value_listener(self.pan_15_id_156_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_15_id_156["element"]) + " does not exist")
		try:
			self.mute_15_id_157_led.remove_mute_listener(self.mute_15_id_157_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_15_id_157["element"]) + " does not exist")
		try:
			self.send_1_id_160_led.remove_value_listener(self.send_1_id_160_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_1_id_160["element"]) + " does not exist")
		try:
			self.send_2_id_161_led.remove_value_listener(self.send_2_id_161_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_2_id_161["element"]) + " does not exist")
		try:
			self.send_3_id_162_led.remove_value_listener(self.send_3_id_162_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_3_id_162["element"]) + " does not exist")
		try:
			self.send_4_id_163_led.remove_value_listener(self.send_4_id_163_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.send_4_id_163["element"]) + " does not exist")
		try:
			self.volume_16_id_164_led.remove_value_listener(self.volume_16_id_164_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_16_id_164["element"]) + " does not exist")
		try:
			self.pan_16_id_165_led.remove_value_listener(self.pan_16_id_165_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.pan_16_id_165["element"]) + " does not exist")
		try:
			self.mute_16_id_166_led.remove_mute_listener(self.mute_16_id_166_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.mute_16_id_166["element"]) + " does not exist")
		try:
			self._session.remove_offset_listener(self.session_box_navigation_1_copy_id_347_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: self._session does not exist")

	def _remove_mode169_ui_listeners(self):
		try:
			self.volume_1_id_174_led.remove_value_listener(self.volume_1_id_174_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_1_id_174["element"]) + " does not exist")
		try:
			self.pan_1_id_175_led.remove_value_listener(self.pan_1_id_175_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_1_id_175["element"]) + " does not exist")
		try:
			self.volume_2_id_182_led.remove_value_listener(self.volume_2_id_182_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_2_id_182["element"]) + " does not exist")
		try:
			self.pan_2_id_183_led.remove_value_listener(self.pan_2_id_183_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_2_id_183["element"]) + " does not exist")
		try:
			self.volume_3_id_190_led.remove_value_listener(self.volume_3_id_190_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_3_id_190["element"]) + " does not exist")
		try:
			self.pan_3_id_191_led.remove_value_listener(self.pan_3_id_191_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_3_id_191["element"]) + " does not exist")
		try:
			self.volume_4_id_198_led.remove_value_listener(self.volume_4_id_198_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_4_id_198["element"]) + " does not exist")
		try:
			self.pan_4_id_199_led.remove_value_listener(self.pan_4_id_199_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_4_id_199["element"]) + " does not exist")
		try:
			self.volume_5_id_206_led.remove_value_listener(self.volume_5_id_206_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_5_id_206["element"]) + " does not exist")
		try:
			self.pan_5_id_207_led.remove_value_listener(self.pan_5_id_207_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_5_id_207["element"]) + " does not exist")
		try:
			self.volume_6_id_214_led.remove_value_listener(self.volume_6_id_214_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_6_id_214["element"]) + " does not exist")
		try:
			self.pan_6_id_215_led.remove_value_listener(self.pan_6_id_215_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_6_id_215["element"]) + " does not exist")
		try:
			self.volume_7_id_222_led.remove_value_listener(self.volume_7_id_222_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_7_id_222["element"]) + " does not exist")
		try:
			self.pan_7_id_223_led.remove_value_listener(self.pan_7_id_223_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_7_id_223["element"]) + " does not exist")
		try:
			self.volume_8_id_230_led.remove_value_listener(self.volume_8_id_230_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_8_id_230["element"]) + " does not exist")
		try:
			self.pan_8_id_231_led.remove_value_listener(self.pan_8_id_231_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_8_id_231["element"]) + " does not exist")
		try:
			self.parameter_1_id_234_led.remove_value_listener(self.parameter_1_id_234_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_1_id_234["element"]) + " does not exist")
		try:
			self.parameter_2_id_235_led.remove_value_listener(self.parameter_2_id_235_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_2_id_235["element"]) + " does not exist")
		try:
			self.parameter_3_id_236_led.remove_value_listener(self.parameter_3_id_236_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_3_id_236["element"]) + " does not exist")
		try:
			self.parameter_4_id_237_led.remove_value_listener(self.parameter_4_id_237_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_4_id_237["element"]) + " does not exist")
		try:
			self.parameter_5_id_238_led.remove_value_listener(self.parameter_5_id_238_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_5_id_238["element"]) + " does not exist")
		try:
			self.parameter_6_id_239_led.remove_value_listener(self.parameter_6_id_239_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_6_id_239["element"]) + " does not exist")
		try:
			self.parameter_7_id_240_led.remove_value_listener(self.parameter_7_id_240_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_7_id_240["element"]) + " does not exist")
		try:
			self.parameter_8_id_241_led.remove_value_listener(self.parameter_8_id_241_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.parameter_8_id_241["element"]) + " does not exist")
		try:
			self.volume_9_id_248_led.remove_value_listener(self.volume_9_id_248_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_9_id_248["element"]) + " does not exist")
		try:
			self.pan_9_id_249_led.remove_value_listener(self.pan_9_id_249_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_9_id_249["element"]) + " does not exist")
		try:
			self.volume_10_id_256_led.remove_value_listener(self.volume_10_id_256_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_10_id_256["element"]) + " does not exist")
		try:
			self.pan_10_id_257_led.remove_value_listener(self.pan_10_id_257_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_10_id_257["element"]) + " does not exist")
		try:
			self.volume_11_id_264_led.remove_value_listener(self.volume_11_id_264_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_11_id_264["element"]) + " does not exist")
		try:
			self.pan_11_id_265_led.remove_value_listener(self.pan_11_id_265_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_11_id_265["element"]) + " does not exist")
		try:
			self.volume_12_id_272_led.remove_value_listener(self.volume_12_id_272_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_12_id_272["element"]) + " does not exist")
		try:
			self.pan_12_id_273_led.remove_value_listener(self.pan_12_id_273_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_12_id_273["element"]) + " does not exist")
		try:
			self.volume_13_id_280_led.remove_value_listener(self.volume_13_id_280_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_13_id_280["element"]) + " does not exist")
		try:
			self.pan_13_id_281_led.remove_value_listener(self.pan_13_id_281_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_13_id_281["element"]) + " does not exist")
		try:
			self.volume_14_id_288_led.remove_value_listener(self.volume_14_id_288_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_14_id_288["element"]) + " does not exist")
		try:
			self.pan_14_id_289_led.remove_value_listener(self.pan_14_id_289_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_14_id_289["element"]) + " does not exist")
		try:
			self.volume_15_id_296_led.remove_value_listener(self.volume_15_id_296_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_15_id_296["element"]) + " does not exist")
		try:
			self.pan_15_id_297_led.remove_value_listener(self.pan_15_id_297_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_15_id_297["element"]) + " does not exist")
		try:
			self.volume_16_id_304_led.remove_value_listener(self.volume_16_id_304_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.volume_16_id_304["element"]) + " does not exist")
		try:
			self.pan_16_id_305_led.remove_value_listener(self.pan_16_id_305_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.pan_16_id_305["element"]) + " does not exist")
		try:
			self.solo_1_id_328_led.remove_solo_listener(self.solo_1_id_328_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_1_id_328["element"]) + " does not exist")
		try:
			self.solo_2_id_329_led.remove_solo_listener(self.solo_2_id_329_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_2_id_329["element"]) + " does not exist")
		try:
			self.solo_3_id_330_led.remove_solo_listener(self.solo_3_id_330_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_3_id_330["element"]) + " does not exist")
		try:
			self.solo_4_id_331_led.remove_solo_listener(self.solo_4_id_331_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_4_id_331["element"]) + " does not exist")
		try:
			self.solo_5_id_332_led.remove_solo_listener(self.solo_5_id_332_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_5_id_332["element"]) + " does not exist")
		try:
			self.solo_6_id_333_led.remove_solo_listener(self.solo_6_id_333_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_6_id_333["element"]) + " does not exist")
		try:
			self.solo_7_id_334_led.remove_solo_listener(self.solo_7_id_334_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_7_id_334["element"]) + " does not exist")
		try:
			self.solo_8_id_335_led.remove_solo_listener(self.solo_8_id_335_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_8_id_335["element"]) + " does not exist")
		try:
			self.solo_9_id_336_led.remove_solo_listener(self.solo_9_id_336_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_9_id_336["element"]) + " does not exist")
		try:
			self.solo_10_id_337_led.remove_solo_listener(self.solo_10_id_337_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_10_id_337["element"]) + " does not exist")
		try:
			self.solo_11_id_338_led.remove_solo_listener(self.solo_11_id_338_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_11_id_338["element"]) + " does not exist")
		try:
			self.solo_12_id_339_led.remove_solo_listener(self.solo_12_id_339_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_12_id_339["element"]) + " does not exist")
		try:
			self.solo_13_id_340_led.remove_solo_listener(self.solo_13_id_340_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_13_id_340["element"]) + " does not exist")
		try:
			self.solo_14_id_341_led.remove_solo_listener(self.solo_14_id_341_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_14_id_341["element"]) + " does not exist")
		try:
			self.solo_15_id_342_led.remove_solo_listener(self.solo_15_id_342_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_15_id_342["element"]) + " does not exist")
		try:
			self.solo_16_id_343_led.remove_solo_listener(self.solo_16_id_343_led_listener)
		except:
			self.log("remove__mode169_ui_listeners: " + str(self.solo_16_id_343["element"]) + " does not exist")

	def _mode1_fire_all_feedback(self):
		self.volume_1_id_3_led_listener()
		self.pan_1_id_4_led_listener()
		self.mute_1_id_5_led_listener()
		self.send_1_id_8_led_listener()
		self.send_2_id_9_led_listener()
		self.send_3_id_10_led_listener()
		self.send_4_id_11_led_listener()
		self.send_1_id_13_led_listener()
		self.send_2_id_14_led_listener()
		self.send_3_id_15_led_listener()
		self.send_4_id_16_led_listener()
		self.volume_2_id_17_led_listener()
		self.pan_2_id_18_led_listener()
		self.mute_2_id_19_led_listener()
		self.send_1_id_23_led_listener()
		self.send_2_id_24_led_listener()
		self.send_3_id_25_led_listener()
		self.send_4_id_26_led_listener()
		self.volume_3_id_27_led_listener()
		self.pan_3_id_28_led_listener()
		self.mute_3_id_29_led_listener()
		self.send_1_id_33_led_listener()
		self.send_2_id_34_led_listener()
		self.send_3_id_35_led_listener()
		self.send_4_id_36_led_listener()
		self.volume_4_id_37_led_listener()
		self.pan_4_id_38_led_listener()
		self.mute_4_id_39_led_listener()
		self.send_1_id_43_led_listener()
		self.send_2_id_44_led_listener()
		self.send_3_id_45_led_listener()
		self.send_4_id_46_led_listener()
		self.volume_5_id_47_led_listener()
		self.pan_5_id_48_led_listener()
		self.mute_5_id_49_led_listener()
		self.send_1_id_53_led_listener()
		self.send_2_id_54_led_listener()
		self.send_3_id_55_led_listener()
		self.send_4_id_56_led_listener()
		self.volume_6_id_57_led_listener()
		self.pan_6_id_58_led_listener()
		self.mute_6_id_59_led_listener()
		self.send_1_id_63_led_listener()
		self.send_2_id_64_led_listener()
		self.send_3_id_65_led_listener()
		self.send_4_id_66_led_listener()
		self.volume_7_id_67_led_listener()
		self.pan_7_id_68_led_listener()
		self.mute_7_id_69_led_listener()
		self.send_1_id_73_led_listener()
		self.send_2_id_74_led_listener()
		self.send_3_id_75_led_listener()
		self.send_4_id_76_led_listener()
		self.volume_8_id_77_led_listener()
		self.pan_8_id_78_led_listener()
		self.mute_8_id_79_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_1_id_88_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_2_id_89_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_3_id_90_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_4_id_91_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_5_id_92_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_6_id_93_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_7_id_94_led_listener()
		if self.device_id_86_active_bank == 0:
			self.parameter_8_id_95_led_listener()
		self.send_1_id_97_led_listener()
		self.send_2_id_98_led_listener()
		self.send_3_id_99_led_listener()
		self.send_4_id_100_led_listener()
		self.volume_9_id_101_led_listener()
		self.pan_9_id_102_led_listener()
		self.mute_9_id_103_led_listener()
		self.send_1_id_106_led_listener()
		self.send_2_id_107_led_listener()
		self.send_3_id_108_led_listener()
		self.send_4_id_109_led_listener()
		self.volume_10_id_110_led_listener()
		self.pan_10_id_111_led_listener()
		self.mute_10_id_112_led_listener()
		self.send_1_id_115_led_listener()
		self.send_2_id_116_led_listener()
		self.send_3_id_117_led_listener()
		self.send_4_id_118_led_listener()
		self.volume_11_id_119_led_listener()
		self.pan_11_id_120_led_listener()
		self.mute_11_id_121_led_listener()
		self.send_1_id_124_led_listener()
		self.send_2_id_125_led_listener()
		self.send_3_id_126_led_listener()
		self.send_4_id_127_led_listener()
		self.volume_12_id_128_led_listener()
		self.pan_12_id_129_led_listener()
		self.mute_12_id_130_led_listener()
		self.send_1_id_133_led_listener()
		self.send_2_id_134_led_listener()
		self.send_3_id_135_led_listener()
		self.send_4_id_136_led_listener()
		self.volume_13_id_137_led_listener()
		self.pan_13_id_138_led_listener()
		self.mute_13_id_139_led_listener()
		self.send_1_id_142_led_listener()
		self.send_2_id_143_led_listener()
		self.send_3_id_144_led_listener()
		self.send_4_id_145_led_listener()
		self.volume_14_id_146_led_listener()
		self.pan_14_id_147_led_listener()
		self.mute_14_id_148_led_listener()
		self.send_1_id_151_led_listener()
		self.send_2_id_152_led_listener()
		self.send_3_id_153_led_listener()
		self.send_4_id_154_led_listener()
		self.volume_15_id_155_led_listener()
		self.pan_15_id_156_led_listener()
		self.mute_15_id_157_led_listener()
		self.send_1_id_160_led_listener()
		self.send_2_id_161_led_listener()
		self.send_3_id_162_led_listener()
		self.send_4_id_163_led_listener()
		self.volume_16_id_164_led_listener()
		self.pan_16_id_165_led_listener()
		self.mute_16_id_166_led_listener()
		self.mode_selector_1_id_168_led_listener()
		self.session_box_navigation_1_copy_id_347_led_listener()

	def _mode169_fire_all_feedback(self):
		self.volume_1_id_174_led_listener()
		self.pan_1_id_175_led_listener()
		self.volume_2_id_182_led_listener()
		self.pan_2_id_183_led_listener()
		self.volume_3_id_190_led_listener()
		self.pan_3_id_191_led_listener()
		self.volume_4_id_198_led_listener()
		self.pan_4_id_199_led_listener()
		self.volume_5_id_206_led_listener()
		self.pan_5_id_207_led_listener()
		self.volume_6_id_214_led_listener()
		self.pan_6_id_215_led_listener()
		self.volume_7_id_222_led_listener()
		self.pan_7_id_223_led_listener()
		self.volume_8_id_230_led_listener()
		self.pan_8_id_231_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_1_id_234_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_2_id_235_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_3_id_236_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_4_id_237_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_5_id_238_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_6_id_239_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_7_id_240_led_listener()
		if self.device_id_243_active_bank == 0:
			self.parameter_8_id_241_led_listener()
		self.volume_9_id_248_led_listener()
		self.pan_9_id_249_led_listener()
		self.volume_10_id_256_led_listener()
		self.pan_10_id_257_led_listener()
		self.volume_11_id_264_led_listener()
		self.pan_11_id_265_led_listener()
		self.volume_12_id_272_led_listener()
		self.pan_12_id_273_led_listener()
		self.volume_13_id_280_led_listener()
		self.pan_13_id_281_led_listener()
		self.volume_14_id_288_led_listener()
		self.pan_14_id_289_led_listener()
		self.volume_15_id_296_led_listener()
		self.pan_15_id_297_led_listener()
		self.volume_16_id_304_led_listener()
		self.pan_16_id_305_led_listener()
		self.solo_1_id_328_led_listener()
		self.solo_2_id_329_led_listener()
		self.solo_3_id_330_led_listener()
		self.solo_4_id_331_led_listener()
		self.solo_5_id_332_led_listener()
		self.solo_6_id_333_led_listener()
		self.solo_7_id_334_led_listener()
		self.solo_8_id_335_led_listener()
		self.solo_9_id_336_led_listener()
		self.solo_10_id_337_led_listener()
		self.solo_11_id_338_led_listener()
		self.solo_12_id_339_led_listener()
		self.solo_13_id_340_led_listener()
		self.solo_14_id_341_led_listener()
		self.solo_15_id_342_led_listener()
		self.solo_16_id_343_led_listener()
		self.mode_selector_1_copy_id_346_led_listener()

	def volume_1_id_3_led_listener(self):
		self.feedback_brain(self.volume_1_id_3)

	def pan_1_id_4_led_listener(self):
		self.feedback_brain(self.pan_1_id_4)

	def mute_1_id_5_led_listener(self):
		self.feedback_brain(self.mute_1_id_5)

	def send_1_id_8_led_listener(self):
		self.feedback_brain(self.send_1_id_8)

	def send_2_id_9_led_listener(self):
		self.feedback_brain(self.send_2_id_9)

	def send_3_id_10_led_listener(self):
		self.feedback_brain(self.send_3_id_10)

	def send_4_id_11_led_listener(self):
		self.feedback_brain(self.send_4_id_11)

	def send_1_id_13_led_listener(self):
		self.feedback_brain(self.send_1_id_13)

	def send_2_id_14_led_listener(self):
		self.feedback_brain(self.send_2_id_14)

	def send_3_id_15_led_listener(self):
		self.feedback_brain(self.send_3_id_15)

	def send_4_id_16_led_listener(self):
		self.feedback_brain(self.send_4_id_16)

	def volume_2_id_17_led_listener(self):
		self.feedback_brain(self.volume_2_id_17)

	def pan_2_id_18_led_listener(self):
		self.feedback_brain(self.pan_2_id_18)

	def mute_2_id_19_led_listener(self):
		self.feedback_brain(self.mute_2_id_19)

	def send_1_id_23_led_listener(self):
		self.feedback_brain(self.send_1_id_23)

	def send_2_id_24_led_listener(self):
		self.feedback_brain(self.send_2_id_24)

	def send_3_id_25_led_listener(self):
		self.feedback_brain(self.send_3_id_25)

	def send_4_id_26_led_listener(self):
		self.feedback_brain(self.send_4_id_26)

	def volume_3_id_27_led_listener(self):
		self.feedback_brain(self.volume_3_id_27)

	def pan_3_id_28_led_listener(self):
		self.feedback_brain(self.pan_3_id_28)

	def mute_3_id_29_led_listener(self):
		self.feedback_brain(self.mute_3_id_29)

	def send_1_id_33_led_listener(self):
		self.feedback_brain(self.send_1_id_33)

	def send_2_id_34_led_listener(self):
		self.feedback_brain(self.send_2_id_34)

	def send_3_id_35_led_listener(self):
		self.feedback_brain(self.send_3_id_35)

	def send_4_id_36_led_listener(self):
		self.feedback_brain(self.send_4_id_36)

	def volume_4_id_37_led_listener(self):
		self.feedback_brain(self.volume_4_id_37)

	def pan_4_id_38_led_listener(self):
		self.feedback_brain(self.pan_4_id_38)

	def mute_4_id_39_led_listener(self):
		self.feedback_brain(self.mute_4_id_39)

	def send_1_id_43_led_listener(self):
		self.feedback_brain(self.send_1_id_43)

	def send_2_id_44_led_listener(self):
		self.feedback_brain(self.send_2_id_44)

	def send_3_id_45_led_listener(self):
		self.feedback_brain(self.send_3_id_45)

	def send_4_id_46_led_listener(self):
		self.feedback_brain(self.send_4_id_46)

	def volume_5_id_47_led_listener(self):
		self.feedback_brain(self.volume_5_id_47)

	def pan_5_id_48_led_listener(self):
		self.feedback_brain(self.pan_5_id_48)

	def mute_5_id_49_led_listener(self):
		self.feedback_brain(self.mute_5_id_49)

	def send_1_id_53_led_listener(self):
		self.feedback_brain(self.send_1_id_53)

	def send_2_id_54_led_listener(self):
		self.feedback_brain(self.send_2_id_54)

	def send_3_id_55_led_listener(self):
		self.feedback_brain(self.send_3_id_55)

	def send_4_id_56_led_listener(self):
		self.feedback_brain(self.send_4_id_56)

	def volume_6_id_57_led_listener(self):
		self.feedback_brain(self.volume_6_id_57)

	def pan_6_id_58_led_listener(self):
		self.feedback_brain(self.pan_6_id_58)

	def mute_6_id_59_led_listener(self):
		self.feedback_brain(self.mute_6_id_59)

	def send_1_id_63_led_listener(self):
		self.feedback_brain(self.send_1_id_63)

	def send_2_id_64_led_listener(self):
		self.feedback_brain(self.send_2_id_64)

	def send_3_id_65_led_listener(self):
		self.feedback_brain(self.send_3_id_65)

	def send_4_id_66_led_listener(self):
		self.feedback_brain(self.send_4_id_66)

	def volume_7_id_67_led_listener(self):
		self.feedback_brain(self.volume_7_id_67)

	def pan_7_id_68_led_listener(self):
		self.feedback_brain(self.pan_7_id_68)

	def mute_7_id_69_led_listener(self):
		self.feedback_brain(self.mute_7_id_69)

	def send_1_id_73_led_listener(self):
		self.feedback_brain(self.send_1_id_73)

	def send_2_id_74_led_listener(self):
		self.feedback_brain(self.send_2_id_74)

	def send_3_id_75_led_listener(self):
		self.feedback_brain(self.send_3_id_75)

	def send_4_id_76_led_listener(self):
		self.feedback_brain(self.send_4_id_76)

	def volume_8_id_77_led_listener(self):
		self.feedback_brain(self.volume_8_id_77)

	def pan_8_id_78_led_listener(self):
		self.feedback_brain(self.pan_8_id_78)

	def mute_8_id_79_led_listener(self):
		self.feedback_brain(self.mute_8_id_79)

	def parameter_1_id_88_led_listener(self):
		self.feedback_brain(self.parameter_1_id_88)

	def parameter_2_id_89_led_listener(self):
		self.feedback_brain(self.parameter_2_id_89)

	def parameter_3_id_90_led_listener(self):
		self.feedback_brain(self.parameter_3_id_90)

	def parameter_4_id_91_led_listener(self):
		self.feedback_brain(self.parameter_4_id_91)

	def parameter_5_id_92_led_listener(self):
		self.feedback_brain(self.parameter_5_id_92)

	def parameter_6_id_93_led_listener(self):
		self.feedback_brain(self.parameter_6_id_93)

	def parameter_7_id_94_led_listener(self):
		self.feedback_brain(self.parameter_7_id_94)

	def parameter_8_id_95_led_listener(self):
		self.feedback_brain(self.parameter_8_id_95)

	def send_1_id_97_led_listener(self):
		self.feedback_brain(self.send_1_id_97)

	def send_2_id_98_led_listener(self):
		self.feedback_brain(self.send_2_id_98)

	def send_3_id_99_led_listener(self):
		self.feedback_brain(self.send_3_id_99)

	def send_4_id_100_led_listener(self):
		self.feedback_brain(self.send_4_id_100)

	def volume_9_id_101_led_listener(self):
		self.feedback_brain(self.volume_9_id_101)

	def pan_9_id_102_led_listener(self):
		self.feedback_brain(self.pan_9_id_102)

	def mute_9_id_103_led_listener(self):
		self.feedback_brain(self.mute_9_id_103)

	def send_1_id_106_led_listener(self):
		self.feedback_brain(self.send_1_id_106)

	def send_2_id_107_led_listener(self):
		self.feedback_brain(self.send_2_id_107)

	def send_3_id_108_led_listener(self):
		self.feedback_brain(self.send_3_id_108)

	def send_4_id_109_led_listener(self):
		self.feedback_brain(self.send_4_id_109)

	def volume_10_id_110_led_listener(self):
		self.feedback_brain(self.volume_10_id_110)

	def pan_10_id_111_led_listener(self):
		self.feedback_brain(self.pan_10_id_111)

	def mute_10_id_112_led_listener(self):
		self.feedback_brain(self.mute_10_id_112)

	def send_1_id_115_led_listener(self):
		self.feedback_brain(self.send_1_id_115)

	def send_2_id_116_led_listener(self):
		self.feedback_brain(self.send_2_id_116)

	def send_3_id_117_led_listener(self):
		self.feedback_brain(self.send_3_id_117)

	def send_4_id_118_led_listener(self):
		self.feedback_brain(self.send_4_id_118)

	def volume_11_id_119_led_listener(self):
		self.feedback_brain(self.volume_11_id_119)

	def pan_11_id_120_led_listener(self):
		self.feedback_brain(self.pan_11_id_120)

	def mute_11_id_121_led_listener(self):
		self.feedback_brain(self.mute_11_id_121)

	def send_1_id_124_led_listener(self):
		self.feedback_brain(self.send_1_id_124)

	def send_2_id_125_led_listener(self):
		self.feedback_brain(self.send_2_id_125)

	def send_3_id_126_led_listener(self):
		self.feedback_brain(self.send_3_id_126)

	def send_4_id_127_led_listener(self):
		self.feedback_brain(self.send_4_id_127)

	def volume_12_id_128_led_listener(self):
		self.feedback_brain(self.volume_12_id_128)

	def pan_12_id_129_led_listener(self):
		self.feedback_brain(self.pan_12_id_129)

	def mute_12_id_130_led_listener(self):
		self.feedback_brain(self.mute_12_id_130)

	def send_1_id_133_led_listener(self):
		self.feedback_brain(self.send_1_id_133)

	def send_2_id_134_led_listener(self):
		self.feedback_brain(self.send_2_id_134)

	def send_3_id_135_led_listener(self):
		self.feedback_brain(self.send_3_id_135)

	def send_4_id_136_led_listener(self):
		self.feedback_brain(self.send_4_id_136)

	def volume_13_id_137_led_listener(self):
		self.feedback_brain(self.volume_13_id_137)

	def pan_13_id_138_led_listener(self):
		self.feedback_brain(self.pan_13_id_138)

	def mute_13_id_139_led_listener(self):
		self.feedback_brain(self.mute_13_id_139)

	def send_1_id_142_led_listener(self):
		self.feedback_brain(self.send_1_id_142)

	def send_2_id_143_led_listener(self):
		self.feedback_brain(self.send_2_id_143)

	def send_3_id_144_led_listener(self):
		self.feedback_brain(self.send_3_id_144)

	def send_4_id_145_led_listener(self):
		self.feedback_brain(self.send_4_id_145)

	def volume_14_id_146_led_listener(self):
		self.feedback_brain(self.volume_14_id_146)

	def pan_14_id_147_led_listener(self):
		self.feedback_brain(self.pan_14_id_147)

	def mute_14_id_148_led_listener(self):
		self.feedback_brain(self.mute_14_id_148)

	def send_1_id_151_led_listener(self):
		self.feedback_brain(self.send_1_id_151)

	def send_2_id_152_led_listener(self):
		self.feedback_brain(self.send_2_id_152)

	def send_3_id_153_led_listener(self):
		self.feedback_brain(self.send_3_id_153)

	def send_4_id_154_led_listener(self):
		self.feedback_brain(self.send_4_id_154)

	def volume_15_id_155_led_listener(self):
		self.feedback_brain(self.volume_15_id_155)

	def pan_15_id_156_led_listener(self):
		self.feedback_brain(self.pan_15_id_156)

	def mute_15_id_157_led_listener(self):
		self.feedback_brain(self.mute_15_id_157)

	def send_1_id_160_led_listener(self):
		self.feedback_brain(self.send_1_id_160)

	def send_2_id_161_led_listener(self):
		self.feedback_brain(self.send_2_id_161)

	def send_3_id_162_led_listener(self):
		self.feedback_brain(self.send_3_id_162)

	def send_4_id_163_led_listener(self):
		self.feedback_brain(self.send_4_id_163)

	def volume_16_id_164_led_listener(self):
		self.feedback_brain(self.volume_16_id_164)

	def pan_16_id_165_led_listener(self):
		self.feedback_brain(self.pan_16_id_165)

	def mute_16_id_166_led_listener(self):
		self.feedback_brain(self.mute_16_id_166)

	def mode_selector_1_id_168_led_listener(self):
		self.feedback_brain(self.mode_selector_1_id_168)

	def volume_1_id_174_led_listener(self):
		self.feedback_brain(self.volume_1_id_174)

	def pan_1_id_175_led_listener(self):
		self.feedback_brain(self.pan_1_id_175)

	def volume_2_id_182_led_listener(self):
		self.feedback_brain(self.volume_2_id_182)

	def pan_2_id_183_led_listener(self):
		self.feedback_brain(self.pan_2_id_183)

	def volume_3_id_190_led_listener(self):
		self.feedback_brain(self.volume_3_id_190)

	def pan_3_id_191_led_listener(self):
		self.feedback_brain(self.pan_3_id_191)

	def volume_4_id_198_led_listener(self):
		self.feedback_brain(self.volume_4_id_198)

	def pan_4_id_199_led_listener(self):
		self.feedback_brain(self.pan_4_id_199)

	def volume_5_id_206_led_listener(self):
		self.feedback_brain(self.volume_5_id_206)

	def pan_5_id_207_led_listener(self):
		self.feedback_brain(self.pan_5_id_207)

	def volume_6_id_214_led_listener(self):
		self.feedback_brain(self.volume_6_id_214)

	def pan_6_id_215_led_listener(self):
		self.feedback_brain(self.pan_6_id_215)

	def volume_7_id_222_led_listener(self):
		self.feedback_brain(self.volume_7_id_222)

	def pan_7_id_223_led_listener(self):
		self.feedback_brain(self.pan_7_id_223)

	def volume_8_id_230_led_listener(self):
		self.feedback_brain(self.volume_8_id_230)

	def pan_8_id_231_led_listener(self):
		self.feedback_brain(self.pan_8_id_231)

	def parameter_1_id_234_led_listener(self):
		self.feedback_brain(self.parameter_1_id_234)

	def parameter_2_id_235_led_listener(self):
		self.feedback_brain(self.parameter_2_id_235)

	def parameter_3_id_236_led_listener(self):
		self.feedback_brain(self.parameter_3_id_236)

	def parameter_4_id_237_led_listener(self):
		self.feedback_brain(self.parameter_4_id_237)

	def parameter_5_id_238_led_listener(self):
		self.feedback_brain(self.parameter_5_id_238)

	def parameter_6_id_239_led_listener(self):
		self.feedback_brain(self.parameter_6_id_239)

	def parameter_7_id_240_led_listener(self):
		self.feedback_brain(self.parameter_7_id_240)

	def parameter_8_id_241_led_listener(self):
		self.feedback_brain(self.parameter_8_id_241)

	def volume_9_id_248_led_listener(self):
		self.feedback_brain(self.volume_9_id_248)

	def pan_9_id_249_led_listener(self):
		self.feedback_brain(self.pan_9_id_249)

	def volume_10_id_256_led_listener(self):
		self.feedback_brain(self.volume_10_id_256)

	def pan_10_id_257_led_listener(self):
		self.feedback_brain(self.pan_10_id_257)

	def volume_11_id_264_led_listener(self):
		self.feedback_brain(self.volume_11_id_264)

	def pan_11_id_265_led_listener(self):
		self.feedback_brain(self.pan_11_id_265)

	def volume_12_id_272_led_listener(self):
		self.feedback_brain(self.volume_12_id_272)

	def pan_12_id_273_led_listener(self):
		self.feedback_brain(self.pan_12_id_273)

	def volume_13_id_280_led_listener(self):
		self.feedback_brain(self.volume_13_id_280)

	def pan_13_id_281_led_listener(self):
		self.feedback_brain(self.pan_13_id_281)

	def volume_14_id_288_led_listener(self):
		self.feedback_brain(self.volume_14_id_288)

	def pan_14_id_289_led_listener(self):
		self.feedback_brain(self.pan_14_id_289)

	def volume_15_id_296_led_listener(self):
		self.feedback_brain(self.volume_15_id_296)

	def pan_15_id_297_led_listener(self):
		self.feedback_brain(self.pan_15_id_297)

	def volume_16_id_304_led_listener(self):
		self.feedback_brain(self.volume_16_id_304)

	def pan_16_id_305_led_listener(self):
		self.feedback_brain(self.pan_16_id_305)

	def solo_1_id_328_led_listener(self):
		self.feedback_brain(self.solo_1_id_328)

	def solo_2_id_329_led_listener(self):
		self.feedback_brain(self.solo_2_id_329)

	def solo_3_id_330_led_listener(self):
		self.feedback_brain(self.solo_3_id_330)

	def solo_4_id_331_led_listener(self):
		self.feedback_brain(self.solo_4_id_331)

	def solo_5_id_332_led_listener(self):
		self.feedback_brain(self.solo_5_id_332)

	def solo_6_id_333_led_listener(self):
		self.feedback_brain(self.solo_6_id_333)

	def solo_7_id_334_led_listener(self):
		self.feedback_brain(self.solo_7_id_334)

	def solo_8_id_335_led_listener(self):
		self.feedback_brain(self.solo_8_id_335)

	def solo_9_id_336_led_listener(self):
		self.feedback_brain(self.solo_9_id_336)

	def solo_10_id_337_led_listener(self):
		self.feedback_brain(self.solo_10_id_337)

	def solo_11_id_338_led_listener(self):
		self.feedback_brain(self.solo_11_id_338)

	def solo_12_id_339_led_listener(self):
		self.feedback_brain(self.solo_12_id_339)

	def solo_13_id_340_led_listener(self):
		self.feedback_brain(self.solo_13_id_340)

	def solo_14_id_341_led_listener(self):
		self.feedback_brain(self.solo_14_id_341)

	def solo_15_id_342_led_listener(self):
		self.feedback_brain(self.solo_15_id_342)

	def solo_16_id_343_led_listener(self):
		self.feedback_brain(self.solo_16_id_343)

	def mode_selector_1_copy_id_346_led_listener(self):
		self.feedback_brain(self.mode_selector_1_copy_id_346)

	def session_box_navigation_1_copy_id_347_led_listener(self):
		self.feedback_brain(self.session_box_navigation_1_copy_id_347)

################################################
################## CORE v1.2 #################
################################################
	def placehold_listener(self, value):
		return
	def pick_brain(self, obj):
		cnfg = obj.copy() 
		if cnfg["output_type"] == "val":
				self.val_brain(cnfg)
		elif cnfg["output_type"] == "func":
			self.func_brain(cnfg)
		elif cnfg["output_type"] == "bool":
			self.bool_brain(cnfg)
	def should_it_fire(self, cnfg):
		controller = getattr(self, cnfg["attached_to"])
		cnfg["value"] = controller.cur_val 
		cnfg["pre_val"] = controller.pre_val 
		cnfg["prev_press_time"] = controller.prev_press_time
		timenow = time.time()
		fire = 0;
		if (cnfg["ctrl_type"] == "on/off" or cnfg["ctrl_type"] == "increment" or cnfg["ctrl_type"] == "decrement"): 
			if(cnfg["switch_type"] == "delay"):
				if((cnfg["value"] == cnfg["enc_second"]) and (timenow - cnfg["prev_press_time"]) > cnfg["delay_amount"]):
					fire = 1;
			elif(cnfg["switch_type"] == "toggle"):
				if cnfg["value"] == cnfg["enc_first"] or cnfg["value"] == cnfg["enc_second"]:
					fire = 1;
			elif (cnfg["switch_type"] == "momentary" and cnfg["value"] == cnfg["enc_first"]):
				fire = 1;
		elif cnfg["ctrl_type"] == "absolute":
			if cnfg["value"] >= cnfg["enc_first"] and cnfg["value"] <= cnfg["enc_second"]:
				fire = 1;
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["value"] == cnfg["enc_first"] or cnfg["value"] == cnfg["enc_second"]:
				fire = 1;
		return fire
	def bool_brain(self, cnfg):
		method_to_call = getattr(eval(cnfg["module"]), cnfg["element"])
		fire = self.should_it_fire(cnfg)
		if fire == 1:	
			if method_to_call is False:
				setattr(eval(cnfg["module"]), cnfg["element"], True)
			else: 
				setattr(eval(cnfg["module"]), cnfg["element"], False)
	def func_brain(self, cnfg):
		fire = self.should_it_fire(cnfg)
		if fire == 1: 
			method_to_call = getattr(eval(cnfg["module"]), cnfg["element"])
			if cnfg["func_arg"] != "" and cnfg["func_arg"] != "cnfg":
				method_to_call(cnfg["func_arg"]) 
			elif cnfg["func_arg"] == "cnfg":
				method_to_call(cnfg) 
			else: 
				method_to_call()
	def val_brain(self, cnfg):
		try:
			cnfg["current_position"] = getattr(eval(cnfg["module"]), cnfg["element"]) 
		except:
			self.show_message("This control does not exist in your session")
			return
		self._parameter_to_map_to = eval(cnfg["module"])
		if cnfg["ctrl_type"] != "on/off" and hasattr(self._parameter_to_map_to, "max") and hasattr(self._parameter_to_map_to, "min"):
			param_range = self._parameter_to_map_to.max - self._parameter_to_map_to.min
			if cnfg.has_key("minimum"):
				usermin = cnfg["minimum"] / 100.;
				min_value = float(usermin * param_range) 
				cnfg["minimum"] = min_value + self._parameter_to_map_to.min
			if cnfg.has_key("maximum") and cnfg["mapping_type"] != "On/Off":
				usermax = cnfg["maximum"] / 100.;
				max_value = float(usermax * param_range) 
				cnfg["maximum"] = max_value + self._parameter_to_map_to.min
		controller = getattr(self, cnfg["attached_to"])
		cnfg["value"] = controller.cur_val 
		cnfg["pre_val"] = controller.pre_val 
		if cnfg.has_key("decimal_places"):
			cnfg["current_position"] = round(cnfg["current_position"], cnfg["decimal_places"])
		if cnfg["ctrl_type"] == "absolute":
			cnfg["steps"] = (cnfg["enc_second"] - cnfg["enc_first"]) 
		if cnfg["ctrl_type"] != "on/off":
			cnfg["distance"] = cnfg["maximum"] - cnfg["minimum"] 
			cnfg["speed"] = cnfg["distance"] / cnfg["steps"] 
			cnfg["step_values"] = self.step_values(cnfg) 
			cnfg["velocity_seq"] = self._velocity_seq(cnfg) 
		
		if int(cnfg["current_position"]) < int(cnfg["minimum"]) or int(cnfg["current_position"]) > int(cnfg["maximum"]):
			new_val = self.snap_to_max_min(cnfg)
		elif cnfg["ctrl_type"] == "absolute":
			new_val = self.absolute_decision(cnfg)
		elif cnfg["ctrl_type"] == "relative":
			new_val = self.relative_decision(cnfg)
		elif cnfg["ctrl_type"] == "on/off" or cnfg["ctrl_type"] == "increment" or cnfg["ctrl_type"] == "decrement":
			new_val = self.button_decision(cnfg)
		try:
			setattr(eval(cnfg["module"]), cnfg["element"], new_val)
		except:
			return
	def snap_to_max_min(self, cnfg):
		if cnfg["snap_to"] == True and cnfg["value"] >= cnfg["enc_first"] and cnfg["value"] <= cnfg["enc_second"]:
			if int(cnfg["current_position"]) < int(cnfg["minimum"]):
				new_val = cnfg["minimum"]
				self.log("snapped to min")
			elif int(cnfg["current_position"]) > int(cnfg["maximum"]):
				new_val = cnfg["maximum"]
				self.log("snapped to max")
		else:
			new_val = cnfg["current_position"]
			self.show_message("remotify: snapping is off for this control. Check min / max values")
		return new_val
	def step_values(self, cnfg):
		calc = []
		for i in range(0, cnfg["steps"] +1):
			val = (i * cnfg["speed"]) + cnfg["minimum"]
			if cnfg.has_key("decimal_places"):
				val = round(val, cnfg["decimal_places"])
			calc.append(val)
		if "reverse_mode" in cnfg and cnfg["reverse_mode"] is True:
			calc = list(reversed(calc))
		return calc
	def relative_decision(self, cnfg):
		fire = 0
		new_val = cnfg["current_position"] 
		if cnfg["value"] == cnfg["enc_second"]: 
			max_min = "max" 
			fire = 1
		elif cnfg["value"] == cnfg["enc_first"]: 
			max_min = "min" 
			fire = 1
		if fire == 0:
			return new_val
		if cnfg["current_position"] in cnfg["step_values"]:
			current_pos_index = cnfg["step_values"].index(cnfg["current_position"])
			
			feedback = current_pos_index / cnfg["steps"] * 127
			feedback = round(feedback, 0)
			method_to_call = getattr(self, cnfg["attached_to"])
			incr_index = current_pos_index + 1
			decr_index = current_pos_index - 1
			if max_min == "max" and incr_index < len(cnfg["step_values"]): 
				incr = cnfg["step_values"][incr_index]
				while incr == cnfg["current_position"]:
					incr_index = incr_index + 1
					if incr_index < len(cnfg["step_values"]):
						incr = cnfg["step_values"][incr_index]
					else:
						break
				new_val = incr
			elif max_min == "min" and decr_index >= 0: 
				decr = cnfg["step_values"][decr_index]
				new_val = decr
			return new_val    
		else:   
			new_val = self.step_in_line(cnfg, max_min)
			return new_val
		return new_val
	def percent_as_value(self, param, percentage):
		param = 		eval(param)
		if hasattr(param, 'max') and hasattr(param, 'min'):
			param_range = param.max - param.min
			val = percentage * param_range / 100
			return val
		else: 
			self.log("param does not have min and/or max attribute(s)")
	def button_decision(self, cnfg):
		new_val = cnfg["current_position"] 
		fire = self.should_it_fire(cnfg)
		if fire == 0:
			return new_val;
		if cnfg["ctrl_type"] == "on/off":
			if(cnfg["switch_type"] == "toggle"):
				if cnfg["value"] == cnfg["enc_first"]:
					new_val = cnfg["maximum"]
					return new_val
				elif cnfg["value"] == cnfg["enc_second"]:
					new_val = cnfg["minimum"]
					return new_val
			elif(cnfg["switch_type"] == "momentary"):
				if(cnfg["current_position"] == cnfg["maximum"]):
					new_val = cnfg["minimum"]
				else: 
					new_val = cnfg["maximum"]
				return new_val
			elif(cnfg["switch_type"] == "delay"):
				if(cnfg["current_position"] == cnfg["maximum"]):
					new_val = cnfg["minimum"]
				elif (cnfg["current_position"] == cnfg["minimum"]):
					new_val = cnfg["maximum"]
				return new_val
			else:
				self.log("neither momentary or toggle were set for on off button")
				return new_val
		if cnfg["current_position"] in cnfg["step_values"]:
			current_pos_index = cnfg["step_values"].index(cnfg["current_position"])
			incr_index = current_pos_index + 1
			decr_index = current_pos_index - 1
			if cnfg["ctrl_type"] ==  "increment" and incr_index < len(cnfg["step_values"]): 
				incr = cnfg["step_values"][incr_index]
				new_val = incr
			elif cnfg["ctrl_type"] == "decrement" and decr_index >= 0: 
				decr = cnfg["step_values"][decr_index]
				new_val = decr
			return new_val
		else:
			if cnfg["ctrl_type"] ==  "increment": 
				max_min = "max"
			elif cnfg["ctrl_type"] == "decrement": max_min = "min"
			new_val = self.step_in_line(cnfg, max_min)
			return new_val
		return new_val
	def step_in_line(self, cnfg, max_min):
		previous = ""
		step_num = 0
		speed = 0 
		for step_val in cnfg["step_values"]:
			step_num += 1
			if cnfg["current_position"] > previous and cnfg["current_position"] < step_val:
				if max_min == "min":
					speed = cnfg["current_position"] - previous 
					new_val = previous
				elif max_min == "max":
					speed = step_val - cnfg["current_position"] 
					new_val = step_val
				break
			previous = step_val
		return new_val
	def absolute_decision(self, cnfg):
		if(cnfg["enc_first"] > cnfg["enc_second"]):
			self.log("enc_first is higher than enc_second, needs to be lower")
		new_val = cnfg["current_position"] 
		if cnfg["pre_val"] is None:
			return new_val
		######### Get pre_val details from list values ######### 
		######### ######### ######### ######## ######
		if cnfg["pre_val"] in cnfg["velocity_seq"]: 
			cnfg["previous_step_num"] = cnfg["velocity_seq"].index(cnfg["pre_val"]) 
			cnfg["previous_step_value"] = cnfg["step_values"][cnfg["previous_step_num"]] 
		else:
			cnfg["previous_step_value"] = None
		######### get value details from list ######### 
		######### ######### ######### ######### ######
		if cnfg["value"] in cnfg["velocity_seq"]:
			cnfg["step_num"] = cnfg["velocity_seq"].index(cnfg["value"]) 
			cnfg["step_value"] = cnfg["step_values"][cnfg["step_num"]] 
		else: 
			cnfg["step_num"] = None
			cnfg["step_value"] = None
			
		######### MAX OR MIN ########
		######### ######### ######### 
		if cnfg["reverse_mode"] is False:
			if cnfg["value"] > cnfg["pre_val"]: max_min = "max"
			elif cnfg["value"] < cnfg["pre_val"]: max_min = "min"
		elif cnfg["reverse_mode"] is True:
			if cnfg["value"] > cnfg["pre_val"]: max_min = "min"
			elif cnfg["value"] < cnfg["pre_val"]: max_min = "max"
		inside_outside = self.inside_outside_checks(cnfg)
		if inside_outside is not False:
			self.log("inside outside was not false")
			return inside_outside
		######### straight assign or takeover ######### 
		######### ######### ######### ######### #######
		if cnfg["previous_step_value"] == cnfg["current_position"]:
			new_val = cnfg["step_value"]
		elif cnfg["takeover_mode"] == "None": 
			new_val = cnfg["step_value"]
		elif cnfg["takeover_mode"] == "Pickup": 
			new_val = self.pickup(cnfg, max_min)
		elif cnfg["takeover_mode"] == "Value scaling": new_val = self.value_scaling(cnfg, max_min)
		else: self.log("nothing got decided")
			
		return new_val
	def inside_outside_checks(self, cnfg):
		new_val = cnfg["current_position"]
		if cnfg["reverse_mode"] is False: 
			minimum = cnfg["minimum"]
			maximum = cnfg["maximum"]
		elif cnfg["reverse_mode"] is True: 
			minimum = cnfg["maximum"]
			maximum = cnfg["minimum"]
		######### was outside and is still outside ######
		######### ######### ######### ######### ######### 
		if (cnfg["pre_val"] < cnfg["enc_first"] and cnfg["value"] < cnfg["enc_first"]):
			self.log("was below and still below")
			return new_val
		elif (cnfg["pre_val"] > cnfg["enc_second"] and cnfg["value"] > cnfg["enc_second"]):
			self.log("was above and still above")
			return new_val
		## 1. Going Below
		if (cnfg["pre_val"] >= cnfg["enc_first"] and cnfg["value"] < cnfg["enc_first"]): 
			self.log("going below enter")
			if cnfg["takeover_mode"] == "Pickup":
				if cnfg["reverse_mode"] is False and cnfg["current_position"] > cnfg["previous_step_value"]:
					return new_val
				elif cnfg["reverse_mode"] is True and cnfg["current_position"] < cnfg["previous_step_value"]:
					return new_val
			if cnfg["reverse_mode"] is False:
				new_val = minimum
				self.log("going below 1")
				return new_val
			elif cnfg["reverse_mode"] is True:
				new_val = minimum
				self.log("going below 2")
				return new_val
		## 2. Going Above
		if (cnfg["pre_val"] <= cnfg["enc_second"] and cnfg["value"] > cnfg["enc_second"]):
			if cnfg["takeover_mode"] == "Pickup":
				self.log("THIS SHOULD FIRE 1")
				if cnfg["reverse_mode"] is False and cnfg["current_position"] < cnfg["previous_step_value"]:
					self.log("THIS SHOULD FIRE 2")
					return new_val
				elif cnfg["reverse_mode"] is True and cnfg["current_position"] > cnfg["previous_step_value"]:
					return new_val 
			if cnfg["reverse_mode"] is False:
				new_val = maximum
				self.log("going above 1")
				return new_val
			elif cnfg["reverse_mode"] is True:
				new_val = maximum
				self.log("going above 2")
				return new_val
		#########  >>0<< Coming inside ########
		######### ######### ######### ######### 
		if (cnfg["pre_val"] < cnfg["enc_first"] and cnfg["value"] >= cnfg["enc_first"]):
			self.log("come in from below")
			
		elif (cnfg["pre_val"] > cnfg["enc_second"] and cnfg["value"] <= cnfg["enc_second"]):
			self.log("coming in from above")
		return False
	def _velocity_seq(self,cnfg):
		number_of_steps = cnfg['enc_second'] - cnfg['enc_first']
		arr = []
		i = 0
		sequence_num = cnfg['enc_first']
		while i <= number_of_steps:
			arr.append(sequence_num)
			i += 1
			sequence_num += 1
		return arr
	def pickup(self, cnfg, max_min):
		new_val = cnfg["current_position"] 
		found = False
		if cnfg["previous_step_value"] is None:
			self.log("just entered")
			
			if cnfg["reverse_mode"] is False:
				if cnfg["pre_val"] < cnfg["enc_first"] and cnfg["step_value"] > cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 1 found")
				elif cnfg["pre_val"] > cnfg["enc_second"] and cnfg["step_value"] < cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 2 found")
			elif cnfg["reverse_mode"] is True:
				if cnfg["pre_val"] < cnfg["enc_first"] and cnfg["step_value"] < cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 3 found")
				elif cnfg["pre_val"] > cnfg["enc_second"] and cnfg["step_value"] > cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 4 found")
		
		else:
			self.log("we were already in here")
			
			if cnfg["previous_step_value"] < cnfg["current_position"] and cnfg["step_value"] > cnfg["current_position"]: 
				new_val = cnfg["step_value"]
				found = True
				self.log("pickup 4 found")
			elif cnfg["previous_step_value"] > cnfg["current_position"] and cnfg["step_value"] < cnfg["current_position"] :
				new_val = cnfg["step_value"]
				found = True  
				self.log("pickup 5 found")
			else: 
				self.log("waiting for pickup")
		if found is False:
			msg = "remotify says: waiting for pickup " + str(cnfg["step_value"]) + " >> " + str(cnfg["current_position"])
			self.show_message(msg)
		return new_val
		step_num = cnfg["step_num"]
		step_value = cnfg["step_value"]
		remaining_steps = cnfg["steps"] - step_num 
		new_val = cnfg["current_position"] 
		distance_to_max = cnfg["maximum"] - cnfg["current_position"]
		distance_to_min = cnfg["current_position"] - cnfg["minimum"]
		speed_to_max = 0
		speed_to_min = 0
		if cnfg["current_position"] >= cnfg["minimum"] and cnfg["current_position"] <= cnfg["maximum"]:
			if max_min == "max" and distance_to_max > 0:
				if cnfg["reverse_mode"] is False and remaining_steps > 0: speed_to_max = distance_to_max / remaining_steps
				elif cnfg["reverse_mode"] is True and step_num > 0: speed_to_max = distance_to_max / step_num
				if speed_to_max is not 0: new_val = speed_to_max + cnfg["current_position"]
			elif max_min == "min" and distance_to_min > 0:
				if cnfg["reverse_mode"] is False and step_num > 0: speed_to_min = distance_to_min / step_num
				elif cnfg["reverse_mode"] is True and remaining_steps > 0: speed_to_min = distance_to_min / remaining_steps
				if speed_to_min is not 0: new_val = cnfg["current_position"] - speed_to_min
		return new_val
	def value_scaling(self, cnfg, max_min):
		step_num = cnfg["step_num"]
		step_value = cnfg["step_value"]
		remaining_steps = cnfg["steps"] - step_num 
		new_val = cnfg["current_position"] 
		distance_to_max = cnfg["maximum"] - cnfg["current_position"]
		distance_to_min = cnfg["current_position"] - cnfg["minimum"]
		speed_to_max = 0
		speed_to_min = 0
		if cnfg["current_position"] >= cnfg["minimum"] and cnfg["current_position"] <= cnfg["maximum"]:
			if max_min == "max" and distance_to_max > 0:
				if cnfg["reverse_mode"] is False and remaining_steps > 0: speed_to_max = distance_to_max / remaining_steps
				elif cnfg["reverse_mode"] is True and step_num > 0: speed_to_max = distance_to_max / step_num
				if speed_to_max is not 0: new_val = speed_to_max + cnfg["current_position"]
			elif max_min == "min" and distance_to_min > 0:
				if cnfg["reverse_mode"] is False and step_num > 0: speed_to_min = distance_to_min / step_num
				elif cnfg["reverse_mode"] is True and remaining_steps > 0: speed_to_min = distance_to_min / remaining_steps
				if speed_to_min is not 0: new_val = cnfg["current_position"] - speed_to_min
		return new_val
	def track_num(self, track_num):
		if ((hasattr(self, '_session')) and (self._session is not None)):
			track_num = track_num + self._session._track_offset
		else: 
			track_num = track_num
		return track_num
	def scene_num(self, scene_num):
		if ((hasattr(self, '_session')) and (self._session is not None)):
			scene_num = scene_num + self._session._scene_offset 
		else: 
			scene_num = scene_num
		return scene_num
	def log_cnfg_settings(self, cnfg):
		for i in cnfg:
			text = i + ": " + str(cnfg[i])
			self.log(text)
	def dump(self, obj):
		for attr in dir(obj):
			self.log("csslog: obj.%s = %r" % (attr, getattr(obj, attr)))
	def log(self, msg):
		if self.debug_on is True:
			self.log_message("csslog:" + str(msg))
	def pret(self, ugly):
		for key,value in sorted(ugly.items()):
			self.log_message(key)
			self.log_message(value)
			self.log_message("")
	################################################
	############# Extra Functions: LED Functions ###
	################################################
	def _quantizeDict(self):
		grid_setting = str(self.song().view.highlighted_clip_slot.clip.view.grid_quantization)
		is_it_triplet = self.song().view.highlighted_clip_slot.clip.view.grid_is_triplet
		if (is_it_triplet is True):
			grid_setting += "_triplet"
		RecordingQuantization = Live.Song.RecordingQuantization
		quantDict = {}
		quantDict["g_thirtysecond"] = RecordingQuantization.rec_q_thirtysecond
		quantDict["g_sixteenth"] = RecordingQuantization.rec_q_sixtenth
		quantDict["g_eighth"] = RecordingQuantization.rec_q_eight
		quantDict["g_quarter"] = RecordingQuantization.rec_q_quarter
		quantDict["g_eighth_triplet"] = RecordingQuantization.rec_q_eight_triplet
		quantDict["g_sixteenth_triplet"] = RecordingQuantization.rec_q_sixtenth_triplet
		return quantDict[grid_setting];
	def _arm_follow_track_selection(self):
		for track in self.song().tracks:
			if track.can_be_armed:
				track.arm = False
		if self.song().view.selected_track.can_be_armed:
			self.song().view.selected_track.arm = True
	def turn_inputs_off(self): 
		send_feedback = False
		if hasattr(self, "global_feedback"): 
			if self.global_feedback == "custom":
				if self.global_feedback_active == True: 
					send_feedback = True
			elif hasattr(self, "controller_LED_on") and hasattr(self, "controller_LED_off"):
				send_feedback = True
		if send_feedback == True: 
			for input_name in self.input_map:
				input_ctrl = getattr(self, input_name)
				input_ctrl.send_value(self.led_off)
	def feedback_brain(self, obj):
		cnfg = obj.copy() 
		try:
			method_to_call = getattr(self, cnfg["feedback_brain"])
			method_to_call(cnfg)
		except:
			return 
	def feedback_bool(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"] + "." + feedback_to["ui_listener"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		if(feedback_to["mapping_type"] == "Mute"):
			if param == False:
				send_val = ctrl_on
			elif param == True:
				send_val = ctrl_off
		else: 
			if param == True:
				send_val = ctrl_on
			elif param == False:
				send_val = ctrl_off
		self.feedback_handler(feedback_to, send_val)
	def feedback_on_off(self, feedback_to):
		param = 		eval(feedback_to["module"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		param_value = round(param.value,2) 
		mapping_type = str(feedback_to["mapping_type"])
		if feedback_to.has_key("maximum") and feedback_to.has_key("minimum"):
			max_val = feedback_to["maximum"]
			min_val = feedback_to["minimum"]
			if mapping_type != "On/Off":
				max_val = self.percent_as_value(feedback_to["module"], feedback_to["maximum"])
				max_val = round(max_val,2)
				min_val = self.percent_as_value(feedback_to["module"], feedback_to["minimum"])
				min_val = round(min_val,2)
		elif hasattr(param, "max") and hasattr(param, "min"): 
			max_val = param.max
			max_val = round(max_val,2)
			min_val = param.min
			min_val = round(min_val,2)
		else: 
			self.log_message(str(param) + " does not have a max/min param")
			return
		send_val = None
		if param_value == max_val:
			send_val = ctrl_on
		elif param_value == min_val:
			send_val = ctrl_off
		if send_val is not None:
			self.feedback_handler(feedback_to, send_val)
		else: 
			return
	def feedback_increment(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		mapping_type = str(feedback_to["mapping_type"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		snapping = feedback_to["snap_to"]
		mapping_type = str(feedback_to["mapping_type"])
		if feedback_to.has_key("maximum") and feedback_to.has_key("minimum"):
			max_val = feedback_to["maximum"]
			min_val = feedback_to["minimum"]
			if mapping_type != "On/Off":
				max_val = self.percent_as_value(feedback_to["module"], feedback_to["maximum"])
				min_val = self.percent_as_value(feedback_to["module"], feedback_to["minimum"])
		elif hasattr(param, "max") and hasattr(param, "min"): 
			max_val = param.max
			min_val = param.min
		else: 
			self.log_message(str(param) + " does not have a max/min param")
			return
		if snapping == False and param.value < min_val:
			send_val = ctrl_off
		elif param.value < max_val: 
			send_val = ctrl_on
		else: 
			send_val = ctrl_off
		self.feedback_handler(feedback_to, send_val)
	def feedback_decrement(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		mapping_type = str(feedback_to["mapping_type"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		snapping = feedback_to["snap_to"]
		if feedback_to.has_key("maximum") and feedback_to.has_key("minimum"):
			max_val = feedback_to["maximum"]
			min_val = feedback_to["minimum"]
			if mapping_type != "On/Off":
				max_val = self.percent_as_value(feedback_to["module"], feedback_to["maximum"])
				min_val = self.percent_as_value(feedback_to["module"], feedback_to["minimum"])
		elif hasattr(param, "max") and hasattr(param, "min"): 
			max_val = param.max
			min_val = param.min
		else: 
			self.log_message(str(param) + " does not have a max/min param")
			return
		if snapping == False and param.value > max_val:
			send_val = ctrl_off
		elif param.value > min_val: 
			send_val = ctrl_on
		else: 
			send_val = ctrl_off
		self.feedback_handler(feedback_to, send_val)
	def feedback_which_ctrl_on_off(self, feedback_to, on_off):
		if feedback_to["LED_feedback"] == "default":
			ctrl_on = self.led_on
			ctrl_off = self.led_off
		elif feedback_to["LED_feedback"] == "custom":
			if feedback_to["ctrl_type"] == "on/off" or feedback_to["ctrl_type"] == "increment" or feedback_to["ctrl_type"] == "decrement":
				ctrl_on = feedback_to["LED_on"]
				ctrl_off = feedback_to["LED_off"]
			elif feedback_to["ctrl_type"] == "absolute" or feedback_to["ctrl_type"] == "relative":
				ctrl_on = feedback_to["enc_first"]
				ctrl_off = feedback_to["enc_second"]
		if on_off == "on":
			value = ctrl_on
		elif on_off == "off":
			value = ctrl_off
		return value;
	def feedback_range(self, feedback_to):
		if feedback_to['ctrl_type'] == "on/off":
			self.feedback_on_off(feedback_to)
		elif feedback_to['ctrl_type'] == "increment":
			self.feedback_increment(feedback_to)
		elif feedback_to['ctrl_type'] == "decrement":
			self.feedback_decrement(feedback_to)
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		ctrl_min = 	feedback_to["minimum"]
		ctrl_max = 	feedback_to["maximum"]
		ctrl_type = feedback_to["ctrl_type"]
		default_ctrl_first = 0 
		default_ctrl_last = 127 
		if ctrl_type == "relative":
			crl_reverse = False
			ctrl_first = 0
			ctrl_last = 127
		else:
			crl_reverse = feedback_to["reverse_mode"]
			ctrl_first = feedback_to["enc_first"]
			ctrl_last = feedback_to["enc_second"]
		param_range = param.max - param.min 
		orig_param_range = param.max - param.min
		param_range = ctrl_max * orig_param_range / 100
		ctrl_min_as_val = ctrl_min * orig_param_range / 100
		param_range = param_range - ctrl_min_as_val
		param_value = param.value - ctrl_min_as_val
		
		if orig_param_range == 2.0 and param.min == -1.0:
			param_value = param_value + 1 
		percentage_control_is_at = param_value / param_range * 100
		ctrl_range = ctrl_last - ctrl_first
		percentage_of_ctrl_range = ctrl_range * percentage_control_is_at / 100 + ctrl_first
		percentage_of_ctrl_range = round(percentage_of_ctrl_range,0)
		if crl_reverse == True:
			percentage_of_ctrl_range = ctrl_range - percentage_of_ctrl_range
		self.feedback_handler(feedback_to, percentage_of_ctrl_range)
	def feedback_a_b_crossfade_assign(self, feedback_to):
		assigned_val = eval(str(feedback_to['parent_track']) + ".mixer_device.crossfade_assign")
		if(assigned_val == 0):
			send_val = feedback_to["LED_on"]
		elif(assigned_val == 1):
			send_val = feedback_to["LED_off"]
		elif(assigned_val == 2):
			send_val = feedback_to["LED_assigned_to_b"]
		else: 
			send_val = 0
		self.feedback_handler(feedback_to, send_val)
	def feedback_handler(self, config, send_val):
		send_feedback = False
		if config.has_key("LED_feedback"):
			if config["LED_feedback"] == "custom": 
				if config["LED_feedback_active"] == "1" or config["LED_feedback_active"] == "true": 
					send_feedback = True
			elif hasattr(self, "global_feedback"): 
				if self.global_feedback == "custom":
					if self.global_feedback_active == True: 
						send_feedback = True
				elif hasattr(self, "controller_LED_on") and hasattr(self, "controller_LED_off"):
					send_feedback = True
			if send_feedback == True: 
				if config["LED_feedback"] == "custom":
					for item in config["LED_send_feedback_to_selected"]:
						feedback_control = 	eval("self." + str(item))
						feedback_control.send_value(send_val)
				else: 
					control = 	eval("self." + str(config["attached_to"]))
					control.send_value(send_val)
			else:
				self.log("feedback_handler says 'not sending led feedback'")
	def sess_highlight_banking_calculate(self, feedback_to, num_of_tracks_scenes, offset_is_at):
		ctrl_first = feedback_to["enc_first"]
		ctrl_last = feedback_to["enc_second"]
		ctrl_range = ctrl_last - ctrl_first
		if feedback_to['ctrl_type'] == "absolute" or feedback_to['ctrl_type'] == "relative":
			percentage_control_is_at = offset_is_at / num_of_tracks_scenes * 100
			velocity_val = ctrl_range * percentage_control_is_at / 100 + ctrl_first
			velocity_val = int(velocity_val) 
		elif feedback_to['ctrl_type'] == "on/off" or feedback_to['ctrl_type'] == "increment":
			if offset_is_at == num_of_tracks_scenes:
				velocity_val = feedback_to["LED_on"]
			else:
				velocity_val = feedback_to["LED_off"]
		elif feedback_to['ctrl_type'] == "decrement":
			if offset_is_at == 0:
				velocity_val = feedback_to["LED_off"]
			else:
				velocity_val = feedback_to["LED_on"]
		if feedback_to['ctrl_type'] == "absolute" and feedback_to["reverse_mode"] == True:
			velocity_val = ctrl_range - velocity_val
		self.feedback_handler(feedback_to, velocity_val)
	def feedback_scroll_mode_selector(self, feedback_to):
		global active_mode
		num_of_tracks_scenes = len(self.modes) - 1
		count = 0
		for mode_num in self.modes.values():
			if mode_num == active_mode:
				offset_is_at = count
				break
			count += 1
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_scroll_mode_selector_select(self, feedback_to):
		global active_mode
		mode_to_select = int(feedback_to["func_arg"])
		if int(active_mode) == mode_to_select:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_param_banking_select(self, feedback_to):
		banking_number = int(feedback_to["banking_number"])
		parent_device_id = feedback_to["parent_device_id"]
		offset_is_at = getattr(self, "device_id_" + str(parent_device_id) + "_active_bank")
		if banking_number == offset_is_at:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_param_banking(self, feedback_to):
		self.log_message("scroll banking fired")
		parent_device_id = feedback_to["parent_device_id"]
		bank_array = getattr(self, "device_id_" + str(parent_device_id) + "_banks")
		num_of_tracks_scenes = len(bank_array) - 1
		offset_is_at = getattr(self, "device_id_" + str(parent_device_id) + "_active_bank")
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_highlight_nav_select(self, feedback_to):
		tracks_or_scenes = feedback_to["tracks_scenes"]
		tracks_scene_num = int(feedback_to["highlight_number"])
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self.selected_track_idx()) - 1
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self.selected_scene_idx()) - 1
		if tracks_scene_num == offset_is_at:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_highlight_nav(self, feedback_to):
		tracks_or_scenes = feedback_to["tracks_scenes"]
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self.selected_track_idx()) - 1
			num_of_tracks_scenes = int(len(self.song().tracks)) - 1
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self.selected_scene_idx()) - 1
			num_of_tracks_scenes = int(len(self.song().scenes)) - 1
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_sessbox_nav_select(self, feedback_to):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to select for feedback")
			return
		tracks_scene_num = int(feedback_to["highlight_number"])
		tracks_or_scenes = feedback_to["tracks_scenes"]
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self._session.track_offset())
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self._session.scene_offset())
		if tracks_scene_num == offset_is_at:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_sessbox_nav(self, feedback_to):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to scroll for feedback sir.")
			return
		tracks_or_scenes = feedback_to["tracks_scenes"]
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self._session.track_offset())
			num_of_tracks_scenes = int(len(self.song().tracks)) - 1
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self._session.scene_offset())
			num_of_tracks_scenes = int(len(self.song().scenes)) - 1
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_tempo(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		ctrl_min = 	feedback_to["minimum"]
		ctrl_max = 	feedback_to["maximum"]
		ctrl_type = feedback_to["ctrl_type"]
		ctrl_first = feedback_to["enc_first"]
		ctrl_last = feedback_to["enc_second"]
		default_ctrl_first = 0 
		default_ctrl_last = 127 
		crl_reverse = feedback_to["reverse_mode"]
		param_range = ctrl_max - ctrl_min
		param = 		eval(feedback_to["module"] + "." + feedback_to["ui_listener"])
		zero = ctrl_min 
		if param < ctrl_min or param > ctrl_max:
			self.log("tempo is outside ctrl_min / ctrl_max")
		else:
			zerod_param = param - zero 
			percentage_control_is_at = zerod_param / param_range * 100
		ctrl_range = ctrl_last - ctrl_first
		percentage_of_ctrl_range = ctrl_range * percentage_control_is_at / 100 + ctrl_first
		if crl_reverse == True:
			percentage_of_ctrl_range = ctrl_range - percentage_of_ctrl_range
		self.feedback_handler(feedback_to, percentage_of_ctrl_range)
	def mode_device_bank_leds(self, mode_id):
		config_map = "mode_" + str(mode_id) + "_configs_map"
		config_map = getattr(self, config_map)
		for config_name in config_map:
			config = getattr(self, config_name)
			if config["mapping_type"] == "Parameter Bank":
				parent_id = config["parent_json_id"]
				bank_names_array_name = "device_id_" + str(parent_id) + "_banks"
				active_bank_name = "device_id_" + str(parent_id) + "_active_bank"
				bank_names_array = getattr(self, bank_names_array_name)
				active_bank = getattr(self, active_bank_name)
				for index, bank_name in enumerate(bank_names_array):
					if bank_name == config_name:
						if index == active_bank:
							led_on = config["LED_on"]
							self.feedback_handler(config, led_on)
						else: 
							led_off = config["LED_off"]
							self.feedback_handler(config, led_off)
	def bank_led_feedback(self, parent_device_id):
		global active_mode
		device = "device_id_" + str(parent_device_id);
		device_bank_array = getattr(self, device + "_banks")
		active_bank_idx = getattr(self, device + "_active_bank")
		device_bank_params = getattr(self, device + "_bank_parameters_" + str(active_bank_idx))
		for index, val in enumerate(device_bank_array):
			bank_cnfg = getattr(self, val)
			bank_cnfg["LED_feedback"] = "custom"; 
			if index == active_bank_idx:
					if bank_cnfg.has_key("LED_on"):
						led_on = bank_cnfg["LED_on"]
						self.feedback_handler(bank_cnfg, led_on)
			else: 
				if bank_cnfg.has_key("LED_off"):
					led_off = bank_cnfg["LED_off"]
					self.feedback_handler(bank_cnfg, led_off)
		
		remove_mode = getattr(self, "_remove_mode" + active_mode + "_ui_listeners")
		remove_mode()
		activate_mode = getattr(self, "_mode" + active_mode + "_ui_listeners")
		activate_mode()
		for param in device_bank_params:
			fire_param_feedback = getattr(self, param + "_led_listener")
			fire_param_feedback()
	def listening_to_devices(self):
		global active_mode, prev_active_mode, modes
		self.log("device added")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
	def _selected_device_listener(self):
		global active_mode, prev_active_mode, modes
		self.log("selected device changed")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
		self.device_feedback()
	def device_feedback(self, mode_id=None):
		if (mode_id == None):
			global active_mode
			mode_id = active_mode
		config_map = "mode_" + str(mode_id) + "_configs_map"
		config_map = getattr(self, config_map)
		for config_name in config_map:
			config = getattr(self, config_name)
			if config.has_key("mapping_type") and config["mapping_type"] == "Device":
				led_on = config["LED_on"]
				led_off = config["LED_off"]
				try: 
					device = eval(config["module"])
				except:
					self.feedback_handler(config, led_off)
					return
				find = config["module"].find("selected_track")
				if find >= 0: 
					selected_device = self.song().view.selected_track.view.selected_device
					if device == selected_device:
						self.feedback_handler(config, led_on)
					else: 
						self.feedback_handler(config, led_off)
				else:
					for parent_name in config_map:
						parent_config = getattr(self, parent_name)
						if parent_config["json_id"] == config["parent_json_id"]:
							parent_track = parent_config["module"]
							break
					tracks_selected_device = eval(parent_track + ".view.selected_device")
					if device == tracks_selected_device:
						self.feedback_handler(config, led_on)
					else: 
						self.feedback_handler(config, led_off)
	def _on_selected_track_changed(self):
		global active_mode, prev_active_mode, modes
		self.log("selected track changed")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
		self.track_feedback()
		self.device_feedback()
		self.refresh_state()
	def track_feedback(self, mode_id=None):
		if (mode_id == None):
			global active_mode
			mode_id = active_mode
		config_map = "mode_" + str(mode_id) + "_configs_map"
		config_map = getattr(self, config_map)
		selected_track = self.song().view.selected_track
		for config_name in config_map:
			config = getattr(self, config_name)
			if config.has_key("mapping_type") and config["mapping_type"] == "Track":
				led_on = config["LED_on"]
				led_off = config["LED_off"]
				try: 
					track = eval(config["module"])
				except:
					self.feedback_handler(config, led_off)
					return
				if track == selected_track:
					self.feedback_handler(config, led_on)
				else: 
					self.feedback_handler(config, led_off)
	def _on_selected_scene_changed(self):
		global active_mode, prev_active_mode, modes
		self.show_message("selected scene changed")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
		self.refresh_state()
	def _all_tracks_listener(self):
		global active_mode, prev_active_mode, modes
		self.show_message("mode 1 tracks listener")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
	def all_track_device_listeners(self):
		numtracks = len(self.song().tracks)
		for index in range(numtracks):
			try:
				self.song().tracks[index].view.add_selected_device_listener(self._selected_device_listener)
				self.song().tracks[index].add_devices_listener(self.listening_to_devices)
			except:
				self.log("all_track_device_listeners exception")
		num_returns = len(self.song().return_tracks)
		for index in range(num_returns):
			try:
				self.song().return_tracks[index].view.add_selected_device_listener(self._selected_device_listener)
				self.song().return_tracks[index].add_devices_listener(self.listening_to_devices)
			except:
				self.log("all_track_device_listeners exception")	
		try:
			self.song().master_track.view.add_selected_device_listener(self._selected_device_listener)
			self.song().master_track.add_devices_listener(self.listening_to_devices)
		except:
			self.log("all_track_device_listeners exception")	
	def _remove_all_track_device_listeners(self):
		numtracks = len(self.song().tracks)
		for index in range(numtracks):
			try:
				self.song().tracks[index].view.remove_selected_device_listener(self._selected_device_listener)
				self.song().tracks[index].remove_devices_listener(self.listening_to_devices)
			except:
				self.log("_remove_all_track_device_listeners exception")
		num_returns = len(self.song().return_tracks)
		for index in range(num_returns):
			try:
				self.song().return_tracks[index].view.remove_selected_device_listener(self._selected_device_listener)
				self.song().return_tracks[index].remove_devices_listener(self.listening_to_devices)
			except:
				self.log("_remove_all_track_device_listeners exception")
		try:
			self.song().master_track.view.remove_selected_device_listener(self._selected_device_listener)
			self.song().master_track.remove_devices_listener(self.listening_to_devices)
		except:
			self.log("_remove_all_track_device_listeners exception")
	################################################
	############# Extra Functions ##################
	################################################
	def scroll_through_devices(self, cnfg):
		NavDirection = Live.Application.Application.View.NavDirection
		if cnfg["ctrl_type"] == "absolute":
			if cnfg["value"] > cnfg["pre_val"]:
				if cnfg["reverse_mode"] is False: 
					goto = "right"
				elif cnfg["reverse_mode"] is True:
					goto = "left"
				times = 1;
			elif cnfg["value"] < cnfg["pre_val"]:
				if cnfg["reverse_mode"] is False: 
					goto = "left"
				elif cnfg["reverse_mode"] is True:
					goto = "right"
				times = 1;
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = "left"
				times = cnfg["steps"];
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = "right"
				times = cnfg["steps"];
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"]:
					goto = "right"
			elif cnfg["enc_second"] == cnfg["value"]:
					goto = "right"
		elif cnfg["ctrl_type"] == "increment":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = "right"
				times = cnfg["steps"];
		elif cnfg["ctrl_type"] == "decrement":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = "left"
				times = cnfg["steps"];
		if goto == "right":
			for x in range(0, times):
				self._scroll_device_chain(NavDirection.right)
		elif goto == "left":
			for x in range(0, times):
				self._scroll_device_chain(NavDirection.left)
	def _scroll_device_chain(self, direction):
		view = self.application().view
		if not view.is_view_visible('Detail') or not view.is_view_visible('Detail/DeviceChain'):
			view.show_view('Detail')
			view.show_view('Detail/DeviceChain')
		else:
			view.scroll_view(direction, 'Detail/DeviceChain', False)
	def selected_device_idx(self):
		self._device = self.song().view.selected_track.view.selected_device
		return self.tuple_index(self.song().view.selected_track.devices, self._device)
	def selected_track_idx(self):
		self._track = self.song().view.selected_track
		self._track_num = self.tuple_index(self.song().tracks, self._track)
		self._track_num = self._track_num + 1
		return self._track_num
	def selected_scene_idx(self):
		self._scene = self.song().view.selected_scene
		self._scene_num = self.tuple_index(self.song().scenes, self._scene)
		self._scene_num = self._scene_num + 1
		return self._scene_num
	def tuple_index(self, tuple, obj):
		for i in xrange(0, len(tuple)):
			if (tuple[i] == obj):
				return i
		return(False)
	def select_a_device(self, cnfg):
		parent_track = cnfg["parent_track"]
		device_chain = cnfg["device_chain"]
		chain_selector = "self.song().view.selected_track" + device_chain
		try:
			self.song().view.selected_track = eval(parent_track)
			try:
				self.song().view.select_device(eval(chain_selector))
			except IndexError:
				self.show_message("Device you are trying to select does not exist on track.") 
		except IndexError:
			self.show_message("Track does not exist for the device you are selecting.")
	def a_b_crossfade_assign(self, cnfg):
		assignment_type = cnfg['assignment_type']; 
		if(assignment_type == "Scroll"):
			goto = self.scroll_a_b_assign(cnfg);
			if goto > 2:
				goto = 2
		elif cnfg["enc_first"] == cnfg["value"]:
			if assignment_type == "Select A":
				goto = 0
			elif assignment_type == "Select None":
				goto = 1
			elif assignment_type == "Select B":
				goto = 2
			else:
				goto = 0
		setattr(eval(str(cnfg['parent_track']) + ".mixer_device"), "crossfade_assign", goto)
	def scroll_a_b_assign(self, cnfg):
		should_it_fire = self.should_it_fire(cnfg)
		if(should_it_fire != 1):
			return
		current_assigned_value = eval(str(cnfg['parent_track']) + ".mixer_device.crossfade_assign")
		length = 3
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			goto = int(cnfg["value"] / divider) 
			if cnfg["reverse_mode"] is True:
				if(goto >= 2):
					goto = 0
				elif(goto == 0):
					goto = 2
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			self.log_message("csslog: relative");
			if cnfg["enc_first"] == cnfg["value"] and current_assigned_value > 0:
				goto = current_assigned_value - 1
			elif cnfg["enc_second"] == cnfg["value"] and current_assigned_value < 2:
				goto = current_assigned_value + 1
		elif cnfg["ctrl_type"] == "on/off":	
			if current_assigned_value < 2:
				goto = current_assigned_value + 1
			elif current_assigned_value >= 2:
				goto = 0
		elif cnfg["ctrl_type"] == "increment":
			if current_assigned_value < 2:
				goto = current_assigned_value + 1
			else: 
				goto = current_assigned_value
		elif cnfg["ctrl_type"] == "decrement":
			if current_assigned_value > 0:
				goto = current_assigned_value - 1
			else: 
				goto = current_assigned_value
		return int(goto)
	def scroll_highlight(self, cnfg):
		if cnfg["tracks_scenes"] == "tracks":
			length = len(self.song().tracks) - 1
			selected = self.selected_track_idx() - 1
		elif cnfg["tracks_scenes"] == "scenes":
			length = len(self.song().scenes)
			selected = self.selected_scene_idx() - 1
		else: 
			self.log("scroll_highlight error, tracks_scenes was not set")
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			if cnfg["reverse_mode"] is False:
				goto = cnfg["value"] / divider
			elif cnfg["reverse_mode"] is True:
				goto = (divider * length) / cnfg["value"]
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = selected - cnfg["steps"]
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"]:
				goto = length
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = 0
		elif cnfg["ctrl_type"] == "increment":
			goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "decrement":
			goto = selected - cnfg["steps"]
		if goto <= length and goto >= 0 and goto != selected:
			cnfg["highlight_number"] = goto
			self.select_highlight(cnfg)
	def select_sess_offset(self, cnfg):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to select, buddy.")
			return
		tracks_scenes = cnfg["tracks_scenes"]
		track_offset = self._session.track_offset()
		scene_offset = self._session.scene_offset()
		if tracks_scenes == "tracks":
			track_offset = cnfg["highlight_number"]
		elif tracks_scenes == "scenes":
			scene_offset = cnfg["highlight_number"]
		try:
			self._session.set_offsets(track_offset, scene_offset)
			self._session._reassign_scenes()
			self.set_highlighting_session_component(self._session)
			self.refresh_state()
		except:
			self.show_message("unable to move session box there.")
	def scroll_sess_offset(self, cnfg):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to scroll, buddy.")
			return
		tracks_scenes = cnfg["tracks_scenes"]
		track_offset = self._session.track_offset()
		scene_offset = self._session.scene_offset()
		if cnfg["tracks_scenes"] == "tracks":
			length = len(self.song().tracks)
			selected = track_offset
		elif cnfg["tracks_scenes"] == "scenes":
			length = len(self.song().scenes)
			selected = scene_offset
		else: 
			self.log("scroll_sess_offset error, tracks_scenes was not set")
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			goto = cnfg["value"] / divider
			if cnfg["reverse_mode"] is True:
				goto = length - goto
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = selected - cnfg["steps"]
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"] or cnfg["enc_second"] == cnfg["value"]:
				if selected != 0 and selected != length - 1:
					goto = length - 1
				elif selected == 0:
					goto = length - 1
				else: 
					goto = 0				
		elif cnfg["ctrl_type"] == "increment":
			goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "decrement":
			goto = selected - cnfg["steps"]
		if cnfg["tracks_scenes"] == "tracks":
			track_offset = goto
		elif cnfg["tracks_scenes"] == "scenes":
			scene_offset = goto
		try:
			self._session.set_offsets(track_offset, scene_offset)
			self._session._reassign_scenes()
			self.set_highlighting_session_component(self._session)
			self.refresh_state()
		except:
			self.show_message("unable to move session box there.")
	def select_highlight(self, cnfg):
		tracks_scenes = cnfg["tracks_scenes"]
		change_to = cnfg["highlight_number"] 
		if tracks_scenes == "tracks":
			num_of_tracks_scenes = len(self.song().tracks)
		elif tracks_scenes == "scenes":
			num_of_tracks_scenes = len(self.song().scenes)
		if num_of_tracks_scenes >= change_to + 1:
			if tracks_scenes == "tracks":
				self.song().view.selected_track = self.song().tracks[change_to]
			elif tracks_scenes == "scenes":
				self.song().view.selected_scene = self.song().scenes[change_to]
		else: 
			self.show_message("Your Session doesn't have " + str(change_to + 1) + " " + tracks_scenes)
	def scroll_active_device_bank(self, cnfg):
		device_id = cnfg["parent_device_id"]
		device = "device_id_" + str(device_id);
		active_bank = getattr(self, device + "_active_bank")
		banks = getattr(self, device + "_banks")
		length = len(banks) - 1
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			if cnfg["reverse_mode"] is False:
				goto = cnfg["value"] / divider
			elif cnfg["reverse_mode"] is True:
				goto = (divider * length) / cnfg["value"]
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = active_bank - 1
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = active_bank + 1
		elif cnfg["ctrl_type"] == "on/off":
			if cnfg["switch_type"] == "toggle":	
				if cnfg["enc_first"] == cnfg["value"]:
					goto = length
				elif cnfg["enc_second"] == cnfg["value"]:
					goto = 0
			elif active_bank == length:
				goto = 0
			else:  
				goto = length
		elif cnfg["ctrl_type"] == "increment":
				goto = active_bank + 1
		elif cnfg["ctrl_type"] == "decrement":
				goto = active_bank - 1
		if goto <= length and goto >= 0 and goto != active_bank:
			cnfg["banking_number"] = goto
			self.change_active_device_bank(cnfg)
	def change_active_device_bank(self, cnfg):
		global active_mode
		device_id = cnfg["parent_device_id"]
		change_to_bank = cnfg["banking_number"]
		device = "device_id_" + str(device_id);
		bank_names = getattr(self, device + "_bank_names")
		length = len(bank_names) - 1; 
		if change_to_bank <= length:
			setattr(self, device + "_active_bank", change_to_bank)
			self.bank_led_feedback(cnfg["parent_json_id"]);
			self.show_message("changed active bank to: " + bank_names[change_to_bank])
		elif change_to_bank > length:
			self.show_message("device does not have " + str(change_to_bank + 1) + " parameter banks set")
		fire_all_mode_feedback = getattr(self, "_mode" + active_mode + "_fire_all_feedback")
		fire_all_mode_feedback()
	def session_box(self, num_tracks, num_scenes, track_offset, scene_offset, clips, stop_all, stop_tracks, scene_launch, feedbackArr, combination_mode):
		self._session = SessionComponent(num_tracks, num_scenes)
		self._session.set_offsets(track_offset, scene_offset)
		self._session.add_offset_listener(self._on_session_offset_changes, identify_sender= False)
		self._session._reassign_scenes()
		self.set_highlighting_session_component(self._session)
		if clips: 
			self._grid = ButtonMatrixElement(rows=[clips[(index*num_tracks):(index*num_tracks)+num_tracks] for index in range(num_scenes)])
			self._session.set_clip_launch_buttons(self._grid)
		if stop_all:
			self._session.set_stop_all_clips_button(stop_all)
		if stop_tracks:
			self._session.set_stop_track_clip_buttons(tuple(stop_tracks))
		if scene_launch:
			scene_launch_buttons = ButtonMatrixElement(rows=[scene_launch])
			self._session.set_scene_launch_buttons(scene_launch_buttons)
			self._session.set_stop_clip_triggered_value(feedbackArr["StopClipTriggered"])
			self._session.set_stop_clip_value(feedbackArr["StopClip"])
		for scene_index in range(num_scenes):
			scene = self._session.scene(scene_index)
			scene.set_scene_value(feedbackArr["Scene"])
			scene.set_no_scene_value(feedbackArr["NoScene"])
			scene.set_triggered_value(feedbackArr["SceneTriggered"])
			for track_index in range(num_tracks):
				clip_slot = scene.clip_slot(track_index)
				clip_slot.set_triggered_to_play_value(feedbackArr["ClipTriggeredPlay"])
				clip_slot.set_triggered_to_record_value(feedbackArr["ClipTriggeredRecord"])
				clip_slot.set_record_button_value(feedbackArr["RecordButton"])
				clip_slot.set_stopped_value(feedbackArr["ClipStopped"])
				clip_slot.set_started_value(feedbackArr["ClipStarted"])
				clip_slot.set_recording_value(feedbackArr["ClipRecording"])
			for index in range(len(stop_tracks)):
				stop_track_button = stop_tracks[index]
				if feedbackArr["StopTrackPlaying"] and feedbackArr["StopTrackStopped"]:
					stop_track_button.set_on_off_values(feedbackArr["StopTrackPlaying"], feedbackArr["StopTrackStopped"])
			if stop_all:
				if feedbackArr["StopAllOn"] and feedbackArr["StopAllOff"]:
					stop_all.set_on_off_values(feedbackArr["StopAllOn"], feedbackArr["StopAllOff"])
		if combination_mode == "on":
			self._session._link()
		self.refresh_state()
	def _on_session_offset_changes(self):
		global active_mode
		try:
			remove_mode = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
			remove_mode()
			activate_mode = getattr(self, "_mode" + active_mode + "_led_listeners")
			activate_mode()
		except:
			self.log("_on_session_offset_changes: could not remove / add led_listeners")
			return;
	def remove_session_box(self, combination_mode): 
		if hasattr(self, "_session"):
			self.current_track_offset = self._session._track_offset
			self.current_scene_offset = self._session._scene_offset
			self._session.set_clip_launch_buttons(None)
			self.set_highlighting_session_component(None)
			self._session.set_stop_all_clips_button(None)
			self._session.set_stop_track_clip_buttons(None)
			self._session.set_scene_launch_buttons(None)
			if combination_mode == "on":
				self._session._unlink()
			self._session = None
	def scroll_modes(self, cnfg):
		controller = getattr(self, cnfg["attached_to"])
		cnfg["value"] = controller.cur_val 
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / (len(self.modes) - 1)
			if cnfg["reverse_mode"] is False:
				goto = cnfg["value"] / divider
			elif cnfg["reverse_mode"] is True:
				length = len(self.modes) - 1
				goto = (divider * length) / cnfg["value"]
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = self.key_num - 1
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = self.key_num + 1
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"]:
				goto = len(self.modes) - 1
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = 0
		elif cnfg["ctrl_type"] == "increment":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = self.key_num + 1
		elif cnfg["ctrl_type"] == "decrement":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = self.key_num - 1
		if goto <= len(self.modes) and goto >= 0 and active_mode != self.modes[goto]:
			self.set_active_mode(self.modes[goto])
	def listening_to_tracks(self):
		global active_mode
		self.remove_listening_to_tracks()
		for index in range(len(self.song().tracks)):
			_track = self.song().tracks[index]
			if _track.can_be_armed and hasattr(self, "_mode" + active_mode + "_arm_listener"):
				_track.add_arm_listener(getattr(self, "_mode" + active_mode + "_arm_listener"))
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				_track.add_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				_track.add_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				_track.mixer_device.volume.add_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				_track.mixer_device.panning.add_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_track.mixer_device.sends)):
					_track.mixer_device.sends[send_index].add_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		for index in range(len(self.song().return_tracks)):
			_return_track = self.song().return_tracks[index]
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				_return_track.add_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				_return_track.add_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				_return_track.mixer_device.volume.add_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				_return_track.mixer_device.panning.add_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_return_track.mixer_device.sends)):
					_return_track.mixer_device.sends[send_index].add_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		_master = self.song().master_track
		if hasattr(self, "_mode" + active_mode + "_volume_listener"):
			_master.mixer_device.volume.add_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
		if hasattr(self, "_mode" + active_mode + "_panning_listener"):
			_master.mixer_device.panning.add_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
	def remove_listening_to_tracks(self):
		global active_mode
		for index in range(len(self.song().tracks)):
			_track = self.song().tracks[index]
			if hasattr(self, "_mode" + active_mode + "_arm_listener"):
				if _track.arm_has_listener(getattr(self, "_mode" + active_mode + "_arm_listener")):
					_track.remove_arm_listener(getattr(self, "_mode" + active_mode + "_arm_listener"))
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				if _track.mute_has_listener(getattr(self, "_mode" + active_mode + "_mute_listener")):
					_track.remove_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				if _track.solo_has_listener(getattr(self, "_mode" + active_mode + "_solo_listener")):
					_track.remove_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				if _track.mixer_device.volume.value_has_listener(getattr(self, "_mode" + active_mode + "_volume_listener")):
					_track.mixer_device.volume.remove_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				if _track.mixer_device.panning.value_has_listener(getattr(self, "_mode" + active_mode + "_panning_listener")):
					_track.mixer_device.panning.remove_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_track.mixer_device.sends)):
					if _track.mixer_device.sends[send_index].value_has_listener(getattr(self, "_mode" + active_mode + "_send_listener")):
						_track.mixer_device.sends[send_index].remove_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		for index in range(len(self.song().return_tracks)):
			_return_track = self.song().return_tracks[index]
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				if _return_track.mute_has_listener(getattr(self, "_mode" + active_mode + "_mute_listener")):
					_return_track.remove_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				if _return_track.solo_has_listener(getattr(self, "_mode" + active_mode + "_solo_listener")):
					_return_track.remove_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				if _return_track.mixer_device.volume.value_has_listener(getattr(self, "_mode" + active_mode + "_volume_listener")):
					_return_track.mixer_device.volume.remove_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				if _return_track.mixer_device.panning.value_has_listener(getattr(self, "_mode" + active_mode + "_panning_listener")):
					_return_track.mixer_device.panning.remove_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_return_track.mixer_device.sends)):
					if _return_track.mixer_device.sends[send_index].value_has_listener(getattr(self, "_mode" + active_mode + "_send_listener")):
						_return_track.mixer_device.sends[send_index].remove_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		_master = self.song().master_track
		if hasattr(self, "_mode" + active_mode + "_volume_listener"):
			if _master.mixer_device.volume.value_has_listener(getattr(self, "_mode" + active_mode + "_volume_listener")):
				_master.mixer_device.volume.remove_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
		if hasattr(self, "_mode" + active_mode + "_panning_listener"):
			if _master.mixer_device.panning.value_has_listener(getattr(self, "_mode" + active_mode + "_panning_listener")):
				_master.mixer_device.panning.remove_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
	def set_active_mode(self, activate_new_mode):
		global active_mode, prev_active_mode, modes
	
		for number, mode_id in self.modes.items():
			if mode_id == activate_new_mode:
				self.key_num = mode_id
		if(activate_new_mode == "Previous Mode"):
			if 'prev_active_mode' not in globals():
				self.show_message("No previous mode is set yet.")
			else:
				remove_mode = getattr(self, "_remove_mode" + active_mode)
				remove_mode()
				activate_new_mode = prev_active_mode
				prev_active_mode = active_mode
				active_mode = activate_new_mode
				mode_to_call = getattr(self, "_mode" + activate_new_mode)
				mode_to_call()
		else:
			if 'active_mode' in globals():
				remove_mode = getattr(self, "_remove_mode" + active_mode)
				remove_mode()
				prev_active_mode = active_mode
			active_mode = activate_new_mode 
			mode_to_call = getattr(self, "_mode" + activate_new_mode)
			mode_to_call()
	def disconnect(self):
		super(css_benctrl, self).disconnect()
