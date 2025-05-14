This script allows you to set the foreground and background colors of your Console output as well as setting a few styles. The script uses ANSI Escape Codes for colors black, red, green, yellow, blue, magenta, cyan, & white. It also allows you to create custom colors that are also passed as ANSI Escape Codes. The script also uses the ANSI Escape Codes for styles bold, underline, and both combined. Coders can either put together a multi-formatted message or simply set the format for a single print() message.

This helps when you're using very verbose libraries where you cannot turn off their output. Meanwhile you're trying to catch Exception messages like 'was that an Exception? It was kinda shaped like an exception...' Now we can make your Exception red!!!!

### OS COMPATIBILITY

Though Linux and Mac are pretty much always compatible... This library seamlessly takes into account Windows machines that are not necessarily configured to support ANSI escape codes. When your script runs, the library attempts to enable this feature for this session. If you're already compatible, we go formatted. If we can make you compatible for this session, we go formatted. If all fails, then we go back to printing with default behavior.

### HOW TO REFERENCE

1. install the library

```batch
    pip install formatted-console-output
```

2. At the top of your script add one of the following import statements:

```python
    from formatted_console_output import ForegroundColor, BackgroundColor, TextFormat, FormattedPhrase, CustomColor, output_formatted_message as print, output_many_format_message as printf
```

...or...

```python
    from formatted_console_output import *
    from formatted_console_output import output_formatted_message as print, output_many_format_message as printf
```

### CODE COMPATIBILITY/OVERLOADING

You do not have to alias the method imports as "print" and "printf" but that makes it more natural for you to code against and allows you to leverage everything else about the print() method. The script passes on all extra keyword arguments that are normally used in a print() call, so go wild. Anyone referencing this library that tries to use the print() method as normal would still get default console output with no format and normal behavior otherwise.

### HOW TO USE IN CODE

#### Keyword Arguments (kwargs)

The added keyword arguments are:

- fg_color (default is ForegroundColor.NONE)
- bg_color (default is BackgroundColor.NONE)
- format (default is TextFormat.NONE)

##### Enumerators & Classes

The enumerators/classes that define these colors/formats are:

- ForegroundColor [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, NONE]
- BackgroundColor [BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, NONE]
- TextFormat [BOLD, UNDERLINE, BOLD_AND_UNDERLINE, NONE]
- CustomColor - any RGB

NOTE: bg_color and fg_color can take either an Enumerator value or a CustomColor object.

### Code Examples

#### Example 1:

In the following example we're printing a message to console with one format for the entire line: blue text on a yellow background in bold style. I also threw in some standard keyword arguments (sep and end) to show that can be included:

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

#### Example 2

In this example, we're passing a CustomColor which is a brown color for bg_color. So this will print yellow on brown:

```python
    print(
        "The quick brown foo jumped over the lazy bar",
        fg_color=ForegroundColor.YELLOW,
        bg_color=CustomColor(r=156, g=101, b=0, is_fg=False),
    )
```

#### Example 3

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

#### Example 4

In this final example, we're not printing until later. First we're gathering formatted output by pulling a FormattedPhrase object's get_output() method into a variable. In essence, a coder could put together an entire formatted paragragh in memory before printing by doing something like this:

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
