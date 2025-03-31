void attempt_serial_init() {
  Serial.begin(9600);

  long start_time = millis();
  bool trying_serial = true;

  while (trying_serial) {
    if (Serial) {
      Serial.println("[Serial Debugging Enabled]");
      Serial.println();
      delay(1000);
      use_serial = true;
      trying_serial = false;
    } else {
      if ((millis() - start_time) > serial_timeout) {
        Serial.end();
        use_serial = false;
        trying_serial = false;
      }
    }
  }
}

void init_buttons() {
  pinMode(ENCODER_BUTTON_PIN, INPUT_PULLUP);
  pinMode(ON_OFF_BUTTON_PIN, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER_BUTTON_PIN), on_encoder_button_pressed, FALLING);
  attachInterrupt(digitalPinToInterrupt(ON_OFF_BUTTON_PIN), on_off_button_changed, CHANGE);
  if (use_serial) {
    Serial.println("Button Initialization Complete");
  }
}

void init_lights() {
  FastLED.addLeds<WS2801, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(led_brightness);
  if (use_serial) {
    Serial.println("LED Initialization Complete");
  }
}

