#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 5, 1, 8, SW_UART_EVEN_PARITY);
  
  // ----------------separator---------------
  pinMode(5, HIGH);
}

void loop() {
  send_phrase(&uart);
}
