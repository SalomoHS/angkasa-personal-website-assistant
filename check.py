from pinecone import Pinecone
print(f"Lokasi file pinecone: {Pinecone.__file__}")
try:
    from pinecone import Pinecone
    print("Berhasil impor class Pinecone!")
except ImportError as e:
    print(f"Gagal: {e}")