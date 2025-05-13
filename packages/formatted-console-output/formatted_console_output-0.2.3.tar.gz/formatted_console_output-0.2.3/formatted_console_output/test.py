from formatted_console_output import (
    ForegroundColor,
    BackgroundColor,
    TextFormat,
    FormattedPhrase,
    output_formatted_message as print,
    output_many_format_message as printf,
)

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
