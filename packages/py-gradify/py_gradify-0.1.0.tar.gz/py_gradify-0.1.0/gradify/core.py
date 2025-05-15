def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" 
def reset_color():
    return "\033[0m"
def interpolate_color(start, end, factor):
    return tuple(
        int(start[i] + (end[i] - start[i]) * factor) for i in range(3)
    )
def gradify(text, start_color, end_color, direction="horizontal"):
    if direction not in ["horizontal", "vertical"]:
        raise ValueError("Direction must be 'horizontal' or 'vertical'.")
    lines = text.splitlines()
    output_lines = []
    if direction == "horizontal":
        for line in lines:
            length = len(line)
            output = ""
            for i, char in enumerate(line):
                factor = i / max(length - 1, 1)
                r, g, b = interpolate_color(start_color, end_color, factor)
                output += f"{rgb_to_ansi(r, g, b)}{char}"
            output += reset_color()
            output_lines.append(output)
    elif direction == "vertical":
        total_lines = len(lines)
        for i, line in enumerate(lines):
            factor = i / max(total_lines - 1, 1)
            r, g, b = interpolate_color(start_color, end_color, factor)
            output_lines.append(f"{rgb_to_ansi(r, g, b)}{line}{reset_color()}")
    return "\n".join(output_lines)