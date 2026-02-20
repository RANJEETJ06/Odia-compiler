def interpreter(ast,variables=None):
    if variables is None:
        variables = {}
    def evaluate_condition(cond):
        # 1. Handle Complex Logical Expressions (o / athaba)
        if "type" in cond and cond["type"] == "LogicalExpr":
            left_val = evaluate_condition(cond["left"])  # Recursive call
            right_val = evaluate_condition(cond["right"]) # Recursive call
        
            if cond["op"] == "o":      # and
                return left_val and right_val
            if cond["op"] == "athaba": # or
                return left_val or right_val

        # 2. Handle Simple Comparisons (x > 10)
        # Only access "l" if it's NOT a LogicalExpr
        v1 = clean(cond["l"])
        v2 = clean(cond["r"])
        op = cond["op"]
    
        if op == "==": return v1 == v2
        elif op == "!=": return v1 != v2
        elif op == ">":  return v1 > v2
        elif op == "<":  return v1 < v2
        elif op == ">=": return v1 >= v2
        elif op == "<=": return v1 <= v2
        return False
    
    def clean(val):
        if isinstance(val, str) and val in variables:
            val = variables[val]
    
        # NEW: Handle boolean strings stored in variables
        if val == "satya": return True
        if val == "mithya": return False
    
        if isinstance(val, str):
            if val.isdigit():
                print(f"Converting '{val}' to integer.")
                return int(val)
            # Handle negative numbers if needed
            if val.startswith('-') and val[1:].isdigit():
                return int(val)
        return val

    for node in ast:
        if node["type"] == "Declaration":
            variables[node["name"]] = node["value"]
        
        elif node["type"] == "Input":
            mode = node["mode"]
            var_name = node["name"]
            
            # 1. lekha (String Input)
            if mode == "lekha":
                variables[var_name] = input()
                
            # 2. gana (Number Input)
            elif mode == "gana":
                val = int(input())
                if val:
                    variables[var_name] = int(val)
                else:
                    raise ValueError(f"gana pani sankya darakar,kintu milichi '{val}'")

            # 3. pachara (Boolean Input)
            elif mode == "pachara":
                val = input().strip().lower()
                # Map user input back to satya/mithya logic
                if val == "satya":
                    variables[var_name] = True
                elif val == "mithya":
                    variables[var_name] = False
                else:
                    raise ValueError(f"pachara pani <satya/mithya> darakar,kintu milichi '{val}'")
        elif node["type"] == "Assignment":
            name = node["name"]
            e = node["expr"]
            v1 = clean(e["l"])
            v2 = clean(e["r"])
            op = e["op"]

            # Calculate the new value
            if op == "+": res = v1 + v2
            elif op == "-": res = v1 - v2
            elif op == "*": res = v1 * v2
            elif op == "/": res = v1 // v2
            elif op == "^": res = v1 ** v2
            elif op == None: res = v1
            
            # Update the variable in memory
            variables[name] = res

        elif node["type"] == "Print":
            e = node["expr"]
            v1 = clean(e["l"])
            v2 = clean(e["r"])
            op = e["op"]
            
            res = None
            if op == "+": 
                if isinstance(v1, int) and isinstance(v2, int): res = v1 + v2
                else: res = str(v1) + str(v2)
            elif op == "-": res = v1 - v2 if isinstance(v1, int) and isinstance(v2, int) else "Error"
            elif op == "*": res = v1 * v2 if isinstance(v1, int) and isinstance(v2, int) else "Error"
            elif op == "/": res = v1 // v2 if v2 != 0 else "0 bhaga error"
            elif op == "^": res = v1 ** v2 if isinstance(v1, int) and isinstance(v2, int) else "Error"
            elif op == "==": res = (v1 == v2)
            elif op == "!=": res = (v1 != v2)
            elif op == ">": res = (v1 > v2)
            elif op == "<": res = (v1 < v2)
            elif op == ">=": res = (v1 >= v2)
            elif op == "<=": res = (v1 <= v2)
            elif op == ",": res = f"{v1}{v2}"
            elif op == None: res = v1
            
            # Use "in" or simple equality to catch both Python booleans and your custom strings
            if res is True or res == "satya": 
                print("satya")
            elif res is False or res == "mithya": 
                print("mithya")
            elif res is not None: 
                print(res)
        elif node["type"] == "IfChain":
            if evaluate_condition(node["if_block"]["condition"]):
                interpreter(node["if_block"]["body"],variables)
            else:
                executed = False
                for el_node in node["elif_blocks"]:
                    if evaluate_condition(el_node["condition"]):
                        interpreter(el_node["body"],variables)
                        executed = True
                        break
                if not executed and node["else_body"]:
                    interpreter(node["else_body"],variables)
        # interpreter.py
        elif node["type"] == "TypeCheck":
            item = node["name"]
            val = clean(item)
            if isinstance(val, bool):
                type_name = "Boolean (Satya/Mithya)"
            elif isinstance(val, int):
                type_name = "Anka (Number)"
            elif isinstance(val, str):
                type_name = "Sabda (String)"
            else:
                type_name = "Unknown"

            if isinstance(val, (int,bool,str)) :
                print(f"Variable '{item}' ra type heuchi: {type_name}")
            else:
                print(f"Literal value '{item}' ra type heuchi: {type_name}")
