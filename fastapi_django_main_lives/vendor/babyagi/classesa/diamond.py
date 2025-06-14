import psycopg2
from sentence_transformers import SentenceTransformer
from fastapi import APIRouter, HTTPException
import os



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
            cursor.execute("UPDATE diamondprice SET vector_col = %s WHERE id = %s", (vector, product_id))
            self.conn.commit()

    def search_similar_vectors(self, query_text, top_k=10):
        query_vector = self.get_embedding(query_text).tolist()  # ndarray をリストに変換
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT id,price,carat, cut, color, clarity, depth, diamondprice.table, x, y, z, vector_col <=> %s::vector AS distance
                FROM diamondprice
                WHERE vector_col IS NOT NULL
                ORDER BY distance asc
                LIMIT %s;
            """, (query_vector, top_k))
            results = cursor.fetchall()
            return results

    def search_similar_all(self, query_text, top_k=5):
        query_vector = self.get_embedding(query_text).tolist()  # ndarray をリストに変換
        with self.conn.cursor() as cursor:
            cursor.execute("""
                SELECT id,carat, cut, color, clarity, depth, diamondprice.table, x, y, z
                FROM diamondprice
                order by id asc
                limit 10000000
            """, (query_vector, top_k))
            results = cursor.fetchall()
            return results      

def create_index():
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
        query_text="1"
        results = db.search_similar_all(query_text)
        print("Search results:")
        DEBUG=1
        if DEBUG==1:
            for result in results:
                print(result) 
                id = result[0]
                sample_text = str(result[1])+str(result[2])+str(result[3])+str(result[4])+str(result[5])+str(result[6])+str(result[7])+str(result[8])+str(result[9])
                print(sample_text)
                db.insert_vector(id, sample_text) 
        #return
        # サンプルデータの挿入
        #sample_text = """"""
        #sample_product_id = 1  # 実際の製品IDを使用
        #db.insert_vector(sample_product_id, sample_text)
        #db.insert_vector(2, sample_text)

        #print(f"Vector inserted for product ID {sample_product_id}.")

        
        # ベクトル検索
        query_text = "2.03Very GoodJSI262.058.08.068.125.05"

        query_text = "2.03Very GoodJSI2"
        #query

        #query_text = "2.03-Very Good-J-SI2-62.2-58.0-7.27-7.33-4.55"
        results = db.search_similar_vectors(query)#query_text)
        res_all = ""
        print("Search results:")
        for result in results:
            print(result)
            res_all += str(result)+"\r\n"
        return res_all
    
    finally:
        # 接続を閉じる
        db.close()    


def calculate(query):
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
        query_text="1"
        results = db.search_similar_all(query_text)
        print("Search results:")
        DEBUG=0
        if DEBUG==1:
            for result in results:
                print(result) 
                id = result[0]
                sample_text = str(result[1])+str(result[2])+str(result[3])+str(result[4])+str(result[5])+str(result[6])+str(result[7])+str(result[8])+str(result[9])
                print(sample_text)
                db.insert_vector(id, sample_text) 
        #return
        # サンプルデータの挿入
        #sample_text = """"""
        #sample_product_id = 1  # 実際の製品IDを使用
        #db.insert_vector(sample_product_id, sample_text)
        #db.insert_vector(2, sample_text)

        #print(f"Vector inserted for product ID {sample_product_id}.")

        
        # ベクトル検索
        query_text = "2.03Very GoodJSI262.058.08.068.125.05"

        query_text = "2.03Very GoodJSI2"
        #query

        #query_text = "2.03-Very Good-J-SI2-62.2-58.0-7.27-7.33-4.55"
        results = db.search_similar_vectors(query)#query_text)
        res_all = ""
        print("Search results:")
        for result in results:
            print(result)
            res_all += str(result)+"\r\n"
        return res_all
    
    finally:
        # 接続を閉じる
        db.close()


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
        query_text="1"
        results = db.search_similar_all(query_text)
        print("Search results:")
        DEBUG=0
        if DEBUG==1:
            for result in results:
                print(result) 
                id = result[0]
                sample_text = str(result[1])+str(result[2])+str(result[3])+str(result[4])+str(result[5])+str(result[6])+str(result[7])+str(result[8])+str(result[9])
                print(sample_text)
                db.insert_vector(id, sample_text) 
        #return
        # サンプルデータの挿入
        #sample_text = """"""
        #sample_product_id = 1  # 実際の製品IDを使用
        #db.insert_vector(sample_product_id, sample_text)
        #db.insert_vector(2, sample_text)

        #print(f"Vector inserted for product ID {sample_product_id}.")

        
        # ベクトル検索
        query_text = "2.03Very GoodJSI262.058.08.068.125.05"

        query_text = "2.03Very GoodJSI2"

        #query_text = "2.03-Very Good-J-SI2-62.2-58.0-7.27-7.33-4.55"
        results = db.search_similar_vectors(query_text)
        res_all = ""
        print("Search results:")
        for result in results:
            print(result)
            res_all += result+""
    
    finally:
        # 接続を閉じる
        db.close()

if __name__ == "__main__":
    main()
