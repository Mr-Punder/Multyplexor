

#define DS 4
#define OE_ 5
#define STSP 6
#define SHSP 7
#define MR_ 8
#define amount 144

const char separator = ',';


void step (int count=1){
  for(int i = 0; i < count; i++){
    digitalWrite(SHSP, 0);
    delayMicroseconds(1);
    digitalWrite(SHSP, 1);
    delayMicroseconds(1);
  }
}

class Multyplexor{
  public:

  Multyplexor(const String mess);
  String Switch();
  String ARR();
  
  String mode = "def";
  int connect[9][16]={{0}};
};

String Multyplexor::ARR(){
  String s;
  // Serial.println("here");
    for(int j=0; j<9; j++){
  for(int i = 0; i < 16; i++){
        s += String(connect[j][i]) + ',';
      }
      s += "\n";
  }
  // Serial.println("here");

  return s;
}

Multyplexor::Multyplexor(const String mess){
  
  if (mess.startsWith("GND")){
    for (auto i = 0; i < 16; ++i){
      connect[8][i] = 1;
    }
    mode = "GND";
   }
  else if (mess.startsWith("MOm")){
    for (int i = 0; i < 16; ++i){
      connect[7][i] = 1;
    }
   mode = "10MOm";
  }
  else if (mess.startsWith("+")){
   
    int ind = 1;

    
    for (int i = 0; i < 16 ; ++i){
      char val = mess.charAt(ind);
      int chanel = int(val) - 48;
      if (chanel != 0){
      connect[chanel-1][i] = 1;
      }
      ind += 1;
    }
    mode = "single";
  }
  
  else if (mess.startsWith("MULTY")){
     int ind = mess.indexOf('*')+1;
    for (int i = 0; i < 16; ++i){
      for (int j = 0; j < 9; ++j){
      char val = mess.charAt(ind);
      int chanel = int(val) - 48;
      connect[j][i] = chanel;
      ind += 1;
      }
    }
    mode = "multy";
  }
  else{
    mode = "unknown";
  }
  

}


String Multyplexor::Switch(){
 digitalWrite(OE_, 0); 

   for(int i = 0; i < 18; i++){
      for(int j=0; j<8; j++)
        if(i<9){
          digitalWrite(DS,connect[i][15-j]);
        step();
        delay(7);
        }
        else{
          digitalWrite(DS,connect[17-i][7-j]);
        step();
        delay(7);
        }
      }

  digitalWrite(STSP, 0);
  delayMicroseconds(1);
  digitalWrite(STSP, 1);
  delayMicroseconds(1);
  return mode;
}





void setup() {
  Serial.begin(9600);
  pinMode(DS, OUTPUT);
  pinMode(OE_, OUTPUT);
  pinMode(STSP, OUTPUT);
  pinMode(SHSP, OUTPUT);
  pinMode(MR_, OUTPUT);
  digitalWrite(OE_, 1);
  digitalWrite(MR_, 1);
  digitalWrite(DS, 0);
  step(144);
}



void loop() {
  if (Serial.available()) { // Проверяем, есть ли доступные данные в последовательном порту
  /*комманда имеет вид GND/MOm/набор цыфр от 1 до 9 (1-7)номер выхода (8-9)земля или резистор*/
    //Serial.println("recived");
    String mess = Serial.readString();
    //Serial.print(mess);
    //Serial.println("recieved");
    Multyplexor multy(mess);
    multy.Switch();
    Serial.println(multy.mode);
    

  }
}
