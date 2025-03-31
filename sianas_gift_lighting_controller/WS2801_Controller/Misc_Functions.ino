#define TEN_MIN_MILLIS 600000

void on_encoder_button_pressed() {
  if (!encoder_button_pressed) {
    encoder_button_pressed = true;
  }
}

void on_off_button_changed() {
  static unsigned long start_time = millis();
  static bool button_down = false;
  //((long)(millis() - timer_end_time) >= 0)
  if (!button_down) {
    if (!digitalRead(ON_OFF_BUTTON_PIN)) {
      start_time = millis();
      button_down = true;
      delay(button_debounce);
    }

  } else {
    if ((millis() - start_time) < timer_threshold) {
      if (!on_off_button_pressed) {
        on_off_button_pressed = true;
      }
    } else {
      if (leds_on) {
        if (!on_off_timer_pressed) {
          on_off_timer_pressed = true;
        }
      }
    }
    button_down = false;
  }
}

void check_on_off() {
  if (on_off_button_pressed) {
    leds_on = !leds_on;
    delay(button_debounce);
    on_off_button_pressed = false;
  }
}

void check_brightness_change() {
  long encoder_position = myEnc.read();
  if (encoder_position != encoder_position_previous) {
    led_brightness += (encoder_position - encoder_position_previous);
    led_brightness = constrain(led_brightness, 2, 255);
    encoder_position_previous = encoder_position;
    FastLED.setBrightness(led_brightness);
    if (use_serial) {
      Serial.print("Brightness Changed To: ");
      Serial.println(led_brightness);
    }
  }
}

void freeze_encoder() {
  encoder_position_previous = myEnc.read();
}

void check_mode_change() {
  if (encoder_button_pressed) {
    nextPattern();
    delay(button_debounce);
    encoder_button_pressed = false;
  }
}

void check_timer() {
  if (on_off_timer_pressed) {

    delay(button_debounce);

    int temp = 4;
    long ten_min_intervals = 1;
    bool edit_timer = true;

    while ((!on_off_button_pressed) && edit_timer) {
      long encoder_position = myEnc.read();
      if (encoder_position != encoder_position_previous) {
        temp += (encoder_position - encoder_position_previous);
        temp = constrain(temp, 4, 255);
        ten_min_intervals = map(temp, 4, 255, 1, 50);
        encoder_position_previous = encoder_position;
      }

      all_black();
      for (int i = 0 ; i < ten_min_intervals ; i++) {
        leds[i] = CRGB::Blue;
      }
      FastLED.show();

      if (encoder_button_pressed) {
        run_timer = false;
        on_off_button_pressed = false;
        encoder_button_pressed = false;
        edit_timer = false;
      }
    }

    if (on_off_button_pressed) {
      timer_end_time = millis() + (TEN_MIN_MILLIS * ten_min_intervals);

      if (use_serial) {
        Serial.print("Timer End Time: ");
        Serial.println(timer_end_time);
      }
      run_timer = true;
      on_off_button_pressed = false;
    }

    on_off_timer_pressed = false;
  }
}

void check_timer_elapsed() {
  if (run_timer) {
    if ((long)(millis() - timer_end_time) >= 0) {
      leds_on = false;
      run_timer = false;
    }
  }
}

