#include <stdio.h>
#include <stdlib.h>

typedef enum gender{
  male,
  female
} gender;

typedef struct person {
  char* name;
  int age;
  gender gender;
} person;

person* init_person (char*, int, gender);

void introduce_person (person*);

person* init_person (char* name, int age, gender gender)
{
  person* person = malloc(sizeof(person));
  person->name = name;
  person->age = age;
  person->gender = gender;
  return person;
}

void introduce_person (person* person)
{
  printf("This is %s.\n", person->name);
  person->gender == male? (printf("He ")) : (printf("She "));
  printf("is %d years old.\n", person->age);
}

int main (void)
{
  person* kojiro = init_person("Kojiro", 25, male);
  introduce_person(kojiro);
  return 0;
}

