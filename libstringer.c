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
// Doesnt works
void concatenate_strings(char *dest, const char *src)
{
  strcat(dest, src);
}

// Function to find a substring
// Should highlight it in the text
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
    if (isalpha(str[i])) // Check if the character is an alphabetic letter
    {
      str[i] = toupper(str[i]);
    }
  }
}

// Function to convert a string to lowercase
void to_lowercase(char *str)
{
  for (int i = 0; str[i] != '\0'; i++)
  {
    if (isalpha(str[i])) // Check if the character is an alphabetic letter
    {
      str[i] = tolower(str[i]);
    }
  }
}

// Function to replace all end of line occurrences with a specific string
void replace_end_of_line(const char *str, const char *replacement, char *result, int result_size)
{
  char buffer[1024];
  int offset = 0;
  for (int i = 0; str[i] != '\0'; i++)
  {
    if (str[i] == '\n')
    {
      snprintf(buffer + offset, result_size - offset, "%s\n", replacement);
      offset += strlen(replacement) + 1;
    }
    else
    {
      buffer[offset++] = str[i];
    }
  }
  buffer[offset] = '\0';
  snprintf(result, result_size, "%s", buffer);
}

// Function to replace all newline characters with a specific string
void replace_all_newlines(const char *str, const char *replacement, char *result, int result_size)
{
  char buffer[1024];
  int offset = 0;
  for (int i = 0; str[i] != '\0'; i++)
  {
    if (str[i] == '\n' || str[i] == '\r')
    {
      snprintf(buffer + offset, result_size - offset, "%s\n", replacement);
      offset += strlen(replacement) + 1;
    }
    else
    {
      buffer[offset++] = str[i];
    }
  }
  buffer[offset] = '\0';
  snprintf(result, result_size, "%s", buffer);
}

// Function to replace start of line with a specific string
void replace_start_of_line(const char *str, const char *replacement, char *result, int result_size)
{
  char buffer[1024];
  int offset = 0;
  int start = 1;
  for (int i = 0; str[i] != '\0'; i++)
  {
    if (start)
    {
      snprintf(buffer + offset, result_size - offset, "%s", replacement);
      offset += strlen(replacement);
      start = 0;
    }
    buffer[offset++] = str[i];
    if (str[i] == '\n')
    {
      start = 1;
    }
  }
  buffer[offset] = '\0';
  snprintf(result, result_size, "%s", buffer);
}

// Function to replace a specific sequence with another sequence
void replace_sequence(const char *str, const char *sequence, const char *replacement, char *result, int result_size)
{
  char buffer[1024];
  int offset = 0;
  const char *current = str;
  const char *match;
  while ((match = strstr(current, sequence)) != NULL)
  {
    int len = match - current;
    snprintf(buffer + offset, len + 1, "%s", current);
    offset += len;
    snprintf(buffer + offset, strlen(replacement) + 1, "%s", replacement);
    offset += strlen(replacement);
    current = match + strlen(sequence);
  }
  snprintf(buffer + offset, strlen(current) + 1, "%s", current);
  snprintf(result, result_size, "%s", buffer);
}