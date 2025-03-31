void rainbow_cyclical() {
  FRAMES_PER_SECOND = 120;
  EVERY_N_MILLISECONDS( 20 ) {
    gHue++;
  }
  fill_rainbow( leds, NUM_LEDS, gHue, 7);
}

void rainbow_full() {
  FRAMES_PER_SECOND = 30;
  EVERY_N_MILLISECONDS( 20 ) {
    gHue++;
  }

  for (int i = 0 ; i < NUM_LEDS ; i++) {
    leds[i] = CHSV(gHue, 255, 255);
  }
}

void rainbow_cyclical_WithGlitter()
{
  // built-in FastLED rainbow, plus some random sparkly glitter
  rainbow_cyclical();
  addGlitter(25);
}

void addGlitter( fract8 chanceOfGlitter)
{
  if ( random8() < chanceOfGlitter) {
    leds[ random16(NUM_LEDS) ] += CRGB::White;
  }
}

void confetti()
{
  FRAMES_PER_SECOND = 60;
  EVERY_N_MILLISECONDS( 20 ) {
    gHue++;
  }
  // random colored speckles that blink in and fade smoothly
  fadeToBlackBy( leds, NUM_LEDS, 10);
  int pos = random16(NUM_LEDS);
  leds[pos] += CHSV( gHue + random8(64), 200, 255);
}

void sinelon()
{
  FRAMES_PER_SECOND = 120;
  EVERY_N_MILLISECONDS( 20 ) {
    gHue++;
  }
  // a colored dot sweeping back and forth, with fading trails
  fadeToBlackBy( leds, NUM_LEDS, 20);
  int pos = beatsin16(13, 0, NUM_LEDS);
  leds[pos] += CHSV( gHue, 255, 192);
}

void nextPattern() {
  // add one to the current pattern number, and wrap around at the end
  gCurrentPatternNumber = (gCurrentPatternNumber + 1) % ARRAY_SIZE( gPatterns);
  all_black();
}

void bpm()
{
  FRAMES_PER_SECOND = 120;
  EVERY_N_MILLISECONDS( 20 ) {
    gHue++;
  }
  // colored stripes pulsing at a defined Beats-Per-Minute (BPM)
  uint8_t BeatsPerMinute = 62;
  CRGBPalette16 palette = PartyColors_p;
  uint8_t beat = beatsin8( BeatsPerMinute, 64, 255);
  for ( int i = 0; i < NUM_LEDS; i++) { //9948
    leds[i] = ColorFromPalette(palette, gHue + (i * 2), beat - gHue + (i * 10));
  }
}

void juggle() {
  FRAMES_PER_SECOND = 120;
  EVERY_N_MILLISECONDS( 20 ) {
    gHue++;
  }
  // eight colored dots, weaving in and out of sync with each other
  fadeToBlackBy( leds, NUM_LEDS, 20);
  byte dothue = 0;
  for ( int i = 0; i < 8; i++) {
    leds[beatsin16(i + 7, 0, NUM_LEDS)] |= CHSV(dothue, 200, 255);
    dothue += 32;
  }
}

void northern_lights_cyclical() {
  static char nlight_dir = 1;
  const unsigned int nlight_max = 200;
  const unsigned int nlight_min = 95;
  FRAMES_PER_SECOND = 40;

  if (gHue > nlight_min) {
    for (int i = 0 ; i < NUM_LEDS ; i++) {
      leds[i] = CHSV(constrain(gHue + i, nlight_min, nlight_max), 255, 255);
    }

    if (gHue > nlight_max) {
      nlight_dir = 0;
    }
  } else {
    for (int i = 0 ; i < NUM_LEDS ; i++) {
      leds[i] = CHSV(constrain(gHue + i, nlight_min, nlight_max), 255, 255);
    }
    if ((gHue + NUM_LEDS) < nlight_min) {
      nlight_dir = 1;
    }
  }




  if (nlight_dir) {
    gHue++;
  } else {
    gHue--;
  }

  if (use_serial) {
    Serial.print("\tHue: ");
    Serial.println(gHue);
  }

}

void northern_lights_random() {
  const unsigned int nlight_max = 200;
  const unsigned int nlight_min = 95;
  FRAMES_PER_SECOND = 240;

  int pos = random16(NUM_LEDS);
  leds[pos] = CHSV( nlight_min + random8(nlight_max - nlight_min), 255, 255);

}


void northern_lights() {
  static char nlight_dir = 1;
  const unsigned int nlight_max = 200;
  const unsigned int nlight_min = 95;
  FRAMES_PER_SECOND = 8;

  if (gHue > nlight_max) {
    gHue = nlight_max;
    nlight_dir = 0;
  } else if (gHue < nlight_min) {
    gHue = nlight_min;
    nlight_dir = 1;
  }

  for (int i = 0 ; i < NUM_LEDS ; i++) {
    leds[i] = CHSV(gHue, 255, 255);
  }

  if (nlight_dir) {
    gHue++;
  } else {
    gHue--;
  }

  if (use_serial) {
    Serial.print("Hue is: ");
    Serial.println(gHue);
  }
}

void northern_lights_flowy() {
  const unsigned char min_hue = 95;
  const unsigned char max_hue = 200;
  const unsigned char color_points[] = {min_hue, 147, max_hue};
  const unsigned char step_size = 2;
  static float percent = 0.0;
  static char current_point = 0;
  static unsigned char current_led = 0;
  FRAMES_PER_SECOND = 120;
  //fill_gradient(leds, NUM_LEDS, CHSV(min_hue, 255, 255), CHSV(max_hue, 255, 255));

  if (gHue > max_hue) {
    gHue = min_hue;
  } else if (gHue < min_hue) {
    gHue = min_hue;
  }

  if (current_led > NUM_LEDS) {
    current_led = 0;
  }

  leds[current_led] = CHSV(gHue, 255, 255);

  current_led++;
  gHue += step_size;
  //  for (int i = 0 ; i < NUM_LEDS ; i++) {
  //    if ((percent + step_size) > 1.0) {
  //      percent = 0;
  //      current_point++;
  //      if (current_point > ARRAY_SIZE(color_points)) {
  //        current_point = 0;
  //      }
  //    }
  //
  //    percent = (percent + step_size);
  //    leds[i] = blend(CHSV(color_points[current_point % ARRAY_SIZE(color_points)], 255, 255), CHSV(color_points[(current_point + 1) % ARRAY_SIZE(color_points)], 255, 255), percent);
  //    if (use_serial) {
  //      Serial.print("Color one: ");
  //      Serial.print(color_points[current_point % ARRAY_SIZE(color_points)]);
  //      Serial.print("\tColor two: ");
  //      Serial.print(color_points[(current_point + 1) % ARRAY_SIZE(color_points)]);
  //      Serial.print("\tPercent of two: ");
  //      Serial.println(percent);
  //    }
  //  }
}

void christmas_no_yellow() {
  const char christmas_colors[] = {0, 96, 160};  //Red 0, Green 85, Blue 170, Yellow 43, Orange 21
  FRAMES_PER_SECOND = 30;
  //fadeToBlackBy( leds, NUM_LEDS, 10);
  int pos = random16(NUM_LEDS);
  leds[pos] = CHSV( christmas_colors[random8(ARRAY_SIZE(christmas_colors))], 255, 255);
}

void christmas_with_yellow() {
  const char christmas_colors[] = {0, 96, 160, 64};  //Red 0, Green 85, Blue 170, Yellow 43, Orange 21
  FRAMES_PER_SECOND = 30;
  //fadeToBlackBy( leds, NUM_LEDS, 10);
  int pos = random16(NUM_LEDS);
  leds[pos] = CHSV( christmas_colors[random8(ARRAY_SIZE(christmas_colors))], 255, 255);
}

void lightning() {
  static uint8_t frequency = 50;                                       // controls the interval between strikes
  static uint8_t flashes = 8;                                          //the upper limit of flashes per strike
  static unsigned int dimmer = 1;

  static uint8_t ledstart;                                             // Starting location of a flash
  static uint8_t ledlen;
  FRAMES_PER_SECOND = 120;

  ledstart = random8(NUM_LEDS);           // Determine starting location of flash
  ledlen = random8(NUM_LEDS - ledstart);  // Determine length of flash (not to go beyond NUM_LEDS-1)
  for (int flashCounter = 0; flashCounter < random8(3, flashes); flashCounter++) {
    if (flashCounter == 0) dimmer = 5;    // the brightness of the leader is scaled down by a factor of 5
    else dimmer = random8(1, 3);          // return strokes are brighter than the leader
    fill_solid(leds + ledstart, ledlen, CHSV(255, 0, 255 / dimmer));
    FastLED.show();                       // Show a section of LED's
    delay(random8(4, 10));                // each flash only lasts 4-10 milliseconds
    fill_solid(leds + ledstart, ledlen, CHSV(255, 0, 0)); // Clear the section of LED's
    FastLED.show();
    if (flashCounter == 0) delay (150);   // longer delay until next flash after the leader
    delay(50 + random8(100));             // shorter delay between strokes
  } // for()
  delay(random8(frequency) * 100);        // delay between strikes
}

void all_black() {
  for (int i = 0 ; i < NUM_LEDS ; i++) {
    leds[i] = CRGB::Black;
  }
}
