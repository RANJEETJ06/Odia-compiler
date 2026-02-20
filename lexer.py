from constant import const_tokens
def lexer(input_str):
    tokens = []
    cursor, line, column = 0, 1, 1
    length = len(input_str)

    while cursor < length:
        char = input_str[cursor]

        if char == "\n":
            line += 1; column = 1; cursor += 1
            continue
        if char.isspace():
            cursor += 1; column += 1
            continue
        if char in ["'", '"']:
            quote_type = char
            string_val = ""
            start_col = column
            cursor += 1; column += 1 # skip start quote
            while cursor < length and input_str[cursor] != quote_type:
                string_val += input_str[cursor]
                cursor += 1; column += 1
            cursor += 1; column += 1 # skip end quote
            tokens.append({"type": "string", "value": string_val, "line": line, "column": start_col})
            continue
        
        if char.isalpha() or char == "_":
            word = ""; start_col = column
            while cursor < length and (input_str[cursor].isalnum() or input_str[cursor] == "_"):
                word += input_str[cursor]
                cursor += 1; column += 1
            
            # Identify specific boolean keywords
            if word in ["satya", "mithya"]:
                type_ = "boolean"
                value = True if word == "satya" else False
            elif word in const_tokens:
                type_ = "keyword"
                value = word
            else:
                type_ = "identifier"
                value = word
                
            tokens.append({"type": type_, "value": value, "line": line, "column": start_col})
            continue

        if char.isdigit():
            num = ""; start_col = column
            while cursor < length and input_str[cursor].isdigit():
                num += input_str[cursor]
                cursor += 1; column += 1
            tokens.append({"type": "number", "value": int(num), "line": line, "column": start_col})
            continue

        # ADDED '^' to this list
        if char in "=./*+-<>!,^{}":
            start_col = column
            full_op = char
            if cursor + 1 < length:
                next_char = input_str[cursor + 1]
                if (char + next_char) in ["==", ">=", "<=", "!="]:
                    full_op = char + next_char
                    cursor += 1 # Skip the extra character
                    column += 1
                    
            tokens.append({"type": "operator", "value": full_op, "line": line, "column": start_col})
            cursor += 1; column += 1
            continue

        tokens.append({"type": "unknown", "value": char, "line": line, "column": column})
        cursor += 1; column += 1
    return tokens
