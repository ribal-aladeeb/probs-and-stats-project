import numpy as np
from numpy.polynomial.polynomial import polyfit


js = [j+1 for j in range(0, len(plug_gpa_list_here))]
prob_dis = [(j-0.5) / (len(js)) for j in js]
plt.scatter(plug_gpa_list_here, prob_dis, s=7, alpha=0.5)
plt.show
plt.figure()


b, m = polyfit(plug_gpa_list_here, prob_dis, 1)
plt.plot(plug_gpa_list_here, prob_dis)
plt.plot(plug_gpa_list_here, b + m * plug_gpa_list_here, '-')
plt.show()