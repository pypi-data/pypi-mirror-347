from formatted_console_output import (
    ForegroundColor,
    BackgroundColor,
    TextFormat,
    FormattedPhrase,
    output_formatted_message as print,
    output_many_format_message as printf,
)

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
