from sympy import *
from IPython.display import display, Latex
import control.matlab as ml


def printer(var_name, var_value, unit):
     return display(Latex("${name} = {var:.4f}\ {unit}$".format(var=var_value,name=var_name,unit=unit)))

# Approximation for Eckfreq for PT1 TF #
def find_eckfreq_PT1(mag,omega):
    index = 0

    for i in ml.mag2db(mag):
        if i <= (max(ml.mag2db(mag))-3):
            display(Latex(f"""$$\\text{{at index: }} {index}$$
                                $$\\text{{mag is: }} {ml.mag2db(mag[index])}\ dB$$
                                $$\\text{{freq is: }} {omega[index]}\ Hz$$"""))
            break
        index+=1
    return index, ml.mag2db(mag[index]), omega[index]


# Approximation for Eckfreq for PT2 TF #
def find_eckfreq_PT2(tf):
    eck = sqrt(tf.pole()[1]*tf.pole()[0]).evalf()
    return display(Latex("$\\omega_0 = {eck:.4f}\ 1/s$".format(eck=eck)))

# Analyzes TF and gets Eckfreq D and K parameters #
def analyze_tf(tf):
    den = tf.den[0][0]
    num = tf.num[0][0]
    if len(den) == 3:
        type_ = "PT2"
        if den[0] == 1:
            omega_calc = sqrt(den[2])
            daempfung = den[1]/(omega_calc*2)
        else:
            vorfaktor = den[0]
            omega_calc = sqrt(den[2]/vorfaktor)
            daempfung = den[1]/(omega_calc*2)
        if len(num) == 1:
            K = num[0]/omega_calc**2
        return omega_calc, K, daempfung

    if len(den) == 2:
        type_ = "PT1"
        daempfung = None
        if den[1] == 1:
            omega_calc = 1/(den[0])
        else:
            vorfaktor = den[1]
            omega_calc = 1/(den[1]/vorfaktor)
        if len(num) == 1:
            K = num[0]
        return omega_calc, K
    # printer("\\omega_0", omega_calc, "1/s")
    # return {
    #         type_:
    #             {
    #                 "omega_0":omega_calc,
    #                 "D":daempfung,
    #                 "K":K
    #             }
    #         }
