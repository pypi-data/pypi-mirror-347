from formatted_console_output import (
    ForegroundColor,
    BackgroundColor,
    TextFormat,
    output_formatted_message as print,
    output_many_format_message as printf,
)

message = {
    "The ": {"bg_color": BackgroundColor.BLACK, "fg_color": ForegroundColor.YELLOW},
    "quick brown foo ": {
        "bg_color": BackgroundColor.RED,
        "fg_color": ForegroundColor.YELLOW,
        "format": TextFormat.BOLD,
    },
    "jumped over the ": {
        "bg_color": BackgroundColor.BLACK,
        "fg_color": ForegroundColor.YELLOW,
    },
    "lazy ": {
        "bg_color": BackgroundColor.BLUE,
        "fg_color": ForegroundColor.YELLOW,
        "format": TextFormat.BOLD,
    },
    "bar": {
        "bg_color": BackgroundColor.BLUE,
        "fg_color": ForegroundColor.YELLOW,
        "format": TextFormat.BOLD_AND_UNDERLINE,
    },
}
printf(message, sep="  -  ", end="\n\n")
print()
