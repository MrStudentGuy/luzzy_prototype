/* PixMobIRForwarder,

   Version 1.0, August 2022
   Daniel Weidman, danielweidman.com

   Based on Ken Shirriff's IrsendDemo
   Copyright 2009 Ken Shirriff, http://arcfn.com

   This script takes IR codes for PixMob bracelets from a connected computer over Serial or
   other device over Bluetooth and transmits those codes to PixMob bracelets.

    ------------------------------------------------------------------------------
   An IR LED circuit *MUST* be connected to the Arduino on a pin
   as specified by kIrLed below.

   TL;DR: The IR LED needs to be driven by a transistor for a good result.

   Suggested circuit:
       https://github.com/crankyoldgit/IRremoteESP8266/wiki#ir-sending

   Common mistakes & tips:
 *   * Don't just connect the IR LED directly to the pin, it won't
       have enough current to drive the IR LED effectively.
 *   * Make sure you have the IR LED polarity correct.
       See: https://learn.sparkfun.com/tutorials/polarity/diode-and-led-polarity
 *   * Typical digital camera/phones can be used to see if the IR LED is flashed.
       Replace the IR LED with a normal LED if you don't have a digital camera
       when debugging.
 *   * Avoid using the following pins unless you really know what you are doing:
 *     * Pin 0/D3: Can interfere with the boot/program mode & support circuits.
 *     * Pin 1/TX/TXD0: Any serial transmissions from the ESP8266 will interfere.
 *     * Pin 3/RX/RXD0: Any serial transmissions to the ESP8266 will interfere.
*/

#include <Arduino.h>
#include <IRremote.hpp>

// SET THIS TO THE DATA PIN USED FOR THE IR TRANSMITTER
const uint16_t kIrLed = 3;

String incomingString = "";
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  //Serial.setTimeout(0.5);
  IrSender.begin(kIrLed);
  IrSender.enableIROut(38);
}

void loop() {
  while (!Serial.available());
  incomingString = Serial.readStringUntil('['); // read the incoming byte:
  incomingString = Serial.readStringUntil(']'); // read the incoming byte:

  int newLength = incomingString.toInt();
  uint16_t newRawData[newLength] = {};
  String newVals = Serial.readStringUntil(',');
  for (int i = 0; i < newVals.length(); i++ ) {
    int intVal = newVals.substring(i, i + 1).toInt() * 700;
    newRawData[i] = intVal;
  }
  IrSender.sendRaw(newRawData, newLength, 38);  // Send a raw data capture at 38kHz.
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(3);
  digitalWrite(LED_BUILTIN, LOW);
}
