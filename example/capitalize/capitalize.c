#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* string_upcase (char*);

char* string_downcase (char*);

char* string_capitalize (char*);

char* string_upcase (char* string)
{
  {
    char* new = malloc(sizeof(char*) * strlen(string));
    int n;
    strcpy(new, string);
    for (n = 0; n < strlen(new); ++n) 
      if (islower(new[n])) 
        new[n] -= 32;
    return new;
  }
}

char* string_downcase (char* string)
{
  {
    char* new = malloc(sizeof(char*) * strlen(string));
    int n;
    strcpy(new, string);
    for (n = 0; n < strlen(new); ++n) 
      if (isupper(new[n])) 
        new[n] += 32;
    return new;
  }
}

char* string_capitalize (char* string)
{
  {
    char* new = malloc(sizeof(char*) * strlen(string));
    unsigned char in_word = 0;
    int n;
    strcpy(new, string);
    for (n = 0; n < strlen(string); ++n) 
      if (isalnum(new[n])) {
        if (in_word && isupper(new[n])) 
          new[n] += 32;
        else if (!in_word && islower(new[n])) 
          new[n] -= 32;
        in_word = 1;
      }
      else in_word = 0;
    return new;
  }
}

int main (void)
{
  {
    char* string = "hELlo, worlD!";
    printf("%s\n", string);
    printf("%s\n", string_downcase(string));
    printf("%s\n", string_upcase(string));
    printf("%s\n", string_capitalize(string));
  }
  return 0;
}
