#include "usb_names.h"

#define MIDI_NAME   {'B','E','N',' ','A','N','D',' ','E','D'}
#define MIDI_NAME_LEN  10

#define MANUFACTURER_NAME  {'B','E','N','S','F','E','O'}
#define MANUFACTURER_NAME_LEN 7

struct usb_string_descriptor_struct usb_string_product_name = {
  2 + MIDI_NAME_LEN * 2,
  3,
  MIDI_NAME
};

struct usb_string_descriptor_struct usb_string_manufacturer_name = {
  2 + MANUFACTURER_NAME_LEN * 2,
  3,
  MANUFACTURER_NAME
};
