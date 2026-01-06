from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

def alpha_to_num(s):
    return [ord(c) for c in s if ' ' <= c <= '~']

def process_code(password, text):
    n_list = alpha_to_num(password)
    s_list = alpha_to_num(text)
    
    # Generate a pattern based on the password
    pattern = [n_list[i % len(n_list)] for i in range(len(s_list))]
    
    # Apply multiple rounds of transformations
    transformed = s_list.copy()
    for round in range(3):  # For example, 3 rounds
        for i in range(len(transformed)):
            if i % 3 == 0:
                transformed[i] = (transformed[i] + pattern[i] + round) % 256
            elif i % 3 == 1:
                transformed[i] = (transformed[i] - pattern[i] + round) % 256
            else:
                transformed[i] = (transformed[i] * pattern[i] + round) % 256

    # Generate C code with the same logic
    code = []
    code.append('#include<stdio.h>\n#include<string.h>\nint main(void) {\n')
    code.append('char str[100];\n')
    code.append('int i, len;\n')
    code.append('printf("Enter Password: ");\n')
    code.append('scanf("%s", str);\n')
    code.append('len = strlen(str);\n')
    
    # Recreate the pattern and operations in C
    code.append('int pattern[len];\n')
    code.append('for (i = 0; i < len; i++) {\n')
    code.append('    pattern[i] = /* logic to generate pattern based on password */;\n')
    code.append('}\n')
    
    # Apply the same operations in C
    code.append('int transformed[len];\n')
    code.append('for (i = 0; i < len; i++) {\n')
    code.append('    if (i %% 3 == 0) {\n')
    code.append('        transformed[i] = (transformed[i] + pattern[i] + round) %% 256;\n')
    code.append('    } else if (i %% 3 == 1) {\n')
    code.append('        transformed[i] = (transformed[i] - pattern[i] + round) %% 256;\n')
    code.append('    } else {\n')
    code.append('        transformed[i] = (transformed[i] * pattern[i] + round) %% 256;\n')
    code.append('    }\n')
    code.append('}\n')
    
    # Check if the transformed sequence matches the expected output
    # and print the original message if correct
    code.append('/* Check logic and print the original message if correct */\n')
    
    code.append('return 0;\n}\n')
    
    return ''.join(code)



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form["password"]
        message = request.form["message"]
        output = process_code(password, message)
        return render_template("result.html", output=output)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )


# if __name__ == "__main__":
#     app.run(debug=True)