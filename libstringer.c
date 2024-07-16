#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Function to calculate the required buffer size for generic string modifications
int calculate_required_size(const char *str, const char *start_replacement, const char *end_replacement, const char *eol_replacement, const char *sequence, const char *replacement)
{
  int size = 0;
  int num_lines = 0;
  int sequence_len = sequence ? strlen(sequence) : 0;
  int replacement_len = replacement ? strlen(replacement) : 0;

  for (int i = 0; str[i] != '\0'; i++)
  {
    size++;
    if (str[i] == '\n')
    {
      num_lines++;
    }
  }

  // Calculate the additional size for start and end replacements
  if (start_replacement)
  {
    size += num_lines * strlen(start_replacement);
  }
  if (end_replacement)
  {
    size += num_lines * strlen(end_replacement);
  }

  // Calculate the additional size for end-of-line replacements
  if (eol_replacement)
  {
    size += num_lines * strlen(eol_replacement);
  }

  // Calculate the additional size for sequence replacements
  if (sequence && replacement)
  {
    const char *ptr = str;
    while ((ptr = strstr(ptr, sequence)) != NULL)
    {
      size += replacement_len - sequence_len;
      ptr += sequence_len;
    }
  }

  return size + 1; // +1 for the null terminator
}

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
  int offset = 0;
  for (int i = 0; str[i] != '\0'; i++)
  {
    if (str[i] == '\n')
    {
      if (offset + strlen(replacement) + 1 >= result_size)
        break; // Avoid overflow
      snprintf(result + offset, result_size - offset, "%s\n", replacement);
      offset += strlen(replacement) + 1;
    }
    else
    {
      if (offset + 1 >= result_size)
        break; // Avoid overflow
      result[offset++] = str[i];
    }
  }
  if (offset < result_size)
  {
    result[offset] = '\0';
  }
}

// Function to replace start of line with a specific string
void replace_start_of_line(const char *str, const char *replacement, char *result, int result_size)
{
  int offset = 0;
  int start = 1;
  for (int i = 0; str[i] != '\0'; i++)
  {
    if (start)
    {
      if (offset + strlen(replacement) >= result_size)
        break; // Avoid overflow
      snprintf(result + offset, result_size - offset, "%s", replacement);
      offset += strlen(replacement);
      start = 0;
    }
    if (offset + 1 >= result_size)
      break; // Avoid overflow
    result[offset++] = str[i];
    if (str[i] == '\n')
    {
      start = 1;
    }
  }
  if (offset < result_size)
  {
    result[offset] = '\0';
  }
}

// Function to replace the start of each line by ' and the end of each line by ',
void sql_format(const char *str, char *result, int result_size)
{
  int offset = 0;
  int start = 1;
  for (int i = 0; str[i] != '\0'; i++)
  {
    if (start)
    {
      if (offset + 1 >= result_size)
        break; // Avoid overflow
      result[offset++] = '\'';
      start = 0;
    }
    if (offset + 1 >= result_size)
      break; // Avoid overflow
    result[offset++] = str[i];

    if (str[i] == '\n')
    {
      if (offset + 3 >= result_size)
        break; // Avoid overflow
      result[offset - 1] = '\'';
      result[offset++] = ',';
      result[offset++] = '\n';
      start = 1;
    }
  }
  if (str[offset - 1] != '\n')
  {
    if (offset + 1 < result_size)
      result[offset++] = '\'';
  }
  if (offset < result_size)
    result[offset] = '\0';
}

// Function to replace a specific sequence with another sequence
void replace_sequence(const char *str, const char *sequence, const char *replacement, char *result, int result_size)
{
  int offset = 0;
  const char *current = str;
  const char *match;
  int sequence_len = strlen(sequence);
  int replacement_len = strlen(replacement);

  while ((match = strstr(current, sequence)) != NULL)
  {
    int len = match - current;
    if (offset + len >= result_size)
      break; // Avoid overflow

    // Copy the part before the match
    snprintf(result + offset, len + 1, "%s", current);
    offset += len;

    if (offset + replacement_len >= result_size)
      break; // Avoid overflow

    // Copy the replacement
    snprintf(result + offset, replacement_len + 1, "%s", replacement);
    offset += replacement_len;

    // Move the current pointer past the sequence
    current = match + sequence_len;
  }

  // Copy the remaining part of the string
  if (offset + strlen(current) < result_size)
  {
    snprintf(result + offset, result_size - offset, "%s", current);
  }
  else if (offset < result_size)
  {
    result[offset] = '\0'; // Null-terminate the result
  }
}

// Function to find all matches of a pattern
int find_all_occurrences(const char *str, const char *pattern, int *start_indices, int *end_indices, int max_matches)
{
  int match_count = 0;
  const char *p = str;
  const char *match;
  while ((match = strstr(p, pattern)) != NULL && match_count < max_matches)
  {
    start_indices[match_count] = match - str;
    end_indices[match_count] = start_indices[match_count] + strlen(pattern);
    p = match + strlen(pattern);
    match_count++;
  }
  return match_count;
}

// Function to split a string by a specific pattern
int split_by_pattern(const char *str, const char *pattern, char **results, int max_splits)
{
  int split_count = 0;
  const char *p = str;
  const char *match;
  while ((match = strstr(p, pattern)) != NULL && split_count < max_splits)
  {
    int len = match - p;
    results[split_count] = (char *)malloc(len + 1);
    strncpy(results[split_count], p, len);
    results[split_count][len] = '\0';
    split_count++;
    p = match + strlen(pattern);
  }
  if (split_count < max_splits)
  {
    results[split_count] = strdup(p);
    split_count++;
  }
  return split_count;
}

// Function to free the memory allocated by split_by_pattern
void free_split_results(char **results, int num_splits)
{
  for (int i = 0; i < num_splits; i++)
  {
    free(results[i]);
  }
}