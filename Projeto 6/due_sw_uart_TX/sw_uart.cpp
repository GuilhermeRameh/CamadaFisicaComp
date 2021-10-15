#include "sw_uart.h"
#pragma GCC optimize ("-O3")

void sw_uart_setup(due_sw_uart *uart, int tx, int stopbits, int databits, int paritybit) {
	
	uart->pin_tx     = tx;
	uart->stopbits   = stopbits;
	uart->paritybit  = paritybit;
  uart->databits   = databits;
  pinMode(tx, OUTPUT);
  
}

int calc_even_parity(char data) {
  int ones = 0;

  for(int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }

  return ones % 2;
}

void send_one(due_sw_uart *uart, char letter) {

  digitalWrite(uart->pin_tx, LOW); // Start Bit
  _sw_uart_wait_T(uart);
  char data = letter;
  // Serial.print("Enviando: ");
  // Serial.println(data);

  for(int i = 0; i < 8; i++){
    // Serial.print(bin[i]);
    int this_bit = (data>>i) & 0x01;
    digitalWrite(uart->pin_tx, this_bit); // Sending individual bits
    _sw_uart_wait_T(uart);
  } 
  // Serial.println("");

  int parity = 0;
  if(uart->paritybit == SW_UART_EVEN_PARITY) {
     parity = calc_even_parity(data);
  } else if(uart->paritybit == SW_UART_ODD_PARITY) {
     parity = !calc_even_parity(data);
  }

  // Serial.print("Parity: ");
  // Serial.println(parity);

  digitalWrite(uart->pin_tx, parity); // Sending Parity
  
  _sw_uart_wait_T(uart);
  digitalWrite(uart->pin_tx, HIGH); // End Bit
  _sw_uart_wait_T(uart);
}

void send_phrase(due_sw_uart *uart){
  char string[] = "oi Guilherme";
  for (int i=0; i<strlen(string); i++){
    send_one(uart, string[i]);
    delay(10);
  }
  exit(0);
}


// MCK 21MHz
void _sw_uart_wait_half_T(due_sw_uart *uart) {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T(due_sw_uart *uart) {
  _sw_uart_wait_half_T(uart);
  _sw_uart_wait_half_T(uart);
}
