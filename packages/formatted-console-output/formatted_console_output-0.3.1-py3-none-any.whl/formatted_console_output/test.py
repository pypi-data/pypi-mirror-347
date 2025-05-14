from formatted_console_output import *
from formatted_console_output import (
    output_formatted_message as print,
    output_many_format_message as printf,
)

print(
    "The quick brown foo jumped over the lazy bar",
    fg_color=ForegroundColor.YELLOW,
    bg_color=CustomColor(r=156, g=101, b=0, is_fg=False),
)
