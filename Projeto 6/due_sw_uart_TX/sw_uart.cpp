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

void send_message(due_sw_uart *uart) {

  digitalWrite(uart->pin_tx, LOW); // Start Bit
  _sw_uart_wait_T(uart);
  char data = 'a';
  uint8_t bin[8];

  // Serial.print("Enviando: ");
  // Serial.println(data);

  charToBinaryArray(data, bin);

  for(int i = 0; i < 8; i++){
    // Serial.print(bin[i]);
    int this_bit = bin[i];
    if(this_bit == 0){
      digitalWrite(uart->pin_tx, LOW);
    }
    else{
      digitalWrite(uart->pin_tx, HIGH);
    }
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

  if(parity == 0){
    digitalWrite(uart->pin_tx, LOW);
  }
  else{
    digitalWrite(uart->pin_tx, HIGH);
  }
  _sw_uart_wait_T(uart);
  digitalWrite(uart->pin_tx, HIGH); // End Bit
  _sw_uart_wait_T(uart);
}

void charToBinaryArray(char c, uint8_t *binary_array){
  for(uint8_t i = 0; i < 8; i++) {
    binary_array[i] = c & (1 << i);
  }
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
