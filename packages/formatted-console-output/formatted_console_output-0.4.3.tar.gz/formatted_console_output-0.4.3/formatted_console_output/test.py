import formatted_console_output as fmt
from formatted_console_output import output_formatted_message as print
from formatted_console_output import output_many_format_message as printf
from formatted_console_output import output_error_message as msg
from formatted_console_output import log_exception_stacktrace as err


# EXAMPLE 1
print(
    f"The quick brown foo jumped over the lazy bar",
    fg_color=fmt.ForegroundColor.BLUE,
    bg_color=fmt.BackgroundColor.YELLOW,
    format=fmt.TextFormat.BOLD,
    sep="  -  ",
    end="\n\n",
)


# EXAMPLE 2
print(
    "The quick brown foo jumped over the lazy bar",
    fg_color=fmt.ForegroundColor.YELLOW,
    bg_color=fmt.CustomColor(r=156, g=101, b=0, is_fg=False),
)


# EXAMPLE 3
# create an array of FormattedPhrase objects to pass to printf()
message = [
    fmt.FormattedPhrase(
        "The ",
        bg_color=fmt.BackgroundColor.BLACK,
        fg_color=fmt.ForegroundColor.YELLOW,
        format=fmt.TextFormat.UNDERLINE,
    ),
    fmt.FormattedPhrase(
        "quick brown foo ",
        bg_color=fmt.BackgroundColor.RED,
        fg_color=fmt.ForegroundColor.YELLOW,
        format=fmt.TextFormat.BOLD,
    ),
    fmt.FormattedPhrase(
        "jumped over the ",
        fg_color=fmt.ForegroundColor.YELLOW,
    ),
    fmt.FormattedPhrase(
        "lazy ",
        bg_color=fmt.BackgroundColor.BLUE,
        fg_color=fmt.ForegroundColor.YELLOW,
    ),
    fmt.FormattedPhrase(
        "bar",
        bg_color=fmt.BackgroundColor.BLUE,
        fg_color=fmt.ForegroundColor.YELLOW,
        format=fmt.TextFormat.BOLD_AND_UNDERLINE,
    ),
]
printf(message)


# EXAMPLE 4
message = ""
# some code
message += fmt.FormattedPhrase(
    "The ",
    bg_color=fmt.BackgroundColor.BLACK,
    fg_color=fmt.ForegroundColor.YELLOW,
    format=fmt.TextFormat.UNDERLINE,
).get_output()
# some more code
message += fmt.FormattedPhrase(
    "quick brown foo ",
    bg_color=fmt.BackgroundColor.RED,
    fg_color=fmt.ForegroundColor.YELLOW,
    format=fmt.TextFormat.BOLD,
).get_output()
# some more code
message += fmt.FormattedPhrase(
    "jumped over the ",
    bg_color=fmt.BackgroundColor.BLACK,
    fg_color=fmt.ForegroundColor.YELLOW,
).get_output()
# some more code
message += fmt.FormattedPhrase(
    "lazy ",
    bg_color=fmt.BackgroundColor.BLUE,
    fg_color=fmt.ForegroundColor.YELLOW,
    format=fmt.TextFormat.BOLD,
).get_output()
# some more code
message += fmt.FormattedPhrase(
    "bar",
    bg_color=fmt.BackgroundColor.BLUE,
    fg_color=fmt.ForegroundColor.YELLOW,
    format=fmt.TextFormat.BOLD_AND_UNDERLINE,
).get_output()
print(message)


# EXAMPLE 5
def func(a, b):
    raise Exception("This is a generic exception for testing purposes.")


def main():
    try:
        a = b = None
        func(a, b)
    except Exception as e:
        err(e)


main()


# EXAMPLE 6
msg("This is an Informational Message.", error_type=fmt.ErrorType.INFO)
msg("This is a Warning Message.", error_type=fmt.ErrorType.WARNING)
msg("This is an Error Message.", error_type=fmt.ErrorType.ERROR)
