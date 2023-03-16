import math
import os
import random
import re
import sys

my_readings = ['1/3/2012 16:00:00	26.96', \
'1/4/2012 16:00:00	27.47', \
'1/5/2012 16:00:00	27.728', \
'1/6/2012 16:00:00	28.19', \
'1/9/2012 16:00:00	28.1', \
'1/10/2012 16:00:00	28.15', \
'1/11/2012 16:00:00	27.98', \
'1/12/2012 16:00:00	28.02', \
'1/13/2012 16:00:00	28.25', \
'1/17/2012 16:00:00	28.65', \
'1/18/2012 16:00:00	28.4', \
'1/19/2012 16:00:00	28.435', \
'1/20/2012 16:00:00	29.74', \
'1/23/2012 16:00:00	29.95', \
'1/24/2012 16:00:00	29.5703', \
'1/25/2012 16:00:00	29.65', \
'1/26/2012 16:00:00	29.7', \
'1/27/2012 16:00:00	29.53', \
'1/30/2012 16:00:00	29.62', \
'1/31/2012 16:00:00	29.7', \
'2/1/2012 16:00:00	30.05', \
'2/2/2012 16:00:00	30.17', \
'2/3/2012 16:00:00	30.4', \
'2/6/2012 16:00:00	30.22', \
'2/7/2012 16:00:00	30.485', \
'2/8/2012 16:00:00	30.67', \
'2/9/2012 16:00:00	30.8', \
'2/10/2012 16:00:00	30.8', \
'2/13/2012 16:00:00	30.77', \
'2/14/2012 16:00:00	30.46', \
'2/15/2012 16:00:00	30.39', \
'2/16/2012 16:00:00	31.55', \
'2/17/2012 16:00:00	31.32', \
'2/21/2012 16:00:00	31.61', \
'2/22/2012 16:00:00	31.68', \
'2/23/2012 16:00:00	31.59', \
'2/24/2012 16:00:00	31.5', \
'2/27/2012 16:00:00	31.5', \
'2/28/2012 16:00:00	31.93', \
'2/29/2012 16:00:00	32', \
'3/1/2012 16:00:00	32.39', \
'3/2/2012 16:00:00	32.44', \
'3/5/2012 16:00:00	32.05', \
'3/6/2012 16:00:00	31.98', \
'3/7/2012 16:00:00	31.92', \
'3/8/2012 16:00:00	32.21', \
'3/9/2012 16:00:00	32.16', \
'3/12/2012 16:00:00	32.2', \
'3/13/2012 16:00:00	Missing_1', \
'3/14/2012 16:00:00	32.88', \
'3/15/2012 16:00:00	32.94', \
'3/16/2012 16:00:00	32.95', \
'3/19/2012 16:00:00	32.61', \
'3/20/2012 16:00:00	32.15', \
'3/21/2012 16:00:00	Missing_2', \
'3/22/2012 16:00:00	32.09', \
'3/23/2012 16:00:00	32.11', \
'3/26/2012 16:00:00	Missing_3', \
'3/27/2012 16:00:00	32.7', \
'3/28/2012 16:00:00	32.7', \
'3/29/2012 16:00:00	32.19', \
'3/30/2012 16:00:00	32.41', \
'4/2/2012 16:00:00	32.46', \
'4/3/2012 16:00:00	32.19', \
'4/4/2012 16:00:00	31.69', \
'4/5/2012 16:00:00	31.63', \
'4/9/2012 16:00:00	31.4', \
'4/10/2012 16:00:00	31.19', \
'4/11/2012 16:00:00	30.53', \
'4/12/2012 16:00:00	31.04', \
'4/13/2012 16:00:00	31.16', \
'4/16/2012 16:00:00	31.19', \
'4/17/2012 16:00:00	31.61', \
'4/18/2012 16:00:00	31.31', \
'4/19/2012 16:00:00	31.68', \
'4/20/2012 16:00:00	32.89', \
'4/23/2012 16:00:00	32.5', \
'4/24/2012 16:00:00	32.52', \
'4/25/2012 16:00:00	32.32', \
'4/26/2012 16:00:00	32.23', \
'4/27/2012 16:00:00	32.22', \
'4/30/2012 16:00:00	32.11', \
'5/1/2012 16:00:00	32.335', \
'5/2/2012 16:00:00	31.925', \
'5/3/2012 16:00:00	31.9', \
'5/4/2012 16:00:00	31.57', \
'5/7/2012 16:00:00	30.86', \
'5/8/2012 16:00:00	30.78', \
'5/9/2012 16:00:00	30.83', \
'5/10/2012 16:00:00	31.02', \
'5/11/2012 16:00:00	31.54', \
'5/14/2012 16:00:00	31.04', \
'5/15/2012 16:00:00	30.795', \
'5/16/2012 16:00:00	30.32', \
'5/17/2012 16:00:00	30.2084', \
'5/18/2012 16:00:00	29.81', \
'5/21/2012 16:00:00	29.79', \
'5/22/2012 16:00:00	29.88', \
'5/23/2012 16:00:00	29.4', \
'5/24/2012 16:00:00	Missing_4', \
'5/25/2012 16:00:00	29.36', \
'5/29/2012 16:00:00	29.72', \
'5/30/2012 16:00:00	29.479', \
'5/31/2012 16:00:00	29.42', \
'6/1/2012 16:00:00	Missing_5', \
'6/4/2012 16:00:00	Missing_6', \
'6/5/2012 16:00:00	28.75', \
'6/6/2012 16:00:00	29.37', \
'6/7/2012 16:00:00	29.7', \
'6/8/2012 16:00:00	29.68', \
'6/11/2012 16:00:00	29.81', \
'6/12/2012 16:00:00	29.3', \
'6/13/2012 16:00:00	29.44', \
'6/14/2012 16:00:00	29.46', \
'6/15/2012 16:00:00	30.08', \
'6/18/2012 16:00:00	30.03', \
'6/19/2012 16:00:00	31.11', \
'6/20/2012 16:00:00	31.05', \
'6/21/2012 16:00:00	31.14', \
'6/22/2012 16:00:00	30.73', \
'6/25/2012 16:00:00	30.32', \
'6/26/2012 16:00:00	30.27', \
'6/27/2012 16:00:00	30.5', \
'6/28/2012 16:00:00	30.05', \
'6/29/2012 16:00:00	30.69', \
'7/2/2012 16:00:00	30.62', \
'7/3/2012 16:00:00	30.76', \
'7/5/2012 16:00:00	30.78', \
'7/6/2012 16:00:00	30.7', \
'7/9/2012 16:00:00	30.23', \
'7/10/2012 16:00:00	30.22', \
'7/11/2012 16:00:00	29.735', \
'7/12/2012 16:00:00	29.18', \
'7/13/2012 16:00:00	29.48', \
'7/16/2012 16:00:00	29.53', \
'7/17/2012 16:00:00	29.86', \
'7/18/2012 16:00:00	30.45', \
'7/19/2012 16:00:00	30.8', \
'7/20/2012 16:00:00	Missing_7', \
'7/23/2012 16:00:00	Missing_8', \
'7/24/2012 16:00:00	29.36', \
'7/25/2012 16:00:00	29.33', \
'7/26/2012 16:00:00	Missing_9', \
'7/27/2012 16:00:00	29.85', \
'7/30/2012 16:00:00	29.82', \
'7/31/2012 16:00:00	29.71', \
'8/1/2012 16:00:00	29.65', \
'8/2/2012 16:00:00	29.525', \
'8/3/2012 16:00:00	29.94', \
'8/6/2012 16:00:00	30.11', \
'8/7/2012 16:00:00	30.35', \
'8/8/2012 16:00:00	30.47', \
'8/9/2012 16:00:00	30.65', \
'8/10/2012 16:00:00	30.62', \
'8/13/2012 16:00:00	30.46', \
'8/14/2012 16:00:00	30.39', \
'8/15/2012 16:00:00	30.28', \
'8/16/2012 16:00:00	30.94', \
'8/17/2012 16:00:00	30.92', \
'8/20/2012 16:00:00	30.85', \
'8/21/2012 16:00:00	30.96', \
'8/22/2012 16:00:00	30.76', \
'8/23/2012 16:00:00	30.4', \
'8/24/2012 16:00:00	30.63', \
'8/27/2012 16:00:00	30.96', \
'8/28/2012 16:00:00	30.8', \
'8/29/2012 16:00:00	30.75', \
'8/30/2012 16:00:00	30.61', \
'8/31/2012 16:00:00	30.96', \
'9/4/2012 16:00:00	30.66', \
'9/5/2012 16:00:00	30.53', \
'9/6/2012 16:00:00	31.36', \
'9/7/2012 16:00:00	31.07', \
'9/10/2012 16:00:00	Missing_10', \
'9/11/2012 16:00:00	30.91', \
'9/12/2012 16:00:00	31.18', \
'9/13/2012 16:00:00	31.18', \
'9/14/2012 16:00:00	31.25', \
'9/17/2012 16:00:00	Missing_11', \
'9/18/2012 16:00:00	31.21', \
'9/19/2012 16:00:00	31.19', \
'9/20/2012 16:00:00	Missing_12', \
'9/21/2012 16:00:00	31.61', \
'9/24/2012 16:00:00	31.07', \
'9/25/2012 16:00:00	31', \
'9/26/2012 16:00:00	30.6', \
'9/27/2012 16:00:00	30.4', \
'9/28/2012 16:00:00	30.26', \
'10/1/2012 16:00:00	29.98', \
'10/2/2012 16:00:00	29.89', \
'10/3/2012 16:00:00	29.99', \
'10/4/2012 16:00:00	30.03', \
'10/5/2012 16:00:00	30.25', \
'10/8/2012 16:00:00	29.92', \
'10/9/2012 16:00:00	Missing_13', \
'10/10/2012 16:00:00	Missing_14', \
'10/11/2012 16:00:00	29.25', \
'10/12/2012 16:00:00	29.32', \
'10/15/2012 16:00:00	Missing_15', \
'10/16/2012 16:00:00	29.74', \
'10/17/2012 16:00:00	29.64', \
'10/18/2012 16:00:00	29.73', \
'10/19/2012 16:00:00	29.08', \
'10/22/2012 16:00:00	28.83', \
'10/23/2012 16:00:00	28.2', \
'10/24/2012 16:00:00	28.2', \
'10/25/2012 16:00:00	28.2', \
'10/26/2012 16:00:00	28.34', \
'10/31/2012 16:00:00	Missing_16', \
'11/1/2012 16:00:00	29.56', \
'11/2/2012 16:00:00	29.77', \
'11/5/2012 16:00:00	29.74', \
'11/6/2012 16:00:00	Missing_17', \
'11/7/2012 16:00:00	29.825', \
'11/8/2012 16:00:00	29.37', \
'11/9/2012 16:00:00	29.19', \
'11/12/2012 16:00:00	29.01', \
'11/13/2012 16:00:00	Missing_18', \
'11/14/2012 16:00:00	27.29', \
'11/15/2012 16:00:00	26.97', \
'11/16/2012 16:00:00	Missing_19', \
'11/19/2012 16:00:00	26.8', \
'11/20/2012 16:00:00	26.8', \
'11/21/2012 16:00:00	27.1666', \
'11/23/2012 13:00:00	27.77', \
'11/26/2012 16:00:00	27.58', \
'11/27/2012 16:00:00	27.38', \
'11/28/2012 16:00:00	27.39', \
'11/29/2012 16:00:00	27.36', \
'11/30/2012 16:00:00	27.13', \
'12/3/2012 16:00:00	26.82', \
'12/4/2012 16:00:00	26.63', \
'12/5/2012 16:00:00	26.93', \
'12/6/2012 16:00:00	26.98', \
'12/7/2012 16:00:00	26.82', \
'12/10/2012 16:00:00	26.97', \
'12/11/2012 16:00:00	27.49', \
'12/12/2012 16:00:00	27.62', \
'12/13/2012 16:00:00	Missing_20', \
'12/14/2012 16:00:00	27.13', \
'12/17/2012 16:00:00	27.215', \
'12/18/2012 16:00:00	27.63', \
'12/19/2012 16:00:00	27.73', \
'12/20/2012 16:00:00	27.68', \
'12/21/2012 16:00:00	27.49', \
'12/24/2012 13:00:00	27.25', \
'12/26/2012 16:00:00	27.2', \
'12/27/2012 16:00:00	27.09', \
'12/28/2012 16:00:00	26.9', \
'12/31/2012 16:00:00	26.77']

readings_count = 250
readings = []
for i in range(readings_count):
    readings_item = my_readings[i]
    readings.append(readings_item)

def calcMissing(readings):

    import tensorflow as tf
    import numpy

    n_missing_data = 20
    n_days_input = 10 # n cells (days) per input layer


    ################################################################################
    ## helper functions

    # extract middle measure from an 11-day input array to use as its label, in training and validation
    def parse_input_array(input_array):

        keys = sorted(list(input_array.keys()))
        full_length = len(keys)

        input_array_parsed = dict()

        # choose a random "key", i.e. the measure that will be used as label and the surrounding -+5 measures fed to the NN
        random_idx = [0]
        while random_idx[0]<=4 or random_idx[0]>=(keys[full_length-5]):
            random_idx = random.sample(keys, 1)    

        true_random_idx = random_idx[0]

        ord_random_idx = keys.index(true_random_idx)

        surrounding_idcs = [x for x in [keys[ord_random_idx-5], keys[ord_random_idx-4], keys[ord_random_idx-3], keys[ord_random_idx-2], keys[ord_random_idx-1],\
                                        keys[ord_random_idx], \
                                        keys[ord_random_idx+1], keys[ord_random_idx+2], keys[ord_random_idx+3], keys[ord_random_idx+4], keys[ord_random_idx+5]]]

        for idx in surrounding_idcs:
            input_array_parsed[idx] = input_array[idx]

        input_label = input_array_parsed[true_random_idx]

        # remove label day from input array
        del input_array_parsed[true_random_idx]

        input_array_parsed = list(input_array_parsed.values())

        return input_array_parsed, input_label


    ##################################################################################################
    ## parse input

    measures_done = dict()
    measures_missing = dict()

    for i,measure in enumerate(readings):

        measure_split = measure.split('\t')

        # time_seconds = int(mktime(datetime.strptime(measure_split[0],
        #                                             "%m/%d/%Y %H:%M:%S").timetuple()))
        level = measure_split[1]

        is_measured = True
        try:
           float(level)
        except ValueError:
           is_measured = False

        if is_measured:
            measures_done[i] = float(level)
        else:
            measures_missing[i] = level


    ## split training and validation data (50%-50%) ; assume that both halves have similar patterns
    # later, will split each into 11-day input arrays, with the value to infer in the middle stored as label, and removed from the input array (so input array has 10 cells)
    length_measures_done = len(measures_done)
    training_data = dict(list(measures_done.items())[:round(length_measures_done/2)])
    validation_data = dict(list(measures_done.items())[round(length_measures_done/2):])


    ## split measures_missing into 20 input arrays, with the missing value in the center and surrounded by the -5 and +5 days
    missing_dict = dict()

    for missing_idx in measures_missing:

        # track which Missing measure this is, e.g. Missing_15
        Missing_n = measures_missing[missing_idx] 
        missing_dict[Missing_n] = []

        ## recover -5 and +5 days around the missing value, from measures_done
        days_before, days_after = [], []

        all_days_before = list(range(0, (missing_idx)))
        all_days_before.reverse()
        for day in all_days_before:
            if day==0:
                # if finished values to the left, try with a few from the end of the measurements list
                for day in [len(measures_done)+x for x in all_days_before]:
                    if len(days_before)==5:
                        break
                    else:
                        try:
                            measures_done[day]
                            # if exists, append
                            days_before.append(day)
                        except KeyError:
                            pass  
            if len(days_before)==5:
                break    
            else:
                try:
                    measures_done[day]
                    # if exists, append
                    days_before.append(day)
                except KeyError:
                    pass

        all_days_after = list(range((missing_idx+1), (length_measures_done + n_missing_data)))
        for day in all_days_after:
            if day==(length_measures_done + n_missing_data):
            # if finished values to the right, try with a few from the beginning of the measurements list
                for day in [x - len(measures_done) for x in all_days_after]:
                    if len(days_before)==5:
                        break
                    else:
                        try:
                            measures_done[day]
                            # if exists, append
                            days_before.append(day)
                        except KeyError:
                            pass         
            if len(days_after)==5:
                break    
            else:
                try:
                    measures_done[day]
                    # if exists, append
                    days_after.append(day)
                except KeyError:
                    pass
        for day in sorted(days_before) + sorted(days_after):
            missing_dict[Missing_n].append(measures_done[day])       

        # I assume they will be printed in order (from 1 to 20)
        missing_arrays = list(missing_dict.values())


    ###############################################################################
    ## set up NN
    n_neurons_hidden = 150
    dropout = 0

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.InputLayer(input_shape = (n_days_input,)))
    model.add(tf.keras.layers.Dense(n_neurons_hidden,
                                    activation='relu'))
    model.add(tf.keras.layers.Dense(1, 
                                    activation='sigmoid')) # sigmoid for final probability between 0 and 1

    model.add(tf.keras.layers.Dropout(dropout))

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.MeanSquaredError())


    #### training and validation
    n_batch = 20
    n_epochs = 1
    n_iters = 10000
    training_arrays_batch, training_labels_batch, validation_arrays_batch, validation_labels_batch = [],[],[],[]

    ## generate training and validation sets
    for i in range(0, n_batch*n_iters):
        # at each n_iters-th iteration generate n_batch × training arrays and n_batch × validation arrays

        array_training, label_training = parse_input_array(training_data)
        training_arrays_batch.append(array_training)
        training_labels_batch.append(label_training)

        array_validation, label_validation = parse_input_array(validation_data)
        validation_arrays_batch.append(array_validation)
        validation_labels_batch.append(label_validation)

    # to numpy array -- and values scaled so between [0,1)
    scaling_max_val = max(list(measures_done.values())) + 0.01 # +0.01 so there are no 1's
    training_arrays_batch = numpy.array(training_arrays_batch) / scaling_max_val
    training_labels_batch = numpy.array(training_labels_batch) / scaling_max_val

    validation_arrays_batch = numpy.array(validation_arrays_batch) / scaling_max_val
    validation_labels_batch = numpy.array(validation_labels_batch) / scaling_max_val

    ## fit model
    model.fit(training_arrays_batch, training_labels_batch, epochs=n_epochs, batch_size=n_batch, verbose=0)

    # eval accuracy
    validation_loss = model.evaluate(validation_arrays_batch, validation_labels_batch, verbose=0)
    #print('\nValidation loss:', validation_loss)

    ### predict missing values
    for missing in missing_arrays:

        if len(missing) < n_days_input:

            n_days_needed = n_days_input - len(missing) 

            days_replace = missing[0:n_days_needed]

            missing = missing + days_replace

        missing_array = numpy.expand_dims(numpy.array(missing)/scaling_max_val,0)
        prediction = round(float(model.predict(missing_array)[0]) * scaling_max_val, 2)
        print(prediction)

        
calcMissing(readings)
