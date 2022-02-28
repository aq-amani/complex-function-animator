import numpy as np
import mpmath
import threading
mpmath.dps = 5

#f = lambda z: mpmath.zeta(z)

def f(z):
    try:
        out = mpmath.zeta(z)
        out = mpmath.chop(out)
        #re,imag = out.real, out.imag
        re,imag = mpmath.polar(out)
        if imag < 0:
            imag += 2*(np.pi)
    except (ValueError, TypeError, ZeroDivisionError):
        out= re = imag = np.nan
    return re, imag

#complex_array = np.frompyfunc(complex, 2, 1)

def thread_target(start_x, end_x, start_y, end_y):
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            W_r[x,y], W_i[x,y] = f(Z[x,y])

X = np.arange(-2, 2, 0.5)
Y = np.arange(-4, 4, 0.5)

print(X,'\n')
print(Y, '\n')
X, Y = np.meshgrid(X, Y)
#print('after mesh')
#print(X,'\n')
#print(Y, '\n')
Z = X + (Y*1j)
#Z = complex_array(X, Y)
print('Z is')
print(Z,'\n')
print(Z.shape)

W_r = np.zeros(Z.shape)
W_i = np.zeros(Z.shape)

x,y = Z.shape
x_ranges = np.arange(0, x+1, x/4, dtype = int)
y_ranges = np.arange(0, y+1, y/4, dtype = int)
print('X ranges', x_ranges)
print('Y ranges', y_ranges)

t1 = threading.Thread(target=thread_target, args=(x_ranges[0],x_ranges[2],y_ranges[0],y_ranges[1],))
t2 = threading.Thread(target=thread_target, args=(x_ranges[0],x_ranges[2],y_ranges[1],y_ranges[2],))
t3 = threading.Thread(target=thread_target, args=(x_ranges[0],x_ranges[2],y_ranges[2],y_ranges[3],))
t4 = threading.Thread(target=thread_target, args=(x_ranges[0],x_ranges[2],y_ranges[3],y_ranges[4],))

t5 = threading.Thread(target=thread_target, args=(x_ranges[2],x_ranges[4],y_ranges[0],y_ranges[1],))
t6 = threading.Thread(target=thread_target, args=(x_ranges[2],x_ranges[4],y_ranges[1],y_ranges[2],))
t7 = threading.Thread(target=thread_target, args=(x_ranges[2],x_ranges[4],y_ranges[2],y_ranges[3],))
t8 = threading.Thread(target=thread_target, args=(x_ranges[2],x_ranges[4],y_ranges[3],y_ranges[4],))

t1.start()
t2.start()
t3.start()
t4.start()

t5.start()
t6.start()
t7.start()
t8.start()

t1.join()
t2.join()
t3.join()
t4.join()

t5.join()
t6.join()
t7.join()
t8.join()
#for i in range(x):
#    for j in range(y):
#        print(f(Z[i,j]))
#f_array = np.frompyfunc(f, 1, 2)

print('W_r is\n', W_r)
print('W_i is\n', W_i)
print(W_r.shape, W_i.shape)


#with open('./W_r.npy', 'wb') as fr:
#    np.save(fr, W_r)
#
#with open('./W_i.npy', 'wb') as fi:
#    np.save(fi, W_i)

with open('./W_r.npy', 'rb') as fr:
    K_r = np.load(fr)
with open('./W_i.npy', 'rb') as fi:
    K_i = np.load(fi)

#W_r, W_i = f_array(Z)
#print(W_r)
#x, y = W.shape
#K_r = np.zeros(Z.shape)
#K_i = np.zeros(Z.shape)
#print('K other way\n')
#for i in range(x):
#    for j in range(y):
#        K_r[i,j], K_i[i,j] = f(Z[i, j])
#print(K_r)
#print('\n',K_i)

#xn, yn = X.shape
#W_r = X*0
#W_i = X*0
#for xk in range(xn):
#    for yk in range(yn):
#        try:
#            z = complex(X[xk,yk],Y[xk,yk])
#            w = mpmath.chop(f(z))
#            if w != w:
#                raise ValueError
#            #W_r[xk,yk] = float(w.real)
#            #W_i[xk,yk] = float(w.imag)
#            #W_r[xk,yk] = mpmath.chop(w.real)
#            #W_i[xk,yk] = mpmath.chop(w.imag)
#            W_r[xk,yk], W_i[xk,yk] = mpmath.polar(w)
#            #W_i[xk,yk] = mpmath.chop(W_i[xk,yk])
#            if W_i[xk,yk] < 0:
#                W_i[xk,yk] += 2*(np.pi)
#            #W_i[xk,yk] = mpmath.cos(W_i[xk,yk])
#            #print(Y[xk,yk])
#            #print(W_r[xk,yk], W_i[xk,yk])
#        except (ValueError, TypeError, ZeroDivisionError):
#            # can handle special values here
#            pass
#    #print(xk, xn)
