import tensorflow as tf
from transformers import TFBertModel, BertTokenizer
from tensorflow.keras import layers

class AttentionLayer(layers.Layer):
    """
    Mecanismo de Atenção customizado para focar em partes 
    relevantes da sequência (ex: termos de desmotivação).
    """
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", 
                                shape=(input_shape[-1], 1),
                                initializer="normal")
        self.b = self.add_weight(name="att_bias", 
                                shape=(input_shape[1], 1),
                                initializer="zeros")
        super(AttentionLayer, self).build(input_shape)

    def call(self, x):
        e = tf.keras.backend.tanh(tf.keras.backend.dot(x, self.W) + self.b)
        a = tf.keras.backend.softmax(e, axis=1)
        output = x * a
        return tf.keras.backend.sum(output, axis=1)

def build_hybrid_model(max_seq_len=128):
    """
    Constrói a arquitetura Híbrida: BERT + BiLSTM + Attention (TensorFlow/Keras).
    """
    # 1. Entrada de IDs do BERT
    input_ids = layers.Input(shape=(max_seq_len,), dtype=tf.int32, name="input_ids")
    attention_mask = layers.Input(shape=(max_seq_len,), dtype=tf.int32, name="attention_mask")

    # 2. Camada BERT (Modelo de Base)
    bert_model = TFBertModel.from_pretrained("bert-base-multilingual-uncased")
    # Congelamos o BERT inicialmente para manter os pesos contextuais estáveis
    bert_model.trainable = False
    
    bert_output = bert_model(input_ids, attention_mask=attention_mask)[0] # Sequence Output

    # 3. Camada Bi-LSTM (Dependências Sequenciais)
    bilstm = layers.Bidirectional(layers.LSTM(64, return_sequences=True))(bert_output)
    
    # 4. Camada de Atenção (Foco no TEA)
    attention = AttentionLayer()(bilstm)

    # 5. Camadas Densas e Saída de Sentimento (3 classes: Pos, Neu, Neg)
    dropout = layers.Dropout(0.3)(attention)
    dense = layers.Dense(32, activation="relu")(dropout)
    output = layers.Dense(3, activation="softmax", name="sentiment_output")(dense)

    model = tf.keras.Model(inputs=[input_ids, attention_mask], outputs=output)
    
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=2e-5),
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    
    return model

# Mock do modelo para o Módulo Experimental
def get_model_summary_scientific():
    """Retorna os dados estatísticos conforme o artigo para exibição no dashboard."""
    return {
        "models": ["LSTM", "GRU", "BERT", "RoBERTa", "Híbrido (BERT+BiLSTM+Att)"],
        "f1_scores": [0.85, 0.87, 0.92, 0.94, 0.97],
        "recall": [0.82, 0.84, 0.90, 0.91, 0.96],
        "precision": [0.86, 0.88, 0.93, 0.95, 0.98]
    }
