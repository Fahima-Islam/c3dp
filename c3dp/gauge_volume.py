import numpy as np
from shapely.geometry import Polygon
from scipy.interpolate import griddata
import matplotlib.pyplot as mpl


def make_square(x, size):
	return [ [x, -size/2, size/2],
			 [x, size/2, size/2],
			 [x, -size/2, -size/2],
			 [x, size/2, -size/2]]


def theta_phi(Collimator_square, sample_point):
    p1,p2,p3,p4=Collimator_square
    pointsNum=sample_point.shape[0]
    points=np.array([p1-sample_point,p2-sample_point,p3-sample_point,p4-sample_point]).reshape(pointsNum,4,3)

    norm=np.array([np.linalg.norm(points, axis=2)]).reshape(pointsNum,4,1)


    point = points/norm

    theta = np.arccos(point[:,:,2])
    phi=np.arcsin(point[:,:,1]/np.sin(theta))

    return theta, phi


def gauge_volume(square_theta_phy_sample, square_theta_phy_detector):
	gauge_volume=[]
	theta_phiS = np.array([square_theta_phy_sample]).reshape(pointsNum, 4, 2).tolist()
	theta_phiD = np.array([square_theta_phy_detector]).reshape(pointsNum, 4, 2).tolist()
	for i in range(pointsNum):
		s=Polygon(theta_phiS[i]).area
		d=Polygon(theta_phiD[i]).area

		gauge_volume.append(s-d)
	return (gauge_volume)


def making_plot(sample_points_x_y, gauge_volume ):
    X,Y= np.meshgrid(xS,yS)


    Z = griddata((xS,yS), np.array(gauge_volume), (X,Y), method='nearest')

    plt.figure()
    r=plt.contourf(X, Y, Z)
    plt.clabel(r, inline=1, fontsize=20)
    plt.pcolormesh(X, Y, Z, cmap = plt.get_cmap('rainbow'))
    plt.colorbar()
    plt.scatter(xS,yS ,marker = 'o', c = 'b', s = 5, zorder = 10)

    plt.show()







