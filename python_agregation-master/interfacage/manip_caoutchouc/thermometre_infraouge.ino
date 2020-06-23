#include <i2cmaster.h>

const int sortiePin = 5;    // pour la sortie PWM
const int offsetT=14650; // seule valeur a changer
// Tref (Kelvin)=offsteT*0.02
// prendre Tref=Tpiece-1K

void setup(){
	Serial.begin(9600);
	Serial.println("Setup...");
	
  	i2c_init(); //Initialise the i2c bus
  	PORTC = (1 << PORTC4) | (1 << PORTC5);//enable pullups
  
        // set the digital pins as outputs
        pinMode(sortiePin, OUTPUT);
  }

void loop(){
    int dev = 0x5A<<1;
    int data_low = 0;
    int data_high = 0;
    int pec = 0;
    
    i2c_start_wait(dev+I2C_WRITE);
    i2c_write(0x07);
    
    // read
    i2c_rep_start(dev+I2C_READ);
    data_low = i2c_readAck(); //Read 1 byte and then send ack
    data_high = i2c_readAck(); //Read 1 byte and then send ack
    pec = i2c_readNak();
    i2c_stop();
    
    //This converts high and low bytes together and processes temperature, MSB is a error bit and is ignored for temps
    double tempFactor = 0.02; // 0.02 degrees per LSB (measurement resolution of the MLX90614)
    double tempData = 0x0000; // zero out the data
    int frac; // data past the decimal point
    
    // This masks off the error bit of the high byte, then moves it left 8 bits and adds the low byte.
    tempData = (double)(((data_high & 0x007F) << 8) + data_low);
    int tempDataRaw;
    int tempDataOut;
    tempDataRaw=tempData;
    tempDataOut=(tempDataRaw-offsetT)/2;
    tempData = (tempData * tempFactor)-0.01;
    
    float celsius = tempData - 273.15;
    float fahrenheit = (celsius*1.8) + 32;
    
    //Serial.print("tempDataOut: ");
    //Serial.println(tempDataOut);

   // Serial.print("Celsius: ");
    Serial.println(celsius);

    //Serial.print("Fahrenheit: ");
    //Serial.println(fahrenheit);
    
    analogWrite(sortiePin, tempDataOut);

    delay(10); // wait a second before printing again
}
