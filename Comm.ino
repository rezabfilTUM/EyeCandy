#include <Wire.h>
#include <Adafruit_NeoPixel.h>
int ldr, i;
int led = 0;
int ledr, ledg, ledb;
int oledr, oledg, oledb;
char temp;
int X0, X1, X_out;
char data[4];
#define PIN      4
#define N_LEDS 35

Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_RGBW + NEO_KHZ800);



void get_rgb(void);
void read_ldr(void);

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
  delay(100);
  strip.begin();

}

void loop() {
  read_ldr();

  if (Serial.available())
  {
    temp = Serial.read();
    if (temp == 'T')
      get_rgb();

    if (temp == 'L')
    {
      Serial.println(ldr);
    }

    delay(400);


  }
}


void read_ldr()
{
  ldr = analogRead(A0) / 4;
  if (ldr > 100)
    ldr = 100;
}



void get_rgb()
{
  oledr = ledr;
  oledg = ledg;
  oledb = ledb;

  i = 0;
  while (temp != ',')
  {
    while (!Serial.available());
    temp = Serial.read();
    if (temp != ',')
      data[i++] = temp;
  }
  data[i] = '\0';
  ledr = atoi(data);

  i = 0; temp = '0';
  while (temp != ',')
  {
    while (!Serial.available());
    temp = Serial.read();
    if (temp != ',')
      data[i++] = temp;
  }
  data[i] = '\0';
  ledg = atoi(data);


  i = 0; temp = '0';
  while (temp != ',')
  {
    while (!Serial.available());
    temp = Serial.read();
    if (temp != ',')
      data[i++] = temp;
  }
  data[i] = '\0';
  ledb = atoi(data);


  if (oledr <= ledr)   //r
  {
    for (int n = oledr; n <= ledr; n=n+2)
    { for (int m = 0; m < 35; m++)
      { strip.setPixelColor(m, strip.Color(oledg, n, oledb)); // GRB
        strip.show();
      }
    }
  }


  if (oledr > ledr)
  {
    for (int n = oledr; n >= ledr; n=n-2)
    { for (int m = 0; m < 35; m++)
      { strip.setPixelColor(m, strip.Color(oledg, n, oledb)); // GRB
        strip.show();
      }
    }
  }

  if (oledg <= ledg)         //g
  {
    for (int n = oledg; n <= ledg; n=n+2)
    { for (int m = 0; m < 35; m++)
      { strip.setPixelColor(m, strip.Color(n, ledr, oledb)); // GRB
        strip.show();
      }
    }
  }


  if (oledg > ledg)
  {
    for (int n = oledg; n >= ledg; n=n-2)
    { for (int m = 0; m < 35; m++)
      { strip.setPixelColor(m, strip.Color(n, ledr, oledb)); // GRB
        strip.show();
      }
    }
  }


  if (oledb <= ledb)         //b
  {
    for (int n = oledb; n <= ledb; n=n+2)
    { for (int m = 0; m < 35; m++)
      { strip.setPixelColor(m, strip.Color(ledg, ledr, n)); // GRB
        strip.show();
      }
    }
  }


  if (oledb > ledb)
  {
    for (int n = oledb; n >= ledb; n=n-2)
    { for (int m = 0; m < 35; m++)
      { strip.setPixelColor(m, strip.Color(ledg, ledr, n)); // GRB
        strip.show();
      }
    }
  }
  Serial.println("done");


}




