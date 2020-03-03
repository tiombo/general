import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures

    
def plot_classifier(X_train, y_train, classifier, order=1, grid=100, xlabel=r"$x_1$", ylabel=r"$x_2$"):
    """
    Affichage des résultats de classification
    
    REMARQUE IMPORTANTE: le code ci-dessous a été écrit à l'arrache et n'est absolument pas un modèle de beau code...
    """
    
    # Create polynomial features
    if classifier.__class__.__name__ == "LogisticRegression":
        poly = PolynomialFeatures(order)
        X = poly.fit_transform(X_train)
        scaler = StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)
    else:
        X = X_train
    
    if classifier.__class__.__name__ == "KNeighborsClassifier":
        a = 0
        b = 1
    else:
        a = 1
        b = 2
    
    f, axes = plt.subplots(1,2)
    xx = np.linspace(X[:,a].min(), X[:,a].max(), grid)
    yy = np.linspace(X[:,b].min(), X[:,b].max(), grid)
    XX, YY = np.meshgrid(xx,yy)
    
    axes[0].set_xlim(X[:,a].min(),X[:,a].max())
    axes[0].set_ylim(X[:,b].min(),X[:,b].max())
    
    if classifier.__class__.__name__ == "KNeighborsClassifier":
        vec = np.c_[XX.ravel(), YY.ravel()]
    elif classifier.__class__.__name__ == "LogisticRegression":
        vec = poly.fit_transform(np.c_[XX.ravel(), YY.ravel()])
    else:
        raise Exception()
        
    z = classifier.predict_proba(vec)[:, 1]
    z = z.reshape(XX.shape)
    
    sns.scatterplot(x=X[:,a], y=X[:,b], hue=y_train.ravel(), ax=axes[0], s=50)
    CS = axes[0].contour(XX,YY,z,[0.5], colors=["g"])
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel(ylabel)
    
    labels = ['Frontière de décision']
    for i in range(len(labels)):
        CS.collections[i].set_label(labels[i])
    axes[0].legend(loc='lower left')
    
    CS2 = axes[1].contourf(XX, YY, z, 100, cmap="inferno")
    CS = axes[1].contour(XX,YY,z,[0.5], colors=["w"])
    