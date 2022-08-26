from asyncore import write
from typing import List
import pandas as pd
import os
import time
import shutil
import graphviz
import matplotlib.image as plt_img
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz, export_text
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from chefboost import Chefboost as chef
from agosuirpa.system_configuration import sep, decision_foldername
# import json
# import sys
# from django.shortcuts import render
# import seaborn as sns
# from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# def clean_dataset(df):
#     assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
#     df.dropna(inplace=True)
#     indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
#     return df[indices_to_keep].astype(np.float64)


# Create your views here.
def flat_dataset_row(data, columns, param_timestamp_column_name, param_variant_column_name, columns_to_drop, param_decision_point_activity, actions_columns):
    """
    Con esta función convertimos el log en un dataset, de manera que aplanamos todos los registros que existan sobre un mismo caso,
    resultando una sola fila por cada caso. Para este aplanamiento solamente se tienen en cuenta los registros relativos a las actividades
    anteriores a la indicada en param_decision_point_activity, incluyendo a esta última. Se concatena el nombre de las columnas de las actividades
    con su identificación, por ejemplo, timestamp_A, timestamp_B, etc.

    :data: map cuyas claves corresponden con el identificador de cada cado y cuyos valores son cada actividad asociada a dicho caso, con su información asociada
    :type data: map
    :columns: nombre de las columnas del dataset que se quieren almacenar para cada actividad
    :type columns: list
    :param_timestamp_column_name: nombre de la columna donde se almacena el timestamp
    :type param_timestamp_column_name: str
    :param_variant_column_name: nombre de la columna donde se almacena la variante, que será la etiqueta de nuestro problema
    :type param_variant_column_name: str
    :columns_to_drop: nombre de las columnas a eliminar del dataset
    :type columns_to_drop: list
    :param_decision_point_activity: identificador de la actividad inmediatamente anterior al punto de decisión cuyo por qué se quiere descubrir
    :type param_decision_point_activity: str
    """
    add_case = False  # Set True to add case column
    df_content = []
    new_list = [col_name for col_name in columns if col_name not in actions_columns]
    for case in data["cases"]:
        # print(case)
        timestamp_start = data["cases"][case]["A"].get(
            key=param_timestamp_column_name)
        timestamp_end = data["cases"][case][param_decision_point_activity].get(
            param_timestamp_column_name)
        variant = data["cases"][case]["A"].get(key=param_variant_column_name)
        if add_case:
            row = [variant, case, timestamp_start,
                   timestamp_end]  # ADDING CASE COLUMN
            headers = ["Variant", "Case", "Timestamp_start", "Timestamp_end"]
        else:
            # WITHOUT CASE COLUMN
            row = [variant, timestamp_start, timestamp_end]
            headers = ["Variant", "Timestamp_start", "Timestamp_end"]
        for act in data["cases"][case]:
            # case
            # variant_id
            if act != param_decision_point_activity:
                # A todas las columnas les añado el sufijo con la letra de la actividad correspondiente
                row.extend(data["cases"][case][act].drop(
                    columns_to_drop).values.tolist())
                for c in columns:
                    headers.append(c+"_"+act)
            else:
                row.extend(data["cases"][case][act].drop(
                    columns_to_drop).drop(actions_columns).values.tolist())
                for c in new_list:
                    headers.append(c+"_"+act)
                break
        # Introducimos la fila con la información de todas las actividades del caso en el dataset
        df_content.append(row)
        # print(row)
        # print(headers)
    df = pd.DataFrame(df_content, columns=headers)
    return df


def extract_training_dataset(
        param_decision_point_activity, param_log_path="media/enriched_log_feature_extracted.csv", param_path_dataset_saved="media/", actions_columns=["Coor_X", "Coor_Y", "MorKeyb", "TextInput", "Click"], param_variant_column_name="Variant", param_case_column_name="Case", param_screenshot_column_name="Screenshot", param_timestamp_column_name="Timestamp", param_activity_column_name="Activity"):
    """
    Recorro cada fila del log:
        Por cada caso:
            Almaceno en un map todos los atributos de las actividades hasta llegar al punto de decisión
            Suponiendo que el punto de decisión estuviese en la actividad D,
            el map tendría la estructura:
        {
            "headers": ["timestamp", "MOUSE", "clipboard"...],
            "caso1":
                {"A": ["value1","value2","value3",...]}
                {"B": ["value1","value2","value3",...]}
                {"C": ["value1","value2","value3",...]},
            "caso2":
                {"A": ["value1","value2","value3",...]}
                {"B": ["value1","value2","value3",...]}
                {"C": ["value1","value2","value3",...]},...
        }

    Una vez generado el map, para cada caso, concatenamos el header con la actividad para nombrar las columnas y asignamos los valores
    Para cada caso se genera una fila nueva en el dataframe
    """

    log = pd.read_csv(param_log_path, sep=",", index_col=0)

    cases = log.loc[:, param_case_column_name].values.tolist()
    actual_case = 0

    log_dict = {"headers": list(log.columns), "cases": {}}
    for index, c in enumerate(cases, start=0):
        if c == actual_case:
            activity = log.at[index, param_activity_column_name]
            if c in log_dict["cases"]:
                log_dict["cases"][c][activity] = log.loc[index, :]
            else:
                log_dict["cases"][c] = {activity: log.loc[index, :]}
        else:
            activity = log.at[index, param_activity_column_name]
            log_dict["cases"][c] = {activity: log.loc[index, :]}
            actual_case = c

    # import p#print
    # pprint.pprint(log_dict)

    # Serializing json
    # json_object = json.dumps(log_dict, indent = 4)

    # Writing to sample.json
    # with open(param_path_dataset_saved + "preprocessed_log.json", "w") as outfile:
    #     outfile.write(json_object)

    columns_to_drop = [param_case_column_name, param_activity_column_name,
                       param_timestamp_column_name, param_screenshot_column_name, param_variant_column_name]
    columns = list(log.columns)
    for c in columns_to_drop:
        columns.remove(c)

    # Establecemos columnas comunes y al resto de columnas se le concatena el "_" actividad
    data_flattened = flat_dataset_row(log_dict, columns, param_timestamp_column_name,
                                      param_variant_column_name, columns_to_drop, param_decision_point_activity, actions_columns)
    # print(data_flattened)
    data_flattened.to_csv(param_path_dataset_saved +
                          "preprocessed_dataset.csv")


# https://gist.github.com/j-adamczyk/dc82f7b54d49f81cb48ac87329dba95e#file-graphviz_disk_op-py
def plot_decision_tree(path: str,
                       clf: DecisionTreeClassifier,
                       feature_names: List[str],
                       class_names: List[str]) -> np.ndarray:
    # 1st disk operation: write DOT
    export_graphviz(clf, out_file=path+".dot",
                    feature_names=feature_names,
                    class_names=class_names,
                    label="all", filled=True, impurity=False,
                    proportion=True, rounded=True, precision=2)

    # 2nd disk operation: read DOT
    graph = graphviz.Source.from_file(path + ".dot")

    # 3rd disk operation: write image
    graph.render(path, format="png")

    # 4th disk operation: read image
    image = plt_img.imread(path + ".png")

    # 5th and 6th disk operations: delete files
    os.remove(path + ".dot")
    # os.remove("decision_tree.png")

    return image

def chefboost_decision_tree(param_preprocessed_log_path, param_path, algorithms, columns_to_ignore):
    flattened_dataset = pd.read_csv(param_preprocessed_log_path, index_col=0, sep=',')
    target_label = 'Variant'
    times = {}
    param_path += decision_foldername + sep
    if not os.path.exists(param_path):
        os.mkdir(param_path)
    one_hot_cols = []

    for c in flattened_dataset.columns:
        if "NameApp" in c:
            one_hot_cols.append(c)
        elif "TextInput" in c:
            columns_to_ignore.append(c)  # TODO: get type of field using NLP: convert to categorical variable (conversation, name, email, number, date, etc)
            
    flattened_dataset = pd.get_dummies(flattened_dataset, columns=one_hot_cols)
    flattened_dataset = flattened_dataset.drop(columns_to_ignore, axis=1)
    flattened_dataset = flattened_dataset.fillna(0.)
    # Splitting dataset
    # X_train, X_test = train_test_split(flattened_dataset, test_size=0.2, random_state=42, stratify=flattened_dataset[target_label])
    
    for alg in list(algorithms):
        df = flattened_dataset
        df.rename(columns = {target_label:'Decision'}, inplace = True)
        df['Decision'] = df['Decision'].astype(object) # which will by default set the length to the max len it encounters
        config = {'algorithm': alg, 'enableParallelism': True, 'num_cores': 2, 'max_depth': 5}
        times[alg] = {"start": time.time()}
        chef.fit(df, config = config)
        times[alg]["finish"] = time.time()
        # TODO: accurracy_score -> store evaluate terminar output
        # model = chef.fit(df, config = config)
        # output = subprocess.Popen( [chef.evaluate(model,df)], stdout=subprocess.PIPE ).communicate()[0]
        # file = open(param_path+alg+'-results.txt','w')
        # file.write(output)
        # file.close()
        # Saving model
        # model = chef.fit(df, config = config, target_label = 'Variant')
        # chef.save_model(model, alg+'model.pkl')
        # TODO: feature importance
        # fi = chef.feature_importance('outputs/rules/rules.py').set_index("feature")
        # fi.to_csv(param_path+alg+"-tree-feature-importance.csv")
        # TODO: Graphical representation of feature importance
        # fi.plot(kind="barh", title="Feature Importance")
        shutil.move('outputs/rules/rules.py', param_path+alg+'-rules.py')
        shutil.move('outputs/rules/rules.json', param_path+alg+'-rules.json')
    accuracy_score = 100
    return accuracy_score, times

def CART_sklearn_decision_tree(param_preprocessed_log_path, param_path, autogeneration):
    df = pd.read_csv(param_preprocessed_log_path, index_col=0, sep=',')

    one_hot_cols = []
    text_cols = []
    for c in df.columns:
        if "NameApp" in c:
            one_hot_cols.append(c)
        elif "TextInput" in c:
            text_cols.append(c)

    # print("\n\nColumns to drop: ")
    # print(one_hot_cols)
    # print(text_cols)

    # for c in one_hot_cols:
    #  df[c] = df[c].map(dict(zip(['Firefox','CRM'],[0,1])))
    df = pd.get_dummies(df, columns=one_hot_cols)
    df = df.drop(text_cols, axis=1)
    df = df.fillna(0.)

    # np.any(np.isnan(df))
    # np.isnan(df)
    # np.all(np.isfinite(df))

    X = df.drop('Variant', axis=1)
    y = df[['Variant']]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1,random_state=42)

    # criterion="gini", random_state=42,max_depth=3, min_samples_leaf=5)
    clf_model = DecisionTreeClassifier()
    # clf_model = RandomForestClassifier(n_estimators=100)
    clf_model.fit(X, y)  # change train set. X_train, y_train

    y_predict = clf_model.predict(X)  # X_test

    # # print("\nTest dataset: ")
    # # print(X_test)
    # # print("\nCorrect labels: ")
    # # print(y_test)
    # # print("\nTest dataset predictions: ")
    # # print(y_predict)
    # print("\n\nAccuracy_score")
    # print(accuracy_score(y_test,y_predict))

    target = list(df['Variant'].unique())
    feature_names = list(X.columns)

    target_casted = [str(t) for t in target]

    # estimator = clf_model.estimators_[5]

    # export_graphviz(estimator, out_file='tree.dot',
    #                 feature_names = feature_names,
    #                 class_names = target_casted,
    #                 rounded = True, proportion = False,
    #                 precision = 2, filled = True)

    # # Convert to png using system command (requires Graphviz)
    # from subprocess import call
    # call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])

    # # Display in jupyter notebook
    # from IPython.display import Image
    # Image(filename = 'tree.png')

    text_representation = export_text(clf_model, feature_names=feature_names)
    print("\n\nDecision Tree Text Representation")
    print(text_representation)

    with open(param_path + "decision_tree.log", "w") as fout:
        fout.write(text_representation)

    type(target_casted[0])

    if not autogeneration == 'autogeneration':
        img = plot_decision_tree(
            param_path + "decision_tree", clf_model, feature_names, target_casted)
        plt.imshow(img)
        plt.show()

    return accuracy_score(y, y_predict)


def decision_tree_training(param_preprocessed_log_path="media/preprocessed_dataset.csv", param_path="mdia/", implementation="sklearn", autogeneration="autogeneration", algorithms=['ID3', 'CART', 'CHAID', 'C4.5'], columns_to_ignore=["Timestamp_start", "Timestamp_end"]):
    if implementation == 'sklearn':
        return CART_sklearn_decision_tree(param_preprocessed_log_path, param_path, autogeneration, columns_to_ignore)
    else:
        return chefboost_decision_tree(param_preprocessed_log_path, param_path, algorithms, columns_to_ignore)

def decision_tree_predict(module_path, instance):
    """
    moduleName = "outputs/rules/rules" #this will load outputs/rules/rules.py
    instance = for example ['Sunny', 'Hot', 'High', 'Weak']
    """
    tree = chef.restoreTree(module_path)
    prediction = tree.findDecision(instance)
    return prediction