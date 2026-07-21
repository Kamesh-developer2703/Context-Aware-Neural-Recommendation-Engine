from sklearn.preprocessing import LabelEncoder, MinMaxScaler

def encode_column(df, column):
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column].astype(str))
    return df

def scale_columns(df, columns):
    scaler = MinMaxScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df