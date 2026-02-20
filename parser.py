def get_block(tokens):
    """Helper to collect tokens inside { } while handling nested brackets."""
    block = []
    balance = 1
    tokens.pop(0) # skip the initial '{'
    
    while tokens and balance > 0:
        t = tokens.pop(0)
        if t["value"] == "{": balance += 1
        if t["value"] == "}": balance -= 1
        
        if balance > 0: # Don't include the final closing '}'
            block.append(t)
    return block

def parse_condition(tokens):
    # Get initial comparison (e.g., x > 5)
    l = tokens.pop(0)["value"]
    op = tokens.pop(0)["value"]
    
    r_token = tokens.pop(0)
    r = r_token["value"]

    if r_token["type"] == "number":
        r = int(r)
    elif r == "satya":
        r = True
    elif r == "mithya":
        r = False

    node = {"l": l, "op": op, "r": r}

    # If the next token is 'o' or 'athaba', wrap this in a LogicalExpr
    if tokens and tokens[0]["value"] in ["o", "athaba"]:
        logic_op = tokens.pop(0)["value"]
        right_side = parse_condition(tokens) # Recursive call for chaining
        return {
            "type": "LogicalExpr",
            "left": node,
            "op": logic_op,
            "right": right_side
        }
    return node

def parser(tokens):
    ast = []
    while tokens:
        token = tokens.pop(0)
        try:
            if token["value"] == "bhai":
                name = tokens.pop(0)["value"]
                tokens.pop(0) # skip =
                val_token = tokens.pop(0)
                val = val_token["value"]
                ast.append({"type": "Declaration", "name": name, "value": val})
            
            # parser.py
            elif token["value"] == "parikhya":
                # Usage: parikhya salary
                target_var = tokens.pop(0)["value"]
                ast.append({
                    "type": "TypeCheck",
                    "name": target_var
                })
            
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
            elif token["value"] == "jadi":
                # 1. Condition
                condition = parse_condition(tokens)
                if_body_tokens = get_block(tokens)
    
                # 3. Handle 'nahale' (elif)
                elif_blocks = []
                while tokens and tokens[0]["value"] == "nahale":
                    tokens.pop(0) # skip 'nahale'
                    # Check if it's an 'else if' or just 'else'
                    # In your logic: nahale + condition + { body }
                    el_condition = parse_condition(tokens)
                    el_body_tokens = get_block(tokens)
        
                    # tokens.pop(0) # skip '{'

                    elif_blocks.append({"condition": el_condition, "body": parser(el_body_tokens)})

                # 4. Handle 'sesa' (else)
                else_body_nodes = []
                if tokens and tokens[0]["value"] == "sesa":
                    tokens.pop(0) # skip 'sesa'
                    else_body_tokens = get_block(tokens)
                    else_body_nodes = parser(else_body_tokens)

                ast.append({
                    "type": "IfChain",
                    "if_block": {"condition": condition, "body": parser(if_body_tokens)},
                    "elif_blocks": elif_blocks,
                    "else_body": else_body_nodes
                })
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
