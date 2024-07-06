#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Function to reverse a string
void reverse_string(char *str)
{
  int n = strlen(str);
  for (int i = 0; i < n / 2; i++)
  {
    char temp = str[i];
    str[i] = str[n - i - 1];
    str[n - i - 1] = temp;
  }
}

// Function to concatenate two strings
void concatenate_strings(char *dest, const char *src)
{
  strcat(dest, src);
}

// Function to find a substring
int find_substring(const char *str, const char *substr)
{
  char *pos = strstr(str, substr);
  if (pos)
  {
    return pos - str;
  }
  return -1;
}

// Function to convert a string to uppercase
void to_uppercase(char *str)
{
  for (int i = 0; str[i] != '\0'; i++)
  {
    str[i] = toupper(str[i]);
  }
}

// Function to convert a string to lowercase
void to_lowercase(char *str)
{
  for (int i = 0; str[i] != '\0'; i++)
  {
    str[i] = tolower(str[i]);
  }
}
