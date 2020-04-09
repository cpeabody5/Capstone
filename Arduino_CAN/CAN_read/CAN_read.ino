#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg;
MCP2515 mcp2515(10);
int canStatus;
uint16_t upperBits, lowerBits, data;
double voltage, percentage;
int iteration = 0;

void printMicData(int);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_1000KBPS, MCP_16MHZ);
  mcp2515.setNormalMode();
  
  Serial.println("------- CAN Read ----------");
  Serial.println("ID  DLC   DATA");
}

void loop() {
  canStatus = mcp2515.readMessage(&canMsg);
  if (canStatus == MCP2515::ERROR_OK) {
    
    for (int i = 0; i<4; i++)  {  // print the data
      //Serial.print(canMsg.data[i],HEX);
      //Serial.print(" ");
      printMicData(i);
    }
    //Serial.println();      
  }

}

/*void loop() {
  
  canStatus = mcp2515.readMessage(&canMsg);
  if (canStatus == MCP2515::ERROR_OK) {
    iteration += 1;
    Serial.print(canMsg.can_id, HEX); // print ID
    Serial.print(" "); 
    Serial.print(canMsg.can_dlc, HEX); // print DLC
    Serial.print(" ");
    
    for (int i = 0; i<canMsg.can_dlc; i++)  {  // print the data
        
      Serial.print(canMsg.data[i],HEX);
      Serial.print(" ");

    }
    Serial.print("       Iteration: ");
    Serial.println(iteration);      
  } else {
    //Serial.println(canStatus);
  }

}*/

void printMicData(int mic){
  /*upperbits = canMsg.data[2*mic];
  upperbits = upperbits & 0x0F;
  lowerbits = canMsg.data[2*mic+1];*/
  upperBits = canMsg.data[2*mic] & 0x0F;
  lowerBits = canMsg.data[2*mic+1];
  data = (upperBits << 8) | lowerBits;
  voltage = 3.3*data/(1<<12);
  percentage = (voltage/3.3)*100;
  Serial.print("Mic ");
  Serial.print(mic);
  Serial.print(" :");
  Serial.print(voltage);
  Serial.print("V, ");
  Serial.print(percentage);
  Serial.println("%");
}

