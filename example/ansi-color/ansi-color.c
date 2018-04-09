#include <stdio.h>

int main (void)
{
  ({
    int i = 0;
    while (++i < 8) 
      ({
        int j = 0;
        while (++j < 8) 
          ({
            int bg = i + 29;
            int fg = j + 39;
            printf("\033[%d;%dm %d;%d; \033[0m", bg, fg, bg, fg);
          });
        printf("\n");
      });
  });
  return 0;
}
