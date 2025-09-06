# 简化print
def p(ob):
    print(ob)


# 用于在JupyterLab中打印-----------------，用以区分
def l(ob="", len_dash=40):
    s = "-" * len_dash
    print(f'{s}{ob}{s}')
