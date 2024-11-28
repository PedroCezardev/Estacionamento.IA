#include <Servo.h>

// Definição dos pinos dos LEDs
const int led1Vaga[] = {3, 5, 6, 8}; // LEDs verdes para as vagas 1 a 4
const int led2Vaga[] = {2, 4, 7, 9}; // LEDs vermelhos para as vagas 1 a 4

Servo meuServo;  // Cria um objeto servo para controlar um servo motor
int pinoServo = 12;  // Pino ao qual o servo está conectado
int pinoBotaoServo = 11;  // Pino ao qual o botão está conectado
int estadoBotaoServo;  // Variável para armazenar o estado do botão do servo

void setup() {
  // Definição dos pinos dos LEDs como saída
  for (int i = 0; i < 4; i++) {
    pinMode(led1Vaga[i], OUTPUT);
    pinMode(led2Vaga[i], OUTPUT);
    digitalWrite(led1Vaga[i], HIGH); // LEDs verdes ligados por padrão
    digitalWrite(led2Vaga[i], LOW);  // LEDs vermelhos desligados por padrão
  }
  
  meuServo.attach(pinoServo);   // Anexa o servo ao pino de controle
  pinMode(pinoBotaoServo, INPUT);  // Define o pino do botão do servo como entrada com pull-up interno

  // Inicializa a comunicação serial para depuração
  Serial.begin(9600);
}

void loop() {
  
  // Controle do servo motor com base no estado do botão
  estadoBotaoServo = digitalRead(pinoBotaoServo);  // Lê o estado do botão do servo

  if (estadoBotaoServo == LOW) {  // Se o botão estiver pressionado (LOW porque estamos usando pull-up)
    meuServo.write(90);  // Gira o servo para 90 graus
    //delay(500);
  } else {  // Caso contrário
    meuServo.write(0);  // Gira o servo para 0 graus
    delay(5000);
  }
  
  // Recebendo valores do monitor serial
  if (Serial.available() > 0) {
    char vaga = Serial.read(); // Lê a identificação da vaga ('1', '2', '3', '4')
    int vagaIndex = vaga - '1'; // Converte '1', '2', '3', '4' em índices 0, 1, 2, 3

    if (vagaIndex >= 0 && vagaIndex < 4) {
      Serial.println(led1Vaga[vagaIndex]);
      Serial.println(led2Vaga[vagaIndex]);
      // Alterna o estado dos LEDs
      if (digitalRead(led1Vaga[vagaIndex]) == HIGH) {
        digitalWrite(led1Vaga[vagaIndex], LOW);
        digitalWrite(led2Vaga[vagaIndex], HIGH);
      } else {
        digitalWrite(led1Vaga[vagaIndex], HIGH);
        digitalWrite(led2Vaga[vagaIndex], LOW);
      }
    }
  }

  delay(100);  // Pequeno atraso para evitar leituras repetidas
}