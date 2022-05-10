#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern void ECDSA_256_sign(unsigned char sig[64], const unsigned char hash[32]);

static unsigned char char_tonum(char ch){
  unsigned char num;
  if (ch >= 'A' && ch <= 'F'){
    num = ch - 'A' + 10;
  }
  else if (ch >= 'a' && ch <= 'f'){
    num = ch - 'a' + 10;
  }
  else if (ch >= '0' && ch <= '9'){
    num = ch - '0';
  }
  else {
    fprintf(stderr, "Invalid hexadecimal character: %c\n", ch);
    exit(EXIT_FAILURE);
  }
  return num;
}

static void char_tohex(unsigned char *out, char *str, unsigned int clen){
  if (clen % 2 != 0){
    fprintf(stderr, "Invalid length of hex string!\n");
    exit(EXIT_FAILURE);
  }
  unsigned char *ptr = out;

  unsigned char num;
  unsigned int i;
  for (i = 0; i < clen; i++){
    num = char_tonum(str[i]);
    *ptr = num << 4;
    i++;
    num = char_tonum(str[i]);
    *ptr = *ptr ^ num;
    ptr++;
  }
}

int main(int argc, char **argv)
{
  unsigned char sig[64];
  unsigned char hash[32];

  if (argc != 2 && strlen(argv[1]) != 64){
    fprintf(stderr, "Given input is invalid!\n");
    exit(EXIT_FAILURE);
  }

  char_tohex(hash, argv[1], 64);
  ECDSA_256_sign(sig, hash);

  int i;
  for(i=0; i<64; i++) printf("%02X", sig[i]); printf("\n");

  return 0;
}
