from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your alpha_to_num + process_code functions (same as before) ...
# Function: your encryption logic
def alpha_to_num(s):
    lis = []
    for letter in s:
        if ' ' <= letter <= '~':
            lis.append(ord(letter))
    return lis

def process_code(password, text):
    n_list = alpha_to_num(password)
    s_list = alpha_to_num(text)
    flag=0
    km=1407
    for i in range(0,len(n_list)):
        if(flag==0):
            km=km+n_list[i]
            flag=1
        else:
            km=km-n_list[i]
            flag=0
    nx = 0
    sx = 0
    ns = []
    op = 0
    while sx < len(s_list) and nx <= len(n_list):
        nx = nx % len(n_list)
        if op < 2:
            t = s_list[sx] - n_list[nx]
            op = op + 1
        else:
            t = s_list[sx] + n_list[nx]
            op = 0
        ns.append(t)
        nx = nx + 1
        sx = sx + 1

    # Generate C program output
    code = []
    code.append("//output generated")
    code.append('#include<stdio.h>\n#include<conio.h>\n#include<string.h>\nint main(void)\n{')
    code.append("char str[100];")
    code.append("int flag=0,sum=1407;")
    code.append("int a[100];")
    code.append("int i, len;")
    '''code.append("clrscr();")'''
    code.append('printf("Enter a Password: ");')
    code.append('scanf("%s",str);')
    code.append("len = strlen(str);")
    code.append("for (i = 0; i < len; i++)\n{")
    code.append("a[i] = (int)str[i];")
    code.append("if(flag==0)")
    code.append("{")
    code.append("sum=sum+a[i];")
    code.append("flag=1;")
    code.append("}")
    code.append("else")
    code.append("{")
    code.append("sum=sum-a[i];")
    code.append("flag=0;")
    code.append("}")
    code.append("}")
    code.append(f"if(sum=={km})")
    f_code="\n".join(code)
    code = []




    # Print encrypted message
    code.append('\nprintf("')
    code.append("%c" * len(ns))
    code_line = '"'
    nx = 0
    sx = 0
    op = 0
    while sx < len(ns) and nx <= len(n_list):
        nx = nx % len(n_list)
        if op < 2:
            code_line += f", {ns[sx]}+a[{nx}]"
            op = op + 1
        else:
            code_line += f", {ns[sx]}-a[{nx}]"
            op = 0
        nx = nx + 1
        sx = sx + 1
    code.append(code_line + ");\n")
    code.append("else\n")
    code.append('printf("Wrong password");\n')
    code.append("getch();\n")
    code.append("return 0;\n}")

    return f_code + "".join(code)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        password = request.form["password"]
        message = request.form["message"]
        output = process_code(password, message)
        return render_template("result3.html", output=output)
    return render_template("index6.html")

if __name__ == "__main__":
    app.run(debug=True)