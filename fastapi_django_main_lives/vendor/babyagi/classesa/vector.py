import psycopg2
from sentence_transformers import SentenceTransformer

class ProductDatabase:
    def __init__(self, database_url):
        self.database_url = database_url
        self.conn = None
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def connect(self):
        self.conn = psycopg2.connect(self.database_url)
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def setup_vector_extension_and_column(self):
        with self.conn.cursor() as cursor:
            # pgvector拡張機能のインストール
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # ベクトルカラムの追加
            cursor.execute("ALTER TABLE products ADD COLUMN IF NOT EXISTS vector_col vector(384);")
            
            self.conn.commit()

    def get_embedding(self, text):
        embedding = self.model.encode(text)
        return embedding

    def insert_vector(self, product_id, text):
        vector = self.get_embedding(text).tolist()  # ndarray をリストに変換
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE products SET vector_col = %s WHERE id = %s", (vector, product_id))
            self.conn.commit()

    def search_similar_vectors(self, query_text, top_k=5):
        query_vector = self.get_embedding(query_text).tolist()  # ndarray をリストに変換
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, vector_col <=> %s::vector AS distance
                FROM products
                ORDER BY distance
                LIMIT %s;
            """, (query_vector, top_k))
            results = cursor.fetchall()
            return results

def main():
    # データベース接続情報
    DATABASE_URL = os.getenv("postgre_url")
    
    # ProductDatabaseクラスのインスタンスを作成
    db = ProductDatabase(DATABASE_URL)
    
    # データベースに接続
    db.connect()
    
    try:
        # pgvector拡張機能のインストールとカラムの追加
        db.setup_vector_extension_and_column()
        print("Vector extension installed and column added successfully.")
        
        # サンプルデータの挿入
        sample_text = """検査にはどのぐらい時間かかりますか？⇒当日に分かります。
法人取引やってますか？⇒大丈夫ですよ。成約時に必要な書類の説明
LINEで金粉送って、査定はできますか？⇒できますが、今お話した内容と同様で、検査が必要な旨を返すだけなので、金粉ではなく、他のお品物でLINE査定くださいと。
分かりました、またどうするか検討して連絡しますと"""
        sample_product_id = 1  # 実際の製品IDを使用
        db.insert_vector(sample_product_id, sample_text)
        db.insert_vector(2, sample_text)

        print(f"Vector inserted for product ID {sample_product_id}.")

        
        # ベクトル検索
        query_text = "今お話した内容と同様で"
        results = db.search_similar_vectors(query_text)
        print("Search results:")
        for result in results:
            print(result)
    
    finally:
        # 接続を閉じる
        db.close()

if __name__ == "__main__":
    main()
