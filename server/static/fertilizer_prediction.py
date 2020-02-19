from keras.models import load_model
import numpy as np
def fertilizer_prediction(_test):
    # model=load_model('D:\\Documents\\Projects\\AppDevelopment\\SIH\\Server\\server\\static\\ml\\fert_pred\\model.h5')
    model=load_model('model.h5')
    test = np.asarray(_test)
    test = test.reshape(1,9)
    prediction = model.predict_classes(test)
    return prediction