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

  pinMode(uart->pin_tx, LOW); // Start Bit
  _sw_uart_wait_T(uart);
  char data = 'a';

  for(int i = 0; i < 8; i++){
    Serial.println(data>>i);
    int this_bit = data>>i;
    if(this_bit == 0){
       pinMode(uart->pin_tx, LOW);
    }
    else{
      pinMode(uart->pin_tx, HIGH);
    }
    _sw_uart_wait_T(uart);
  } 

  int parity = calc_even_parity(data);
  if(parity == 0){
    pinMode(uart->pin_tx, LOW);
  }
  else{
    pinMode(uart->pin_tx, HIGH);
  }
  _sw_uart_wait_T(uart);
  pinMode(uart->pin_tx, HIGH); // End Bit
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
