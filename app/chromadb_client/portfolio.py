
import chromadb
import uuid

class portfolio:
    def __init__(self):
        self.chroma_client =chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name = 'portfolio')

    def add_project(self, user_id, link, stack):
        self.collection.add(
            documents=[stack],
            metadatas={"links": link, "user_id": user_id},
            ids=[str(uuid.uuid4())]
        )
        return {"message": "added new project"}

    def get_all_project(self, user_id):
        response = self.collection.get(where={"user_id": user_id})
        return response

    def query_user_projects(self, skills, user_id):
        """Query projects based on skills and filter by user_id."""
        results = self.collection.query(
            query_texts=[skills],
            n_results=2,
            where={"user_id": user_id}  # Filter results by user_id
        )
        return results
