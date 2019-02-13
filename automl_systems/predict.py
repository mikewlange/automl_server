import os
import pickle

import numpy
import sklearn

from autokeras.utils import pickle_from_file
from sklearn.metrics import confusion_matrix

from automl_server.settings import AUTO_ML_DATA_PATH
from automl_systems.shared import load_ml_data, reformat_data


def predict(conf):
    try:
        if conf.model.framework == 'auto_sklearn' or conf.model.framework == 'tpot':
            with open(conf.model.model_path.replace(':', '_'), 'rb') as f:
                my_model = pickle.load(f)

            x = numpy.load(os.path.join(AUTO_ML_DATA_PATH, conf.model.validation_data_filename.replace(':', '_')))
            y = numpy.load(os.path.join(AUTO_ML_DATA_PATH, conf.model.validation_labels_filename.replace(':', '_')))

            if conf.model.preprocessing_object.input_data_type == 'png':
                x = reformat_data(x)

        elif conf.model.framework == 'auto_keras':
            my_model = pickle_from_file(conf.model.model_path.replace(':', '_'))
            x, y = load_ml_data(conf.model.validation_data_filename, conf.model.validation_labels_filename, False, conf.model.label_one_hot_encoding_binary)
        else:
            print('notimpl (epic fail)')

        y_pred = my_model.predict(x)

        if conf.scoring_strategy == 'accuracy':
            score=sklearn.metrics.accuracy_score(y, y_pred)
        elif(conf.scoring_strategy == 'precision'):
            score=sklearn.metrics.average_precision_score(y, y_pred)
        elif(conf.scoring_strategy == 'roc_auc'):
            score=sklearn.metrics.roc_auc_score(y, y_pred)
        else:
            score = 0
            print('epic fail! no Strat applied')

        print(numpy.unique((y)))

        cnf_matrix = confusion_matrix(y, y_pred)

        target_names = []
        if len(numpy.unique(y)) == 2:
            target_names = numpy.unique(y)
        else:
            for y in numpy.unique(y):
                target_names.append(y.replace('_behavior', '').replace('_rod(0.5mm)', '').replace('_condition', '').replace('_element', '').replace('force_', ''))

        plot_confusion_matrix(conf=conf,cm=cnf_matrix,
                              normalize=False,
                              target_names=target_names,
                              title="Confusion Matrix")

        conf.status = 'success'
        conf.score = str(round(score,4))
        conf.save()

    except Exception as e:
        conf.status = 'fail'
        conf.additional_remarks = e
        conf.save()

def plot_confusion_matrix(conf, cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(13, 11))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.gcf().subplots_adjust(left=0.1, bottom=0.2)
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()
    plt.savefig('plots/' + conf.model.framework + '_' + ( conf.model.preprocessing_object.input_data_type if conf.model.preprocessing_object else '') + '_' + conf.model.task_type + '_' + conf.model.training_time + ('_normalized' if normalize==True else '') +'.jpg')
