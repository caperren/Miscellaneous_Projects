const int touch_pin = 15;
const int led_pin = 13;

const float num_starting_senses = 100;
const float threshold_multiplier = 1.5;

int touch_threshold = 0;

bool touch_activated = false;
bool movement_enabled = false;

const int mouse_move_delay = 1;

const int movement_max = 300;

int current_x = 0;
int current_y = 0;

int desired_x = movement_max;
int desired_y = 0;

const int millis_before_reactivation = 500;
unsigned long millis_allowed_time = millis_before_reactivation;


void setup() {
  Serial.begin(9600);

  pinMode(touch_pin, INPUT);
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, LOW);

  int sum = 0;

  for (int i = 0 ; i < num_starting_senses ; i++) {
    sum += touchRead(touch_pin);
  }

  float untouched_baseline = (sum / num_starting_senses);
  touch_threshold = int(untouched_baseline * threshold_multiplier);

  Serial.print("Baseline: ");
  Serial.print(int(untouched_baseline));
  Serial.print("\tThreshold: ");
  Serial.println(touch_threshold);

}

void loop() {
  // Movement enable/disable
  if (long(millis() - millis_allowed_time) >= 0) {
    int touch_val = touchRead(touch_pin);
    Serial.print("Current Value: ");
    Serial.println(touch_val);
    
    if ((touch_val > touch_threshold) and !touch_activated) {
      touch_activated = true;
      movement_enabled = !movement_enabled;
      digitalWrite(led_pin, movement_enabled);
    } else if ((touch_val < touch_threshold) and touch_activated) {
      touch_activated = false;
    }
    
    millis_allowed_time = millis() + millis_before_reactivation;
  }


  // Move mouse if needed and enabled
  if (movement_enabled) {
    if (current_x != desired_x) {
      int movement = (desired_x > current_x) ? 1 : -1;
      Mouse.move(movement, 0);
      current_x += movement;
    }

    if (current_y != desired_y) {
      int movement = (desired_y > current_y) ? 1 : -1;
      Mouse.move(0, movement);
      current_y += movement;
    }
    
    delay(mouse_move_delay);
  }

  // Change mouse destination when ends reached
  if (current_x == movement_max and current_y == 0) {
    desired_y = movement_max;
  } else if (current_x == movement_max and current_y == movement_max) {
    desired_x = 0;
  } else if (current_x == 0 and current_y == movement_max) {
    desired_y = 0;
  } else if (current_x == 0 and current_y == 0) {
    desired_x = movement_max;
  }
}
