//This example implements a simple sliding On/Off button. The example
// demonstrates drawing and touch operations.
//
//Thanks to Adafruit forums member Asteroid for the original sketch!
//
#include <SPI.h>
#include <Wire.h>
#include <ILI9341_t3.h>
#include <XPT2046_Touchscreen.h>

// This is calibration data for the raw touch data to the screen coordinates
#define TS_MINX 150
#define TS_MINY 130
#define TS_MAXX 3800
#define TS_MAXY 4000

#define TIRQ_PIN  2
#define CS_PIN  8
XPT2046_Touchscreen ts(CS_PIN, TIRQ_PIN);
#define TFT_CS 10
#define TFT_DC  9
ILI9341_t3 tft = ILI9341_t3(TFT_CS, TFT_DC);  //240x320

boolean RecordOn = false;

#define FRAME_X 210
#define FRAME_Y 180
#define FRAME_W 100
#define FRAME_H 50

#define REDBUTTON_X FRAME_X
#define REDBUTTON_Y FRAME_Y
#define REDBUTTON_W (FRAME_W/2)
#define REDBUTTON_H FRAME_H

#define GREENBUTTON_X (REDBUTTON_X + REDBUTTON_W)
#define GREENBUTTON_Y FRAME_Y
#define GREENBUTTON_W (FRAME_W/2)
#define GREENBUTTON_H FRAME_H

void draw_bar_graph_frames()
{
  for (uint8_t i = 3 ; i < 7 ; i++) {
    uint16_t center = (tft.width() / 7.0) * i;
    tft.drawRect(center - 20, 10, 40, 220, ILI9341_WHITE);

  }
}

void draw_bar_graph_data(uint8_t bar_index, uint8_t input)
{
  uint16_t center = (tft.width() / 7.0) * (bar_index + 2);
  uint16_t bar_height = 216 * (input / 100.0);
  tft.fillRect(center - 18, 12, 36, 216, ILI9341_BLACK);
  tft.fillRect(center - 18, min(max(bar_height-2, 12), 216), 36, 4, ILI9341_RED);
}

void drawFrame()
{
  tft.drawRect(FRAME_X, FRAME_Y, FRAME_W, FRAME_H, ILI9341_BLACK);
}

void redBtn()
{
  tft.fillRect(REDBUTTON_X, REDBUTTON_Y, REDBUTTON_W, REDBUTTON_H, ILI9341_RED);
  tft.fillRect(GREENBUTTON_X, GREENBUTTON_Y, GREENBUTTON_W, GREENBUTTON_H, ILI9341_BLUE);
  drawFrame();
  tft.setCursor(GREENBUTTON_X + 6 , GREENBUTTON_Y + (GREENBUTTON_H / 2));
  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(2);
  tft.println("ON");
  RecordOn = false;
}

void greenBtn()
{
  tft.fillRect(GREENBUTTON_X, GREENBUTTON_Y, GREENBUTTON_W, GREENBUTTON_H, ILI9341_GREEN);
  tft.fillRect(REDBUTTON_X, REDBUTTON_Y, REDBUTTON_W, REDBUTTON_H, ILI9341_BLUE);
  drawFrame();
  tft.setCursor(REDBUTTON_X + 6 , REDBUTTON_Y + (REDBUTTON_H / 2));
  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(2);
  tft.println("OFF");
  RecordOn = true;
}

void setup(void)
{
  Serial.begin(9600);
  tft.begin();
  ts.begin();

  tft.fillScreen(ILI9341_BLACK);
  // origin = left,top landscape (USB left upper)
  ts.setRotation(2);
  tft.setRotation(3);

  draw_bar_graph_frames();
}

uint16_t wait = 66;

void loop()
{
//  for (uint8_t i = 0 ; i < 100 ; i ++) {
    for (uint8_t bar = 1 ; bar < 5 ; bar++) {
      draw_bar_graph_data(bar, min(max(random(-25, 25), 0), 100) + 50);
    }
    delay(wait);
//  }
//  for (uint8_t i = 100 ; i > 0 ; i--) {
//    for (uint8_t bar = 1 ; bar < 5 ; bar++) {
//      draw_bar_graph_data(bar, min(max(random(-25, 25), 0), 100) + i);
//    }
//    delay(wait);
//  }

  // See if there's any  touch data for us
  //  if (!ts.bufferEmpty())
  //  {
  //    // Retrieve a point
  //    TS_Point p = ts.getPoint();
  //    // Scale using the calibration #'s
  //    // and rotate coordinate system
  //    p.x = map(p.x, TS_MINY, TS_MAXY, 0, tft.height());
  //    p.y = map(p.y, TS_MINX, TS_MAXX, 0, tft.width());
  //    int y = tft.height() - p.x;
  //    int x = p.y;
  //
  //    if (RecordOn)
  //    {
  //      if((x > REDBUTTON_X) && (x < (REDBUTTON_X + REDBUTTON_W))) {
  //        if ((y > REDBUTTON_Y) && (y <= (REDBUTTON_Y + REDBUTTON_H))) {
  //          Serial.println("Red btn hit");
  //          redBtn();
  //        }
  //      }
  //    }
  //    else //Record is off (RecordOn == false)
  //    {
  //      if((x > GREENBUTTON_X) && (x < (GREENBUTTON_X + GREENBUTTON_W))) {
  //        if ((y > GREENBUTTON_Y) && (y <= (GREENBUTTON_Y + GREENBUTTON_H))) {
  //          Serial.println("Green btn hit");
  //          greenBtn();
  //        }
  //      }
  //    }
  //
  //    Serial.println(RecordOn);
  //  }
}
