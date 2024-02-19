#include <Arduino.h>
#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#include <soc/soc.h>
#include <soc/rtc_cntl_reg.h>

#define MISO_PIN 19
#define MOSI_PIN 23
#define SCK_PIN 18
#define SS_PIN 5
#define RST_PIN 13

MFRC522 rfid(SS_PIN, RST_PIN); // Instanca klase

// NUID - kartica sa 4-bajtnim ID brojevima (Non-Unique ID)
// PICC - RFID kartica ili tag koja koristi IS0/IEC 14443A sučelje, u ovom slučaju Mifare (Proximity Integrated Circuit Card)
// PCD - RFID čitač temeljen na integriranom krugu beskontaktnog čitača NXP MFRC522 (Proximity Coupling Device)

void printHex(byte *buffer, byte bufferSize);
void printDec(byte *buffer, byte bufferSize);
String stringHex(byte *buffer, byte bufferSize);

// Inicijalizacija array-a za spremanje novih NUID-a 
byte nuidPICC[4];
// Kreiranje json dokumenta
StaticJsonDocument<200> doc;

const char* SSID = "Komusar-O-2.4G";
const char* PASSWORD = "Komusar11";
const int USER_ID = 4;

const char *serverName = "http://192.168.100.24:80/rfid"; //Domena servera
HTTPClient http; //Instanca klase

void setup() { 
  Serial.begin(9600);
  SPI.begin(); // Inicijalizacija SPI komunikacije
  rfid.PCD_Init(); // Inicijlizacija MFRC522
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);

  // Spajanje na WiFi
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Spajanje na WiFi...");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(1000);
  }
  Serial.println(WiFi.localIP());
}


void loop() {

  // Resetiraj petlju ako kartica nije u blizini čitača. Stavlja proces u stanje mirovanja.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Provjerava je li NUID pročitan
  if ( ! rfid.PICC_ReadCardSerial())
    return;

  // Spremanje NUID u nuidPICC array
  for (byte i = 0; i < 4; i++) {
    nuidPICC[i] = rfid.uid.uidByte[i];
  }
   
  //Serial.println(("NUID glasi:"));
  //Serial.print(("Heksadecimalno: "));
  //printHex(rfid.uid.uidByte, rfid.uid.size);
  Serial.println();
  //Serial.print(("Decimalno: "));
  //printDec(rfid.uid.uidByte, rfid.uid.size);
  Serial.println();
  
  String card_uid = stringHex(rfid.uid.uidByte, rfid.uid.size);
  doc["nuid"] = card_uid;
  doc["user_id"] = USER_ID;

  String json;
  serializeJson(doc, json);
  
  http.begin(serverName); //Otvori komunikaciju sa serverom
  http.addHeader("Content-Type", "application/json");

  int httpResponseCode = http.POST(json);

  Serial.print("Statusni kod: ");
  Serial.println(httpResponseCode);
  Serial.println(http.getString());
  http.end(); //Zatvori komunikaciju

  // Zaustavljanje PICC-a
  rfid.PICC_HaltA();

  // Zaustavljanje enkripcije na čitaču
  rfid.PCD_StopCrypto1();
}

// Funkcija za ispisivanje array u heksadecimalnom obliku na Serial
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

// Funkcija za ispisivanje array u decimalnom obliku na Serial
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(' ');
    Serial.print(buffer[i], DEC);
  }
}

// Funkcija za spremanje stringa UID-a kartice
String stringHex(byte *buffer, byte bufferSize) {
  String id = "";
  for (byte i = 0; i < bufferSize; i++) {
    id += buffer[i] < 0x10 ? "0" : "";
    id += String(buffer[i], HEX);
  }
  return id;
}