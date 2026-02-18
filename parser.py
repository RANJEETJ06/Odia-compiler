def parser(tokens):
    ast = []
    while tokens:
        token = tokens.pop(0)
        try:
            if token["value"] == "bhai":
                name = tokens.pop(0)["value"]
                tokens.pop(0) # skip =
                val = tokens.pop(0)["value"]
                ast.append({"type": "Declaration", "name": name, "value": val})
            
            elif token["value"] in ["gana", "lekha","pachara"]:
                # The command should be followed by a variable name: "gana x"
                target_var = tokens.pop(0)["value"]
                ast.append({
                    "type": "Input",
                    "mode": token["value"], # gana or lekha or pachara
                    "name": target_var
                })             
            elif token["value"] == "kuha":
                # Get Left side (v1)
                l = tokens.pop(0)["value"]
                
                # Check if there is an operator (like ^, +, ==)
                if tokens and tokens[0]["type"] in ["operator", "unknown"]:
                    op = tokens.pop(0)["value"]
                    # Get Right side (v2)
                    r = tokens.pop(0)["value"]
                    ast.append({"type": "Print", "expr": {"l": l, "op": op, "r": r}})
                else:
                    # Case for single value: kuha x
                    ast.append({"type": "Print", "expr": {"l": l, "op": None, "r": None}})
            # ... existing bhai, gana, kuha blocks ...

            elif token["type"] == "identifier":
                # Handle Assignment: x = x + 5
                name = token["value"]
                tokens.pop(0)  # skip '='
                
                # Get expression parts
                l = tokens.pop(0)["value"]
                if tokens and tokens[0]["type"] == "operator":
                    op = tokens.pop(0)["value"]
                    r = tokens.pop(0)["value"]
                    ast.append({"type": "Assignment", "name": name, "expr": {"l": l, "op": op, "r": r}})
                else:
                    ast.append({"type": "Assignment", "name": name, "expr": {"l": l, "op": None, "r": None}})

            else:
                print(f"Syntax Error: '{token['value']}' bhul achhi at Line {token['line']}")
                return None
        except IndexError:
            print("Syntax Error: Code adha achhi")
            return None
    return ast
