#include <Control_Surface.h>

//#include <name.c>
// celà doit etre écrit avant la library control surface
 //USBDebugMIDI_Interface midi = 115200; // enlever les // en début de ligne pour entrer en mode debug usb et voir dans le panneau de control si vos controler envoient bien les infos

//auto &serial = Serial1;// Selectionne le port série à utiliser remplacer par serial pour une arduino
//SerialMIDI_Interface<decltype(serial)> midi = {serial, MIDI_BAUD};// démarre une interface midi serial au midi baud rate par defaut
USBMIDI_Interface usbmidi;// enlever les / en debut de ligne pour activer l'interface usb, penser à désactiver l'interface série(din)
HardwareSerialMIDI_Interface midiser = Serial1;
 
 
MIDI_PipeFactory<8> pipes;


CD74HC4067 mux1 = {
  14,       // numéro de broche de l'arduino
  {9, 3, 4, 5} // numéro de pins de l'arduino sur lesquels sont branchés tous les multiplexeurs apellés mux S0, S1, S2
};

CD74HC4067 mux2 = {
  15,              
  {9, 3, 4, 5}, 
};

CD74HC4067 mux3 = {
  16,       
  {9, 3, 4, 5} 
};
CD74HC4067 mux4 = {
  17,       
  {9, 3, 4, 5} 
};
CD74HC4067 mux5 = {
  18,      
  {9, 3, 4, 5} 
};

Bank<2> bank = {16}; // active 2 bank avec 8 adresses par bank
IncrementDecrementSelector<2> selector = {
    bank,       // Bank to manage
    {19, 20},     // push button pins (increment, decrement)
    Wrap::Wrap, // Wrap around
};
CCPotentiometer fxparameter [] = {
  {mux1.pin(0), {85, CHANNEL_16}},//delay time
  {mux1.pin(1), {86, CHANNEL_16}},//pingpong
  {mux1.pin(2), {87, CHANNEL_16}},//stereo width
  {mux1.pin(3), {88, CHANNEL_16}},//feedback
  {mux1.pin(4), {89, CHANNEL_16}},//hph
  {mux1.pin(5), {90, CHANNEL_16}},//lpf
  {mux1.pin(6), {91, CHANNEL_16}},//reverb send
  {mux1.pin(7), {92, CHANNEL_16}},//mix volume
  {mux1.pin(15), {24, CHANNEL_16}},//pre delay
  {mux1.pin(14), {25, CHANNEL_16}},//reverb decay
  {mux1.pin(13), {26, CHANNEL_16}},//reverb filter
  {mux1.pin(12), {27, CHANNEL_16}},//shelving gain
  {mux1.pin(11), {28, CHANNEL_16}},//hpf
  {mux1.pin(10), {29, CHANNEL_16}},//lpf
  {mux1.pin(9), {31, CHANNEL_16}},//mux volume
  {mux1.pin(8), {119, CHANNEL_16}},//pattern volume
};

Bankable::CCPotentiometer ODPAN [] = {
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(0), {81, CHANNEL_1}},//overdrive
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(1), {81, CHANNEL_2}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(2), {81, CHANNEL_3}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(3), {81, CHANNEL_4}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(4), {81, CHANNEL_5}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(5), {81, CHANNEL_6}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(6), {81, CHANNEL_7}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(7), {81, CHANNEL_8}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(15), {10, CHANNEL_1}},//pan
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(14), {10, CHANNEL_2}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(13), {10, CHANNEL_3}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(12), {10, CHANNEL_4}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(11), {10, CHANNEL_5}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(10), {10, CHANNEL_6}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(9), {10, CHANNEL_7}},
  {{bank, BankType::CHANGE_CHANNEL},mux2.pin(8), {10, CHANNEL_8}},
};
Bankable::CCPotentiometer fx [] = {
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(0), {83, CHANNEL_1}},//reverb send
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(1), {83, CHANNEL_2}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(2), {83, CHANNEL_3}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(3), {83, CHANNEL_4}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(4), {83, CHANNEL_5}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(5), {83, CHANNEL_6}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(6), {83, CHANNEL_7}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(7), {83, CHANNEL_8}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(15), {82, CHANNEL_1}},//delay send
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(14), {82, CHANNEL_2}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(13), {82, CHANNEL_3}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(12), {82, CHANNEL_4}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(11), {82, CHANNEL_5}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(10), {82, CHANNEL_6}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(9), {82, CHANNEL_7}},
  {{bank, BankType::CHANGE_CHANNEL},mux4.pin(8), {82, CHANNEL_8}},
};

Bankable::CCPotentiometer filtre [] = {
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(0), {74, CHANNEL_1}},//filtre freq
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(1), {74, CHANNEL_2}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(2), {74, CHANNEL_3}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(3), {74, CHANNEL_4}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(4), {74, CHANNEL_5}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(5), {74, CHANNEL_6}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(6), {74, CHANNEL_7}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(7), {74, CHANNEL_8}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(15), {75, CHANNEL_1}},//filtre reso
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(14), {75, CHANNEL_2}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(13), {75, CHANNEL_3}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(12), {75, CHANNEL_4}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(11), {75, CHANNEL_5}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(10), {75, CHANNEL_6}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(9), {75, CHANNEL_7}},
  {{bank, BankType::CHANGE_CHANNEL},mux3.pin(8), {75, CHANNEL_8}},
};

Bankable::CCPotentiometer fader [] = { //ici on déclare les faders avec comme vu plus haut le numéro de CC et le canal
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(15), {7, CHANNEL_1}},//volume
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(14), {7, CHANNEL_2}},
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(13), {7, CHANNEL_3}},
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(12), {7, CHANNEL_4}},
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(11), {7, CHANNEL_5}},
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(10), {7, CHANNEL_6}},
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(9), {7, CHANNEL_7}},
  {{bank, BankType::CHANGE_CHANNEL},mux5.pin(8), {7, CHANNEL_8}},
};
 Bankable::CCButtonLatched<2> buttonmute[] = { 
  {{bank,BankType::CHANGE_CHANNEL}, mux5.pin(0), {94, CHANNEL_8}},//numéro de bank correspondant/indique que le changement de bank change le canal midi (+8 car on a 8 adresses par bank)/pin sur laquelle le controleur est branché/numéro de cc/numéro de canal midi
  {{bank,BankType::CHANGE_CHANNEL},mux5.pin(1), {94, CHANNEL_7}},
  {{bank,BankType::CHANGE_CHANNEL},mux5.pin(2), {94, CHANNEL_6}},
  {{bank,BankType::CHANGE_CHANNEL},mux5.pin(3), {94, CHANNEL_5}},
  {{bank,BankType::CHANGE_CHANNEL},mux5.pin(4), {94, CHANNEL_4}},
  {{bank,BankType::CHANGE_CHANNEL},mux5.pin(5), {94, CHANNEL_3}},
  {{bank,BankType::CHANGE_CHANNEL},mux5.pin(6), {94, CHANNEL_2}},
  {{bank,BankType::CHANGE_CHANNEL},mux5.pin(7), {94, CHANNEL_1}},
};
  
void setup() {
  Control_Surface.begin(); // initialise la library surface de control
  usbmidi >> pipes >> midiser; // all incoming midi from USB is sent to serial
  usbmidi << pipes << midiser; // all incoming midi from Serial is sent to USB
  usbmidi >> pipes >> usbmidi; // all incoming midi from USB is looped back
  midiser << pipes << midiser;
  Control_Surface >> pipes >> usbmidi;
  Control_Surface << pipes << usbmidi;
  Control_Surface >> pipes >> midiser;
  Control_Surface << pipes << midiser;
  usbmidi.begin();
  midiser.begin();
}                           
void loop() {
  

  Control_Surface.loop(); // Update the Control Surface
  usbmidi.update();
  midiser.update();
}
