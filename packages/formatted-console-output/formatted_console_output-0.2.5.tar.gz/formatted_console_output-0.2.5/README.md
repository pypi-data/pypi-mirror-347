This script allows you to set the foreground and background colors of your Console output as well as setting a few styles. The script uses ANSI Escape Codes for colors black, red, green, yellow, blue, magenta, cyan, & white. It also uses the ANSI Escape Codes for styles bold, underline, and both combined. Coders can either put together a mult-formatted message or simply set the format for a single print() message.

This helps when you're using very verbose libraries where you cannot turn off their output. Meanwhile you're trying to catch Exception messages like 'was that an Exception? It was kinda shaped like an exception...' Now we can make your Exception red!!!!

### OS COMPATIBILITY

Though Linux and Mac are pretty much alsways compatible... This library seamlessly takes into account Windows machines that are not configured to support ANSI escape codes. When your script runs, the library attempts to enable this feature for this session. If you're compatible, I go formatted. If I can make you compatible for this seesion, I go formatted. If all fails, then I go back to printing with default behavior.

### HOW TO REFERENCE

1. install the library

```batch
    pip install formatted-console-output
```

1. At the top of your main script add the following import statement:

```python
    from formatted_console_output import ForegroundColor, BackgroundColor, TextFormat, output_formatted_message as print, output_many_format_message as printf
```

### CODE COMPATIBILITY/OVERLOADING

You do not have to alias the method imports as "print" and "printf" but that makes it more natural for you to code against and allows you to leverage everything else about the print() method. The script passes on all extra keyword arguments that are normally used in a print() call, so go wild. Anyone referencing this library that tries to use the print() method as normal would still get default console output with no format and normal behavior otherwise.

### HOW TO USE IN CODE

The enumerators that define these colors/formats are:

- ForegroundColor [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, NONE]
- BackgroundColor [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, NONE]
- TextFormat [BOLD, UNDERLINE, BOLD_AND_UNDERLINE, NONE]

The added keyword arguments are:

- fg_color (default is ForegroundColor.NONE)
- bg_color (default is BackgroundColor.NONE)
- format (default is TextFormat.NONE)

In the following example we're printing a message to console with one format for the entire line: blue text on a yellow background in bold style.

I also threw in some standard keyword arguments to show that:

```python
print(
    f"Archiving files and reporting against them in '{dir_path}'",
    fg_color=ForegroundColor.BLUE,
    bg_color=BackgroundColor.YELLOW,
    format=TextFormat.BOLD,
    sep="  -  ",
    end="\n\n"
)
```

In this example we're formatting each phrase differently and putting it together using an array of FormattedPhrase objects (any left out parameters in any Phrase object is considered to be set to NONE):

```python
message = [
    FormattedPhrase(
        "The ",
        bg_color=BackgroundColor.BLACK,
        fg_color=ForegroundColor.YELLOW,
        format=TextFormat.UNDERLINE,
    ),
    FormattedPhrase(
        "quick brown foo ",
        bg_color=BackgroundColor.RED,
        fg_color=ForegroundColor.YELLOW,
        format=TextFormat.BOLD,
    ),
    FormattedPhrase(
        "jumped over the ",
        bg_color=BackgroundColor.BLACK,
        fg_color=ForegroundColor.YELLOW,
    ),
    FormattedPhrase(
        "lazy ",
        bg_color=BackgroundColor.BLUE,
        fg_color=ForegroundColor.YELLOW,
        format=TextFormat.BOLD,
    ),
    FormattedPhrase(
        "bar",
        bg_color=BackgroundColor.BLUE,
        fg_color=ForegroundColor.YELLOW,
        format=TextFormat.BOLD_AND_UNDERLINE,
    ),
]
printf(message)
```

In this final example, we're not printing, we're gathering formatted output to print later by pulling a FormattedPhrase object's get_output() method. In essence, a coder could put together an entire formatted paragragh in memory before printing by doing something like this:

```python
message1 = FormattedPhrase(
    "The ",
    bg_color=BackgroundColor.BLACK,
    fg_color=ForegroundColor.YELLOW,
    format=TextFormat.UNDERLINE,
)
message2 = FormattedPhrase(
    "quick brown foo ",
    bg_color=BackgroundColor.RED,
    fg_color=ForegroundColor.YELLOW,
    format=TextFormat.BOLD,
)
message3 = FormattedPhrase(
    "jumped over the ",
    bg_color=BackgroundColor.BLACK,
    fg_color=ForegroundColor.YELLOW,
)
message4 = FormattedPhrase(
    "lazy ",
    bg_color=BackgroundColor.BLUE,
    fg_color=ForegroundColor.YELLOW,
    format=TextFormat.BOLD,
)
message5 = FormattedPhrase(
    "bar",
    bg_color=BackgroundColor.BLUE,
    fg_color=ForegroundColor.YELLOW,
    format=TextFormat.BOLD_AND_UNDERLINE,
)
my_message = (
    message1.get_output()
    + message2.get_output()
    + message3.get_output()
    + message4.get_output()
    + message5.get_output()
)
print(my_message)
```

### How do I make Exceptions Red?

You can intercept an Exception in a catch blcok (Except statement) by doing something like this at the top level:

```python
def kill_empty_directory(dir_path):
    print(
        f"Removing {dir_path}\n",
        fg_color=ForegroundColor.BLUE,
        bg_color=BackgroundColor.YELLOW,
    )
    try:
        os.rmdir(dir_path)
    except Exception as e:
        original_error = str(e)
        print(f"Error deleting directory '{dir_path}': {original_error}",fg_color=ForegroundColor.RED)
```
