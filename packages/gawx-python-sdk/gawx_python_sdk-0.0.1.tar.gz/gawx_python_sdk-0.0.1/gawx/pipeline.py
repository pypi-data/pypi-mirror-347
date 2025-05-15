from gawx.apis import get_session, create_pipeline, run_pipeline, get_pipeline

class Pipeline:
    def __init__(self, pipeline_id=None, session_id=None, vector_db_id=None, data_sources=None):
        """
        Initialize the pipeline
        """
        self.pipeline_id = pipeline_id
        self.session_id = session_id
        self.vector_db_id = vector_db_id
        self.data_sources = data_sources
        self.pipeline = None
        
        if self.pipeline_id is None:
            self.__create()
        else:
            self.__get()
        
    def __create(self):
        """
        Create the pipeline
        """
        response = create_pipeline(self.session_id, self.vector_db_id, self.data_sources)
        if response.get("status") == "success":
            self.pipeline = response.get("data")
            self.pipeline_id = self.pipeline.get("id")
            return self.pipeline
        else:
            return None 
        
    def __get(self):
        """
        Get the pipeline
        """
        response = get_pipeline(self.pipeline_id)
        if response.get("status") == "success":
            self.pipeline = response.get("data")
            return self.pipeline
        else:
            return None
        
    def run(self):
        """
        Run the pipeline
        """
        response = run_pipeline(self.pipeline.get("id"))
        if response.get("status") == "success":
            self.pipeline = response.get("data")
        else:
            raise Exception(response.get("message"))
        
        return self.pipeline
        
    def get(self):
        """
        Get the pipeline
        """
        response = get_pipeline(self.pipeline.get("id"))
        if response.get("status") == "success":
            self.pipeline = response.get("data")
        else:
            raise Exception(response.get("message"))
        
        return self.pipeline

    def get_status(self):
        """
        Get the status of the pipeline
        """
        # get pipeline again
        self.__get()
        return self.pipeline.get("status")
    
    def get_response(self):
        """
        Get the response of the pipeline
        """
        # get pipeline again
        self.__get()
        return self.pipeline.get("response")
