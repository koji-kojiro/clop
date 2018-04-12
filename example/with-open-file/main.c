#include <stdio.h>

int main (void)
{
  ({
    FILE* fd = fopen("hello.txt", "w");
    fd == NULL? (perror("Failed to open file")) : (({
      fprintf(fd, "Hello, world!\n");
      fclose(fd);
    }));
  });
  return 0;
}
