#include <stdio.h>
void fizzbuzz (int);

void fizzbuzz (int n)
{
  if (n % 15 == 0) 
    printf("fizzbuzz\n");
  else if (n % 5 == 0) 
    printf("buzz\n");
  else if (n % 3 == 0) 
    printf("buzz\n");
  else if (1) 
    printf("%d\n", n);
}

int main (void)
{
  int n;
  for (n = 0; n < 30; ++n) 
    fizzbuzz(n + 1);
  return 0;
}
